# Detailed platform analysis: windows-amd64

- System: `Windows`
- Architecture: `AMD64`
- Native profile enabled: `False`

## Setting: `baseline_default`

![scalability-baseline_default](scalability.png)

### Parity checks (thread=1)

| dataset | model | r2 | fitted_trees | expected_trees | trees_match | total_nodes | avg_nodes_per_tree |
| --- | --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 0.674331 | 220 | 220 | True | 13420 | 61 |
| large | sklearn_hgb | 0.64901 | 220 | 220 | True | 13420 | 61 |
| large | sklearn_hgb_fixed | 0.64901 | 220 | 220 | True | 13420 | 61 |
| large | xgboost_hist | 0.679039 | 220 | 220 | True | 13420 | 61 |
| medium | lightgbm_hist | 0.762334 | 220 | 220 | True | 13420 | 61 |
| medium | sklearn_hgb | 0.745971 | 220 | 220 | True | 13420 | 61 |
| medium | sklearn_hgb_fixed | 0.745971 | 220 | 220 | True | 13420 | 61 |
| medium | xgboost_hist | 0.761535 | 220 | 220 | True | 13420 | 61 |
| small | lightgbm_hist | 0.893078 | 220 | 220 | True | 13420 | 61 |
| small | sklearn_hgb | 0.88762 | 220 | 220 | True | 13420 | 61 |
| small | sklearn_hgb_fixed | 0.88762 | 220 | 220 | True | 13420 | 61 |
| small | xgboost_hist | 0.893059 | 220 | 220 | True | 13420 | 61 |

### Scalability summary

| dataset | model | max_threads | fit_s_1_thread | fit_s_max_threads | speedup_1_to_max |
| --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 4 | 3.29911 | 1.34054 | 2.46104 |
| large | sklearn_hgb | 4 | 4.44231 | 2.59529 | 1.71168 |
| large | sklearn_hgb_fixed | 4 | 4.44576 | 2.59229 | 1.71499 |
| large | xgboost_hist | 4 | 5.23632 | 3.34737 | 1.56431 |
| medium | lightgbm_hist | 4 | 3.81927 | 1.62621 | 2.34858 |
| medium | sklearn_hgb | 4 | 4.53009 | 2.49628 | 1.81474 |
| medium | sklearn_hgb_fixed | 4 | 4.54663 | 2.47952 | 1.83367 |
| medium | xgboost_hist | 4 | 5.51263 | 3.26279 | 1.68955 |
| small | lightgbm_hist | 4 | 2.45109 | 1.08832 | 2.25218 |
| small | sklearn_hgb | 4 | 2.83918 | 1.65259 | 1.71802 |
| small | sklearn_hgb_fixed | 4 | 2.83476 | 1.65419 | 1.71369 |
| small | xgboost_hist | 4 | 3.44981 | 1.96103 | 1.75918 |

### Underperformance findings and root cause analysis

- Root cause signal: Python-level dispatch/orchestration contributes meaningfully to sklearn runtime.
- Issue (single_thread, dataset `large`): Best sklearn total is 1.353x slower than best alternative at thread=1.
  - Implementation plan:
    - Move short-lived orchestration loops to Cython/C-level helpers.
    - Preallocate and reuse temporary buffers in split and histogram kernels.
    - Add lightweight fast paths for small-node splits to bypass heavy orchestration.
- Issue (single_thread, dataset `medium`): Best sklearn total is 1.204x slower than best alternative at thread=1.
  - Implementation plan:
    - Move short-lived orchestration loops to Cython/C-level helpers.
    - Preallocate and reuse temporary buffers in split and histogram kernels.
    - Add lightweight fast paths for small-node splits to bypass heavy orchestration.
- Issue (single_thread, dataset `small`): Best sklearn total is 1.195x slower than best alternative at thread=1.
  - Implementation plan:
    - Move short-lived orchestration loops to Cython/C-level helpers.
    - Preallocate and reuse temporary buffers in split and histogram kernels.
    - Add lightweight fast paths for small-node splits to bypass heavy orchestration.
- Issue (scalability, dataset `large`): Best sklearn speedup trails best alternative by 0.746 (1->max threads).
  - Implementation plan:
    - Move short-lived orchestration loops to Cython/C-level helpers.
    - Preallocate and reuse temporary buffers in split and histogram kernels.
    - Add lightweight fast paths for small-node splits to bypass heavy orchestration.
- Issue (scalability, dataset `medium`): Best sklearn speedup trails best alternative by 0.515 (1->max threads).
  - Implementation plan:
    - Move short-lived orchestration loops to Cython/C-level helpers.
    - Preallocate and reuse temporary buffers in split and histogram kernels.
    - Add lightweight fast paths for small-node splits to bypass heavy orchestration.
- Issue (scalability, dataset `small`): Best sklearn speedup trails best alternative by 0.534 (1->max threads).
  - Implementation plan:
    - Move short-lived orchestration loops to Cython/C-level helpers.
    - Preallocate and reuse temporary buffers in split and histogram kernels.
    - Add lightweight fast paths for small-node splits to bypass heavy orchestration.

