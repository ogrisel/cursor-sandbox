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

[013](013-large-k-lloyd-optimization/index.html) explains why cuML Lloyd is
faster at large `k`, tests portable and backend-specific optimizations, and
checks whether fewer scalable-initialization rounds change its trade-off.

| 12 Lloyd iterations, seconds | 100 clusters | 550 clusters | 3000 clusters |
| --- | --- | --- | --- |
| Array API - Torch CUDA, current | 0.626 s | 0.793 s | 1.001 s |
| Array API - Torch CUDA, portable tuned | 0.251 s | 0.377 s | 0.508 s |
| Array API - CuPy, current | 0.992 s | 0.997 s | 1.228 s |
| Array API - CuPy, portable tuned | 0.461 s | 0.484 s | 0.610 s |
| PyTorch compiled assignment + native update | 0.091 s | 0.119 s | 0.150 s |
| cuML, device-resident input | 0.126 s | 0.090 s | 0.086 s |

Main conclusions:

- The current scalable initializer is not competitive here: every 2-, 4-, and 8-round configuration costs more than greedy k-means++, and Lloyd erases its initial-quality gains.
- cuVS fuses distance evaluation with top-1 reduction and updates centers with keyed reductions. The array-API code materializes score tiles and builds about 400 one-hot membership tiles per iteration.
- Larger one-hot tiles plus argmin-and-gather make 12 Lloyd iterations 2.0x to 2.5x faster on PyTorch and 2.0x to 2.2x faster on CuPy, with unchanged final inertia.
- A compiled PyTorch assignment plus native `index_add_` is faster than the cuML times in 011. Device-resident cuML remains faster at 550 and 3000 clusters.
- The next implementation step is the portable tile change, followed by an optional native centroid-update hook and cached compiled assignment.

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
