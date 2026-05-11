# Histogram GBDT Regressor Benchmark Report

## Experiment controls
- Timeout budget per individual run: `5.0 s`
- Adaptive reduction factor after timeout: `0.6`
- Threads tested: `[1, 3, 6]`
- Dataset templates: `[{'name': 'small', 'start_n_samples': 12000, 'n_features': 24}, {'name': 'large', 'start_n_samples': 180000, 'n_features': 120}]`

## Overall ranking (lower is faster)
| model | median_total_s | mean_total_s | geo_mean_total_s | mean_peak_rss_mb | mean_r2 | max_r2_spread_for_matched_scenario |
| --- | --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 0.94445 | 1.06924 | 0.769872 | 203.659 | 0.780311 | 0.0413064 |
| xgboost_hist | 1.36872 | 1.61803 | 1.07986 | 214.852 | 0.789377 | 0.0413064 |
| sklearn_hgb | 1.40902 | 1.5515 | 1.26591 | 205.964 | 0.754284 | 0.0413064 |
| sklearn_hgb_fixed | 1.67468 | 1.64101 | 1.18298 | 210.086 | 0.754284 | 0.0413064 |


## Single-thread behavior
| dataset_name | model | n_samples | n_features | fit_seconds | predict_seconds | total_seconds | peak_rss_mb | r2 | fitted_trees | expected_trees | total_nodes | avg_nodes_per_tree |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 13996 | 120 | 2.25159 | 0.031882 | 2.31254 | 233.281 | 0.693811 | 220 | 220 | 13420 | 61 |
| large | sklearn_hgb_fixed | 13996 | 120 | 2.70259 | 0.0303633 | 2.74073 | 252.375 | 0.670338 | 220 | 220 | 13420 | 61 |
| large | sklearn_hgb | 13996 | 120 | 2.70069 | 0.0337031 | 2.78713 | 251.516 | 0.670338 | 220 | 220 | 13420 | 61 |
| large | xgboost_hist | 13996 | 120 | 3.68967 | 0.00604563 | 3.71553 | 265.75 | 0.699219 | 220 | 220 | 13420 | 61 |
| small | lightgbm_hist | 1555 | 24 | 0.139536 | 0.003806 | 0.193245 | 167.641 | 0.866811 | 220 | 220 | 8348 | 37.9455 |
| small | sklearn_hgb_fixed | 1555 | 24 | 0.241485 | 0.00327258 | 0.28118 | 168.5 | 0.838229 | 220 | 220 | 9210 | 41.8636 |
| small | sklearn_hgb | 1555 | 24 | 0.26505 | 0.00368162 | 0.288573 | 168.156 | 0.838229 | 220 | 220 | 9210 | 41.8636 |
| small | xgboost_hist | 1555 | 24 | 0.269276 | 0.00110083 | 0.326119 | 171.156 | 0.879536 | 220 | 220 | 8248 | 37.4909 |


## Multi-thread scalability
| dataset_name | model | max_threads | fit_s_1_thread | fit_s_max_threads | speedup_vs_1_thread | parallel_efficiency |
| --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 6 | 2.25159 | 1.54852 | 1.45403 | 0.242339 |
| small | lightgbm_hist | 6 | 0.139536 | 0.411702 | 0.338925 | 0.0564875 |
| large | sklearn_hgb | 6 | 2.70069 | 2.22128 | 1.21583 | 0.202638 |
| small | sklearn_hgb | 6 | 0.26505 | 1.36388 | 0.194335 | 0.0323891 |
| large | sklearn_hgb_fixed | 6 | 2.70259 | 1.87662 | 1.44014 | 0.240023 |
| small | sklearn_hgb_fixed | 6 | 0.241485 | 0.367639 | 0.656852 | 0.109475 |
| large | xgboost_hist | 6 | 3.68967 | 2.36085 | 1.56285 | 0.260476 |
| small | xgboost_hist | 6 | 0.269276 | 0.445476 | 0.604468 | 0.100745 |


## Memory growth trend (thread=1)
| model | smallest_samples | largest_samples | peak_mb_smallest | peak_mb_largest | approx_mb_per_1k_samples |
| --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 1555 | 13996 | 167.641 | 233.281 | 5.27615 |
| sklearn_hgb | 1555 | 13996 | 168.156 | 251.516 | 6.70038 |
| sklearn_hgb_fixed | 1555 | 13996 | 168.5 | 252.375 | 6.74182 |
| xgboost_hist | 1555 | 13996 | 171.156 | 265.75 | 7.60339 |


## Initial conclusion
- Best median runtime model: `lightgbm_hist`
- Least-performing median runtime model: `sklearn_hgb_fixed`
- All scenarios report explicit `r2_spread_for_scenario` to verify score parity while keeping matched hyperparameter values.
