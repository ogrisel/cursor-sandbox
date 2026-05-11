# Histogram GBDT Regressor Benchmark Report

## Experiment controls
- Timeout budget per individual run: `10.0 s`
- Adaptive reduction factor after timeout: `0.6`
- Threads tested: `[1, 2, 4, 8, 16]`
- Dataset templates: `[{'name': 'small', 'start_n_samples': 50000, 'n_features': 40}, {'name': 'medium', 'start_n_samples': 140000, 'n_features': 80}, {'name': 'large', 'start_n_samples': 320000, 'n_features': 120}]`

## Overall ranking (lower is faster)
| model | median_total_s | mean_total_s | geo_mean_total_s | mean_peak_rss_mb | mean_r2 | max_r2_spread_for_matched_scenario |
| --- | --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 2.44654 | 2.36239 | 1.92402 | 354.021 | 0.602111 | 0.00381969 |
| xgboost_hist | 2.66846 | 2.75674 | 2.23649 | 370.001 | 0.604071 | 0.00381969 |
| sklearn_hgb_fixed | 3.50163 | 3.04275 | 2.62972 | 358.667 | 0.602247 | 0.00381969 |
| sklearn_hgb | 3.56742 | 3.11503 | 2.68513 | 358.976 | 0.602247 | 0.00381969 |


## Single-thread behavior
| dataset_name | model | n_samples | n_features | fit_seconds | predict_seconds | total_seconds | peak_rss_mb | r2 | fitted_trees | expected_trees | total_nodes | avg_nodes_per_tree |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| large | sklearn_hgb_fixed | 69120 | 120 | 4.51126 | 0.0557916 | 4.57248 | 391.129 | 0.487854 | 48 | 48 | 12144 | 253 |
| large | sklearn_hgb | 69120 | 120 | 4.99091 | 0.0587639 | 5.05543 | 391.059 | 0.487854 | 48 | 48 | 12144 | 253 |
| large | lightgbm_hist | 69120 | 120 | 5.48138 | 0.0603435 | 5.54428 | 351.719 | 0.488072 | 48 | 48 | 12144 | 253 |
| large | xgboost_hist | 69120 | 120 | 7.39329 | 0.0219534 | 7.41959 | 402.59 | 0.491673 | 48 | 48 | 12144 | 253 |
| medium | sklearn_hgb | 140000 | 80 | 4.369 | 0.0920471 | 4.47127 | 412.328 | 0.568121 | 48 | 48 | 12144 | 253 |
| medium | sklearn_hgb_fixed | 140000 | 80 | 4.40956 | 0.0926967 | 4.51238 | 411.082 | 0.568121 | 48 | 48 | 12144 | 253 |
| medium | lightgbm_hist | 140000 | 80 | 4.60946 | 0.10844 | 4.72251 | 401.07 | 0.56851 | 48 | 48 | 12144 | 253 |
| medium | xgboost_hist | 140000 | 80 | 5.30337 | 0.0358645 | 5.34317 | 386.848 | 0.568178 | 48 | 48 | 12144 | 253 |
| small | lightgbm_hist | 50000 | 40 | 1.1195 | 0.0386968 | 1.16844 | 239.926 | 0.749752 | 48 | 48 | 12144 | 253 |
| small | sklearn_hgb | 50000 | 40 | 1.16262 | 0.030298 | 1.20004 | 248.605 | 0.750765 | 48 | 48 | 12144 | 253 |
| small | sklearn_hgb_fixed | 50000 | 40 | 1.21961 | 0.0306831 | 1.25657 | 248.797 | 0.750765 | 48 | 48 | 12144 | 253 |
| small | xgboost_hist | 50000 | 40 | 1.6545 | 0.0124882 | 1.66731 | 284.68 | 0.752362 | 48 | 48 | 12144 | 253 |


## Multi-thread scalability
| dataset_name | model | max_threads | fit_s_1_thread | fit_s_max_threads | speedup_vs_1_thread | parallel_efficiency |
| --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 16 | 5.48138 | 3.23293 | 1.69548 | 0.105968 |
| medium | lightgbm_hist | 16 | 4.60946 | 3.76391 | 1.22465 | 0.0765404 |
| small | lightgbm_hist | 16 | 1.1195 | 1.52103 | 0.736016 | 0.046001 |
| large | sklearn_hgb | 16 | 4.99091 | 3.95412 | 1.2622 | 0.0788878 |
| medium | sklearn_hgb | 16 | 4.369 | 3.53673 | 1.23532 | 0.0772076 |
| small | sklearn_hgb | 16 | 1.16262 | 1.18995 | 0.977034 | 0.0610646 |
| large | sklearn_hgb_fixed | 16 | 4.51126 | 3.81071 | 1.18384 | 0.0739898 |
| medium | sklearn_hgb_fixed | 16 | 4.40956 | 3.86243 | 1.14165 | 0.0713533 |
| small | sklearn_hgb_fixed | 16 | 1.21961 | 1.14428 | 1.06583 | 0.0666143 |
| large | xgboost_hist | 16 | 7.39329 | 3.05131 | 2.42299 | 0.151437 |
| medium | xgboost_hist | 16 | 5.30337 | 2.64543 | 2.00473 | 0.125296 |
| small | xgboost_hist | 16 | 1.6545 | 0.866252 | 1.90995 | 0.119372 |


## Memory growth trend (thread=1)
| model | smallest_samples | largest_samples | peak_mb_smallest | peak_mb_largest | approx_mb_per_1k_samples |
| --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 50000 | 140000 | 239.926 | 401.07 | 1.79049 |
| sklearn_hgb | 50000 | 140000 | 248.605 | 412.328 | 1.81914 |
| sklearn_hgb_fixed | 50000 | 140000 | 248.797 | 411.082 | 1.80317 |
| xgboost_hist | 50000 | 140000 | 284.68 | 386.848 | 1.1352 |


## Initial conclusion
- Best median runtime model: `lightgbm_hist`
- Least-performing median runtime model: `sklearn_hgb`
- All scenarios report explicit `r2_spread_for_scenario` to verify score parity while keeping matched hyperparameter values.
