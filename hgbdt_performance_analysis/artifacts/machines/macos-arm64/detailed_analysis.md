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
- Thread grid: `[1, 2, 3, 6, 12]`
- Native profile enabled: `True`

## Setting: `baseline_default`

![scalability-baseline_default](scalability.png)

![absolute-fit-time-baseline_default](fit_time_threads.png)

_Vertical markers denote `cores=3`, `2x=6`, and `4x=12` thread regimes._

### Parity checks (thread=1)

| dataset | model | r2 | fitted_trees | expected_trees | trees_match | total_nodes | avg_nodes_per_tree |
| --- | --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 0.670334 | 220 | 220 | True | 13420 | 61 |
| large | sklearn_hgb | 0.658445 | 220 | 220 | True | 13420 | 61 |
| large | sklearn_hgb_fixed | 0.658445 | 220 | 220 | True | 13420 | 61 |
| large | xgboost_hist | 0.671732 | 220 | 220 | True | 13420 | 61 |
| medium | lightgbm_hist | 0.753709 | 220 | 220 | True | 13420 | 61 |
| medium | sklearn_hgb | 0.746237 | 220 | 220 | True | 13420 | 61 |
| medium | sklearn_hgb_fixed | 0.746237 | 220 | 220 | True | 13420 | 61 |
| medium | xgboost_hist | 0.75389 | 220 | 220 | True | 13420 | 61 |
| small | lightgbm_hist | 0.893078 | 220 | 220 | True | 13420 | 61 |
| small | sklearn_hgb | 0.88762 | 220 | 220 | True | 13420 | 61 |
| small | sklearn_hgb_fixed | 0.88762 | 220 | 220 | True | 13420 | 61 |
| small | xgboost_hist | 0.894341 | 220 | 220 | True | 13420 | 61 |

### Scalability summary (`1 -> cores=3`)

| dataset | model | max_regular_threads | fit_s_1_thread | fit_s_regular_max_threads | speedup_1_to_regular_max |
| --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 3 | 6.55101 | 5.97094 | 1.09715 |
| large | sklearn_hgb | 3 | 6.80019 | 3.27134 | 2.07872 |
| large | sklearn_hgb_fixed | 3 | 6.97552 | 2.91754 | 2.39089 |
| large | xgboost_hist | 3 | 8.41013 | 7.54394 | 1.11482 |
| medium | lightgbm_hist | 3 | 7.365 | 4.86721 | 1.51319 |
| medium | sklearn_hgb | 3 | 6.82315 | 3.69544 | 1.84637 |
| medium | sklearn_hgb_fixed | 3 | 7.30941 | 4.71212 | 1.55119 |
| medium | xgboost_hist | 3 | 7.6959 | 5.22637 | 1.47251 |
| small | lightgbm_hist | 3 | 2.29991 | 2.25361 | 1.02054 |
| small | sklearn_hgb | 3 | 2.28328 | 1.78381 | 1.28 |
| small | sklearn_hgb_fixed | 3 | 2.40795 | 1.67725 | 1.43565 |
| small | xgboost_hist | 3 | 2.68392 | 3.03695 | 0.883756 |

### Oversubscription regime summary (`cores=3`, `2x`, `4x`)

