# Histogram GBDT Regressor Benchmark Report

## Experiment controls
- Timeout budget per individual run: `10.0 s`
- Adaptive reduction factor after timeout: `0.6`
- Threads tested: `[1, 2, 4, 8, 16]`
- Dataset templates: `[{'name': 'small', 'start_n_samples': 50000, 'n_features': 40}, {'name': 'medium', 'start_n_samples': 140000, 'n_features': 80}, {'name': 'large', 'start_n_samples': 320000, 'n_features': 120}]`

## Overall ranking (lower is faster)
| model | median_total_s | mean_total_s | geo_mean_total_s | mean_peak_rss_mb | mean_r2 | max_r2_spread_for_matched_scenario |
| --- | --- | --- | --- | --- | --- | --- |
| sklearn_hgb_fixed | 1.94619 | 2.54192 | 2.04926 | 320.14 | 0.765253 | 0.0126772 |
| sklearn_hgb | 2.09707 | 2.55799 | 2.12765 | 320 | 0.765253 | 0.0126772 |
| lightgbm_hist | 2.49561 | 3.1499 | 2.63541 | 336.86 | 0.773388 | 0.0126772 |
| xgboost_hist | 2.89534 | 3.36749 | 2.74669 | 331.424 | 0.774732 | 0.0126772 |


## Single-thread behavior
| dataset_name | model | n_samples | n_features | fit_seconds | predict_seconds | total_seconds | peak_rss_mb | r2 | fitted_trees | expected_trees | total_nodes | avg_nodes_per_tree |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| large | sklearn_hgb | 69120 | 120 | 5.65941 | 0.175995 | 5.84103 | 332.914 | 0.663288 | 220 | 220 | 13420 | 61 |
| large | sklearn_hgb_fixed | 69120 | 120 | 5.68815 | 0.176068 | 5.86782 | 333.078 | 0.663288 | 220 | 220 | 13420 | 61 |
| large | lightgbm_hist | 69120 | 120 | 5.90854 | 0.156402 | 6.06806 | 348.051 | 0.673375 | 220 | 220 | 13420 | 61 |
| large | xgboost_hist | 69120 | 120 | 8.10449 | 0.0324454 | 8.13731 | 377.309 | 0.675965 | 220 | 220 | 13420 | 61 |
| medium | sklearn_hgb | 140000 | 80 | 6.37869 | 0.285221 | 6.66909 | 373.902 | 0.745521 | 220 | 220 | 13420 | 61 |
| medium | sklearn_hgb_fixed | 140000 | 80 | 6.72075 | 0.297432 | 7.02074 | 374.406 | 0.745521 | 220 | 220 | 13420 | 61 |
| medium | lightgbm_hist | 140000 | 80 | 7.0125 | 0.318846 | 7.34102 | 402.102 | 0.753709 | 220 | 220 | 13420 | 61 |
| medium | xgboost_hist | 140000 | 80 | 8.335 | 0.0613051 | 8.40394 | 370.555 | 0.75389 | 220 | 220 | 13420 | 61 |
| small | sklearn_hgb_fixed | 50000 | 40 | 1.70002 | 0.0922164 | 1.80006 | 229.387 | 0.886951 | 220 | 220 | 13420 | 61 |
| small | lightgbm_hist | 50000 | 40 | 1.74707 | 0.122556 | 1.87213 | 236.008 | 0.893078 | 220 | 220 | 13420 | 61 |
| small | sklearn_hgb | 50000 | 40 | 1.87378 | 0.102965 | 1.98717 | 229.668 | 0.886951 | 220 | 220 | 13420 | 61 |
| small | xgboost_hist | 50000 | 40 | 2.21628 | 0.0238178 | 2.24421 | 240.465 | 0.894341 | 220 | 220 | 13420 | 61 |


## Multi-thread scalability
| dataset_name | model | max_threads | fit_s_1_thread | fit_s_max_threads | speedup_vs_1_thread | parallel_efficiency |
| --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 16 | 5.90854 | 4.10987 | 1.43765 | 0.089853 |
| medium | lightgbm_hist | 16 | 7.0125 | 4.37247 | 1.60378 | 0.100237 |
| small | lightgbm_hist | 16 | 1.74707 | 1.79926 | 0.970995 | 0.0606872 |
| large | sklearn_hgb | 16 | 5.65941 | 1.87131 | 3.02431 | 0.189019 |
| medium | sklearn_hgb | 16 | 6.37869 | 2.35307 | 2.7108 | 0.169425 |
| small | sklearn_hgb | 16 | 1.87378 | 0.83814 | 2.23564 | 0.139728 |
| large | sklearn_hgb_fixed | 16 | 5.68815 | 1.76848 | 3.21641 | 0.201025 |
| medium | sklearn_hgb_fixed | 16 | 6.72075 | 2.19184 | 3.06626 | 0.191641 |
| small | sklearn_hgb_fixed | 16 | 1.70002 | 0.773641 | 2.19742 | 0.137339 |
| large | xgboost_hist | 16 | 8.10449 | 2.89909 | 2.79553 | 0.174721 |
| medium | xgboost_hist | 16 | 8.335 | 2.8864 | 2.88768 | 0.18048 |
| small | xgboost_hist | 16 | 2.21628 | 0.986441 | 2.24675 | 0.140422 |


## Memory growth trend (thread=1)
| model | smallest_samples | largest_samples | peak_mb_smallest | peak_mb_largest | approx_mb_per_1k_samples |
| --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 50000 | 140000 | 236.008 | 402.102 | 1.84549 |
| sklearn_hgb | 50000 | 140000 | 229.668 | 373.902 | 1.6026 |
| sklearn_hgb_fixed | 50000 | 140000 | 229.387 | 374.406 | 1.61133 |
| xgboost_hist | 50000 | 140000 | 240.465 | 370.555 | 1.44544 |


## Initial conclusion
- Best median runtime model: `sklearn_hgb_fixed`
- Least-performing median runtime model: `xgboost_hist`
- All scenarios report explicit `r2_spread_for_scenario` to verify score parity while keeping matched hyperparameter values.
