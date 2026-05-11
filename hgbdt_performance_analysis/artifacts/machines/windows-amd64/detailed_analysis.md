# Detailed platform analysis: windows-amd64

- System: `Windows`
- Architecture: `AMD64`
- CPU count (logical): `4`
- Thread grid: `[1, 2, 4, 8, 16]`
- Native profile enabled: `False`

## Setting: `baseline_default`

![scalability-baseline_default](scalability.png)

### Parity checks (thread=1)

| dataset | model | r2 | fitted_trees | expected_trees | trees_match | total_nodes | avg_nodes_per_tree |
| --- | --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 0.692337 | 220 | 220 | True | 13420 | 61 |
| large | sklearn_hgb | 0.675577 | 220 | 220 | True | 13420 | 61 |
| large | sklearn_hgb_fixed | 0.675577 | 220 | 220 | True | 13420 | 61 |
| large | xgboost_hist | 0.694704 | 220 | 220 | True | 13420 | 61 |
| medium | lightgbm_hist | 0.79359 | 220 | 220 | True | 13420 | 61 |
| medium | sklearn_hgb | 0.785099 | 220 | 220 | True | 13420 | 61 |
| medium | sklearn_hgb_fixed | 0.785099 | 220 | 220 | True | 13420 | 61 |
| medium | xgboost_hist | 0.793602 | 220 | 220 | True | 13420 | 61 |
| small | lightgbm_hist | 0.893078 | 220 | 220 | True | 13420 | 61 |
| small | sklearn_hgb | 0.88762 | 220 | 220 | True | 13420 | 61 |
| small | sklearn_hgb_fixed | 0.88762 | 220 | 220 | True | 13420 | 61 |
| small | xgboost_hist | 0.893059 | 220 | 220 | True | 13420 | 61 |

### Scalability summary

| dataset | model | max_threads | fit_s_1_thread | fit_s_max_threads | speedup_1_to_max |
| --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 16 | 6.17854 | 2.79495 | 2.21061 |
| large | sklearn_hgb | 16 | 7.1055 | 4.19273 | 1.69472 |
| large | sklearn_hgb_fixed | 16 | 7.15107 | 3.66667 | 1.95029 |
| large | xgboost_hist | 16 | 8.70489 | 5.25525 | 1.65642 |
| medium | lightgbm_hist | 16 | 5.91744 | 2.72668 | 2.1702 |
| medium | sklearn_hgb | 16 | 6.38825 | 3.79622 | 1.68279 |
| medium | sklearn_hgb_fixed | 16 | 6.3533 | 3.29303 | 1.92932 |
| medium | xgboost_hist | 16 | 7.78988 | 4.52119 | 1.72297 |
| small | lightgbm_hist | 16 | 2.45082 | 1.32633 | 1.84782 |
| small | sklearn_hgb | 16 | 2.8241 | 2.20205 | 1.28249 |
| small | sklearn_hgb_fixed | 16 | 2.83614 | 1.66094 | 1.70755 |
| small | xgboost_hist | 16 | 3.42834 | 1.96077 | 1.74847 |

### Oversubscription regime summary (`cores=4`, `2x`, `4x`)

| dataset | model | fit_s_cores | fit_s_2x_cores | fit_s_4x_cores | fit_ratio_2x_vs_cores | fit_ratio_4x_vs_cores |
| --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 2.57047 | 2.67938 | 2.79495 | 1.04237 | 1.08733 |
| large | sklearn_hgb | 3.65851 | 3.94357 | 4.19273 | 1.07792 | 1.14602 |
| large | sklearn_hgb_fixed | 3.66834 | 3.66247 | 3.66667 | 0.9984 | 0.999545 |
| large | xgboost_hist | 5.26415 | 5.27681 | 5.25525 | 1.0024 | 0.998309 |
| medium | lightgbm_hist | 2.48741 | 2.59515 | 2.72668 | 1.04332 | 1.09619 |
| medium | sklearn_hgb | 3.30331 | 3.5849 | 3.79622 | 1.08524 | 1.14921 |
| medium | sklearn_hgb_fixed | 3.25243 | 3.32393 | 3.29303 | 1.02198 | 1.01248 |
| medium | xgboost_hist | 4.48869 | 4.52159 | 4.52119 | 1.00733 | 1.00724 |
| small | lightgbm_hist | 1.09087 | 1.17761 | 1.32633 | 1.07952 | 1.21584 |
| small | sklearn_hgb | 1.6718 | 1.92424 | 2.20205 | 1.151 | 1.31717 |
| small | sklearn_hgb_fixed | 1.7173 | 1.66492 | 1.66094 | 0.9695 | 0.96718 |
| small | xgboost_hist | 1.97044 | 1.95045 | 1.96077 | 0.989853 | 0.995092 |

