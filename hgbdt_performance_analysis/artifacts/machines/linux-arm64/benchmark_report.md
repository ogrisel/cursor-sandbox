# Histogram GBDT Regressor Benchmark Report

## Experiment controls
- Timeout budget per individual run: `5.0 s`
- Adaptive reduction factor after timeout: `0.6`
- Threads tested: `[1, 2, 4, 8]`
- Dataset templates: `[{'name': 'small', 'start_n_samples': 12000, 'n_features': 24}, {'name': 'medium', 'start_n_samples': 180000, 'n_features': 120}]`

## Overall ranking (lower is faster)
| model | median_total_s | mean_total_s | geo_mean_total_s | mean_peak_rss_mb | mean_r2 | max_r2_spread_for_matched_scenario |
| --- | --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 1.64997 | 1.68138 | 1.67892 | 208.83 | 0.768005 | 0.0567536 |
| sklearn_hgb_fixed | 1.91473 | 1.91751 | 1.89735 | 202.802 | 0.736093 | 0.0567536 |
| sklearn_hgb | 1.94593 | 2.21005 | 2.08824 | 202.397 | 0.736093 | 0.0567536 |
| xgboost_hist | 2.08795 | 2.078 | 2.05547 | 220.798 | 0.767544 | 0.0567536 |


## Single-thread behavior
| dataset_name | model | n_samples | n_features | fit_seconds | predict_seconds | total_seconds | peak_rss_mb | r2 | fitted_trees | expected_trees | total_nodes | avg_nodes_per_tree |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| medium | lightgbm_hist | 1813 | 120 | 1.10252 | 0.00423214 | 1.60752 | 213.352 | 0.586641 | 220 | 220 | 11256 | 51.1636 |
| medium | sklearn_hgb_fixed | 1813 | 120 | 1.41 | 0.0047747 | 1.91607 | 204.477 | 0.529888 | 220 | 220 | 12398 | 56.3545 |
| medium | sklearn_hgb | 1813 | 120 | 1.47773 | 0.00482432 | 1.98947 | 204.5 | 0.529888 | 220 | 220 | 12398 | 56.3545 |
| medium | xgboost_hist | 1813 | 120 | 2.01045 | 0.00131731 | 2.51853 | 225.742 | 0.585335 | 220 | 220 | 11618 | 52.8091 |
| small | lightgbm_hist | 12000 | 24 | 0.538086 | 0.023739 | 1.60781 | 202.914 | 0.949369 | 220 | 220 | 13386 | 60.8455 |
| small | sklearn_hgb_fixed | 12000 | 24 | 0.713696 | 0.020405 | 1.93879 | 198.367 | 0.942299 | 220 | 220 | 13414 | 60.9727 |
| small | sklearn_hgb | 12000 | 24 | 0.721377 | 0.0203707 | 1.95742 | 198.371 | 0.942299 | 220 | 220 | 13414 | 60.9727 |
| small | xgboost_hist | 12000 | 24 | 0.82913 | 0.00566787 | 2.16854 | 211.551 | 0.949753 | 220 | 220 | 13390 | 60.8636 |


## Multi-thread scalability
| dataset_name | model | max_threads | fit_s_1_thread | fit_s_max_threads | speedup_vs_1_thread | parallel_efficiency |
| --- | --- | --- | --- | --- | --- | --- |
| medium | lightgbm_hist | 8 | 1.10252 | 1.18558 | 0.929944 | 0.116243 |
| small | lightgbm_hist | 8 | 0.538086 | 1.30255 | 0.413103 | 0.0516379 |
| medium | sklearn_hgb | 8 | 1.47773 | 3.03858 | 0.486324 | 0.0607906 |
| small | sklearn_hgb | 8 | 0.721377 | 3.05519 | 0.236115 | 0.0295144 |
| medium | sklearn_hgb_fixed | 8 | 1.41 | 0.700618 | 2.01251 | 0.251564 |
| small | sklearn_hgb_fixed | 8 | 0.713696 | 0.501788 | 1.42231 | 0.177788 |
| medium | xgboost_hist | 8 | 2.01045 | 0.93006 | 2.16163 | 0.270204 |
| small | xgboost_hist | 8 | 0.82913 | 0.410092 | 2.02181 | 0.252726 |


## Memory growth trend (thread=1)
| model | smallest_samples | largest_samples | peak_mb_smallest | peak_mb_largest | approx_mb_per_1k_samples |
| --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 1813 | 12000 | 213.352 | 202.914 | -1.02459 |
| sklearn_hgb | 1813 | 12000 | 204.5 | 198.371 | -0.60164 |
| sklearn_hgb_fixed | 1813 | 12000 | 204.477 | 198.367 | -0.599723 |
| xgboost_hist | 1813 | 12000 | 225.742 | 211.551 | -1.39309 |


## Initial conclusion
- Best median runtime model: `lightgbm_hist`
- Least-performing median runtime model: `xgboost_hist`
- All scenarios report explicit `r2_spread_for_scenario` to verify score parity while keeping matched hyperparameter values.
