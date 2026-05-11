# Histogram GBDT Regressor Benchmark Report

## Experiment controls
- Timeout budget per individual run: `12.0 s`
- Adaptive reduction factor after timeout: `0.5`
- Threads tested: `[1, 2, 4, 8, 16]`
- Dataset templates: `[{'name': 'small', 'start_n_samples': 50000, 'n_features': 40}, {'name': 'medium', 'start_n_samples': 140000, 'n_features': 80}, {'name': 'large', 'start_n_samples': 320000, 'n_features': 120}]`

## Overall ranking (lower is faster)
| model | median_total_s | mean_total_s | geo_mean_total_s | mean_peak_rss_mb | mean_r2 | max_r2_spread_for_matched_scenario |
| --- | --- | --- | --- | --- | --- | --- |
| sklearn_hgb_fixed | 2.77495 | 2.69562 | 2.31441 | 372.32 | 0.603328 | 0.0026101 |
| lightgbm_hist | 3.13349 | 3.20124 | 2.72517 | 368.359 | 0.603228 | 0.0026101 |
| xgboost_hist | 4.07772 | 3.89769 | 3.36745 | 380.82 | 0.603871 | 0.0026101 |
| sklearn_hgb | 4.11981 | 4.65768 | 3.78138 | 379.613 | 0.603328 | 0.0026101 |


## Single-thread behavior
| dataset_name | model | n_samples | n_features | fit_seconds | predict_seconds | total_seconds | peak_rss_mb | r2 | fitted_trees | expected_trees | total_nodes | avg_nodes_per_tree |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| large | sklearn_hgb | 80000 | 120 | 5.80408 | 0.0724387 | 5.88176 | 418.496 | 0.490287 | 48 | 48 | 12144 | 253 |
| large | sklearn_hgb_fixed | 80000 | 120 | 5.89654 | 0.0721736 | 5.97295 | 418 | 0.490287 | 48 | 48 | 12144 | 253 |
| large | lightgbm_hist | 80000 | 120 | 6.06889 | 0.0748752 | 6.14554 | 374.094 | 0.491423 | 48 | 48 | 12144 | 253 |
| large | xgboost_hist | 80000 | 120 | 8.06121 | 0.0248432 | 8.08962 | 420.516 | 0.491074 | 48 | 48 | 12144 | 253 |
| medium | sklearn_hgb | 140000 | 80 | 5.35695 | 0.113102 | 5.47292 | 420.34 | 0.568235 | 48 | 48 | 12144 | 253 |
| medium | sklearn_hgb_fixed | 140000 | 80 | 5.40238 | 0.11875 | 5.52867 | 420.395 | 0.568235 | 48 | 48 | 12144 | 253 |
| medium | lightgbm_hist | 140000 | 80 | 5.68987 | 0.127486 | 5.82039 | 409.754 | 0.56851 | 48 | 48 | 12144 | 253 |
| medium | xgboost_hist | 140000 | 80 | 6.66734 | 0.0400133 | 6.71438 | 395.574 | 0.568178 | 48 | 48 | 12144 | 253 |
| small | lightgbm_hist | 50000 | 40 | 1.50059 | 0.0455586 | 1.55364 | 248.375 | 0.749752 | 48 | 48 | 12144 | 253 |
| small | sklearn_hgb | 50000 | 40 | 1.64966 | 0.03659 | 1.68992 | 257.227 | 0.751461 | 48 | 48 | 12144 | 253 |
| small | sklearn_hgb_fixed | 50000 | 40 | 1.66552 | 0.036707 | 1.7101 | 256.801 | 0.751461 | 48 | 48 | 12144 | 253 |
| small | xgboost_hist | 50000 | 40 | 2.11793 | 0.0140872 | 2.13843 | 293.105 | 0.752362 | 48 | 48 | 12144 | 253 |


## Multi-thread scalability
| dataset_name | model | max_threads | fit_s_1_thread | fit_s_max_threads | speedup_vs_1_thread | parallel_efficiency |
| --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 16 | 6.06889 | 4.71 | 1.28851 | 0.080532 |
| medium | lightgbm_hist | 16 | 5.68987 | 4.87636 | 1.16683 | 0.0729268 |
| small | lightgbm_hist | 16 | 1.50059 | 2.68297 | 0.559302 | 0.0349564 |
| large | sklearn_hgb | 16 | 5.80408 | 9.45501 | 0.613863 | 0.0383664 |
| medium | sklearn_hgb | 16 | 5.35695 | 9.30707 | 0.575579 | 0.0359737 |
| small | sklearn_hgb | 16 | 1.64966 | 7.06018 | 0.233656 | 0.0146035 |
| large | sklearn_hgb_fixed | 16 | 5.89654 | 2.92245 | 2.01767 | 0.126104 |
| medium | sklearn_hgb_fixed | 16 | 5.40238 | 2.69732 | 2.00287 | 0.12518 |
| small | sklearn_hgb_fixed | 16 | 1.66552 | 1.00903 | 1.65063 | 0.103164 |
| large | xgboost_hist | 16 | 8.06121 | 4.96987 | 1.62202 | 0.101376 |
| medium | xgboost_hist | 16 | 6.66734 | 4.20084 | 1.58714 | 0.0991964 |
| small | xgboost_hist | 16 | 2.11793 | 1.49972 | 1.41221 | 0.0882632 |


## Memory growth trend (thread=1)
| model | smallest_samples | largest_samples | peak_mb_smallest | peak_mb_largest | approx_mb_per_1k_samples |
| --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 50000 | 140000 | 248.375 | 409.754 | 1.7931 |
| sklearn_hgb | 50000 | 140000 | 257.227 | 420.34 | 1.81237 |
| sklearn_hgb_fixed | 50000 | 140000 | 256.801 | 420.395 | 1.81771 |
| xgboost_hist | 50000 | 140000 | 293.105 | 395.574 | 1.13854 |


## Initial conclusion
- Best median runtime model: `sklearn_hgb_fixed`
- Least-performing median runtime model: `sklearn_hgb`
- All scenarios report explicit `r2_spread_for_scenario` to verify score parity while keeping matched hyperparameter values.
