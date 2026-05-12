# Histogram GBDT Regressor Benchmark Report

## Experiment controls
- Timeout budget per individual run: `5.0 s`
- Adaptive reduction factor after timeout: `0.6`
- Threads tested: `[1, 3, 6]`
- Dataset templates: `[{'name': 'small', 'start_n_samples': 12000, 'n_features': 24}, {'name': 'medium', 'start_n_samples': 180000, 'n_features': 120}]`

## Overall ranking (lower is faster)
| model | median_total_s | mean_total_s | geo_mean_total_s | mean_peak_rss_mb | mean_r2 | max_r2_spread_for_matched_scenario |
| --- | --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 1.09495 | 1.16121 | 1.01884 | 208.529 | 0.82159 | 0.0288809 |
| sklearn_hgb_fixed | 1.32755 | 1.53702 | 1.39336 | 214.914 | 0.806318 | 0.0288809 |
| xgboost_hist | 1.58443 | 1.801 | 1.47301 | 220.341 | 0.824486 | 0.0288809 |
| sklearn_hgb | 2.04006 | 1.97765 | 1.78036 | 210.878 | 0.806318 | 0.0288809 |


## Single-thread behavior
| dataset_name | model | n_samples | n_features | fit_seconds | predict_seconds | total_seconds | peak_rss_mb | r2 | fitted_trees | expected_trees | total_nodes | avg_nodes_per_tree |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| medium | lightgbm_hist | 13996 | 120 | 2.12833 | 0.0271055 | 2.17478 | 245.625 | 0.693811 | 220 | 220 | 13420 | 61 |
| medium | sklearn_hgb_fixed | 13996 | 120 | 2.66656 | 0.0295148 | 2.69774 | 252.312 | 0.670338 | 220 | 220 | 13420 | 61 |
| medium | sklearn_hgb | 13996 | 120 | 2.68482 | 0.0298287 | 2.73113 | 252.078 | 0.670338 | 220 | 220 | 13420 | 61 |
| medium | xgboost_hist | 13996 | 120 | 3.701 | 0.00617338 | 3.70889 | 262.344 | 0.699219 | 220 | 220 | 13420 | 61 |
| small | lightgbm_hist | 12000 | 24 | 0.407695 | 0.0212794 | 0.441665 | 176.219 | 0.949369 | 220 | 220 | 13386 | 60.8455 |
| small | sklearn_hgb_fixed | 12000 | 24 | 0.597006 | 0.0189821 | 0.641432 | 177.422 | 0.942299 | 220 | 220 | 13414 | 60.9727 |
| small | xgboost_hist | 12000 | 24 | 0.662189 | 0.00623429 | 0.676017 | 180.766 | 0.949753 | 220 | 220 | 13390 | 60.8636 |
| small | sklearn_hgb | 12000 | 24 | 0.682941 | 0.0178504 | 0.742547 | 178.219 | 0.942299 | 220 | 220 | 13414 | 60.9727 |


## Multi-thread scalability
| dataset_name | model | max_threads | fit_s_1_thread | fit_s_max_threads | speedup_vs_1_thread | parallel_efficiency |
| --- | --- | --- | --- | --- | --- | --- |
| medium | lightgbm_hist | 6 | 2.12833 | 1.45728 | 1.46048 | 0.243414 |
| small | lightgbm_hist | 6 | 0.407695 | 0.847959 | 0.480796 | 0.0801326 |
| medium | sklearn_hgb | 6 | 2.68482 | 1.89594 | 1.41609 | 0.236016 |
| small | sklearn_hgb | 6 | 0.682941 | 2.84137 | 0.240356 | 0.0400594 |
| medium | sklearn_hgb_fixed | 6 | 2.66656 | 1.23013 | 2.16771 | 0.361284 |
| small | sklearn_hgb_fixed | 6 | 0.597006 | 2.04545 | 0.29187 | 0.0486451 |
| medium | xgboost_hist | 6 | 3.701 | 2.38879 | 1.54932 | 0.25822 |
| small | xgboost_hist | 6 | 0.662189 | 0.804786 | 0.822814 | 0.137136 |


## Memory growth trend (thread=1)
| model | smallest_samples | largest_samples | peak_mb_smallest | peak_mb_largest | approx_mb_per_1k_samples |
| --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 12000 | 13996 | 176.219 | 245.625 | 34.7727 |
| sklearn_hgb | 12000 | 13996 | 178.219 | 252.078 | 37.0037 |
| sklearn_hgb_fixed | 12000 | 13996 | 177.422 | 252.312 | 37.5204 |
| xgboost_hist | 12000 | 13996 | 180.766 | 262.344 | 40.8708 |


## Initial conclusion
- Best median runtime model: `lightgbm_hist`
- Least-performing median runtime model: `sklearn_hgb`
- All scenarios report explicit `r2_spread_for_scenario` to verify score parity while keeping matched hyperparameter values.
