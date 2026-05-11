# Detailed platform analysis: linux-arm64

- System: `Linux`
- Architecture: `aarch64`
- CPU count (logical): `4`
- CPU count (physical): `n/a`
- Hyper-threading enabled: `n/a`
- CPU model: `Neoverse-N2`
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
| medium | lightgbm_hist | 0.753709 | 220 | 220 | True | 13420 | 61 |
| medium | sklearn_hgb | 0.746237 | 220 | 220 | True | 13420 | 61 |
| medium | sklearn_hgb_fixed | 0.746237 | 220 | 220 | True | 13420 | 61 |
| medium | xgboost_hist | 0.75389 | 220 | 220 | True | 13420 | 61 |
| small | lightgbm_hist | 0.893078 | 220 | 220 | True | 13420 | 61 |
| small | sklearn_hgb | 0.88762 | 220 | 220 | True | 13420 | 61 |
| small | sklearn_hgb_fixed | 0.88762 | 220 | 220 | True | 13420 | 61 |
| small | xgboost_hist | 0.894341 | 220 | 220 | True | 13420 | 61 |

### Scalability summary (`1 -> cores=4`)

| dataset | model | max_regular_threads | fit_s_1_thread | fit_s_regular_max_threads | speedup_1_to_regular_max |
| --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 4 | 4.79215 | 1.34373 | 3.56631 |
| large | sklearn_hgb | 4 | 5.07717 | 1.63724 | 3.10106 |
| large | sklearn_hgb_fixed | 4 | 5.05701 | 1.62954 | 3.10333 |
| large | xgboost_hist | 4 | 7.27568 | 2.61711 | 2.78005 |
| medium | lightgbm_hist | 4 | 8.12146 | 2.28036 | 3.56148 |
| medium | sklearn_hgb | 4 | 8.42685 | 2.50018 | 3.37049 |
| medium | sklearn_hgb_fixed | 4 | 8.33303 | 2.46888 | 3.37523 |
| medium | xgboost_hist | 4 | 10.1674 | 3.11684 | 3.26209 |
| small | lightgbm_hist | 4 | 1.87855 | 0.591311 | 3.17693 |
| small | sklearn_hgb | 4 | 2.11023 | 0.84964 | 2.48368 |
| small | sklearn_hgb_fixed | 4 | 2.08089 | 0.860104 | 2.41935 |
| small | xgboost_hist | 4 | 2.56541 | 0.962428 | 2.66556 |

### Oversubscription regime summary (`cores=4`, `2x`, `4x`)

| dataset | model | fit_s_cores | fit_s_2x_cores | fit_s_4x_cores | fit_ratio_2x_vs_cores | fit_ratio_4x_vs_cores |
| --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 1.34373 | 2.61504 | 3.14625 | 1.94611 | 2.34144 |
| large | sklearn_hgb | 1.63724 | 4.80108 | 6.31416 | 2.93243 | 3.85659 |
| large | sklearn_hgb_fixed | 1.62954 | 1.64391 | 1.64885 | 1.00882 | 1.01185 |
| large | xgboost_hist | 2.61711 | 2.58061 | 2.59948 | 0.986056 | 0.993265 |
| medium | lightgbm_hist | 2.28036 | 3.32656 | 4.33735 | 1.45879 | 1.90205 |
| medium | sklearn_hgb | 2.50018 | 5.7723 | 7.23649 | 2.30875 | 2.89438 |
| medium | sklearn_hgb_fixed | 2.46888 | 2.47662 | 2.47939 | 1.00314 | 1.00426 |
| medium | xgboost_hist | 3.11684 | 3.14449 | 3.1922 | 1.00887 | 1.02418 |
| small | lightgbm_hist | 0.591311 | 1.66034 | 2.27107 | 2.8079 | 3.84074 |
| small | sklearn_hgb | 0.84964 | 3.69067 | 5.27032 | 4.3438 | 6.203 |
| small | sklearn_hgb_fixed | 0.860104 | 0.849613 | 0.93626 | 0.987803 | 1.08854 |
| small | xgboost_hist | 0.962428 | 1.11702 | 1.06087 | 1.16063 | 1.10229 |

### Underperformance findings and root cause analysis

- Root cause signal: Native hotspots indicate synchronization/runtime overhead (OpenMP/pthread wait-heavy stacks).
- Issue (single_thread, dataset `large`): Best sklearn total is 1.055x slower than best alternative at thread=1.
  - Implementation plan:
    - Introduce adaptive thread gating based on node sample count and feature count.
    - Batch multiple frontier nodes per parallel region to increase task granularity.
    - Reduce barrier frequency by fusing short OpenMP regions in split/histogram paths.
- Issue (single_thread, dataset `small`): Best sklearn total is 1.086x slower than best alternative at thread=1.
  - Implementation plan:
    - Introduce adaptive thread gating based on node sample count and feature count.
    - Batch multiple frontier nodes per parallel region to increase task granularity.
    - Reduce barrier frequency by fusing short OpenMP regions in split/histogram paths.
