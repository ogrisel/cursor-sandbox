# Histogram GBDT Regressor Benchmark Report

## Experiment controls
- Timeout budget per individual run: `8.0 s`
- Adaptive reduction factor after timeout: `0.5`
- Threads tested: `[1, 2, 4]`
- Dataset templates: `[{'name': 'small', 'start_n_samples': 50000, 'n_features': 40}, {'name': 'medium', 'start_n_samples': 140000, 'n_features': 80}, {'name': 'large', 'start_n_samples': 320000, 'n_features': 120}]`

## Overall ranking (lower is faster)
| model | median_total_s | mean_total_s | geo_mean_total_s | mean_peak_rss_mb | mean_r2 | max_r2_spread_for_matched_scenario |
| --- | --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 1.58397 | 1.67394 | 1.53082 | 218.577 | 0.606182 | 0.00947562 |
| sklearn_hgb | 2.28919 | 2.46676 | 2.35735 | 228.762 | 0.603327 | 0.00947562 |
| sklearn_hgb_fixed | 2.31926 | 2.45965 | 2.35283 | 228.671 | 0.603327 | 0.00947562 |
| xgboost_hist | 3.79159 | 3.81438 | 3.60058 | 324.923 | 0.603505 | 0.00947562 |


## Single-thread behavior
| dataset_name | model | n_samples | n_features | fit_seconds | predict_seconds | total_seconds | peak_rss_mb | r2 | fitted_trees | expected_trees | total_nodes | avg_nodes_per_tree |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 10000 | 120 | 2.79955 | 0.0115283 | 2.81318 | 231.531 | 0.49027 | 48 | 48 | 12144 | 253 |
| large | sklearn_hgb_fixed | 10000 | 120 | 3.47497 | 0.0213541 | 3.4993 | 224.539 | 0.480794 | 48 | 48 | 12144 | 253 |
| large | sklearn_hgb | 10000 | 120 | 3.49591 | 0.021198 | 3.51938 | 227.168 | 0.480794 | 48 | 48 | 12144 | 253 |
| large | xgboost_hist | 10000 | 120 | 5.63497 | 0.0056796 | 5.64964 | 387.176 | 0.481133 | 48 | 48 | 12144 | 253 |
| medium | lightgbm_hist | 35000 | 80 | 2.98866 | 0.0349355 | 3.02459 | 224.992 | 0.578524 | 48 | 48 | 12144 | 253 |
| medium | sklearn_hgb | 35000 | 80 | 3.83913 | 0.0608319 | 3.9001 | 247.367 | 0.577725 | 48 | 48 | 12144 | 253 |
| medium | sklearn_hgb_fixed | 35000 | 80 | 3.84002 | 0.060473 | 3.90627 | 247.738 | 0.577725 | 48 | 48 | 12144 | 253 |
| medium | xgboost_hist | 35000 | 80 | 5.33204 | 0.0156458 | 5.35303 | 334.098 | 0.57702 | 48 | 48 | 12144 | 253 |
| small | lightgbm_hist | 50000 | 40 | 1.70275 | 0.048922 | 1.76038 | 198.195 | 0.749752 | 48 | 48 | 12144 | 253 |
| small | sklearn_hgb | 50000 | 40 | 2.19869 | 0.0846249 | 2.28407 | 211.879 | 0.751461 | 48 | 48 | 12144 | 253 |
| small | sklearn_hgb_fixed | 50000 | 40 | 2.21356 | 0.0837221 | 2.29841 | 211.121 | 0.751461 | 48 | 48 | 12144 | 253 |
| small | xgboost_hist | 50000 | 40 | 2.88419 | 0.0194608 | 2.90632 | 250.66 | 0.752362 | 48 | 48 | 12144 | 253 |


## Multi-thread scalability
| dataset_name | model | max_threads | fit_s_1_thread | fit_s_max_threads | speedup_vs_1_thread | parallel_efficiency |
| --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 4 | 2.79955 | 1.14179 | 2.4519 | 0.612976 |
| medium | lightgbm_hist | 4 | 2.98866 | 1.244 | 2.40247 | 0.600617 |
| small | lightgbm_hist | 4 | 1.70275 | 0.764206 | 2.22813 | 0.557032 |
| large | sklearn_hgb | 4 | 3.49591 | 2.27876 | 1.53413 | 0.383533 |
| medium | sklearn_hgb | 4 | 3.83913 | 2.35151 | 1.63262 | 0.408156 |
| small | sklearn_hgb | 4 | 2.19869 | 1.45348 | 1.5127 | 0.378176 |
| large | sklearn_hgb_fixed | 4 | 3.47497 | 2.27674 | 1.5263 | 0.381574 |
| medium | sklearn_hgb_fixed | 4 | 3.84002 | 2.33407 | 1.6452 | 0.411301 |
| small | sklearn_hgb_fixed | 4 | 2.21356 | 1.46119 | 1.5149 | 0.378726 |
| large | xgboost_hist | 4 | 5.63497 | 4.3036 | 1.30936 | 0.327341 |
| medium | xgboost_hist | 4 | 5.33204 | 3.74318 | 1.42447 | 0.356117 |
| small | xgboost_hist | 4 | 2.88419 | 2.02199 | 1.42641 | 0.356603 |


## Memory growth trend (thread=1)
| model | smallest_samples | largest_samples | peak_mb_smallest | peak_mb_largest | approx_mb_per_1k_samples |
| --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 10000 | 50000 | 231.531 | 198.195 | -0.833398 |
| sklearn_hgb | 10000 | 50000 | 227.168 | 211.879 | -0.382227 |
| sklearn_hgb_fixed | 10000 | 50000 | 224.539 | 211.121 | -0.335449 |
| xgboost_hist | 10000 | 50000 | 387.176 | 250.66 | -3.41289 |


## Initial conclusion
- Best median runtime model: `lightgbm_hist`
- Least-performing median runtime model: `xgboost_hist`
- All scenarios report explicit `r2_spread_for_scenario` to verify score parity while keeping matched hyperparameter values.
