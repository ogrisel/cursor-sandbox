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
| medium | lightgbm_hist | 0.670972 | 220 | 220 | True | 13420 | 61 |
| medium | sklearn_hgb | 0.662975 | 220 | 220 | True | 13420 | 61 |
| medium | sklearn_hgb_fixed | 0.662975 | 220 | 220 | True | 13420 | 61 |
| medium | xgboost_hist | 0.670433 | 220 | 220 | True | 13420 | 61 |
| small | lightgbm_hist | 0.949369 | 220 | 220 | True | 13386 | 60.8455 |
| small | sklearn_hgb | 0.942299 | 220 | 220 | True | 13414 | 60.9727 |
| small | sklearn_hgb_fixed | 0.942299 | 220 | 220 | True | 13414 | 60.9727 |
| small | xgboost_hist | 0.949753 | 220 | 220 | True | 13390 | 60.8636 |

### Scalability summary (`1 -> cores=3`)

| dataset | model | max_regular_threads | fit_s_1_thread | fit_s_regular_max_threads | speedup_1_to_regular_max |
| --- | --- | --- | --- | --- | --- |
| medium | lightgbm_hist | 3 | 15.0258 | 6.54178 | 2.2969 |
| medium | sklearn_hgb | 3 | 14.2668 | 6.67812 | 2.13635 |
| medium | sklearn_hgb_fixed | 3 | 14.0204 | 7.47127 | 1.87658 |
| medium | xgboost_hist | 3 | 15.495 | 6.83123 | 2.26826 |
| small | lightgbm_hist | 3 | 0.506795 | 0.842401 | 0.601608 |
| small | sklearn_hgb | 3 | 0.839609 | 0.440812 | 1.90469 |
| small | sklearn_hgb_fixed | 3 | 0.912365 | 0.620242 | 1.47098 |
| small | xgboost_hist | 3 | 0.880403 | 1.6338 | 0.538868 |

### Oversubscription regime summary (`cores=3`, `2x`)

| dataset | model | fit_s_cores | fit_s_2x_cores | fit_ratio_2x_vs_cores |
| --- | --- | --- | --- | --- |
| medium | lightgbm_hist | 6.54178 | 6.83115 | 1.04423 |
| medium | sklearn_hgb | 6.67812 | 6.04917 | 0.905819 |
| medium | sklearn_hgb_fixed | 7.47127 | 5.41001 | 0.724109 |
| medium | xgboost_hist | 6.83123 | 6.5456 | 0.958187 |
| small | lightgbm_hist | 0.842401 | 1.84042 | 2.18473 |
| small | sklearn_hgb | 0.440812 | 2.90477 | 6.58958 |
| small | sklearn_hgb_fixed | 0.620242 | 0.565359 | 0.911512 |
| small | xgboost_hist | 1.6338 | 0.874809 | 0.535444 |

### Underperformance findings and root cause analysis

- Root cause signal: Python-level dispatch/orchestration contributes meaningfully to sklearn runtime.
- Issue (single_thread, dataset `small`): Best sklearn total is 1.436x slower than best alternative at thread=1.
  - Implementation plan:
    - Move short-lived orchestration loops to Cython/C-level helpers.
    - Preallocate and reuse temporary buffers in split and histogram kernels.
    - Add lightweight fast paths for small-node splits to bypass heavy orchestration.
- Issue (oversubscription, dataset `small`): At 2x cores, sklearn fit-time ratio vs cores is 1.283 vs 1.038 for best alternative.
  - Implementation plan:
    - Move short-lived orchestration loops to Cython/C-level helpers.
    - Preallocate and reuse temporary buffers in split and histogram kernels.
    - Add lightweight fast paths for small-node splits to bypass heavy orchestration.

