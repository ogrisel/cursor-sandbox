# Histogram GBDT Regressor Benchmark Report

## Experiment controls
- Timeout budget per individual run: `5.0 s`
- Adaptive reduction factor after timeout: `0.6`
- Threads tested: `[1, 2, 4, 8]`
- Dataset templates: `[{'name': 'small', 'start_n_samples': 12000, 'n_features': 24}, {'name': 'medium', 'start_n_samples': 180000, 'n_features': 120}]`

## Overall ranking (lower is faster)
| model | median_total_s | mean_total_s | geo_mean_total_s | mean_peak_rss_mb | mean_r2 | max_r2_spread_for_matched_scenario |
| --- | --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 0.715087 | 0.764675 | 0.703527 | 170.92 | 0.768005 | 0.0760385 |
| sklearn_hgb_fixed | 1.26848 | 1.29148 | 1.1784 | 166.865 | 0.736093 | 0.0760385 |
| sklearn_hgb | 1.34976 | 1.39109 | 1.28085 | 167.268 | 0.736093 | 0.0760385 |
| xgboost_hist | 1.57674 | 1.60683 | 1.43937 | 182.967 | 0.772938 | 0.0760385 |


## Single-thread behavior
| dataset_name | model | n_samples | n_features | fit_seconds | predict_seconds | total_seconds | peak_rss_mb | r2 | fitted_trees | expected_trees | total_nodes | avg_nodes_per_tree |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| medium | lightgbm_hist | 1813 | 120 | 1.53138 | 0.0067066 | 1.54183 | 176.395 | 0.586641 | 220 | 220 | 11256 | 51.1636 |
| medium | sklearn_hgb_fixed | 1813 | 120 | 2.27142 | 0.0102986 | 2.28855 | 169.184 | 0.529888 | 220 | 220 | 12398 | 56.3545 |
| medium | sklearn_hgb | 1813 | 120 | 2.28688 | 0.0106524 | 2.3038 | 168.457 | 0.529888 | 220 | 220 | 12398 | 56.3545 |
| medium | xgboost_hist | 1813 | 120 | 2.81441 | 0.0021976 | 2.82163 | 194.047 | 0.593432 | 220 | 220 | 11426 | 51.9364 |
| small | lightgbm_hist | 12000 | 24 | 0.651413 | 0.0332149 | 0.689691 | 164.77 | 0.949369 | 220 | 220 | 13386 | 60.8455 |
| small | sklearn_hgb_fixed | 12000 | 24 | 0.879062 | 0.05476 | 0.937006 | 164.199 | 0.942299 | 220 | 220 | 13414 | 60.9727 |
| small | sklearn_hgb | 12000 | 24 | 0.87922 | 0.0609556 | 0.944556 | 163.969 | 0.942299 | 220 | 220 | 13414 | 60.9727 |
| small | xgboost_hist | 12000 | 24 | 1.13572 | 0.0082345 | 1.14572 | 169.98 | 0.948866 | 220 | 220 | 13394 | 60.8818 |


## Multi-thread scalability
| dataset_name | model | max_threads | fit_s_1_thread | fit_s_max_threads | speedup_vs_1_thread | parallel_efficiency |
| --- | --- | --- | --- | --- | --- | --- |
| medium | lightgbm_hist | 8 | 1.53138 | 0.827019 | 1.85168 | 0.23146 |
| small | lightgbm_hist | 8 | 0.651413 | 0.49985 | 1.30322 | 0.162902 |
| medium | sklearn_hgb | 8 | 2.28688 | 2.00169 | 1.14248 | 0.14281 |
| small | sklearn_hgb | 8 | 0.87922 | 1.1069 | 0.794308 | 0.0992884 |
| medium | sklearn_hgb_fixed | 8 | 2.27142 | 1.64071 | 1.38442 | 0.173052 |
| small | sklearn_hgb_fixed | 8 | 0.879062 | 0.743279 | 1.18268 | 0.147835 |
| medium | xgboost_hist | 8 | 2.81441 | 2.00325 | 1.40492 | 0.175615 |
| small | xgboost_hist | 8 | 1.13572 | 0.841083 | 1.35031 | 0.168789 |


## Memory growth trend (thread=1)
| model | smallest_samples | largest_samples | peak_mb_smallest | peak_mb_largest | approx_mb_per_1k_samples |
| --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 1813 | 12000 | 176.395 | 164.77 | -1.14116 |
| sklearn_hgb | 1813 | 12000 | 168.457 | 163.969 | -0.440589 |
| sklearn_hgb_fixed | 1813 | 12000 | 169.184 | 164.199 | -0.489288 |
| xgboost_hist | 1813 | 12000 | 194.047 | 169.98 | -2.36246 |


## Initial conclusion
- Best median runtime model: `lightgbm_hist`
- Least-performing median runtime model: `xgboost_hist`
- All scenarios report explicit `r2_spread_for_scenario` to verify score parity while keeping matched hyperparameter values.
