# Histogram GBDT Regressor Benchmark Report

## Experiment controls
- Timeout budget per individual run: `5.0 s`
- Adaptive reduction factor after timeout: `0.6`
- Threads tested: `[1, 2, 3, 6]`
- Dataset templates: `[{'name': 'small', 'start_n_samples': 12000, 'n_features': 24}, {'name': 'medium', 'start_n_samples': 180000, 'n_features': 120}]`

## Overall ranking (lower is faster)
| model | median_total_s | mean_total_s | geo_mean_total_s | mean_peak_rss_mb | mean_r2 | max_r2_spread_for_matched_scenario |
| --- | --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 1.84455 | 1.85211 | 1.84516 | 182.158 | 0.710231 | 0.0740629 |
| sklearn_hgb_fixed | 1.88128 | 1.85019 | 1.84083 | 175.977 | 0.666158 | 0.0740629 |
| xgboost_hist | 1.92165 | 1.97454 | 1.96473 | 188.256 | 0.694928 | 0.0740629 |
| sklearn_hgb | 1.96387 | 2.13114 | 2.08459 | 174.801 | 0.666158 | 0.0740629 |


## Single-thread behavior
| dataset_name | model | n_samples | n_features | fit_seconds | predict_seconds | total_seconds | peak_rss_mb | r2 | fitted_trees | expected_trees | total_nodes | avg_nodes_per_tree |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| medium | lightgbm_hist | 652 | 120 | 0.320248 | 0.00181265 | 1.80279 | 204.031 | 0.508565 | 220 | 220 | 6114 | 27.7909 |
| medium | sklearn_hgb_fixed | 652 | 120 | 0.642184 | 0.00219625 | 1.81158 | 180.594 | 0.434502 | 220 | 220 | 7040 | 32 |
| medium | sklearn_hgb | 652 | 120 | 0.676866 | 0.00250912 | 1.9382 | 180.469 | 0.434502 | 220 | 220 | 7040 | 32 |
| medium | xgboost_hist | 652 | 120 | 0.917093 | 0.000409282 | 2.34788 | 204.094 | 0.47647 | 220 | 220 | 6168 | 28.0364 |
| small | sklearn_hgb | 2592 | 24 | 0.541923 | 0.00704192 | 1.6309 | 171.109 | 0.897813 | 220 | 220 | 10976 | 49.8909 |
| small | sklearn_hgb_fixed | 2592 | 24 | 0.52598 | 0.00777457 | 1.63378 | 171.719 | 0.897813 | 220 | 220 | 10976 | 49.8909 |
| small | lightgbm_hist | 2592 | 24 | 0.304242 | 0.0068985 | 1.728 | 179 | 0.911898 | 220 | 220 | 10082 | 45.8273 |
| small | xgboost_hist | 2592 | 24 | 0.491953 | 0.00224297 | 1.98642 | 189.078 | 0.913386 | 220 | 220 | 10162 | 46.1909 |


## Multi-thread scalability
| dataset_name | model | max_threads | fit_s_1_thread | fit_s_max_threads | speedup_vs_1_thread | parallel_efficiency |
| --- | --- | --- | --- | --- | --- | --- |
| medium | lightgbm_hist | 6 | 0.320248 | 1.09777 | 0.291726 | 0.048621 |
| small | lightgbm_hist | 6 | 0.304242 | 1.63704 | 0.185849 | 0.0309748 |
| medium | sklearn_hgb | 6 | 0.676866 | 1.99884 | 0.33863 | 0.0564383 |
| small | sklearn_hgb | 6 | 0.541923 | 2.47874 | 0.218629 | 0.0364381 |
| medium | sklearn_hgb_fixed | 6 | 0.642184 | 0.754917 | 0.850668 | 0.141778 |
| small | sklearn_hgb_fixed | 6 | 0.52598 | 0.576645 | 0.912138 | 0.152023 |
| medium | xgboost_hist | 6 | 0.917093 | 1.42833 | 0.642073 | 0.107012 |
| small | xgboost_hist | 6 | 0.491953 | 1.26272 | 0.389597 | 0.0649328 |


## Memory growth trend (thread=1)
| model | smallest_samples | largest_samples | peak_mb_smallest | peak_mb_largest | approx_mb_per_1k_samples |
| --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 652 | 2592 | 204.031 | 179 | -12.9027 |
| sklearn_hgb | 652 | 2592 | 180.469 | 171.109 | -4.82442 |
| sklearn_hgb_fixed | 652 | 2592 | 180.594 | 171.719 | -4.57474 |
| xgboost_hist | 652 | 2592 | 204.094 | 189.078 | -7.74001 |


## Initial conclusion
- Best median runtime model: `lightgbm_hist`
- Least-performing median runtime model: `sklearn_hgb`
- All scenarios report explicit `r2_spread_for_scenario` to verify score parity while keeping matched hyperparameter values.
