# Histogram GBDT Regressor Benchmark Report

## Experiment controls
- Timeout budget per individual run: `5.0 s`
- Adaptive reduction factor after timeout: `0.6`
- Threads tested: `[1, 2, 4, 8]`
- Dataset templates: `[{'name': 'small', 'start_n_samples': 12000, 'n_features': 24}, {'name': 'medium', 'start_n_samples': 180000, 'n_features': 120}]`

## Overall ranking (lower is faster)
| model | median_total_s | mean_total_s | geo_mean_total_s | mean_peak_rss_mb | mean_r2 | max_r2_spread_for_matched_scenario |
| --- | --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 0.783265 | 0.821329 | 0.741483 | 170.955 | 0.768005 | 0.0760385 |
| sklearn_hgb_fixed | 1.23247 | 1.22125 | 1.12178 | 166.923 | 0.736093 | 0.0760385 |
| sklearn_hgb | 1.23379 | 1.28892 | 1.19875 | 167.241 | 0.736093 | 0.0760385 |
| xgboost_hist | 1.5006 | 1.54716 | 1.38169 | 181.733 | 0.772938 | 0.0760385 |


## Single-thread behavior
| dataset_name | model | n_samples | n_features | fit_seconds | predict_seconds | total_seconds | peak_rss_mb | r2 | fitted_trees | expected_trees | total_nodes | avg_nodes_per_tree |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| medium | lightgbm_hist | 1813 | 120 | 1.72212 | 0.0074666 | 1.73964 | 175.758 | 0.586641 | 220 | 220 | 11256 | 51.1636 |
| medium | sklearn_hgb | 1813 | 120 | 2.17184 | 0.0138355 | 2.19131 | 169.445 | 0.529888 | 220 | 220 | 12398 | 56.3545 |
| medium | sklearn_hgb_fixed | 1813 | 120 | 2.21131 | 0.0140597 | 2.23034 | 169.258 | 0.529888 | 220 | 220 | 12398 | 56.3545 |
| medium | xgboost_hist | 1813 | 120 | 2.98523 | 0.0026374 | 2.99659 | 184.297 | 0.593432 | 220 | 220 | 11426 | 51.9364 |
| small | lightgbm_hist | 12000 | 24 | 0.777204 | 0.0378096 | 0.821756 | 164.484 | 0.949369 | 220 | 220 | 13386 | 60.8455 |
| small | sklearn_hgb | 12000 | 24 | 0.911878 | 0.0746523 | 0.988312 | 164.164 | 0.942299 | 220 | 220 | 13414 | 60.9727 |
| small | sklearn_hgb_fixed | 12000 | 24 | 0.916144 | 0.0746636 | 1.00007 | 163.918 | 0.942299 | 220 | 220 | 13414 | 60.9727 |
| small | xgboost_hist | 12000 | 24 | 1.20563 | 0.0098268 | 1.22202 | 168.398 | 0.948866 | 220 | 220 | 13394 | 60.8818 |


## Multi-thread scalability
| dataset_name | model | max_threads | fit_s_1_thread | fit_s_max_threads | speedup_vs_1_thread | parallel_efficiency |
| --- | --- | --- | --- | --- | --- | --- |
| medium | lightgbm_hist | 8 | 1.72212 | 0.805214 | 2.13872 | 0.267339 |
| small | lightgbm_hist | 8 | 0.777204 | 0.470369 | 1.65233 | 0.206541 |
| medium | sklearn_hgb | 8 | 2.17184 | 1.732 | 1.25395 | 0.156743 |
| small | sklearn_hgb | 8 | 0.911878 | 0.960863 | 0.949019 | 0.118627 |
| medium | sklearn_hgb_fixed | 8 | 2.21131 | 1.4519 | 1.52304 | 0.190381 |
| small | sklearn_hgb_fixed | 8 | 0.916144 | 0.693439 | 1.32116 | 0.165145 |
| medium | xgboost_hist | 8 | 2.98523 | 1.7836 | 1.67371 | 0.209214 |
| small | xgboost_hist | 8 | 1.20563 | 0.78074 | 1.54421 | 0.193026 |


## Memory growth trend (thread=1)
| model | smallest_samples | largest_samples | peak_mb_smallest | peak_mb_largest | approx_mb_per_1k_samples |
| --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 1813 | 12000 | 175.758 | 164.484 | -1.10665 |
| sklearn_hgb | 1813 | 12000 | 169.445 | 164.164 | -0.51843 |
| sklearn_hgb_fixed | 1813 | 12000 | 169.258 | 163.918 | -0.524182 |
| xgboost_hist | 1813 | 12000 | 184.297 | 168.398 | -1.56066 |


## Initial conclusion
- Best median runtime model: `lightgbm_hist`
- Least-performing median runtime model: `xgboost_hist`
- All scenarios report explicit `r2_spread_for_scenario` to verify score parity while keeping matched hyperparameter values.
