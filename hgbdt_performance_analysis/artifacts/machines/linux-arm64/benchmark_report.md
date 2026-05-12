# Histogram GBDT Regressor Benchmark Report

## Experiment controls
- Timeout budget per individual run: `5.0 s`
- Adaptive reduction factor after timeout: `0.6`
- Threads tested: `[1, 2, 4, 8]`
- Dataset templates: `[{'name': 'small', 'start_n_samples': 12000, 'n_features': 24}, {'name': 'medium', 'start_n_samples': 180000, 'n_features': 120}]`

## Overall ranking (lower is faster)
| model | median_total_s | mean_total_s | geo_mean_total_s | mean_peak_rss_mb | mean_r2 | max_r2_spread_for_matched_scenario |
| --- | --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 0.807664 | 0.972324 | 0.788345 | 210.468 | 0.80576 | 0.0280657 |
| sklearn_hgb_fixed | 0.815542 | 0.95894 | 0.846475 | 207.521 | 0.788192 | 0.0280657 |
| sklearn_hgb | 1.12237 | 1.60459 | 1.25341 | 207.803 | 0.788192 | 0.0280657 |
| xgboost_hist | 1.1274 | 1.35116 | 1.07513 | 224.975 | 0.805608 | 0.0280657 |


## Single-thread behavior
| dataset_name | model | n_samples | n_features | fit_seconds | predict_seconds | total_seconds | peak_rss_mb | r2 | fitted_trees | expected_trees | total_nodes | avg_nodes_per_tree |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| medium | lightgbm_hist | 5038 | 120 | 1.85308 | 0.0126403 | 1.87321 | 216.902 | 0.66215 | 220 | 220 | 13326 | 60.5727 |
| medium | sklearn_hgb_fixed | 5038 | 120 | 2.17528 | 0.0134221 | 2.1957 | 215.066 | 0.634085 | 220 | 220 | 13402 | 60.9182 |
| medium | sklearn_hgb | 5038 | 120 | 2.18136 | 0.0129918 | 2.20173 | 215.555 | 0.634085 | 220 | 220 | 13402 | 60.9182 |
| medium | xgboost_hist | 5038 | 120 | 3.30414 | 0.00349139 | 3.31376 | 234.668 | 0.661463 | 220 | 220 | 13336 | 60.6182 |
| small | lightgbm_hist | 12000 | 24 | 0.535526 | 0.0242475 | 0.566931 | 202.312 | 0.949369 | 220 | 220 | 13386 | 60.8455 |
| small | sklearn_hgb | 12000 | 24 | 0.714097 | 0.0206789 | 0.738336 | 198.141 | 0.942299 | 220 | 220 | 13414 | 60.9727 |
| small | sklearn_hgb_fixed | 12000 | 24 | 0.725436 | 0.0206919 | 0.749148 | 198.145 | 0.942299 | 220 | 220 | 13414 | 60.9727 |
| small | xgboost_hist | 12000 | 24 | 0.833126 | 0.00631254 | 0.842303 | 206.398 | 0.949753 | 220 | 220 | 13390 | 60.8636 |


## Multi-thread scalability
| dataset_name | model | max_threads | fit_s_1_thread | fit_s_max_threads | speedup_vs_1_thread | parallel_efficiency |
| --- | --- | --- | --- | --- | --- | --- |
| medium | lightgbm_hist | 8 | 1.85308 | 1.95626 | 0.947257 | 0.118407 |
| small | lightgbm_hist | 8 | 0.535526 | 1.07764 | 0.496945 | 0.0621181 |
| medium | sklearn_hgb | 8 | 2.18136 | 3.5641 | 0.612036 | 0.0765045 |
| small | sklearn_hgb | 8 | 0.714097 | 2.96104 | 0.241164 | 0.0301455 |
| medium | sklearn_hgb_fixed | 8 | 2.17528 | 0.867043 | 2.50885 | 0.313606 |
| small | sklearn_hgb_fixed | 8 | 0.725436 | 0.485463 | 1.49432 | 0.18679 |
| medium | xgboost_hist | 8 | 3.30414 | 1.40619 | 2.34972 | 0.293715 |
| small | xgboost_hist | 8 | 0.833126 | 0.471942 | 1.76531 | 0.220664 |


## Memory growth trend (thread=1)
| model | smallest_samples | largest_samples | peak_mb_smallest | peak_mb_largest | approx_mb_per_1k_samples |
| --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 5038 | 12000 | 216.902 | 202.312 | -2.09564 |
| sklearn_hgb | 5038 | 12000 | 215.555 | 198.141 | -2.5013 |
| sklearn_hgb_fixed | 5038 | 12000 | 215.066 | 198.145 | -2.43061 |
| xgboost_hist | 5038 | 12000 | 234.668 | 206.398 | -4.06055 |


## Initial conclusion
- Best median runtime model: `lightgbm_hist`
- Least-performing median runtime model: `xgboost_hist`
- All scenarios report explicit `r2_spread_for_scenario` to verify score parity while keeping matched hyperparameter values.
