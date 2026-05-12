# Detailed platform analysis: linux-amd64

- System: `Linux`
- Architecture: `x86_64`
- CPU count (logical): `4`
- CPU count (physical): `2`
- Hyper-threading enabled: `True`
- CPU model: `AMD EPYC 9V74 80-Core Processor`
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
| medium | lightgbm_hist | 0.586641 | 220 | 220 | True | 11256 | 51.1636 |
| medium | sklearn_hgb | 0.529888 | 220 | 220 | True | 12398 | 56.3545 |
| medium | sklearn_hgb_fixed | 0.529888 | 220 | 220 | True | 12398 | 56.3545 |
| medium | xgboost_hist | 0.585335 | 220 | 220 | True | 11618 | 52.8091 |
| small | lightgbm_hist | 0.949369 | 220 | 220 | True | 13386 | 60.8455 |
| small | sklearn_hgb | 0.942299 | 220 | 220 | True | 13414 | 60.9727 |
| small | sklearn_hgb_fixed | 0.942299 | 220 | 220 | True | 13414 | 60.9727 |
| small | xgboost_hist | 0.949753 | 220 | 220 | True | 13390 | 60.8636 |

### Scalability summary (`1 -> cores=4`)

| dataset | model | max_regular_threads | fit_s_1_thread | fit_s_regular_max_threads | speedup_1_to_regular_max |
| --- | --- | --- | --- | --- | --- |
| medium | lightgbm_hist | 4 | 1.21781 | 0.494025 | 2.46508 |
| medium | sklearn_hgb | 4 | 1.12134 | 0.767625 | 1.46079 |
| medium | sklearn_hgb_fixed | 4 | 1.12445 | 0.69902 | 1.60861 |
| medium | xgboost_hist | 4 | 2.16768 | 1.28401 | 1.68821 |
| small | lightgbm_hist | 4 | 0.571655 | 0.273629 | 2.08916 |
| small | sklearn_hgb | 4 | 0.609867 | 0.445726 | 1.36826 |
| small | sklearn_hgb_fixed | 4 | 0.589467 | 0.44082 | 1.3372 |
| small | xgboost_hist | 4 | 0.824292 | 0.53415 | 1.54318 |

### Oversubscription regime summary (`cores=4`, `2x`)

| dataset | model | fit_s_cores | fit_s_2x_cores | fit_ratio_2x_vs_cores |
| --- | --- | --- | --- | --- |
| medium | lightgbm_hist | 0.494025 | 1.78413 | 3.61141 |
| medium | sklearn_hgb | 0.767625 | 3.68722 | 4.80341 |
| medium | sklearn_hgb_fixed | 0.69902 | 0.746785 | 1.06833 |
| medium | xgboost_hist | 1.28401 | 1.42194 | 1.10742 |
| small | lightgbm_hist | 0.273629 | 1.76078 | 6.4349 |
| small | sklearn_hgb | 0.445726 | 3.83703 | 8.6085 |
| small | sklearn_hgb_fixed | 0.44082 | 0.445014 | 1.00951 |
| small | xgboost_hist | 0.53415 | 0.638909 | 1.19612 |

### Underperformance findings and root cause analysis

- Root cause signal: Native hotspots indicate synchronization/runtime overhead (OpenMP/pthread wait-heavy stacks).
- Issue (scalability, dataset `medium`): Best sklearn speedup trails best alternative by 0.856 (1->regular max threads).
  - Implementation plan:
    - Introduce adaptive thread gating based on node sample count and feature count.
    - Batch multiple frontier nodes per parallel region to increase task granularity.
    - Reduce barrier frequency by fusing short OpenMP regions in split/histogram paths.
- Issue (scalability, dataset `small`): Best sklearn speedup trails best alternative by 0.721 (1->regular max threads).
  - Implementation plan:
    - Introduce adaptive thread gating based on node sample count and feature count.
    - Batch multiple frontier nodes per parallel region to increase task granularity.
    - Reduce barrier frequency by fusing short OpenMP regions in split/histogram paths.

## Setting: `deep_few_trees`

![scalability-deep_few_trees](scalability_deep_few_trees.png)

![absolute-fit-time-deep_few_trees](fit_time_threads_deep_few_trees.png)

_Vertical markers denote `cores=4` and `2x=8` thread regimes._

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

