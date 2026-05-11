# Histogram GBDT Regressor Benchmark Report

## Experiment controls
- Timeout budget per individual run: `12.0 s`
- Adaptive reduction factor after timeout: `0.5`
- Threads tested: `[1, 2, 4, 8, 16]`
- Dataset templates: `[{'name': 'small', 'start_n_samples': 50000, 'n_features': 40}, {'name': 'medium', 'start_n_samples': 140000, 'n_features': 80}, {'name': 'large', 'start_n_samples': 320000, 'n_features': 120}]`

## Overall ranking (lower is faster)
| model | median_total_s | mean_total_s | geo_mean_total_s | mean_peak_rss_mb | mean_r2 | max_r2_spread_for_matched_scenario |
| --- | --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 2.36422 | 2.68984 | 2.26894 | 276.569 | 0.608506 | 0.00309473 |
| sklearn_hgb_fixed | 3.68718 | 3.61141 | 3.21167 | 295.61 | 0.607953 | 0.00309473 |
| sklearn_hgb | 3.96472 | 3.76018 | 3.40865 | 296.466 | 0.607953 | 0.00309473 |
| xgboost_hist | 5.43681 | 4.96072 | 4.4115 | 365.172 | 0.608242 | 0.00309473 |


## Single-thread behavior
| dataset_name | model | n_samples | n_features | fit_seconds | predict_seconds | total_seconds | peak_rss_mb | r2 | fitted_trees | expected_trees | total_nodes | avg_nodes_per_tree |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 40000 | 120 | 5.1992 | 0.0451578 | 5.24613 | 262.945 | 0.507257 | 48 | 48 | 12144 | 253 |
| large | sklearn_hgb | 40000 | 120 | 6.41499 | 0.128472 | 6.54795 | 299.961 | 0.504162 | 48 | 48 | 12144 | 253 |
| large | sklearn_hgb_fixed | 40000 | 120 | 6.54147 | 0.10386 | 6.65521 | 300.34 | 0.504162 | 48 | 48 | 12144 | 253 |
| large | xgboost_hist | 40000 | 120 | 8.77577 | 0.0216849 | 8.80578 | 422.066 | 0.504185 | 48 | 48 | 12144 | 253 |
| medium | lightgbm_hist | 140000 | 80 | 6.62576 | 0.15263 | 6.78505 | 362.934 | 0.56851 | 48 | 48 | 12144 | 253 |
| medium | sklearn_hgb | 140000 | 80 | 7.27094 | 0.300935 | 7.57639 | 374.188 | 0.568235 | 48 | 48 | 12144 | 253 |
| medium | sklearn_hgb_fixed | 140000 | 80 | 7.46591 | 0.327954 | 7.80355 | 374.113 | 0.568235 | 48 | 48 | 12144 | 253 |
| medium | xgboost_hist | 140000 | 80 | 9.04595 | 0.0655475 | 9.11169 | 412.914 | 0.568178 | 48 | 48 | 12144 | 253 |
| small | lightgbm_hist | 50000 | 40 | 1.86703 | 0.054824 | 1.92587 | 198.375 | 0.749752 | 48 | 48 | 12144 | 253 |
| small | sklearn_hgb | 50000 | 40 | 2.3882 | 0.0959668 | 2.4913 | 210.785 | 0.751461 | 48 | 48 | 12144 | 253 |
| small | sklearn_hgb_fixed | 50000 | 40 | 2.39185 | 0.0986757 | 2.49762 | 211.402 | 0.751461 | 48 | 48 | 12144 | 253 |
| small | xgboost_hist | 50000 | 40 | 3.01496 | 0.0212635 | 3.04003 | 251.352 | 0.752362 | 48 | 48 | 12144 | 253 |


## Multi-thread scalability
| dataset_name | model | max_threads | fit_s_1_thread | fit_s_max_threads | speedup_vs_1_thread | parallel_efficiency |
| --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 16 | 5.1992 | 2.33808 | 2.22371 | 0.138982 |
| medium | lightgbm_hist | 16 | 6.62576 | 3.01534 | 2.19735 | 0.137334 |
| small | lightgbm_hist | 16 | 1.86703 | 1.02793 | 1.81631 | 0.113519 |
| large | sklearn_hgb | 16 | 6.41499 | 4.17252 | 1.53744 | 0.0960898 |
| medium | sklearn_hgb | 16 | 7.27094 | 4.27832 | 1.69948 | 0.106218 |
| small | sklearn_hgb | 16 | 2.3882 | 2.18997 | 1.09052 | 0.0681574 |
| large | sklearn_hgb_fixed | 16 | 6.54147 | 3.63412 | 1.80001 | 0.112501 |
| medium | sklearn_hgb_fixed | 16 | 7.46591 | 3.70564 | 2.01475 | 0.125922 |
| small | sklearn_hgb_fixed | 16 | 2.39185 | 1.56357 | 1.52974 | 0.0956085 |
| large | xgboost_hist | 16 | 8.77577 | 5.61747 | 1.56223 | 0.0976392 |
| medium | xgboost_hist | 16 | 9.04595 | 5.35435 | 1.68946 | 0.105591 |
| small | xgboost_hist | 16 | 3.01496 | 2.03434 | 1.48203 | 0.0926269 |


## Memory growth trend (thread=1)
| model | smallest_samples | largest_samples | peak_mb_smallest | peak_mb_largest | approx_mb_per_1k_samples |
| --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 40000 | 140000 | 262.945 | 362.934 | 0.999883 |
| sklearn_hgb | 40000 | 140000 | 299.961 | 374.188 | 0.742266 |
| sklearn_hgb_fixed | 40000 | 140000 | 300.34 | 374.113 | 0.737734 |
| xgboost_hist | 40000 | 140000 | 422.066 | 412.914 | -0.0915234 |


## Initial conclusion
- Best median runtime model: `lightgbm_hist`
- Least-performing median runtime model: `xgboost_hist`
- All scenarios report explicit `r2_spread_for_scenario` to verify score parity while keeping matched hyperparameter values.
