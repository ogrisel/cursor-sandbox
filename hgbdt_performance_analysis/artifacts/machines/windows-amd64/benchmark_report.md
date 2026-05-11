# Histogram GBDT Regressor Benchmark Report

## Experiment controls
- Timeout budget per individual run: `12.0 s`
- Adaptive reduction factor after timeout: `0.5`
- Threads tested: `[1, 2, 4, 8, 16]`
- Dataset templates: `[{'name': 'small', 'start_n_samples': 50000, 'n_features': 40}, {'name': 'medium', 'start_n_samples': 140000, 'n_features': 80}, {'name': 'large', 'start_n_samples': 320000, 'n_features': 120}]`

## Overall ranking (lower is faster)
| model | median_total_s | mean_total_s | geo_mean_total_s | mean_peak_rss_mb | mean_r2 | max_r2_spread_for_matched_scenario |
| --- | --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 2.67335 | 2.91672 | 2.58054 | 234.674 | 0.793002 | 0.0191276 |
| sklearn_hgb_fixed | 3.45566 | 3.64564 | 3.32434 | 229.199 | 0.782765 | 0.0191276 |
| sklearn_hgb | 3.74964 | 3.80733 | 3.51483 | 230.688 | 0.782765 | 0.0191276 |
| xgboost_hist | 4.55244 | 4.60874 | 4.14193 | 248.485 | 0.793471 | 0.0191276 |


## Single-thread behavior
| dataset_name | model | n_samples | n_features | fit_seconds | predict_seconds | total_seconds | peak_rss_mb | r2 | fitted_trees | expected_trees | total_nodes | avg_nodes_per_tree |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 40000 | 120 | 6.17854 | 0.126197 | 6.31172 | 248.164 | 0.692337 | 220 | 220 | 13420 | 61 |
| large | sklearn_hgb | 40000 | 120 | 7.1055 | 0.293803 | 7.40226 | 243.629 | 0.675577 | 220 | 220 | 13420 | 61 |
| large | sklearn_hgb_fixed | 40000 | 120 | 7.15107 | 0.322291 | 7.47871 | 243.055 | 0.675577 | 220 | 220 | 13420 | 61 |
| large | xgboost_hist | 40000 | 120 | 8.70489 | 0.0316212 | 8.73677 | 282.773 | 0.694704 | 220 | 220 | 13420 | 61 |
| medium | lightgbm_hist | 70000 | 80 | 5.91744 | 0.216283 | 6.13959 | 257.242 | 0.79359 | 220 | 220 | 13420 | 61 |
| medium | sklearn_hgb_fixed | 70000 | 80 | 6.3533 | 0.414413 | 6.76972 | 251.227 | 0.785099 | 220 | 220 | 13420 | 61 |
| medium | sklearn_hgb | 70000 | 80 | 6.38825 | 0.413309 | 6.80961 | 251.02 | 0.785099 | 220 | 220 | 13420 | 61 |
| medium | xgboost_hist | 70000 | 80 | 7.78988 | 0.0523864 | 7.85005 | 278.559 | 0.793602 | 220 | 220 | 13420 | 61 |
| small | lightgbm_hist | 50000 | 40 | 2.45082 | 0.14776 | 2.60582 | 192.535 | 0.893078 | 220 | 220 | 13420 | 61 |
| small | sklearn_hgb | 50000 | 40 | 2.8241 | 0.271844 | 3.10492 | 191.859 | 0.88762 | 220 | 220 | 13420 | 61 |
| small | sklearn_hgb_fixed | 50000 | 40 | 2.83614 | 0.27474 | 3.11567 | 192.098 | 0.88762 | 220 | 220 | 13420 | 61 |
| small | xgboost_hist | 50000 | 40 | 3.42834 | 0.0352257 | 3.4662 | 201.531 | 0.893059 | 220 | 220 | 13420 | 61 |


## Multi-thread scalability
| dataset_name | model | max_threads | fit_s_1_thread | fit_s_max_threads | speedup_vs_1_thread | parallel_efficiency |
| --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 16 | 6.17854 | 2.79495 | 2.21061 | 0.138163 |
| medium | lightgbm_hist | 16 | 5.91744 | 2.72668 | 2.1702 | 0.135638 |
| small | lightgbm_hist | 16 | 2.45082 | 1.32633 | 1.84782 | 0.115489 |
| large | sklearn_hgb | 16 | 7.1055 | 4.19273 | 1.69472 | 0.10592 |
| medium | sklearn_hgb | 16 | 6.38825 | 3.79622 | 1.68279 | 0.105175 |
| small | sklearn_hgb | 16 | 2.8241 | 2.20205 | 1.28249 | 0.0801554 |
| large | sklearn_hgb_fixed | 16 | 7.15107 | 3.66667 | 1.95029 | 0.121893 |
| medium | sklearn_hgb_fixed | 16 | 6.3533 | 3.29303 | 1.92932 | 0.120582 |
| small | sklearn_hgb_fixed | 16 | 2.83614 | 1.66094 | 1.70755 | 0.106722 |
| large | xgboost_hist | 16 | 8.70489 | 5.25525 | 1.65642 | 0.103526 |
| medium | xgboost_hist | 16 | 7.78988 | 4.52119 | 1.72297 | 0.107686 |
| small | xgboost_hist | 16 | 3.42834 | 1.96077 | 1.74847 | 0.109279 |


## Memory growth trend (thread=1)
| model | smallest_samples | largest_samples | peak_mb_smallest | peak_mb_largest | approx_mb_per_1k_samples |
| --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 40000 | 70000 | 248.164 | 257.242 | 0.302604 |
| sklearn_hgb | 40000 | 70000 | 243.629 | 251.02 | 0.246354 |
| sklearn_hgb_fixed | 40000 | 70000 | 243.055 | 251.227 | 0.272396 |
| xgboost_hist | 40000 | 70000 | 282.773 | 278.559 | -0.140495 |


## Initial conclusion
- Best median runtime model: `lightgbm_hist`
- Least-performing median runtime model: `xgboost_hist`
- All scenarios report explicit `r2_spread_for_scenario` to verify score parity while keeping matched hyperparameter values.
