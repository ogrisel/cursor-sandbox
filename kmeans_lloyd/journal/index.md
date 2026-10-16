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

[010](010-scalable-initialization/index.html) replaces stochastic empty-center
handling with scikit-learn's farthest-point policy and compares greedy,
scalable, and random initializers. The new array-API k-means|| strategy runs on
PyTorch CPU/CUDA and CuPy. All 84 new workers complete within 60 seconds.

| initializer | 3 clusters | 17 clusters | 100 clusters | 550 clusters | 3000 clusters |
| --- | --- | --- | --- | --- | --- |
| API CUDA, scalable | 0.94 s | 1.67 s | 1.29 s | 1.26 s | 2.58 s |
| API CuPy, scalable | 1.61 s | 2.58 s | 1.93 s | 1.88 s | 4.16 s |
| API CPU, scalable | 18.57 s | 9.46 s | 14.77 s | 36.06 s | 47.09 s |
| cuML, scalable | 0.49 s | 0.27 s | 0.25 s | 0.36 s | 0.91 s |

Main conclusions:

- Farthest-point relocation lowers 3000-cluster inertia by 6.50% relative to
  keeping empty centers and matches scikit-learn within 0.07%.
- Array-API scalable initialization improves no-Lloyd inertia by up to 5.1%
  at 17 and 100 clusters, but costs more than greedy k-means++ and is about 1%
  worse at 550 clusters.
- cuML scalable initialization is fastest or tied from 17 through 3000
  clusters and has the lowest no-Lloyd inertia on every task. Its internal
  candidate consolidation returns refined, non-row centers, unlike the
  row-selecting array-API strategy.
- The tiled Gram schedule remains the practical array-API Lloyd path.
  `torch.compile` can eliminate a tile's distance matrix with a running
  schedule, but that full schedule is slower than eager tiled GEMM.

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
