# Lloyd k-means, one iteration, kernel fusion

Does `torch.compile` or `cupy.fuse` fuse nearest-centroid `argmin` into the squared Euclidean distance?

## Answer

Eager execution is the baseline under each library. Host: NVIDIA L4, 23 GiB. PyTorch 2.14.1+cu130, CuPy 14.2.0, array-api-compat 1.15.0. Float32, TF32 off. The assignment is written with the Python array API (`array_api_compat`). Peak memory is bytes allocated above the inputs.

### PyTorch

`torch.compile` fuses `argmin` into the squared-distance kernel when the assignment is a running minimum over a tile of 32 centroids. One Triton kernel writes the label vector and the winning distances. Its peak is `n * 12` bytes. The `(n, k)` distance matrix, 1–4 GiB on these problems, is absent.

On the naive broadcast and on the Gram form, `torch.compile` still writes that distance matrix. The broadcast reduction becomes one kernel and `argmin` stays a second kernel. On the Gram form, `argmin` moves into the epilogue that reads the cuBLAS output; `ampere_sgemm` still stores `(n, k)`. That epilogue fusion cuts the eager peak from 16 GiB to 4 GiB on the sample-heavy problem and leaves the runtime on the GEMM (2.04 s compiled, 2.18 s eager).

The full running assignment is the schedule that removes the distance matrix, and it is slower than the Gram GEMM: 12.8 s against about 2 s on sample-heavy and centroid-heavy, 6.1 s against 1.07 s on feature-heavy.

