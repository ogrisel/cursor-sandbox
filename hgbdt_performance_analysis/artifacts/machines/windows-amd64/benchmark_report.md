# Histogram GBDT Regressor Benchmark Report

## Experiment controls
- Timeout budget per individual run: `5.0 s`
- Adaptive reduction factor after timeout: `0.6`
- Threads tested: `[1, 4, 8]`
- Dataset templates: `[{'name': 'small', 'start_n_samples': 12000, 'n_features': 24}, {'name': 'large', 'start_n_samples': 180000, 'n_features': 120}]`

## Overall ranking (lower is faster)
| model | median_total_s | mean_total_s | geo_mean_total_s | mean_peak_rss_mb | mean_r2 | max_r2_spread_for_matched_scenario |
| --- | --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 0.723693 | 0.791896 | 0.712018 | 171.156 | 0.768005 | 0.0654218 |
| sklearn_hgb_fixed | 1.23192 | 1.28875 | 1.1918 | 167.009 | 0.736093 | 0.0654218 |
| sklearn_hgb | 1.24701 | 1.38057 | 1.2963 | 167.71 | 0.736093 | 0.0654218 |
| xgboost_hist | 1.52545 | 1.5609 | 1.39633 | 182.459 | 0.771449 | 0.0654218 |


## Single-thread behavior
| dataset_name | model | n_samples | n_features | fit_seconds | predict_seconds | total_seconds | peak_rss_mb | r2 | fitted_trees | expected_trees | total_nodes | avg_nodes_per_tree |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 1813 | 120 | 1.61168 | 0.0075314 | 1.62903 | 175.684 | 0.586641 | 220 | 220 | 11256 | 51.1636 |
| large | sklearn_hgb_fixed | 1813 | 120 | 2.19479 | 0.0135289 | 2.21378 | 169.234 | 0.529888 | 220 | 220 | 12398 | 56.3545 |
| large | sklearn_hgb | 1813 | 120 | 2.22457 | 0.0139472 | 2.246 | 169.613 | 0.529888 | 220 | 220 | 12398 | 56.3545 |
| large | xgboost_hist | 1813 | 120 | 2.83257 | 0.0024113 | 2.84064 | 199.855 | 0.593432 | 220 | 220 | 11426 | 51.9364 |
| small | lightgbm_hist | 12000 | 24 | 0.747212 | 0.0371659 | 0.790882 | 166.426 | 0.949369 | 220 | 220 | 13386 | 60.8455 |
| small | sklearn_hgb | 12000 | 24 | 0.922864 | 0.0687416 | 0.997107 | 164.309 | 0.942299 | 220 | 220 | 13414 | 60.9727 |
| small | sklearn_hgb_fixed | 12000 | 24 | 0.931075 | 0.0669161 | 0.998276 | 163.809 | 0.942299 | 220 | 220 | 13414 | 60.9727 |
| small | xgboost_hist | 12000 | 24 | 1.17401 | 0.0090889 | 1.18818 | 166.82 | 0.948866 | 220 | 220 | 13394 | 60.8818 |


## Multi-thread scalability
| dataset_name | model | max_threads | fit_s_1_thread | fit_s_max_threads | speedup_vs_1_thread | parallel_efficiency |
| --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 8 | 1.61168 | 0.758074 | 2.12603 | 0.265753 |
| small | lightgbm_hist | 8 | 0.747212 | 0.458337 | 1.63027 | 0.203784 |
| large | sklearn_hgb | 8 | 2.22457 | 1.71576 | 1.29655 | 0.162069 |
| small | sklearn_hgb | 8 | 0.922864 | 0.993093 | 0.929283 | 0.11616 |
| large | sklearn_hgb_fixed | 8 | 2.19479 | 1.52966 | 1.43482 | 0.179353 |
| small | sklearn_hgb_fixed | 8 | 0.931075 | 0.731951 | 1.27204 | 0.159006 |
| large | xgboost_hist | 8 | 2.83257 | 1.88659 | 1.50142 | 0.187678 |
| small | xgboost_hist | 8 | 1.17401 | 0.781645 | 1.50197 | 0.187747 |


## Memory growth trend (thread=1)
| model | smallest_samples | largest_samples | peak_mb_smallest | peak_mb_largest | approx_mb_per_1k_samples |
| --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 1813 | 12000 | 175.684 | 166.426 | -0.908787 |
| sklearn_hgb | 1813 | 12000 | 169.613 | 164.309 | -0.520731 |
| sklearn_hgb_fixed | 1813 | 12000 | 169.234 | 163.809 | -0.532618 |
| xgboost_hist | 1813 | 12000 | 199.855 | 166.82 | -3.24287 |


## Initial conclusion
- Best median runtime model: `lightgbm_hist`
- Least-performing median runtime model: `xgboost_hist`
- All scenarios report explicit `r2_spread_for_scenario` to verify score parity while keeping matched hyperparameter values.
