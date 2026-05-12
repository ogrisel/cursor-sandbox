# Histogram GBDT Regressor Benchmark Report

## Experiment controls
- Timeout budget per individual run: `5.0 s`
- Adaptive reduction factor after timeout: `0.6`
- Threads tested: `[1, 2, 4, 8]`
- Dataset templates: `[{'name': 'small', 'start_n_samples': 12000, 'n_features': 24}, {'name': 'medium', 'start_n_samples': 180000, 'n_features': 120}]`

## Overall ranking (lower is faster)
| model | median_total_s | mean_total_s | geo_mean_total_s | mean_peak_rss_mb | mean_r2 | max_r2_spread_for_matched_scenario |
| --- | --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 0.28993 | 0.475855 | 0.361677 | 204.739 | 0.687688 | 0.0740629 |
| sklearn_hgb_fixed | 0.457611 | 0.482565 | 0.456067 | 198.313 | 0.636365 | 0.0740629 |
| sklearn_hgb | 0.578606 | 1.10371 | 0.730657 | 198.352 | 0.636365 | 0.0740629 |
| xgboost_hist | 0.672669 | 0.72931 | 0.628003 | 211.433 | 0.678003 | 0.0740629 |


## Single-thread behavior
| dataset_name | model | n_samples | n_features | fit_seconds | predict_seconds | total_seconds | peak_rss_mb | r2 | fitted_trees | expected_trees | total_nodes | avg_nodes_per_tree |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| medium | lightgbm_hist | 652 | 120 | 0.573856 | 0.00292289 | 0.579152 | 208.406 | 0.508565 | 220 | 220 | 6114 | 27.7909 |
| medium | sklearn_hgb_fixed | 652 | 120 | 0.796677 | 0.00338179 | 0.804451 | 199.688 | 0.434502 | 220 | 220 | 7040 | 32 |
| medium | sklearn_hgb | 652 | 120 | 0.800289 | 0.00340509 | 0.806611 | 199.668 | 0.434502 | 220 | 220 | 7040 | 32 |
| medium | xgboost_hist | 652 | 120 | 1.44142 | 0.00140433 | 1.44972 | 216.594 | 0.47647 | 220 | 220 | 6168 | 28.0364 |
| small | lightgbm_hist | 1555 | 24 | 0.250301 | 0.00544148 | 0.264183 | 202.094 | 0.866811 | 220 | 220 | 8348 | 37.9455 |
| small | sklearn_hgb | 1555 | 24 | 0.33251 | 0.00529805 | 0.347471 | 195.785 | 0.838229 | 220 | 220 | 9210 | 41.8636 |
| small | sklearn_hgb_fixed | 1555 | 24 | 0.335904 | 0.00536143 | 0.349261 | 195.82 | 0.838229 | 220 | 220 | 9210 | 41.8636 |
| small | xgboost_hist | 1555 | 24 | 0.430639 | 0.00177284 | 0.437827 | 205.418 | 0.879536 | 220 | 220 | 8248 | 37.4909 |


## Multi-thread scalability
| dataset_name | model | max_threads | fit_s_1_thread | fit_s_max_threads | speedup_vs_1_thread | parallel_efficiency |
| --- | --- | --- | --- | --- | --- | --- |
| medium | lightgbm_hist | 8 | 0.573856 | 1.03415 | 0.554905 | 0.0693631 |
| small | lightgbm_hist | 8 | 0.250301 | 1.06003 | 0.236125 | 0.0295157 |
| medium | sklearn_hgb | 8 | 0.800289 | 2.74507 | 0.291537 | 0.0364421 |
| small | sklearn_hgb | 8 | 0.33251 | 3.07119 | 0.108267 | 0.0135334 |
| medium | sklearn_hgb_fixed | 8 | 0.796677 | 0.560889 | 1.42038 | 0.177548 |
| small | sklearn_hgb_fixed | 8 | 0.335904 | 0.335015 | 1.00265 | 0.125331 |
| medium | xgboost_hist | 8 | 1.44142 | 1.00685 | 1.43161 | 0.178951 |
| small | xgboost_hist | 8 | 0.430639 | 0.431329 | 0.998401 | 0.1248 |


## Memory growth trend (thread=1)
| model | smallest_samples | largest_samples | peak_mb_smallest | peak_mb_largest | approx_mb_per_1k_samples |
| --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 652 | 1555 | 208.406 | 202.094 | -6.99059 |
| sklearn_hgb | 652 | 1555 | 199.668 | 195.785 | -4.2999 |
| sklearn_hgb_fixed | 652 | 1555 | 199.688 | 195.82 | -4.2826 |
| xgboost_hist | 652 | 1555 | 216.594 | 205.418 | -12.3763 |


## Initial conclusion
- Best median runtime model: `lightgbm_hist`
- Least-performing median runtime model: `xgboost_hist`
- All scenarios report explicit `r2_spread_for_scenario` to verify score parity while keeping matched hyperparameter values.