### Underperformance findings and root cause analysis

- Root cause signal: Python-level dispatch/orchestration contributes meaningfully to sklearn runtime.
- Issue (single_thread, dataset `large`): Best sklearn total is 1.173x slower than best alternative at thread=1.
  - Implementation plan:
    - Move short-lived orchestration loops to Cython/C-level helpers.
    - Preallocate and reuse temporary buffers in split and histogram kernels.
    - Add lightweight fast paths for small-node splits to bypass heavy orchestration.
- Issue (single_thread, dataset `medium`): Best sklearn total is 1.103x slower than best alternative at thread=1.
  - Implementation plan:
    - Move short-lived orchestration loops to Cython/C-level helpers.
    - Preallocate and reuse temporary buffers in split and histogram kernels.
    - Add lightweight fast paths for small-node splits to bypass heavy orchestration.
- Issue (single_thread, dataset `small`): Best sklearn total is 1.192x slower than best alternative at thread=1.
  - Implementation plan:
    - Move short-lived orchestration loops to Cython/C-level helpers.
    - Preallocate and reuse temporary buffers in split and histogram kernels.
    - Add lightweight fast paths for small-node splits to bypass heavy orchestration.
- Issue (scalability, dataset `large`): Best sklearn speedup trails best alternative by 0.260 (1->max threads).
  - Implementation plan:
    - Move short-lived orchestration loops to Cython/C-level helpers.
    - Preallocate and reuse temporary buffers in split and histogram kernels.
    - Add lightweight fast paths for small-node splits to bypass heavy orchestration.
- Issue (scalability, dataset `medium`): Best sklearn speedup trails best alternative by 0.241 (1->max threads).
  - Implementation plan:
    - Move short-lived orchestration loops to Cython/C-level helpers.
    - Preallocate and reuse temporary buffers in split and histogram kernels.
    - Add lightweight fast paths for small-node splits to bypass heavy orchestration.

## Setting: `deep_few_trees`

![scalability-deep_few_trees](scalability_deep_few_trees.png)

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

### Scalability summary

| dataset | model | max_threads | fit_s_1_thread | fit_s_max_threads | speedup_1_to_max |
| --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 16 | 4.71402 | 2.14296 | 2.19977 |
| large | sklearn_hgb | 16 | 5.78752 | 3.92468 | 1.47465 |
| large | sklearn_hgb_fixed | 16 | 5.7884 | 3.34867 | 1.72857 |
| large | xgboost_hist | 16 | 8.16799 | 5.60979 | 1.45602 |
| medium | lightgbm_hist | 16 | 6.18465 | 2.811 | 2.20016 |
| medium | sklearn_hgb | 16 | 6.51922 | 3.93642 | 1.65613 |
| medium | sklearn_hgb_fixed | 16 | 6.52418 | 3.40864 | 1.91401 |
| medium | xgboost_hist | 16 | 8.41318 | 5.32432 | 1.58014 |
| small | lightgbm_hist | 16 | 1.68073 | 0.955578 | 1.75887 |
| small | sklearn_hgb | 16 | 2.21503 | 1.99673 | 1.10933 |
| small | sklearn_hgb_fixed | 16 | 2.20551 | 1.45011 | 1.52093 |
| small | xgboost_hist | 16 | 2.83088 | 1.97857 | 1.43077 |

