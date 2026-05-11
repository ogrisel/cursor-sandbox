# Detailed platform analysis: macos-arm64

- System: `Darwin`
- Architecture: `arm64`
- CPU count (logical): `3`
- Thread grid: `[1, 2, 3, 6, 12]`
- Native profile enabled: `True`

## Setting: `baseline_default`

![scalability-baseline_default](scalability.png)

### Parity checks (thread=1)

| dataset | model | r2 | fitted_trees | expected_trees | trees_match | total_nodes | avg_nodes_per_tree |
| --- | --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 0.670334 | 220 | 220 | True | 13420 | 61 |
| large | sklearn_hgb | 0.658445 | 220 | 220 | True | 13420 | 61 |
| large | sklearn_hgb_fixed | 0.658445 | 220 | 220 | True | 13420 | 61 |
| large | xgboost_hist | 0.671732 | 220 | 220 | True | 13420 | 61 |
| medium | lightgbm_hist | 0.79359 | 220 | 220 | True | 13420 | 61 |
| medium | sklearn_hgb | 0.785099 | 220 | 220 | True | 13420 | 61 |
| medium | sklearn_hgb_fixed | 0.785099 | 220 | 220 | True | 13420 | 61 |
| medium | xgboost_hist | 0.793248 | 220 | 220 | True | 13420 | 61 |
| small | lightgbm_hist | 0.893078 | 220 | 220 | True | 13420 | 61 |
| small | sklearn_hgb | 0.88762 | 220 | 220 | True | 13420 | 61 |
| small | sklearn_hgb_fixed | 0.88762 | 220 | 220 | True | 13420 | 61 |
| small | xgboost_hist | 0.894341 | 220 | 220 | True | 13420 | 61 |

### Scalability summary

| dataset | model | max_threads | fit_s_1_thread | fit_s_max_threads | speedup_1_to_max |
| --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 12 | 6.8822 | 5.56456 | 1.23679 |
| large | sklearn_hgb | 12 | 6.8463 | 6.13493 | 1.11595 |
| large | sklearn_hgb_fixed | 12 | 7.31555 | 2.82469 | 2.58986 |
| large | xgboost_hist | 12 | 8.33898 | 6.72742 | 1.23955 |
| medium | lightgbm_hist | 12 | 3.83284 | 4.03794 | 0.949206 |
| medium | sklearn_hgb | 12 | 4.65608 | 4.28232 | 1.08728 |
| medium | sklearn_hgb_fixed | 12 | 4.35686 | 3.04004 | 1.43316 |
| medium | xgboost_hist | 12 | 4.64477 | 4.04191 | 1.14915 |
| small | lightgbm_hist | 12 | 1.5578 | 3.46026 | 0.450198 |
| small | sklearn_hgb | 12 | 2.65641 | 3.09392 | 0.858589 |
| small | sklearn_hgb_fixed | 12 | 2.61381 | 2.02458 | 1.29104 |
| small | xgboost_hist | 12 | 2.83902 | 3.557 | 0.798149 |

### Oversubscription regime summary (`cores=3`, `2x`, `4x`)

| dataset | model | fit_s_cores | fit_s_2x_cores | fit_s_4x_cores | fit_ratio_2x_vs_cores | fit_ratio_4x_vs_cores |
| --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 4.5238 | 4.30867 | 5.56456 | 0.952445 | 1.23006 |
| large | sklearn_hgb | 4.83269 | 6.06788 | 6.13493 | 1.25559 | 1.26946 |
| large | sklearn_hgb_fixed | 3.95871 | 2.67366 | 2.82469 | 0.675387 | 0.713539 |
| large | xgboost_hist | 4.24258 | 4.3031 | 6.72742 | 1.01427 | 1.58569 |
| medium | lightgbm_hist | 2.1598 | 2.70332 | 4.03794 | 1.25165 | 1.86959 |
| medium | sklearn_hgb | 1.66127 | 2.58791 | 4.28232 | 1.55779 | 2.57774 |
| medium | sklearn_hgb_fixed | 2.07813 | 1.65307 | 3.04004 | 0.795457 | 1.46287 |
| medium | xgboost_hist | 2.71115 | 2.94376 | 4.04191 | 1.0858 | 1.49085 |
| small | lightgbm_hist | 2.47096 | 1.7304 | 3.46026 | 0.700296 | 1.40037 |
| small | sklearn_hgb | 1.46766 | 3.66339 | 3.09392 | 2.49607 | 2.10806 |
| small | sklearn_hgb_fixed | 1.40875 | 1.88637 | 2.02458 | 1.33903 | 1.43714 |
| small | xgboost_hist | 1.90726 | 2.36274 | 3.557 | 1.23881 | 1.86499 |

### Underperformance findings and root cause analysis

