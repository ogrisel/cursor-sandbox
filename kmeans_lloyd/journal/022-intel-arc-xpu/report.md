# 022 — PyTorch XPU and the CPU contenders on Arc B390

[015](../015-native-backend-estimator-benchmark/report.md) through [021](../021-device-resident-cuml-five-tasks/report.md) timed this six-task mix on one NVIDIA L4 host. This entry repeats the same tasks on a laptop: PyTorch on the integrated Arc GPU, PyTorch on the CPU, stock scikit-learn, and cakedev0's optimized scikit-learn. There is no CUDA device here, so CuPy and cuML are absent. Seed-level rows are in [runs.jsonl](runs.jsonl). Means are in [results.json](results.json).

## Setup

- Host `xps-ultra-x7`: Intel Core Ultra X7 358H, 16 physical cores (4 P-cores up to 4.8 GHz, then 8 and 4 slower cores), 30 GiB RAM. The CPU governor is `powersave` with energy-performance preference `balance_performance`, and the laptop is on AC power.
- CPU contenders are pinned to CPUs 0–3. PyTorch CPU and both scikit-learn builds use 4 threads (`OMP_NUM_THREADS`, `MKL_NUM_THREADS`, `OPENBLAS_NUM_THREADS`, and `torch.set_num_threads`). XPU workers are left unpinned so the Level Zero runtime can use the rest of the host.
- GPU: Intel Arc B390, 96 execution units, driver 1.17.39395, PyTorch 2.11.0+xpu. Float32 matmul precision is `highest`. The timed region is a `torch.xpu` event pair, and the memory figure is the XPU allocator peak above the input that was already on the device.
- Stock scikit-learn is 1.9.1. cakedev0 is scikit-learn 1.10.dev0 at [`7e26a5c`](https://github.com/cakedev0/scikit-learn/commit/7e26a5c37e1fa8031bef7da0ee43b633b07c8b9b), the same PRs 23 and 26 build as on the L4 host. The L4 journal's stock build was 1.7.2. This host uses 1.9.1 because the estimator imports `check_same_namespace`, which 1.7.2 does not provide.
- Tasks, dtype, and stopping rule match the earlier journals: float32, seeds 0–2, greedy k-means++ or the shared random-row centers, `max_iter=12`, `tol=1e-8`. Each XPU shape gets one discarded warmup process so the timed seeds exclude one-time kernel compilation.
- "Native" on XPU is `index_add_` plus `bincount` at every shape. The CUDA rule that keeps the one-hot update when `16 * k < d` is not applied on XPU. "Generic" forces that portable one-hot update.
- The worker limit is 60 s, and 90 s for the repeated `k3-d1000` and `k17-d180` cells. Every run finished. `k550-d6` was measured again after a compile on the other cores overlapped the first pass. `k3-d1000` and `k17-d180` for native XPU, stock scikit-learn, and cakedev0 were measured again after the first pass showed large seed spreads; the tables use that second pass. The generated arrays, about 5.3 GiB, are in `~/task-mix-data-v4`.

## Full fit from greedy k-means++

Time in seconds, mean ± sample standard deviation. **Bold** is the fastest mean in that hardware group.

| implementation | k3-d1000 | k17-d180 | k100-d32 | k256-d128 | k550-d6 | k3000-d2 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Torch CPU, native | **4.99 ± 0.06** | 3.82 ± 0.07 | 5.12 ± 0.10 | 1.85 ± 0.04 | 5.98 ± 0.17 | 17.06 ± 0.19 |
| Torch CPU, generic | 5.01 ± 0.19 | 4.16 ± 0.29 | 5.79 ± 0.05 | 2.32 ± 0.01 | 7.61 ± 0.11 | 20.49 ± 0.26 |
| scikit-learn 1.9.1 | 33.12 ± 6.69 | 7.31 ± 0.23 | 8.95 ± 0.07 | 5.72 ± 0.01 | 10.26 ± 0.03 | 13.67 ± 0.67 |
| cakedev0 PRs 23+26 | 9.01 ± 0.22 | **2.35 ± 0.10** | **1.92 ± 0.04** | **1.06 ± 0.02** | **2.18 ± 0.01** | **3.01 ± 0.01** |
| Torch XPU, native | 4.45 ± 0.00 | 3.36 ± 0.01 | 2.98 ± 0.01 | 2.05 ± 0.01 | **4.02 ± 0.01** | **4.88 ± 0.03** |
| Torch XPU, generic | **3.22 ± 0.25** | **2.83 ± 0.43** | **2.78 ± 0.01** | **1.87 ± 0.01** | 4.07 ± 0.01 | 4.97 ± 0.01 |

- On the Arc GPU the one-hot update is faster through 256 clusters. At 3 clusters it takes 3.22 s against 4.45 s for `index_add_`. At 550 and 3000 clusters the two updates are within 0.1 s, with native ahead by 4.02 s against 4.07 s and 4.88 s against 4.97 s.
- The CUDA cutoff (`16 * k < d`) would select the one-hot update only for `k3-d1000`. On `k17-d180` it would select `index_add_`, which is the slower XPU update (3.36 s against 2.83 s).
- XPU with the one-hot update is the fastest full fit at 3 clusters: 3.22 s, against 4.99 s for native Torch CPU and 9.01 s for cakedev0. From 17 clusters up, cakedev0 is the fastest full fit.
- Native Torch CPU beats the portable update on every full fit. The gap is small at 3 clusters (4.99 s against 5.01 s) and grows with `k` (17.06 s against 20.49 s at 3000 clusters). cakedev0 is still 1.7× to 5.7× faster than native Torch CPU from 17 clusters up.
- Stock scikit-learn's full fit at 3 clusters is 33.12 ± 6.69 s (seeds 36.5 s, 25.4 s, 37.4 s). Its shared-start Lloyd on the same task is 8.53 s, so the spread is the greedy initializer. cakedev0's full fit on that task is 9.01 ± 0.22 s.

## Lloyd from the same random rows

| implementation | k3-d1000 | k17-d180 | k100-d32 | k256-d128 | k550-d6 | k3000-d2 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Torch CPU, native | 4.55 ± 0.27 | 2.66 ± 0.01 | 1.69 ± 0.11 | 1.13 ± 0.00 | 1.92 ± 0.00 | 10.62 ± 0.38 |
| Torch CPU, generic | **4.33 ± 0.15** | 2.83 ± 0.16 | 2.34 ± 0.11 | 1.57 ± 0.06 | 3.37 ± 0.02 | 13.23 ± 0.96 |
| scikit-learn 1.9.1 | 8.53 ± 0.19 | **1.80 ± 0.02** | **0.88 ± 0.00** | 0.47 ± 0.01 | **1.13 ± 0.00** | **1.59 ± 0.00** |
| cakedev0 PRs 23+26 | 8.64 ± 0.22 | **1.80 ± 0.02** | 0.95 ± 0.01 | **0.46 ± 0.00** | 1.20 ± 0.01 | 1.63 ± 0.01 |
| Torch XPU, native | 4.18 ± 0.00 | 2.95 ± 0.00 | 2.24 ± 0.00 | 1.66 ± 0.00 | **2.68 ± 0.01** | **3.08 ± 0.01** |
| Torch XPU, generic | **3.15 ± 0.47** | **2.23 ± 0.15** | **2.05 ± 0.00** | **1.48 ± 0.00** | 2.73 ± 0.00 | 3.29 ± 0.01 |

Shared-start Lloyd removes the initializer. Stock scikit-learn and cakedev0 then agree: 8.53 s against 8.64 s at 3 clusters, 1.80 s against 1.80 s at 17, 0.88 s against 0.95 s at 100, 0.47 s against 0.46 s at 256, 1.13 s against 1.20 s at 550, and 1.59 s against 1.63 s at 3000. cakedev0's full-fit lead is the k-means++ work in PR 23. The chunked Lloyd kernel in PR 26 matches stock Lloyd on this host, as it did on the L4 host.

XPU Lloyd is fastest at 3 clusters (3.15 s with the one-hot update). From 17 clusters up the Cython Lloyd kernel is faster. At 3000 clusters native XPU takes 3.08 s and native Torch CPU takes 10.62 s, while both scikit-learn builds take about 1.6 s.

## Quality and memory

Greedy inertias agree across the six implementations. On `k3-d1000` every greedy mean is 998.867. On `k256-d128` they sit between 118.919 and 118.930. On `k3000-d2` every greedy mean is 0.0181 and every shared-start mean is 0.0248, 37% higher, for Torch, both scikit-learn builds, and both XPU updates together. That gap is the shared random-row start.

Peak memory above the input, greedy full fits:

| implementation | k3-d1000 | k17-d180 | k100-d32 | k256-d128 | k550-d6 | k3000-d2 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Torch CPU | 944 MiB | 2075 MiB | 386 MiB | 156 MiB | 157 MiB | 53 MiB |
| Torch XPU | 939 MiB | 2051 MiB | 368 MiB | 148 MiB | 98 MiB | 68 MiB |
| scikit-learn and cakedev0 | 7248 MiB | 2884 MiB | 366 MiB | 147 MiB | 59 MiB | 16 MiB |

The XPU figure is the device-allocator peak after the input copy. On this shared-memory GPU that copy also occupies system RAM; it is outside the timed region and outside the increment, same as the device-resident CUDA measurements. The 7.1 GiB scikit-learn peak on `k3-d1000` matches the L4 host.

## Conclusion

On this Arc B390 the portable one-hot update is the faster PyTorch XPU path through 256 clusters, and `index_add_` is only a small win at 550 and 3000. The CUDA few-cluster cutoff would keep the slower update on `k17-d180`. With the one-hot update, XPU is the fastest full fit at 3 clusters (3.22 s). From 17 clusters up, cakedev0 is the fastest full fit, and the gap against stock scikit-learn is initialization. Cython Lloyd stays ahead of XPU Lloyd from 17 clusters up.

Previous: [device-resident cuML on the original five tasks](../021-device-resident-cuml-five-tasks/report.md).
Index: [journal](../index.md).
