# Histogram GBDT Regressor Benchmark Report

## Experiment controls
- Timeout budget per individual run: `10.0 s`
- Adaptive reduction factor after timeout: `0.6`
- Threads tested: `[1, 2, 4, 8, 16]`
- Dataset templates: `[{'name': 'small', 'start_n_samples': 50000, 'n_features': 40}, {'name': 'medium', 'start_n_samples': 140000, 'n_features': 80}, {'name': 'large', 'start_n_samples': 320000, 'n_features': 120}]`

## Overall ranking (lower is faster)
| model | median_total_s | mean_total_s | geo_mean_total_s | mean_peak_rss_mb | mean_r2 | max_r2_spread_for_matched_scenario |
| --- | --- | --- | --- | --- | --- | --- |
| sklearn_hgb_fixed | 1.85509 | 2.34182 | 1.91129 | 302.425 | 0.769548 | 0.0140304 |
| lightgbm_hist | 2.77726 | 3.0032 | 2.50404 | 322.195 | 0.778996 | 0.0140304 |
| xgboost_hist | 2.93847 | 3.21368 | 2.63504 | 312.917 | 0.779237 | 0.0140304 |
| sklearn_hgb | 3.72378 | 3.89376 | 3.21745 | 309.715 | 0.769548 | 0.0140304 |


## Single-thread behavior
| dataset_name | model | n_samples | n_features | fit_seconds | predict_seconds | total_seconds | peak_rss_mb | r2 | fitted_trees | expected_trees | total_nodes | avg_nodes_per_tree |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 41472 | 120 | 4.28914 | 0.106772 | 4.3978 | 304.762 | 0.690202 | 220 | 220 | 13420 | 61 |
| large | sklearn_hgb_fixed | 41472 | 120 | 4.53234 | 0.106218 | 4.64434 | 283.684 | 0.676171 | 220 | 220 | 13420 | 61 |
| large | sklearn_hgb | 41472 | 120 | 5.07145 | 0.11641 | 5.1983 | 283.281 | 0.676171 | 220 | 220 | 13420 | 61 |
| large | xgboost_hist | 41472 | 120 | 6.1681 | 0.023184 | 6.19716 | 321.922 | 0.689481 | 220 | 220 | 13420 | 61 |
| medium | sklearn_hgb | 140000 | 80 | 6.43286 | 0.291207 | 6.73197 | 374.129 | 0.745521 | 220 | 220 | 13420 | 61 |
| medium | sklearn_hgb_fixed | 140000 | 80 | 6.67976 | 0.301761 | 6.98755 | 374.094 | 0.745521 | 220 | 220 | 13420 | 61 |
| medium | lightgbm_hist | 140000 | 80 | 7.01002 | 0.314768 | 7.33387 | 400.934 | 0.753709 | 220 | 220 | 13420 | 61 |
| medium | xgboost_hist | 140000 | 80 | 8.28718 | 0.0615787 | 8.35375 | 370.074 | 0.75389 | 220 | 220 | 13420 | 61 |
| small | sklearn_hgb | 50000 | 40 | 1.61926 | 0.0907842 | 1.71167 | 229.348 | 0.886951 | 220 | 220 | 13420 | 61 |
| small | sklearn_hgb_fixed | 50000 | 40 | 1.61115 | 0.0974448 | 1.71316 | 229.59 | 0.886951 | 220 | 220 | 13420 | 61 |
| small | lightgbm_hist | 50000 | 40 | 1.60156 | 0.111133 | 1.71792 | 236.145 | 0.893078 | 220 | 220 | 13420 | 61 |
| small | xgboost_hist | 50000 | 40 | 2.12948 | 0.0228236 | 2.15752 | 240.16 | 0.894341 | 220 | 220 | 13420 | 61 |


## Multi-thread scalability
| dataset_name | model | max_threads | fit_s_1_thread | fit_s_max_threads | speedup_vs_1_thread | parallel_efficiency |
| --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 16 | 4.28914 | 3.53192 | 1.21439 | 0.0758995 |
| medium | lightgbm_hist | 16 | 7.01002 | 5.01454 | 1.39794 | 0.0873711 |
| small | lightgbm_hist | 16 | 1.60156 | 1.83623 | 0.872201 | 0.0545126 |
| large | sklearn_hgb | 16 | 5.07145 | 6.08649 | 0.833231 | 0.0520769 |
| medium | sklearn_hgb | 16 | 6.43286 | 7.99738 | 0.80437 | 0.0502731 |
| small | sklearn_hgb | 16 | 1.61926 | 4.75335 | 0.340656 | 0.021291 |
| large | sklearn_hgb_fixed | 16 | 4.53234 | 1.51299 | 2.99562 | 0.187226 |
| medium | sklearn_hgb_fixed | 16 | 6.67976 | 2.17519 | 3.07089 | 0.191931 |
| small | sklearn_hgb_fixed | 16 | 1.61115 | 0.728492 | 2.21162 | 0.138226 |
| large | xgboost_hist | 16 | 6.1681 | 3.07846 | 2.00363 | 0.125227 |
| medium | xgboost_hist | 16 | 8.28718 | 2.98284 | 2.77828 | 0.173643 |
| small | xgboost_hist | 16 | 2.12948 | 0.97975 | 2.17349 | 0.135843 |


## Memory growth trend (thread=1)
| model | smallest_samples | largest_samples | peak_mb_smallest | peak_mb_largest | approx_mb_per_1k_samples |
| --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 41472 | 140000 | 304.762 | 400.934 | 0.976087 |
| sklearn_hgb | 41472 | 140000 | 283.281 | 374.129 | 0.922049 |
| sklearn_hgb_fixed | 41472 | 140000 | 283.684 | 374.094 | 0.917609 |
| xgboost_hist | 41472 | 140000 | 321.922 | 370.074 | 0.488717 |


## Initial conclusion
- Best median runtime model: `sklearn_hgb_fixed`
- Least-performing median runtime model: `sklearn_hgb`
- All scenarios report explicit `r2_spread_for_scenario` to verify score parity while keeping matched hyperparameter values.
