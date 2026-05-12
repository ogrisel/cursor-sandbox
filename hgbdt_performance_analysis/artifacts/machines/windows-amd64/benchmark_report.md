# Histogram GBDT Regressor Benchmark Report

## Experiment controls
- Timeout budget per individual run: `5.0 s`
- Adaptive reduction factor after timeout: `0.6`
- Threads tested: `[1, 2, 4, 8]`
- Dataset templates: `[{'name': 'small', 'start_n_samples': 12000, 'n_features': 24}, {'name': 'medium', 'start_n_samples': 180000, 'n_features': 120}]`

## Overall ranking (lower is faster)
| model | median_total_s | mean_total_s | geo_mean_total_s | mean_peak_rss_mb | mean_r2 | max_r2_spread_for_matched_scenario |
| --- | --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 0.71444 | 0.786197 | 0.718521 | 171.255 | 0.768005 | 0.0760385 |
| sklearn_hgb_fixed | 1.26388 | 1.2498 | 1.15637 | 166.775 | 0.736093 | 0.0760385 |
| sklearn_hgb | 1.2842 | 1.31835 | 1.22941 | 167.447 | 0.736093 | 0.0760385 |
| xgboost_hist | 1.52707 | 1.54171 | 1.38894 | 180.761 | 0.772938 | 0.0760385 |


## Single-thread behavior
| dataset_name | model | n_samples | n_features | fit_seconds | predict_seconds | total_seconds | peak_rss_mb | r2 | fitted_trees | expected_trees | total_nodes | avg_nodes_per_tree |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| medium | lightgbm_hist | 1813 | 120 | 1.64421 | 0.0075293 | 1.65778 | 177.168 | 0.586641 | 220 | 220 | 11256 | 51.1636 |
| medium | sklearn_hgb_fixed | 1813 | 120 | 2.17257 | 0.0135351 | 2.19326 | 169.012 | 0.529888 | 220 | 220 | 12398 | 56.3545 |
| medium | sklearn_hgb | 1813 | 120 | 2.17953 | 0.0133158 | 2.20296 | 170.168 | 0.529888 | 220 | 220 | 12398 | 56.3545 |
| medium | xgboost_hist | 1813 | 120 | 2.85886 | 0.0023698 | 2.86636 | 194.059 | 0.593432 | 220 | 220 | 11426 | 51.9364 |
| small | lightgbm_hist | 12000 | 24 | 0.743814 | 0.0363171 | 0.789431 | 164.859 | 0.949369 | 220 | 220 | 13386 | 60.8455 |
| small | sklearn_hgb_fixed | 12000 | 24 | 0.933611 | 0.067374 | 1.00909 | 163.434 | 0.942299 | 220 | 220 | 13414 | 60.9727 |
| small | sklearn_hgb | 12000 | 24 | 0.949944 | 0.0681223 | 1.02231 | 163.789 | 0.942299 | 220 | 220 | 13414 | 60.9727 |
| small | xgboost_hist | 12000 | 24 | 1.17796 | 0.0092299 | 1.19295 | 170.441 | 0.948866 | 220 | 220 | 13394 | 60.8818 |


## Multi-thread scalability
| dataset_name | model | max_threads | fit_s_1_thread | fit_s_max_threads | speedup_vs_1_thread | parallel_efficiency |
| --- | --- | --- | --- | --- | --- | --- |
| medium | lightgbm_hist | 8 | 1.64421 | 0.730813 | 2.24984 | 0.28123 |
| small | lightgbm_hist | 8 | 0.743814 | 0.455889 | 1.63157 | 0.203946 |
| medium | sklearn_hgb | 8 | 2.17953 | 1.71804 | 1.26861 | 0.158577 |
| small | sklearn_hgb | 8 | 0.949944 | 0.972723 | 0.976582 | 0.122073 |
| medium | sklearn_hgb_fixed | 8 | 2.17257 | 1.50478 | 1.44378 | 0.180473 |
| small | sklearn_hgb_fixed | 8 | 0.933611 | 0.729567 | 1.27968 | 0.15996 |
| medium | xgboost_hist | 8 | 2.85886 | 1.85279 | 1.54301 | 0.192876 |
| small | xgboost_hist | 8 | 1.17796 | 0.782145 | 1.50607 | 0.188258 |


## Memory growth trend (thread=1)
| model | smallest_samples | largest_samples | peak_mb_smallest | peak_mb_largest | approx_mb_per_1k_samples |
| --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 1813 | 12000 | 177.168 | 164.859 | -1.20826 |
| sklearn_hgb | 1813 | 12000 | 170.168 | 163.789 | -0.626181 |
| sklearn_hgb_fixed | 1813 | 12000 | 169.012 | 163.434 | -0.547573 |
| xgboost_hist | 1813 | 12000 | 194.059 | 170.441 | -2.31837 |


## Initial conclusion
- Best median runtime model: `lightgbm_hist`
- Least-performing median runtime model: `xgboost_hist`
- All scenarios report explicit `r2_spread_for_scenario` to verify score parity while keeping matched hyperparameter values.
