# Lloyd k-means in the Python array API

## Current result

[007](007-seeded-fixed-centers/index.html) is the current comparison. It repeats all 17 datasets from [006](006-breadth/index.html) with seeds 0 through 4: 1,700 successful runs. The array-API numbers are eager PyTorch, on CPU and on CUDA. `torch.compile` is not used in this comparison. Host: NVIDIA L4, float32, TF32 off. A full fit stops after 12 Lloyd iterations or when the center shift falls under `1e-8` times the mean feature variance.

On 131072 samples, 2048 features, and 256 clusters, five-seed means and sample standard deviations are:

| implementation | k-means++ | full fit | fit peak increment | fit inertia |
| --- | --- | --- | --- | --- |
| [array API, CUDA](007-seeded-fixed-centers/index.html) | 1.344 ± 0.001 s | 1.484 ± 0.034 s | 135.6 MiB | 2252 ± 144 |
| [cuML 26.10](007-seeded-fixed-centers/index.html) | 3.966 ± 0.016 s | 4.018 ± 0.018 s | 1042 MiB | 2113 ± 95 |
| [scikit-learn, PRs 23 and 26](007-seeded-fixed-centers/index.html) | 23.96 ± 0.05 s | 26.60 ± 0.46 s | 2048 MiB | 2288 ± 154 |
| [array API, CPU](007-seeded-fixed-centers/index.html) | 41.41 ± 1.07 s | 46.06 ± 1.05 s | 175 MiB | 2149 ± 96 |
| [scikit-learn 1.7.2](007-seeded-fixed-centers/index.html) | 126.80 ± 2.22 s | 128.35 ± 6.01 s | 2048 MiB | 2322 ± 155 |

Eager CUDA is the fastest full fit. cuML has the lowest average inertia, and its error bar overlaps the array-API CPU result. Runtime rankings are stable across seeds. Fit-quality rankings from the single seed in 006 are not.

The same rows of each dataset are given to every implementation for a separate Lloyd track. One Lloyd step then agrees within 0.080% on every case and seed. On the shape above that step takes 0.025 s and 131 MiB on eager CUDA, 0.285 s and about 1.0 GiB in cuML, 1.848 s and 164 MiB for the array API on CPU, and about 2.03 s and 2.0 GiB in both scikit-learn builds.

Longer fits from those shared centers can diverge. Scikit-learn relocates a cluster that becomes empty. The array API keeps the previous center, and cuML followed that result. On one four-cluster seed the resulting mean inertia is 32.02 for scikit-learn and 249.50 for the array API and cuML. The one-step comparison is the measurement that keeps the implementations on the same work.

Peak increments use different meters: PyTorch allocator bytes above the input, first-call `VmHWM` for the CPU libraries, and 1 MiB nvidia-smi samples for cuML.

## Current implementation

The measured path is eager array-API code on branch `cursor/kmeans-lloyd-fusion-8896`. `fit_kmeans` draws k-means++ centers and then calls `fit_lloyd`. The benchmark passes no compiled `step` or `distance` hook.

