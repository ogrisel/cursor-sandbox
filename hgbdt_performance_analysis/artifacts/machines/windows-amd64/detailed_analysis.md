# Detailed platform analysis: windows-amd64

- System: `Windows`
- Architecture: `AMD64`
- CPU count (logical): `4`
- CPU count (physical): `2`
- Hyper-threading enabled: `True`
- CPU model: `Intel(R) Xeon(R) Platinum 8370C CPU @ 2.80GHz`
- Core type counts: `{'performance': None, 'efficiency': None, 'low_power': None}`
- CFS/CPU quota: `n/a`
- CPU set: `n/a`
- Thread grid: `[1, 2, 4, 8]`
- Native profile enabled: `False`

## Setting: `baseline_default`

![scalability-baseline_default](scalability.png)

![absolute-fit-time-baseline_default](fit_time_threads.png)

_Vertical markers denote `cores=4` and `2x=8` thread regimes._

### Parity checks (thread=1)

| dataset | model | r2 | fitted_trees | expected_trees | trees_match | total_nodes | avg_nodes_per_tree |
| --- | --- | --- | --- | --- | --- | --- | --- |
| medium | lightgbm_hist | 0.586641 | 220 | 220 | True | 11256 | 51.1636 |
| medium | sklearn_hgb | 0.529888 | 220 | 220 | True | 12398 | 56.3545 |
| medium | sklearn_hgb_fixed | 0.529888 | 220 | 220 | True | 12398 | 56.3545 |
| medium | xgboost_hist | 0.593432 | 220 | 220 | True | 11426 | 51.9364 |
| small | lightgbm_hist | 0.949369 | 220 | 220 | True | 13386 | 60.8455 |
| small | sklearn_hgb | 0.942299 | 220 | 220 | True | 13414 | 60.9727 |
| small | sklearn_hgb_fixed | 0.942299 | 220 | 220 | True | 13414 | 60.9727 |
| small | xgboost_hist | 0.948866 | 220 | 220 | True | 13394 | 60.8818 |

### Scalability summary (`1 -> cores=4`)

| dataset | model | max_regular_threads | fit_s_1_thread | fit_s_regular_max_threads | speedup_1_to_regular_max |
| --- | --- | --- | --- | --- | --- |
| medium | lightgbm_hist | 4 | 1.53138 | 0.733855 | 2.08676 |
| medium | sklearn_hgb | 4 | 2.28688 | 1.66048 | 1.37724 |
| medium | sklearn_hgb_fixed | 4 | 2.27142 | 1.63523 | 1.38905 |
| medium | xgboost_hist | 4 | 2.81441 | 2.04084 | 1.37904 |
| small | lightgbm_hist | 4 | 0.651413 | 0.393234 | 1.65655 |
| small | sklearn_hgb | 4 | 0.87922 | 0.773673 | 1.13642 |
| small | sklearn_hgb_fixed | 4 | 0.879062 | 0.742918 | 1.18326 |
| small | xgboost_hist | 4 | 1.13572 | 0.82685 | 1.37355 |

### Oversubscription regime summary (`cores=4`, `2x`)

| dataset | model | fit_s_cores | fit_s_2x_cores | fit_ratio_2x_vs_cores |
| --- | --- | --- | --- | --- |
| medium | lightgbm_hist | 0.733855 | 0.827019 | 1.12695 |
| medium | sklearn_hgb | 1.66048 | 2.00169 | 1.20549 |
| medium | sklearn_hgb_fixed | 1.63523 | 1.64071 | 1.00335 |
| medium | xgboost_hist | 2.04084 | 2.00325 | 0.981581 |
| small | lightgbm_hist | 0.393234 | 0.49985 | 1.27112 |
| small | sklearn_hgb | 0.773673 | 1.1069 | 1.43071 |
| small | sklearn_hgb_fixed | 0.742918 | 0.743279 | 1.00049 |
| small | xgboost_hist | 0.82685 | 0.841083 | 1.01721 |

### Underperformance findings and root cause analysis

- Root cause signal: Python-level dispatch/orchestration contributes meaningfully to sklearn runtime.
- Issue (single_thread, dataset `medium`): Best sklearn total is 1.484x slower than best alternative at thread=1.
  - Implementation plan:
    - Move short-lived orchestration loops to Cython/C-level helpers.
    - Preallocate and reuse temporary buffers in split and histogram kernels.
    - Add lightweight fast paths for small-node splits to bypass heavy orchestration.
- Issue (single_thread, dataset `small`): Best sklearn total is 1.359x slower than best alternative at thread=1.
  - Implementation plan:
    - Move short-lived orchestration loops to Cython/C-level helpers.
    - Preallocate and reuse temporary buffers in split and histogram kernels.
    - Add lightweight fast paths for small-node splits to bypass heavy orchestration.
- Issue (scalability, dataset `medium`): Best sklearn speedup trails best alternative by 0.698 (1->regular max threads).
  - Implementation plan:
    - Move short-lived orchestration loops to Cython/C-level helpers.
    - Preallocate and reuse temporary buffers in split and histogram kernels.
    - Add lightweight fast paths for small-node splits to bypass heavy orchestration.
- Issue (scalability, dataset `small`): Best sklearn speedup trails best alternative by 0.473 (1->regular max threads).
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

