# Histogram GBDT Regressor Benchmark Report

## Experiment controls
- Timeout budget per individual run: `8.0 s`
- Adaptive reduction factor after timeout: `0.5`
- Threads tested: `[1, 2, 4]`
- Dataset templates: `[{'name': 'small', 'start_n_samples': 50000, 'n_features': 40}, {'name': 'medium', 'start_n_samples': 140000, 'n_features': 80}, {'name': 'large', 'start_n_samples': 320000, 'n_features': 120}]`

## Overall ranking (lower is faster)
| model | median_total_s | mean_total_s | geo_mean_total_s | mean_peak_rss_mb | mean_r2 | max_r2_spread_for_matched_scenario |
| --- | --- | --- | --- | --- | --- | --- |
| sklearn_hgb_fixed | 2.45241 | 2.49236 | 2.20753 | 269.905 | 0.782765 | 0.0177437 |
| lightgbm_hist | 2.56232 | 2.60565 | 2.44369 | 294.285 | 0.793002 | 0.0177437 |
| sklearn_hgb | 2.60104 | 2.97779 | 2.83392 | 263.641 | 0.782765 | 0.0177437 |
| xgboost_hist | 3.08697 | 3.22406 | 2.97614 | 310.436 | 0.793637 | 0.0177437 |


## Single-thread behavior
| dataset_name | model | n_samples | n_features | fit_seconds | predict_seconds | total_seconds | peak_rss_mb | r2 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 40000 | 120 | 3.94735 | 0.0821558 | 4.04082 | 324.297 | 0.692337 |
| large | sklearn_hgb_fixed | 40000 | 120 | 4.27555 | 0.107729 | 4.41319 | 303.984 | 0.675577 |
| large | sklearn_hgb | 40000 | 120 | 4.30493 | 0.107974 | 4.41869 | 304.469 | 0.675577 |
| large | xgboost_hist | 40000 | 120 | 5.63189 | 0.0154145 | 5.67812 | 369.781 | 0.69332 |
| medium | lightgbm_hist | 70000 | 80 | 3.90558 | 0.127916 | 4.0658 | 347.141 | 0.79359 |
| medium | sklearn_hgb_fixed | 70000 | 80 | 4.21966 | 0.142364 | 4.37089 | 300.438 | 0.785099 |
| medium | sklearn_hgb | 70000 | 80 | 4.27908 | 0.124141 | 4.4955 | 300.609 | 0.785099 |
| medium | xgboost_hist | 70000 | 80 | 4.77284 | 0.0288852 | 4.80729 | 348.906 | 0.793248 |
| small | lightgbm_hist | 50000 | 40 | 2.28441 | 0.0949423 | 2.39796 | 225.5 | 0.893078 |
| small | sklearn_hgb | 50000 | 40 | 2.35941 | 0.0907106 | 2.45389 | 206.391 | 0.88762 |
| small | xgboost_hist | 50000 | 40 | 2.64663 | 0.0213176 | 2.75577 | 218.641 | 0.894341 |
| small | sklearn_hgb_fixed | 50000 | 40 | 2.91092 | 0.0950831 | 3.0386 | 206.156 | 0.88762 |


## Multi-thread scalability
| dataset_name | model | max_threads | fit_s_1_thread | fit_s_max_threads | speedup_vs_1_thread | parallel_efficiency |
| --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 4 | 3.94735 | 2.40445 | 1.64168 | 0.410421 |
| medium | lightgbm_hist | 4 | 3.90558 | 2.46805 | 1.58246 | 0.395614 |
| small | lightgbm_hist | 4 | 2.28441 | 1.32828 | 1.71983 | 0.429958 |
| large | sklearn_hgb | 4 | 4.30493 | 2.60545 | 1.65228 | 0.413069 |
| medium | sklearn_hgb | 4 | 4.27908 | 2.46367 | 1.73687 | 0.434217 |
| small | sklearn_hgb | 4 | 2.35941 | 1.52807 | 1.54405 | 0.386012 |
| large | sklearn_hgb_fixed | 4 | 4.27555 | 1.69393 | 2.52404 | 0.631011 |
| medium | sklearn_hgb_fixed | 4 | 4.21966 | 1.58416 | 2.66365 | 0.665913 |
| small | sklearn_hgb_fixed | 4 | 2.91092 | 0.973591 | 2.98988 | 0.74747 |
| large | xgboost_hist | 4 | 5.63189 | 2.99121 | 1.88281 | 0.470703 |
| medium | xgboost_hist | 4 | 4.77284 | 2.68675 | 1.77643 | 0.444109 |
| small | xgboost_hist | 4 | 2.64663 | 1.46812 | 1.80273 | 0.450683 |


## Memory growth trend (thread=1)
| model | smallest_samples | largest_samples | peak_mb_smallest | peak_mb_largest | approx_mb_per_1k_samples |
| --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 40000 | 70000 | 324.297 | 347.141 | 0.761458 |
| sklearn_hgb | 40000 | 70000 | 304.469 | 300.609 | -0.128646 |
| sklearn_hgb_fixed | 40000 | 70000 | 303.984 | 300.438 | -0.118229 |
| xgboost_hist | 40000 | 70000 | 369.781 | 348.906 | -0.695833 |


## Initial conclusion
- Best median runtime model: `sklearn_hgb_fixed`
- Least-performing median runtime model: `xgboost_hist`
- All scenarios report explicit `r2_spread_for_scenario` to verify score parity while keeping matched hyperparameter values.
