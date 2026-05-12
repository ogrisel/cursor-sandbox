# Histogram GBDT Regressor Benchmark Report

## Experiment controls
- Timeout budget per individual run: `5.0 s`
- Adaptive reduction factor after timeout: `0.6`
- Threads tested: `[1, 2, 3, 6]`
- Dataset templates: `[{'name': 'small', 'start_n_samples': 12000, 'n_features': 24}, {'name': 'medium', 'start_n_samples': 180000, 'n_features': 120}]`

## Overall ranking (lower is faster)
| model | median_total_s | mean_total_s | geo_mean_total_s | mean_peak_rss_mb | mean_r2 | max_r2_spread_for_matched_scenario |
| --- | --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 1.1158 | 1.13775 | 0.997074 | 207.484 | 0.82159 | 0.0288809 |
| sklearn_hgb_fixed | 1.2494 | 1.25578 | 1.08662 | 214.041 | 0.806318 | 0.0288809 |
| sklearn_hgb | 1.41754 | 1.8789 | 1.65464 | 212.254 | 0.806318 | 0.0288809 |
| xgboost_hist | 1.51081 | 1.73266 | 1.44098 | 220.023 | 0.824486 | 0.0288809 |


## Single-thread behavior
| dataset_name | model | n_samples | n_features | fit_seconds | predict_seconds | total_seconds | peak_rss_mb | r2 | fitted_trees | expected_trees | total_nodes | avg_nodes_per_tree |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| medium | lightgbm_hist | 13996 | 120 | 1.97978 | 0.0260922 | 2.01687 | 230.641 | 0.693811 | 220 | 220 | 13420 | 61 |
| medium | sklearn_hgb_fixed | 13996 | 120 | 2.42074 | 0.026591 | 2.46408 | 250.5 | 0.670338 | 220 | 220 | 13420 | 61 |
| medium | sklearn_hgb | 13996 | 120 | 2.48555 | 0.0268944 | 2.56989 | 251.375 | 0.670338 | 220 | 220 | 13420 | 61 |
| medium | xgboost_hist | 13996 | 120 | 3.60553 | 0.00561242 | 3.61387 | 255.875 | 0.699219 | 220 | 220 | 13420 | 61 |
| small | lightgbm_hist | 12000 | 24 | 0.408589 | 0.0229077 | 0.450243 | 178.141 | 0.949369 | 220 | 220 | 13386 | 60.8455 |
| small | sklearn_hgb | 12000 | 24 | 0.579447 | 0.0182991 | 0.625077 | 178.359 | 0.942299 | 220 | 220 | 13414 | 60.9727 |
| small | sklearn_hgb_fixed | 12000 | 24 | 0.647126 | 0.0199708 | 0.710961 | 177.906 | 0.942299 | 220 | 220 | 13414 | 60.9727 |
| small | xgboost_hist | 12000 | 24 | 0.66326 | 0.0577589 | 0.791323 | 187.625 | 0.949753 | 220 | 220 | 13390 | 60.8636 |


## Multi-thread scalability
| dataset_name | model | max_threads | fit_s_1_thread | fit_s_max_threads | speedup_vs_1_thread | parallel_efficiency |
| --- | --- | --- | --- | --- | --- | --- |
| medium | lightgbm_hist | 6 | 1.97978 | 1.51284 | 1.30866 | 0.218109 |
| small | lightgbm_hist | 6 | 0.408589 | 0.762306 | 0.535991 | 0.0893319 |
| medium | sklearn_hgb | 6 | 2.48555 | 2.53413 | 0.980828 | 0.163471 |
| small | sklearn_hgb | 6 | 0.579447 | 3.64612 | 0.158922 | 0.0264869 |
| medium | sklearn_hgb_fixed | 6 | 2.42074 | 1.71377 | 1.41252 | 0.235421 |
| small | sklearn_hgb_fixed | 6 | 0.647126 | 0.433132 | 1.49406 | 0.24901 |
| medium | xgboost_hist | 6 | 3.60553 | 2.15868 | 1.67025 | 0.278374 |
| small | xgboost_hist | 6 | 0.66326 | 0.78601 | 0.843831 | 0.140639 |


## Memory growth trend (thread=1)
| model | smallest_samples | largest_samples | peak_mb_smallest | peak_mb_largest | approx_mb_per_1k_samples |
| --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 12000 | 13996 | 178.141 | 230.641 | 26.3026 |
| sklearn_hgb | 12000 | 13996 | 178.359 | 251.375 | 36.581 |
| sklearn_hgb_fixed | 12000 | 13996 | 177.906 | 250.5 | 36.3696 |
| xgboost_hist | 12000 | 13996 | 187.625 | 255.875 | 34.1934 |


## Initial conclusion
- Best median runtime model: `lightgbm_hist`
- Least-performing median runtime model: `xgboost_hist`
- All scenarios report explicit `r2_spread_for_scenario` to verify score parity while keeping matched hyperparameter values.
