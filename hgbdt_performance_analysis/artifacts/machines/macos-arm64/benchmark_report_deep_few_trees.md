# Histogram GBDT Regressor Benchmark Report

## Experiment controls
- Timeout budget per individual run: `12.0 s`
- Adaptive reduction factor after timeout: `0.5`
- Threads tested: `[1, 2, 3, 6, 12]`
- Dataset templates: `[{'name': 'small', 'start_n_samples': 50000, 'n_features': 40}, {'name': 'medium', 'start_n_samples': 140000, 'n_features': 80}, {'name': 'large', 'start_n_samples': 320000, 'n_features': 120}]`

## Overall ranking (lower is faster)
| model | median_total_s | mean_total_s | geo_mean_total_s | mean_peak_rss_mb | mean_r2 | max_r2_spread_for_matched_scenario |
| --- | --- | --- | --- | --- | --- | --- |
| sklearn_hgb_fixed | 2.05225 | 2.70042 | 2.10455 | 522.62 | 0.602739 | 0.0026101 |
| lightgbm_hist | 2.79577 | 3.0368 | 2.52458 | 473.084 | 0.602758 | 0.0026101 |
| xgboost_hist | 2.8675 | 3.15654 | 2.69615 | 484.426 | 0.60321 | 0.0026101 |
| sklearn_hgb | 2.88762 | 3.31723 | 2.73298 | 488.578 | 0.602739 | 0.0026101 |


## Single-thread behavior
| dataset_name | model | n_samples | n_features | fit_seconds | predict_seconds | total_seconds | peak_rss_mb | r2 | fitted_trees | expected_trees | total_nodes | avg_nodes_per_tree |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 160000 | 120 | 6.82629 | 0.150117 | 6.98039 | 596.781 | 0.490012 | 48 | 48 | 12144 | 253 |
| large | sklearn_hgb_fixed | 160000 | 120 | 7.52049 | 0.111396 | 7.65103 | 726.859 | 0.488521 | 48 | 48 | 12144 | 253 |
| large | xgboost_hist | 160000 | 120 | 7.62314 | 0.0425829 | 7.68944 | 658.078 | 0.489088 | 48 | 48 | 12144 | 253 |
| large | sklearn_hgb | 160000 | 120 | 7.53978 | 0.115227 | 7.72073 | 725.469 | 0.488521 | 48 | 48 | 12144 | 253 |
| medium | lightgbm_hist | 140000 | 80 | 3.98004 | 0.117328 | 4.15447 | 562.359 | 0.56851 | 48 | 48 | 12144 | 253 |
| medium | sklearn_hgb_fixed | 140000 | 80 | 4.27206 | 0.0886042 | 4.44478 | 579.781 | 0.568235 | 48 | 48 | 12144 | 253 |
| medium | sklearn_hgb | 140000 | 80 | 4.35726 | 0.0877443 | 4.5207 | 578.438 | 0.568235 | 48 | 48 | 12144 | 253 |
| medium | xgboost_hist | 140000 | 80 | 4.45558 | 0.0435859 | 4.57405 | 581.469 | 0.568178 | 48 | 48 | 12144 | 253 |
| small | lightgbm_hist | 50000 | 40 | 0.909141 | 0.0405806 | 0.951166 | 258.406 | 0.749752 | 48 | 48 | 12144 | 253 |
| small | sklearn_hgb | 50000 | 40 | 1.18348 | 0.0304224 | 1.23236 | 299.203 | 0.751461 | 48 | 48 | 12144 | 253 |
| small | sklearn_hgb_fixed | 50000 | 40 | 1.21143 | 0.0307785 | 1.26418 | 294.984 | 0.751461 | 48 | 48 | 12144 | 253 |
| small | xgboost_hist | 50000 | 40 | 1.38894 | 0.0119944 | 1.44861 | 265.438 | 0.752362 | 48 | 48 | 12144 | 253 |


## Multi-thread scalability
| dataset_name | model | max_threads | fit_s_1_thread | fit_s_max_threads | speedup_vs_1_thread | parallel_efficiency |
| --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 12 | 6.82629 | 5.08667 | 1.34199 | 0.111833 |
| medium | lightgbm_hist | 12 | 3.98004 | 2.70098 | 1.47355 | 0.122796 |
| small | lightgbm_hist | 12 | 0.909141 | 1.41146 | 0.644115 | 0.0536763 |
| large | sklearn_hgb | 12 | 7.53978 | 5.7211 | 1.31789 | 0.109824 |
| medium | sklearn_hgb | 12 | 4.35726 | 3.87971 | 1.12309 | 0.0935906 |
| small | sklearn_hgb | 12 | 1.18348 | 2.81549 | 0.420346 | 0.0350289 |
| large | sklearn_hgb_fixed | 12 | 7.52049 | 3.6525 | 2.059 | 0.171583 |
| medium | sklearn_hgb_fixed | 12 | 4.27206 | 1.96453 | 2.1746 | 0.181216 |
| small | sklearn_hgb_fixed | 12 | 1.21143 | 0.623066 | 1.9443 | 0.162025 |
| large | xgboost_hist | 12 | 7.62314 | 3.95891 | 1.92557 | 0.160464 |
| medium | xgboost_hist | 12 | 4.45558 | 2.72628 | 1.63431 | 0.136192 |
| small | xgboost_hist | 12 | 1.38894 | 1.199 | 1.15842 | 0.0965348 |


## Memory growth trend (thread=1)
| model | smallest_samples | largest_samples | peak_mb_smallest | peak_mb_largest | approx_mb_per_1k_samples |
| --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 50000 | 160000 | 258.406 | 596.781 | 3.07614 |
| sklearn_hgb | 50000 | 160000 | 299.203 | 725.469 | 3.87514 |
| sklearn_hgb_fixed | 50000 | 160000 | 294.984 | 726.859 | 3.92614 |
| xgboost_hist | 50000 | 160000 | 265.438 | 658.078 | 3.56946 |


## Initial conclusion
- Best median runtime model: `sklearn_hgb_fixed`
- Least-performing median runtime model: `sklearn_hgb`
- All scenarios report explicit `r2_spread_for_scenario` to verify score parity while keeping matched hyperparameter values.
