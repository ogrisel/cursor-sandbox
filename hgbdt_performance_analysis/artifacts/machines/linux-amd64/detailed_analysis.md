# Detailed platform analysis: linux-amd64

- System: `Linux`
- Architecture: `x86_64`
- CPU count (logical): `4`
- CPU count (physical): `2`
- Hyper-threading enabled: `True`
- CPU model: `AMD EPYC 7763 64-Core Processor`
- Core type counts: `{'performance': 4, 'efficiency': None, 'low_power': None}`
- CFS/CPU quota: `n/a`
- CPU set: `0-3`
- Thread grid: `[1, 2, 4, 8]`
- Native profile enabled: `True`

## Setting: `baseline_default`

![scalability-baseline_default](scalability.png)

![absolute-fit-time-baseline_default](fit_time_threads.png)

_Vertical markers denote `cores=4` and `2x=8` thread regimes._

### Parity checks (thread=1)

| dataset | model | r2 | fitted_trees | expected_trees | trees_match | total_nodes | avg_nodes_per_tree |
| --- | --- | --- | --- | --- | --- | --- | --- |
| medium | lightgbm_hist | 0.508565 | 220 | 220 | True | 6114 | 27.7909 |
| medium | sklearn_hgb | 0.434502 | 220 | 220 | True | 7040 | 32 |
| medium | sklearn_hgb_fixed | 0.434502 | 220 | 220 | True | 7040 | 32 |
| medium | xgboost_hist | 0.47647 | 220 | 220 | True | 6168 | 28.0364 |
| small | lightgbm_hist | 0.866811 | 220 | 220 | True | 8348 | 37.9455 |
| small | sklearn_hgb | 0.838229 | 220 | 220 | True | 9210 | 41.8636 |
| small | sklearn_hgb_fixed | 0.838229 | 220 | 220 | True | 9210 | 41.8636 |
| small | xgboost_hist | 0.879536 | 220 | 220 | True | 8248 | 37.4909 |

### Scalability summary (`1 -> cores=4`)

| dataset | model | max_regular_threads | fit_s_1_thread | fit_s_regular_max_threads | speedup_1_to_regular_max |
| --- | --- | --- | --- | --- | --- |
| medium | lightgbm_hist | 4 | 0.549469 | 0.214867 | 2.55725 |
| medium | sklearn_hgb | 4 | 0.767379 | 0.555417 | 1.38163 |
| medium | sklearn_hgb_fixed | 4 | 0.774354 | 0.553657 | 1.39862 |
| medium | xgboost_hist | 4 | 1.38104 | 0.851856 | 1.62122 |
| small | lightgbm_hist | 4 | 0.237123 | 0.118473 | 2.00149 |
| small | sklearn_hgb | 4 | 0.317431 | 0.313828 | 1.01148 |
| small | sklearn_hgb_fixed | 4 | 0.32018 | 0.314647 | 1.01758 |
| small | xgboost_hist | 4 | 0.421539 | 0.301237 | 1.39936 |

### Oversubscription regime summary (`cores=4`, `2x`)

| dataset | model | fit_s_cores | fit_s_2x_cores | fit_ratio_2x_vs_cores |
| --- | --- | --- | --- | --- |
| medium | lightgbm_hist | 0.214867 | 0.902898 | 4.20212 |
| medium | sklearn_hgb | 0.555417 | 2.54598 | 4.58391 |
| medium | sklearn_hgb_fixed | 0.553657 | 0.558282 | 1.00835 |
| medium | xgboost_hist | 0.851856 | 0.909197 | 1.06731 |
| small | lightgbm_hist | 0.118473 | 1.00992 | 8.52448 |
| small | sklearn_hgb | 0.313828 | 2.84028 | 9.05045 |
| small | sklearn_hgb_fixed | 0.314647 | 0.317556 | 1.00924 |
| small | xgboost_hist | 0.301237 | 0.341558 | 1.13385 |

### Underperformance findings and root cause analysis

- Root cause signal: Python-level dispatch/orchestration contributes meaningfully to sklearn runtime.
- Issue (single_thread, dataset `medium`): Best sklearn total is 1.268x slower than best alternative at thread=1.
  - Implementation plan:
    - Move short-lived orchestration loops to Cython/C-level helpers.
    - Preallocate and reuse temporary buffers in split and histogram kernels.
    - Add lightweight fast paths for small-node splits to bypass heavy orchestration.
- Issue (scalability, dataset `medium`): Best sklearn speedup trails best alternative by 1.159 (1->regular max threads).
  - Implementation plan:
    - Move short-lived orchestration loops to Cython/C-level helpers.
    - Preallocate and reuse temporary buffers in split and histogram kernels.
    - Add lightweight fast paths for small-node splits to bypass heavy orchestration.
- Issue (scalability, dataset `small`): Best sklearn speedup trails best alternative by 0.984 (1->regular max threads).
  - Implementation plan:
    - Move short-lived orchestration loops to Cython/C-level helpers.
    - Preallocate and reuse temporary buffers in split and histogram kernels.
    - Add lightweight fast paths for small-node splits to bypass heavy orchestration.

