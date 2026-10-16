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

[015](015-native-backend-estimator-benchmark/index.html) adds PyTorch
`index_add_` and CuPy `add.at` centroid updates to the portable `KMeans`
estimator, keeps the one-hot update for other namespaces, and reruns the full
benchmark through the estimator.

| shared-start fit, 12 Lloyd iterations | k3-d1000 | k17-d180 | k100-d32 | k550-d6 | k3000-d2 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Array API - Torch CUDA | 0.89 s | 0.64 s | 0.39 s | 0.49 s | 0.62 s |
| Array API - Torch CUDA, generic update | 0.89 s | 0.63 s | 0.46 s | 0.59 s | 0.75 s |
| Array API - CuPy | 1.06 s | 0.67 s | 0.39 s | 0.42 s | 0.58 s |
| Array API - CuPy, generic update | 1.00 s | 0.87 s | 0.58 s | 0.60 s | 0.76 s |
| cuML 26.10 | 6.88 s | 2.12 s | 0.54 s | 0.35 s | 0.32 s |

Main conclusions:

- The native update speeds up CUDA fits by 1.06x to 1.47x from 17 clusters up on CuPy and 100 clusters up on PyTorch, and Torch CPU fits by up to 4.6x.
- With few clusters and many features, atomic contention makes the CUDA scatter-add slower than the one-hot GEMM, so the dispatch keeps the portable update there.
- The first run also found a PyTorch finiteness check that used 5.3 GiB of temporaries on the widest task; the estimator now checks column sums first.
- The array-API backends now beat cuML's Lloyd iterations up to 100 clusters; cuML stays 1.2x to 1.9x faster at 550 and 3000 clusters.

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
- [015 — native backend updates in the estimator](015-native-backend-estimator-benchmark/index.html): PyTorch and CuPy scatter-add updates, the CUDA contention crossover, and the full benchmark rerun.
