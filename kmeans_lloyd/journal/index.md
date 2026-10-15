# Lloyd k-means, one iteration, kernel fusion

Does `torch.compile` or `cupy.fuse` fuse nearest-centroid `argmin` into the squared Euclidean distance?

The assignment is written with the Python array API (`array_api_compat`). Eager execution is measured beside every compiled or fused call. Peak memory, not just runtime, is the test: a fused argmin does not allocate the distance matrix, and a fused broadcast does not allocate the `(samples, centroids, features)` difference.

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

Host: NVIDIA L4, 23 GiB. PyTorch 2.14.1+cu130, CuPy 14.2.0, array-api-compat 1.15.0. Float32, TF32 off.
