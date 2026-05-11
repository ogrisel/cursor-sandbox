# Histogram GBDT Regressor Benchmark Report

## Experiment controls
- Timeout budget per individual run: `12.0 s`
- Adaptive reduction factor after timeout: `0.5`
- Threads tested: `[1, 2, 3, 6, 12]`
- Dataset templates: `[{'name': 'small', 'start_n_samples': 50000, 'n_features': 40}, {'name': 'medium', 'start_n_samples': 140000, 'n_features': 80}, {'name': 'large', 'start_n_samples': 320000, 'n_features': 120}]`

## Overall ranking (lower is faster)
| model | median_total_s | mean_total_s | geo_mean_total_s | mean_peak_rss_mb | mean_r2 | max_r2_spread_for_matched_scenario |
| --- | --- | --- | --- | --- | --- | --- |
| sklearn_hgb_fixed | 3.32594 | 3.99835 | 3.5423 | 386.702 | 0.764101 | 0.0132866 |
| sklearn_hgb | 4.16993 | 4.53123 | 4.24339 | 380.356 | 0.764101 | 0.0132866 |
| lightgbm_hist | 4.87682 | 4.3978 | 3.85691 | 436.993 | 0.772374 | 0.0132866 |
| xgboost_hist | 5.31234 | 4.87485 | 4.28058 | 430.805 | 0.773321 | 0.0132866 |


## Single-thread behavior
| dataset_name | model | n_samples | n_features | fit_seconds | predict_seconds | total_seconds | peak_rss_mb | r2 | fitted_trees | expected_trees | total_nodes | avg_nodes_per_tree |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 80000 | 120 | 6.55101 | 0.154461 | 6.75381 | 509.156 | 0.670334 | 220 | 220 | 13420 | 61 |
| large | sklearn_hgb | 80000 | 120 | 6.80019 | 0.258487 | 7.12079 | 469.359 | 0.658445 | 220 | 220 | 13420 | 61 |
| large | sklearn_hgb_fixed | 80000 | 120 | 6.97552 | 0.370512 | 7.3557 | 470.359 | 0.658445 | 220 | 220 | 13420 | 61 |
| large | xgboost_hist | 80000 | 120 | 8.41013 | 0.0426042 | 8.46511 | 548.531 | 0.671732 | 220 | 220 | 13420 | 61 |
| medium | sklearn_hgb | 140000 | 80 | 6.82315 | 0.22164 | 7.07591 | 460.984 | 0.746237 | 220 | 220 | 13420 | 61 |
| medium | sklearn_hgb_fixed | 140000 | 80 | 7.30941 | 0.263521 | 7.61402 | 460.766 | 0.746237 | 220 | 220 | 13420 | 61 |
| medium | lightgbm_hist | 140000 | 80 | 7.365 | 0.250635 | 7.63122 | 537.172 | 0.753709 | 220 | 220 | 13420 | 61 |
| medium | xgboost_hist | 140000 | 80 | 7.6959 | 0.082741 | 7.84553 | 515.781 | 0.75389 | 220 | 220 | 13420 | 61 |
| small | lightgbm_hist | 50000 | 40 | 2.29991 | 0.10405 | 2.41222 | 251.297 | 0.893078 | 220 | 220 | 13420 | 61 |
| small | sklearn_hgb | 50000 | 40 | 2.28328 | 0.126559 | 2.41433 | 234.016 | 0.88762 | 220 | 220 | 13420 | 61 |
| small | sklearn_hgb_fixed | 50000 | 40 | 2.40795 | 0.137085 | 2.563 | 233.094 | 0.88762 | 220 | 220 | 13420 | 61 |
| small | xgboost_hist | 50000 | 40 | 2.68392 | 0.0303042 | 2.73364 | 245.266 | 0.894341 | 220 | 220 | 13420 | 61 |


## Multi-thread scalability
| dataset_name | model | max_threads | fit_s_1_thread | fit_s_max_threads | speedup_vs_1_thread | parallel_efficiency |
| --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 12 | 6.55101 | 3.72017 | 1.76095 | 0.146746 |
| medium | lightgbm_hist | 12 | 7.365 | 6.90924 | 1.06596 | 0.0888302 |
| small | lightgbm_hist | 12 | 2.29991 | 1.81657 | 1.26607 | 0.105506 |
| large | sklearn_hgb | 12 | 6.80019 | 4.7161 | 1.44191 | 0.120159 |
| medium | sklearn_hgb | 12 | 6.82315 | 7.61703 | 0.895776 | 0.074648 |
| small | sklearn_hgb | 12 | 2.28328 | 3.68225 | 0.620077 | 0.0516731 |
| large | sklearn_hgb_fixed | 12 | 6.97552 | 2.51015 | 2.77893 | 0.231577 |
| medium | sklearn_hgb_fixed | 12 | 7.30941 | 5.4614 | 1.33838 | 0.111531 |
| small | sklearn_hgb_fixed | 12 | 2.40795 | 1.23067 | 1.95662 | 0.163052 |
| large | xgboost_hist | 12 | 8.41013 | 3.91143 | 2.15014 | 0.179179 |
| medium | xgboost_hist | 12 | 7.6959 | 5.52638 | 1.39257 | 0.116048 |
| small | xgboost_hist | 12 | 2.68392 | 1.60622 | 1.67095 | 0.139246 |


## Memory growth trend (thread=1)
| model | smallest_samples | largest_samples | peak_mb_smallest | peak_mb_largest | approx_mb_per_1k_samples |
| --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 50000 | 140000 | 251.297 | 537.172 | 3.17639 |
| sklearn_hgb | 50000 | 140000 | 234.016 | 460.984 | 2.52187 |
| sklearn_hgb_fixed | 50000 | 140000 | 233.094 | 460.766 | 2.52969 |
| xgboost_hist | 50000 | 140000 | 245.266 | 515.781 | 3.00573 |


## Initial conclusion
- Best median runtime model: `sklearn_hgb_fixed`
- Least-performing median runtime model: `xgboost_hist`
- All scenarios report explicit `r2_spread_for_scenario` to verify score parity while keeping matched hyperparameter values.
