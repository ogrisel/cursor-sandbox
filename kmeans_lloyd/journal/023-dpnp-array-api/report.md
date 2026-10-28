# 023 — dpnp array API on Arc B390

[022](../022-intel-arc-xpu/report.md) timed PyTorch XPU, PyTorch CPU, stock scikit-learn 1.9.1, and cakedev0 on this laptop. This entry adds the same estimator on dpnp GPU arrays, using the portable one-hot centroid update. The 022 rows are unchanged. Seed-level rows are in [runs.jsonl](runs.jsonl). Means are in [results.json](results.json).

## Setup

- Same host, tasks, dtype, seeds, and stopping rule as 022: `xps-ultra-x7`, Intel Arc B390, float32, seeds 0–2, greedy k-means++ or the shared random-row centers, `max_iter=12`, `tol=1e-8`, a fresh process per run.
- dpnp 0.19.1+1.gcc1019cbc92 and dpctl 0.21.1. Samples and the shared centers are copied with `dpnp.asarray(..., device="gpu")`, which selects the Level Zero Arc B390. The worker is left unpinned. The timed region is `perf_counter` between `sycl_queue.wait()` calls, so the host-to-device copy sits outside the timer. The memory figure is host VmHWM above that copy.
- `native_accumulate` returns `None` for dpnp, so every cell is the portable one-hot update. There is no scatter-add variant to compare.
- Each shape and initializer gets one discarded warmup process, as the XPU cells did in 022. The worker limit is 90 s. Every run finished. The first `k3-d1000` pass still had a cold seed 0 (9.48 s greedy, 8.96 s shared-start). That task was measured again after the other shapes; the tables use the second pass. The generated arrays, about 5.3 GiB, remain at `~/task-mix-data-v4`.

## Full fit from greedy k-means++

Time in seconds, mean ± sample standard deviation. The non-dpnp rows are the 022 means. **Bold** is the fastest mean in the column.

| implementation | k3-d1000 | k17-d180 | k100-d32 | k256-d128 | k550-d6 | k3000-d2 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| dpnp, portable | 4.83 ± 0.17 | 2.57 ± 0.09 | 2.71 ± 0.04 | 1.11 ± 0.01 | 5.74 ± 0.14 | 11.28 ± 0.82 |
| Torch XPU, generic | **3.22 ± 0.25** | 2.83 ± 0.43 | 2.78 ± 0.01 | 1.87 ± 0.01 | 4.07 ± 0.01 | 4.97 ± 0.01 |
| Torch XPU, native | 4.45 ± 0.00 | 3.36 ± 0.01 | 2.98 ± 0.01 | 2.05 ± 0.01 | 4.02 ± 0.01 | 4.88 ± 0.03 |
| Torch CPU, native | 4.99 ± 0.06 | 3.82 ± 0.07 | 5.12 ± 0.10 | 1.85 ± 0.04 | 5.98 ± 0.17 | 17.06 ± 0.19 |
| scikit-learn 1.9.1 | 33.12 ± 6.69 | 7.31 ± 0.23 | 8.95 ± 0.07 | 5.72 ± 0.01 | 10.26 ± 0.03 | 13.67 ± 0.67 |
| cakedev0 PRs 23+26 | 9.01 ± 0.22 | **2.35 ± 0.10** | **1.92 ± 0.04** | **1.06 ± 0.02** | **2.18 ± 0.01** | **3.01 ± 0.01** |

