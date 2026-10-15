# 004 — tile sizes, a Cython Lloyd step, and k-means++

The compiled running tile from [003](../003-resized-shapes/index.html) removes the distance matrix and is slower than the Gram GEMM. This iteration asks three things:

- How sample-tile and centroid-tile sizes move the speed and memory of a Gram assignment.
- Whether that tiled Gram step, after profiling, gets closer to a chunked GEMM Lloyd iteration.
- What k-means++ initialization costs in the same array-API code.

The core functions stay in Python array-API syntax and run without `torch.compile`. The compiler, when used, is wrapped around those functions by the benchmark driver.

## Schedules added

| piece | source |
| --- | --- |
| centroid-norm scores, then argmin | [`gemm_scores_argmin`](https://github.com/ogrisel/cursor-sandbox/blob/cursor/kmeans-lloyd-fusion-8896/kmeans_lloyd/src/kmeans_lloyd/iteration.py#L240-L251) |
| Gram assignment over sample and centroid tiles | [`assign_gemm_tiled`](https://github.com/ogrisel/cursor-sandbox/blob/cursor/kmeans-lloyd-fusion-8896/kmeans_lloyd/src/kmeans_lloyd/iteration.py#L253-L286) |
| mean update with a `(n, tile_k)` one-hot | [`update_centroids_tiled`](https://github.com/ogrisel/cursor-sandbox/blob/cursor/kmeans-lloyd-fusion-8896/kmeans_lloyd/src/kmeans_lloyd/iteration.py#L288-L309) |
| one Lloyd step using those two tiles | [`lloyd_step`](https://github.com/ogrisel/cursor-sandbox/blob/cursor/kmeans-lloyd-fusion-8896/kmeans_lloyd/src/kmeans_lloyd/iteration.py#L311-L329) |
| running tile that also merges the best distance | [`running_tile_update`](https://github.com/ogrisel/cursor-sandbox/blob/cursor/kmeans-lloyd-fusion-8896/kmeans_lloyd/src/kmeans_lloyd/iteration.py#L331-L342) |
| k-means++ | [`kmeans_plusplus`](https://github.com/ogrisel/cursor-sandbox/blob/cursor/kmeans-lloyd-fusion-8896/kmeans_lloyd/src/kmeans_lloyd/iteration.py#L365-L403) |

`||x||²` is omitted inside a tile because it does not change the argmin. That is the same reduction the Cython kernel uses. Centroid norms are computed once per centroid tile, then reused for every sample tile.

## Cython reference

The comparison target is [`lloyd_iter_chunked_dense`](https://github.com/cakedev0/scikit-learn/blob/kmeans/lloyd_no_blocking_sync/sklearn/cluster/_k_means_lloyd.pyx) from [cakedev0/scikit-learn#26](https://github.com/cakedev0/scikit-learn/pull/26). Each chunk has 256 samples. The chunk computes `||c||² - 2 X Cᵀ` with a GEMM, takes argmin, and scatters the samples into per-thread center buffers. Those buffers are reduced after the parallel region.

The branch is built on the L4 host as scikit-learn `1.10.dev0` (g++ 13.3). The host has 4 CPUs, so the iteration uses 4 threads.

## Gram tiles on feature-heavy

65536 samples, 4096 centroids, 16384 features, float32, TF32 off. Median of two calls after one warmup. Compile time is not included in the steady median. The first compiled tile took 9.0 s to compile; the others took 0.4–1.4 s.

| tile (samples x centroids) | eager | compiled |
| --- | --- | --- |
| 256 x 4096 | 1.078 s, 256.5 MiB | 1.091 s, 256.5 MiB |
| 1024 x 4096 | 0.918 s, 256.5 MiB | 0.940 s, 256.5 MiB |
| 4096 x 4096 | 0.940 s, 256.5 MiB | 0.939 s, 256.5 MiB |
| 65536 x 4096 | 0.967 s, 2.00 GiB | 0.950 s, 1.00 GiB |
| 4096 x 1024 | 0.946 s, 64.5 MiB | 0.928 s, 64.5 MiB |
| 4096 x 256 | 1.098 s, 16.5 MiB | 1.107 s, 16.5 MiB |
| 1024 x 1024 | 0.963 s, 64.5 MiB | 0.967 s, 64.5 MiB |
| 1024 x 256 | 1.302 s, 16.5 MiB | 1.333 s, 16.5 MiB |
| full Gram, including x norm | 1.042 s, 4.00 GiB | |

For every tile whose distance matrix is smaller than the centroid tile, the measured peak is `tile_k * 16384 * 4` bytes plus 528 KiB. That is one float32 copy of the centroid tile, the buffer a transposed GEMM needs, plus a fixed half megabyte. It does not grow with the sample tile. The 256-sample chunk used by the Cython kernel is the same 256.5 MiB as a 4096-sample tile when every centroid is in the product, and it is slightly slower (1.08 s against 0.92 s).

The distance matrix exceeds that copy only for the full 65536 by 4096 product, which is 1.00 GiB. Eager execution peaks at 2.00 GiB there. `torch.compile` leaves the 1.00 GiB product and drops the extra gigabyte. It does not change the steady time of the tiled products. The fastest compiled tile in this grid is 4096 by 1024: 0.928 s and 64.5 MiB, against 1.042 s and 4.00 GiB for the eager full Gram.

## Compiled running tiles

Same feature-heavy problem. One `torch.compile` block covers `tile_k` centroids, then the driver walks every centroid. Steady time excludes compile. `tiled` merges the running minimum outside the compiled block. `stateful` merges inside it. `tile_k` 256 was not run: at 128 the compile was already 28 s and the distance tile was back.

| tile centroids | tiled | stateful |
| --- | --- | --- |
| 16 | 6.84 s, 2.56 MiB, compile 4.0 s | 6.83 s, 1.50 MiB, compile 2.9 s |
| 32 | 5.98 s, 2.56 MiB, compile 6.1 s | 6.60 s, 1.50 MiB, compile 6.0 s |
| 64 | 10.10 s, 18.3 MiB, compile 13.0 s | 10.16 s, 17.5 MiB, compile 9.6 s |
| 128 | 10.19 s, 34.1 MiB, compile 27.7 s | 10.18 s, 33.3 MiB, compile 21.7 s |

At 16 and 32 the stateful peak is 1.50 MiB, two copies of the `n * 12` byte label-and-distance state. At 64 and 128 the peak jumps to the `(n, tile_k)` distance tile (16 MiB and 32 MiB) plus about 2 MiB, and the assignment gets slower. The fastest running schedule is the outside merge at 32 centroids: 5.98 s and 2.56 MiB. The fastest Gram tile, 0.928 s and 64.5 MiB, is still about six times faster.

Putting the merge inside the compiled block saves the extra copy at 16 and 32 and does not make the assignment faster. The kernel profile of these two schedules, the tiled centroid update, and k-means++ are still running.

## Cython timing

Same host as the GPU runs. One dense iteration on 65536 samples, 1024 centroids, 2048 features, float32. Chunk length 256. Median of 3 calls after one warmup. The assignment call sets `update_centers=False`. The Lloyd call also updates centers and relocates empty clusters.

| call | median | notes |
| --- | --- | --- |
| assignment | 1.437 s | 2 of 65536 labels differ from a NumPy centers-only argmin |
| full Lloyd iteration | 1.526 s | assignment plus the center update |

The thread-local distance tiles and center buffers are 36.0 MiB together (`4` threads times a 256 by 1024 distance tile, plus the center sums). Process `ru_maxrss` after the run was 1.63 GiB, which includes the 512 MiB sample matrix. The matching PyTorch `lloyd_step` on this shape is not timed yet.

## Progress

- Gram tiles and compiled running tiles are both in the tables above. `results.json` in this folder is the source.
- Cython Lloyd on 65536×1024×2048 is in. The same shape has not been timed with `lloyd_step` yet.
- The kernel profile, the tiled Lloyd update, and k-means++ are running on the L4.
