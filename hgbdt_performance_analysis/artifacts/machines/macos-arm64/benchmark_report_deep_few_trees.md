# Histogram GBDT Regressor Benchmark Report

## Experiment controls
- Timeout budget per individual run: `8.0 s`
- Adaptive reduction factor after timeout: `0.5`
- Threads tested: `[1, 2, 4]`
- Dataset templates: `[{'name': 'small', 'start_n_samples': 50000, 'n_features': 40}, {'name': 'medium', 'start_n_samples': 140000, 'n_features': 80}, {'name': 'large', 'start_n_samples': 320000, 'n_features': 120}]`

## Overall ranking (lower is faster)
| model | median_total_s | mean_total_s | geo_mean_total_s | mean_peak_rss_mb | mean_r2 | max_r2_spread_for_matched_scenario |
| --- | --- | --- | --- | --- | --- | --- |
| sklearn_hgb_fixed | 3.17847 | 3.27397 | 2.8646 | 493.825 | 0.603328 | 0.0026101 |
| sklearn_hgb | 3.51263 | 3.4942 | 3.03139 | 473.104 | 0.603328 | 0.0026101 |
| lightgbm_hist | 3.54719 | 3.2543 | 2.86629 | 454.792 | 0.603228 | 0.0026101 |
| xgboost_hist | 4.14116 | 3.57449 | 3.20218 | 478.026 | 0.603871 | 0.0026101 |


## Single-thread behavior
| dataset_name | model | n_samples | n_features | fit_seconds | predict_seconds | total_seconds | peak_rss_mb | r2 | fitted_trees | expected_trees | total_nodes | avg_nodes_per_tree |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 80000 | 120 | 4.7726 | 0.0849361 | 4.87446 | 561.172 | 0.491423 | 48 | 48 | 12144 | 253 |
| large | xgboost_hist | 80000 | 120 | 5.89955 | 0.0249749 | 5.96298 | 666.266 | 0.491074 | 48 | 48 | 12144 | 253 |
| large | sklearn_hgb | 80000 | 120 | 5.88368 | 0.0603284 | 6.02961 | 642.656 | 0.490287 | 48 | 48 | 12144 | 253 |
| large | sklearn_hgb_fixed | 80000 | 120 | 5.9781 | 0.0762009 | 6.1353 | 636.406 | 0.490287 | 48 | 48 | 12144 | 253 |
| medium | xgboost_hist | 140000 | 80 | 5.01937 | 0.0384896 | 5.13257 | 574.5 | 0.568178 | 48 | 48 | 12144 | 253 |
| medium | lightgbm_hist | 140000 | 80 | 5.07837 | 0.140598 | 5.23301 | 559.766 | 0.56851 | 48 | 48 | 12144 | 253 |
| medium | sklearn_hgb | 140000 | 80 | 5.45277 | 0.102517 | 5.5835 | 577.781 | 0.568235 | 48 | 48 | 12144 | 253 |
| medium | sklearn_hgb_fixed | 140000 | 80 | 5.61636 | 0.1153 | 5.79775 | 576.344 | 0.568235 | 48 | 48 | 12144 | 253 |
| small | lightgbm_hist | 50000 | 40 | 0.962995 | 0.0420163 | 1.01659 | 258.094 | 0.749752 | 48 | 48 | 12144 | 253 |
| small | xgboost_hist | 50000 | 40 | 1.5841 | 0.0136182 | 1.60184 | 267.656 | 0.752362 | 48 | 48 | 12144 | 253 |
| small | sklearn_hgb_fixed | 50000 | 40 | 1.61634 | 0.0360355 | 1.70924 | 297.578 | 0.751461 | 48 | 48 | 12144 | 253 |
| small | sklearn_hgb | 50000 | 40 | 1.77164 | 0.0335735 | 1.84969 | 290.344 | 0.751461 | 48 | 48 | 12144 | 253 |


## Multi-thread scalability
| dataset_name | model | max_threads | fit_s_1_thread | fit_s_max_threads | speedup_vs_1_thread | parallel_efficiency |
| --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 4 | 4.7726 | 3.50838 | 1.36034 | 0.340086 |
| medium | lightgbm_hist | 4 | 5.07837 | 4.29289 | 1.18297 | 0.295743 |
| small | lightgbm_hist | 4 | 0.962995 | 1.74806 | 0.550894 | 0.137723 |
| large | sklearn_hgb | 4 | 5.88368 | 3.23983 | 1.81604 | 0.454011 |
| medium | sklearn_hgb | 4 | 5.45277 | 4.74232 | 1.14981 | 0.287452 |
| small | sklearn_hgb | 4 | 1.77164 | 1.28962 | 1.37377 | 0.343442 |
| large | sklearn_hgb_fixed | 4 | 5.9781 | 2.29639 | 2.60326 | 0.650816 |
| medium | sklearn_hgb_fixed | 4 | 5.61636 | 3.68421 | 1.52444 | 0.38111 |
| small | sklearn_hgb_fixed | 4 | 1.61634 | 1.4259 | 1.13356 | 0.28339 |
| large | xgboost_hist | 4 | 5.89955 | 4.12326 | 1.4308 | 0.357699 |
| medium | xgboost_hist | 4 | 5.01937 | 3.01077 | 1.66714 | 0.416784 |
| small | xgboost_hist | 4 | 1.5841 | 1.92473 | 0.823023 | 0.205756 |


## Memory growth trend (thread=1)
| model | smallest_samples | largest_samples | peak_mb_smallest | peak_mb_largest | approx_mb_per_1k_samples |
| --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 50000 | 140000 | 258.094 | 559.766 | 3.35191 |
| sklearn_hgb | 50000 | 140000 | 290.344 | 577.781 | 3.19375 |
| sklearn_hgb_fixed | 50000 | 140000 | 297.578 | 576.344 | 3.0974 |
| xgboost_hist | 50000 | 140000 | 267.656 | 574.5 | 3.40938 |


## Initial conclusion
- Best median runtime model: `sklearn_hgb_fixed`
- Least-performing median runtime model: `xgboost_hist`
- All scenarios report explicit `r2_spread_for_scenario` to verify score parity while keeping matched hyperparameter values.
