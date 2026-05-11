# Histogram GBDT Regressor Benchmark Report

## Experiment controls
- Timeout budget per individual run: `12.0 s`
- Adaptive reduction factor after timeout: `0.5`
- Threads tested: `[1, 2, 4, 8, 16]`
- Dataset templates: `[{'name': 'small', 'start_n_samples': 50000, 'n_features': 40}, {'name': 'medium', 'start_n_samples': 140000, 'n_features': 80}, {'name': 'large', 'start_n_samples': 320000, 'n_features': 120}]`

## Overall ranking (lower is faster)
| model | median_total_s | mean_total_s | geo_mean_total_s | mean_peak_rss_mb | mean_r2 | max_r2_spread_for_matched_scenario |
| --- | --- | --- | --- | --- | --- | --- |
| sklearn_hgb_fixed | 1.85487 | 2.23933 | 1.82894 | 362.45 | 0.603328 | 0.0026101 |
| xgboost_hist | 2.3117 | 2.84648 | 2.29713 | 371.533 | 0.603871 | 0.0026101 |
| lightgbm_hist | 2.83467 | 2.53687 | 2.09302 | 358.589 | 0.603228 | 0.0026101 |
| sklearn_hgb | 3.5465 | 3.9065 | 3.2002 | 369.872 | 0.603328 | 0.0026101 |


## Single-thread behavior
| dataset_name | model | n_samples | n_features | fit_seconds | predict_seconds | total_seconds | peak_rss_mb | r2 | fitted_trees | expected_trees | total_nodes | avg_nodes_per_tree |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 80000 | 120 | 5.3734 | 0.058975 | 5.43352 | 364.527 | 0.491423 | 48 | 48 | 12144 | 253 |
| large | sklearn_hgb | 80000 | 120 | 5.59087 | 0.0533358 | 5.6531 | 408.508 | 0.490287 | 48 | 48 | 12144 | 253 |
| large | sklearn_hgb_fixed | 80000 | 120 | 5.6837 | 0.0532188 | 5.74528 | 408.594 | 0.490287 | 48 | 48 | 12144 | 253 |
| large | xgboost_hist | 80000 | 120 | 7.40006 | 0.0217709 | 7.42627 | 410.438 | 0.491074 | 48 | 48 | 12144 | 253 |
| medium | lightgbm_hist | 140000 | 80 | 5.20613 | 0.0992681 | 5.30724 | 400.227 | 0.56851 | 48 | 48 | 12144 | 253 |
| medium | sklearn_hgb_fixed | 140000 | 80 | 5.40072 | 0.0862001 | 5.49329 | 410.484 | 0.568235 | 48 | 48 | 12144 | 253 |
| medium | sklearn_hgb | 140000 | 80 | 5.42559 | 0.0830683 | 5.51692 | 410.492 | 0.568235 | 48 | 48 | 12144 | 253 |
| medium | xgboost_hist | 140000 | 80 | 6.45764 | 0.0347379 | 6.5008 | 385.18 | 0.568178 | 48 | 48 | 12144 | 253 |
| small | lightgbm_hist | 50000 | 40 | 1.30788 | 0.0347138 | 1.35056 | 238.84 | 0.749752 | 48 | 48 | 12144 | 253 |
| small | sklearn_hgb_fixed | 50000 | 40 | 1.62532 | 0.0262087 | 1.65252 | 247.148 | 0.751461 | 48 | 48 | 12144 | 253 |
| small | sklearn_hgb | 50000 | 40 | 1.65148 | 0.0264898 | 1.67889 | 247.137 | 0.751461 | 48 | 48 | 12144 | 253 |
| small | xgboost_hist | 50000 | 40 | 1.9191 | 0.0121903 | 1.93974 | 283.074 | 0.752362 | 48 | 48 | 12144 | 253 |


## Multi-thread scalability
| dataset_name | model | max_threads | fit_s_1_thread | fit_s_max_threads | speedup_vs_1_thread | parallel_efficiency |
| --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 16 | 5.3734 | 3.43889 | 1.56254 | 0.0976588 |
| medium | lightgbm_hist | 16 | 5.20613 | 3.41899 | 1.52271 | 0.0951693 |
| small | lightgbm_hist | 16 | 1.30788 | 1.91384 | 0.68338 | 0.0427113 |
| large | sklearn_hgb | 16 | 5.59087 | 7.13318 | 0.783784 | 0.0489865 |
| medium | sklearn_hgb | 16 | 5.42559 | 6.96333 | 0.779165 | 0.0486978 |
| small | sklearn_hgb | 16 | 1.65148 | 5.44674 | 0.303205 | 0.0189503 |
| large | sklearn_hgb_fixed | 16 | 5.6837 | 1.89626 | 2.99732 | 0.187332 |
| medium | sklearn_hgb_fixed | 16 | 5.40072 | 1.7893 | 3.01834 | 0.188646 |
| small | sklearn_hgb_fixed | 16 | 1.62532 | 0.733293 | 2.21647 | 0.138529 |
| large | xgboost_hist | 16 | 7.40006 | 2.78231 | 2.65968 | 0.16623 |
| medium | xgboost_hist | 16 | 6.45764 | 2.2976 | 2.81061 | 0.175663 |
| small | xgboost_hist | 16 | 1.9191 | 0.841437 | 2.28074 | 0.142546 |


## Memory growth trend (thread=1)
| model | smallest_samples | largest_samples | peak_mb_smallest | peak_mb_largest | approx_mb_per_1k_samples |
| --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 50000 | 140000 | 238.84 | 400.227 | 1.79319 |
| sklearn_hgb | 50000 | 140000 | 247.137 | 410.492 | 1.81506 |
| sklearn_hgb_fixed | 50000 | 140000 | 247.148 | 410.484 | 1.81484 |
| xgboost_hist | 50000 | 140000 | 283.074 | 385.18 | 1.13451 |


## Initial conclusion
- Best median runtime model: `sklearn_hgb_fixed`
- Least-performing median runtime model: `sklearn_hgb`
- All scenarios report explicit `r2_spread_for_scenario` to verify score parity while keeping matched hyperparameter values.