## Setting: `deep_few_trees`

![scalability-deep_few_trees](scalability_deep_few_trees.png)

### Parity checks (thread=1)

| dataset | model | r2 | fitted_trees | expected_trees | trees_match | total_nodes | avg_nodes_per_tree |
| --- | --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 0.49027 | 48 | 48 | True | 12144 | 253 |
| large | sklearn_hgb | 0.480794 | 48 | 48 | True | 12144 | 253 |
| large | sklearn_hgb_fixed | 0.480794 | 48 | 48 | True | 12144 | 253 |
| large | xgboost_hist | 0.481133 | 48 | 48 | True | 12144 | 253 |
| medium | lightgbm_hist | 0.578524 | 48 | 48 | True | 12144 | 253 |
| medium | sklearn_hgb | 0.577725 | 48 | 48 | True | 12144 | 253 |
| medium | sklearn_hgb_fixed | 0.577725 | 48 | 48 | True | 12144 | 253 |
| medium | xgboost_hist | 0.57702 | 48 | 48 | True | 12144 | 253 |
| small | lightgbm_hist | 0.749752 | 48 | 48 | True | 12144 | 253 |
| small | sklearn_hgb | 0.751461 | 48 | 48 | True | 12144 | 253 |
| small | sklearn_hgb_fixed | 0.751461 | 48 | 48 | True | 12144 | 253 |
| small | xgboost_hist | 0.752362 | 48 | 48 | True | 12144 | 253 |

### Scalability summary

| dataset | model | max_threads | fit_s_1_thread | fit_s_max_threads | speedup_1_to_max |
| --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 4 | 2.79955 | 1.14179 | 2.4519 |
| large | sklearn_hgb | 4 | 3.49591 | 2.27876 | 1.53413 |
| large | sklearn_hgb_fixed | 4 | 3.47497 | 2.27674 | 1.5263 |
| large | xgboost_hist | 4 | 5.63497 | 4.3036 | 1.30936 |
| medium | lightgbm_hist | 4 | 2.98866 | 1.244 | 2.40247 |
| medium | sklearn_hgb | 4 | 3.83913 | 2.35151 | 1.63262 |
| medium | sklearn_hgb_fixed | 4 | 3.84002 | 2.33407 | 1.6452 |
| medium | xgboost_hist | 4 | 5.33204 | 3.74318 | 1.42447 |
| small | lightgbm_hist | 4 | 1.70275 | 0.764206 | 2.22813 |
| small | sklearn_hgb | 4 | 2.19869 | 1.45348 | 1.5127 |
| small | sklearn_hgb_fixed | 4 | 2.21356 | 1.46119 | 1.5149 |
| small | xgboost_hist | 4 | 2.88419 | 2.02199 | 1.42641 |

### Underperformance findings and root cause analysis

- Root cause signal: Python-level dispatch/orchestration contributes meaningfully to sklearn runtime.
- Issue (single_thread, dataset `large`): Best sklearn total is 1.244x slower than best alternative at thread=1.
  - Implementation plan:
    - Move short-lived orchestration loops to Cython/C-level helpers.
    - Preallocate and reuse temporary buffers in split and histogram kernels.
    - Add lightweight fast paths for small-node splits to bypass heavy orchestration.
- Issue (single_thread, dataset `medium`): Best sklearn total is 1.289x slower than best alternative at thread=1.
  - Implementation plan:
    - Move short-lived orchestration loops to Cython/C-level helpers.
    - Preallocate and reuse temporary buffers in split and histogram kernels.
    - Add lightweight fast paths for small-node splits to bypass heavy orchestration.
- Issue (single_thread, dataset `small`): Best sklearn total is 1.297x slower than best alternative at thread=1.
  - Implementation plan:
    - Move short-lived orchestration loops to Cython/C-level helpers.
    - Preallocate and reuse temporary buffers in split and histogram kernels.
    - Add lightweight fast paths for small-node splits to bypass heavy orchestration.
- Issue (scalability, dataset `large`): Best sklearn speedup trails best alternative by 0.918 (1->max threads).
  - Implementation plan:
    - Move short-lived orchestration loops to Cython/C-level helpers.
    - Preallocate and reuse temporary buffers in split and histogram kernels.
    - Add lightweight fast paths for small-node splits to bypass heavy orchestration.
- Issue (scalability, dataset `medium`): Best sklearn speedup trails best alternative by 0.757 (1->max threads).
  - Implementation plan:
    - Move short-lived orchestration loops to Cython/C-level helpers.
    - Preallocate and reuse temporary buffers in split and histogram kernels.
    - Add lightweight fast paths for small-node splits to bypass heavy orchestration.
- Issue (scalability, dataset `small`): Best sklearn speedup trails best alternative by 0.713 (1->max threads).
  - Implementation plan:
    - Move short-lived orchestration loops to Cython/C-level helpers.
    - Preallocate and reuse temporary buffers in split and histogram kernels.
    - Add lightweight fast paths for small-node splits to bypass heavy orchestration.

