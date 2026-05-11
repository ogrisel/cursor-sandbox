# Histogram GBDT Regressor Benchmark Report

## Experiment controls
- Timeout budget per individual run: `5.0 s`
- Adaptive reduction factor after timeout: `0.6`
- Threads tested: `[1, 3, 12]`
- Dataset templates: `[{'name': 'small', 'start_n_samples': 12000, 'n_features': 24}, {'name': 'medium', 'start_n_samples': 36000, 'n_features': 48}, {'name': 'large', 'start_n_samples': 90000, 'n_features': 80}]`

## Overall ranking (lower is faster)
| model | median_total_s | mean_total_s | geo_mean_total_s | mean_peak_rss_mb | mean_r2 | max_r2_spread_for_matched_scenario |
| --- | --- | --- | --- | --- | --- | --- |
| sklearn_hgb_fixed | 1.57107 | 2.47603 | 1.86546 | 359.469 | 0.857486 | 0.00991913 |
| lightgbm_hist | 1.59706 | 2.46654 | 1.89061 | 385.438 | 0.866003 | 0.00991913 |
| xgboost_hist | 2.21382 | 2.79923 | 2.35031 | 367.562 | 0.864851 | 0.00991913 |
| sklearn_hgb | 4.19703 | 3.77366 | 2.74625 | 358.042 | 0.857486 | 0.00991913 |


## Single-thread behavior
| dataset_name | model | n_samples | n_features | fit_seconds | predict_seconds | total_seconds | peak_rss_mb | r2 | fitted_trees | expected_trees | total_nodes | avg_nodes_per_tree |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 90000 | 80 | 6.49704 | 0.185529 | 6.70218 | 575.328 | 0.774775 | 220 | 220 | 13420 | 61 |
| large | xgboost_hist | 90000 | 80 | 6.95889 | 0.0495645 | 7.0241 | 519.016 | 0.772948 | 220 | 220 | 13420 | 61 |
| large | sklearn_hgb_fixed | 90000 | 80 | 7.0623 | 0.280611 | 7.34355 | 470.375 | 0.766213 | 220 | 220 | 13420 | 61 |
| large | sklearn_hgb | 90000 | 80 | 7.45465 | 0.318045 | 7.79608 | 470.375 | 0.766213 | 220 | 220 | 13420 | 61 |
| medium | lightgbm_hist | 36000 | 48 | 1.50421 | 0.0655148 | 1.59706 | 295.156 | 0.873865 | 220 | 220 | 13420 | 61 |
| medium | sklearn_hgb_fixed | 36000 | 48 | 1.93855 | 0.0637067 | 2.00709 | 279.922 | 0.863946 | 220 | 220 | 13420 | 61 |
| medium | xgboost_hist | 36000 | 48 | 2.03244 | 0.0139809 | 2.05273 | 288.922 | 0.87185 | 220 | 220 | 13420 | 61 |
| medium | sklearn_hgb | 36000 | 48 | 2.42269 | 0.111897 | 2.54094 | 275.797 | 0.863946 | 220 | 220 | 13420 | 61 |
| small | lightgbm_hist | 12000 | 24 | 0.50538 | 0.0254117 | 0.536182 | 216.469 | 0.949369 | 220 | 220 | 13386 | 60.8455 |
| small | sklearn_hgb_fixed | 12000 | 24 | 0.633484 | 0.022871 | 0.656598 | 206.984 | 0.942299 | 220 | 220 | 13414 | 60.9727 |
| small | sklearn_hgb | 12000 | 24 | 0.644178 | 0.0176173 | 0.670954 | 201.828 | 0.942299 | 220 | 220 | 13414 | 60.9727 |
| small | xgboost_hist | 12000 | 24 | 0.79638 | 0.00796204 | 0.83045 | 211.547 | 0.949753 | 220 | 220 | 13390 | 60.8636 |


## Multi-thread scalability
| dataset_name | model | max_threads | fit_s_1_thread | fit_s_max_threads | speedup_vs_1_thread | parallel_efficiency |
| --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 12 | 6.49704 | 3.2578 | 1.9943 | 0.166192 |
| medium | lightgbm_hist | 12 | 1.50421 | 3.45518 | 0.435348 | 0.036279 |
| small | lightgbm_hist | 12 | 0.50538 | 1.4767 | 0.342235 | 0.0285196 |
| large | sklearn_hgb | 12 | 7.45465 | 7.77423 | 0.958893 | 0.0799077 |
| medium | sklearn_hgb | 12 | 2.42269 | 4.33225 | 0.559221 | 0.0466017 |
| small | sklearn_hgb | 12 | 0.644178 | 4.12297 | 0.156241 | 0.0130201 |
| large | sklearn_hgb_fixed | 12 | 7.0623 | 2.56804 | 2.75007 | 0.229173 |
| medium | sklearn_hgb_fixed | 12 | 1.93855 | 1.11734 | 1.73497 | 0.144581 |
| small | sklearn_hgb_fixed | 12 | 0.633484 | 1.5354 | 0.412585 | 0.0343821 |
| large | xgboost_hist | 12 | 6.95889 | 3.24314 | 2.14572 | 0.17881 |
| medium | xgboost_hist | 12 | 2.03244 | 2.96999 | 0.684327 | 0.0570273 |
| small | xgboost_hist | 12 | 0.79638 | 1.27365 | 0.625276 | 0.0521063 |


## Memory growth trend (thread=1)
| model | smallest_samples | largest_samples | peak_mb_smallest | peak_mb_largest | approx_mb_per_1k_samples |
| --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 12000 | 90000 | 216.469 | 575.328 | 4.60076 |
| sklearn_hgb | 12000 | 90000 | 201.828 | 470.375 | 3.44291 |
| sklearn_hgb_fixed | 12000 | 90000 | 206.984 | 470.375 | 3.3768 |
| xgboost_hist | 12000 | 90000 | 211.547 | 519.016 | 3.94191 |


## Initial conclusion
- Best median runtime model: `sklearn_hgb_fixed`
- Least-performing median runtime model: `sklearn_hgb`
- All scenarios report explicit `r2_spread_for_scenario` to verify score parity while keeping matched hyperparameter values.
