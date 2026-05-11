# Detailed platform analysis: linux-amd64

- System: `Linux`
- Architecture: `x86_64`
- CPU count (logical): `4`
- CPU count (physical): `n/a`
- Hyper-threading enabled: `n/a`
- CPU model: `Intel(R) Xeon(R) Platinum 8370C CPU @ 2.80GHz`
- Core type counts: `{'performance': 4, 'efficiency': None, 'low_power': None}`
- CFS/CPU quota: `n/a`
- CPU set: `0-3`
- Thread grid: `[1, 2, 4, 8, 16]`
- Native profile enabled: `True`

## Setting: `baseline_default`

![scalability-baseline_default](scalability.png)

![absolute-fit-time-baseline_default](fit_time_threads.png)

_Vertical markers denote `cores=4`, `2x=8`, and `4x=16` thread regimes._

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

### Scalability summary (`1 -> cores=4`)

| dataset | model | max_regular_threads | fit_s_1_thread | fit_s_regular_max_threads | speedup_1_to_regular_max |
| --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 4 | 5.40205 | 2.37927 | 2.27047 |
| large | sklearn_hgb | 4 | 5.30422 | 2.71782 | 1.95165 |
| large | sklearn_hgb_fixed | 4 | 5.35296 | 2.68567 | 1.99315 |
| large | xgboost_hist | 4 | 7.51141 | 4.67194 | 1.60777 |
| medium | lightgbm_hist | 4 | 5.13426 | 2.31241 | 2.22031 |
| medium | sklearn_hgb | 4 | 4.96071 | 2.63602 | 1.88189 |
| medium | sklearn_hgb_fixed | 4 | 4.97149 | 2.66439 | 1.8659 |
| medium | xgboost_hist | 4 | 6.43017 | 3.90854 | 1.64516 |
| small | lightgbm_hist | 4 | 2.15228 | 0.994686 | 2.16377 |
| small | sklearn_hgb | 4 | 2.19558 | 1.28684 | 1.70618 |
| small | sklearn_hgb_fixed | 4 | 2.17447 | 1.2681 | 1.71475 |
| small | xgboost_hist | 4 | 2.66919 | 1.75279 | 1.52282 |

### Oversubscription regime summary (`cores=4`, `2x`, `4x`)

| dataset | model | fit_s_cores | fit_s_2x_cores | fit_s_4x_cores | fit_ratio_2x_vs_cores | fit_ratio_4x_vs_cores |
| --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 2.37927 | 3.40509 | 4.62645 | 1.43115 | 1.94448 |
| large | sklearn_hgb | 2.71782 | 6.27198 | 8.99255 | 2.30772 | 3.30874 |
| large | sklearn_hgb_fixed | 2.68567 | 2.70903 | 2.73026 | 1.0087 | 1.0166 |
| large | xgboost_hist | 4.67194 | 4.77375 | 4.99765 | 1.02179 | 1.06972 |
| medium | lightgbm_hist | 2.31241 | 3.36658 | 4.65214 | 1.45587 | 2.01181 |
| medium | sklearn_hgb | 2.63602 | 5.88219 | 8.77341 | 2.23147 | 3.32828 |
| medium | sklearn_hgb_fixed | 2.66439 | 2.6027 | 2.62308 | 0.976849 | 0.984497 |
| medium | xgboost_hist | 3.90854 | 3.93934 | 3.96195 | 1.00788 | 1.01367 |
| small | lightgbm_hist | 0.994686 | 2.12911 | 3.2482 | 2.14049 | 3.26555 |
| small | sklearn_hgb | 1.28684 | 4.35406 | 7.28174 | 3.38353 | 5.65862 |
| small | sklearn_hgb_fixed | 1.2681 | 1.39111 | 1.30003 | 1.09701 | 1.02518 |
| small | xgboost_hist | 1.75279 | 1.89042 | 1.83202 | 1.07852 | 1.0452 |

### Underperformance findings and root cause analysis

- Root cause signal: Native hotspots indicate synchronization/runtime overhead (OpenMP/pthread wait-heavy stacks).
- Issue (scalability, dataset `large`): Best sklearn speedup trails best alternative by 0.277 (1->regular max threads).
  - Implementation plan:
    - Introduce adaptive thread gating based on node sample count and feature count.
    - Batch multiple frontier nodes per parallel region to increase task granularity.
    - Reduce barrier frequency by fusing short OpenMP regions in split/histogram paths.
- Issue (scalability, dataset `medium`): Best sklearn speedup trails best alternative by 0.338 (1->regular max threads).
  - Implementation plan:
    - Introduce adaptive thread gating based on node sample count and feature count.
    - Batch multiple frontier nodes per parallel region to increase task granularity.
    - Reduce barrier frequency by fusing short OpenMP regions in split/histogram paths.
- Issue (scalability, dataset `small`): Best sklearn speedup trails best alternative by 0.449 (1->regular max threads).
  - Implementation plan:
    - Introduce adaptive thread gating based on node sample count and feature count.
    - Batch multiple frontier nodes per parallel region to increase task granularity.
    - Reduce barrier frequency by fusing short OpenMP regions in split/histogram paths.

## Setting: `deep_few_trees`

![scalability-deep_few_trees](scalability_deep_few_trees.png)

![absolute-fit-time-deep_few_trees](fit_time_threads_deep_few_trees.png)

_Vertical markers denote `cores=4`, `2x=8`, and `4x=16` thread regimes._

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

### Oversubscription regime summary (`cores=4`, `2x`, `4x`)

| dataset | model | fit_s_cores | fit_s_2x_cores | fit_s_4x_cores | fit_ratio_2x_vs_cores | fit_ratio_4x_vs_cores |
| --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 2.65034 | 3.59256 | 4.71 | 1.35551 | 1.77713 |
| large | sklearn_hgb | 2.84119 | 6.5013 | 9.45501 | 2.28823 | 3.32783 |
| large | sklearn_hgb_fixed | 2.87628 | 2.85644 | 2.92245 | 0.9931 | 1.01605 |
| large | xgboost_hist | 4.90204 | 4.95196 | 4.96987 | 1.01018 | 1.01384 |
| medium | lightgbm_hist | 2.56251 | 3.53553 | 4.87636 | 1.37971 | 1.90296 |
| medium | sklearn_hgb | 2.74419 | 6.20535 | 9.30707 | 2.26127 | 3.39156 |
| medium | sklearn_hgb_fixed | 2.72663 | 2.67282 | 2.69732 | 0.980264 | 0.989249 |
| medium | xgboost_hist | 3.99949 | 4.05055 | 4.20084 | 1.01277 | 1.05034 |
| small | lightgbm_hist | 0.702916 | 1.68037 | 2.68297 | 2.39056 | 3.81691 |
| small | sklearn_hgb | 0.969712 | 4.09229 | 7.06018 | 4.22011 | 7.2807 |
| small | sklearn_hgb_fixed | 0.962269 | 0.99477 | 1.00903 | 1.03378 | 1.04859 |
| small | xgboost_hist | 1.47587 | 1.56456 | 1.49972 | 1.06009 | 1.01616 |

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

