# Histogram GBDT Regressor Benchmark Report

## Experiment controls
- Timeout budget per individual run: `8.0 s`
- Adaptive reduction factor after timeout: `0.5`
- Threads tested: `[1, 2, 4]`
- Dataset templates: `[{'name': 'small', 'start_n_samples': 50000, 'n_features': 40}, {'name': 'medium', 'start_n_samples': 140000, 'n_features': 80}, {'name': 'large', 'start_n_samples': 320000, 'n_features': 120}]`

## Overall ranking (lower is faster)
| model | median_total_s | mean_total_s | geo_mean_total_s | mean_peak_rss_mb | mean_r2 | max_r2_spread_for_matched_scenario |
| --- | --- | --- | --- | --- | --- | --- |
| sklearn_hgb | 1.95866 | 2.22825 | 1.93163 | 345.015 | 0.607953 | 0.00309473 |
| sklearn_hgb_fixed | 1.99197 | 2.23725 | 1.94324 | 345.054 | 0.607953 | 0.00309473 |
| lightgbm_hist | 2.10091 | 2.30286 | 1.88733 | 333.953 | 0.608506 | 0.00309473 |
| xgboost_hist | 2.97921 | 3.0659 | 2.65875 | 363.065 | 0.608242 | 0.00309473 |


## Single-thread behavior
| dataset_name | model | n_samples | n_features | fit_seconds | predict_seconds | total_seconds | peak_rss_mb | r2 | fitted_trees | expected_trees | total_nodes | avg_nodes_per_tree |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| large | sklearn_hgb_fixed | 40000 | 120 | 3.42274 | 0.031872 | 3.46001 | 345.102 | 0.504162 | 48 | 48 | 12144 | 253 |
| large | sklearn_hgb | 40000 | 120 | 3.42092 | 0.0321183 | 3.46318 | 345.273 | 0.504162 | 48 | 48 | 12144 | 253 |
| large | lightgbm_hist | 40000 | 120 | 3.95187 | 0.0342305 | 3.99525 | 309.297 | 0.507257 | 48 | 48 | 12144 | 253 |
| large | xgboost_hist | 40000 | 120 | 5.45169 | 0.0121584 | 5.46849 | 379.227 | 0.504185 | 48 | 48 | 12144 | 253 |
| medium | sklearn_hgb_fixed | 140000 | 80 | 4.69051 | 0.0948358 | 4.79246 | 420.164 | 0.568235 | 48 | 48 | 12144 | 253 |
| medium | sklearn_hgb | 140000 | 80 | 4.73715 | 0.0943728 | 4.84035 | 420.332 | 0.568235 | 48 | 48 | 12144 | 253 |
| medium | lightgbm_hist | 140000 | 80 | 5.12474 | 0.115825 | 5.24818 | 410 | 0.56851 | 48 | 48 | 12144 | 253 |
| medium | xgboost_hist | 140000 | 80 | 5.72618 | 0.0384356 | 5.76904 | 395.039 | 0.568178 | 48 | 48 | 12144 | 253 |
| small | sklearn_hgb | 50000 | 40 | 1.39593 | 0.0323585 | 1.43669 | 257.023 | 0.751461 | 48 | 48 | 12144 | 253 |
| small | lightgbm_hist | 50000 | 40 | 1.41511 | 0.0410183 | 1.45778 | 247.949 | 0.749752 | 48 | 48 | 12144 | 253 |
| small | sklearn_hgb_fixed | 50000 | 40 | 1.43439 | 0.0323722 | 1.47476 | 256.922 | 0.751461 | 48 | 48 | 12144 | 253 |
| small | xgboost_hist | 50000 | 40 | 1.87466 | 0.0131785 | 1.89685 | 293.355 | 0.752362 | 48 | 48 | 12144 | 253 |


## Multi-thread scalability
| dataset_name | model | max_threads | fit_s_1_thread | fit_s_max_threads | speedup_vs_1_thread | parallel_efficiency |
| --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 4 | 3.95187 | 1.5665 | 2.52274 | 0.630686 |
| medium | lightgbm_hist | 4 | 5.12474 | 2.0773 | 2.46702 | 0.616754 |
| small | lightgbm_hist | 4 | 1.41511 | 0.610161 | 2.31924 | 0.57981 |
| large | sklearn_hgb | 4 | 3.42092 | 1.71303 | 1.997 | 0.49925 |
| medium | sklearn_hgb | 4 | 4.73715 | 2.18432 | 2.16871 | 0.542177 |
| small | sklearn_hgb | 4 | 1.39593 | 0.834037 | 1.6737 | 0.418425 |
| large | sklearn_hgb_fixed | 4 | 3.42274 | 1.73869 | 1.96857 | 0.492143 |
| medium | sklearn_hgb_fixed | 4 | 4.69051 | 2.23589 | 2.09782 | 0.524456 |
| small | sklearn_hgb_fixed | 4 | 1.43439 | 0.82633 | 1.73586 | 0.433965 |
| large | xgboost_hist | 4 | 5.45169 | 2.96484 | 1.83878 | 0.459695 |
| medium | xgboost_hist | 4 | 5.72618 | 2.86986 | 1.99528 | 0.49882 |
| small | xgboost_hist | 4 | 1.87466 | 1.10054 | 1.70339 | 0.425849 |


## Memory growth trend (thread=1)
| model | smallest_samples | largest_samples | peak_mb_smallest | peak_mb_largest | approx_mb_per_1k_samples |
| --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 40000 | 140000 | 309.297 | 410 | 1.00703 |
| sklearn_hgb | 40000 | 140000 | 345.273 | 420.332 | 0.750586 |
| sklearn_hgb_fixed | 40000 | 140000 | 345.102 | 420.164 | 0.750625 |
| xgboost_hist | 40000 | 140000 | 379.227 | 395.039 | 0.158125 |


## Initial conclusion
- Best median runtime model: `sklearn_hgb`
- Least-performing median runtime model: `xgboost_hist`
- All scenarios report explicit `r2_spread_for_scenario` to verify score parity while keeping matched hyperparameter values.
