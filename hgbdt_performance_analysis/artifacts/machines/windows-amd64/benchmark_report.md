# Histogram GBDT Regressor Benchmark Report

## Experiment controls
- Timeout budget per individual run: `8.0 s`
- Adaptive reduction factor after timeout: `0.5`
- Threads tested: `[1, 2, 4]`
- Dataset templates: `[{'name': 'small', 'start_n_samples': 50000, 'n_features': 40}, {'name': 'medium', 'start_n_samples': 140000, 'n_features': 80}, {'name': 'large', 'start_n_samples': 320000, 'n_features': 120}]`

## Overall ranking (lower is faster)
| model | median_total_s | mean_total_s | geo_mean_total_s | mean_peak_rss_mb | mean_r2 | max_r2_spread_for_matched_scenario |
| --- | --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 2.00393 | 2.1846 | 2.04189 | 171.386 | 0.776581 | 0.0300294 |
| sklearn_hgb_fixed | 3.15447 | 3.38237 | 3.22231 | 170.694 | 0.760867 | 0.0300294 |
| sklearn_hgb | 3.22632 | 3.38933 | 3.22618 | 170.95 | 0.760867 | 0.0300294 |
| xgboost_hist | 3.75925 | 3.93313 | 3.75272 | 188.359 | 0.776342 | 0.0300294 |


## Single-thread behavior
| dataset_name | model | n_samples | n_features | fit_seconds | predict_seconds | total_seconds | peak_rss_mb | r2 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 10000 | 120 | 3.34411 | 0.0292328 | 3.37975 | 159.48 | 0.674331 |
| large | sklearn_hgb | 10000 | 120 | 4.99797 | 0.0658344 | 5.06978 | 162.938 | 0.64901 |
| large | sklearn_hgb_fixed | 10000 | 120 | 5.13329 | 0.0654879 | 5.20865 | 162.875 | 0.64901 |
| large | xgboost_hist | 10000 | 120 | 5.68037 | 0.007936 | 5.69025 | 185.676 | 0.679039 |
| medium | lightgbm_hist | 35000 | 80 | 3.65708 | 0.0987128 | 3.7577 | 187.254 | 0.762334 |
| medium | sklearn_hgb_fixed | 35000 | 80 | 5.03684 | 0.208787 | 5.2501 | 182.223 | 0.745971 |
| medium | sklearn_hgb | 35000 | 80 | 5.06943 | 0.217113 | 5.28939 | 182.543 | 0.745971 |
| medium | xgboost_hist | 35000 | 80 | 6.01951 | 0.0240319 | 6.04918 | 211.051 | 0.761535 |
| small | lightgbm_hist | 50000 | 40 | 2.24268 | 0.135322 | 2.3844 | 166.602 | 0.893078 |
| small | sklearn_hgb_fixed | 50000 | 40 | 3.05668 | 0.238552 | 3.29954 | 166.012 | 0.88762 |
| small | sklearn_hgb | 50000 | 40 | 3.08927 | 0.250613 | 3.3465 | 166.488 | 0.88762 |
| small | xgboost_hist | 50000 | 40 | 3.69236 | 0.0334045 | 3.72673 | 175.133 | 0.893059 |


## Multi-thread scalability
| dataset_name | model | max_threads | fit_s_1_thread | fit_s_max_threads | speedup_vs_1_thread | parallel_efficiency |
| --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 4 | 3.34411 | 1.5156 | 2.20646 | 0.551614 |
| medium | lightgbm_hist | 4 | 3.65708 | 1.68038 | 2.17634 | 0.544084 |
| small | lightgbm_hist | 4 | 2.24268 | 1.12837 | 1.98754 | 0.496884 |
| large | sklearn_hgb | 4 | 4.99797 | 3.18147 | 1.57096 | 0.392741 |
| medium | sklearn_hgb | 4 | 5.06943 | 3.00903 | 1.68474 | 0.421185 |
| small | sklearn_hgb | 4 | 3.08927 | 1.92023 | 1.6088 | 0.402201 |
| large | sklearn_hgb_fixed | 4 | 5.13329 | 3.15005 | 1.62959 | 0.407398 |
| medium | sklearn_hgb_fixed | 4 | 5.03684 | 2.99732 | 1.68045 | 0.420112 |
| small | sklearn_hgb_fixed | 4 | 3.05668 | 1.95108 | 1.56666 | 0.391665 |
| large | xgboost_hist | 4 | 5.68037 | 3.80781 | 1.49177 | 0.372942 |
| medium | xgboost_hist | 4 | 6.01951 | 3.64151 | 1.65303 | 0.413257 |
| small | xgboost_hist | 4 | 3.69236 | 2.27968 | 1.61969 | 0.404922 |


## Memory growth trend (thread=1)
| model | smallest_samples | largest_samples | peak_mb_smallest | peak_mb_largest | approx_mb_per_1k_samples |
| --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 10000 | 50000 | 159.48 | 166.602 | 0.178027 |
| sklearn_hgb | 10000 | 50000 | 162.938 | 166.488 | 0.0887695 |
| sklearn_hgb_fixed | 10000 | 50000 | 162.875 | 166.012 | 0.078418 |
| xgboost_hist | 10000 | 50000 | 185.676 | 175.133 | -0.263574 |


## Initial conclusion
- Best median runtime model: `lightgbm_hist`
- Least-performing median runtime model: `xgboost_hist`
- All scenarios report explicit `r2_spread_for_scenario` to verify score parity while keeping matched hyperparameter values.
