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

[011](011-consolidated-benchmark/index.html) consolidates initialization-only,
Lloyd-only, and full-fit results for all contenders on one page and explains
the scalable-initializer gap between the array API and cuML.

| full fit, seconds | 3 clusters | 17 clusters | 100 clusters | 550 clusters | 3000 clusters |
| --- | --- | --- | --- | --- | --- |
| Array API - Torch CUDA, greedy | 0.94 s | 1.25 s | 1.20 s | 1.66 s | 2.62 s |
| Array API - CuPy, greedy | 1.13 s | 1.77 s | 1.79 s | 2.44 s | 4.32 s |
| scikit-learn PRs 23+26, greedy | 6.66 s | 5.04 s | 2.94 s | 3.25 s | 4.52 s |
| cuML 26.10, greedy | 7.18 s | 2.52 s | 0.98 s | 0.99 s | 1.18 s |
| cuML 26.10, scalable | 6.48 s | 2.41 s | 0.73 s | 0.63 s | 1.18 s |

Main conclusions:

- Array API - Torch CUDA is the fastest full fit and Lloyd-only run at 3 and 17 clusters; cuML is fastest from 100 clusters up.
- After 12 Lloyd iterations, every configuration ends within 0.4% of the best objective except cuML scalable at 3000 clusters, which ends 5.6% above it.
- Farthest-point empty-center relocation makes all array-API backends match scikit-learn on the only task with empty clusters, 9.5 percentage points better than cuML.
- cuML's scalable initializer looks best before Lloyd because it runs weighted Lloyd on its candidates; it ends worse at 3000 clusters because its greedy candidate reduction ignores the candidate weights.
- Adding a weighted Lloyd recluster to the array-API scalable initializer, while keeping its weighted reduction, gave the best initializer and final objectives at 550 and 3000 clusters in an ablation.
- The tiled Gram schedule remains the practical array-API Lloyd path; `torch.compile` can remove a tile's distance matrix with a running schedule, but that full schedule is slower than eager tiled GEMM.

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
