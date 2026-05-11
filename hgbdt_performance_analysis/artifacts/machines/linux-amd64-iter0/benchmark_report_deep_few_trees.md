# Histogram GBDT Regressor Benchmark Report

## Experiment controls
- Timeout budget per individual run: `10.0 s`
- Adaptive reduction factor after timeout: `0.6`
- Threads tested: `[1, 2, 4, 8, 16]`
- Dataset templates: `[{'name': 'small', 'start_n_samples': 50000, 'n_features': 40}, {'name': 'medium', 'start_n_samples': 140000, 'n_features': 80}, {'name': 'large', 'start_n_samples': 320000, 'n_features': 120}]`

## Overall ranking (lower is faster)
| model | median_total_s | mean_total_s | geo_mean_total_s | mean_peak_rss_mb | mean_r2 | max_r2_spread_for_matched_scenario |
| --- | --- | --- | --- | --- | --- | --- |
| sklearn_hgb_fixed | 1.60595 | 2.2073 | 1.77021 | 387.971 | 0.608359 | 0.00353867 |
| xgboost_hist | 2.29546 | 3.0351 | 2.4874 | 385.247 | 0.607731 | 0.00353867 |
| lightgbm_hist | 2.37938 | 2.76246 | 2.22731 | 392.438 | 0.607389 | 0.00353867 |
| sklearn_hgb | 3.4407 | 3.71239 | 2.97913 | 397.548 | 0.608359 | 0.00353867 |


## Single-thread behavior
| dataset_name | model | n_samples | n_features | fit_seconds | predict_seconds | total_seconds | peak_rss_mb | r2 | fitted_trees | expected_trees | total_nodes | avg_nodes_per_tree |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| large | sklearn_hgb_fixed | 115200 | 120 | 5.93416 | 0.0856642 | 6.02353 | 473.898 | 0.506192 | 48 | 48 | 12144 | 253 |
| large | sklearn_hgb | 115200 | 120 | 6.08665 | 0.0857732 | 6.17748 | 473.43 | 0.506192 | 48 | 48 | 12144 | 253 |
| large | lightgbm_hist | 115200 | 120 | 6.32739 | 0.0899596 | 6.41762 | 464.969 | 0.503905 | 48 | 48 | 12144 | 253 |
| large | xgboost_hist | 115200 | 120 | 8.24531 | 0.0347366 | 8.28827 | 448.078 | 0.502653 | 48 | 48 | 12144 | 253 |
| medium | lightgbm_hist | 140000 | 80 | 5.56571 | 0.13117 | 5.70236 | 400.23 | 0.56851 | 48 | 48 | 12144 | 253 |
| medium | sklearn_hgb_fixed | 140000 | 80 | 5.63435 | 0.10534 | 5.74167 | 412.16 | 0.568121 | 48 | 48 | 12144 | 253 |
| medium | sklearn_hgb | 140000 | 80 | 5.65477 | 0.104596 | 5.7623 | 412.18 | 0.568121 | 48 | 48 | 12144 | 253 |
| medium | xgboost_hist | 140000 | 80 | 6.44218 | 0.0413278 | 6.49181 | 386.539 | 0.568178 | 48 | 48 | 12144 | 253 |
| small | lightgbm_hist | 50000 | 40 | 1.14655 | 0.0386717 | 1.18632 | 240.125 | 0.749752 | 48 | 48 | 12144 | 253 |
| small | sklearn_hgb_fixed | 50000 | 40 | 1.3266 | 0.0365764 | 1.37292 | 249.617 | 0.750765 | 48 | 48 | 12144 | 253 |
| small | sklearn_hgb | 50000 | 40 | 1.39284 | 0.0333101 | 1.43594 | 249.281 | 0.750765 | 48 | 48 | 12144 | 253 |
| small | xgboost_hist | 50000 | 40 | 1.69218 | 0.0140541 | 1.70952 | 284.73 | 0.752362 | 48 | 48 | 12144 | 253 |


## Multi-thread scalability
| dataset_name | model | max_threads | fit_s_1_thread | fit_s_max_threads | speedup_vs_1_thread | parallel_efficiency |
| --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 16 | 6.32739 | 4.27118 | 1.48141 | 0.0925884 |
| medium | lightgbm_hist | 16 | 5.56571 | 3.32925 | 1.67176 | 0.104485 |
| small | lightgbm_hist | 16 | 1.14655 | 1.84198 | 0.622456 | 0.0389035 |
| large | sklearn_hgb | 16 | 6.08665 | 7.74569 | 0.785811 | 0.0491132 |
| medium | sklearn_hgb | 16 | 5.65477 | 6.13804 | 0.921267 | 0.0575792 |
| small | sklearn_hgb | 16 | 1.39284 | 4.83688 | 0.287963 | 0.0179977 |
| large | sklearn_hgb_fixed | 16 | 5.93416 | 2.05824 | 2.88313 | 0.180195 |
| medium | sklearn_hgb_fixed | 16 | 5.63435 | 1.44938 | 3.88741 | 0.242963 |
| small | sklearn_hgb_fixed | 16 | 1.3266 | 0.762198 | 1.74049 | 0.108781 |
| large | xgboost_hist | 16 | 8.24531 | 3.10324 | 2.657 | 0.166063 |
| medium | xgboost_hist | 16 | 6.44218 | 2.22666 | 2.89321 | 0.180825 |
| small | xgboost_hist | 16 | 1.69218 | 1.04788 | 1.61486 | 0.100929 |


## Memory growth trend (thread=1)
| model | smallest_samples | largest_samples | peak_mb_smallest | peak_mb_largest | approx_mb_per_1k_samples |
| --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 50000 | 140000 | 240.125 | 400.23 | 1.77895 |
| sklearn_hgb | 50000 | 140000 | 249.281 | 412.18 | 1.80998 |
| sklearn_hgb_fixed | 50000 | 140000 | 249.617 | 412.16 | 1.80603 |
| xgboost_hist | 50000 | 140000 | 284.73 | 386.539 | 1.13121 |


## Initial conclusion
- Best median runtime model: `sklearn_hgb_fixed`
- Least-performing median runtime model: `sklearn_hgb`
- All scenarios report explicit `r2_spread_for_scenario` to verify score parity while keeping matched hyperparameter values.
