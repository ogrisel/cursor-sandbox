# Detailed platform analysis: linux-amd64

- System: `Linux`
- Architecture: `x86_64`
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
| large | lightgbm_hist | 4 | 4.88786 | 1.98523 | 2.46211 |
| large | sklearn_hgb | 4 | 4.24922 | 2.05369 | 2.06907 |
| large | sklearn_hgb_fixed | 4 | 4.20839 | 2.05651 | 2.04638 |
| large | xgboost_hist | 4 | 6.17215 | 3.30429 | 1.86792 |
| medium | lightgbm_hist | 4 | 4.56175 | 1.88345 | 2.42202 |
| medium | sklearn_hgb | 4 | 4.01832 | 1.92588 | 2.08649 |
| medium | sklearn_hgb_fixed | 4 | 4.00654 | 1.89852 | 2.11034 |
| medium | xgboost_hist | 4 | 5.17406 | 2.70227 | 1.91471 |
| small | lightgbm_hist | 4 | 1.93594 | 0.851125 | 2.27456 |
| small | sklearn_hgb | 4 | 1.79218 | 0.993343 | 1.80419 |
| small | sklearn_hgb_fixed | 4 | 1.74299 | 0.982948 | 1.77323 |
| small | xgboost_hist | 4 | 2.2531 | 1.3 | 1.73316 |

### Underperformance findings and root cause analysis

- Root cause signal: Native hotspots indicate synchronization/runtime overhead (OpenMP/pthread wait-heavy stacks).
- Issue (scalability, dataset `large`): Best sklearn speedup trails best alternative by 0.393 (1->max threads).
  - Implementation plan:
    - Introduce adaptive thread gating based on node sample count and feature count.
    - Batch multiple frontier nodes per parallel region to increase task granularity.
    - Reduce barrier frequency by fusing short OpenMP regions in split/histogram paths.
- Issue (scalability, dataset `medium`): Best sklearn speedup trails best alternative by 0.312 (1->max threads).
  - Implementation plan:
    - Introduce adaptive thread gating based on node sample count and feature count.
    - Batch multiple frontier nodes per parallel region to increase task granularity.
    - Reduce barrier frequency by fusing short OpenMP regions in split/histogram paths.
- Issue (scalability, dataset `small`): Best sklearn speedup trails best alternative by 0.470 (1->max threads).
  - Implementation plan:
    - Introduce adaptive thread gating based on node sample count and feature count.
    - Batch multiple frontier nodes per parallel region to increase task granularity.
    - Reduce barrier frequency by fusing short OpenMP regions in split/histogram paths.

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
| large | lightgbm_hist | 4 | 3.95187 | 1.5665 | 2.52274 |
| large | sklearn_hgb | 4 | 3.42092 | 1.71303 | 1.997 |
| large | sklearn_hgb_fixed | 4 | 3.42274 | 1.73869 | 1.96857 |
| large | xgboost_hist | 4 | 5.45169 | 2.96484 | 1.83878 |
| medium | lightgbm_hist | 4 | 5.12474 | 2.0773 | 2.46702 |
| medium | sklearn_hgb | 4 | 4.73715 | 2.18432 | 2.16871 |
| medium | sklearn_hgb_fixed | 4 | 4.69051 | 2.23589 | 2.09782 |
| medium | xgboost_hist | 4 | 5.72618 | 2.86986 | 1.99528 |
| small | lightgbm_hist | 4 | 1.41511 | 0.610161 | 2.31924 |
| small | sklearn_hgb | 4 | 1.39593 | 0.834037 | 1.6737 |
| small | sklearn_hgb_fixed | 4 | 1.43439 | 0.82633 | 1.73586 |
| small | xgboost_hist | 4 | 1.87466 | 1.10054 | 1.70339 |

### Underperformance findings and root cause analysis

- Root cause signal: Native hotspots indicate synchronization/runtime overhead (OpenMP/pthread wait-heavy stacks).
- Issue (scalability, dataset `large`): Best sklearn speedup trails best alternative by 0.526 (1->max threads).
  - Implementation plan:
    - Introduce adaptive thread gating based on node sample count and feature count.
    - Batch multiple frontier nodes per parallel region to increase task granularity.
    - Reduce barrier frequency by fusing short OpenMP regions in split/histogram paths.
- Issue (scalability, dataset `medium`): Best sklearn speedup trails best alternative by 0.298 (1->max threads).
  - Implementation plan:
    - Introduce adaptive thread gating based on node sample count and feature count.
    - Batch multiple frontier nodes per parallel region to increase task granularity.
    - Reduce barrier frequency by fusing short OpenMP regions in split/histogram paths.
- Issue (scalability, dataset `small`): Best sklearn speedup trails best alternative by 0.583 (1->max threads).
  - Implementation plan:
    - Introduce adaptive thread gating based on node sample count and feature count.
    - Batch multiple frontier nodes per parallel region to increase task granularity.
    - Reduce barrier frequency by fusing short OpenMP regions in split/histogram paths.

