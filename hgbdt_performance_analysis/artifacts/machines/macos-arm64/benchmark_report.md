# Histogram GBDT Regressor Benchmark Report

## Experiment controls
- Timeout budget per individual run: `8.0 s`
- Adaptive reduction factor after timeout: `0.5`
- Threads tested: `[1, 2, 4]`
- Dataset templates: `[{'name': 'small', 'start_n_samples': 50000, 'n_features': 40}, {'name': 'medium', 'start_n_samples': 140000, 'n_features': 80}, {'name': 'large', 'start_n_samples': 320000, 'n_features': 120}]`

## Overall ranking (lower is faster)
| model | median_total_s | mean_total_s | geo_mean_total_s | mean_peak_rss_mb | mean_r2 | max_r2_spread_for_matched_scenario |
| --- | --- | --- | --- | --- | --- | --- |
| sklearn_hgb_fixed | 2.60347 | 2.88627 | 2.74369 | 268.483 | 0.782765 | 0.0177437 |
| sklearn_hgb | 2.64762 | 3.00267 | 2.88626 | 263.559 | 0.782765 | 0.0177437 |
| lightgbm_hist | 2.8073 | 3.0447 | 2.89055 | 298.811 | 0.793002 | 0.0177437 |
| xgboost_hist | 3.73044 | 3.68861 | 3.52782 | 312.24 | 0.793637 | 0.0177437 |


## Single-thread behavior
| dataset_name | model | n_samples | n_features | fit_seconds | predict_seconds | total_seconds | peak_rss_mb | r2 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 40000 | 120 | 3.83026 | 0.0784583 | 3.93278 | 330.562 | 0.692337 |
| large | sklearn_hgb_fixed | 40000 | 120 | 4.38892 | 0.0772284 | 4.49601 | 303.719 | 0.675577 |
| large | sklearn_hgb | 40000 | 120 | 4.54979 | 0.076374 | 4.65826 | 304.578 | 0.675577 |
| large | xgboost_hist | 40000 | 120 | 5.54468 | 0.0175126 | 5.59983 | 380.484 | 0.69332 |
| medium | lightgbm_hist | 70000 | 80 | 4.06279 | 0.153276 | 4.24369 | 340.766 | 0.79359 |
| medium | sklearn_hgb | 70000 | 80 | 4.38465 | 0.141553 | 4.57202 | 299.719 | 0.785099 |
| medium | sklearn_hgb_fixed | 70000 | 80 | 4.46793 | 0.140245 | 4.63114 | 297.281 | 0.785099 |
| medium | xgboost_hist | 70000 | 80 | 4.75057 | 0.0259813 | 4.8358 | 350.75 | 0.793248 |
| small | lightgbm_hist | 50000 | 40 | 1.62564 | 0.0843643 | 1.77806 | 215.406 | 0.893078 |
| small | sklearn_hgb | 50000 | 40 | 1.9117 | 0.074443 | 1.99323 | 205.5 | 0.88762 |
| small | xgboost_hist | 50000 | 40 | 2.03196 | 0.0230299 | 2.07224 | 217.734 | 0.894341 |
| small | sklearn_hgb_fixed | 50000 | 40 | 2.23103 | 0.105455 | 2.41308 | 206.266 | 0.88762 |


## Multi-thread scalability
| dataset_name | model | max_threads | fit_s_1_thread | fit_s_max_threads | speedup_vs_1_thread | parallel_efficiency |
| --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 4 | 3.83026 | 2.41093 | 1.58871 | 0.397176 |
| medium | lightgbm_hist | 4 | 4.06279 | 4.1119 | 0.988058 | 0.247015 |
| small | lightgbm_hist | 4 | 1.62564 | 2.18049 | 0.745538 | 0.186384 |
| large | sklearn_hgb | 4 | 4.54979 | 2.8701 | 1.58523 | 0.396309 |
| medium | sklearn_hgb | 4 | 4.38465 | 2.49988 | 1.75395 | 0.438486 |
| small | sklearn_hgb | 4 | 1.9117 | 2.20702 | 0.866187 | 0.216547 |
| large | sklearn_hgb_fixed | 4 | 4.38892 | 1.80413 | 2.4327 | 0.608176 |
| medium | sklearn_hgb_fixed | 4 | 4.46793 | 1.70197 | 2.62515 | 0.656288 |
| small | sklearn_hgb_fixed | 4 | 2.23103 | 2.57526 | 0.86633 | 0.216583 |
| large | xgboost_hist | 4 | 5.54468 | 3.70672 | 1.49584 | 0.373961 |
| medium | xgboost_hist | 4 | 4.75057 | 3.52658 | 1.34707 | 0.336768 |
| small | xgboost_hist | 4 | 2.03196 | 2.48503 | 0.817681 | 0.20442 |


## Memory growth trend (thread=1)
| model | smallest_samples | largest_samples | peak_mb_smallest | peak_mb_largest | approx_mb_per_1k_samples |
| --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 40000 | 70000 | 330.562 | 340.766 | 0.340104 |
| sklearn_hgb | 40000 | 70000 | 304.578 | 299.719 | -0.161979 |
| sklearn_hgb_fixed | 40000 | 70000 | 303.719 | 297.281 | -0.214583 |
| xgboost_hist | 40000 | 70000 | 380.484 | 350.75 | -0.991146 |


## Initial conclusion
- Best median runtime model: `sklearn_hgb_fixed`
- Least-performing median runtime model: `xgboost_hist`
- All scenarios report explicit `r2_spread_for_scenario` to verify score parity while keeping matched hyperparameter values.
