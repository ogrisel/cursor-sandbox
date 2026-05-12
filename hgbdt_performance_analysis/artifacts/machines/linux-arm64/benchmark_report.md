# Histogram GBDT Regressor Benchmark Report

## Experiment controls
- Timeout budget per individual run: `5.0 s`
- Adaptive reduction factor after timeout: `0.6`
- Threads tested: `[1, 2, 4, 8]`
- Dataset templates: `[{'name': 'small', 'start_n_samples': 12000, 'n_features': 24}, {'name': 'medium', 'start_n_samples': 180000, 'n_features': 120}]`

## Overall ranking (lower is faster)
| model | median_total_s | mean_total_s | geo_mean_total_s | mean_peak_rss_mb | mean_r2 | max_r2_spread_for_matched_scenario |
| --- | --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 0.71548 | 0.840014 | 0.709888 | 208.711 | 0.784676 | 0.0405318 |
| sklearn_hgb_fixed | 0.783833 | 0.878703 | 0.803904 | 204.675 | 0.760875 | 0.0405318 |
| sklearn_hgb | 0.974196 | 1.53581 | 1.18851 | 204.986 | 0.760875 | 0.0405318 |
| xgboost_hist | 1.03935 | 1.19015 | 0.994031 | 221.907 | 0.782729 | 0.0405318 |


## Single-thread behavior
| dataset_name | model | n_samples | n_features | fit_seconds | predict_seconds | total_seconds | peak_rss_mb | r2 | fitted_trees | expected_trees | total_nodes | avg_nodes_per_tree |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| medium | lightgbm_hist | 3022 | 120 | 1.52631 | 0.00772269 | 1.53776 | 214.621 | 0.619983 | 220 | 220 | 12996 | 59.0727 |
| medium | sklearn_hgb_fixed | 3022 | 120 | 1.83168 | 0.00798347 | 1.84443 | 209.645 | 0.579451 | 220 | 220 | 13266 | 60.3 |
| medium | sklearn_hgb | 3022 | 120 | 1.85792 | 0.00868962 | 1.87368 | 209.656 | 0.579451 | 220 | 220 | 13266 | 60.3 |
| medium | xgboost_hist | 3022 | 120 | 2.70768 | 0.00273154 | 2.71134 | 232.758 | 0.615705 | 220 | 220 | 13032 | 59.2364 |
| small | lightgbm_hist | 12000 | 24 | 0.534244 | 0.0241743 | 0.567509 | 202.301 | 0.949369 | 220 | 220 | 13386 | 60.8455 |
| small | sklearn_hgb | 12000 | 24 | 0.738575 | 0.0208241 | 0.759869 | 198.148 | 0.942299 | 220 | 220 | 13414 | 60.9727 |
| small | sklearn_hgb_fixed | 12000 | 24 | 0.732712 | 0.0208128 | 0.760635 | 198.121 | 0.942299 | 220 | 220 | 13414 | 60.9727 |
| small | xgboost_hist | 12000 | 24 | 0.839744 | 0.00636584 | 0.850094 | 206.383 | 0.949753 | 220 | 220 | 13390 | 60.8636 |


## Multi-thread scalability
| dataset_name | model | max_threads | fit_s_1_thread | fit_s_max_threads | speedup_vs_1_thread | parallel_efficiency |
| --- | --- | --- | --- | --- | --- | --- |
| medium | lightgbm_hist | 8 | 1.52631 | 1.47965 | 1.03154 | 0.128942 |
| small | lightgbm_hist | 8 | 0.534244 | 1.1033 | 0.484224 | 0.0605279 |
| medium | sklearn_hgb | 8 | 1.85792 | 3.53052 | 0.526246 | 0.0657808 |
| small | sklearn_hgb | 8 | 0.738575 | 3.06939 | 0.240626 | 0.0300782 |
| medium | sklearn_hgb_fixed | 8 | 1.83168 | 0.796954 | 2.29835 | 0.287294 |
| small | sklearn_hgb_fixed | 8 | 0.732712 | 0.523727 | 1.39903 | 0.174879 |
| medium | xgboost_hist | 8 | 2.70768 | 1.23242 | 2.19705 | 0.274631 |
| small | xgboost_hist | 8 | 0.839744 | 0.476308 | 1.76303 | 0.220378 |


## Memory growth trend (thread=1)
| model | smallest_samples | largest_samples | peak_mb_smallest | peak_mb_largest | approx_mb_per_1k_samples |
| --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 3022 | 12000 | 214.621 | 202.301 | -1.37228 |
| sklearn_hgb | 3022 | 12000 | 209.656 | 198.148 | -1.28178 |
| sklearn_hgb_fixed | 3022 | 12000 | 209.645 | 198.121 | -1.28352 |
| xgboost_hist | 3022 | 12000 | 232.758 | 206.383 | -2.93774 |


## Initial conclusion
- Best median runtime model: `lightgbm_hist`
- Least-performing median runtime model: `xgboost_hist`
- All scenarios report explicit `r2_spread_for_scenario` to verify score parity while keeping matched hyperparameter values.
