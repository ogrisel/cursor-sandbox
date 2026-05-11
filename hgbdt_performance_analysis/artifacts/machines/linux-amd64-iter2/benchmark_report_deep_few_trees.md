# Histogram GBDT Regressor Benchmark Report

## Experiment controls
- Timeout budget per individual run: `10.0 s`
- Adaptive reduction factor after timeout: `0.6`
- Threads tested: `[1, 2, 4, 8, 16]`
- Dataset templates: `[{'name': 'small', 'start_n_samples': 50000, 'n_features': 40}, {'name': 'medium', 'start_n_samples': 140000, 'n_features': 80}, {'name': 'large', 'start_n_samples': 320000, 'n_features': 120}]`

## Overall ranking (lower is faster)
| model | median_total_s | mean_total_s | geo_mean_total_s | mean_peak_rss_mb | mean_r2 | max_r2_spread_for_matched_scenario |
| --- | --- | --- | --- | --- | --- | --- |
| sklearn_hgb_fixed | 1.44049 | 1.93898 | 1.55607 | 387.616 | 0.608359 | 0.00353867 |
| sklearn_hgb | 1.57792 | 1.97377 | 1.59632 | 387.704 | 0.608359 | 0.00353867 |
| xgboost_hist | 2.04359 | 2.63179 | 2.12443 | 385.27 | 0.607731 | 0.00353867 |
| lightgbm_hist | 2.17499 | 2.39005 | 1.9387 | 392.501 | 0.607389 | 0.00353867 |


## Single-thread behavior
| dataset_name | model | n_samples | n_features | fit_seconds | predict_seconds | total_seconds | peak_rss_mb | r2 | fitted_trees | expected_trees | total_nodes | avg_nodes_per_tree |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| large | sklearn_hgb_fixed | 115200 | 120 | 5.56658 | 0.084786 | 5.65258 | 474.277 | 0.506192 | 48 | 48 | 12144 | 253 |
| large | sklearn_hgb | 115200 | 120 | 5.80777 | 0.0835698 | 5.89556 | 473.988 | 0.506192 | 48 | 48 | 12144 | 253 |
| large | lightgbm_hist | 115200 | 120 | 5.98302 | 0.0886596 | 6.07248 | 465.062 | 0.503905 | 48 | 48 | 12144 | 253 |
| large | xgboost_hist | 115200 | 120 | 7.33451 | 0.0314189 | 7.37128 | 448.941 | 0.502653 | 48 | 48 | 12144 | 253 |
| medium | sklearn_hgb | 140000 | 80 | 4.17856 | 0.0911324 | 4.27281 | 412.152 | 0.568121 | 48 | 48 | 12144 | 253 |
| medium | sklearn_hgb_fixed | 140000 | 80 | 4.28936 | 0.0931527 | 4.39138 | 412.305 | 0.568121 | 48 | 48 | 12144 | 253 |
| medium | lightgbm_hist | 140000 | 80 | 4.54013 | 0.108369 | 4.65827 | 400.445 | 0.56851 | 48 | 48 | 12144 | 253 |
| medium | xgboost_hist | 140000 | 80 | 5.19202 | 0.0373434 | 5.23632 | 386.629 | 0.568178 | 48 | 48 | 12144 | 253 |
| small | lightgbm_hist | 50000 | 40 | 1.12533 | 0.0389393 | 1.16869 | 239.539 | 0.749752 | 48 | 48 | 12144 | 253 |
| small | sklearn_hgb | 50000 | 40 | 1.14637 | 0.0303825 | 1.17896 | 248.98 | 0.750765 | 48 | 48 | 12144 | 253 |
| small | sklearn_hgb_fixed | 50000 | 40 | 1.16564 | 0.0314147 | 1.20051 | 249.098 | 0.750765 | 48 | 48 | 12144 | 253 |
| small | xgboost_hist | 50000 | 40 | 1.58692 | 0.0123276 | 1.60231 | 284.715 | 0.752362 | 48 | 48 | 12144 | 253 |


## Multi-thread scalability
| dataset_name | model | max_threads | fit_s_1_thread | fit_s_max_threads | speedup_vs_1_thread | parallel_efficiency |
| --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 16 | 5.98302 | 3.3256 | 1.79908 | 0.112442 |
| medium | lightgbm_hist | 16 | 4.54013 | 2.99904 | 1.51386 | 0.0946162 |
| small | lightgbm_hist | 16 | 1.12533 | 1.62761 | 0.6914 | 0.0432125 |
| large | sklearn_hgb | 16 | 5.80777 | 1.90382 | 3.0506 | 0.190662 |
| medium | sklearn_hgb | 16 | 4.17856 | 1.54995 | 2.69593 | 0.168496 |
| small | sklearn_hgb | 16 | 1.14637 | 0.691667 | 1.6574 | 0.103587 |
| large | sklearn_hgb_fixed | 16 | 5.56658 | 1.77988 | 3.1275 | 0.195469 |
| medium | sklearn_hgb_fixed | 16 | 4.28936 | 1.40881 | 3.04467 | 0.190292 |
| small | sklearn_hgb_fixed | 16 | 1.16564 | 0.631175 | 1.84678 | 0.115424 |
| large | xgboost_hist | 16 | 7.33451 | 2.76411 | 2.65348 | 0.165843 |
| medium | xgboost_hist | 16 | 5.19202 | 2.0332 | 2.55362 | 0.159601 |
| small | xgboost_hist | 16 | 1.58692 | 0.837749 | 1.89427 | 0.118392 |


## Memory growth trend (thread=1)
| model | smallest_samples | largest_samples | peak_mb_smallest | peak_mb_largest | approx_mb_per_1k_samples |
| --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 50000 | 140000 | 239.539 | 400.445 | 1.78785 |
| sklearn_hgb | 50000 | 140000 | 248.98 | 412.152 | 1.81302 |
| sklearn_hgb_fixed | 50000 | 140000 | 249.098 | 412.305 | 1.81341 |
| xgboost_hist | 50000 | 140000 | 284.715 | 386.629 | 1.13238 |


## Initial conclusion
- Best median runtime model: `sklearn_hgb_fixed`
- Least-performing median runtime model: `lightgbm_hist`
- All scenarios report explicit `r2_spread_for_scenario` to verify score parity while keeping matched hyperparameter values.
