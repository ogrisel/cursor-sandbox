# Detailed platform analysis: windows-amd64

- System: `Windows`
- Architecture: `AMD64`
- CPU count (logical): `4`
- CPU count (physical): `2`
- Hyper-threading enabled: `True`
- CPU model: `AMD EPYC 7763 64-Core Processor`
- Core type counts: `{'performance': None, 'efficiency': None, 'low_power': None}`
- CFS/CPU quota: `n/a`
- CPU set: `n/a`
- Thread grid: `[1, 4, 8]`
- Native profile enabled: `False`

## Setting: `baseline_default`

![scalability-baseline_default](scalability.png)

![absolute-fit-time-baseline_default](fit_time_threads.png)

_Vertical markers denote `cores=4` and `2x=8` thread regimes._

### Parity checks (thread=1)

| dataset | model | r2 | fitted_trees | expected_trees | trees_match | total_nodes | avg_nodes_per_tree |
| --- | --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 0.586641 | 220 | 220 | True | 11256 | 51.1636 |
| large | sklearn_hgb | 0.529888 | 220 | 220 | True | 12398 | 56.3545 |
| large | sklearn_hgb_fixed | 0.529888 | 220 | 220 | True | 12398 | 56.3545 |
| large | xgboost_hist | 0.593432 | 220 | 220 | True | 11426 | 51.9364 |
| small | lightgbm_hist | 0.949369 | 220 | 220 | True | 13386 | 60.8455 |
| small | sklearn_hgb | 0.942299 | 220 | 220 | True | 13414 | 60.9727 |
| small | sklearn_hgb_fixed | 0.942299 | 220 | 220 | True | 13414 | 60.9727 |
| small | xgboost_hist | 0.948866 | 220 | 220 | True | 13394 | 60.8818 |

### Scalability summary (`1 -> cores=4`)

| dataset | model | max_regular_threads | fit_s_1_thread | fit_s_regular_max_threads | speedup_1_to_regular_max |
| --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 4 | 1.61168 | 0.67387 | 2.39168 |
| large | sklearn_hgb | 4 | 2.22457 | 1.46896 | 1.51439 |
| large | sklearn_hgb_fixed | 4 | 2.19479 | 1.45767 | 1.50568 |
| large | xgboost_hist | 4 | 2.83257 | 1.85957 | 1.52324 |
| small | lightgbm_hist | 4 | 0.747212 | 0.379384 | 1.96954 |
| small | sklearn_hgb | 4 | 0.922864 | 0.784839 | 1.17586 |
| small | sklearn_hgb_fixed | 4 | 0.931075 | 0.724826 | 1.28455 |
| small | xgboost_hist | 4 | 1.17401 | 0.773893 | 1.51702 |

### Oversubscription regime summary (`cores=4`, `2x`)

| dataset | model | fit_s_cores | fit_s_2x_cores | fit_ratio_2x_vs_cores |
| --- | --- | --- | --- | --- |
| large | lightgbm_hist | 0.67387 | 0.758074 | 1.12496 |
| large | sklearn_hgb | 1.46896 | 1.71576 | 1.16801 |
| large | sklearn_hgb_fixed | 1.45767 | 1.52966 | 1.04938 |
| large | xgboost_hist | 1.85957 | 1.88659 | 1.01453 |
| small | lightgbm_hist | 0.379384 | 0.458337 | 1.20811 |
| small | sklearn_hgb | 0.784839 | 0.993093 | 1.26535 |
| small | sklearn_hgb_fixed | 0.724826 | 0.731951 | 1.00983 |
| small | xgboost_hist | 0.773893 | 0.781645 | 1.01002 |

### Underperformance findings and root cause analysis

- Root cause signal: Python-level dispatch/orchestration contributes meaningfully to sklearn runtime.
- Issue (single_thread, dataset `large`): Best sklearn total is 1.359x slower than best alternative at thread=1.
  - Implementation plan:
    - Move short-lived orchestration loops to Cython/C-level helpers.
    - Preallocate and reuse temporary buffers in split and histogram kernels.
    - Add lightweight fast paths for small-node splits to bypass heavy orchestration.
