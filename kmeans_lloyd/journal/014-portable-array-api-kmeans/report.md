# 014 — a portable KMeans estimator and CuPy-native update paths

This iteration turns the experimental Lloyd functions into a reusable
[`KMeans`](https://github.com/ogrisel/cursor-sandbox/blob/49f904a3aea28e55f4e015347324bd9603001615/kmeans_lloyd/src/kmeans_lloyd/kmeans.py#L39-L277)
estimator while keeping the portable path backend-agnostic. It also tests
which CuPy-specific primitive should sit behind the future centroid-update
hook proposed in [013](../013-large-k-lloyd-optimization/report.md).

## Public estimator surface

The estimator mirrors the dense Lloyd subset of
`sklearn.cluster.KMeans`:

| parameter | supported behavior |
| --- | --- |
| `n_clusters` | positive integer |
| `init` | `"k-means++"` or `"random"` |
| `n_init` | positive integer or `"auto"`; auto means 1 for k-means++ and 10 for random |
| `max_iter`, `tol`, `verbose`, `random_state`, `copy_x` | same public role as scikit-learn |
| `algorithm` | `"lloyd"` only |

Scalable k-means++ is not exposed by this class. The old experimental helper
remains in the benchmark module so entries 010–013 stay reproducible, but it
is no longer part of the package-level API. Sparse input, sample weights,
callable or array initializers, and Elkan are intentionally outside this
portable implementation.

`fit` exposes the conventional `cluster_centers_`, `labels_`, `inertia_`, and
`n_iter_` attributes. `predict`, `transform`, `score`, `fit_predict`, and
`fit_transform` follow the estimator API. NumPy, PyTorch, CuPy, and strict
array-API arrays retain their namespace, device, and float32 or float64
dtype.

The implementation uses shape- and device-based tile budgets rather than
backend names. The CUDA schedule incorporates the portable 013 result:
argmin plus gather, update tiles of 16384 rows by up to 512 centers, and
smaller assignment center tiles for low-dimensional large-`k` inputs.

Two inline TODOs define the intended acceleration boundary:

1. an assignment factory may cache `torch.compile` or a CuPy fused top-1
   kernel by shape and dtype;
2. a centroid-update callable may select `torch.index_add_`,
   `cupyx.scatter_add`, or another native keyed reduction while retaining the
   one-hot array-API fallback.

## Estimator compliance

The complete local suite passes with `SCIPY_ARRAY_API=1`:

| check | result |
| --- | --- |
| scikit-learn estimator checks | 60 passed, 17 skipped for unavailable optional backends |
| full local package suite | 79 passed, 20 skipped |
| strict array-API namespace and device checks | passed on `array_api_strict` CPU and secondary device |
| CUDA smoke and package tests | 58 estimator checks passed; PyTorch and CuPy fit/predict/transform tests passed |

The estimator checks caught portability details that NumPy accepts but the
standard does not: out-of-bounds slice stops, row indexing without an
explicit second axis, zero-dimensional indices passed to `take`, and calls
with a different namespace after fitting. Fixing those made the low-level
initializer and Lloyd path conform to strict array-API indexing.

## CuPy update experiment

The new
[`probe_cupy_updates.py`](https://github.com/ogrisel/cursor-sandbox/blob/27747a6570f592858a799c6ca17a1a52e8e0f806/kmeans_lloyd/scripts/probe_cupy_updates.py)
compares five ways to accumulate rows by label on the same L4 and full task
shapes as 013. Labels are a fixed uniform random draw so every implementation
receives identical contention. Times are medians of five warm measurements
and cover one complete centroid update.

| update time | k100-d32 | k550-d6 | k3000-d2 |
| --- | ---: | ---: | ---: |
| portable current one-hot tiles | 56.95 ms | 60.02 ms | 65.89 ms |
| portable tuned one-hot tiles | 19.20 ms | 17.66 ms | 18.00 ms |
| `cupyx.scatter_add` + `bincount` | 1.172 ms | 0.350 ms | 0.365 ms |
| `cupy.add.at` + `bincount` | 1.143 ms | 0.336 ms | 0.336 ms |
| fused sum/count `RawKernel` | 1.064 ms | 0.161 ms | 0.152 ms |

`cupyx.scatter_add` is 16x to 50x faster than the tuned portable update and
49x to 181x faster than the old tile schedule. It reduces the same structural
bottleneck as PyTorch `index_add_`: work scales with `n_samples x
n_features`, not with a dense membership matrix covering every center tile.

The raw kernel fuses feature sums and counts into one launch. It is only 1.1x
faster than `scatter_add` at 100 clusters, but 2.2x to 2.4x faster at 550 and
3000 clusters. All native variants agree with `scatter_add` within
`8.4e-7` maximum absolute center error; the small differences are expected
from non-deterministic floating-point atomic order.

## What should become a CuPy fast path

`cupyx.scatter_add` is the best first backend-specific implementation:

- it is a public, small, auditable operation and already matches NumPy
  `add.at` semantics for repeated labels;
- it captures almost all the measured gain without maintaining CUDA source;
- it composes directly with `cupy.bincount` and the existing empty-center
  policy.

It has important constraints. CuPy 14.2 documents indexed `scatter_add` only
for CUDA `atomicAdd` types, including float32 but not float64. Out-of-range
indices wrap instead of raising. Floating-point atomics are not deterministic.
The adapter must therefore validate labels, use this path for supported
dtypes only, and fall back to the portable update for float64 unless a
separate implementation is validated. `cupy.bincount` may also synchronize
the device, so microbenchmarks must time the complete update rather than infer
its cost from asynchronous launches.

`cupy.add.at` has the same semantics and nearly identical timing, so it adds
no useful alternative. The fused `RawKernel` is worth retaining as a second
experiment, not as the first production path: the present probe is float32
and int64-label specific, and production code would need per-dtype kernels,
launch caching, bounds guarantees, empty-center tests, and documented atomic
non-determinism.

After the update hook lands, assignment becomes the next CuPy target. Neither
`cupy.fuse` nor a standard reduction expresses distance-plus-top-1 without a
score tile. A `RawKernel` or `cupyx.jit` kernel can stream centers and retain
one best label per sample, analogous to cuVS, but it should be attempted only
after end-to-end measurements with the inexpensive scatter update show that
assignment is again dominant.

## Next implementation steps

1. Keep the new estimator's default path pure array API.
2. Add a private optional centroid-update callable to `lloyd_step` and
   `fit_lloyd`; keep it out of the sklearn-compatible constructor. Lock down
   the contract `(X, labels, old_centers) -> updated_centers`: empty clusters
   keep their old center unless the caller requested farthest-point
   relocation, in which case the native path must still invoke the shared
   relocation bookkeeping.
3. Implement a CuPy adapter with `cupyx.scatter_add` plus `bincount` for
   float32 and strict label validation. Add agreement, empty-center, and
   namespace tests.
4. Implement the matching PyTorch adapter with `index_add_`, under the same
   hook and tests.
5. Benchmark full fits before considering the fused raw accumulator or a
   CuPy top-1 assignment kernel.

The result is a stable portable estimator now, with a narrow extension point
for backend acceleration later. The CuPy measurements show that this boundary
can recover essentially all of the update gap without contaminating the
portable implementation with backend branches.

Previous: [large-k Lloyd optimization](../013-large-k-lloyd-optimization/report.md).
Index: [journal](../index.md).