| solution | source |
| --- | --- |
| k-means++ | [`kmeans_plusplus`](https://github.com/ogrisel/cursor-sandbox/blob/cursor/kmeans-lloyd-fusion-8896/kmeans_lloyd/src/kmeans_lloyd/iteration.py#L390-L432) |
| one tiled Lloyd step | [`lloyd_step`](https://github.com/ogrisel/cursor-sandbox/blob/cursor/kmeans-lloyd-fusion-8896/kmeans_lloyd/src/kmeans_lloyd/iteration.py#L326-L353) |
| Lloyd from given centers | [`fit_lloyd`](https://github.com/ogrisel/cursor-sandbox/blob/cursor/kmeans-lloyd-fusion-8896/kmeans_lloyd/src/kmeans_lloyd/iteration.py#L492-L545) |
| k-means++ plus Lloyd | [`fit_kmeans`](https://github.com/ogrisel/cursor-sandbox/blob/cursor/kmeans-lloyd-fusion-8896/kmeans_lloyd/src/kmeans_lloyd/iteration.py#L453-L489) |

## Original question

Does `torch.compile` or `cupy.fuse` fuse nearest-centroid `argmin` into the squared Euclidean distance?

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

The fusion schedules are linked from [001](001-fusion-probe/index.html), [002](002-large-shape-oom/index.html), and [003](003-resized-shapes/index.html). `torch.compile` is applied in [`_compile_torch`](https://github.com/ogrisel/cursor-sandbox/blob/cursor/kmeans-lloyd-fusion-8896/kmeans_lloyd/scripts/run_experiments.py#L255-L276). `cupy.fuse` is applied in [`_try_cupy_fuse`](https://github.com/ogrisel/cursor-sandbox/blob/cursor/kmeans-lloyd-fusion-8896/kmeans_lloyd/scripts/run_experiments.py#L303-L330). On the later full-fit timing shape, wrapping the Gram tile and candidate distances with `torch.compile` took 2.40 s against 2.33 s eager, at the same 152 MiB peak ([005](005-full-kmeans/index.html)).

## Iterations

- [001 — fusion probe](001-fusion-probe/index.html) on a problem small enough that the naive broadcast tensor fits.
- [002 — large shape, eager out of memory](002-large-shape-oom/index.html). Compiled GEMM still runs; a compiled running tile of 32 centroids does not allocate the distance matrix.
- [003 — three shapes](003-resized-shapes/index.html) that vary samples, centroids, and features. `torch.compile` writes the Gram distance matrix and folds argmin into its epilogue. A running tile is the schedule that drops that matrix. `cupy.fuse` still stops at `argmin`.
- [004 — tile sizes, Cython Lloyd, k-means++](004-tile-tradeoff/index.html). A Gram tile of 4096 by 1024 plus a tiled mean update finishes a feature-heavy Lloyd step in 1.70 s, with assignment peak 64.5 MiB and update peak 432 MiB. The compiled running tile is fastest at 32 centroids (5.98 s, 2.56 MiB). On 65536×1024×2048 the L4 step takes 0.071 s and the 4-thread Cython Lloyd step takes 1.53 s, with 1 label differing. k-means++ on 65536×1024×8192 takes 10.3 s after the sample norm is computed once.
- [005 — full fit, Cython k-means++, cuML](005-full-kmeans/index.html). On 131072×256×2048 the tiled eager fit takes 2.33 s and 152 MiB above the input (30 iterations). The same k-means++ on 4 CPU threads takes 24.2 s. cuML's k-means++ fit takes 3.98 s and stops at iteration 6. Inertia agrees within 0.02% on that problem, with an explicit note that our center shift has not reached the scikit-learn tolerance. On separated blobs the labels match exactly. `torch.compile` does not shorten the fit.
- [006 — structure, centroid count, five implementations](006-breadth/index.html). One seed of the eager array API, stock scikit-learn, both cakedev0 patches, and cuML, from tight blobs to noise and up to 131072×2048×256.
- [007 — repeated seeds and shared fixed centers](007-seeded-fixed-centers/index.html). Seeds 0 through 4 add uncertainty bars. Shared dataset rows isolate one Lloyd step. One-step objectives agree within 0.080%. Longer runs expose scikit-learn's empty-cluster relocation.

## Cases

The current headline shape is `speed-xl` from the [five-seed report](007-seeded-fixed-centers/index.html): 131072 samples, 2048 features, 256 clusters, separated blobs. That report also covers blob separation, noise, centroid counts from 4 to 128, and the intermediate shapes `tall`, `wide`, `mixed`, `speed-m`, and `speed-l`.

The fusion measurements in 003 use three larger assignment shapes:

| case | samples | centroids | features |
| --- | --- | --- | --- |
| sample-heavy | 131072 | 8192 | 8192 |
| centroid-heavy | 65536 | 16384 | 8192 |
| feature-heavy | 65536 | 4096 | 16384 |

The [probe](001-fusion-probe/index.html) records the kernel names on a problem small enough for the naive broadcast. The [three-shape report](003-resized-shapes/index.html) records every timed fusion call.
