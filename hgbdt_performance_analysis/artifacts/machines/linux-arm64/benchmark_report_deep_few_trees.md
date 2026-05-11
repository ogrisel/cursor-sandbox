# Histogram GBDT Regressor Benchmark Report

## Experiment controls
- Timeout budget per individual run: `12.0 s`
- Adaptive reduction factor after timeout: `0.5`
- Threads tested: `[1, 2, 4, 8, 16]`
- Dataset templates: `[{'name': 'small', 'start_n_samples': 50000, 'n_features': 40}, {'name': 'medium', 'start_n_samples': 140000, 'n_features': 80}, {'name': 'large', 'start_n_samples': 320000, 'n_features': 120}]`

## Overall ranking (lower is faster)
| model | median_total_s | mean_total_s | geo_mean_total_s | mean_peak_rss_mb | mean_r2 | max_r2_spread_for_matched_scenario |
| --- | --- | --- | --- | --- | --- | --- |
| sklearn_hgb_fixed | 2.02728 | 2.42586 | 2.00059 | 362.387 | 0.603328 | 0.0026101 |
| xgboost_hist | 2.4746 | 2.97079 | 2.41133 | 371.521 | 0.603871 | 0.0026101 |
| lightgbm_hist | 2.93007 | 2.70573 | 2.22604 | 358.644 | 0.603228 | 0.0026101 |
| sklearn_hgb | 3.91638 | 4.26938 | 3.4942 | 369.896 | 0.603328 | 0.0026101 |


## Single-thread behavior
| dataset_name | model | n_samples | n_features | fit_seconds | predict_seconds | total_seconds | peak_rss_mb | r2 | fitted_trees | expected_trees | total_nodes | avg_nodes_per_tree |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 80000 | 120 | 5.62466 | 0.0587069 | 5.68663 | 364.371 | 0.491423 | 48 | 48 | 12144 | 253 |
| large | sklearn_hgb | 80000 | 120 | 6.10667 | 0.0655553 | 6.17551 | 408.535 | 0.490287 | 48 | 48 | 12144 | 253 |
| large | sklearn_hgb_fixed | 80000 | 120 | 6.17271 | 0.0713783 | 6.25064 | 408.527 | 0.490287 | 48 | 48 | 12144 | 253 |
| large | xgboost_hist | 80000 | 120 | 7.68508 | 0.0219553 | 7.71203 | 410.395 | 0.491074 | 48 | 48 | 12144 | 253 |
| medium | lightgbm_hist | 140000 | 80 | 5.44555 | 0.100013 | 5.54777 | 400.18 | 0.56851 | 48 | 48 | 12144 | 253 |
| medium | sklearn_hgb_fixed | 140000 | 80 | 5.75135 | 0.0975421 | 5.84912 | 410.469 | 0.568235 | 48 | 48 | 12144 | 253 |
| medium | sklearn_hgb | 140000 | 80 | 5.77285 | 0.105824 | 5.88544 | 410.492 | 0.568235 | 48 | 48 | 12144 | 253 |
| medium | xgboost_hist | 140000 | 80 | 6.58752 | 0.0349631 | 6.62889 | 385.18 | 0.568178 | 48 | 48 | 12144 | 253 |
| small | lightgbm_hist | 50000 | 40 | 1.36578 | 0.0349682 | 1.41043 | 238.812 | 0.749752 | 48 | 48 | 12144 | 253 |
| small | sklearn_hgb | 50000 | 40 | 1.76322 | 0.0266926 | 1.79377 | 247.145 | 0.751461 | 48 | 48 | 12144 | 253 |
| small | sklearn_hgb_fixed | 50000 | 40 | 1.76394 | 0.0268149 | 1.79658 | 247.121 | 0.751461 | 48 | 48 | 12144 | 253 |
| small | xgboost_hist | 50000 | 40 | 2.00587 | 0.0125036 | 2.01929 | 283.035 | 0.752362 | 48 | 48 | 12144 | 253 |


## Multi-thread scalability
| dataset_name | model | max_threads | fit_s_1_thread | fit_s_max_threads | speedup_vs_1_thread | parallel_efficiency |
| --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 16 | 5.62466 | 3.69919 | 1.52051 | 0.095032 |
| medium | lightgbm_hist | 16 | 5.44555 | 3.91131 | 1.39226 | 0.0870161 |
| small | lightgbm_hist | 16 | 1.36578 | 2.02845 | 0.673313 | 0.042082 |
| large | sklearn_hgb | 16 | 6.10667 | 7.75127 | 0.787829 | 0.0492393 |
| medium | sklearn_hgb | 16 | 5.77285 | 7.8907 | 0.731602 | 0.0457251 |
| small | sklearn_hgb | 16 | 1.76322 | 5.72692 | 0.307882 | 0.0192427 |
| large | sklearn_hgb_fixed | 16 | 6.17271 | 2.04974 | 3.01147 | 0.188217 |
| medium | sklearn_hgb_fixed | 16 | 5.75135 | 1.96544 | 2.92624 | 0.18289 |
| small | sklearn_hgb_fixed | 16 | 1.76394 | 0.817898 | 2.15667 | 0.134792 |
| large | xgboost_hist | 16 | 7.68508 | 2.91475 | 2.63662 | 0.164789 |
| medium | xgboost_hist | 16 | 6.58752 | 2.46293 | 2.67466 | 0.167166 |
| small | xgboost_hist | 16 | 2.00587 | 0.909308 | 2.20594 | 0.137871 |


## Memory growth trend (thread=1)
| model | smallest_samples | largest_samples | peak_mb_smallest | peak_mb_largest | approx_mb_per_1k_samples |
| --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 50000 | 140000 | 238.812 | 400.18 | 1.79297 |
| sklearn_hgb | 50000 | 140000 | 247.145 | 410.492 | 1.81497 |
| sklearn_hgb_fixed | 50000 | 140000 | 247.121 | 410.469 | 1.81497 |
| xgboost_hist | 50000 | 140000 | 283.035 | 385.18 | 1.13494 |


## Initial conclusion
- Best median runtime model: `sklearn_hgb_fixed`
- Least-performing median runtime model: `sklearn_hgb`
- All scenarios report explicit `r2_spread_for_scenario` to verify score parity while keeping matched hyperparameter values.