| schedule | what remains allocated | sample-heavy | centroid-heavy | feature-heavy |
| --- | --- | --- | --- | --- |
| [eager Gram](https://github.com/ogrisel/cursor-sandbox/blob/cursor/kmeans-lloyd-fusion-8896/kmeans_lloyd/src/kmeans_lloyd/iteration.py#L194-L197) | `X * X`, the `(n, k)` product, and the epilogue | 2.18 s, 16.00 GiB | 2.18 s inside the Lloyd step, 16.00 GiB | 1.07 s, 4.00 GiB |
| [`torch.compile` Gram](https://github.com/ogrisel/cursor-sandbox/blob/cursor/kmeans-lloyd-fusion-8896/kmeans_lloyd/src/kmeans_lloyd/iteration.py#L194-L197) | the `(n, k)` GEMM output | 2.04 s, 4.00 GiB | 2.01 s, 4.00 GiB | 1.02 s, 1.00 GiB |
| [eager running tile, 32 centroids](https://github.com/ogrisel/cursor-sandbox/blob/cursor/kmeans-lloyd-fusion-8896/kmeans_lloyd/src/kmeans_lloyd/iteration.py#L130-L136) | an `(n, d)` difference | 2.88 s, 8.00 GiB | 1.45 s, 4.00 GiB | 2.89 s, 8.00 GiB |
| [`torch.compile` running tile](https://github.com/ogrisel/cursor-sandbox/blob/cursor/kmeans-lloyd-fusion-8896/kmeans_lloyd/src/kmeans_lloyd/iteration.py#L130-L136) | labels and winning distances, `n * 12` bytes | 49 ms, 1.50 MiB | 25 ms, 768 KiB | 49 ms, 768 KiB |
| [`torch.compile` running tile, every centroid](https://github.com/ogrisel/cursor-sandbox/blob/cursor/kmeans-lloyd-fusion-8896/kmeans_lloyd/src/kmeans_lloyd/iteration.py#L139-L157) | the same per-tile kernel, plus a small Python merge | 12.75 s, 5.13 MiB | 12.78 s, 2.56 MiB | 6.13 s, 2.56 MiB |

### CuPy

`cupy.fuse` fuses the elementwise square and the reduction for a single centroid. `argmin` is not a method of the tracer proxy, so the nearest-centroid step stays outside the fused call. A running update that uses `where` still keeps one `(n, d)` buffer and is slower than the eager step. The Gram form is rejected because `sum(..., keepdims=True)` is unsupported inside the tracer.

The one-centroid fused times below are a single step. The matching eager measurement is four steps, and that fused step is slower than those four eager steps.

| schedule | what remains allocated | sample-heavy | centroid-heavy | feature-heavy |
| --- | --- | --- | --- | --- |
| [eager Gram](https://github.com/ogrisel/cursor-sandbox/blob/cursor/kmeans-lloyd-fusion-8896/kmeans_lloyd/src/kmeans_lloyd/iteration.py#L194-L197) | `X * X`, the `(n, k)` product, and the epilogue | out of memory | out of memory | 1.06 s, 4.00 GiB |
| [`cupy.fuse` Gram](https://github.com/ogrisel/cursor-sandbox/blob/cursor/kmeans-lloyd-fusion-8896/kmeans_lloyd/src/kmeans_lloyd/iteration.py#L180-L185) | call rejected: `sum(..., keepdims=True)` is unsupported | | | |
| [eager running step, 4 centroids](https://github.com/ogrisel/cursor-sandbox/blob/cursor/kmeans-lloyd-fusion-8896/kmeans_lloyd/src/kmeans_lloyd/iteration.py#L222-L232) | two `(n, d)` buffers, difference and square | 360 ms, 8.00 GiB | 180 ms, 4.00 GiB | 360 ms, 8.00 GiB |
| [`cupy.fuse` one centroid](https://github.com/ogrisel/cursor-sandbox/blob/cursor/kmeans-lloyd-fusion-8896/kmeans_lloyd/src/kmeans_lloyd/iteration.py#L222-L232) | one `(n, d)` difference | 606 ms, 4.00 GiB | 293 ms, 2.00 GiB | 585 ms, 4.00 GiB |

## Implementations

Each schedule is one function on branch `cursor/kmeans-lloyd-fusion-8896`. `torch.compile` is applied in [`_compile_torch`](https://github.com/ogrisel/cursor-sandbox/blob/cursor/kmeans-lloyd-fusion-8896/kmeans_lloyd/scripts/run_experiments.py#L255-L276). `cupy.fuse` is applied in [`_try_cupy_fuse`](https://github.com/ogrisel/cursor-sandbox/blob/cursor/kmeans-lloyd-fusion-8896/kmeans_lloyd/scripts/run_experiments.py#L303-L330).

| solution | source |
| --- | --- |
| one Lloyd iteration | [`lloyd_iteration`](https://github.com/ogrisel/cursor-sandbox/blob/cursor/kmeans-lloyd-fusion-8896/kmeans_lloyd/src/kmeans_lloyd/iteration.py#L21-L53) |
| centroid update | [`update_centroids`](https://github.com/ogrisel/cursor-sandbox/blob/cursor/kmeans-lloyd-fusion-8896/kmeans_lloyd/src/kmeans_lloyd/iteration.py#L160-L171) |
| naive broadcast distance | [`squared_distances_broadcast`](https://github.com/ogrisel/cursor-sandbox/blob/cursor/kmeans-lloyd-fusion-8896/kmeans_lloyd/src/kmeans_lloyd/iteration.py#L174-L177) |
| naive broadcast and `argmin` | [`broadcast_distance_argmin`](https://github.com/ogrisel/cursor-sandbox/blob/cursor/kmeans-lloyd-fusion-8896/kmeans_lloyd/src/kmeans_lloyd/iteration.py#L188-L191) |
| broadcast distance only | [`broadcast_distance_only`](https://github.com/ogrisel/cursor-sandbox/blob/cursor/kmeans-lloyd-fusion-8896/kmeans_lloyd/src/kmeans_lloyd/iteration.py#L235-L237) |
| Gram distance | [`squared_distances_gemm`](https://github.com/ogrisel/cursor-sandbox/blob/cursor/kmeans-lloyd-fusion-8896/kmeans_lloyd/src/kmeans_lloyd/iteration.py#L180-L185) |
| Gram distance and `argmin` | [`gemm_distance_argmin`](https://github.com/ogrisel/cursor-sandbox/blob/cursor/kmeans-lloyd-fusion-8896/kmeans_lloyd/src/kmeans_lloyd/iteration.py#L194-L197) |
| broadcast tile | [`tile_broadcast_argmin`](https://github.com/ogrisel/cursor-sandbox/blob/cursor/kmeans-lloyd-fusion-8896/kmeans_lloyd/src/kmeans_lloyd/iteration.py#L200-L203) |
| Gram tile | [`tile_gemm_argmin`](https://github.com/ogrisel/cursor-sandbox/blob/cursor/kmeans-lloyd-fusion-8896/kmeans_lloyd/src/kmeans_lloyd/iteration.py#L206-L209) |
| one-centroid distance | [`centroid_squared_distance`](https://github.com/ogrisel/cursor-sandbox/blob/cursor/kmeans-lloyd-fusion-8896/kmeans_lloyd/src/kmeans_lloyd/iteration.py#L212-L219) |
| running `argmin` step | [`running_argmin_step`](https://github.com/ogrisel/cursor-sandbox/blob/cursor/kmeans-lloyd-fusion-8896/kmeans_lloyd/src/kmeans_lloyd/iteration.py#L222-L232) |
| running assignment | [`assign_running`](https://github.com/ogrisel/cursor-sandbox/blob/cursor/kmeans-lloyd-fusion-8896/kmeans_lloyd/src/kmeans_lloyd/iteration.py#L106-L127) |
| running tile of 32 centroids | [`running_tile_distances`](https://github.com/ogrisel/cursor-sandbox/blob/cursor/kmeans-lloyd-fusion-8896/kmeans_lloyd/src/kmeans_lloyd/iteration.py#L130-L136) |
| running tile over every centroid | [`assign_running_tiled`](https://github.com/ogrisel/cursor-sandbox/blob/cursor/kmeans-lloyd-fusion-8896/kmeans_lloyd/src/kmeans_lloyd/iteration.py#L139-L157) |

## Iterations

- [001 — fusion probe](001-fusion-probe/index.html) on a problem small enough that the naive broadcast tensor fits.
- [002 — large shape, eager out of memory](002-large-shape-oom/index.html). Compiled GEMM still runs; a compiled running tile of 32 centroids does not allocate the distance matrix.
- [003 — three shapes](003-resized-shapes/index.html) that vary samples, centroids, and features. `torch.compile` writes the Gram distance matrix and folds argmin into its epilogue. A running tile is the schedule that drops that matrix. `cupy.fuse` still stops at `argmin`.

## Cases

The three shapes used in the last iteration:

| case | samples | centroids | features |
| --- | --- | --- | --- |
| sample-heavy | 131072 | 8192 | 8192 |
| centroid-heavy | 65536 | 16384 | 8192 |
| feature-heavy | 65536 | 4096 | 16384 |

The [probe](001-fusion-probe/index.html) records the kernel names on a problem small enough for the naive broadcast. The [three-shape report](003-resized-shapes/index.html) records every timed call.
