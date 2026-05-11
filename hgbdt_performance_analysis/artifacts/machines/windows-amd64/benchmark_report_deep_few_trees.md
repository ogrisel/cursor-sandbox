# Histogram GBDT Regressor Benchmark Report

## Experiment controls
- Timeout budget per individual run: `12.0 s`
- Adaptive reduction factor after timeout: `0.5`
- Threads tested: `[1, 2, 4, 8, 16]`
- Dataset templates: `[{'name': 'small', 'start_n_samples': 50000, 'n_features': 40}, {'name': 'medium', 'start_n_samples': 140000, 'n_features': 80}, {'name': 'large', 'start_n_samples': 320000, 'n_features': 120}]`

## Overall ranking (lower is faster)
| model | median_total_s | mean_total_s | geo_mean_total_s | mean_peak_rss_mb | mean_r2 | max_r2_spread_for_matched_scenario |
| --- | --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 2.15866 | 2.50055 | 2.10276 | 276.556 | 0.608506 | 0.00309473 |
| sklearn_hgb_fixed | 3.37974 | 3.29201 | 2.95245 | 295.755 | 0.607953 | 0.00309473 |
| sklearn_hgb | 3.58794 | 3.44218 | 3.13335 | 296.536 | 0.607953 | 0.00309473 |
| xgboost_hist | 5.34867 | 4.79775 | 4.27623 | 365.529 | 0.608242 | 0.00309473 |


## Single-thread behavior
| dataset_name | model | n_samples | n_features | fit_seconds | predict_seconds | total_seconds | peak_rss_mb | r2 | fitted_trees | expected_trees | total_nodes | avg_nodes_per_tree |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 40000 | 120 | 4.71402 | 0.0418411 | 4.75851 | 263.242 | 0.507257 | 48 | 48 | 12144 | 253 |
| large | sklearn_hgb | 40000 | 120 | 5.78752 | 0.0841923 | 5.87869 | 301.078 | 0.504162 | 48 | 48 | 12144 | 253 |
| large | sklearn_hgb_fixed | 40000 | 120 | 5.7884 | 0.0812082 | 5.87959 | 300.293 | 0.504162 | 48 | 48 | 12144 | 253 |
| large | xgboost_hist | 40000 | 120 | 8.16799 | 0.0195657 | 8.19043 | 425.887 | 0.504185 | 48 | 48 | 12144 | 253 |
| medium | lightgbm_hist | 140000 | 80 | 6.18465 | 0.1366 | 6.32178 | 362.93 | 0.56851 | 48 | 48 | 12144 | 253 |
| medium | sklearn_hgb | 140000 | 80 | 6.51922 | 0.236666 | 6.76327 | 373.582 | 0.568235 | 48 | 48 | 12144 | 253 |
| medium | sklearn_hgb_fixed | 140000 | 80 | 6.52418 | 0.236675 | 6.76377 | 373.707 | 0.568235 | 48 | 48 | 12144 | 253 |
| medium | xgboost_hist | 140000 | 80 | 8.41318 | 0.0593289 | 8.4786 | 411.348 | 0.568178 | 48 | 48 | 12144 | 253 |
| small | lightgbm_hist | 50000 | 40 | 1.68073 | 0.0484453 | 1.73003 | 198.023 | 0.749752 | 48 | 48 | 12144 | 253 |
| small | sklearn_hgb_fixed | 50000 | 40 | 2.20551 | 0.0846924 | 2.29183 | 212.203 | 0.751461 | 48 | 48 | 12144 | 253 |
| small | sklearn_hgb | 50000 | 40 | 2.21503 | 0.0835163 | 2.30857 | 211.902 | 0.751461 | 48 | 48 | 12144 | 253 |
| small | xgboost_hist | 50000 | 40 | 2.83088 | 0.018324 | 2.8533 | 251.898 | 0.752362 | 48 | 48 | 12144 | 253 |


## Multi-thread scalability
| dataset_name | model | max_threads | fit_s_1_thread | fit_s_max_threads | speedup_vs_1_thread | parallel_efficiency |
| --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 16 | 4.71402 | 2.14296 | 2.19977 | 0.137486 |
| medium | lightgbm_hist | 16 | 6.18465 | 2.811 | 2.20016 | 0.13751 |
| small | lightgbm_hist | 16 | 1.68073 | 0.955578 | 1.75887 | 0.109929 |
| large | sklearn_hgb | 16 | 5.78752 | 3.92468 | 1.47465 | 0.0921655 |
| medium | sklearn_hgb | 16 | 6.51922 | 3.93642 | 1.65613 | 0.103508 |
| small | sklearn_hgb | 16 | 2.21503 | 1.99673 | 1.10933 | 0.069333 |
| large | sklearn_hgb_fixed | 16 | 5.7884 | 3.34867 | 1.72857 | 0.108035 |
| medium | sklearn_hgb_fixed | 16 | 6.52418 | 3.40864 | 1.91401 | 0.119626 |
| small | sklearn_hgb_fixed | 16 | 2.20551 | 1.45011 | 1.52093 | 0.0950579 |
| large | xgboost_hist | 16 | 8.16799 | 5.60979 | 1.45602 | 0.0910015 |
| medium | xgboost_hist | 16 | 8.41318 | 5.32432 | 1.58014 | 0.0987589 |
| small | xgboost_hist | 16 | 2.83088 | 1.97857 | 1.43077 | 0.0894233 |


## Memory growth trend (thread=1)
| model | smallest_samples | largest_samples | peak_mb_smallest | peak_mb_largest | approx_mb_per_1k_samples |
| --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 40000 | 140000 | 263.242 | 362.93 | 0.996875 |
| sklearn_hgb | 40000 | 140000 | 301.078 | 373.582 | 0.725039 |
| sklearn_hgb_fixed | 40000 | 140000 | 300.293 | 373.707 | 0.734141 |
| xgboost_hist | 40000 | 140000 | 425.887 | 411.348 | -0.145391 |


## Initial conclusion
- Best median runtime model: `lightgbm_hist`
- Least-performing median runtime model: `xgboost_hist`
- All scenarios report explicit `r2_spread_for_scenario` to verify score parity while keeping matched hyperparameter values.
