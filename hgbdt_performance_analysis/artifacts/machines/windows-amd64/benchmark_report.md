# Histogram GBDT Regressor Benchmark Report

## Experiment controls
- Timeout budget per individual run: `5.0 s`
- Adaptive reduction factor after timeout: `0.6`
- Threads tested: `[1, 2, 4, 8]`
- Dataset templates: `[{'name': 'small', 'start_n_samples': 12000, 'n_features': 24}, {'name': 'medium', 'start_n_samples': 180000, 'n_features': 120}]`

## Overall ranking (lower is faster)
| model | median_total_s | mean_total_s | geo_mean_total_s | mean_peak_rss_mb | mean_r2 | max_r2_spread_for_matched_scenario |
| --- | --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 0.716981 | 0.77851 | 0.708934 | 171.574 | 0.768005 | 0.0760385 |
| sklearn_hgb_fixed | 1.2486 | 1.25718 | 1.16136 | 167.192 | 0.736093 | 0.0760385 |
| sklearn_hgb | 1.25995 | 1.32727 | 1.23754 | 167.073 | 0.736093 | 0.0760385 |
| xgboost_hist | 1.52589 | 1.54962 | 1.38567 | 184.112 | 0.772938 | 0.0760385 |


## Single-thread behavior
| dataset_name | model | n_samples | n_features | fit_seconds | predict_seconds | total_seconds | peak_rss_mb | r2 | fitted_trees | expected_trees | total_nodes | avg_nodes_per_tree |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| medium | lightgbm_hist | 1813 | 120 | 1.63908 | 0.0072084 | 1.65313 | 177.188 | 0.586641 | 220 | 220 | 11256 | 51.1636 |
| medium | sklearn_hgb_fixed | 1813 | 120 | 2.21978 | 0.0133307 | 2.24024 | 169.535 | 0.529888 | 220 | 220 | 12398 | 56.3545 |
| medium | sklearn_hgb | 1813 | 120 | 2.22275 | 0.0134799 | 2.24094 | 169.527 | 0.529888 | 220 | 220 | 12398 | 56.3545 |
| medium | xgboost_hist | 1813 | 120 | 2.87877 | 0.0025319 | 2.88314 | 195.461 | 0.593432 | 220 | 220 | 11426 | 51.9364 |
| small | lightgbm_hist | 12000 | 24 | 0.753198 | 0.0370032 | 0.79975 | 164.57 | 0.949369 | 220 | 220 | 13386 | 60.8455 |
| small | sklearn_hgb_fixed | 12000 | 24 | 0.93398 | 0.0677232 | 1.00848 | 163.973 | 0.942299 | 220 | 220 | 13414 | 60.9727 |
| small | sklearn_hgb | 12000 | 24 | 0.947986 | 0.0675435 | 1.02066 | 163.777 | 0.942299 | 220 | 220 | 13414 | 60.9727 |
| small | xgboost_hist | 12000 | 24 | 1.19598 | 0.0092697 | 1.21123 | 171.359 | 0.948866 | 220 | 220 | 13394 | 60.8818 |


## Multi-thread scalability
| dataset_name | model | max_threads | fit_s_1_thread | fit_s_max_threads | speedup_vs_1_thread | parallel_efficiency |
| --- | --- | --- | --- | --- | --- | --- |
| medium | lightgbm_hist | 8 | 1.63908 | 0.74263 | 2.20713 | 0.275891 |
| small | lightgbm_hist | 8 | 0.753198 | 0.470471 | 1.60094 | 0.200118 |
| medium | sklearn_hgb | 8 | 2.22275 | 1.73552 | 1.28074 | 0.160093 |
| small | sklearn_hgb | 8 | 0.947986 | 0.997709 | 0.950163 | 0.11877 |
| medium | sklearn_hgb_fixed | 8 | 2.21978 | 1.55253 | 1.42978 | 0.178723 |
| small | sklearn_hgb_fixed | 8 | 0.93398 | 0.739826 | 1.26243 | 0.157804 |
| medium | xgboost_hist | 8 | 2.87877 | 1.83707 | 1.56704 | 0.19588 |
| small | xgboost_hist | 8 | 1.19598 | 0.777292 | 1.53865 | 0.192332 |


## Memory growth trend (thread=1)
| model | smallest_samples | largest_samples | peak_mb_smallest | peak_mb_largest | approx_mb_per_1k_samples |
| --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 1813 | 12000 | 177.188 | 164.57 | -1.23856 |
| sklearn_hgb | 1813 | 12000 | 169.527 | 163.777 | -0.564445 |
| sklearn_hgb_fixed | 1813 | 12000 | 169.535 | 163.973 | -0.546039 |
| xgboost_hist | 1813 | 12000 | 195.461 | 171.359 | -2.36591 |


## Initial conclusion
- Best median runtime model: `lightgbm_hist`
- Least-performing median runtime model: `xgboost_hist`
- All scenarios report explicit `r2_spread_for_scenario` to verify score parity while keeping matched hyperparameter values.
