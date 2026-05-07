# Histogram GBDT Regressor Benchmark Report

## Experiment controls
- Timeout budget per individual run: `8.0 s`
- Adaptive reduction factor after timeout: `0.5`
- Threads tested: `[1, 2, 4]`
- Dataset templates: `[{'name': 'small', 'start_n_samples': 50000, 'n_features': 40}, {'name': 'medium', 'start_n_samples': 140000, 'n_features': 80}, {'name': 'large', 'start_n_samples': 320000, 'n_features': 120}]`

## Overall ranking (lower is faster)
| model | median_total_s | mean_total_s | geo_mean_total_s | mean_peak_rss_mb | mean_r2 | max_r2_spread_for_matched_scenario |
| --- | --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 1.77861 | 2.06705 | 1.72634 | 232.303 | 0.787406 | 0.0223186 |
| sklearn_hgb | 2.18189 | 2.37952 | 2.08587 | 227.491 | 0.775317 | 0.0223186 |
| sklearn_hgb_fixed | 2.19312 | 2.37973 | 2.08111 | 227.562 | 0.775317 | 0.0223186 |
| xgboost_hist | 2.60779 | 3.19109 | 2.75566 | 249.59 | 0.786618 | 0.0223186 |


## Single-thread behavior
| dataset_name | model | n_samples | n_features | fit_seconds | predict_seconds | total_seconds | peak_rss_mb | r2 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 20000 | 120 | 3.30931 | 0.0424917 | 3.35663 | 207.859 | 0.675551 |
| large | sklearn_hgb | 20000 | 120 | 3.6766 | 0.0491719 | 3.72882 | 214.656 | 0.653232 |
| large | sklearn_hgb_fixed | 20000 | 120 | 3.6868 | 0.0498092 | 3.74601 | 214.664 | 0.653232 |
| large | xgboost_hist | 20000 | 120 | 5.45333 | 0.0107828 | 5.47331 | 227.469 | 0.672265 |
| medium | lightgbm_hist | 70000 | 80 | 4.68638 | 0.143654 | 4.83653 | 268.922 | 0.79359 |
| medium | sklearn_hgb | 70000 | 80 | 4.95576 | 0.139307 | 5.09734 | 259.473 | 0.785099 |
| medium | sklearn_hgb_fixed | 70000 | 80 | 4.98355 | 0.137853 | 5.12444 | 259.559 | 0.785099 |
| medium | xgboost_hist | 70000 | 80 | 6.4192 | 0.0330856 | 6.45241 | 287.84 | 0.793248 |
| small | lightgbm_hist | 50000 | 40 | 1.9025 | 0.0997158 | 2.0037 | 207.145 | 0.893078 |
| small | sklearn_hgb_fixed | 50000 | 40 | 2.1429 | 0.086771 | 2.23428 | 200.145 | 0.88762 |
| small | sklearn_hgb | 50000 | 40 | 2.14982 | 0.0860987 | 2.24372 | 200.121 | 0.88762 |
| small | xgboost_hist | 50000 | 40 | 2.58313 | 0.0232777 | 2.60779 | 213.062 | 0.894341 |


## Multi-thread scalability
| dataset_name | model | max_threads | fit_s_1_thread | fit_s_max_threads | speedup_vs_1_thread | parallel_efficiency |
| --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 4 | 3.30931 | 0.965014 | 3.42928 | 0.857321 |
| medium | lightgbm_hist | 4 | 4.68638 | 1.33672 | 3.50587 | 0.876468 |
| small | lightgbm_hist | 4 | 1.9025 | 0.599239 | 3.17486 | 0.793716 |
| large | sklearn_hgb | 4 | 3.6766 | 1.33935 | 2.74507 | 0.686267 |
| medium | sklearn_hgb | 4 | 4.95576 | 1.60972 | 3.07865 | 0.769662 |
| small | sklearn_hgb | 4 | 2.14982 | 0.867982 | 2.4768 | 0.6192 |
| large | sklearn_hgb_fixed | 4 | 3.6868 | 1.33008 | 2.77186 | 0.692964 |
| medium | sklearn_hgb_fixed | 4 | 4.98355 | 1.64125 | 3.03643 | 0.759108 |
| small | sklearn_hgb_fixed | 4 | 2.1429 | 0.854246 | 2.50853 | 0.627132 |
| large | xgboost_hist | 4 | 5.45333 | 2.20574 | 2.47233 | 0.618082 |
| medium | xgboost_hist | 4 | 6.4192 | 2.18964 | 2.93162 | 0.732906 |
| small | xgboost_hist | 4 | 2.58313 | 0.980979 | 2.63321 | 0.658303 |


## Memory growth trend (thread=1)
| model | smallest_samples | largest_samples | peak_mb_smallest | peak_mb_largest | approx_mb_per_1k_samples |
| --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 20000 | 70000 | 207.859 | 268.922 | 1.22125 |
| sklearn_hgb | 20000 | 70000 | 214.656 | 259.473 | 0.896328 |
| sklearn_hgb_fixed | 20000 | 70000 | 214.664 | 259.559 | 0.897891 |
| xgboost_hist | 20000 | 70000 | 227.469 | 287.84 | 1.20742 |


## Initial conclusion
- Best median runtime model: `lightgbm_hist`
- Least-performing median runtime model: `xgboost_hist`
- All scenarios report explicit `r2_spread_for_scenario` to verify score parity while keeping matched hyperparameter values.
