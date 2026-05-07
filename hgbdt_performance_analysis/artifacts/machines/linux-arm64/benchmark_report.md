# Histogram GBDT Regressor Benchmark Report

## Experiment controls
- Timeout budget per individual run: `8.0 s`
- Adaptive reduction factor after timeout: `0.5`
- Threads tested: `[1, 2, 4]`
- Dataset templates: `[{'name': 'small', 'start_n_samples': 50000, 'n_features': 40}, {'name': 'medium', 'start_n_samples': 140000, 'n_features': 80}, {'name': 'large', 'start_n_samples': 320000, 'n_features': 120}]`

## Overall ranking (lower is faster)
| model | median_total_s | mean_total_s | geo_mean_total_s | mean_peak_rss_mb | mean_r2 | max_r2_spread_for_matched_scenario |
| --- | --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 1.76539 | 2.05554 | 1.71751 | 232.341 | 0.787406 | 0.0223186 |
| sklearn_hgb_fixed | 2.15773 | 2.34458 | 2.04659 | 227.487 | 0.775317 | 0.0223186 |
| sklearn_hgb | 2.1675 | 2.34817 | 2.0578 | 227.497 | 0.775317 | 0.0223186 |
| xgboost_hist | 2.60685 | 3.15298 | 2.71398 | 249.562 | 0.786618 | 0.0223186 |


## Single-thread behavior
| dataset_name | model | n_samples | n_features | fit_seconds | predict_seconds | total_seconds | peak_rss_mb | r2 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 20000 | 120 | 3.31577 | 0.0427837 | 3.36213 | 207.855 | 0.675551 |
| large | sklearn_hgb | 20000 | 120 | 3.65155 | 0.0475967 | 3.69971 | 214.715 | 0.653232 |
| large | sklearn_hgb_fixed | 20000 | 120 | 3.66102 | 0.0469365 | 3.71386 | 214.684 | 0.653232 |
| large | xgboost_hist | 20000 | 120 | 5.45837 | 0.0107895 | 5.47037 | 227.355 | 0.672265 |
| medium | lightgbm_hist | 70000 | 80 | 4.63729 | 0.143553 | 4.7839 | 268.949 | 0.79359 |
| medium | sklearn_hgb | 70000 | 80 | 4.86891 | 0.134086 | 5.00467 | 259.277 | 0.785099 |
| medium | sklearn_hgb_fixed | 70000 | 80 | 4.89914 | 0.135088 | 5.03834 | 259.586 | 0.785099 |
| medium | xgboost_hist | 70000 | 80 | 6.38912 | 0.0328041 | 6.42944 | 287.84 | 0.793248 |
| small | lightgbm_hist | 50000 | 40 | 1.90118 | 0.0994248 | 2.00729 | 206.77 | 0.893078 |
| small | sklearn_hgb_fixed | 50000 | 40 | 2.09128 | 0.0860174 | 2.18613 | 200.219 | 0.88762 |
| small | sklearn_hgb | 50000 | 40 | 2.13052 | 0.0865576 | 2.22445 | 200.125 | 0.88762 |
| small | xgboost_hist | 50000 | 40 | 2.58075 | 0.0232697 | 2.60685 | 213.066 | 0.894341 |


## Multi-thread scalability
| dataset_name | model | max_threads | fit_s_1_thread | fit_s_max_threads | speedup_vs_1_thread | parallel_efficiency |
| --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 4 | 3.31577 | 0.950769 | 3.48745 | 0.871864 |
| medium | lightgbm_hist | 4 | 4.63729 | 1.32778 | 3.49252 | 0.873131 |
| small | lightgbm_hist | 4 | 1.90118 | 0.590965 | 3.21707 | 0.804267 |
| large | sklearn_hgb | 4 | 3.65155 | 1.29643 | 2.81663 | 0.704158 |
| medium | sklearn_hgb | 4 | 4.86891 | 1.62592 | 2.99456 | 0.748641 |
| small | sklearn_hgb | 4 | 2.13052 | 0.865052 | 2.46288 | 0.615719 |
| large | sklearn_hgb_fixed | 4 | 3.66102 | 1.3184 | 2.77687 | 0.694217 |
| medium | sklearn_hgb_fixed | 4 | 4.89914 | 1.5864 | 3.08822 | 0.772054 |
| small | sklearn_hgb_fixed | 4 | 2.09128 | 0.835259 | 2.50375 | 0.625937 |
| large | xgboost_hist | 4 | 5.45837 | 2.12336 | 2.57063 | 0.642657 |
| medium | xgboost_hist | 4 | 6.38912 | 2.13351 | 2.99466 | 0.748664 |
| small | xgboost_hist | 4 | 2.58075 | 0.971121 | 2.65749 | 0.664373 |


## Memory growth trend (thread=1)
| model | smallest_samples | largest_samples | peak_mb_smallest | peak_mb_largest | approx_mb_per_1k_samples |
| --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 20000 | 70000 | 207.855 | 268.949 | 1.22188 |
| sklearn_hgb | 20000 | 70000 | 214.715 | 259.277 | 0.89125 |
| sklearn_hgb_fixed | 20000 | 70000 | 214.684 | 259.586 | 0.898047 |
| xgboost_hist | 20000 | 70000 | 227.355 | 287.84 | 1.20969 |


## Initial conclusion
- Best median runtime model: `lightgbm_hist`
- Least-performing median runtime model: `xgboost_hist`
- All scenarios report explicit `r2_spread_for_scenario` to verify score parity while keeping matched hyperparameter values.
