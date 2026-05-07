# Histogram GBDT Regressor Benchmark Report

## Experiment controls
- Timeout budget per individual run: `8.0 s`
- Adaptive reduction factor after timeout: `0.5`
- Threads tested: `[1, 2, 4]`
- Dataset templates: `[{'name': 'small', 'start_n_samples': 50000, 'n_features': 40}, {'name': 'medium', 'start_n_samples': 140000, 'n_features': 80}, {'name': 'large', 'start_n_samples': 320000, 'n_features': 120}]`

## Overall ranking (lower is faster)
| model | median_total_s | mean_total_s | geo_mean_total_s | mean_peak_rss_mb | mean_r2 | max_r2_spread_for_matched_scenario |
| --- | --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 1.75883 | 2.07624 | 1.74096 | 260.057 | 0.787406 | 0.0223186 |
| sklearn_hgb | 2.16937 | 2.3786 | 2.08965 | 255.275 | 0.775317 | 0.0223186 |
| sklearn_hgb_fixed | 2.18567 | 2.38882 | 2.09444 | 255.273 | 0.775317 | 0.0223186 |
| xgboost_hist | 2.61357 | 3.16361 | 2.72444 | 277.342 | 0.786618 | 0.0223186 |


## Single-thread behavior
| dataset_name | model | n_samples | n_features | fit_seconds | predict_seconds | total_seconds | peak_rss_mb | r2 | fitted_trees | expected_trees | total_nodes | avg_nodes_per_tree |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 20000 | 120 | 3.31873 | 0.0424592 | 3.3616 | 235.598 | 0.675551 | 220 | 220 | 13420 | 61 |
| large | sklearn_hgb_fixed | 20000 | 120 | 3.64802 | 0.0463779 | 3.69804 | 242.363 | 0.653232 | 220 | 220 | 13420 | 61 |
| large | sklearn_hgb | 20000 | 120 | 3.6511 | 0.0469052 | 3.69959 | 242.387 | 0.653232 | 220 | 220 | 13420 | 61 |
| large | xgboost_hist | 20000 | 120 | 5.43607 | 0.0107217 | 5.4527 | 255.113 | 0.672265 | 220 | 220 | 13420 | 61 |
| medium | lightgbm_hist | 70000 | 80 | 4.71335 | 0.149247 | 4.87251 | 296.98 | 0.79359 | 220 | 220 | 13420 | 61 |
| medium | sklearn_hgb | 70000 | 80 | 4.89414 | 0.132518 | 5.03242 | 287.32 | 0.785099 | 220 | 220 | 13420 | 61 |
| medium | sklearn_hgb_fixed | 70000 | 80 | 4.97626 | 0.135973 | 5.11827 | 287.324 | 0.785099 | 220 | 220 | 13420 | 61 |
| medium | xgboost_hist | 70000 | 80 | 6.45483 | 0.0329267 | 6.4905 | 315.605 | 0.793248 | 220 | 220 | 13420 | 61 |
| small | lightgbm_hist | 50000 | 40 | 1.92118 | 0.109628 | 2.03929 | 234.91 | 0.893078 | 220 | 220 | 13420 | 61 |
| small | sklearn_hgb | 50000 | 40 | 2.20687 | 0.0864555 | 2.29767 | 228.012 | 0.88762 | 220 | 220 | 13420 | 61 |
| small | sklearn_hgb_fixed | 50000 | 40 | 2.21103 | 0.0859959 | 2.30425 | 227.898 | 0.88762 | 220 | 220 | 13420 | 61 |
| small | xgboost_hist | 50000 | 40 | 2.58826 | 0.0231228 | 2.61357 | 240.832 | 0.894341 | 220 | 220 | 13420 | 61 |


## Multi-thread scalability
| dataset_name | model | max_threads | fit_s_1_thread | fit_s_max_threads | speedup_vs_1_thread | parallel_efficiency |
| --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 4 | 3.31873 | 0.959185 | 3.45994 | 0.864986 |
| medium | lightgbm_hist | 4 | 4.71335 | 1.34056 | 3.51594 | 0.878986 |
| small | lightgbm_hist | 4 | 1.92118 | 0.619095 | 3.1032 | 0.7758 |
| large | sklearn_hgb | 4 | 3.6511 | 1.27596 | 2.86147 | 0.715366 |
| medium | sklearn_hgb | 4 | 4.89414 | 1.65709 | 2.95346 | 0.738365 |
| small | sklearn_hgb | 4 | 2.20687 | 0.877176 | 2.51588 | 0.628971 |
| large | sklearn_hgb_fixed | 4 | 3.64802 | 1.28659 | 2.83542 | 0.708855 |
| medium | sklearn_hgb_fixed | 4 | 4.97626 | 1.63578 | 3.04214 | 0.760534 |
| small | sklearn_hgb_fixed | 4 | 2.21103 | 0.868937 | 2.54452 | 0.636131 |
| large | xgboost_hist | 4 | 5.43607 | 2.11748 | 2.56723 | 0.641808 |
| medium | xgboost_hist | 4 | 6.45483 | 2.16492 | 2.98156 | 0.745389 |
| small | xgboost_hist | 4 | 2.58826 | 0.96825 | 2.67313 | 0.668283 |


## Memory growth trend (thread=1)
| model | smallest_samples | largest_samples | peak_mb_smallest | peak_mb_largest | approx_mb_per_1k_samples |
| --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 20000 | 70000 | 235.598 | 296.98 | 1.22766 |
| sklearn_hgb | 20000 | 70000 | 242.387 | 287.32 | 0.898672 |
| sklearn_hgb_fixed | 20000 | 70000 | 242.363 | 287.324 | 0.899219 |
| xgboost_hist | 20000 | 70000 | 255.113 | 315.605 | 1.20984 |


## Initial conclusion
- Best median runtime model: `lightgbm_hist`
- Least-performing median runtime model: `xgboost_hist`
- All scenarios report explicit `r2_spread_for_scenario` to verify score parity while keeping matched hyperparameter values.