- dpnp and Torch XPU generic run the same one-hot update. dpnp is faster at 17 clusters (2.57 s against 2.83 s) and at 256 (1.11 s against 1.87 s). At 100 clusters the two are within 0.1 s (2.71 s against 2.78 s). XPU is faster at 3 clusters (3.22 s against 4.83 s), at 550 (4.07 s against 5.74 s), and at 3000 (4.97 s against 11.28 s).
- dpnp is faster than native Torch CPU on every full fit. The gap is 4.83 s against 4.99 s at 3 clusters and 5.74 s against 5.98 s at 550, and it widens at 100 clusters (2.71 s against 5.12 s) and at 3000 (11.28 s against 17.06 s).
- cakedev0 remains the fastest full fit from 17 clusters up. dpnp is second at 17 clusters (2.57 s against 2.35 s) and at 256 (1.11 s against 1.06 s). At 3 clusters the fastest fit is still the XPU one-hot update, at 3.22 s; dpnp takes 4.83 s and cakedev0 takes 9.01 s.
- The `k3000-d2` greedy seeds are 10.89 s, 10.74 s, and 12.22 s, all 12 iterations, with inertia 0.0182. Shared-start Lloyd on that task is 4.83 ± 0.07 s, so the full-fit spread includes the greedy initializer.

## Lloyd from the same random rows

| implementation | k3-d1000 | k17-d180 | k100-d32 | k256-d128 | k550-d6 | k3000-d2 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| dpnp, portable | 4.20 ± 0.16 | 2.11 ± 0.07 | 1.95 ± 0.17 | 0.47 ± 0.01 | 3.56 ± 0.11 | 4.83 ± 0.07 |
| Torch XPU, generic | **3.15 ± 0.47** | 2.23 ± 0.15 | 2.05 ± 0.00 | 1.48 ± 0.00 | 2.73 ± 0.00 | 3.29 ± 0.01 |
| Torch XPU, native | 4.18 ± 0.00 | 2.95 ± 0.00 | 2.24 ± 0.00 | 1.66 ± 0.00 | 2.68 ± 0.01 | 3.08 ± 0.01 |
| Torch CPU, native | 4.55 ± 0.27 | 2.66 ± 0.01 | 1.69 ± 0.11 | 1.13 ± 0.00 | 1.92 ± 0.00 | 10.62 ± 0.38 |
| scikit-learn 1.9.1 | 8.53 ± 0.19 | **1.80 ± 0.02** | **0.88 ± 0.00** | 0.47 ± 0.01 | **1.13 ± 0.00** | **1.59 ± 0.00** |
| cakedev0 PRs 23+26 | 8.64 ± 0.22 | **1.80 ± 0.02** | 0.95 ± 0.01 | **0.46 ± 0.00** | 1.20 ± 0.01 | 1.63 ± 0.01 |

At 256 clusters dpnp Lloyd takes 0.47 s, level with stock scikit-learn (0.47 s) and cakedev0 (0.46 s), and ahead of the XPU one-hot update (1.48 s). At 3 clusters dpnp takes 4.20 s, ahead of both scikit-learn builds (8.53 s and 8.64 s) and native Torch CPU (4.55 s). The XPU one-hot update is still faster there, at 3.15 s.

From 17 clusters up, Cython Lloyd is faster except at 256 clusters, where the three times agree. At 3000 clusters dpnp takes 4.83 s and native XPU takes 3.08 s, while both scikit-learn builds take about 1.6 s.

## Quality and memory

Greedy inertias match the 022 table. On `k3-d1000` the dpnp mean is 998.867. On `k256-d128` it is 118.923. On `k3000-d2` the greedy mean is 0.0182 and the shared-start mean is 0.0248, 37% higher, the same gap 022 reported for every implementation there.

The recorded VmHWM increments are 22–120 MiB. On `k3-d1000` the 3.54 GiB copy already sets the high-water mark, so the later one-hot tiles do not raise it and the 26 MiB increment understates the working set. These figures are host RSS deltas, separate from the XPU allocator peaks in 022.

## Conclusion

On this Arc B390 the portable dpnp path is faster than native Torch CPU on every full fit, and it matches Cython Lloyd at 256 clusters (0.47 s). It is also faster than the XPU one-hot update at 17 and 256 clusters. The XPU one-hot update stays ahead at 3 clusters (3.22 s against 4.83 s). From 17 clusters up, cakedev0 remains the fastest full fit. At 550 and 3000 clusters both XPU updates and Cython Lloyd are faster than dpnp.

Previous: [PyTorch XPU on Arc B390](../022-intel-arc-xpu/report.md).
Index: [journal](../index.md).
