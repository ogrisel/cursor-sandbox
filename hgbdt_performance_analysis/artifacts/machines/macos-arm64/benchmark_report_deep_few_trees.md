# Histogram GBDT Regressor Benchmark Report

## Experiment controls
- Timeout budget per individual run: `12.0 s`
- Adaptive reduction factor after timeout: `0.5`
- Threads tested: `[1, 2, 3, 6, 12]`
- Dataset templates: `[{'name': 'small', 'start_n_samples': 50000, 'n_features': 40}, {'name': 'medium', 'start_n_samples': 140000, 'n_features': 80}, {'name': 'large', 'start_n_samples': 320000, 'n_features': 120}]`

## Overall ranking (lower is faster)
| model | median_total_s | mean_total_s | geo_mean_total_s | mean_peak_rss_mb | mean_r2 | max_r2_spread_for_matched_scenario |
| --- | --- | --- | --- | --- | --- | --- |
| sklearn_hgb_fixed | 2.27441 | 2.84993 | 2.3357 | 520.757 | 0.602739 | 0.0026101 |
| sklearn_hgb | 2.74038 | 3.32579 | 2.85853 | 488.208 | 0.602739 | 0.0026101 |
| lightgbm_hist | 2.81133 | 3.01951 | 2.54935 | 477.557 | 0.602758 | 0.0026101 |
| xgboost_hist | 2.98296 | 3.2306 | 2.84162 | 489.291 | 0.60321 | 0.0026101 |


## Single-thread behavior
| dataset_name | model | n_samples | n_features | fit_seconds | predict_seconds | total_seconds | peak_rss_mb | r2 | fitted_trees | expected_trees | total_nodes | avg_nodes_per_tree |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 160000 | 120 | 6.74268 | 0.144504 | 6.90072 | 642.109 | 0.490012 | 48 | 48 | 12144 | 253 |
| large | xgboost_hist | 160000 | 120 | 7.52236 | 0.0415728 | 7.5999 | 631.172 | 0.489088 | 48 | 48 | 12144 | 253 |
| large | sklearn_hgb_fixed | 160000 | 120 | 7.47811 | 0.111311 | 7.65185 | 723.922 | 0.488521 | 48 | 48 | 12144 | 253 |
| large | sklearn_hgb | 160000 | 120 | 7.64075 | 0.112014 | 7.77104 | 718.812 | 0.488521 | 48 | 48 | 12144 | 253 |
| medium | lightgbm_hist | 140000 | 80 | 3.8286 | 0.115302 | 3.99802 | 564.141 | 0.56851 | 48 | 48 | 12144 | 253 |
| medium | sklearn_hgb | 140000 | 80 | 4.30719 | 0.0932306 | 4.43713 | 576.672 | 0.568235 | 48 | 48 | 12144 | 253 |
| medium | xgboost_hist | 140000 | 80 | 4.45374 | 0.0350786 | 4.49298 | 569.766 | 0.568178 | 48 | 48 | 12144 | 253 |
| medium | sklearn_hgb_fixed | 140000 | 80 | 4.43531 | 0.0888418 | 4.53698 | 580.359 | 0.568235 | 48 | 48 | 12144 | 253 |
| small | lightgbm_hist | 50000 | 40 | 0.916127 | 0.0443528 | 0.976666 | 262.578 | 0.749752 | 48 | 48 | 12144 | 253 |
| small | sklearn_hgb | 50000 | 40 | 1.26099 | 0.033643 | 1.29874 | 298.844 | 0.751461 | 48 | 48 | 12144 | 253 |
| small | sklearn_hgb_fixed | 50000 | 40 | 1.25093 | 0.0486596 | 1.30953 | 294.938 | 0.751461 | 48 | 48 | 12144 | 253 |
| small | xgboost_hist | 50000 | 40 | 1.4339 | 0.0128157 | 1.45133 | 277.969 | 0.752362 | 48 | 48 | 12144 | 253 |


## Multi-thread scalability
| dataset_name | model | max_threads | fit_s_1_thread | fit_s_max_threads | speedup_vs_1_thread | parallel_efficiency |
| --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 12 | 6.74268 | 4.41806 | 1.52617 | 0.12718 |
| medium | lightgbm_hist | 12 | 3.8286 | 2.59257 | 1.47676 | 0.123063 |
| small | lightgbm_hist | 12 | 0.916127 | 1.31054 | 0.699043 | 0.0582536 |
| large | sklearn_hgb | 12 | 7.64075 | 5.40685 | 1.41316 | 0.117763 |
| medium | sklearn_hgb | 12 | 4.30719 | 3.86161 | 1.11539 | 0.0929488 |
| small | sklearn_hgb | 12 | 1.26099 | 2.63146 | 0.479199 | 0.0399333 |
| large | sklearn_hgb_fixed | 12 | 7.47811 | 3.53617 | 2.11475 | 0.176229 |
| medium | sklearn_hgb_fixed | 12 | 4.43531 | 1.9835 | 2.2361 | 0.186341 |
| small | sklearn_hgb_fixed | 12 | 1.25093 | 1.10972 | 1.12725 | 0.0939376 |
| large | xgboost_hist | 12 | 7.52236 | 3.96261 | 1.89834 | 0.158195 |
| medium | xgboost_hist | 12 | 4.45374 | 2.90203 | 1.5347 | 0.127892 |
| small | xgboost_hist | 12 | 1.4339 | 1.24163 | 1.15485 | 0.0962377 |


## Memory growth trend (thread=1)
| model | smallest_samples | largest_samples | peak_mb_smallest | peak_mb_largest | approx_mb_per_1k_samples |
| --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 50000 | 160000 | 262.578 | 642.109 | 3.45028 |
| sklearn_hgb | 50000 | 160000 | 298.844 | 718.812 | 3.8179 |
| sklearn_hgb_fixed | 50000 | 160000 | 294.938 | 723.922 | 3.89986 |
| xgboost_hist | 50000 | 160000 | 277.969 | 631.172 | 3.21094 |


## Initial conclusion
- Best median runtime model: `sklearn_hgb_fixed`
- Least-performing median runtime model: `xgboost_hist`
- All scenarios report explicit `r2_spread_for_scenario` to verify score parity while keeping matched hyperparameter values.