- Issue (single_thread, dataset `small`): Best sklearn total is 1.261x slower than best alternative at thread=1.
  - Implementation plan:
    - Move short-lived orchestration loops to Cython/C-level helpers.
    - Preallocate and reuse temporary buffers in split and histogram kernels.
    - Add lightweight fast paths for small-node splits to bypass heavy orchestration.
- Issue (scalability, dataset `large`): Best sklearn speedup trails best alternative by 0.877 (1->regular max threads).
  - Implementation plan:
    - Move short-lived orchestration loops to Cython/C-level helpers.
    - Preallocate and reuse temporary buffers in split and histogram kernels.
    - Add lightweight fast paths for small-node splits to bypass heavy orchestration.
- Issue (scalability, dataset `small`): Best sklearn speedup trails best alternative by 0.685 (1->regular max threads).
  - Implementation plan:
    - Move short-lived orchestration loops to Cython/C-level helpers.
    - Preallocate and reuse temporary buffers in split and histogram kernels.
    - Add lightweight fast paths for small-node splits to bypass heavy orchestration.

## Setting: `deep_few_trees`

![scalability-deep_few_trees](scalability_deep_few_trees.png)

![absolute-fit-time-deep_few_trees](fit_time_threads_deep_few_trees.png)

_Vertical markers denote `cores=4` and `2x=8` thread regimes._

### Parity checks (thread=1)

| dataset | model | r2 | fitted_trees | expected_trees | trees_match | total_nodes | avg_nodes_per_tree |
| --- | --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 0.507257 | 48 | 48 | True | 12144 | 253 |
| large | sklearn_hgb | 0.504162 | 48 | 48 | True | 12144 | 253 |
| large | sklearn_hgb_fixed | 0.504162 | 48 | 48 | True | 12144 | 253 |
| large | xgboost_hist | 0.504185 | 48 | 48 | True | 12144 | 253 |
| medium | lightgbm_hist | 0.56851 | 48 | 48 | True | 12144 | 253 |
| medium | sklearn_hgb | 0.568235 | 48 | 48 | True | 12144 | 253 |
| medium | sklearn_hgb_fixed | 0.568235 | 48 | 48 | True | 12144 | 253 |
| medium | xgboost_hist | 0.568178 | 48 | 48 | True | 12144 | 253 |
| small | lightgbm_hist | 0.749752 | 48 | 48 | True | 12144 | 253 |
| small | sklearn_hgb | 0.751461 | 48 | 48 | True | 12144 | 253 |
| small | sklearn_hgb_fixed | 0.751461 | 48 | 48 | True | 12144 | 253 |
| small | xgboost_hist | 0.752362 | 48 | 48 | True | 12144 | 253 |

### Scalability summary (`1 -> cores=4`)

| dataset | model | max_regular_threads | fit_s_1_thread | fit_s_regular_max_threads | speedup_1_to_regular_max |
| --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 4 | 5.1992 | 2.17188 | 2.39387 |
| large | sklearn_hgb | 4 | 6.41499 | 3.54537 | 1.8094 |
| large | sklearn_hgb_fixed | 4 | 6.54147 | 3.53694 | 1.84947 |
| large | xgboost_hist | 4 | 8.77577 | 5.63424 | 1.55758 |
| medium | lightgbm_hist | 4 | 6.62576 | 2.78701 | 2.37737 |
| medium | sklearn_hgb | 4 | 7.27094 | 3.72931 | 1.94967 |
| medium | sklearn_hgb_fixed | 4 | 7.46591 | 3.69216 | 2.0221 |
| medium | xgboost_hist | 4 | 9.04595 | 5.31736 | 1.70121 |
| small | lightgbm_hist | 4 | 1.86703 | 0.852749 | 2.18942 |
| small | sklearn_hgb | 4 | 2.3882 | 1.55149 | 1.53929 |
| small | sklearn_hgb_fixed | 4 | 2.39185 | 1.52459 | 1.56884 |
| small | xgboost_hist | 4 | 3.01496 | 2.0111 | 1.49915 |

