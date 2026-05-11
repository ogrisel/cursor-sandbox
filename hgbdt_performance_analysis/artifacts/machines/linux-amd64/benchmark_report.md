# Histogram GBDT Regressor Benchmark Report

## Experiment controls
- Timeout budget per individual run: `12.0 s`
- Adaptive reduction factor after timeout: `0.5`
- Threads tested: `[1, 2, 4, 8, 16]`
- Dataset templates: `[{'name': 'small', 'start_n_samples': 50000, 'n_features': 40}, {'name': 'medium', 'start_n_samples': 140000, 'n_features': 80}, {'name': 'large', 'start_n_samples': 320000, 'n_features': 120}]`

## Overall ranking (lower is faster)
| model | median_total_s | mean_total_s | geo_mean_total_s | mean_peak_rss_mb | mean_r2 | max_r2_spread_for_matched_scenario |
| --- | --- | --- | --- | --- | --- | --- |
| sklearn_hgb_fixed | 0.960876 | 1.05277 | 1.034 | 214.561 | 0.727475 | 0.033623 |
| sklearn_hgb | 1.48579 | 3.6816 | 2.31187 | 215.266 | 0.727475 | 0.033623 |
| lightgbm_hist | 1.64637 | 1.85139 | 1.51112 | 218.714 | 0.751541 | 0.033623 |
| xgboost_hist | 1.73268 | 1.82288 | 1.77202 | 234.114 | 0.752159 | 0.033623 |


## Single-thread behavior
| dataset_name | model | n_samples | n_features | fit_seconds | predict_seconds | total_seconds | peak_rss_mb | r2 | fitted_trees | expected_trees | total_nodes | avg_nodes_per_tree |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| large | sklearn_hgb_fixed | 2500 | 120 | 1.51083 | 0.00929631 | 1.52998 | 211.395 | 0.603268 | 220 | 220 | 12804 | 58.2 |
| large | sklearn_hgb | 2500 | 120 | 1.52587 | 0.00943481 | 1.54157 | 211.328 | 0.603268 | 220 | 220 | 12804 | 58.2 |
| large | lightgbm_hist | 2500 | 120 | 1.66456 | 0.00892283 | 1.68162 | 217.066 | 0.634649 | 220 | 220 | 12342 | 56.1 |
| large | xgboost_hist | 2500 | 120 | 2.9774 | 0.00251769 | 2.98897 | 234.57 | 0.636891 | 220 | 220 | 12378 | 56.2636 |
| medium | sklearn_hgb | 4375 | 80 | 1.33509 | 0.0131267 | 1.35354 | 208.523 | 0.687753 | 220 | 220 | 13340 | 60.6364 |
| medium | sklearn_hgb_fixed | 4375 | 80 | 1.39866 | 0.0131069 | 1.41607 | 208.902 | 0.687753 | 220 | 220 | 13340 | 60.6364 |
| medium | lightgbm_hist | 4375 | 80 | 1.44101 | 0.0146824 | 1.46252 | 212.895 | 0.720404 | 220 | 220 | 13190 | 59.9545 |
| medium | xgboost_hist | 4375 | 80 | 2.3957 | 0.00349637 | 2.4086 | 224.09 | 0.719562 | 220 | 220 | 13198 | 59.9909 |
| small | sklearn_hgb | 25000 | 40 | 1.41925 | 0.0586898 | 1.48579 | 220.566 | 0.891404 | 220 | 220 | 13420 | 61 |
| small | sklearn_hgb_fixed | 25000 | 40 | 1.42159 | 0.0580693 | 1.48659 | 220.562 | 0.891404 | 220 | 220 | 13420 | 61 |
| small | lightgbm_hist | 25000 | 40 | 1.561 | 0.0766276 | 1.64637 | 223.293 | 0.89957 | 220 | 220 | 13420 | 61 |
| small | xgboost_hist | 25000 | 40 | 2.13201 | 0.0149826 | 2.15715 | 232.168 | 0.900025 | 220 | 220 | 13420 | 61 |


## Multi-thread scalability
| dataset_name | model | max_threads | fit_s_1_thread | fit_s_max_threads | speedup_vs_1_thread | parallel_efficiency |
| --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 16 | 1.66456 | 3.65439 | 0.455495 | 0.0284685 |
| medium | lightgbm_hist | 16 | 1.44101 | 3.85009 | 0.37428 | 0.0233925 |
| small | lightgbm_hist | 16 | 1.561 | 4.18671 | 0.372846 | 0.0233029 |
| large | sklearn_hgb | 16 | 1.52587 | 9.22585 | 0.16539 | 0.0103369 |
| medium | sklearn_hgb | 16 | 1.33509 | 9.87433 | 0.135208 | 0.00845053 |
| small | sklearn_hgb | 16 | 1.41925 | 10.2818 | 0.138034 | 0.00862713 |
| large | sklearn_hgb_fixed | 16 | 1.51083 | 0.980294 | 1.5412 | 0.0963251 |
| medium | sklearn_hgb_fixed | 16 | 1.39866 | 0.914233 | 1.52988 | 0.0956174 |
| small | sklearn_hgb_fixed | 16 | 1.42159 | 0.926503 | 1.53436 | 0.0958975 |
| large | xgboost_hist | 16 | 2.9774 | 2.0446 | 1.45623 | 0.0910141 |
| medium | xgboost_hist | 16 | 2.3957 | 1.7199 | 1.39293 | 0.087058 |
| small | xgboost_hist | 16 | 2.13201 | 1.35468 | 1.57381 | 0.0983631 |


## Memory growth trend (thread=1)
| model | smallest_samples | largest_samples | peak_mb_smallest | peak_mb_largest | approx_mb_per_1k_samples |
| --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 2500 | 25000 | 217.066 | 223.293 | 0.276736 |
| sklearn_hgb | 2500 | 25000 | 211.328 | 220.566 | 0.41059 |
| sklearn_hgb_fixed | 2500 | 25000 | 211.395 | 220.562 | 0.407465 |
| xgboost_hist | 2500 | 25000 | 234.57 | 232.168 | -0.106771 |


## Initial conclusion
- Best median runtime model: `sklearn_hgb_fixed`
- Least-performing median runtime model: `xgboost_hist`
- All scenarios report explicit `r2_spread_for_scenario` to verify score parity while keeping matched hyperparameter values.
