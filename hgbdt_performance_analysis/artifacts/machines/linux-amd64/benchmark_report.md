# Histogram GBDT Regressor Benchmark Report

## Experiment controls
- Timeout budget per individual run: `8.0 s`
- Adaptive reduction factor after timeout: `0.5`
- Threads tested: `[1, 2, 4]`
- Dataset templates: `[{'name': 'small', 'start_n_samples': 50000, 'n_features': 40}, {'name': 'medium', 'start_n_samples': 140000, 'n_features': 80}, {'name': 'large', 'start_n_samples': 320000, 'n_features': 120}]`

## Overall ranking (lower is faster)
| model | median_total_s | mean_total_s | geo_mean_total_s | mean_peak_rss_mb | mean_r2 | max_r2_spread_for_matched_scenario |
| --- | --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 2.05909 | 2.53942 | 2.2061 | 283.829 | 0.793002 | 0.0177437 |
| sklearn_hgb | 2.09681 | 2.36839 | 2.12859 | 277.52 | 0.782765 | 0.0177437 |
| sklearn_hgb_fixed | 2.10272 | 2.35553 | 2.11644 | 277.351 | 0.782765 | 0.0177437 |
| xgboost_hist | 2.92685 | 3.20384 | 2.8453 | 302.812 | 0.793637 | 0.0177437 |


## Single-thread behavior
| dataset_name | model | n_samples | n_features | fit_seconds | predict_seconds | total_seconds | peak_rss_mb | r2 | fitted_trees | expected_trees | total_nodes | avg_nodes_per_tree |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| large | sklearn_hgb_fixed | 40000 | 120 | 4.20839 | 0.111163 | 4.32129 | 288.152 | 0.675577 | 220 | 220 | 13420 | 61 |
| large | sklearn_hgb | 40000 | 120 | 4.24922 | 0.11243 | 4.36248 | 288.23 | 0.675577 | 220 | 220 | 13420 | 61 |
| large | lightgbm_hist | 40000 | 120 | 4.88786 | 0.0998479 | 4.99538 | 287.77 | 0.692337 | 220 | 220 | 13420 | 61 |
| large | xgboost_hist | 40000 | 120 | 6.17215 | 0.0184157 | 6.19373 | 328.918 | 0.69332 | 220 | 220 | 13420 | 61 |
| medium | sklearn_hgb_fixed | 70000 | 80 | 4.00654 | 0.155022 | 4.16909 | 296.781 | 0.785099 | 220 | 220 | 13420 | 61 |
| medium | sklearn_hgb | 70000 | 80 | 4.01832 | 0.152615 | 4.17789 | 297.023 | 0.785099 | 220 | 220 | 13420 | 61 |
| medium | lightgbm_hist | 70000 | 80 | 4.56175 | 0.170423 | 4.73859 | 305.961 | 0.79359 | 220 | 220 | 13420 | 61 |
| medium | xgboost_hist | 70000 | 80 | 5.17406 | 0.0309695 | 5.20731 | 324.914 | 0.793248 | 220 | 220 | 13420 | 61 |
| small | sklearn_hgb_fixed | 50000 | 40 | 1.74299 | 0.101738 | 1.84548 | 237.617 | 0.88762 | 220 | 220 | 13420 | 61 |
| small | sklearn_hgb | 50000 | 40 | 1.79218 | 0.102186 | 1.89917 | 238.125 | 0.88762 | 220 | 220 | 13420 | 61 |
| small | lightgbm_hist | 50000 | 40 | 1.93594 | 0.120028 | 2.05909 | 243.652 | 0.893078 | 220 | 220 | 13420 | 61 |
| small | xgboost_hist | 50000 | 40 | 2.2531 | 0.02126 | 2.28058 | 250.551 | 0.894341 | 220 | 220 | 13420 | 61 |


## Multi-thread scalability
| dataset_name | model | max_threads | fit_s_1_thread | fit_s_max_threads | speedup_vs_1_thread | parallel_efficiency |
| --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 4 | 4.88786 | 1.98523 | 2.46211 | 0.615528 |
| medium | lightgbm_hist | 4 | 4.56175 | 1.88345 | 2.42202 | 0.605504 |
| small | lightgbm_hist | 4 | 1.93594 | 0.851125 | 2.27456 | 0.568641 |
| large | sklearn_hgb | 4 | 4.24922 | 2.05369 | 2.06907 | 0.517267 |
| medium | sklearn_hgb | 4 | 4.01832 | 1.92588 | 2.08649 | 0.521623 |
| small | sklearn_hgb | 4 | 1.79218 | 0.993343 | 1.80419 | 0.451047 |
| large | sklearn_hgb_fixed | 4 | 4.20839 | 2.05651 | 2.04638 | 0.511595 |
| medium | sklearn_hgb_fixed | 4 | 4.00654 | 1.89852 | 2.11034 | 0.527586 |
| small | sklearn_hgb_fixed | 4 | 1.74299 | 0.982948 | 1.77323 | 0.443308 |
| large | xgboost_hist | 4 | 6.17215 | 3.30429 | 1.86792 | 0.466979 |
| medium | xgboost_hist | 4 | 5.17406 | 2.70227 | 1.91471 | 0.478677 |
| small | xgboost_hist | 4 | 2.2531 | 1.3 | 1.73316 | 0.433289 |


## Memory growth trend (thread=1)
| model | smallest_samples | largest_samples | peak_mb_smallest | peak_mb_largest | approx_mb_per_1k_samples |
| --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 40000 | 70000 | 287.77 | 305.961 | 0.60638 |
| sklearn_hgb | 40000 | 70000 | 288.23 | 297.023 | 0.293099 |
| sklearn_hgb_fixed | 40000 | 70000 | 288.152 | 296.781 | 0.28763 |
| xgboost_hist | 40000 | 70000 | 328.918 | 324.914 | -0.133464 |


## Initial conclusion
- Best median runtime model: `lightgbm_hist`
- Least-performing median runtime model: `xgboost_hist`
- All scenarios report explicit `r2_spread_for_scenario` to verify score parity while keeping matched hyperparameter values.
