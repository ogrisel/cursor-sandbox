# 005 — full k-means against a Cython init and cuML

[004](../004-tile-tradeoff/index.html) left a tiled Gram Lloyd step and a k-means++ init in the array API. This iteration times the whole fit, then compares it with two optimized implementations:

- k-means++ from [cakedev0/scikit-learn#23](https://github.com/cakedev0/scikit-learn/pull/23) (`7e26a5c`, scikit-learn 1.10.dev0, 4 CPU threads).
- `cuml.cluster.KMeans` 26.10.00 on the same L4, `init="k-means++"`, `n_init=1`, `tol=1e-4`.

The core functions stay in Python array-API syntax. `torch.compile` is applied only in the benchmark, around the distance function and the Gram tile. The same functions run without that wrapper.

## What was added

| piece | source |
| --- | --- |
| k-means++ | [`kmeans_plusplus`](https://github.com/ogrisel/cursor-sandbox/blob/cursor/kmeans-lloyd-fusion-8896/kmeans_lloyd/src/kmeans_lloyd/iteration.py#L390-L432) |
| squared row norm, one feature tile at a time | [`_row_squared_norm`](https://github.com/ogrisel/cursor-sandbox/blob/cursor/kmeans-lloyd-fusion-8896/kmeans_lloyd/src/kmeans_lloyd/iteration.py#L522-L534) |
| one-hot update accumulated over sample tiles | [`update_centroids_tiled`](https://github.com/ogrisel/cursor-sandbox/blob/cursor/kmeans-lloyd-fusion-8896/kmeans_lloyd/src/kmeans_lloyd/iteration.py#L288-L324) |
| inertia over sample tiles | [`inertia`](https://github.com/ogrisel/cursor-sandbox/blob/cursor/kmeans-lloyd-fusion-8896/kmeans_lloyd/src/kmeans_lloyd/iteration.py#L435-L450) |
| mean feature variance over feature tiles | [`_mean_feature_variance`](https://github.com/ogrisel/cursor-sandbox/blob/cursor/kmeans-lloyd-fusion-8896/kmeans_lloyd/src/kmeans_lloyd/iteration.py#L508-L520) |
| init plus Lloyd until the center shift falls under the scaled tolerance | [`fit_kmeans`](https://github.com/ogrisel/cursor-sandbox/blob/cursor/kmeans-lloyd-fusion-8896/kmeans_lloyd/src/kmeans_lloyd/iteration.py#L453-L505) |

Empty clusters keep their previous center. scikit-learn relocates them. That difference did not show up on the separated blobs below: every sample received the same cluster as cuML, up to label permutation.

## Shape

The timing problem is standard normal data, float32, TF32 off: 131072 samples, 2048 features, 256 clusters. The matrix is 1.00 GiB. A second problem is 8 blobs in 32 dimensions (32768 samples, separation 12, noise 0.4) and is used only as a quality check. Both generators are NumPy `Generator` streams fixed in the scripts.

PyTorch peaks are bytes allocated above the input. cuML memory is the nvidia-smi device high-water, sampled every 50 ms, and it includes the input and the library context. Those two meters are not the same quantity.

## Tile size on this shape

One eager Lloyd step. The update one-hot covers every selected centroid (`tile_k` or 256, whichever is smaller) and, in this table, every sample. Median of two calls after one warmup.

| tile (samples x centroids) | time | peak above the input |
| --- | --- | --- |
| 1024 x 256 | 0.0356 s | 175.0 MiB |
| 4096 x 256 | 0.0303 s | 175.0 MiB |
| 16384 x 256 | 0.0296 s | 175.0 MiB |
| 65536 x 256 | 0.0295 s | 175.0 MiB |
| 131072 x 256 | 0.0315 s | 258.5 MiB |
| 4096 x 128 | 0.0317 s | 149.0 MiB |
| 4096 x 64 | 0.0439 s | 76.0 MiB |
| 4096 x 32 | 0.0735 s | 39.5 MiB |

Time is flat from a few thousand samples per tile up to half the matrix. The 175 MiB peak is the full `(n, 256)` one-hot, not the distance tile: it does not grow with `tile_n` until the distance tile itself becomes the larger tensor, at 131072 x 256. Splitting the centroids below 128 saves memory and costs time.

Accumulating the one-hot in sample tiles of 4096, on the 65536 x 256 assignment, brings that step to 0.0261 s and 130.6 MiB.

## k-means++

Each new center rereads `X`. There are 255 such passes after the first center, and `2 + log(256) = 7` candidates share one GEMM. 255 GiB of reads in 1.34 s is about 190 GB/s. The L4's device bandwidth is about 300 GB/s, so this init is already near the cost of streaming `X` once per center. `torch.compile` on the candidate distances does not remove those reads.

| implementation | time | memory | init inertia |
| --- | --- | --- | --- |
| array API, eager, before the norm tile | 1.346 s | 1.000 GiB above the input |  |
| array API, `torch.compile` on the candidate distances, before the norm tile | 1.326 s | 1.000 GiB above the input |  |
| array API, eager, feature tiles of 256 for the row norm | 1.342 s | 129.5 MiB above the input | 489574400 |
| [PR 23](https://github.com/cakedev0/scikit-learn/pull/23), 4 threads | 24.16 s | RSS 3.13 GiB, including the 1.00 GiB matrix | 490031100 |

**Disclaimer on init quality.** PR 23 samples a chunk from the per-chunk sums, then a row inside that chunk. The array-API init draws from one cumulative sum. The selected centers are not the same sequence, and a shared seed does not make them the same draw. On this isotropic matrix the init inertias differ by 0.093% (489574400 against 490031100). On the separated blobs the array-API init inertia is 316887 and the PR 23 init inertia is 339266, which is 6.6% higher. That gap is the different sampler. PR 23 was not continued into Lloyd iterations here.

## Full fit

`fit_kmeans` runs k-means++ and then Lloyd steps until the sum of squared center movement is at most `tol` times the mean feature variance (`tol` 1e-4). The fit below uses an assignment tile of 65536 x 256.

The first measured fit peaked at 3.003 GiB. That was the final inertia forming a second and third copy of `X`. Tiling the inertia removed it. The next peak, 514 MiB, was `var` along samples: a 512 MiB workspace, and the scalar it returned was 1.0000989437103271. Feature tiles of 128 produce that same scalar and peak at 128 MiB. After both changes the fit peak is the Lloyd step.

| run | time | peak above the input | iterations | inertia | center shift |
| --- | --- | --- | --- | --- | --- |
| eager, 6 iterations | 1.572 s | 152.0 MiB | 6 | 266535392 | 31.43 |
| eager, 30 iterations | 2.330 s | 152.0 MiB | 30 | 266495072 | 0.134 |
| `torch.compile` on the Gram tile and the candidate distances, 30 iterations | 2.398 s | 152.0 MiB | 30 | 266491984 | 0.199 |
| cuML k-means++, first large call in a fresh process | 5.11 s | device high-water 1240 MiB | 6 | 266531024 |  |
| cuML k-means++, later call in a warm process | 3.982 s |  | 6 | 266531040 |  |
| cuML, centers fixed to the first 256 rows, tolerance 1e-12, 30 iterations | 0.827 s |  | 30 | 266601184 |  |
| cuML, scalable k-means++ | 1.544 s |  | 2 | 267938112 |  |

cuML's fixed-init run does 30 iterations in 0.827 s, which is 27.6 ms per iteration. The array-API step with a 4096-row update tile is 26.1 ms. The compiled fit is not faster than the eager fit, and it uses the same 152 MiB.

A repeated eager 30-iteration fit on this GPU landed at inertia 266492032 and 266495072. The relative gap between those two, and between either of them and the compiled inertia 266491984, is about 0.001%. GEMM reductions on this device are not locked to one accumulation order.

## Quality

**Separated blobs, agreement.** Both the array-API fit and cuML stop at iteration 2 with center shift 0. Recomputed inertia is 167259.875 on both sides. All 32768 labels match after a permutation of cluster ids. Center locations agree to about 1e-9 in squared distance. No quality gap on this problem.

**Disclaimer: `cuml` `inertia_` is a different number.** On the blobs, `inertia_` is 167351.03 while the sum of squared distances to the returned centers is 167259.875. The comparison above uses the recomputed sum. On the timing problem the two cuML figures agree (266531024 recomputed, 266531040 reported).

**Disclaimer: the timing problem has not met the scikit-learn tolerance.** After 30 iterations the center shift is still 0.134, and the threshold is 1.00e-4. cuML stops at iteration 6 under its own rule. Inertia still agrees: the array-API value after 6 iterations is 266535392, cuML's is 266531040 (relative difference 0.0016%), and after 30 iterations the array-API inertia is 266495072, which is 0.013% lower than cuML's stopped value. These are similar fits. They are not the same run, because the inits differ and our loop has not converged by the scaled center-shift test.

**Disclaimer: scalable k-means++ is a worse init on this draw.** cuML's default init finished in 1.54 s and 2 iterations with inertia 267938112, 0.53% higher than the k-means++ cuML run. The comparison in the table uses `init="k-means++"` for that reason.

## Where the gap went

The Cython k-means++ is slower here (24.2 s against 1.34 s) because each center rereads 1 GiB and the L4 streams that faster than 4 CPU cores. The array-API Lloyd step matches cuML's fixed-init rate (about 26 ms against 28 ms). The full eager fit is shorter than cuML's k-means++ fit (2.33 s for 30 iterations against 3.98 s for 6) on this shape. Compiling the Gram tile does not move either number.

The memory work that did move the result was deleting full-size temporaries inside the array API: the row-norm product, the inertia difference, and the variance workspace. The fit peak above the input went from 3.00 GiB to 152 MiB. cuML's device high-water during the fit is 1240 MiB, which already contains the 1.00 GiB matrix.
