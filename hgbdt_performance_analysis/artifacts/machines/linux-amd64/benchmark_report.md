# Histogram GBDT Regressor Benchmark Report

## Experiment controls
- Timeout budget per individual run: `5.0 s`
- Adaptive reduction factor after timeout: `0.6`
- Threads tested: `[1, 4, 16]`
- Dataset templates: `[{'name': 'small', 'start_n_samples': 12000, 'n_features': 24}, {'name': 'medium', 'start_n_samples': 36000, 'n_features': 48}, {'name': 'large', 'start_n_samples': 90000, 'n_features': 80}]`

## Overall ranking (lower is faster)
| model | median_total_s | mean_total_s | geo_mean_total_s | mean_peak_rss_mb | mean_r2 | max_r2_spread_for_matched_scenario |
| --- | --- | --- | --- | --- | --- | --- |
| sklearn_hgb_fixed | 1.24396 | 2.07453 | 1.53219 | 315.604 | 0.857486 | 0.00991913 |
| xgboost_hist | 1.71425 | 2.76334 | 2.01909 | 321.689 | 0.864851 | 0.00991913 |
| sklearn_hgb | 2.90886 | 5.24133 | 3.14576 | 315.607 | 0.857486 | 0.00991913 |
| lightgbm_hist | 3.11945 | 3.38049 | 2.33623 | 336.259 | 0.866003 | 0.00991913 |


## Single-thread behavior
| dataset_name | model | n_samples | n_features | fit_seconds | predict_seconds | total_seconds | peak_rss_mb | r2 | fitted_trees | expected_trees | total_nodes | avg_nodes_per_tree |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| large | sklearn_hgb | 90000 | 80 | 5.92093 | 0.273265 | 6.20376 | 408.578 | 0.766213 | 220 | 220 | 13420 | 61 |
| large | sklearn_hgb_fixed | 90000 | 80 | 5.93438 | 0.272775 | 6.21478 | 402.617 | 0.766213 | 220 | 220 | 13420 | 61 |
| large | lightgbm_hist | 90000 | 80 | 7.33829 | 0.291516 | 7.63968 | 435.859 | 0.774775 | 220 | 220 | 13420 | 61 |
| large | xgboost_hist | 90000 | 80 | 7.87713 | 0.0510306 | 7.93668 | 427.242 | 0.772948 | 220 | 220 | 13420 | 61 |
| medium | sklearn_hgb | 36000 | 48 | 2.08917 | 0.0961753 | 2.1912 | 276.586 | 0.863946 | 220 | 220 | 13420 | 61 |
| medium | sklearn_hgb_fixed | 36000 | 48 | 2.10041 | 0.0961973 | 2.20048 | 276.586 | 0.863946 | 220 | 220 | 13420 | 61 |
| medium | lightgbm_hist | 36000 | 48 | 2.41505 | 0.115064 | 2.53963 | 274.812 | 0.873865 | 220 | 220 | 13420 | 61 |
| medium | xgboost_hist | 36000 | 48 | 2.98833 | 0.0202607 | 3.01493 | 292.613 | 0.87185 | 220 | 220 | 13420 | 61 |
| small | lightgbm_hist | 12000 | 24 | 0.724993 | 0.0374753 | 0.762953 | 225.941 | 0.949369 | 220 | 220 | 13386 | 60.8455 |
| small | sklearn_hgb_fixed | 12000 | 24 | 0.746223 | 0.0324349 | 0.786064 | 212.086 | 0.942299 | 220 | 220 | 13414 | 60.9727 |
| small | sklearn_hgb | 12000 | 24 | 0.764674 | 0.0324512 | 0.807207 | 211.945 | 0.942299 | 220 | 220 | 13414 | 60.9727 |
| small | xgboost_hist | 12000 | 24 | 1.03725 | 0.00766824 | 1.04787 | 219.699 | 0.949753 | 220 | 220 | 13390 | 60.8636 |


## Multi-thread scalability
| dataset_name | model | max_threads | fit_s_1_thread | fit_s_max_threads | speedup_vs_1_thread | parallel_efficiency |
| --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 16 | 7.33829 | 6.77451 | 1.08322 | 0.0677012 |
| medium | lightgbm_hist | 16 | 2.41505 | 4.44446 | 0.543384 | 0.0339615 |
| small | lightgbm_hist | 16 | 0.724993 | 3.53478 | 0.205102 | 0.0128189 |
| large | sklearn_hgb | 16 | 5.92093 | 12.5013 | 0.473626 | 0.0296016 |
| medium | sklearn_hgb | 16 | 2.08917 | 10.5579 | 0.197878 | 0.0123674 |
| small | sklearn_hgb | 16 | 0.764674 | 9.8977 | 0.0772578 | 0.00482861 |
| large | sklearn_hgb_fixed | 16 | 5.93438 | 2.81907 | 2.10509 | 0.131568 |
| medium | sklearn_hgb_fixed | 16 | 2.10041 | 1.20743 | 1.73958 | 0.108724 |
| small | sklearn_hgb_fixed | 16 | 0.746223 | 0.553349 | 1.34856 | 0.0842849 |
| large | xgboost_hist | 16 | 7.87713 | 3.98807 | 1.97518 | 0.123448 |
| medium | xgboost_hist | 16 | 2.98833 | 1.69709 | 1.76086 | 0.110054 |
| small | xgboost_hist | 16 | 1.03725 | 0.666147 | 1.55709 | 0.097318 |


## Memory growth trend (thread=1)
| model | smallest_samples | largest_samples | peak_mb_smallest | peak_mb_largest | approx_mb_per_1k_samples |
| --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 12000 | 90000 | 225.941 | 435.859 | 2.69126 |
| sklearn_hgb | 12000 | 90000 | 211.945 | 408.578 | 2.52093 |
| sklearn_hgb_fixed | 12000 | 90000 | 212.086 | 402.617 | 2.44271 |
| xgboost_hist | 12000 | 90000 | 219.699 | 427.242 | 2.66081 |


## Initial conclusion
- Best median runtime model: `sklearn_hgb_fixed`
- Least-performing median runtime model: `lightgbm_hist`
- All scenarios report explicit `r2_spread_for_scenario` to verify score parity while keeping matched hyperparameter values.