### Oversubscription regime summary (`cores=4`, `2x`)

| dataset | model | fit_s_cores | fit_s_2x_cores | fit_ratio_2x_vs_cores |
| --- | --- | --- | --- | --- |
| large | lightgbm_hist | 2.17188 | 2.2459 | 1.03408 |
| large | sklearn_hgb | 3.54537 | 3.97659 | 1.12163 |
| large | sklearn_hgb_fixed | 3.53694 | 3.65635 | 1.03376 |
| large | xgboost_hist | 5.63424 | 5.6238 | 0.998147 |
| medium | lightgbm_hist | 2.78701 | 2.93674 | 1.05373 |
| medium | sklearn_hgb | 3.72931 | 4.00856 | 1.07488 |
| medium | sklearn_hgb_fixed | 3.69216 | 3.70269 | 1.00285 |
| medium | xgboost_hist | 5.31736 | 5.40338 | 1.01618 |
| small | lightgbm_hist | 0.852749 | 0.907564 | 1.06428 |
| small | sklearn_hgb | 1.55149 | 1.87453 | 1.20821 |
| small | sklearn_hgb_fixed | 1.52459 | 1.54887 | 1.01592 |
| small | xgboost_hist | 2.0111 | 2.02142 | 1.00513 |

### Underperformance findings and root cause analysis

- Root cause signal: Python-level dispatch/orchestration contributes meaningfully to sklearn runtime.
- Issue (single_thread, dataset `large`): Best sklearn total is 1.248x slower than best alternative at thread=1.
  - Implementation plan:
    - Move short-lived orchestration loops to Cython/C-level helpers.
    - Preallocate and reuse temporary buffers in split and histogram kernels.
    - Add lightweight fast paths for small-node splits to bypass heavy orchestration.
- Issue (single_thread, dataset `medium`): Best sklearn total is 1.117x slower than best alternative at thread=1.
  - Implementation plan:
    - Move short-lived orchestration loops to Cython/C-level helpers.
    - Preallocate and reuse temporary buffers in split and histogram kernels.
    - Add lightweight fast paths for small-node splits to bypass heavy orchestration.
- Issue (single_thread, dataset `small`): Best sklearn total is 1.294x slower than best alternative at thread=1.
  - Implementation plan:
    - Move short-lived orchestration loops to Cython/C-level helpers.
    - Preallocate and reuse temporary buffers in split and histogram kernels.
    - Add lightweight fast paths for small-node splits to bypass heavy orchestration.
- Issue (scalability, dataset `large`): Best sklearn speedup trails best alternative by 0.544 (1->regular max threads).
  - Implementation plan:
    - Move short-lived orchestration loops to Cython/C-level helpers.
    - Preallocate and reuse temporary buffers in split and histogram kernels.
    - Add lightweight fast paths for small-node splits to bypass heavy orchestration.
- Issue (scalability, dataset `medium`): Best sklearn speedup trails best alternative by 0.355 (1->regular max threads).
  - Implementation plan:
    - Move short-lived orchestration loops to Cython/C-level helpers.
    - Preallocate and reuse temporary buffers in split and histogram kernels.
    - Add lightweight fast paths for small-node splits to bypass heavy orchestration.
- Issue (scalability, dataset `small`): Best sklearn speedup trails best alternative by 0.621 (1->regular max threads).
  - Implementation plan:
    - Move short-lived orchestration loops to Cython/C-level helpers.
    - Preallocate and reuse temporary buffers in split and histogram kernels.
    - Add lightweight fast paths for small-node splits to bypass heavy orchestration.