### Oversubscription regime summary (`cores=4`, `2x`, `4x`)

| dataset | model | fit_s_cores | fit_s_2x_cores | fit_s_4x_cores | fit_ratio_2x_vs_cores | fit_ratio_4x_vs_cores |
| --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 1.95469 | 2.00173 | 2.14296 | 1.02407 | 1.09632 |
| large | sklearn_hgb | 3.33919 | 3.62438 | 3.92468 | 1.08541 | 1.17534 |
| large | sklearn_hgb_fixed | 3.34049 | 3.34361 | 3.34867 | 1.00093 | 1.00245 |
| large | xgboost_hist | 5.63062 | 5.61246 | 5.60979 | 0.996775 | 0.9963 |
| medium | lightgbm_hist | 2.63271 | 2.73452 | 2.811 | 1.03867 | 1.06772 |
| medium | sklearn_hgb | 3.42245 | 3.69876 | 3.93642 | 1.08074 | 1.15018 |
| medium | sklearn_hgb_fixed | 3.4211 | 3.42663 | 3.40864 | 1.00162 | 0.996358 |
| medium | xgboost_hist | 5.31023 | 5.26735 | 5.32432 | 0.991925 | 1.00265 |
| small | lightgbm_hist | 0.765636 | 0.827071 | 0.955578 | 1.08024 | 1.24808 |
| small | sklearn_hgb | 1.46987 | 1.73415 | 1.99673 | 1.1798 | 1.35844 |
| small | sklearn_hgb_fixed | 1.45873 | 1.4346 | 1.45011 | 0.983462 | 0.994092 |
| small | xgboost_hist | 1.98513 | 1.9769 | 1.97857 | 0.995853 | 0.996693 |

### Underperformance findings and root cause analysis

- Root cause signal: Python-level dispatch/orchestration contributes meaningfully to sklearn runtime.
- Issue (single_thread, dataset `large`): Best sklearn total is 1.235x slower than best alternative at thread=1.
  - Implementation plan:
    - Move short-lived orchestration loops to Cython/C-level helpers.
    - Preallocate and reuse temporary buffers in split and histogram kernels.
    - Add lightweight fast paths for small-node splits to bypass heavy orchestration.
- Issue (single_thread, dataset `medium`): Best sklearn total is 1.070x slower than best alternative at thread=1.
  - Implementation plan:
    - Move short-lived orchestration loops to Cython/C-level helpers.
    - Preallocate and reuse temporary buffers in split and histogram kernels.
    - Add lightweight fast paths for small-node splits to bypass heavy orchestration.
- Issue (single_thread, dataset `small`): Best sklearn total is 1.325x slower than best alternative at thread=1.
  - Implementation plan:
    - Move short-lived orchestration loops to Cython/C-level helpers.
    - Preallocate and reuse temporary buffers in split and histogram kernels.
    - Add lightweight fast paths for small-node splits to bypass heavy orchestration.
- Issue (scalability, dataset `large`): Best sklearn speedup trails best alternative by 0.471 (1->max threads).
  - Implementation plan:
    - Move short-lived orchestration loops to Cython/C-level helpers.
    - Preallocate and reuse temporary buffers in split and histogram kernels.
    - Add lightweight fast paths for small-node splits to bypass heavy orchestration.
- Issue (scalability, dataset `medium`): Best sklearn speedup trails best alternative by 0.286 (1->max threads).
  - Implementation plan:
    - Move short-lived orchestration loops to Cython/C-level helpers.
    - Preallocate and reuse temporary buffers in split and histogram kernels.
    - Add lightweight fast paths for small-node splits to bypass heavy orchestration.
- Issue (scalability, dataset `small`): Best sklearn speedup trails best alternative by 0.238 (1->max threads).
  - Implementation plan:
    - Move short-lived orchestration loops to Cython/C-level helpers.
    - Preallocate and reuse temporary buffers in split and histogram kernels.
    - Add lightweight fast paths for small-node splits to bypass heavy orchestration.

