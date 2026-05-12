# Detailed platform analysis: linux-arm64

- System: `Linux`
- Architecture: `aarch64`
- CPU count (logical): `4`
- CPU count (physical): `4`
- Hyper-threading enabled: `False`
- CPU model: `Neoverse-N2`
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
| medium | lightgbm_hist | 0.685065 | 220 | 220 | True | 13420 | 61 |
| medium | sklearn_hgb | 0.673129 | 220 | 220 | True | 13420 | 61 |
| medium | sklearn_hgb_fixed | 0.673129 | 220 | 220 | True | 13420 | 61 |
| medium | xgboost_hist | 0.685182 | 220 | 220 | True | 13420 | 61 |
| small | lightgbm_hist | 0.949369 | 220 | 220 | True | 13386 | 60.8455 |
| small | sklearn_hgb | 0.942299 | 220 | 220 | True | 13414 | 60.9727 |
| small | sklearn_hgb_fixed | 0.942299 | 220 | 220 | True | 13414 | 60.9727 |
| small | xgboost_hist | 0.949753 | 220 | 220 | True | 13390 | 60.8636 |

### Scalability summary (`1 -> cores=4`)

| dataset | model | max_regular_threads | fit_s_1_thread | fit_s_regular_max_threads | speedup_1_to_regular_max |
| --- | --- | --- | --- | --- | --- |
| medium | lightgbm_hist | 4 | 10.1683 | 2.78559 | 3.65033 |
| medium | sklearn_hgb | 4 | 10.6328 | 3.19969 | 3.32308 |
| medium | sklearn_hgb_fixed | 4 | 10.4794 | 3.09416 | 3.38683 |
| medium | xgboost_hist | 4 | 13.2869 | 4.19814 | 3.16496 |
| small | lightgbm_hist | 4 | 0.532713 | 0.210057 | 2.53604 |
| small | sklearn_hgb | 4 | 0.725291 | 0.466692 | 1.55411 |
| small | sklearn_hgb_fixed | 4 | 0.722317 | 0.468852 | 1.54061 |
| small | xgboost_hist | 4 | 0.840391 | 0.423503 | 1.98438 |

### Oversubscription regime summary (`cores=4`, `2x`)

| dataset | model | fit_s_cores | fit_s_2x_cores | fit_ratio_2x_vs_cores |
| --- | --- | --- | --- | --- |
| medium | lightgbm_hist | 2.78559 | 3.9777 | 1.42796 |
| medium | sklearn_hgb | 3.19969 | 6.75509 | 2.11117 |
| medium | sklearn_hgb_fixed | 3.09416 | 3.03019 | 0.979324 |
| medium | xgboost_hist | 4.19814 | 4.20944 | 1.00269 |
| small | lightgbm_hist | 0.210057 | 1.24848 | 5.94354 |
| small | sklearn_hgb | 0.466692 | 3.12294 | 6.69165 |
| small | sklearn_hgb_fixed | 0.468852 | 0.505851 | 1.07892 |
| small | xgboost_hist | 0.423503 | 0.435928 | 1.02934 |

### Underperformance findings and root cause analysis

- Root cause signal: Native hotspots indicate synchronization/runtime overhead (OpenMP/pthread wait-heavy stacks).
- Issue (single_thread, dataset `small`): Best sklearn total is 1.229x slower than best alternative at thread=1.
  - Implementation plan:
    - Introduce adaptive thread gating based on node sample count and feature count.
    - Batch multiple frontier nodes per parallel region to increase task granularity.
    - Reduce barrier frequency by fusing short OpenMP regions in split/histogram paths.
- Issue (scalability, dataset `medium`): Best sklearn speedup trails best alternative by 0.264 (1->regular max threads).
  - Implementation plan:
    - Introduce adaptive thread gating based on node sample count and feature count.
    - Batch multiple frontier nodes per parallel region to increase task granularity.
    - Reduce barrier frequency by fusing short OpenMP regions in split/histogram paths.
- Issue (scalability, dataset `small`): Best sklearn speedup trails best alternative by 0.982 (1->regular max threads).
  - Implementation plan:
    - Introduce adaptive thread gating based on node sample count and feature count.
    - Batch multiple frontier nodes per parallel region to increase task granularity.
    - Reduce barrier frequency by fusing short OpenMP regions in split/histogram paths.

