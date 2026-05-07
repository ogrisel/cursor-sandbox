# Histogram GBDT Regressor Benchmark Report

## Experiment controls
- Timeout budget per individual run: `8.0 s`
- Adaptive reduction factor after timeout: `0.5`
- Threads tested: `[1, 2, 4]`
- Dataset templates: `[{'name': 'small', 'start_n_samples': 50000, 'n_features': 40}, {'name': 'medium', 'start_n_samples': 140000, 'n_features': 80}, {'name': 'large', 'start_n_samples': 320000, 'n_features': 120}]`

## Overall ranking (lower is faster)
| model | median_total_s | mean_total_s | geo_mean_total_s | mean_peak_rss_mb | mean_r2 | max_r2_spread_for_matched_scenario |
| --- | --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 1.56309 | 2.11272 | 1.64119 | 324.349 | 0.608506 | 0.00309473 |
| sklearn_hgb | 1.84093 | 2.41873 | 2.04071 | 335.339 | 0.607953 | 0.00309473 |
| sklearn_hgb_fixed | 1.85162 | 2.42138 | 2.03925 | 335.488 | 0.607953 | 0.00309473 |
| xgboost_hist | 2.29037 | 3.08396 | 2.55653 | 353.026 | 0.608242 | 0.00309473 |


## Single-thread behavior
| dataset_name | model | n_samples | n_features | fit_seconds | predict_seconds | total_seconds | peak_rss_mb | r2 | fitted_trees | expected_trees | total_nodes | avg_nodes_per_tree |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 40000 | 120 | 3.66219 | 0.0300456 | 3.69365 | 299.324 | 0.507257 | 48 | 48 | 12144 | 253 |
| large | sklearn_hgb | 40000 | 120 | 3.98509 | 0.0272181 | 4.01624 | 335.414 | 0.504162 | 48 | 48 | 12144 | 253 |
| large | sklearn_hgb_fixed | 40000 | 120 | 3.99892 | 0.0267743 | 4.02964 | 335.398 | 0.504162 | 48 | 48 | 12144 | 253 |
| large | xgboost_hist | 40000 | 120 | 5.69479 | 0.0113772 | 5.71249 | 369.316 | 0.504185 | 48 | 48 | 12144 | 253 |
| medium | lightgbm_hist | 140000 | 80 | 5.17834 | 0.0985366 | 5.27943 | 400.262 | 0.56851 | 48 | 48 | 12144 | 253 |
| medium | sklearn_hgb_fixed | 140000 | 80 | 5.33973 | 0.0845927 | 5.42843 | 410.453 | 0.568235 | 48 | 48 | 12144 | 253 |
| medium | sklearn_hgb | 140000 | 80 | 5.37175 | 0.0831349 | 5.45796 | 410.453 | 0.568235 | 48 | 48 | 12144 | 253 |
| medium | xgboost_hist | 140000 | 80 | 6.32645 | 0.0349405 | 6.36485 | 385.18 | 0.568178 | 48 | 48 | 12144 | 253 |
| small | lightgbm_hist | 50000 | 40 | 1.34057 | 0.0349451 | 1.37873 | 238.762 | 0.749752 | 48 | 48 | 12144 | 253 |
| small | sklearn_hgb_fixed | 50000 | 40 | 1.6634 | 0.0265062 | 1.69042 | 247.152 | 0.751461 | 48 | 48 | 12144 | 253 |
| small | sklearn_hgb | 50000 | 40 | 1.67436 | 0.0264594 | 1.70298 | 247.137 | 0.751461 | 48 | 48 | 12144 | 253 |
| small | xgboost_hist | 50000 | 40 | 1.95574 | 0.0124128 | 1.97014 | 283.043 | 0.752362 | 48 | 48 | 12144 | 253 |


## Multi-thread scalability
| dataset_name | model | max_threads | fit_s_1_thread | fit_s_max_threads | speedup_vs_1_thread | parallel_efficiency |
| --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 4 | 3.66219 | 1.08466 | 3.37636 | 0.844089 |
| medium | lightgbm_hist | 4 | 5.17834 | 1.52615 | 3.39307 | 0.848267 |
| small | lightgbm_hist | 4 | 1.34057 | 0.426305 | 3.14461 | 0.786154 |
| large | sklearn_hgb | 4 | 3.98509 | 1.39894 | 2.84864 | 0.712161 |
| medium | sklearn_hgb | 4 | 5.37175 | 1.80684 | 2.97301 | 0.743252 |
| small | sklearn_hgb | 4 | 1.67436 | 0.772773 | 2.16669 | 0.541672 |
| large | sklearn_hgb_fixed | 4 | 3.99892 | 1.46879 | 2.7226 | 0.680651 |
| medium | sklearn_hgb_fixed | 4 | 5.33973 | 1.82158 | 2.93137 | 0.732843 |
| small | sklearn_hgb_fixed | 4 | 1.6634 | 0.733795 | 2.26684 | 0.56671 |
| large | xgboost_hist | 4 | 5.69479 | 2.16534 | 2.62997 | 0.657493 |
| medium | xgboost_hist | 4 | 6.32645 | 2.27413 | 2.78192 | 0.695479 |
| small | xgboost_hist | 4 | 1.95574 | 0.806353 | 2.42541 | 0.606353 |


## Memory growth trend (thread=1)
| model | smallest_samples | largest_samples | peak_mb_smallest | peak_mb_largest | approx_mb_per_1k_samples |
| --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 40000 | 140000 | 299.324 | 400.262 | 1.00938 |
| sklearn_hgb | 40000 | 140000 | 335.414 | 410.453 | 0.750391 |
| sklearn_hgb_fixed | 40000 | 140000 | 335.398 | 410.453 | 0.750547 |
| xgboost_hist | 40000 | 140000 | 369.316 | 385.18 | 0.158633 |


## Initial conclusion
- Best median runtime model: `lightgbm_hist`
- Least-performing median runtime model: `xgboost_hist`
- All scenarios report explicit `r2_spread_for_scenario` to verify score parity while keeping matched hyperparameter values.
