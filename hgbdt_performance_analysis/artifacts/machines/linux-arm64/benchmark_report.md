# Histogram GBDT Regressor Benchmark Report

## Experiment controls
- Timeout budget per individual run: `5.0 s`
- Adaptive reduction factor after timeout: `0.6`
- Threads tested: `[1, 2, 4, 8]`
- Dataset templates: `[{'name': 'small', 'start_n_samples': 12000, 'n_features': 24}, {'name': 'medium', 'start_n_samples': 180000, 'n_features': 120}]`

## Overall ranking (lower is faster)
| model | median_total_s | mean_total_s | geo_mean_total_s | mean_peak_rss_mb | mean_r2 | max_r2_spread_for_matched_scenario |
| --- | --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 0.809875 | 0.939636 | 0.765865 | 209.864 | 0.80576 | 0.0280657 |
| sklearn_hgb_fixed | 0.818603 | 0.96157 | 0.847473 | 207.547 | 0.788192 | 0.0280657 |
| sklearn_hgb | 1.11736 | 1.60925 | 1.25446 | 207.804 | 0.788192 | 0.0280657 |
| xgboost_hist | 1.12855 | 1.35847 | 1.08368 | 224.868 | 0.805608 | 0.0280657 |


## Single-thread behavior
| dataset_name | model | n_samples | n_features | fit_seconds | predict_seconds | total_seconds | peak_rss_mb | r2 | fitted_trees | expected_trees | total_nodes | avg_nodes_per_tree |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| medium | lightgbm_hist | 5038 | 120 | 1.85841 | 0.0122715 | 1.8782 | 216.793 | 0.66215 | 220 | 220 | 13326 | 60.5727 |
| medium | sklearn_hgb | 5038 | 120 | 2.17438 | 0.0131869 | 2.19661 | 215.074 | 0.634085 | 220 | 220 | 13402 | 60.9182 |
| medium | sklearn_hgb_fixed | 5038 | 120 | 2.19229 | 0.0131588 | 2.21084 | 215.07 | 0.634085 | 220 | 220 | 13402 | 60.9182 |
| medium | xgboost_hist | 5038 | 120 | 3.31766 | 0.00363746 | 3.32249 | 234.625 | 0.661463 | 220 | 220 | 13336 | 60.6182 |
| small | lightgbm_hist | 12000 | 24 | 0.532288 | 0.0241905 | 0.560805 | 202.305 | 0.949369 | 220 | 220 | 13386 | 60.8455 |
| small | sklearn_hgb_fixed | 12000 | 24 | 0.717507 | 0.02061 | 0.740176 | 198.148 | 0.942299 | 220 | 220 | 13414 | 60.9727 |
| small | sklearn_hgb | 12000 | 24 | 0.721389 | 0.0207192 | 0.749502 | 198.16 | 0.942299 | 220 | 220 | 13414 | 60.9727 |
| small | xgboost_hist | 12000 | 24 | 0.827819 | 0.00627132 | 0.834515 | 204.992 | 0.949753 | 220 | 220 | 13390 | 60.8636 |


## Multi-thread scalability
| dataset_name | model | max_threads | fit_s_1_thread | fit_s_max_threads | speedup_vs_1_thread | parallel_efficiency |
| --- | --- | --- | --- | --- | --- | --- |
| medium | lightgbm_hist | 8 | 1.85841 | 1.59312 | 1.16652 | 0.145815 |
| small | lightgbm_hist | 8 | 0.532288 | 1.21535 | 0.437972 | 0.0547465 |
| medium | sklearn_hgb | 8 | 2.17438 | 3.6138 | 0.601687 | 0.0752108 |
| small | sklearn_hgb | 8 | 0.721389 | 2.95496 | 0.244128 | 0.030516 |
| medium | sklearn_hgb_fixed | 8 | 2.19229 | 0.886211 | 2.47377 | 0.309222 |
| small | sklearn_hgb_fixed | 8 | 0.717507 | 0.482598 | 1.48676 | 0.185845 |
| medium | xgboost_hist | 8 | 3.31766 | 1.43053 | 2.31918 | 0.289897 |
| small | xgboost_hist | 8 | 0.827819 | 0.50141 | 1.65098 | 0.206373 |


## Memory growth trend (thread=1)
| model | smallest_samples | largest_samples | peak_mb_smallest | peak_mb_largest | approx_mb_per_1k_samples |
| --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 5038 | 12000 | 216.793 | 202.305 | -2.08105 |
| sklearn_hgb | 5038 | 12000 | 215.074 | 198.16 | -2.42948 |
| sklearn_hgb_fixed | 5038 | 12000 | 215.07 | 198.148 | -2.43061 |
| xgboost_hist | 5038 | 12000 | 234.625 | 204.992 | -4.25636 |


## Initial conclusion
- Best median runtime model: `lightgbm_hist`
- Least-performing median runtime model: `xgboost_hist`
- All scenarios report explicit `r2_spread_for_scenario` to verify score parity while keeping matched hyperparameter values.
