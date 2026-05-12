# Detailed platform analysis: linux-amd64

- System: `Linux`
- Architecture: `x86_64`
- CPU count (logical): `4`
- CPU count (physical): `2`
- Hyper-threading enabled: `True`
- CPU model: `Intel(R) Xeon(R) Platinum 8370C CPU @ 2.80GHz`
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
| medium | lightgbm_hist | 4 | 10.8823 | 4.89169 | 2.22465 |
| medium | sklearn_hgb | 4 | 10.1744 | 4.96676 | 2.0485 |
| medium | sklearn_hgb_fixed | 4 | 10.0283 | 5.28576 | 1.89723 |
| medium | xgboost_hist | 4 | 12.9392 | 7.50333 | 1.72446 |
| small | lightgbm_hist | 4 | 0.568576 | 0.318356 | 1.78597 |
| small | sklearn_hgb | 4 | 0.695147 | 0.567231 | 1.22551 |
| small | sklearn_hgb_fixed | 4 | 0.690888 | 0.568871 | 1.21449 |
| small | xgboost_hist | 4 | 0.866713 | 0.662947 | 1.30736 |

### Oversubscription regime summary (`cores=4`, `2x`)

| dataset | model | fit_s_cores | fit_s_2x_cores | fit_ratio_2x_vs_cores |
| --- | --- | --- | --- | --- |
| medium | lightgbm_hist | 4.89169 | 6.01795 | 1.23024 |
| medium | sklearn_hgb | 4.96676 | 8.11518 | 1.6339 |
| medium | sklearn_hgb_fixed | 5.28576 | 5.03006 | 0.951624 |
| medium | xgboost_hist | 7.50333 | 7.43705 | 0.991166 |
| small | lightgbm_hist | 0.318356 | 1.35543 | 4.25759 |
| small | sklearn_hgb | 0.567231 | 3.43328 | 6.05271 |
| small | sklearn_hgb_fixed | 0.568871 | 0.564677 | 0.992627 |
| small | xgboost_hist | 0.662947 | 0.719384 | 1.08513 |

### Underperformance findings and root cause analysis

- Root cause signal: Native hotspots indicate synchronization/runtime overhead (OpenMP/pthread wait-heavy stacks).
- Issue (single_thread, dataset `small`): Best sklearn total is 1.147x slower than best alternative at thread=1.
  - Implementation plan:
    - Introduce adaptive thread gating based on node sample count and feature count.
    - Batch multiple frontier nodes per parallel region to increase task granularity.
    - Reduce barrier frequency by fusing short OpenMP regions in split/histogram paths.
- Issue (scalability, dataset `small`): Best sklearn speedup trails best alternative by 0.560 (1->regular max threads).
  - Implementation plan:
    - Introduce adaptive thread gating based on node sample count and feature count.
    - Batch multiple frontier nodes per parallel region to increase task granularity.
    - Reduce barrier frequency by fusing short OpenMP regions in split/histogram paths.

