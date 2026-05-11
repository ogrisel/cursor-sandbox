# Histogram GBDT Regressor Benchmark Report

## Experiment controls
- Timeout budget per individual run: `5.0 s`
- Adaptive reduction factor after timeout: `0.6`
- Threads tested: `[1, 4, 16]`
- Dataset templates: `[{'name': 'small', 'start_n_samples': 12000, 'n_features': 24}, {'name': 'medium', 'start_n_samples': 36000, 'n_features': 48}, {'name': 'large', 'start_n_samples': 90000, 'n_features': 80}]`

## Overall ranking (lower is faster)
| model | median_total_s | mean_total_s | geo_mean_total_s | mean_peak_rss_mb | mean_r2 | max_r2_spread_for_matched_scenario |
| --- | --- | --- | --- | --- | --- | --- |
| sklearn_hgb_fixed | 0.880118 | 1.71354 | 1.22431 | 308.021 | 0.857486 | 0.00991913 |
| xgboost_hist | 1.02713 | 2.09774 | 1.4096 | 313.661 | 0.864851 | 0.00991913 |
| lightgbm_hist | 1.71609 | 2.02243 | 1.39751 | 328.073 | 0.866003 | 0.00991913 |
| sklearn_hgb | 2.12015 | 3.1841 | 2.22363 | 307.492 | 0.857486 | 0.00991913 |


## Single-thread behavior
| dataset_name | model | n_samples | n_features | fit_seconds | predict_seconds | total_seconds | peak_rss_mb | r2 | fitted_trees | expected_trees | total_nodes | avg_nodes_per_tree |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 90000 | 80 | 5.75651 | 0.210968 | 5.97332 | 426.805 | 0.774775 | 220 | 220 | 13420 | 61 |
| large | sklearn_hgb_fixed | 90000 | 80 | 5.83911 | 0.170555 | 6.01555 | 394.082 | 0.766213 | 220 | 220 | 13420 | 61 |
| large | sklearn_hgb | 90000 | 80 | 5.85708 | 0.173543 | 6.03107 | 393.816 | 0.766213 | 220 | 220 | 13420 | 61 |
| large | xgboost_hist | 90000 | 80 | 7.47725 | 0.0445607 | 7.52889 | 418.508 | 0.772948 | 220 | 220 | 13420 | 61 |
| medium | lightgbm_hist | 36000 | 48 | 1.81766 | 0.0778887 | 1.90063 | 265.121 | 0.873865 | 220 | 220 | 13420 | 61 |
| medium | sklearn_hgb_fixed | 36000 | 48 | 2.02953 | 0.0644142 | 2.09949 | 266.965 | 0.863946 | 220 | 220 | 13420 | 61 |
| medium | sklearn_hgb | 36000 | 48 | 2.05218 | 0.064668 | 2.12015 | 267.051 | 0.863946 | 220 | 220 | 13420 | 61 |
| medium | xgboost_hist | 36000 | 48 | 2.62328 | 0.0179988 | 2.6473 | 282.953 | 0.87185 | 220 | 220 | 13420 | 61 |
| small | lightgbm_hist | 12000 | 24 | 0.530997 | 0.0247291 | 0.556996 | 222.305 | 0.949369 | 220 | 220 | 13386 | 60.8455 |
| small | sklearn_hgb_fixed | 12000 | 24 | 0.715941 | 0.0208371 | 0.742594 | 208.316 | 0.942299 | 220 | 220 | 13414 | 60.9727 |
| small | sklearn_hgb | 12000 | 24 | 0.731139 | 0.0208955 | 0.759699 | 208.25 | 0.942299 | 220 | 220 | 13414 | 60.9727 |
| small | xgboost_hist | 12000 | 24 | 0.829698 | 0.00654925 | 0.839466 | 216.48 | 0.949753 | 220 | 220 | 13390 | 60.8636 |


## Multi-thread scalability
| dataset_name | model | max_threads | fit_s_1_thread | fit_s_max_threads | speedup_vs_1_thread | parallel_efficiency |
| --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 16 | 5.75651 | 3.46281 | 1.66238 | 0.103899 |
| medium | lightgbm_hist | 16 | 1.81766 | 2.07167 | 0.877386 | 0.0548366 |
| small | lightgbm_hist | 16 | 0.530997 | 1.53136 | 0.346748 | 0.0216718 |
| large | sklearn_hgb | 16 | 5.85708 | 6.52693 | 0.897371 | 0.0560857 |
| medium | sklearn_hgb | 16 | 2.05218 | 5.14147 | 0.399143 | 0.0249464 |
| small | sklearn_hgb | 16 | 0.731139 | 4.56948 | 0.160005 | 0.0100003 |
| large | sklearn_hgb_fixed | 16 | 5.83911 | 1.85874 | 3.14143 | 0.19634 |
| medium | sklearn_hgb_fixed | 16 | 2.02953 | 0.851485 | 2.38351 | 0.14897 |
| small | sklearn_hgb_fixed | 16 | 0.715941 | 0.472977 | 1.51369 | 0.0946058 |
| large | xgboost_hist | 16 | 7.47725 | 2.42466 | 3.08384 | 0.19274 |
| medium | xgboost_hist | 16 | 2.62328 | 1.0181 | 2.57665 | 0.161041 |
| small | xgboost_hist | 16 | 0.829698 | 0.444717 | 1.86568 | 0.116605 |


## Memory growth trend (thread=1)
| model | smallest_samples | largest_samples | peak_mb_smallest | peak_mb_largest | approx_mb_per_1k_samples |
| --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 12000 | 90000 | 222.305 | 426.805 | 2.62179 |
| sklearn_hgb | 12000 | 90000 | 208.25 | 393.816 | 2.37906 |
| sklearn_hgb_fixed | 12000 | 90000 | 208.316 | 394.082 | 2.38161 |
| xgboost_hist | 12000 | 90000 | 216.48 | 418.508 | 2.59009 |


## Initial conclusion
- Best median runtime model: `sklearn_hgb_fixed`
- Least-performing median runtime model: `sklearn_hgb`
- All scenarios report explicit `r2_spread_for_scenario` to verify score parity while keeping matched hyperparameter values.
