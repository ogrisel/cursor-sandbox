# Histogram GBDT Regressor Benchmark Report

## Experiment controls
- Timeout budget per individual run: `5.0 s`
- Adaptive reduction factor after timeout: `0.6`
- Threads tested: `[1, 2, 3, 6]`
- Dataset templates: `[{'name': 'small', 'start_n_samples': 12000, 'n_features': 24}, {'name': 'medium', 'start_n_samples': 180000, 'n_features': 120}]`

## Overall ranking (lower is faster)
| model | median_total_s | mean_total_s | geo_mean_total_s | mean_peak_rss_mb | mean_r2 | max_r2_spread_for_matched_scenario |
| --- | --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 0.870259 | 0.958365 | 0.87729 | 179.637 | 0.751436 | 0.0621126 |
| sklearn_hgb_fixed | 1.04154 | 1.11976 | 1.00644 | 183.201 | 0.720734 | 0.0621126 |
| sklearn_hgb | 1.39908 | 1.72341 | 1.33531 | 182.08 | 0.720734 | 0.0621126 |
| xgboost_hist | 1.53307 | 1.44822 | 1.33503 | 191.002 | 0.755517 | 0.0621126 |


## Single-thread behavior
| dataset_name | model | n_samples | n_features | fit_seconds | predict_seconds | total_seconds | peak_rss_mb | r2 | fitted_trees | expected_trees | total_nodes | avg_nodes_per_tree |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| medium | lightgbm_hist | 1087 | 120 | 0.648143 | 0.00318 | 0.652305 | 181.734 | 0.553503 | 220 | 220 | 8646 | 39.3 |
| medium | sklearn_hgb_fixed | 1087 | 120 | 0.939276 | 0.00318513 | 0.979727 | 189.578 | 0.499169 | 220 | 220 | 9918 | 45.0818 |
| medium | sklearn_hgb | 1087 | 120 | 1.06066 | 0.00439392 | 1.09753 | 188.5 | 0.499169 | 220 | 220 | 9918 | 45.0818 |
| medium | xgboost_hist | 1087 | 120 | 1.2587 | 0.00107954 | 1.26736 | 200.953 | 0.561282 | 220 | 220 | 8630 | 39.2273 |
| small | lightgbm_hist | 12000 | 24 | 0.446068 | 0.0216448 | 0.477679 | 177.562 | 0.949369 | 220 | 220 | 13386 | 60.8455 |
| small | sklearn_hgb_fixed | 12000 | 24 | 0.572623 | 0.0178775 | 0.611044 | 178.156 | 0.942299 | 220 | 220 | 13414 | 60.9727 |
| small | sklearn_hgb | 12000 | 24 | 0.630643 | 0.018499 | 0.678996 | 178.188 | 0.942299 | 220 | 220 | 13414 | 60.9727 |
| small | xgboost_hist | 12000 | 24 | 0.676759 | 0.00658729 | 0.702498 | 182.891 | 0.949753 | 220 | 220 | 13390 | 60.8636 |


## Multi-thread scalability
| dataset_name | model | max_threads | fit_s_1_thread | fit_s_max_threads | speedup_vs_1_thread | parallel_efficiency |
| --- | --- | --- | --- | --- | --- | --- |
| medium | lightgbm_hist | 6 | 0.648143 | 1.35182 | 0.47946 | 0.0799101 |
| small | lightgbm_hist | 6 | 0.446068 | 1.5048 | 0.296431 | 0.0494052 |
| medium | sklearn_hgb | 6 | 1.06066 | 3.54593 | 0.299121 | 0.0498535 |
| small | sklearn_hgb | 6 | 0.630643 | 3.26162 | 0.193353 | 0.0322254 |
| medium | sklearn_hgb_fixed | 6 | 0.939276 | 1.27341 | 0.737608 | 0.122935 |
| small | sklearn_hgb_fixed | 6 | 0.572623 | 1.07754 | 0.531414 | 0.088569 |
| medium | xgboost_hist | 6 | 1.2587 | 2.11969 | 0.593814 | 0.098969 |
| small | xgboost_hist | 6 | 0.676759 | 1.75578 | 0.385446 | 0.0642409 |


## Memory growth trend (thread=1)
| model | smallest_samples | largest_samples | peak_mb_smallest | peak_mb_largest | approx_mb_per_1k_samples |
| --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 1087 | 12000 | 181.734 | 177.562 | -0.382285 |
| sklearn_hgb | 1087 | 12000 | 188.5 | 178.188 | -0.944974 |
| sklearn_hgb_fixed | 1087 | 12000 | 189.578 | 178.156 | -1.04663 |
| xgboost_hist | 1087 | 12000 | 200.953 | 182.891 | -1.65514 |


## Initial conclusion
- Best median runtime model: `lightgbm_hist`
- Least-performing median runtime model: `xgboost_hist`
- All scenarios report explicit `r2_spread_for_scenario` to verify score parity while keeping matched hyperparameter values.