| dataset | model | fit_s_cores | fit_s_2x_cores | fit_s_4x_cores | fit_ratio_2x_vs_cores | fit_ratio_4x_vs_cores |
| --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 5.97094 | 3.39877 | 3.72017 | 0.569219 | 0.623045 |
| large | sklearn_hgb | 3.27134 | 3.97222 | 4.7161 | 1.21425 | 1.44164 |
| large | sklearn_hgb_fixed | 2.91754 | 2.75923 | 2.51015 | 0.945739 | 0.860365 |
| large | xgboost_hist | 7.54394 | 3.95332 | 3.91143 | 0.524039 | 0.518487 |
| medium | lightgbm_hist | 4.86721 | 4.89196 | 6.90924 | 1.00508 | 1.41955 |
| medium | sklearn_hgb | 3.69544 | 3.91457 | 7.61703 | 1.0593 | 2.0612 |
| medium | sklearn_hgb_fixed | 4.71212 | 3.12154 | 5.4614 | 0.66245 | 1.15901 |
| medium | xgboost_hist | 5.22637 | 6.46109 | 5.52638 | 1.23625 | 1.0574 |
| small | lightgbm_hist | 2.25361 | 1.85011 | 1.81657 | 0.820951 | 0.806072 |
| small | sklearn_hgb | 1.78381 | 4.8323 | 3.68225 | 2.70897 | 2.06426 |
| small | sklearn_hgb_fixed | 1.67725 | 2.14397 | 1.23067 | 1.27827 | 0.733741 |
| small | xgboost_hist | 3.03695 | 2.15458 | 1.60622 | 0.709456 | 0.528894 |

### Underperformance findings and root cause analysis

- Root cause signal: Python-level dispatch/orchestration contributes meaningfully to sklearn runtime.
- Issue (single_thread, dataset `large`): Best sklearn total is 1.054x slower than best alternative at thread=1.
  - Implementation plan:
    - Move short-lived orchestration loops to Cython/C-level helpers.
    - Preallocate and reuse temporary buffers in split and histogram kernels.
    - Add lightweight fast paths for small-node splits to bypass heavy orchestration.
- Issue (oversubscription, dataset `large`): At 4x cores, sklearn fit-time ratio vs cores is 0.860 vs 0.623 for best alternative.
  - Implementation plan:
    - Move short-lived orchestration loops to Cython/C-level helpers.
    - Preallocate and reuse temporary buffers in split and histogram kernels.
    - Add lightweight fast paths for small-node splits to bypass heavy orchestration.
- Issue (oversubscription, dataset `medium`): At 4x cores, sklearn fit-time ratio vs cores is 1.478 vs 1.135 for best alternative.
  - Implementation plan:
    - Move short-lived orchestration loops to Cython/C-level helpers.
    - Preallocate and reuse temporary buffers in split and histogram kernels.
    - Add lightweight fast paths for small-node splits to bypass heavy orchestration.

## Setting: `deep_few_trees`

![scalability-deep_few_trees](scalability_deep_few_trees.png)

![absolute-fit-time-deep_few_trees](fit_time_threads_deep_few_trees.png)

_Vertical markers denote `cores=3`, `2x=6`, and `4x=12` thread regimes._

### Parity checks (thread=1)

| dataset | model | r2 | fitted_trees | expected_trees | trees_match | total_nodes | avg_nodes_per_tree |
| --- | --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 0.490012 | 48 | 48 | True | 12144 | 253 |
| large | sklearn_hgb | 0.488521 | 48 | 48 | True | 12144 | 253 |
| large | sklearn_hgb_fixed | 0.488521 | 48 | 48 | True | 12144 | 253 |
| large | xgboost_hist | 0.489088 | 48 | 48 | True | 12144 | 253 |
| medium | lightgbm_hist | 0.56851 | 48 | 48 | True | 12144 | 253 |
| medium | sklearn_hgb | 0.568235 | 48 | 48 | True | 12144 | 253 |
| medium | sklearn_hgb_fixed | 0.568235 | 48 | 48 | True | 12144 | 253 |
| medium | xgboost_hist | 0.568178 | 48 | 48 | True | 12144 | 253 |
| small | lightgbm_hist | 0.749752 | 48 | 48 | True | 12144 | 253 |
| small | sklearn_hgb | 0.751461 | 48 | 48 | True | 12144 | 253 |
| small | sklearn_hgb_fixed | 0.751461 | 48 | 48 | True | 12144 | 253 |
| small | xgboost_hist | 0.752362 | 48 | 48 | True | 12144 | 253 |

### Scalability summary (`1 -> cores=3`)

