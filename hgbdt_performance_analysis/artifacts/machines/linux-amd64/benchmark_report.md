# Histogram GBDT Regressor Benchmark Report

## Experiment controls
- Timeout budget per individual run: `8.0 s`
- Adaptive reduction factor after timeout: `0.5`
- Threads tested: `[1, 2, 4]`
- Dataset templates: `[{'name': 'small', 'start_n_samples': 50000, 'n_features': 40}, {'name': 'medium', 'start_n_samples': 140000, 'n_features': 80}, {'name': 'large', 'start_n_samples': 320000, 'n_features': 120}]`

## Overall ranking (lower is faster)
| model | median_total_s | mean_total_s | geo_mean_total_s | mean_peak_rss_mb | mean_r2 | max_r2_spread_for_matched_scenario |
| --- | --- | --- | --- | --- | --- | --- |
| sklearn_hgb_fixed | 1.92313 | 2.11238 | 1.98959 | 222.236 | 0.762274 | 0.0223186 |
| sklearn_hgb | 1.94402 | 2.12749 | 2.00324 | 222.24 | 0.762274 | 0.0223186 |
| lightgbm_hist | 1.99744 | 2.25408 | 2.05708 | 224.374 | 0.776988 | 0.0223186 |
| xgboost_hist | 2.91719 | 3.38622 | 3.11858 | 247.89 | 0.77509 | 0.0223186 |


## Single-thread behavior
| dataset_name | model | n_samples | n_features | fit_seconds | predict_seconds | total_seconds | peak_rss_mb | r2 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| large | sklearn_hgb | 20000 | 120 | 3.53508 | 0.0606632 | 3.60278 | 224.43 | 0.653232 |
| large | sklearn_hgb_fixed | 20000 | 120 | 3.56063 | 0.0607305 | 3.6311 | 223.922 | 0.653232 |
| large | lightgbm_hist | 20000 | 120 | 4.10209 | 0.0634631 | 4.17459 | 217.086 | 0.675551 |
| large | xgboost_hist | 20000 | 120 | 6.11291 | 0.0130154 | 6.13023 | 237.074 | 0.672265 |
| medium | sklearn_hgb_fixed | 35000 | 80 | 3.0972 | 0.0878441 | 3.18847 | 226.473 | 0.745971 |
| medium | sklearn_hgb | 35000 | 80 | 3.10915 | 0.087461 | 3.20013 | 225.961 | 0.745971 |
| medium | lightgbm_hist | 35000 | 80 | 3.63697 | 0.105271 | 3.74361 | 226.633 | 0.762334 |
| medium | xgboost_hist | 35000 | 80 | 4.97712 | 0.0210771 | 5.0041 | 255.82 | 0.758663 |
| small | sklearn_hgb_fixed | 50000 | 40 | 2.02901 | 0.112811 | 2.14502 | 209.902 | 0.88762 |
| small | sklearn_hgb | 50000 | 40 | 2.03693 | 0.114623 | 2.15918 | 209.797 | 0.88762 |
| small | lightgbm_hist | 50000 | 40 | 2.34885 | 0.150893 | 2.50042 | 216.109 | 0.893078 |
| small | xgboost_hist | 50000 | 40 | 2.86501 | 0.0286354 | 2.89392 | 222.844 | 0.894341 |


## Multi-thread scalability
| dataset_name | model | max_threads | fit_s_1_thread | fit_s_max_threads | speedup_vs_1_thread | parallel_efficiency |
| --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 4 | 4.10209 | 1.63468 | 2.50942 | 0.627354 |
| medium | lightgbm_hist | 4 | 3.63697 | 1.4905 | 2.4401 | 0.610026 |
| small | lightgbm_hist | 4 | 2.34885 | 1.05639 | 2.22348 | 0.555869 |
| large | sklearn_hgb | 4 | 3.53508 | 1.91506 | 1.84593 | 0.461483 |
| medium | sklearn_hgb | 4 | 3.10915 | 1.64593 | 1.88899 | 0.472248 |
| small | sklearn_hgb | 4 | 2.03693 | 1.15529 | 1.76313 | 0.440782 |
| large | sklearn_hgb_fixed | 4 | 3.56063 | 1.89763 | 1.87636 | 0.46909 |
| medium | sklearn_hgb_fixed | 4 | 3.0972 | 1.62841 | 1.90198 | 0.475495 |
| small | sklearn_hgb_fixed | 4 | 2.02901 | 1.19152 | 1.70288 | 0.42572 |
| large | xgboost_hist | 4 | 6.11291 | 3.66936 | 1.66593 | 0.416483 |
| medium | xgboost_hist | 4 | 4.97712 | 2.90089 | 1.71573 | 0.428931 |
| small | xgboost_hist | 4 | 2.86501 | 1.63721 | 1.74993 | 0.437483 |


## Memory growth trend (thread=1)
| model | smallest_samples | largest_samples | peak_mb_smallest | peak_mb_largest | approx_mb_per_1k_samples |
| --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 20000 | 50000 | 217.086 | 216.109 | -0.0325521 |
| sklearn_hgb | 20000 | 50000 | 224.43 | 209.797 | -0.48776 |
| sklearn_hgb_fixed | 20000 | 50000 | 223.922 | 209.902 | -0.467318 |
| xgboost_hist | 20000 | 50000 | 237.074 | 222.844 | -0.474349 |


## Initial conclusion
- Best median runtime model: `sklearn_hgb_fixed`
- Least-performing median runtime model: `xgboost_hist`
- All scenarios report explicit `r2_spread_for_scenario` to verify score parity while keeping matched hyperparameter values.
