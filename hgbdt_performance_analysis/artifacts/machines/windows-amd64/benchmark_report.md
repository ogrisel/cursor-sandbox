# Histogram GBDT Regressor Benchmark Report

## Experiment controls
- Timeout budget per individual run: `12.0 s`
- Adaptive reduction factor after timeout: `0.5`
- Threads tested: `[1, 2, 4, 8, 16]`
- Dataset templates: `[{'name': 'small', 'start_n_samples': 50000, 'n_features': 40}, {'name': 'medium', 'start_n_samples': 140000, 'n_features': 80}, {'name': 'large', 'start_n_samples': 320000, 'n_features': 120}]`

## Overall ranking (lower is faster)
| model | median_total_s | mean_total_s | geo_mean_total_s | mean_peak_rss_mb | mean_r2 | max_r2_spread_for_matched_scenario |
| --- | --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 2.79297 | 3.05309 | 2.70787 | 234.534 | 0.793002 | 0.0191276 |
| sklearn_hgb_fixed | 4.05138 | 3.97053 | 3.60187 | 229.197 | 0.782765 | 0.0191276 |
| sklearn_hgb | 4.06037 | 4.07937 | 3.74542 | 230.652 | 0.782765 | 0.0191276 |
| xgboost_hist | 4.42158 | 4.61767 | 4.15274 | 250.498 | 0.793471 | 0.0191276 |


## Single-thread behavior
| dataset_name | model | n_samples | n_features | fit_seconds | predict_seconds | total_seconds | peak_rss_mb | r2 | fitted_trees | expected_trees | total_nodes | avg_nodes_per_tree |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 40000 | 120 | 6.49309 | 0.128695 | 6.62974 | 247.879 | 0.692337 | 220 | 220 | 13420 | 61 |
| large | sklearn_hgb | 40000 | 120 | 7.68034 | 0.376642 | 8.05926 | 242.758 | 0.675577 | 220 | 220 | 13420 | 61 |
| large | sklearn_hgb_fixed | 40000 | 120 | 7.67244 | 0.393953 | 8.07248 | 243.27 | 0.675577 | 220 | 220 | 13420 | 61 |
| large | xgboost_hist | 40000 | 120 | 9.33896 | 0.0346706 | 9.38039 | 282.645 | 0.694704 | 220 | 220 | 13420 | 61 |
| medium | lightgbm_hist | 70000 | 80 | 6.04011 | 0.217602 | 6.26454 | 257.617 | 0.79359 | 220 | 220 | 13420 | 61 |
| medium | sklearn_hgb | 70000 | 80 | 6.75536 | 0.487311 | 7.24661 | 251.555 | 0.785099 | 220 | 220 | 13420 | 61 |
| medium | sklearn_hgb_fixed | 70000 | 80 | 6.76673 | 0.494035 | 7.26514 | 250.973 | 0.785099 | 220 | 220 | 13420 | 61 |
| medium | xgboost_hist | 70000 | 80 | 8.19298 | 0.0561747 | 8.25285 | 279.07 | 0.793602 | 220 | 220 | 13420 | 61 |
| small | lightgbm_hist | 50000 | 40 | 2.56243 | 0.156325 | 2.72691 | 192.48 | 0.893078 | 220 | 220 | 13420 | 61 |
| small | sklearn_hgb | 50000 | 40 | 3.02075 | 0.304799 | 3.32758 | 192.117 | 0.88762 | 220 | 220 | 13420 | 61 |
| small | sklearn_hgb_fixed | 50000 | 40 | 3.27314 | 0.303278 | 3.58163 | 192.32 | 0.88762 | 220 | 220 | 13420 | 61 |
| small | xgboost_hist | 50000 | 40 | 3.59205 | 0.0378873 | 3.63802 | 201.324 | 0.893059 | 220 | 220 | 13420 | 61 |


## Multi-thread scalability
| dataset_name | model | max_threads | fit_s_1_thread | fit_s_max_threads | speedup_vs_1_thread | parallel_efficiency |
| --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 16 | 6.49309 | 3.02242 | 2.14831 | 0.134269 |
| medium | lightgbm_hist | 16 | 6.04011 | 2.81507 | 2.14563 | 0.134102 |
| small | lightgbm_hist | 16 | 2.56243 | 1.37231 | 1.86724 | 0.116702 |
| large | sklearn_hgb | 16 | 7.68034 | 4.76002 | 1.61351 | 0.100844 |
| medium | sklearn_hgb | 16 | 6.75536 | 4.04277 | 1.67097 | 0.104436 |
| small | sklearn_hgb | 16 | 3.02075 | 2.34094 | 1.2904 | 0.0806501 |
| large | sklearn_hgb_fixed | 16 | 7.67244 | 4.09991 | 1.87137 | 0.11696 |
| medium | sklearn_hgb_fixed | 16 | 6.76673 | 4.19042 | 1.61481 | 0.100926 |
| small | sklearn_hgb_fixed | 16 | 3.27314 | 1.74405 | 1.87675 | 0.117297 |
| large | xgboost_hist | 16 | 9.33896 | 5.08123 | 1.83793 | 0.114871 |
| medium | xgboost_hist | 16 | 8.19298 | 4.38673 | 1.86767 | 0.11673 |
| small | xgboost_hist | 16 | 3.59205 | 1.99751 | 1.79826 | 0.112391 |


## Memory growth trend (thread=1)
| model | smallest_samples | largest_samples | peak_mb_smallest | peak_mb_largest | approx_mb_per_1k_samples |
| --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 40000 | 70000 | 247.879 | 257.617 | 0.324609 |
| sklearn_hgb | 40000 | 70000 | 242.758 | 251.555 | 0.293229 |
| sklearn_hgb_fixed | 40000 | 70000 | 243.27 | 250.973 | 0.256771 |
| xgboost_hist | 40000 | 70000 | 282.645 | 279.07 | -0.119141 |


## Initial conclusion
- Best median runtime model: `lightgbm_hist`
- Least-performing median runtime model: `xgboost_hist`
- All scenarios report explicit `r2_spread_for_scenario` to verify score parity while keeping matched hyperparameter values.
