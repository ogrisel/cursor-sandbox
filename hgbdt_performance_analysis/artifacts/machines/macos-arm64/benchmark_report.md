# Histogram GBDT Regressor Benchmark Report

## Experiment controls
- Timeout budget per individual run: `12.0 s`
- Adaptive reduction factor after timeout: `0.5`
- Threads tested: `[1, 2, 3, 6, 12]`
- Dataset templates: `[{'name': 'small', 'start_n_samples': 50000, 'n_features': 40}, {'name': 'medium', 'start_n_samples': 140000, 'n_features': 80}, {'name': 'large', 'start_n_samples': 320000, 'n_features': 120}]`

## Overall ranking (lower is faster)
| model | median_total_s | mean_total_s | geo_mean_total_s | mean_peak_rss_mb | mean_r2 | max_r2_spread_for_matched_scenario |
| --- | --- | --- | --- | --- | --- | --- |
| sklearn_hgb_fixed | 2.73559 | 3.08405 | 2.80609 | 340.876 | 0.777055 | 0.0132866 |
| lightgbm_hist | 3.55344 | 3.61239 | 3.3123 | 378.377 | 0.785667 | 0.0132866 |
| xgboost_hist | 3.59899 | 4.16546 | 3.80143 | 387.979 | 0.78644 | 0.0132866 |
| sklearn_hgb | 4.42875 | 4.42347 | 3.96004 | 334.605 | 0.777055 | 0.0132866 |


## Single-thread behavior
| dataset_name | model | n_samples | n_features | fit_seconds | predict_seconds | total_seconds | peak_rss_mb | r2 | fitted_trees | expected_trees | total_nodes | avg_nodes_per_tree |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 80000 | 120 | 6.8822 | 0.163181 | 7.12048 | 525.859 | 0.670334 | 220 | 220 | 13420 | 61 |
| large | sklearn_hgb | 80000 | 120 | 6.8463 | 0.42193 | 7.31695 | 470.453 | 0.658445 | 220 | 220 | 13420 | 61 |
| large | sklearn_hgb_fixed | 80000 | 120 | 7.31555 | 0.259835 | 7.58654 | 470.516 | 0.658445 | 220 | 220 | 13420 | 61 |
| large | xgboost_hist | 80000 | 120 | 8.33898 | 0.0336081 | 8.40337 | 546.344 | 0.671732 | 220 | 220 | 13420 | 61 |
| medium | lightgbm_hist | 70000 | 80 | 3.83284 | 0.127167 | 4.00237 | 379.703 | 0.79359 | 220 | 220 | 13420 | 61 |
| medium | sklearn_hgb_fixed | 70000 | 80 | 4.35686 | 0.157836 | 4.55866 | 325.094 | 0.785099 | 220 | 220 | 13420 | 61 |
| medium | xgboost_hist | 70000 | 80 | 4.64477 | 0.0292264 | 4.67629 | 379.531 | 0.793248 | 220 | 220 | 13420 | 61 |
| medium | sklearn_hgb | 70000 | 80 | 4.65608 | 0.126394 | 4.83418 | 328.672 | 0.785099 | 220 | 220 | 13420 | 61 |
| small | lightgbm_hist | 50000 | 40 | 1.5578 | 0.0929706 | 1.66883 | 256.562 | 0.893078 | 220 | 220 | 13420 | 61 |
| small | sklearn_hgb_fixed | 50000 | 40 | 2.61381 | 0.0884518 | 2.73559 | 233.781 | 0.88762 | 220 | 220 | 13420 | 61 |
| small | sklearn_hgb | 50000 | 40 | 2.65641 | 0.146687 | 2.82773 | 233.094 | 0.88762 | 220 | 220 | 13420 | 61 |
| small | xgboost_hist | 50000 | 40 | 2.83902 | 0.0594711 | 2.9048 | 245.688 | 0.894341 | 220 | 220 | 13420 | 61 |


## Multi-thread scalability
| dataset_name | model | max_threads | fit_s_1_thread | fit_s_max_threads | speedup_vs_1_thread | parallel_efficiency |
| --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 12 | 6.8822 | 5.56456 | 1.23679 | 0.103066 |
| medium | lightgbm_hist | 12 | 3.83284 | 4.03794 | 0.949206 | 0.0791005 |
| small | lightgbm_hist | 12 | 1.5578 | 3.46026 | 0.450198 | 0.0375165 |
| large | sklearn_hgb | 12 | 6.8463 | 6.13493 | 1.11595 | 0.0929962 |
| medium | sklearn_hgb | 12 | 4.65608 | 4.28232 | 1.08728 | 0.0906067 |
| small | sklearn_hgb | 12 | 2.65641 | 3.09392 | 0.858589 | 0.0715491 |
| large | sklearn_hgb_fixed | 12 | 7.31555 | 2.82469 | 2.58986 | 0.215821 |
| medium | sklearn_hgb_fixed | 12 | 4.35686 | 3.04004 | 1.43316 | 0.11943 |
| small | sklearn_hgb_fixed | 12 | 2.61381 | 2.02458 | 1.29104 | 0.107587 |
| large | xgboost_hist | 12 | 8.33898 | 6.72742 | 1.23955 | 0.103296 |
| medium | xgboost_hist | 12 | 4.64477 | 4.04191 | 1.14915 | 0.0957626 |
| small | xgboost_hist | 12 | 2.83902 | 3.557 | 0.798149 | 0.0665124 |


## Memory growth trend (thread=1)
| model | smallest_samples | largest_samples | peak_mb_smallest | peak_mb_largest | approx_mb_per_1k_samples |
| --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 50000 | 80000 | 256.562 | 525.859 | 8.97656 |
| sklearn_hgb | 50000 | 80000 | 233.094 | 470.453 | 7.91198 |
| sklearn_hgb_fixed | 50000 | 80000 | 233.781 | 470.516 | 7.89115 |
| xgboost_hist | 50000 | 80000 | 245.688 | 546.344 | 10.0219 |


## Initial conclusion
- Best median runtime model: `sklearn_hgb_fixed`
- Least-performing median runtime model: `sklearn_hgb`
- All scenarios report explicit `r2_spread_for_scenario` to verify score parity while keeping matched hyperparameter values.
