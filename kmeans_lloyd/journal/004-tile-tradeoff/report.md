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

## What is being measured

Feature-heavy, the shape from 003: 65536 samples, 4096 centroids, 16384 features, float32, TF32 off. Eager and `torch.compile` Gram tiles:

| tile samples | tile centroids |
| --- | --- |
| 256 | 4096 |
| 1024 | 4096 |
| 4096 | 4096 |
| 65536 | 4096 |
| 4096 | 1024 |
| 4096 | 256 |
| 1024 | 1024 |
| 1024 | 256 |

256 is the Cython chunk length. 65536×4096 is one GEMM for the whole problem. A running-tile sweep (`tile_k` 16, 32, 64, 128, 256), a profile of the kernels, one tiled Lloyd step, k-means++, and the Cython iteration on a smaller shared problem (65536×1024×2048) follow the tile table.

## Cython timing

Same host as the GPU runs. One dense iteration on 65536 samples, 1024 centroids, 2048 features, float32. Chunk length 256. Median of 3 calls after one warmup. The assignment call sets `update_centers=False`. The Lloyd call also updates centers and relocates empty clusters.

| call | median | notes |
| --- | --- | --- |
| assignment | 1.437 s | 2 of 65536 labels differ from a NumPy centers-only argmin |
| full Lloyd iteration | 1.526 s | assignment plus the center update |

The thread-local distance tiles and center buffers are 36.0 MiB together (`4` threads times a 256 by 1024 distance tile, plus the center sums). Process `ru_maxrss` after the run was 1.63 GiB, which includes the 512 MiB sample matrix. The matching PyTorch `lloyd_step` on this shape is not timed yet.

## Progress

- Array-API tile assignment, tiled update, and k-means++ are in the tree. CPU tests cover tiles that do not divide the problem, the tiled mean, and a k-means++ draw that must pick the far cluster.
- Cython numbers above are in. The feature-heavy Gram tile sweep on the L4 is running.
