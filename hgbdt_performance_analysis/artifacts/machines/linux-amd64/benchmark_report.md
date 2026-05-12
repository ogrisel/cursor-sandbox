# Histogram GBDT Regressor Benchmark Report

## Experiment controls
- Timeout budget per individual run: `5.0 s`
- Adaptive reduction factor after timeout: `0.6`
- Threads tested: `[1, 2, 4, 8]`
- Dataset templates: `[{'name': 'small', 'start_n_samples': 12000, 'n_features': 24}, {'name': 'medium', 'start_n_samples': 180000, 'n_features': 120}]`

## Overall ranking (lower is faster)
| model | median_total_s | mean_total_s | geo_mean_total_s | mean_peak_rss_mb | mean_r2 | max_r2_spread_for_matched_scenario |
| --- | --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 0.632248 | 0.899162 | 0.726981 | 211.02 | 0.768005 | 0.0567536 |
| sklearn_hgb_fixed | 0.665418 | 0.668259 | 0.6363 | 205.457 | 0.736093 | 0.0567536 |
| sklearn_hgb | 0.74547 | 1.46936 | 1.02221 | 205.727 | 0.736093 | 0.0567536 |
| xgboost_hist | 1.06394 | 1.10903 | 0.987894 | 222.743 | 0.767544 | 0.0567536 |


## Single-thread behavior
| dataset_name | model | n_samples | n_features | fit_seconds | predict_seconds | total_seconds | peak_rss_mb | r2 | fitted_trees | expected_trees | total_nodes | avg_nodes_per_tree |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| medium | sklearn_hgb_fixed | 1813 | 120 | 1.12445 | 0.00596868 | 1.13629 | 207.645 | 0.529888 | 220 | 220 | 12398 | 56.3545 |
| medium | sklearn_hgb | 1813 | 120 | 1.12134 | 0.0058824 | 1.13714 | 207.434 | 0.529888 | 220 | 220 | 12398 | 56.3545 |
| medium | lightgbm_hist | 1813 | 120 | 1.21781 | 0.00560249 | 1.22555 | 216.164 | 0.586641 | 220 | 220 | 11256 | 51.1636 |
| medium | xgboost_hist | 1813 | 120 | 2.16768 | 0.00171119 | 2.17882 | 229.254 | 0.585335 | 220 | 220 | 11618 | 52.8091 |
| small | lightgbm_hist | 12000 | 24 | 0.571655 | 0.0284564 | 0.607461 | 205.492 | 0.949369 | 220 | 220 | 13386 | 60.8455 |
| small | sklearn_hgb_fixed | 12000 | 24 | 0.589467 | 0.0269552 | 0.619455 | 201.59 | 0.942299 | 220 | 220 | 13414 | 60.9727 |
| small | sklearn_hgb | 12000 | 24 | 0.609867 | 0.0251385 | 0.63988 | 202.016 | 0.942299 | 220 | 220 | 13414 | 60.9727 |
| small | xgboost_hist | 12000 | 24 | 0.824292 | 0.00577625 | 0.839507 | 210.168 | 0.949753 | 220 | 220 | 13390 | 60.8636 |


## Multi-thread scalability
| dataset_name | model | max_threads | fit_s_1_thread | fit_s_max_threads | speedup_vs_1_thread | parallel_efficiency |
| --- | --- | --- | --- | --- | --- | --- |
| medium | lightgbm_hist | 8 | 1.21781 | 1.78413 | 0.682582 | 0.0853227 |
| small | lightgbm_hist | 8 | 0.571655 | 1.76078 | 0.324661 | 0.0405826 |
| medium | sklearn_hgb | 8 | 1.12134 | 3.68722 | 0.304115 | 0.0380143 |
| small | sklearn_hgb | 8 | 0.609867 | 3.83703 | 0.158943 | 0.0198678 |
| medium | sklearn_hgb_fixed | 8 | 1.12445 | 0.746785 | 1.50572 | 0.188215 |
| small | sklearn_hgb_fixed | 8 | 0.589467 | 0.445014 | 1.3246 | 0.165575 |
| medium | xgboost_hist | 8 | 2.16768 | 1.42194 | 1.52445 | 0.190556 |
| small | xgboost_hist | 8 | 0.824292 | 0.638909 | 1.29015 | 0.161269 |


## Memory growth trend (thread=1)
| model | smallest_samples | largest_samples | peak_mb_smallest | peak_mb_largest | approx_mb_per_1k_samples |
| --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 1813 | 12000 | 216.164 | 205.492 | -1.0476 |
| sklearn_hgb | 1813 | 12000 | 207.434 | 202.016 | -0.531851 |
| sklearn_hgb_fixed | 1813 | 12000 | 207.645 | 201.59 | -0.594354 |
| xgboost_hist | 1813 | 12000 | 229.254 | 210.168 | -1.87356 |


## Initial conclusion
- Best median runtime model: `lightgbm_hist`
- Least-performing median runtime model: `xgboost_hist`
- All scenarios report explicit `r2_spread_for_scenario` to verify score parity while keeping matched hyperparameter values.
