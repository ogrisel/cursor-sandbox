# Detailed platform analysis: macos-arm64

- System: `Darwin`
- Architecture: `arm64`
- Native profile enabled: `True`

## Setting: `baseline_default`

![scalability-baseline_default](scalability.png)

### Parity checks (thread=1)

| dataset | model | r2 | fitted_trees | expected_trees | trees_match | total_nodes | avg_nodes_per_tree |
| --- | --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 0.692337 | 220 | 220 | True | 13420 | 61 |
| large | sklearn_hgb | 0.675577 | 220 | 220 | True | 13420 | 61 |
| large | sklearn_hgb_fixed | 0.675577 | 220 | 220 | True | 13420 | 61 |
| large | xgboost_hist | 0.69332 | 220 | 220 | True | 13420 | 61 |
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
| large | lightgbm_hist | 4 | 4.11001 | 2.81186 | 1.46167 |
| large | sklearn_hgb | 4 | 5.16046 | 2.70223 | 1.90971 |
| large | sklearn_hgb_fixed | 4 | 4.56778 | 1.77362 | 2.5754 |
| large | xgboost_hist | 4 | 5.8842 | 3.65509 | 1.60986 |
| medium | lightgbm_hist | 4 | 4.08332 | 4.44555 | 0.918518 |
| medium | sklearn_hgb | 4 | 4.72179 | 2.73961 | 1.72353 |
| medium | sklearn_hgb_fixed | 4 | 4.55738 | 2.23254 | 2.04134 |
| medium | xgboost_hist | 4 | 5.15926 | 2.94905 | 1.74946 |
| small | lightgbm_hist | 4 | 2.37759 | 1.87722 | 1.26655 |
| small | sklearn_hgb | 4 | 2.8553 | 1.52284 | 1.87498 |
| small | sklearn_hgb_fixed | 4 | 2.38758 | 1.57805 | 1.513 |
| small | xgboost_hist | 4 | 2.49817 | 2.56347 | 0.97453 |

### Underperformance findings and root cause analysis

- Root cause signal: Python-level dispatch/orchestration contributes meaningfully to sklearn runtime.
- Issue (single_thread, dataset `large`): Best sklearn total is 1.110x slower than best alternative at thread=1.
  - Implementation plan:
    - Move short-lived orchestration loops to Cython/C-level helpers.
    - Preallocate and reuse temporary buffers in split and histogram kernels.
    - Add lightweight fast paths for small-node splits to bypass heavy orchestration.
- Issue (single_thread, dataset `medium`): Best sklearn total is 1.107x slower than best alternative at thread=1.
  - Implementation plan:
    - Move short-lived orchestration loops to Cython/C-level helpers.
    - Preallocate and reuse temporary buffers in split and histogram kernels.
    - Add lightweight fast paths for small-node splits to bypass heavy orchestration.

## Setting: `deep_few_trees`

![scalability-deep_few_trees](scalability_deep_few_trees.png)

### Parity checks (thread=1)

| dataset | model | r2 | fitted_trees | expected_trees | trees_match | total_nodes | avg_nodes_per_tree |
| --- | --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 0.491423 | 48 | 48 | True | 12144 | 253 |
| large | sklearn_hgb | 0.490287 | 48 | 48 | True | 12144 | 253 |
| large | sklearn_hgb_fixed | 0.490287 | 48 | 48 | True | 12144 | 253 |
| large | xgboost_hist | 0.491074 | 48 | 48 | True | 12144 | 253 |
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
| large | lightgbm_hist | 4 | 4.7726 | 3.50838 | 1.36034 |
| large | sklearn_hgb | 4 | 5.88368 | 3.23983 | 1.81604 |
| large | sklearn_hgb_fixed | 4 | 5.9781 | 2.29639 | 2.60326 |
| large | xgboost_hist | 4 | 5.89955 | 4.12326 | 1.4308 |
| medium | lightgbm_hist | 4 | 5.07837 | 4.29289 | 1.18297 |
| medium | sklearn_hgb | 4 | 5.45277 | 4.74232 | 1.14981 |
| medium | sklearn_hgb_fixed | 4 | 5.61636 | 3.68421 | 1.52444 |
| medium | xgboost_hist | 4 | 5.01937 | 3.01077 | 1.66714 |
| small | lightgbm_hist | 4 | 0.962995 | 1.74806 | 0.550894 |
| small | sklearn_hgb | 4 | 1.77164 | 1.28962 | 1.37377 |
| small | sklearn_hgb_fixed | 4 | 1.61634 | 1.4259 | 1.13356 |
| small | xgboost_hist | 4 | 1.5841 | 1.92473 | 0.823023 |

### Underperformance findings and root cause analysis

- Root cause signal: Python-level dispatch/orchestration contributes meaningfully to sklearn runtime.
- Issue (single_thread, dataset `large`): Best sklearn total is 1.237x slower than best alternative at thread=1.
  - Implementation plan:
    - Move short-lived orchestration loops to Cython/C-level helpers.
    - Preallocate and reuse temporary buffers in split and histogram kernels.
    - Add lightweight fast paths for small-node splits to bypass heavy orchestration.
- Issue (single_thread, dataset `medium`): Best sklearn total is 1.088x slower than best alternative at thread=1.
  - Implementation plan:
    - Move short-lived orchestration loops to Cython/C-level helpers.
    - Preallocate and reuse temporary buffers in split and histogram kernels.
    - Add lightweight fast paths for small-node splits to bypass heavy orchestration.
- Issue (single_thread, dataset `small`): Best sklearn total is 1.681x slower than best alternative at thread=1.
  - Implementation plan:
    - Move short-lived orchestration loops to Cython/C-level helpers.
    - Preallocate and reuse temporary buffers in split and histogram kernels.
    - Add lightweight fast paths for small-node splits to bypass heavy orchestration.

