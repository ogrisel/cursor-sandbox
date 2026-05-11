# Histogram GBDT Regressor Benchmark Report

## Experiment controls
- Timeout budget per individual run: `10.0 s`
- Adaptive reduction factor after timeout: `0.6`
- Threads tested: `[1, 2, 4, 8, 16]`
- Dataset templates: `[{'name': 'small', 'start_n_samples': 50000, 'n_features': 40}, {'name': 'medium', 'start_n_samples': 140000, 'n_features': 80}, {'name': 'large', 'start_n_samples': 320000, 'n_features': 120}]`

## Overall ranking (lower is faster)
| model | median_total_s | mean_total_s | geo_mean_total_s | mean_peak_rss_mb | mean_r2 | max_r2_spread_for_matched_scenario |
| --- | --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 1.96747 | 2.48701 | 2.1316 | 316.589 | 0.783123 | 0.0126772 |
| xgboost_hist | 2.12336 | 2.88662 | 2.37531 | 319.693 | 0.784259 | 0.0126772 |
| sklearn_hgb_fixed | 2.85386 | 3.0068 | 2.72064 | 295.613 | 0.774666 | 0.0126772 |
| sklearn_hgb | 2.93229 | 3.05283 | 2.76601 | 295.718 | 0.774666 | 0.0126772 |


## Single-thread behavior
| dataset_name | model | n_samples | n_features | fit_seconds | predict_seconds | total_seconds | peak_rss_mb | r2 | fitted_trees | expected_trees | total_nodes | avg_nodes_per_tree |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| large | sklearn_hgb_fixed | 69120 | 120 | 5.60705 | 0.177125 | 5.79048 | 332.66 | 0.663288 | 220 | 220 | 13420 | 61 |
| large | sklearn_hgb | 69120 | 120 | 5.67726 | 0.175313 | 5.86292 | 333.305 | 0.663288 | 220 | 220 | 13420 | 61 |
| large | lightgbm_hist | 69120 | 120 | 5.92169 | 0.156967 | 6.08159 | 348.48 | 0.673375 | 220 | 220 | 13420 | 61 |
| large | xgboost_hist | 69120 | 120 | 7.96472 | 0.032191 | 8.0036 | 377.004 | 0.675965 | 220 | 220 | 13420 | 61 |
| medium | sklearn_hgb | 84000 | 80 | 4.3293 | 0.174071 | 4.50903 | 305.434 | 0.77376 | 220 | 220 | 13420 | 61 |
| medium | sklearn_hgb_fixed | 84000 | 80 | 4.35877 | 0.177415 | 4.53998 | 305.887 | 0.77376 | 220 | 220 | 13420 | 61 |
| medium | lightgbm_hist | 84000 | 80 | 4.58747 | 0.194614 | 4.78584 | 342.223 | 0.782916 | 220 | 220 | 13420 | 61 |
| medium | xgboost_hist | 84000 | 80 | 5.7599 | 0.0430157 | 5.81328 | 334.98 | 0.78247 | 220 | 220 | 13420 | 61 |
| small | sklearn_hgb | 50000 | 40 | 1.59468 | 0.0916186 | 1.69113 | 229.371 | 0.886951 | 220 | 220 | 13420 | 61 |
| small | lightgbm_hist | 50000 | 40 | 1.61908 | 0.111437 | 1.73729 | 236.137 | 0.893078 | 220 | 220 | 13420 | 61 |
| small | sklearn_hgb_fixed | 50000 | 40 | 1.64869 | 0.0892066 | 1.74228 | 228.707 | 0.886951 | 220 | 220 | 13420 | 61 |
| small | xgboost_hist | 50000 | 40 | 2.03936 | 0.0222293 | 2.06969 | 240.305 | 0.894341 | 220 | 220 | 13420 | 61 |


## Multi-thread scalability
| dataset_name | model | max_threads | fit_s_1_thread | fit_s_max_threads | speedup_vs_1_thread | parallel_efficiency |
| --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 16 | 5.92169 | 3.41473 | 1.73416 | 0.108385 |
| medium | lightgbm_hist | 16 | 4.58747 | 2.93443 | 1.56333 | 0.0977078 |
| small | lightgbm_hist | 16 | 1.61908 | 1.92721 | 0.840115 | 0.0525072 |
| large | sklearn_hgb | 16 | 5.67726 | 3.89582 | 1.45727 | 0.0910793 |
| medium | sklearn_hgb | 16 | 4.3293 | 2.8657 | 1.51073 | 0.0944206 |
| small | sklearn_hgb | 16 | 1.59468 | 1.43416 | 1.11193 | 0.0694955 |
| large | sklearn_hgb_fixed | 16 | 5.60705 | 3.63227 | 1.54368 | 0.0964798 |
| medium | sklearn_hgb_fixed | 16 | 4.35877 | 2.80309 | 1.55499 | 0.0971868 |
| small | sklearn_hgb_fixed | 16 | 1.64869 | 1.36184 | 1.21063 | 0.0756643 |
| large | xgboost_hist | 16 | 7.96472 | 2.86784 | 2.77726 | 0.173579 |
| medium | xgboost_hist | 16 | 5.7599 | 2.10487 | 2.73647 | 0.171029 |
| small | xgboost_hist | 16 | 2.03936 | 0.975973 | 2.08957 | 0.130598 |


## Memory growth trend (thread=1)
| model | smallest_samples | largest_samples | peak_mb_smallest | peak_mb_largest | approx_mb_per_1k_samples |
| --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 50000 | 84000 | 236.137 | 342.223 | 3.12017 |
| sklearn_hgb | 50000 | 84000 | 229.371 | 305.434 | 2.23713 |
| sklearn_hgb_fixed | 50000 | 84000 | 228.707 | 305.887 | 2.26999 |
| xgboost_hist | 50000 | 84000 | 240.305 | 334.98 | 2.78458 |


## Initial conclusion
- Best median runtime model: `lightgbm_hist`
- Least-performing median runtime model: `sklearn_hgb`
- All scenarios report explicit `r2_spread_for_scenario` to verify score parity while keeping matched hyperparameter values.
