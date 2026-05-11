# Histogram GBDT Regressor Benchmark Report

## Experiment controls
- Timeout budget per individual run: `12.0 s`
- Adaptive reduction factor after timeout: `0.5`
- Threads tested: `[1, 2, 4, 8, 16]`
- Dataset templates: `[{'name': 'small', 'start_n_samples': 50000, 'n_features': 40}, {'name': 'medium', 'start_n_samples': 140000, 'n_features': 80}, {'name': 'large', 'start_n_samples': 320000, 'n_features': 120}]`

## Overall ranking (lower is faster)
| model | median_total_s | mean_total_s | geo_mean_total_s | mean_peak_rss_mb | mean_r2 | max_r2_spread_for_matched_scenario |
| --- | --- | --- | --- | --- | --- | --- |
| sklearn_hgb_fixed | 2.17079 | 2.68611 | 2.16465 | 298.697 | 0.769811 | 0.0177437 |
| lightgbm_hist | 2.55131 | 3.02348 | 2.51431 | 313.044 | 0.779708 | 0.0177437 |
| xgboost_hist | 2.62888 | 3.47675 | 2.79384 | 311.619 | 0.780517 | 0.0177437 |
| sklearn_hgb | 4.64392 | 4.24303 | 3.55208 | 305.233 | 0.769811 | 0.0177437 |


## Single-thread behavior
| dataset_name | model | n_samples | n_features | fit_seconds | predict_seconds | total_seconds | peak_rss_mb | r2 | fitted_trees | expected_trees | total_nodes | avg_nodes_per_tree |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 40000 | 120 | 4.79215 | 0.0837313 | 4.88339 | 278.91 | 0.692337 | 220 | 220 | 13420 | 61 |
| large | sklearn_hgb_fixed | 40000 | 120 | 5.05701 | 0.0889904 | 5.15131 | 278.609 | 0.675577 | 220 | 220 | 13420 | 61 |
| large | sklearn_hgb | 40000 | 120 | 5.07717 | 0.0888514 | 5.17259 | 278.484 | 0.675577 | 220 | 220 | 13420 | 61 |
| large | xgboost_hist | 40000 | 120 | 7.27568 | 0.0199771 | 7.29654 | 319.324 | 0.69332 | 220 | 220 | 13420 | 61 |
| medium | lightgbm_hist | 140000 | 80 | 8.12146 | 0.285135 | 8.40727 | 400.398 | 0.753709 | 220 | 220 | 13420 | 61 |
| medium | sklearn_hgb_fixed | 140000 | 80 | 8.33303 | 0.26928 | 8.60524 | 371.883 | 0.746237 | 220 | 220 | 13420 | 61 |
| medium | sklearn_hgb | 140000 | 80 | 8.42685 | 0.272227 | 8.7064 | 371.934 | 0.746237 | 220 | 220 | 13420 | 61 |
| medium | xgboost_hist | 140000 | 80 | 10.1674 | 0.0642243 | 10.2377 | 368.809 | 0.75389 | 220 | 220 | 13420 | 61 |
| small | lightgbm_hist | 50000 | 40 | 1.87855 | 0.113255 | 1.99922 | 234.93 | 0.893078 | 220 | 220 | 13420 | 61 |
| small | sklearn_hgb_fixed | 50000 | 40 | 2.08089 | 0.0858877 | 2.17079 | 227.859 | 0.88762 | 220 | 220 | 13420 | 61 |
| small | sklearn_hgb | 50000 | 40 | 2.11023 | 0.0856574 | 2.20485 | 228.004 | 0.88762 | 220 | 220 | 13420 | 61 |
| small | xgboost_hist | 50000 | 40 | 2.56541 | 0.023246 | 2.5893 | 240.828 | 0.894341 | 220 | 220 | 13420 | 61 |


## Multi-thread scalability
| dataset_name | model | max_threads | fit_s_1_thread | fit_s_max_threads | speedup_vs_1_thread | parallel_efficiency |
| --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 16 | 4.79215 | 3.14625 | 1.52313 | 0.0951956 |
| medium | lightgbm_hist | 16 | 8.12146 | 4.33735 | 1.87245 | 0.117028 |
| small | lightgbm_hist | 16 | 1.87855 | 2.27107 | 0.827168 | 0.051698 |
| large | sklearn_hgb | 16 | 5.07717 | 6.31416 | 0.804094 | 0.0502559 |
| medium | sklearn_hgb | 16 | 8.42685 | 7.23649 | 1.16449 | 0.0727809 |
| small | sklearn_hgb | 16 | 2.11023 | 5.27032 | 0.400399 | 0.025025 |
| large | sklearn_hgb_fixed | 16 | 5.05701 | 1.64885 | 3.067 | 0.191687 |
| medium | sklearn_hgb_fixed | 16 | 8.33303 | 2.47939 | 3.36092 | 0.210057 |
| small | sklearn_hgb_fixed | 16 | 2.08089 | 0.93626 | 2.22256 | 0.13891 |
| large | xgboost_hist | 16 | 7.27568 | 2.59948 | 2.7989 | 0.174931 |
| medium | xgboost_hist | 16 | 10.1674 | 3.1922 | 3.18508 | 0.199068 |
| small | xgboost_hist | 16 | 2.56541 | 1.06087 | 2.41821 | 0.151138 |


## Memory growth trend (thread=1)
| model | smallest_samples | largest_samples | peak_mb_smallest | peak_mb_largest | approx_mb_per_1k_samples |
| --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 40000 | 140000 | 278.91 | 400.398 | 1.21488 |
| sklearn_hgb | 40000 | 140000 | 278.484 | 371.934 | 0.934492 |
| sklearn_hgb_fixed | 40000 | 140000 | 278.609 | 371.883 | 0.932734 |
| xgboost_hist | 40000 | 140000 | 319.324 | 368.809 | 0.494844 |


## Initial conclusion
- Best median runtime model: `sklearn_hgb_fixed`
- Least-performing median runtime model: `sklearn_hgb`
- All scenarios report explicit `r2_spread_for_scenario` to verify score parity while keeping matched hyperparameter values.
