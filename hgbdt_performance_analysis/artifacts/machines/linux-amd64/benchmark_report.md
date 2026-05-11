# Histogram GBDT Regressor Benchmark Report

## Experiment controls
- Timeout budget per individual run: `5.0 s`
- Adaptive reduction factor after timeout: `0.6`
- Threads tested: `[1, 4, 8]`
- Dataset templates: `[{'name': 'small', 'start_n_samples': 12000, 'n_features': 24}, {'name': 'large', 'start_n_samples': 180000, 'n_features': 120}]`

## Overall ranking (lower is faster)
| model | median_total_s | mean_total_s | geo_mean_total_s | mean_peak_rss_mb | mean_r2 | max_r2_spread_for_matched_scenario |
| --- | --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 0.429723 | 0.560736 | 0.429865 | 205.277 | 0.687688 | 0.0740629 |
| sklearn_hgb_fixed | 0.490232 | 0.525574 | 0.493447 | 198.3 | 0.636365 | 0.0740629 |
| sklearn_hgb | 0.735086 | 1.35748 | 0.909949 | 198.538 | 0.636365 | 0.0740629 |
| xgboost_hist | 0.744253 | 0.794534 | 0.686008 | 211.601 | 0.678003 | 0.0740629 |


## Single-thread behavior
| dataset_name | model | n_samples | n_features | fit_seconds | predict_seconds | total_seconds | peak_rss_mb | r2 | fitted_trees | expected_trees | total_nodes | avg_nodes_per_tree |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 652 | 120 | 0.585759 | 0.00304809 | 0.593617 | 209.207 | 0.508565 | 220 | 220 | 6114 | 27.7909 |
| large | sklearn_hgb_fixed | 652 | 120 | 0.782511 | 0.00346003 | 0.794407 | 199.555 | 0.434502 | 220 | 220 | 7040 | 32 |
| large | sklearn_hgb | 652 | 120 | 0.783456 | 0.00355776 | 0.794851 | 199.797 | 0.434502 | 220 | 220 | 7040 | 32 |
| large | xgboost_hist | 652 | 120 | 1.43027 | 0.00138695 | 1.43617 | 216.434 | 0.47647 | 220 | 220 | 6168 | 28.0364 |
| small | lightgbm_hist | 1555 | 24 | 0.252421 | 0.00544453 | 0.265829 | 202.02 | 0.866811 | 220 | 220 | 8348 | 37.9455 |
| small | sklearn_hgb_fixed | 1555 | 24 | 0.33899 | 0.00546949 | 0.349494 | 195.699 | 0.838229 | 220 | 220 | 9210 | 41.8636 |
| small | sklearn_hgb | 1555 | 24 | 0.340813 | 0.00527335 | 0.349908 | 195.906 | 0.838229 | 220 | 220 | 9210 | 41.8636 |
| small | xgboost_hist | 1555 | 24 | 0.440792 | 0.00198977 | 0.449203 | 205.371 | 0.879536 | 220 | 220 | 8248 | 37.4909 |


## Multi-thread scalability
| dataset_name | model | max_threads | fit_s_1_thread | fit_s_max_threads | speedup_vs_1_thread | parallel_efficiency |
| --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 8 | 0.585759 | 1.02015 | 0.574189 | 0.0717737 |
| small | lightgbm_hist | 8 | 0.252421 | 1.07206 | 0.235454 | 0.0294318 |
| large | sklearn_hgb | 8 | 0.783456 | 2.77394 | 0.282434 | 0.0353043 |
| small | sklearn_hgb | 8 | 0.340813 | 3.14973 | 0.108204 | 0.0135255 |
| large | sklearn_hgb_fixed | 8 | 0.782511 | 0.680815 | 1.14937 | 0.143672 |
| small | sklearn_hgb_fixed | 8 | 0.33899 | 0.3356 | 1.0101 | 0.126263 |
| large | xgboost_hist | 8 | 1.43027 | 1.03113 | 1.38708 | 0.173385 |
| small | xgboost_hist | 8 | 0.440792 | 0.435271 | 1.01268 | 0.126585 |


## Memory growth trend (thread=1)
| model | smallest_samples | largest_samples | peak_mb_smallest | peak_mb_largest | approx_mb_per_1k_samples |
| --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 652 | 1555 | 209.207 | 202.02 | -7.95958 |
| sklearn_hgb | 652 | 1555 | 199.797 | 195.906 | -4.30855 |
| sklearn_hgb_fixed | 652 | 1555 | 199.555 | 195.699 | -4.26962 |
| xgboost_hist | 652 | 1555 | 216.434 | 205.371 | -12.2508 |


## Initial conclusion
- Best median runtime model: `lightgbm_hist`
- Least-performing median runtime model: `xgboost_hist`
- All scenarios report explicit `r2_spread_for_scenario` to verify score parity while keeping matched hyperparameter values.
