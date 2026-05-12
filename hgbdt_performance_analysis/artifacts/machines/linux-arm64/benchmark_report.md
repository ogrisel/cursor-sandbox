# Histogram GBDT Regressor Benchmark Report

## Experiment controls
- Timeout budget per individual run: `5.0 s`
- Adaptive reduction factor after timeout: `0.6`
- Threads tested: `[1, 2, 4, 8]`
- Dataset templates: `[{'name': 'small', 'start_n_samples': 12000, 'n_features': 24}, {'name': 'medium', 'start_n_samples': 180000, 'n_features': 120}]`

## Overall ranking (lower is faster)
| model | median_total_s | mean_total_s | geo_mean_total_s | mean_peak_rss_mb | mean_r2 | max_r2_spread_for_matched_scenario |
| --- | --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 0.798531 | 0.918943 | 0.761976 | 209.6 | 0.80576 | 0.0280657 |
| sklearn_hgb_fixed | 0.806774 | 0.967294 | 0.865907 | 207.525 | 0.788192 | 0.0280657 |
| xgboost_hist | 1.11059 | 1.3513 | 1.07935 | 224.992 | 0.805608 | 0.0280657 |
| sklearn_hgb | 1.12338 | 1.61166 | 1.26126 | 207.87 | 0.788192 | 0.0280657 |


## Single-thread behavior
| dataset_name | model | n_samples | n_features | fit_seconds | predict_seconds | total_seconds | peak_rss_mb | r2 | fitted_trees | expected_trees | total_nodes | avg_nodes_per_tree |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| medium | lightgbm_hist | 5038 | 120 | 1.84388 | 0.0116671 | 1.86591 | 216.852 | 0.66215 | 220 | 220 | 13326 | 60.5727 |
| medium | sklearn_hgb_fixed | 5038 | 120 | 2.13363 | 0.012672 | 2.14682 | 215.066 | 0.634085 | 220 | 220 | 13402 | 60.9182 |
| medium | sklearn_hgb | 5038 | 120 | 2.16976 | 0.0132706 | 2.18737 | 215.555 | 0.634085 | 220 | 220 | 13402 | 60.9182 |
| medium | xgboost_hist | 5038 | 120 | 3.29806 | 0.00355202 | 3.31025 | 234.633 | 0.661463 | 220 | 220 | 13336 | 60.6182 |
| small | lightgbm_hist | 12000 | 24 | 0.531791 | 0.024167 | 0.560505 | 202.309 | 0.949369 | 220 | 220 | 13386 | 60.8455 |
| small | sklearn_hgb_fixed | 12000 | 24 | 0.71483 | 0.0205621 | 0.738595 | 198.145 | 0.942299 | 220 | 220 | 13414 | 60.9727 |
| small | sklearn_hgb | 12000 | 24 | 0.724463 | 0.0204504 | 0.751152 | 198.27 | 0.942299 | 220 | 220 | 13414 | 60.9727 |
| small | xgboost_hist | 12000 | 24 | 0.825295 | 0.00625456 | 0.840289 | 206.754 | 0.949753 | 220 | 220 | 13390 | 60.8636 |


## Multi-thread scalability
| dataset_name | model | max_threads | fit_s_1_thread | fit_s_max_threads | speedup_vs_1_thread | parallel_efficiency |
| --- | --- | --- | --- | --- | --- | --- |
| medium | lightgbm_hist | 8 | 1.84388 | 1.58657 | 1.16219 | 0.145273 |
| small | lightgbm_hist | 8 | 0.531791 | 1.05513 | 0.504004 | 0.0630005 |
| medium | sklearn_hgb | 8 | 2.16976 | 3.58878 | 0.604597 | 0.0755746 |
| small | sklearn_hgb | 8 | 0.724463 | 2.9769 | 0.243361 | 0.0304201 |
| medium | sklearn_hgb_fixed | 8 | 2.13363 | 0.866556 | 2.46219 | 0.307774 |
| small | sklearn_hgb_fixed | 8 | 0.71483 | 0.521165 | 1.3716 | 0.17145 |
| medium | xgboost_hist | 8 | 3.29806 | 1.43022 | 2.30599 | 0.288248 |
| small | xgboost_hist | 8 | 0.825295 | 0.479749 | 1.72026 | 0.215033 |


## Memory growth trend (thread=1)
| model | smallest_samples | largest_samples | peak_mb_smallest | peak_mb_largest | approx_mb_per_1k_samples |
| --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 5038 | 12000 | 216.852 | 202.309 | -2.08891 |
| sklearn_hgb | 5038 | 12000 | 215.555 | 198.27 | -2.48279 |
| sklearn_hgb_fixed | 5038 | 12000 | 215.066 | 198.145 | -2.43061 |
| xgboost_hist | 5038 | 12000 | 234.633 | 206.754 | -4.00444 |


## Initial conclusion
- Best median runtime model: `lightgbm_hist`
- Least-performing median runtime model: `sklearn_hgb`
- All scenarios report explicit `r2_spread_for_scenario` to verify score parity while keeping matched hyperparameter values.