- Issue (scalability, dataset `large`): Best sklearn speedup trails best alternative by 0.463 (1->regular max threads).
  - Implementation plan:
    - Introduce adaptive thread gating based on node sample count and feature count.
    - Batch multiple frontier nodes per parallel region to increase task granularity.
    - Reduce barrier frequency by fusing short OpenMP regions in split/histogram paths.
- Issue (scalability, dataset `small`): Best sklearn speedup trails best alternative by 0.693 (1->regular max threads).
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
| large | lightgbm_hist | 4 | 5.3734 | 1.53953 | 3.49028 |
| large | sklearn_hgb | 4 | 5.59087 | 1.88764 | 2.96184 |
| large | sklearn_hgb_fixed | 4 | 5.6837 | 1.87603 | 3.02964 |
| large | xgboost_hist | 4 | 7.40006 | 2.68574 | 2.75532 |
| medium | lightgbm_hist | 4 | 5.20613 | 1.5187 | 3.42802 |
| medium | sklearn_hgb | 4 | 5.42559 | 1.85345 | 2.92729 |
| medium | sklearn_hgb_fixed | 4 | 5.40072 | 1.82291 | 2.96269 |
| medium | xgboost_hist | 4 | 6.45764 | 2.22805 | 2.89834 |
| small | lightgbm_hist | 4 | 1.30788 | 0.420371 | 3.11125 |
| small | sklearn_hgb | 4 | 1.65148 | 0.694858 | 2.37671 |
| small | sklearn_hgb_fixed | 4 | 1.62532 | 0.699564 | 2.32333 |
| small | xgboost_hist | 4 | 1.9191 | 0.80161 | 2.39405 |

### Oversubscription regime summary (`cores=4`, `2x`, `4x`)

| dataset | model | fit_s_cores | fit_s_2x_cores | fit_s_4x_cores | fit_ratio_2x_vs_cores | fit_ratio_4x_vs_cores |
| --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 1.53953 | 2.84446 | 3.43889 | 1.84762 | 2.23372 |
| large | sklearn_hgb | 1.88764 | 5.42849 | 7.13318 | 2.87581 | 3.7789 |
| large | sklearn_hgb_fixed | 1.87603 | 1.84008 | 1.89626 | 0.980836 | 1.01079 |
| large | xgboost_hist | 2.68574 | 2.71607 | 2.78231 | 1.01129 | 1.03596 |
| medium | lightgbm_hist | 1.5187 | 2.80581 | 3.41899 | 1.84751 | 2.25126 |
| medium | sklearn_hgb | 1.85345 | 5.2636 | 6.96333 | 2.83989 | 3.75695 |
| medium | sklearn_hgb_fixed | 1.82291 | 1.82115 | 1.7893 | 0.999033 | 0.981561 |
| medium | xgboost_hist | 2.22805 | 2.25602 | 2.2976 | 1.01255 | 1.03121 |
| small | lightgbm_hist | 0.420371 | 1.35542 | 1.91384 | 3.22435 | 4.55273 |
| small | sklearn_hgb | 0.694858 | 3.52978 | 5.44674 | 5.07986 | 7.83863 |
| small | sklearn_hgb_fixed | 0.699564 | 0.691542 | 0.733293 | 0.988534 | 1.04822 |
| small | xgboost_hist | 0.80161 | 0.831167 | 0.841437 | 1.03687 | 1.04968 |

### Underperformance findings and root cause analysis

- Root cause signal: Native hotspots indicate synchronization/runtime overhead (OpenMP/pthread wait-heavy stacks).
- Issue (single_thread, dataset `small`): Best sklearn total is 1.224x slower than best alternative at thread=1.
  - Implementation plan:
    - Introduce adaptive thread gating based on node sample count and feature count.
    - Batch multiple frontier nodes per parallel region to increase task granularity.
    - Reduce barrier frequency by fusing short OpenMP regions in split/histogram paths.
- Issue (scalability, dataset `large`): Best sklearn speedup trails best alternative by 0.461 (1->regular max threads).
  - Implementation plan:
    - Introduce adaptive thread gating based on node sample count and feature count.
    - Batch multiple frontier nodes per parallel region to increase task granularity.
    - Reduce barrier frequency by fusing short OpenMP regions in split/histogram paths.
- Issue (scalability, dataset `medium`): Best sklearn speedup trails best alternative by 0.465 (1->regular max threads).
  - Implementation plan:
    - Introduce adaptive thread gating based on node sample count and feature count.
    - Batch multiple frontier nodes per parallel region to increase task granularity.
    - Reduce barrier frequency by fusing short OpenMP regions in split/histogram paths.
- Issue (scalability, dataset `small`): Best sklearn speedup trails best alternative by 0.735 (1->regular max threads).
  - Implementation plan:
    - Introduce adaptive thread gating based on node sample count and feature count.
    - Batch multiple frontier nodes per parallel region to increase task granularity.
    - Reduce barrier frequency by fusing short OpenMP regions in split/histogram paths.

