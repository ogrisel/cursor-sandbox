# Detailed platform analysis: macos-arm64

- System: `Darwin`
- Architecture: `arm64`
- CPU count (logical): `3`
- CPU count (physical): `3`
- Hyper-threading enabled: `False`
- CPU model: `Apple M1 (Virtual)`
- Core type counts: `{'performance': 3, 'efficiency': None, 'low_power': None}`
- CFS/CPU quota: `n/a`
- CPU set: `n/a`
- Thread grid: `[1, 2, 3, 6]`
- Native profile enabled: `True`

## Setting: `baseline_default`

![scalability-baseline_default](scalability.png)

![absolute-fit-time-baseline_default](fit_time_threads.png)

_Vertical markers denote `cores=3` and `2x=6` thread regimes._

### Parity checks (thread=1)

| dataset | model | r2 | fitted_trees | expected_trees | trees_match | total_nodes | avg_nodes_per_tree |
| --- | --- | --- | --- | --- | --- | --- | --- |
| medium | lightgbm_hist | 0.553503 | 220 | 220 | True | 8646 | 39.3 |
| medium | sklearn_hgb | 0.499169 | 220 | 220 | True | 9918 | 45.0818 |
| medium | sklearn_hgb_fixed | 0.499169 | 220 | 220 | True | 9918 | 45.0818 |
| medium | xgboost_hist | 0.561282 | 220 | 220 | True | 8630 | 39.2273 |
| small | lightgbm_hist | 0.949369 | 220 | 220 | True | 13386 | 60.8455 |
| small | sklearn_hgb | 0.942299 | 220 | 220 | True | 13414 | 60.9727 |
| small | sklearn_hgb_fixed | 0.942299 | 220 | 220 | True | 13414 | 60.9727 |
| small | xgboost_hist | 0.949753 | 220 | 220 | True | 13390 | 60.8636 |

### Scalability summary (`1 -> cores=3`)

| dataset | model | max_regular_threads | fit_s_1_thread | fit_s_regular_max_threads | speedup_1_to_regular_max |
| --- | --- | --- | --- | --- | --- |
| medium | lightgbm_hist | 3 | 0.648143 | 1.2213 | 0.530699 |
| medium | sklearn_hgb | 3 | 1.06066 | 2.30073 | 0.461012 |
| medium | sklearn_hgb_fixed | 3 | 0.939276 | 2.10899 | 0.445367 |
| medium | xgboost_hist | 3 | 1.2587 | 2.03043 | 0.619919 |
| small | lightgbm_hist | 3 | 0.446068 | 0.596261 | 0.748109 |
| small | sklearn_hgb | 3 | 0.630643 | 0.534391 | 1.18012 |
| small | sklearn_hgb_fixed | 3 | 0.572623 | 0.565038 | 1.01342 |
| small | xgboost_hist | 3 | 0.676759 | 0.860153 | 0.786789 |

### Oversubscription regime summary (`cores=3`, `2x`)

| dataset | model | fit_s_cores | fit_s_2x_cores | fit_ratio_2x_vs_cores |
| --- | --- | --- | --- | --- |
| medium | lightgbm_hist | 1.2213 | 1.35182 | 1.10687 |
| medium | sklearn_hgb | 2.30073 | 3.54593 | 1.54122 |
| medium | sklearn_hgb_fixed | 2.10899 | 1.27341 | 0.603799 |
| medium | xgboost_hist | 2.03043 | 2.11969 | 1.04396 |
| small | lightgbm_hist | 0.596261 | 1.5048 | 2.52372 |
| small | sklearn_hgb | 0.534391 | 3.26162 | 6.10344 |
| small | sklearn_hgb_fixed | 0.565038 | 1.07754 | 1.90703 |
| small | xgboost_hist | 0.860153 | 1.75578 | 2.04125 |

### Underperformance findings and root cause analysis

- Root cause signal: Python-level dispatch/orchestration contributes meaningfully to sklearn runtime.
- Issue (single_thread, dataset `medium`): Best sklearn total is 1.502x slower than best alternative at thread=1.
  - Implementation plan:
    - Move short-lived orchestration loops to Cython/C-level helpers.
    - Preallocate and reuse temporary buffers in split and histogram kernels.
    - Add lightweight fast paths for small-node splits to bypass heavy orchestration.
- Issue (single_thread, dataset `small`): Best sklearn total is 1.279x slower than best alternative at thread=1.
  - Implementation plan:
    - Move short-lived orchestration loops to Cython/C-level helpers.
    - Preallocate and reuse temporary buffers in split and histogram kernels.
    - Add lightweight fast paths for small-node splits to bypass heavy orchestration.

