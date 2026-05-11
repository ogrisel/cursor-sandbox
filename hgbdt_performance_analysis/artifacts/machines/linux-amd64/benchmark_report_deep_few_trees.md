# Histogram GBDT Regressor Benchmark Report

## Experiment controls
- Timeout budget per individual run: `12.0 s`
- Adaptive reduction factor after timeout: `0.5`
- Threads tested: `[1, 2, 4, 8, 16]`
- Dataset templates: `[{'name': 'small', 'start_n_samples': 50000, 'n_features': 40}, {'name': 'medium', 'start_n_samples': 140000, 'n_features': 80}, {'name': 'large', 'start_n_samples': 320000, 'n_features': 120}]`

## Overall ranking (lower is faster)
| model | median_total_s | mean_total_s | geo_mean_total_s | mean_peak_rss_mb | mean_r2 | max_r2_spread_for_matched_scenario |
| --- | --- | --- | --- | --- | --- | --- |
| sklearn_hgb_fixed | 0.933632 | 1.00281 | 0.982076 | 243.205 | 0.596412 | 0.0171468 |
| sklearn_hgb | 1.41951 | 3.68734 | 2.29285 | 244.387 | 0.596412 | 0.0171468 |
| lightgbm_hist | 1.62501 | 1.84296 | 1.49277 | 254.2 | 0.603522 | 0.0171468 |
| xgboost_hist | 1.77641 | 1.84875 | 1.77487 | 308.28 | 0.602533 | 0.0171468 |


## Single-thread behavior
| dataset_name | model | n_samples | n_features | fit_seconds | predict_seconds | total_seconds | peak_rss_mb | r2 | fitted_trees | expected_trees | total_nodes | avg_nodes_per_tree |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| large | sklearn_hgb | 5000 | 120 | 1.59812 | 0.00519326 | 1.60614 | 240.543 | 0.443827 | 48 | 48 | 12032 | 250.667 |
| large | sklearn_hgb_fixed | 5000 | 120 | 1.60073 | 0.00517661 | 1.61506 | 241.246 | 0.443827 | 48 | 48 | 12032 | 250.667 |
| large | lightgbm_hist | 5000 | 120 | 1.70401 | 0.00616788 | 1.7183 | 271.383 | 0.460974 | 48 | 48 | 12072 | 251.5 |
| large | xgboost_hist | 5000 | 120 | 3.19278 | 0.00269739 | 3.19676 | 334.73 | 0.459013 | 48 | 48 | 12126 | 252.625 |
| medium | sklearn_hgb | 8750 | 80 | 1.40911 | 0.00764086 | 1.41951 | 244.805 | 0.570187 | 48 | 48 | 12144 | 253 |
| medium | sklearn_hgb_fixed | 8750 | 80 | 1.41421 | 0.00763765 | 1.42997 | 244.785 | 0.570187 | 48 | 48 | 12144 | 253 |
| medium | lightgbm_hist | 8750 | 80 | 1.60739 | 0.00974428 | 1.62501 | 251.957 | 0.571939 | 48 | 48 | 12144 | 253 |
| medium | xgboost_hist | 8750 | 80 | 2.61238 | 0.00372967 | 2.61798 | 299.312 | 0.571463 | 48 | 48 | 12144 | 253 |
| small | sklearn_hgb | 25000 | 40 | 1.1537 | 0.0183849 | 1.17738 | 240.027 | 0.775221 | 48 | 48 | 12144 | 253 |
| small | sklearn_hgb_fixed | 25000 | 40 | 1.16427 | 0.0182432 | 1.19134 | 240.5 | 0.775221 | 48 | 48 | 12144 | 253 |
| small | lightgbm_hist | 25000 | 40 | 1.17734 | 0.0249419 | 1.21045 | 235.031 | 0.777653 | 48 | 48 | 12144 | 253 |
| small | xgboost_hist | 25000 | 40 | 1.79014 | 0.00831058 | 1.80057 | 271.074 | 0.777123 | 48 | 48 | 12144 | 253 |


## Multi-thread scalability
| dataset_name | model | max_threads | fit_s_1_thread | fit_s_max_threads | speedup_vs_1_thread | parallel_efficiency |
| --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 16 | 1.70401 | 3.51771 | 0.48441 | 0.0302756 |
| medium | lightgbm_hist | 16 | 1.60739 | 4.51889 | 0.355705 | 0.0222316 |
| small | lightgbm_hist | 16 | 1.17734 | 3.73819 | 0.314949 | 0.0196843 |
| large | sklearn_hgb | 16 | 1.59812 | 8.91853 | 0.179191 | 0.0111994 |
| medium | sklearn_hgb | 16 | 1.40911 | 10.1689 | 0.138571 | 0.00866066 |
| small | sklearn_hgb | 16 | 1.1537 | 10.5815 | 0.10903 | 0.00681437 |
| large | sklearn_hgb_fixed | 16 | 1.60073 | 0.942795 | 1.69785 | 0.106116 |
| medium | sklearn_hgb_fixed | 16 | 1.41421 | 0.914895 | 1.54576 | 0.0966099 |
| small | sklearn_hgb_fixed | 16 | 1.16427 | 0.806397 | 1.44379 | 0.0902371 |
| large | xgboost_hist | 16 | 3.19278 | 2.06746 | 1.5443 | 0.0965185 |
| medium | xgboost_hist | 16 | 2.61238 | 1.76894 | 1.4768 | 0.0923002 |
| small | xgboost_hist | 16 | 1.79014 | 1.22706 | 1.45889 | 0.0911806 |


## Memory growth trend (thread=1)
| model | smallest_samples | largest_samples | peak_mb_smallest | peak_mb_largest | approx_mb_per_1k_samples |
| --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 5000 | 25000 | 271.383 | 235.031 | -1.81758 |
| sklearn_hgb | 5000 | 25000 | 240.543 | 240.027 | -0.0257812 |
| sklearn_hgb_fixed | 5000 | 25000 | 241.246 | 240.5 | -0.0373047 |
| xgboost_hist | 5000 | 25000 | 334.73 | 271.074 | -3.18281 |


## Initial conclusion
- Best median runtime model: `sklearn_hgb_fixed`
- Least-performing median runtime model: `xgboost_hist`
- All scenarios report explicit `r2_spread_for_scenario` to verify score parity while keeping matched hyperparameter values.
