# Lloyd k-means, one iteration, kernel fusion

Does `torch.compile` or `cupy.fuse` fuse nearest-centroid `argmin` into the squared Euclidean distance?

## Answer

`torch.compile` fuses `argmin` into the squared-distance kernel when the assignment is a running minimum over a tile of 32 centroids. One Triton kernel writes the label vector and the winning distances. Its peak is `n * 12` bytes. The `(n, k)` distance matrix, 1–4 GiB on these problems, is absent.

On the naive broadcast and on the Gram form, `torch.compile` still writes that distance matrix. The broadcast reduction becomes one kernel and `argmin` stays a second kernel. On the Gram form, `argmin` moves into the epilogue that reads the cuBLAS output; `ampere_sgemm` still stores `(n, k)`. That epilogue fusion cuts the eager peak from 16 GiB to 4 GiB on the sample-heavy problem and leaves the runtime on the GEMM (2.04 s compiled, 2.18 s eager).

`cupy.fuse` fuses the elementwise square and the reduction for a single centroid. `argmin` is not a method of the tracer proxy, so the nearest-centroid step is outside its reach. A running update that uses `where` still keeps one `(n, d)` buffer and is slower than the eager step.

Eager calls of both libraries are the baseline in every row. The full running assignment is the schedule that removes the distance matrix, and it is slower than the Gram GEMM: 12.8 s against about 2 s on sample-heavy and centroid-heavy, 6.1 s against 1.07 s on feature-heavy.

| schedule | what remains allocated | sample-heavy | centroid-heavy | feature-heavy |
| --- | --- | --- | --- | --- |
| eager Gram, PyTorch | `X * X`, the `(n, k)` product, and the epilogue | 2.18 s, 16.00 GiB | 2.18 s inside the Lloyd step, 16.00 GiB | 1.07 s, 4.00 GiB |
| `torch.compile` Gram | the `(n, k)` GEMM output | 2.04 s, 4.00 GiB | 2.01 s, 4.00 GiB | 1.02 s, 1.00 GiB |
| eager Gram, CuPy | same buffers as eager PyTorch | out of memory | out of memory | 1.06 s, 4.00 GiB |
| `cupy.fuse` Gram | call rejected: `sum(..., keepdims=True)` is unsupported | | | |
| eager running tile, 32 centroids | an `(n, d)` difference | 2.88 s, 8.00 GiB | 1.45 s, 4.00 GiB | 2.89 s, 8.00 GiB |
| `torch.compile` running tile | labels and winning distances, `n * 12` bytes | 49 ms, 1.50 MiB | 25 ms, 768 KiB | 49 ms, 768 KiB |
| `torch.compile` running tile, every centroid | the same per-tile kernel, plus a small Python merge | 12.75 s, 5.13 MiB | 12.78 s, 2.56 MiB | 6.13 s, 2.56 MiB |
| `cupy.fuse` one centroid | one `(n, d)` difference; `argmin` is unavailable | 606 ms, 4.00 GiB | 293 ms, 2.00 GiB | 585 ms, 4.00 GiB |

The one-centroid CuPy times are a single fused step. The matching eager measurement is four steps: 360 ms, 180 ms, and 360 ms, with peaks of 8 GiB, 4 GiB, and 8 GiB. The fused step is slower than those four eager steps.

Host: NVIDIA L4, 23 GiB. PyTorch 2.14.1+cu130, CuPy 14.2.0, array-api-compat 1.15.0. Float32, TF32 off. The assignment is written with the Python array API (`array_api_compat`). Peak memory is bytes allocated above the inputs.

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
