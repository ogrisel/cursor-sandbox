# Detailed platform analysis: macos-arm64

- System: `Darwin`
- Architecture: `arm64`
- CPU count (logical): `3`
- CPU count (physical): `3`
- Hyper-threading enabled: `False`
- CPU model: `Apple M1 (Virtual)`
- Core type counts: `{'performance': 3, 'efficiency': None, 'low_power': None}`
- CFS/CPU quota: `n/a`
- CPU set: `n/a`
- Thread grid: `[1, 2, 3, 6]`
- Native profile enabled: `True`

## Setting: `baseline_default`

![scalability-baseline_default](scalability.png)

![absolute-fit-time-baseline_default](fit_time_threads.png)

_Vertical markers denote `cores=3` and `2x=6` thread regimes._

### Parity checks (thread=1)

| dataset | model | r2 | fitted_trees | expected_trees | trees_match | total_nodes | avg_nodes_per_tree |
| --- | --- | --- | --- | --- | --- | --- | --- |
| medium | lightgbm_hist | 0.508565 | 220 | 220 | True | 6114 | 27.7909 |
| medium | sklearn_hgb | 0.434502 | 220 | 220 | True | 7040 | 32 |
| medium | sklearn_hgb_fixed | 0.434502 | 220 | 220 | True | 7040 | 32 |
| medium | xgboost_hist | 0.47647 | 220 | 220 | True | 6168 | 28.0364 |
| small | lightgbm_hist | 0.911898 | 220 | 220 | True | 10082 | 45.8273 |
| small | sklearn_hgb | 0.897813 | 220 | 220 | True | 10976 | 49.8909 |
| small | sklearn_hgb_fixed | 0.897813 | 220 | 220 | True | 10976 | 49.8909 |
| small | xgboost_hist | 0.913386 | 220 | 220 | True | 10162 | 46.1909 |

### Scalability summary (`1 -> cores=3`)

| dataset | model | max_regular_threads | fit_s_1_thread | fit_s_regular_max_threads | speedup_1_to_regular_max |
| --- | --- | --- | --- | --- | --- |
| medium | lightgbm_hist | 3 | 0.320248 | 0.715046 | 0.447871 |
| medium | sklearn_hgb | 3 | 0.676866 | 0.971283 | 0.696879 |
| medium | sklearn_hgb_fixed | 3 | 0.642184 | 0.703187 | 0.913248 |
| medium | xgboost_hist | 3 | 0.917093 | 1.40069 | 0.654744 |
| small | lightgbm_hist | 3 | 0.304242 | 0.688646 | 0.441797 |
| small | sklearn_hgb | 3 | 0.541923 | 0.598627 | 0.905277 |
| small | sklearn_hgb_fixed | 3 | 0.52598 | 0.779819 | 0.67449 |
| small | xgboost_hist | 3 | 0.491953 | 1.33881 | 0.367454 |

### Oversubscription regime summary (`cores=3`, `2x`)

| dataset | model | fit_s_cores | fit_s_2x_cores | fit_ratio_2x_vs_cores |
| --- | --- | --- | --- | --- |
| medium | lightgbm_hist | 0.715046 | 1.09777 | 1.53525 |
| medium | sklearn_hgb | 0.971283 | 1.99884 | 2.05794 |
| medium | sklearn_hgb_fixed | 0.703187 | 0.754917 | 1.07357 |
| medium | xgboost_hist | 1.40069 | 1.42833 | 1.01973 |
| small | lightgbm_hist | 0.688646 | 1.63704 | 2.37719 |
| small | sklearn_hgb | 0.598627 | 2.47874 | 4.1407 |
| small | sklearn_hgb_fixed | 0.779819 | 0.576645 | 0.73946 |
| small | xgboost_hist | 1.33881 | 1.26272 | 0.943165 |

### Underperformance findings

- No material sklearn underperformance flags detected for this setting under current thresholds.