- Root cause signal: Python-level dispatch/orchestration contributes meaningfully to sklearn runtime.
- Issue (single_thread, dataset `medium`): Best sklearn total is 1.139x slower than best alternative at thread=1.
  - Implementation plan:
    - Move short-lived orchestration loops to Cython/C-level helpers.
    - Preallocate and reuse temporary buffers in split and histogram kernels.
    - Add lightweight fast paths for small-node splits to bypass heavy orchestration.
- Issue (single_thread, dataset `small`): Best sklearn total is 1.639x slower than best alternative at thread=1.
  - Implementation plan:
    - Move short-lived orchestration loops to Cython/C-level helpers.
    - Preallocate and reuse temporary buffers in split and histogram kernels.
    - Add lightweight fast paths for small-node splits to bypass heavy orchestration.

## Setting: `deep_few_trees`

![scalability-deep_few_trees](scalability_deep_few_trees.png)

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

### Scalability summary

| dataset | model | max_threads | fit_s_1_thread | fit_s_max_threads | speedup_1_to_max |
| --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 12 | 6.74268 | 4.41806 | 1.52617 |
| large | sklearn_hgb | 12 | 7.64075 | 5.40685 | 1.41316 |
| large | sklearn_hgb_fixed | 12 | 7.47811 | 3.53617 | 2.11475 |
| large | xgboost_hist | 12 | 7.52236 | 3.96261 | 1.89834 |
| medium | lightgbm_hist | 12 | 3.8286 | 2.59257 | 1.47676 |
| medium | sklearn_hgb | 12 | 4.30719 | 3.86161 | 1.11539 |
| medium | sklearn_hgb_fixed | 12 | 4.43531 | 1.9835 | 2.2361 |
| medium | xgboost_hist | 12 | 4.45374 | 2.90203 | 1.5347 |
| small | lightgbm_hist | 12 | 0.916127 | 1.31054 | 0.699043 |
| small | sklearn_hgb | 12 | 1.26099 | 2.63146 | 0.479199 |
| small | sklearn_hgb_fixed | 12 | 1.25093 | 1.10972 | 1.12725 |
| small | xgboost_hist | 12 | 1.4339 | 1.24163 | 1.15485 |

### Oversubscription regime summary (`cores=3`, `2x`, `4x`)

| dataset | model | fit_s_cores | fit_s_2x_cores | fit_s_4x_cores | fit_ratio_2x_vs_cores | fit_ratio_4x_vs_cores |
| --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 4.08334 | 3.99825 | 4.41806 | 0.979162 | 1.08197 |
| large | sklearn_hgb | 3.83333 | 4.43767 | 5.40685 | 1.15765 | 1.41048 |
| large | sklearn_hgb_fixed | 3.71191 | 3.54992 | 3.53617 | 0.95636 | 0.952657 |
| large | xgboost_hist | 3.9281 | 3.97281 | 3.96261 | 1.01138 | 1.00879 |
| medium | lightgbm_hist | 2.72168 | 2.43146 | 2.59257 | 0.893367 | 0.952561 |
| medium | sklearn_hgb | 1.9737 | 2.65385 | 3.86161 | 1.34461 | 1.95653 |
| medium | sklearn_hgb_fixed | 1.85039 | 2.19906 | 1.9835 | 1.18843 | 1.07194 |
| medium | xgboost_hist | 2.96417 | 2.66538 | 2.90203 | 0.8992 | 0.979036 |
| small | lightgbm_hist | 0.969907 | 1.1412 | 1.31054 | 1.17661 | 1.35121 |
| small | sklearn_hgb | 1.17381 | 1.47514 | 2.63146 | 1.25671 | 2.2418 |
| small | sklearn_hgb_fixed | 1.10104 | 0.741944 | 1.10972 | 0.673857 | 1.00788 |
| small | xgboost_hist | 1.54818 | 1.24697 | 1.24163 | 0.805444 | 0.801998 |

### Underperformance findings and root cause analysis

- Root cause signal: Python-level dispatch/orchestration contributes meaningfully to sklearn runtime.
- Issue (single_thread, dataset `large`): Best sklearn total is 1.109x slower than best alternative at thread=1.
  - Implementation plan:
    - Move short-lived orchestration loops to Cython/C-level helpers.
    - Preallocate and reuse temporary buffers in split and histogram kernels.
    - Add lightweight fast paths for small-node splits to bypass heavy orchestration.
- Issue (single_thread, dataset `medium`): Best sklearn total is 1.110x slower than best alternative at thread=1.
  - Implementation plan:
    - Move short-lived orchestration loops to Cython/C-level helpers.
    - Preallocate and reuse temporary buffers in split and histogram kernels.
    - Add lightweight fast paths for small-node splits to bypass heavy orchestration.
- Issue (single_thread, dataset `small`): Best sklearn total is 1.330x slower than best alternative at thread=1.
  - Implementation plan:
    - Move short-lived orchestration loops to Cython/C-level helpers.
    - Preallocate and reuse temporary buffers in split and histogram kernels.
    - Add lightweight fast paths for small-node splits to bypass heavy orchestration.

