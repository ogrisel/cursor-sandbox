# Lloyd k-means in the Python array API

## What this PR explores

This experiment studies nearest-centroid assignment, Lloyd updates, empty
clusters, and centroid initialization through the Python array API. The eager
implementation runs with PyTorch on CPU and CUDA and with CuPy on CUDA.
Comparisons cover stock scikit-learn, scikit-learn with k-means++ performance
patches, Cython, and cuML.

The journal progresses from kernel-fusion probes to bounded-memory tiled
assignment, full fits, repeated-seed and shared-start comparisons, empty-center
relocation, and greedy versus scalable initialization. The current five-task
mix spans 3 to 3000 clusters, 2 to 1000 features, and 135000 to 2100000
samples. Runs use float32, eager execution, TF32 disabled, three seeds, and a
60-second worker limit.

## Latest results

[014](014-portable-array-api-kmeans/index.html) extracts a scikit-learn
compatible portable `KMeans` estimator and evaluates CuPy-native replacements
for the one-hot centroid update identified in 013.

| one CuPy centroid update | 100 clusters | 550 clusters | 3000 clusters |
| --- | --- | --- | --- |
| Portable current | 56.95 ms | 60.02 ms | 65.89 ms |
| Portable tuned | 19.20 ms | 17.66 ms | 18.00 ms |
| `cupyx.scatter_add` | 1.172 ms | 0.350 ms | 0.365 ms |
| Fused atomic `RawKernel` | 1.064 ms | 0.161 ms | 0.152 ms |

Main conclusions:

- The public estimator supports only random and greedy k-means++ initialization, dense Lloyd iterations, and the applicable scikit-learn KMeans hyperparameters.
- It passes the scikit-learn estimator suite, including strict array-API namespace, device, indexing, and dtype checks.
- The default path remains backend-agnostic and carries explicit TODO boundaries for optional compiled assignment and keyed centroid-update callables.
- `cupyx.scatter_add` is 16x to 50x faster than the tuned portable update. It is the best first CuPy fast path, subject to its float32 atomic and non-determinism constraints.
- A custom fused sum/count kernel is another 2.2x to 2.4x faster at large `k`, but should follow the simpler public CuPy primitive rather than precede it.

## Journal

- [001 — fusion probe](001-fusion-probe/index.html): eager and compiled distance-plus-argmin kernels.
- [002 — large-shape OOM](002-large-shape-oom/index.html): which schedules avoid the full distance matrix.
- [003 — three shapes](003-resized-shapes/index.html): sample-, centroid-, and feature-heavy fusion behavior.
- [004 — tile trade-offs](004-tile-tradeoff/index.html): bounded-memory tiles, Cython Lloyd, and k-means++.
- [005 — full k-means](005-full-kmeans/index.html): eager array API, Cython, patched scikit-learn, and cuML.
- [006 — benchmark breadth](006-breadth/index.html): structure and cluster-count sensitivity across five implementations.
- [007 — repeated seeds and shared centers](007-seeded-fixed-centers/index.html): uncertainty bars and initializer-independent Lloyd comparisons.
- [008 — empty-center task mix](008-empty-reassignment-task-mix/index.html): stochastic relocation across five bounded tasks.
- [009 — k-means++ only](009-kmeans-plusplus-only/index.html): timing, memory, and quality before Lloyd.
- [010 — scalable initialization](010-scalable-initialization/index.html): farthest relocation, cuML initializer options, and array-API k-means||.
- [011 — consolidated benchmark](011-consolidated-benchmark/index.html): initialization, Lloyd-only, and full-fit results on one page, plus the scalable-init ablation.
- [012 — source link audit](012-source-link-audit/index.html): source links pinned to the commits that each report measured.
- [013 — large-k Lloyd optimization](013-large-k-lloyd-optimization/index.html): scalable-init sensitivity, cuML kernel analysis, optimization probes, and next steps.
- [014 — portable array-API KMeans](014-portable-array-api-kmeans/index.html): sklearn-compatible estimator extraction and CuPy-native centroid-update probes.
