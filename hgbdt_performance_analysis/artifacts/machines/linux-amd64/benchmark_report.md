# Histogram GBDT Regressor Benchmark Report

## Experiment controls
- Timeout budget per individual run: `5.0 s`
- Adaptive reduction factor after timeout: `0.6`
- Threads tested: `[1, 2, 4, 8]`
- Dataset templates: `[{'name': 'small', 'start_n_samples': 12000, 'n_features': 24}, {'name': 'medium', 'start_n_samples': 180000, 'n_features': 120}]`

## Overall ranking (lower is faster)
| model | median_total_s | mean_total_s | geo_mean_total_s | mean_peak_rss_mb | mean_r2 | max_r2_spread_for_matched_scenario |
| --- | --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 1.6172 | 1.7012 | 1.68715 | 207.021 | 0.687688 | 0.0740629 |
| sklearn_hgb_fixed | 1.69627 | 1.72603 | 1.71998 | 198.945 | 0.636365 | 0.0740629 |
| sklearn_hgb | 1.77116 | 2.0959 | 2.00853 | 198.699 | 0.636365 | 0.0740629 |
| xgboost_hist | 1.82611 | 1.93054 | 1.90868 | 214.167 | 0.678003 | 0.0740629 |


## Single-thread behavior
| dataset_name | model | n_samples | n_features | fit_seconds | predict_seconds | total_seconds | peak_rss_mb | r2 | fitted_trees | expected_trees | total_nodes | avg_nodes_per_tree |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| medium | lightgbm_hist | 652 | 120 | 0.549469 | 0.00213765 | 1.60488 | 210.301 | 0.508565 | 220 | 220 | 6114 | 27.7909 |
| medium | xgboost_hist | 652 | 120 | 1.38104 | 0.000705853 | 1.88205 | 216.184 | 0.47647 | 220 | 220 | 6168 | 28.0364 |
| medium | sklearn_hgb | 652 | 120 | 0.767379 | 0.00306922 | 2.03561 | 199.742 | 0.434502 | 220 | 220 | 7040 | 32 |
| medium | sklearn_hgb_fixed | 652 | 120 | 0.774354 | 0.00307577 | 2.05785 | 200.289 | 0.434502 | 220 | 220 | 7040 | 32 |
| small | lightgbm_hist | 1555 | 24 | 0.237123 | 0.00453532 | 1.69387 | 202.438 | 0.866811 | 220 | 220 | 8348 | 37.9455 |
| small | xgboost_hist | 1555 | 24 | 0.421539 | 0.00126402 | 1.77018 | 208.605 | 0.879536 | 220 | 220 | 8248 | 37.4909 |
| small | sklearn_hgb | 1555 | 24 | 0.317431 | 0.00490778 | 1.77656 | 196.621 | 0.838229 | 220 | 220 | 9210 | 41.8636 |
| small | sklearn_hgb_fixed | 1555 | 24 | 0.32018 | 0.00497722 | 1.78624 | 196.586 | 0.838229 | 220 | 220 | 9210 | 41.8636 |


## Multi-thread scalability
| dataset_name | model | max_threads | fit_s_1_thread | fit_s_max_threads | speedup_vs_1_thread | parallel_efficiency |
| --- | --- | --- | --- | --- | --- | --- |
| medium | lightgbm_hist | 8 | 0.549469 | 0.902898 | 0.608562 | 0.0760702 |
| small | lightgbm_hist | 8 | 0.237123 | 1.00992 | 0.234794 | 0.0293492 |
| medium | sklearn_hgb | 8 | 0.767379 | 2.54598 | 0.301408 | 0.037676 |
| small | sklearn_hgb | 8 | 0.317431 | 2.84028 | 0.111761 | 0.0139701 |
| medium | sklearn_hgb_fixed | 8 | 0.774354 | 0.558282 | 1.38703 | 0.173379 |
| small | sklearn_hgb_fixed | 8 | 0.32018 | 0.317556 | 1.00826 | 0.126033 |
| medium | xgboost_hist | 8 | 1.38104 | 0.909197 | 1.51897 | 0.189871 |
| small | xgboost_hist | 8 | 0.421539 | 0.341558 | 1.23417 | 0.154271 |


## Memory growth trend (thread=1)
| model | smallest_samples | largest_samples | peak_mb_smallest | peak_mb_largest | approx_mb_per_1k_samples |
| --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 652 | 1555 | 210.301 | 202.438 | -8.70795 |
| sklearn_hgb | 652 | 1555 | 199.742 | 196.621 | -3.45636 |
| sklearn_hgb_fixed | 652 | 1555 | 200.289 | 196.586 | -4.10091 |
| xgboost_hist | 652 | 1555 | 216.184 | 208.605 | -8.39217 |


## Initial conclusion
- Best median runtime model: `lightgbm_hist`
- Least-performing median runtime model: `xgboost_hist`
- All scenarios report explicit `r2_spread_for_scenario` to verify score parity while keeping matched hyperparameter values.
