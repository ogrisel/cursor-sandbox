# Histogram GBDT Regressor Benchmark Report

## Experiment controls
- Timeout budget per individual run: `5.0 s`
- Adaptive reduction factor after timeout: `0.6`
- Threads tested: `[1, 3, 6]`
- Dataset templates: `[{'name': 'small', 'start_n_samples': 12000, 'n_features': 24}, {'name': 'medium', 'start_n_samples': 180000, 'n_features': 120}]`

## Overall ranking (lower is faster)
| model | median_total_s | mean_total_s | geo_mean_total_s | mean_peak_rss_mb | mean_r2 | max_r2_spread_for_matched_scenario |
| --- | --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 0.972857 | 1.03426 | 0.930941 | 187.846 | 0.810824 | 0.0290426 |
| xgboost_hist | 1.38057 | 1.68936 | 1.40595 | 203.411 | 0.814056 | 0.0290426 |
| sklearn_hgb_fixed | 1.39535 | 1.60447 | 1.45055 | 202.044 | 0.795808 | 0.0290426 |
| sklearn_hgb | 1.57563 | 1.60758 | 1.49739 | 198.339 | 0.795808 | 0.0290426 |


## Single-thread behavior
| dataset_name | model | n_samples | n_features | fit_seconds | predict_seconds | total_seconds | peak_rss_mb | r2 | fitted_trees | expected_trees | total_nodes | avg_nodes_per_tree |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| medium | lightgbm_hist | 8397 | 120 | 1.77952 | 0.0182338 | 1.83924 | 194.688 | 0.67228 | 220 | 220 | 13420 | 61 |
| medium | sklearn_hgb | 8397 | 120 | 2.33941 | 0.0183333 | 2.36085 | 226.656 | 0.649317 | 220 | 220 | 13420 | 61 |
| medium | sklearn_hgb_fixed | 8397 | 120 | 2.61405 | 0.0222109 | 2.64389 | 224.969 | 0.649317 | 220 | 220 | 13420 | 61 |
| medium | xgboost_hist | 8397 | 120 | 3.25455 | 0.00438054 | 3.33936 | 233.922 | 0.67836 | 220 | 220 | 13420 | 61 |
| small | lightgbm_hist | 12000 | 24 | 0.396159 | 0.0215188 | 0.435355 | 177.719 | 0.949369 | 220 | 220 | 13386 | 60.8455 |
| small | sklearn_hgb_fixed | 12000 | 24 | 0.647791 | 0.0177378 | 0.691151 | 178.328 | 0.942299 | 220 | 220 | 13414 | 60.9727 |
| small | xgboost_hist | 12000 | 24 | 0.686883 | 0.00671087 | 0.717089 | 183.906 | 0.949753 | 220 | 220 | 13390 | 60.8636 |
| small | sklearn_hgb | 12000 | 24 | 0.662144 | 0.0178221 | 0.763784 | 177.734 | 0.942299 | 220 | 220 | 13414 | 60.9727 |


## Multi-thread scalability
| dataset_name | model | max_threads | fit_s_1_thread | fit_s_max_threads | speedup_vs_1_thread | parallel_efficiency |
| --- | --- | --- | --- | --- | --- | --- |
| medium | lightgbm_hist | 6 | 1.77952 | 1.26918 | 1.4021 | 0.233684 |
| small | lightgbm_hist | 6 | 0.396159 | 0.7743 | 0.511636 | 0.0852726 |
| medium | sklearn_hgb | 6 | 2.33941 | 1.88643 | 1.24012 | 0.206687 |
| small | sklearn_hgb | 6 | 0.662144 | 2.11685 | 0.312798 | 0.0521329 |
| medium | sklearn_hgb_fixed | 6 | 2.61405 | 1.07665 | 2.42796 | 0.404659 |
| small | sklearn_hgb_fixed | 6 | 0.647791 | 2.36966 | 0.273368 | 0.0455614 |
| medium | xgboost_hist | 6 | 3.25455 | 1.92588 | 1.6899 | 0.281651 |
| small | xgboost_hist | 6 | 0.686883 | 0.774822 | 0.886504 | 0.147751 |


## Memory growth trend (thread=1)
| model | smallest_samples | largest_samples | peak_mb_smallest | peak_mb_largest | approx_mb_per_1k_samples |
| --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 8397 | 12000 | 194.688 | 177.719 | -4.70962 |
| sklearn_hgb | 8397 | 12000 | 226.656 | 177.734 | -13.5781 |
| sklearn_hgb_fixed | 8397 | 12000 | 224.969 | 178.328 | -12.9449 |
| xgboost_hist | 8397 | 12000 | 233.922 | 183.906 | -13.8817 |


## Initial conclusion
- Best median runtime model: `lightgbm_hist`
- Least-performing median runtime model: `sklearn_hgb`
- All scenarios report explicit `r2_spread_for_scenario` to verify score parity while keeping matched hyperparameter values.
