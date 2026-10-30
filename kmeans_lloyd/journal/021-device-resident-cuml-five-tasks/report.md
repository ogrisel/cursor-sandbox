# 021 — device-resident cuML on the original five tasks

[015](../015-native-backend-estimator-benchmark/report.md) timed cuML on a NumPy array, so those cells include the host-to-device copy. [020](../020-balanced-kd-device-resident-cuml/report.md) changed [`_worker_cuml`](https://github.com/ogrisel/cursor-sandbox/blob/8c85d915f5fc2984cfdc7becb38d36beb98a524b/kmeans_lloyd/scripts/bench_task_mix.py#L393-L430) so the timer starts only after the samples and the shared random-row centers are CuPy arrays, and it measured that protocol on `k256-d128` only. This iteration reruns the other five tasks under the same contract. Array-API, stock scikit-learn, and cakedev0 cells are unchanged and stay in 015 and 020.

The full result set is [results.json](results.json). Each task's `.npy` was deleted after its three seeds so the host kept its free-disk headroom.

## Setup

- Same host and limits as 015 and 020: four CPU threads, one NVIDIA L4, float32, TF32 disabled, seeds 0 to 2, `max_iter=12`, `tol=1e-8`, a fresh process per run, and a 60-second worker limit. cuML 26.10.00. Commit [`8c85d91`](https://github.com/ogrisel/cursor-sandbox/commit/8c85d915f5fc2984cfdc7becb38d36beb98a524b).
- Tasks: `k3-d1000` (950,000 × 1000, about 3.54 GiB), `k17-d180` (2,100,000 × 180, about 1.41 GiB), `k100-d32` (1,500,000 × 32), `k550-d6` (525,000 × 6), and `k3000-d2` (135,000 × 2).
- `output_type="cupy"`. The inertia conversion copies centers back to the host after the timed region. The nvidia-smi increment excludes the preallocated device input.

## Full fit

Time in seconds, mean ± sample standard deviation. The 015 column is the published seed mean with the copy inside the timer.

| init | k3-d1000 | k17-d180 | k100-d32 | k550-d6 | k3000-d2 |
| --- | ---: | ---: | ---: | ---: | ---: |
| greedy, 015 | 7.18 | 2.50 | 0.98 | 1.01 | 1.20 |
| greedy, device-resident | 3.849 ± 0.013 | 0.937 ± 0.001 | 0.683 ± 0.003 | 0.876 ± 0.003 | 1.064 ± 0.004 |
| scalable, 015 | 6.38 ± 1.67 | 2.39 | 0.73 | 0.64 | 1.16 |
| scalable, device-resident | 3.238 ± 1.673 | 0.831 ± 0.021 | 0.440 ± 0.001 | 0.515 ± 0.001 | 1.065 ± 0.007 |

The 015 means are slower by 3.33 / 1.56 / 0.30 / 0.13 / 0.14 s on the greedy fits and by 3.14 / 1.56 / 0.29 / 0.13 / 0.10 s on the scalable fits. The gaps follow the input size.

`k3-d1000` scalable seed 1 stops after 2 iterations (1.306 s, inertia 999.974). Seeds 0 and 2 run all 12 iterations (4.201 s and 4.206 s, inertia 999.320 and 998.869). A separate process of seed 1 stops after 2 iterations again, at 1.298 s. The mean includes that early stop, as the 015 mean of 6.38 ± 1.67 s did. The two 12-iteration seeds average 4.20 s.

Against the 015 array-API GPU rows, which were already device-resident:

- At 3 clusters, Torch CUDA generic remains fastest (1.04 s). cuML greedy is 3.85 s and cuML scalable is 3.24 s.
- At 17 clusters, cuML scalable (0.83 s) passes Torch CUDA generic (0.86 s). cuML greedy (0.94 s) is still behind it.
- At 100, 550, and 3000 clusters, cuML scalable stays fastest (0.44 s, 0.51 s, and 1.06 s). Greedy cuML now also beats native Torch CUDA at 100 clusters (0.68 s against 0.79 s). At 3000 clusters greedy and scalable tie at 1.06 s, against 2.00 s for native Torch CUDA.

## Lloyd from the same random rows

| init | k3-d1000 | k17-d180 | k100-d32 | k550-d6 | k3000-d2 |
| --- | ---: | ---: | ---: | ---: | ---: |
| cuML, 015 | 6.88 | 2.12 | 0.54 | 0.35 | 0.32 |
| cuML, device-resident | 3.694 ± 0.023 | 0.525 ± 0.004 | 0.202 ± 0.001 | 0.198 ± 0.001 | 0.160 ± 0.001 |
| fastest array API in 015 | 0.89 | 0.63 | 0.39 | 0.42 | 0.58 |

The 015 Lloyd means are slower by 3.19 / 1.59 / 0.34 / 0.15 / 0.16 s. Removing the copy reverses the ranking at 17 and 100 clusters: cuML is now 0.53 s against 0.63 s, and 0.20 s against 0.39 s. It was already ahead at 550 and 3000 clusters and is now 0.20 s and 0.16 s. At 3 clusters Torch CUDA remains faster (0.89 s against 3.69 s). The copy was about half of the old 6.88 s cell; the remaining gap is the Lloyd kernel.

## Quality and memory

Greedy and shared-start inertias on `k3-d1000`, `k17-d180`, and `k100-d32` agree within 0.11%. On `k550-d6`, scalable is 0.13% below greedy and the shared start is 0.21% above it. On `k3000-d2`, scalable is 5.4% above greedy, and the shared start is 47% above greedy because cuML keeps empty centers. That shared-start gap against the other implementations was 7% in 015 and is a quality result, not a placement result.

nvidia-smi growth above the preallocated input, greedy fits: 54 MiB, 136 MiB, 98 MiB, 56 MiB, and 14 MiB. The 3.8 GiB cuML figure in 015 for `k3-d1000` included allocating the device copy of the 3.54 GiB input.

## Conclusion

The five cuML columns in 015 were the cells affected by the placement change, and they are replaced by this run. `k256-d128` was already device-resident in 020. Initialization-only cuML timings in 015 already copied to the device before the timer and are left as published.

With every GPU contender starting from device-resident data, cuML's shared-start Lloyd is faster from 17 clusters up, and cuML scalable is the fastest full fit from 17 clusters up. The array API remains faster at 3 clusters on both Lloyd and the greedy full fit. The wide-task gap is smaller than 015 reported, and it is still a kernel gap.

Previous: [balanced clusters and features](../020-balanced-kd-device-resident-cuml/report.md).
Index: [journal](../index.md).
