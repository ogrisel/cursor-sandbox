# Histogram GBDT Regressor Benchmark Report

## Experiment controls
- Timeout budget per individual run: `5.0 s`
- Adaptive reduction factor after timeout: `0.6`
- Threads tested: `[1, 4, 16]`
- Dataset templates: `[{'name': 'small', 'start_n_samples': 12000, 'n_features': 24}, {'name': 'medium', 'start_n_samples': 36000, 'n_features': 48}, {'name': 'large', 'start_n_samples': 90000, 'n_features': 80}]`

## Overall ranking (lower is faster)
| model | median_total_s | mean_total_s | geo_mean_total_s | mean_peak_rss_mb | mean_r2 | max_r2_spread_for_matched_scenario |
| --- | --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 1.30443 | 2.32277 | 1.56424 | 244.972 | 0.866003 | 0.00991913 |
| sklearn_hgb_fixed | 1.5764 | 2.60221 | 1.90973 | 234.82 | 0.857486 | 0.00991913 |
| xgboost_hist | 1.99379 | 3.34372 | 2.37717 | 248.96 | 0.864913 | 0.00991913 |
| sklearn_hgb | 2.07859 | 2.82503 | 2.17573 | 236.304 | 0.857486 | 0.00991913 |


## Single-thread behavior
| dataset_name | model | n_samples | n_features | fit_seconds | predict_seconds | total_seconds | peak_rss_mb | r2 | fitted_trees | expected_trees | total_nodes | avg_nodes_per_tree |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 90000 | 80 | 7.18446 | 0.280221 | 7.47445 | 325.52 | 0.774775 | 220 | 220 | 13420 | 61 |
| large | sklearn_hgb_fixed | 90000 | 80 | 7.14226 | 0.642076 | 7.7886 | 303.379 | 0.766213 | 220 | 220 | 13420 | 61 |
| large | sklearn_hgb | 90000 | 80 | 7.16068 | 0.64175 | 7.81056 | 304.594 | 0.766213 | 220 | 220 | 13420 | 61 |
| large | xgboost_hist | 90000 | 80 | 9.62937 | 0.0715382 | 9.70105 | 335.148 | 0.773861 | 220 | 220 | 13420 | 61 |
| medium | lightgbm_hist | 36000 | 48 | 2.43689 | 0.111288 | 2.54953 | 218.602 | 0.873865 | 220 | 220 | 13420 | 61 |
| medium | sklearn_hgb_fixed | 36000 | 48 | 2.65263 | 0.226375 | 2.87915 | 214.793 | 0.863946 | 220 | 220 | 13420 | 61 |
| medium | sklearn_hgb | 36000 | 48 | 2.91156 | 0.226825 | 3.14587 | 215.281 | 0.863946 | 220 | 220 | 13420 | 61 |
| medium | xgboost_hist | 36000 | 48 | 3.49808 | 0.0277468 | 3.52734 | 231.031 | 0.873224 | 220 | 220 | 13420 | 61 |
| small | lightgbm_hist | 12000 | 24 | 0.754449 | 0.0375776 | 0.792809 | 182.289 | 0.949369 | 220 | 220 | 13386 | 60.8455 |
| small | sklearn_hgb_fixed | 12000 | 24 | 0.8856 | 0.0753619 | 0.968345 | 174.504 | 0.942299 | 220 | 220 | 13414 | 60.9727 |
| small | sklearn_hgb | 12000 | 24 | 0.910922 | 0.0753109 | 0.987464 | 174.074 | 0.942299 | 220 | 220 | 13414 | 60.9727 |
| small | xgboost_hist | 12000 | 24 | 1.19587 | 0.0095607 | 1.21048 | 178.84 | 0.948866 | 220 | 220 | 13394 | 60.8818 |


## Multi-thread scalability
| dataset_name | model | max_threads | fit_s_1_thread | fit_s_max_threads | speedup_vs_1_thread | parallel_efficiency |
| --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 16 | 7.18446 | 3.35715 | 2.14004 | 0.133753 |
| medium | lightgbm_hist | 16 | 2.43689 | 1.25955 | 1.93473 | 0.12092 |
| small | lightgbm_hist | 16 | 0.754449 | 0.554372 | 1.36091 | 0.0850568 |
| large | sklearn_hgb | 16 | 7.16068 | 4.00898 | 1.78616 | 0.111635 |
| medium | sklearn_hgb | 16 | 2.91156 | 1.99719 | 1.45783 | 0.0911143 |
| small | sklearn_hgb | 16 | 0.910922 | 1.20398 | 0.756593 | 0.0472871 |
| large | sklearn_hgb_fixed | 16 | 7.14226 | 3.44491 | 2.07328 | 0.12958 |
| medium | sklearn_hgb_fixed | 16 | 2.65263 | 1.4327 | 1.85149 | 0.115718 |
| small | sklearn_hgb_fixed | 16 | 0.8856 | 0.673376 | 1.31516 | 0.0821977 |
| large | xgboost_hist | 16 | 9.62937 | 5.02029 | 1.91809 | 0.119881 |
| medium | xgboost_hist | 16 | 3.49808 | 1.97435 | 1.77176 | 0.110735 |
| small | xgboost_hist | 16 | 1.19587 | 0.741926 | 1.61185 | 0.10074 |


## Memory growth trend (thread=1)
| model | smallest_samples | largest_samples | peak_mb_smallest | peak_mb_largest | approx_mb_per_1k_samples |
| --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 12000 | 90000 | 182.289 | 325.52 | 1.83629 |
| sklearn_hgb | 12000 | 90000 | 174.074 | 304.594 | 1.67333 |
| sklearn_hgb_fixed | 12000 | 90000 | 174.504 | 303.379 | 1.65224 |
| xgboost_hist | 12000 | 90000 | 178.84 | 335.148 | 2.00396 |


## Initial conclusion
- Best median runtime model: `lightgbm_hist`
- Least-performing median runtime model: `sklearn_hgb`
- All scenarios report explicit `r2_spread_for_scenario` to verify score parity while keeping matched hyperparameter values.
