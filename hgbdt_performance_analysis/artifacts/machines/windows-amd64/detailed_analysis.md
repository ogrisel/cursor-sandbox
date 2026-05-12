# Detailed platform analysis: windows-amd64

- System: `Windows`
- Architecture: `AMD64`
- CPU count (logical): `4`
- CPU count (physical): `2`
- Hyper-threading enabled: `True`
- CPU model: `AMD EPYC 7763 64-Core Processor`
- Core type counts: `{'performance': None, 'efficiency': None, 'low_power': None}`
- CFS/CPU quota: `n/a`
- CPU set: `n/a`
- Thread grid: `[1, 2, 4, 8]`
- Native profile enabled: `False`

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
| medium | xgboost_hist | 0.684843 | 220 | 220 | True | 13420 | 61 |
| small | lightgbm_hist | 0.949369 | 220 | 220 | True | 13386 | 60.8455 |
| small | sklearn_hgb | 0.942299 | 220 | 220 | True | 13414 | 60.9727 |
| small | sklearn_hgb_fixed | 0.942299 | 220 | 220 | True | 13414 | 60.9727 |
| small | xgboost_hist | 0.948866 | 220 | 220 | True | 13394 | 60.8818 |

### Scalability summary (`1 -> cores=4`)

| dataset | model | max_regular_threads | fit_s_1_thread | fit_s_regular_max_threads | speedup_1_to_regular_max |
| --- | --- | --- | --- | --- | --- |
| medium | lightgbm_hist | 4 | 12.3364 | 5.18168 | 2.38077 |
| medium | sklearn_hgb | 4 | 12.7535 | 6.30882 | 2.02154 |
| medium | sklearn_hgb_fixed | 4 | 12.714 | 6.17337 | 2.0595 |
| medium | xgboost_hist | 4 | 15.6394 | 8.98878 | 1.73987 |
| small | lightgbm_hist | 4 | 0.723327 | 0.343896 | 2.10333 |
| small | sklearn_hgb | 4 | 0.893586 | 0.698192 | 1.27986 |
| small | sklearn_hgb_fixed | 4 | 0.902376 | 0.707648 | 1.27518 |
| small | xgboost_hist | 4 | 1.1664 | 0.752824 | 1.54936 |

### Oversubscription regime summary (`cores=4`, `2x`)

| dataset | model | fit_s_cores | fit_s_2x_cores | fit_ratio_2x_vs_cores |
| --- | --- | --- | --- | --- |
| medium | lightgbm_hist | 5.18168 | 5.39866 | 1.04187 |
| medium | sklearn_hgb | 6.30882 | 6.45909 | 1.02382 |
| medium | sklearn_hgb_fixed | 6.17337 | 6.23939 | 1.01069 |
| medium | xgboost_hist | 8.98878 | 9.02686 | 1.00424 |
| small | lightgbm_hist | 0.343896 | 0.431244 | 1.254 |
| small | sklearn_hgb | 0.698192 | 0.948828 | 1.35898 |
| small | sklearn_hgb_fixed | 0.707648 | 0.697777 | 0.986051 |
| small | xgboost_hist | 0.752824 | 0.756086 | 1.00433 |

### Underperformance findings and root cause analysis

- Root cause signal: Underperformance likely combines tree-growth orchestration overhead and suboptimal threading granularity.
- Issue (single_thread, dataset `medium`): Best sklearn total is 1.084x slower than best alternative at thread=1.
  - Implementation plan:
    - Instrument per-stage timings (binning, split search, partitioning) inside sklearn HGBT fit loop.
    - Tune scheduling policy and chunk sizes to improve effective parallel work per task.
    - Prototype fused split+partition kernels to reduce memory traffic.
- Issue (single_thread, dataset `small`): Best sklearn total is 1.398x slower than best alternative at thread=1.
  - Implementation plan:
    - Instrument per-stage timings (binning, split search, partitioning) inside sklearn HGBT fit loop.
    - Tune scheduling policy and chunk sizes to improve effective parallel work per task.
    - Prototype fused split+partition kernels to reduce memory traffic.
- Issue (scalability, dataset `medium`): Best sklearn speedup trails best alternative by 0.321 (1->regular max threads).
  - Implementation plan:
    - Instrument per-stage timings (binning, split search, partitioning) inside sklearn HGBT fit loop.
    - Tune scheduling policy and chunk sizes to improve effective parallel work per task.
    - Prototype fused split+partition kernels to reduce memory traffic.
- Issue (scalability, dataset `small`): Best sklearn speedup trails best alternative by 0.823 (1->regular max threads).
  - Implementation plan:
    - Instrument per-stage timings (binning, split search, partitioning) inside sklearn HGBT fit loop.
    - Tune scheduling policy and chunk sizes to improve effective parallel work per task.
    - Prototype fused split+partition kernels to reduce memory traffic.