| dataset | model | max_regular_threads | fit_s_1_thread | fit_s_regular_max_threads | speedup_1_to_regular_max |
| --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 3 | 6.82629 | 3.76954 | 1.81091 |
| large | sklearn_hgb | 3 | 7.53978 | 3.81173 | 1.97804 |
| large | sklearn_hgb_fixed | 3 | 7.52049 | 3.54489 | 2.1215 |
| large | xgboost_hist | 3 | 7.62314 | 3.98212 | 1.91434 |
| medium | lightgbm_hist | 3 | 3.98004 | 2.4007 | 1.65787 |
| medium | sklearn_hgb | 3 | 4.35726 | 1.86695 | 2.33389 |
| medium | sklearn_hgb_fixed | 3 | 4.27206 | 1.92269 | 2.22191 |
| medium | xgboost_hist | 3 | 4.45558 | 2.6892 | 1.65684 |
| small | lightgbm_hist | 3 | 0.909141 | 0.963743 | 0.943343 |
| small | sklearn_hgb | 3 | 1.18348 | 0.660433 | 1.79198 |
| small | sklearn_hgb_fixed | 3 | 1.21143 | 0.673212 | 1.79947 |
| small | xgboost_hist | 3 | 1.38894 | 1.17422 | 1.18286 |

### Oversubscription regime summary (`cores=3`, `2x`, `4x`)

| dataset | model | fit_s_cores | fit_s_2x_cores | fit_s_4x_cores | fit_ratio_2x_vs_cores | fit_ratio_4x_vs_cores |
| --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 3.76954 | 3.99649 | 5.08667 | 1.06021 | 1.34942 |
| large | sklearn_hgb | 3.81173 | 4.38256 | 5.7211 | 1.14975 | 1.50092 |
| large | sklearn_hgb_fixed | 3.54489 | 3.49424 | 3.6525 | 0.985713 | 1.03035 |
| large | xgboost_hist | 3.98212 | 4.01096 | 3.95891 | 1.00724 | 0.994171 |
| medium | lightgbm_hist | 2.4007 | 2.8501 | 2.70098 | 1.1872 | 1.12508 |
| medium | sklearn_hgb | 1.86695 | 2.83968 | 3.87971 | 1.52102 | 2.0781 |
| medium | sklearn_hgb_fixed | 1.92269 | 1.96379 | 1.96453 | 1.02137 | 1.02176 |
| medium | xgboost_hist | 2.6892 | 2.8247 | 2.72628 | 1.05039 | 1.01379 |
| small | lightgbm_hist | 0.963743 | 1.1298 | 1.41146 | 1.1723 | 1.46456 |
| small | sklearn_hgb | 0.660433 | 1.79805 | 2.81549 | 2.72253 | 4.2631 |
| small | sklearn_hgb_fixed | 0.673212 | 0.867231 | 0.623066 | 1.2882 | 0.925511 |
| small | xgboost_hist | 1.17422 | 1.18025 | 1.199 | 1.00513 | 1.0211 |

### Underperformance findings and root cause analysis

- Root cause signal: Python-level dispatch/orchestration contributes meaningfully to sklearn runtime.
- Issue (single_thread, dataset `large`): Best sklearn total is 1.096x slower than best alternative at thread=1.
  - Implementation plan:
    - Move short-lived orchestration loops to Cython/C-level helpers.
    - Preallocate and reuse temporary buffers in split and histogram kernels.
    - Add lightweight fast paths for small-node splits to bypass heavy orchestration.
- Issue (single_thread, dataset `medium`): Best sklearn total is 1.070x slower than best alternative at thread=1.
  - Implementation plan:
    - Move short-lived orchestration loops to Cython/C-level helpers.
    - Preallocate and reuse temporary buffers in split and histogram kernels.
    - Add lightweight fast paths for small-node splits to bypass heavy orchestration.
- Issue (single_thread, dataset `small`): Best sklearn total is 1.296x slower than best alternative at thread=1.
  - Implementation plan:
    - Move short-lived orchestration loops to Cython/C-level helpers.
    - Preallocate and reuse temporary buffers in split and histogram kernels.
    - Add lightweight fast paths for small-node splits to bypass heavy orchestration.

