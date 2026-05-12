# Histogram GBDT Regressor Benchmark Report

## Experiment controls
- Timeout budget per individual run: `20.0 s`
- Adaptive reduction factor after timeout: `0.6`
- Threads tested: `[1, 2, 3, 6]`
- Dataset templates: `[{'name': 'small', 'start_n_samples': 12000, 'n_features': 24}, {'name': 'medium', 'start_n_samples': 180000, 'n_features': 120}]`

## Overall ranking (lower is faster)
| model | median_total_s | mean_total_s | geo_mean_total_s | mean_peak_rss_mb | mean_r2 | max_r2_spread_for_matched_scenario |
| --- | --- | --- | --- | --- | --- | --- |
| sklearn_hgb_fixed | 4.19882 | 5.87514 | 4.20401 | 371.488 | 0.802637 | 0.00799633 |
| xgboost_hist | 4.71036 | 6.60501 | 4.79664 | 379.926 | 0.810093 | 0.00799633 |
| lightgbm_hist | 4.76744 | 6.00895 | 4.3044 | 464.314 | 0.81017 | 0.00799633 |
| sklearn_hgb | 7.02962 | 6.75993 | 5.46413 | 367.283 | 0.802637 | 0.00799633 |


## Single-thread behavior
| dataset_name | model | n_samples | n_features | fit_seconds | predict_seconds | total_seconds | peak_rss_mb | r2 | fitted_trees | expected_trees | total_nodes | avg_nodes_per_tree |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| medium | sklearn_hgb_fixed | 180000 | 120 | 14.0204 | 0.849924 | 14.905 | 564.297 | 0.662975 | 220 | 220 | 13420 | 61 |
| medium | sklearn_hgb | 180000 | 120 | 14.2668 | 0.815107 | 15.1113 | 563.719 | 0.662975 | 220 | 220 | 13420 | 61 |
| medium | lightgbm_hist | 180000 | 120 | 15.0258 | 0.392221 | 15.8587 | 776.453 | 0.670972 | 220 | 220 | 13420 | 61 |
| medium | xgboost_hist | 180000 | 120 | 15.495 | 0.0723071 | 16.0775 | 590.266 | 0.670433 | 220 | 220 | 13420 | 61 |
| small | lightgbm_hist | 12000 | 24 | 0.506795 | 0.022384 | 1.55774 | 184.078 | 0.949369 | 220 | 220 | 13386 | 60.8455 |
| small | sklearn_hgb | 12000 | 24 | 0.839609 | 0.0231214 | 2.2375 | 181.25 | 0.942299 | 220 | 220 | 13414 | 60.9727 |
| small | xgboost_hist | 12000 | 24 | 0.880403 | 0.00555756 | 2.35007 | 188.125 | 0.949753 | 220 | 220 | 13390 | 60.8636 |
| small | sklearn_hgb_fixed | 12000 | 24 | 0.912365 | 0.0297856 | 2.36771 | 179.359 | 0.942299 | 220 | 220 | 13414 | 60.9727 |


## Multi-thread scalability
| dataset_name | model | max_threads | fit_s_1_thread | fit_s_max_threads | speedup_vs_1_thread | parallel_efficiency |
| --- | --- | --- | --- | --- | --- | --- |
| medium | lightgbm_hist | 6 | 15.0258 | 6.83115 | 2.1996 | 0.3666 |
| small | lightgbm_hist | 6 | 0.506795 | 1.84042 | 0.275369 | 0.0458949 |
| medium | sklearn_hgb | 6 | 14.2668 | 6.04917 | 2.35847 | 0.393079 |
| small | sklearn_hgb | 6 | 0.839609 | 2.90477 | 0.289045 | 0.0481742 |
| medium | sklearn_hgb_fixed | 6 | 14.0204 | 5.41001 | 2.59157 | 0.431929 |
| small | sklearn_hgb_fixed | 6 | 0.912365 | 0.565359 | 1.61378 | 0.268964 |
| medium | xgboost_hist | 6 | 15.495 | 6.5456 | 2.36724 | 0.39454 |
| small | xgboost_hist | 6 | 0.880403 | 0.874809 | 1.00639 | 0.167732 |


## Memory growth trend (thread=1)
| model | smallest_samples | largest_samples | peak_mb_smallest | peak_mb_largest | approx_mb_per_1k_samples |
| --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 12000 | 180000 | 184.078 | 776.453 | 3.52604 |
| sklearn_hgb | 12000 | 180000 | 181.25 | 563.719 | 2.2766 |
| sklearn_hgb_fixed | 12000 | 180000 | 179.359 | 564.297 | 2.29129 |
| xgboost_hist | 12000 | 180000 | 188.125 | 590.266 | 2.39369 |


## Initial conclusion
- Best median runtime model: `sklearn_hgb_fixed`
- Least-performing median runtime model: `sklearn_hgb`
- All scenarios report explicit `r2_spread_for_scenario` to verify score parity while keeping matched hyperparameter values.