### Scalability summary (`1 -> cores=4`)

| dataset | model | max_regular_threads | fit_s_1_thread | fit_s_regular_max_threads | speedup_1_to_regular_max |
| --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 4 | 6.06889 | 2.65034 | 2.28985 |
| large | sklearn_hgb | 4 | 5.80408 | 2.84119 | 2.04283 |
| large | sklearn_hgb_fixed | 4 | 5.89654 | 2.87628 | 2.05006 |
| large | xgboost_hist | 4 | 8.06121 | 4.90204 | 1.64446 |
| medium | lightgbm_hist | 4 | 5.68987 | 2.56251 | 2.22043 |
| medium | sklearn_hgb | 4 | 5.35695 | 2.74419 | 1.95211 |
| medium | sklearn_hgb_fixed | 4 | 5.40238 | 2.72663 | 1.98134 |
| medium | xgboost_hist | 4 | 6.66734 | 3.99949 | 1.66705 |
| small | lightgbm_hist | 4 | 1.50059 | 0.702916 | 2.13481 |
| small | sklearn_hgb | 4 | 1.64966 | 0.969712 | 1.70118 |
| small | sklearn_hgb_fixed | 4 | 1.66552 | 0.962269 | 1.73083 |
| small | xgboost_hist | 4 | 2.11793 | 1.47587 | 1.43504 |

### Oversubscription regime summary (`cores=4`, `2x`)

| dataset | model | fit_s_cores | fit_s_2x_cores | fit_ratio_2x_vs_cores |
| --- | --- | --- | --- | --- |
| large | lightgbm_hist | 2.65034 | 3.59256 | 1.35551 |
| large | sklearn_hgb | 2.84119 | 6.5013 | 2.28823 |
| large | sklearn_hgb_fixed | 2.87628 | 2.85644 | 0.9931 |
| large | xgboost_hist | 4.90204 | 4.95196 | 1.01018 |
| medium | lightgbm_hist | 2.56251 | 3.53553 | 1.37971 |
| medium | sklearn_hgb | 2.74419 | 6.20535 | 2.26127 |
| medium | sklearn_hgb_fixed | 2.72663 | 2.67282 | 0.980264 |
| medium | xgboost_hist | 3.99949 | 4.05055 | 1.01277 |
| small | lightgbm_hist | 0.702916 | 1.68037 | 2.39056 |
| small | sklearn_hgb | 0.969712 | 4.09229 | 4.22011 |
| small | sklearn_hgb_fixed | 0.962269 | 0.99477 | 1.03378 |
| small | xgboost_hist | 1.47587 | 1.56456 | 1.06009 |

### Underperformance findings and root cause analysis

- Root cause signal: Native hotspots indicate synchronization/runtime overhead (OpenMP/pthread wait-heavy stacks).
- Issue (single_thread, dataset `small`): Best sklearn total is 1.088x slower than best alternative at thread=1.
  - Implementation plan:
    - Introduce adaptive thread gating based on node sample count and feature count.
    - Batch multiple frontier nodes per parallel region to increase task granularity.
    - Reduce barrier frequency by fusing short OpenMP regions in split/histogram paths.
- Issue (scalability, dataset `large`): Best sklearn speedup trails best alternative by 0.240 (1->regular max threads).
  - Implementation plan:
    - Introduce adaptive thread gating based on node sample count and feature count.
    - Batch multiple frontier nodes per parallel region to increase task granularity.
    - Reduce barrier frequency by fusing short OpenMP regions in split/histogram paths.
- Issue (scalability, dataset `medium`): Best sklearn speedup trails best alternative by 0.239 (1->regular max threads).
  - Implementation plan:
    - Introduce adaptive thread gating based on node sample count and feature count.
    - Batch multiple frontier nodes per parallel region to increase task granularity.
    - Reduce barrier frequency by fusing short OpenMP regions in split/histogram paths.
- Issue (scalability, dataset `small`): Best sklearn speedup trails best alternative by 0.404 (1->regular max threads).
  - Implementation plan:
    - Introduce adaptive thread gating based on node sample count and feature count.
    - Batch multiple frontier nodes per parallel region to increase task granularity.
    - Reduce barrier frequency by fusing short OpenMP regions in split/histogram paths.

