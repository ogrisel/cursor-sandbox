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

[018](018-cpu-array-api-optimization/index.html) evaluates backend-neutral
CPU optimizations for initialization, Lloyd iterations, and full fit.

Main conclusions:

- Labels-only assignment and augmented GEMM recover 1.2–2.5x on three
  representative CPU tasks.
- Augmented GEMM is the strongest optimization, but it retains another
  input-sized array and still needs cancellation-safe direct-distance repair.
- Larger score tiles, hierarchical sampling, `torch.compile`, and fused
  Python-level statistics do not provide robust wins.
- The projected remaining gap to cakedev0 is 2.3–6.1x; closing it likely
  requires a compiled fused CPU kernel.

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
- [016 — GEMM versus broadcast distances](016-gemm-vs-broadcast-distances/index.html): time, memory, and quality across initialization, Lloyd, and full fit on CPU and CUDA.
- [017 — GEMM cancellation fallback](017-gemm-cancellation-fallback/index.html): translated-data failures, threshold sensitivity, and selective direct-distance repair.
- [018 — backend-neutral CPU optimizations](018-cpu-array-api-optimization/index.html): labels-only assignment, tiling, interleaving, augmented GEMM, compilation, and sampling experiments.
