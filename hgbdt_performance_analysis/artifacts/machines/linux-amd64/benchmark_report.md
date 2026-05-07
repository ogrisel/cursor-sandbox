# Histogram GBDT Regressor Benchmark Report

## Experiment controls
- Timeout budget per individual run: `8.0 s`
- Adaptive reduction factor after timeout: `0.5`
- Threads tested: `[1, 2, 4]`
- Dataset templates: `[{'name': 'small', 'start_n_samples': 50000, 'n_features': 40}, {'name': 'medium', 'start_n_samples': 140000, 'n_features': 80}, {'name': 'large', 'start_n_samples': 320000, 'n_features': 120}]`

## Overall ranking (lower is faster)
| model | median_total_s | mean_total_s | geo_mean_total_s | mean_peak_rss_mb | mean_r2 | max_r2_spread_for_matched_scenario |
| --- | --- | --- | --- | --- | --- | --- |
| sklearn_hgb | 1.84372 | 2.08712 | 1.96558 | 222.328 | 0.762274 | 0.0223186 |
| sklearn_hgb_fixed | 1.8509 | 2.08327 | 1.95994 | 222.302 | 0.762274 | 0.0223186 |
| lightgbm_hist | 1.97934 | 2.22599 | 2.03298 | 224.433 | 0.776988 | 0.0223186 |
| xgboost_hist | 2.88918 | 3.34312 | 3.08517 | 248.28 | 0.77509 | 0.0223186 |


## Single-thread behavior
| dataset_name | model | n_samples | n_features | fit_seconds | predict_seconds | total_seconds | peak_rss_mb | r2 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| large | sklearn_hgb_fixed | 20000 | 120 | 3.49256 | 0.0595979 | 3.55372 | 224.391 | 0.653232 |
| large | sklearn_hgb | 20000 | 120 | 3.48985 | 0.0603397 | 3.55391 | 224.484 | 0.653232 |
| large | lightgbm_hist | 20000 | 120 | 4.02406 | 0.0617103 | 4.0943 | 217.141 | 0.675551 |
| large | xgboost_hist | 20000 | 120 | 6.05115 | 0.0127623 | 6.066 | 237.016 | 0.672265 |
| medium | sklearn_hgb | 35000 | 80 | 3.08558 | 0.0864967 | 3.17652 | 226.375 | 0.745971 |
| medium | sklearn_hgb_fixed | 35000 | 80 | 3.10541 | 0.0867817 | 3.19731 | 226.535 | 0.745971 |
| medium | lightgbm_hist | 35000 | 80 | 3.61391 | 0.104098 | 3.71865 | 226.953 | 0.762334 |
| medium | xgboost_hist | 35000 | 80 | 4.90757 | 0.0209393 | 4.93456 | 255.949 | 0.758663 |
| small | sklearn_hgb_fixed | 50000 | 40 | 2.02098 | 0.112926 | 2.13467 | 209.418 | 0.88762 |
| small | sklearn_hgb | 50000 | 40 | 2.05602 | 0.112547 | 2.17445 | 209.957 | 0.88762 |
| small | lightgbm_hist | 50000 | 40 | 2.3358 | 0.146053 | 2.48634 | 216.117 | 0.893078 |
| small | xgboost_hist | 50000 | 40 | 2.85599 | 0.0295027 | 2.88918 | 222.863 | 0.894341 |


## Multi-thread scalability
| dataset_name | model | max_threads | fit_s_1_thread | fit_s_max_threads | speedup_vs_1_thread | parallel_efficiency |
| --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 4 | 4.02406 | 1.60085 | 2.5137 | 0.628426 |
| medium | lightgbm_hist | 4 | 3.61391 | 1.47428 | 2.45131 | 0.612828 |
| small | lightgbm_hist | 4 | 2.3358 | 1.05025 | 2.22405 | 0.556013 |
| large | sklearn_hgb | 4 | 3.48985 | 1.81804 | 1.91956 | 0.479891 |
| medium | sklearn_hgb | 4 | 3.08558 | 1.62018 | 1.90446 | 0.476116 |
| small | sklearn_hgb | 4 | 2.05602 | 1.17471 | 1.75024 | 0.43756 |
| large | sklearn_hgb_fixed | 4 | 3.49256 | 1.80878 | 1.9309 | 0.482724 |
| medium | sklearn_hgb_fixed | 4 | 3.10541 | 1.61475 | 1.92315 | 0.480788 |
| small | sklearn_hgb_fixed | 4 | 2.02098 | 1.14187 | 1.76989 | 0.442472 |
| large | xgboost_hist | 4 | 6.05115 | 3.55599 | 1.70168 | 0.42542 |
| medium | xgboost_hist | 4 | 4.90757 | 2.82596 | 1.7366 | 0.43415 |
| small | xgboost_hist | 4 | 2.85599 | 1.64817 | 1.73282 | 0.433205 |


## Memory growth trend (thread=1)
| model | smallest_samples | largest_samples | peak_mb_smallest | peak_mb_largest | approx_mb_per_1k_samples |
| --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 20000 | 50000 | 217.141 | 216.117 | -0.0341146 |
| sklearn_hgb | 20000 | 50000 | 224.484 | 209.957 | -0.484245 |
| sklearn_hgb_fixed | 20000 | 50000 | 224.391 | 209.418 | -0.499089 |
| xgboost_hist | 20000 | 50000 | 237.016 | 222.863 | -0.471745 |


## Initial conclusion
- Best median runtime model: `sklearn_hgb`
- Least-performing median runtime model: `xgboost_hist`
- All scenarios report explicit `r2_spread_for_scenario` to verify score parity while keeping matched hyperparameter values.
