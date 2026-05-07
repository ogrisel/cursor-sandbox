# Histogram GBDT Regressor Benchmark Report

## Experiment controls
- Timeout budget per individual run: `8.0 s`
- Adaptive reduction factor after timeout: `0.5`
- Threads tested: `[1, 2, 4]`
- Dataset templates: `[{'name': 'small', 'start_n_samples': 50000, 'n_features': 40}, {'name': 'medium', 'start_n_samples': 140000, 'n_features': 80}, {'name': 'large', 'start_n_samples': 320000, 'n_features': 120}]`

## Overall ranking (lower is faster)
| model | median_total_s | mean_total_s | geo_mean_total_s | mean_peak_rss_mb | mean_r2 | max_r2_spread_for_matched_scenario |
| --- | --- | --- | --- | --- | --- | --- |
| sklearn_hgb_fixed | 2.59654 | 3.00813 | 2.81933 | 295.858 | 0.782765 | 0.0177437 |
| sklearn_hgb | 2.82736 | 3.46688 | 3.20785 | 292.566 | 0.782765 | 0.0177437 |
| lightgbm_hist | 2.86357 | 3.09437 | 2.94457 | 325.349 | 0.793002 | 0.0177437 |
| xgboost_hist | 3.72146 | 3.68806 | 3.48756 | 341.609 | 0.793637 | 0.0177437 |


## Single-thread behavior
| dataset_name | model | n_samples | n_features | fit_seconds | predict_seconds | total_seconds | peak_rss_mb | r2 | fitted_trees | expected_trees | total_nodes | avg_nodes_per_tree |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 40000 | 120 | 4.11001 | 0.0781403 | 4.26621 | 366.938 | 0.692337 | 220 | 220 | 13420 | 61 |
| large | sklearn_hgb_fixed | 40000 | 120 | 4.56778 | 0.0935648 | 4.7347 | 327.578 | 0.675577 | 220 | 220 | 13420 | 61 |
| large | sklearn_hgb | 40000 | 120 | 5.16046 | 0.10032 | 5.30136 | 331.328 | 0.675577 | 220 | 220 | 13420 | 61 |
| large | xgboost_hist | 40000 | 120 | 5.8842 | 0.0154203 | 5.92541 | 414.094 | 0.69332 | 220 | 220 | 13420 | 61 |
| medium | lightgbm_hist | 70000 | 80 | 4.08332 | 0.141573 | 4.30412 | 376.094 | 0.79359 | 220 | 220 | 13420 | 61 |
| medium | sklearn_hgb_fixed | 70000 | 80 | 4.55738 | 0.134336 | 4.76256 | 328.609 | 0.785099 | 220 | 220 | 13420 | 61 |
| medium | sklearn_hgb | 70000 | 80 | 4.72179 | 0.163445 | 4.92535 | 328.688 | 0.785099 | 220 | 220 | 13420 | 61 |
| medium | xgboost_hist | 70000 | 80 | 5.15926 | 0.0283683 | 5.20726 | 377.297 | 0.793248 | 220 | 220 | 13420 | 61 |
| small | sklearn_hgb_fixed | 50000 | 40 | 2.38758 | 0.102764 | 2.51284 | 232.859 | 0.88762 | 220 | 220 | 13420 | 61 |
| small | lightgbm_hist | 50000 | 40 | 2.37759 | 0.132956 | 2.53587 | 251.75 | 0.893078 | 220 | 220 | 13420 | 61 |
| small | xgboost_hist | 50000 | 40 | 2.49817 | 0.045831 | 2.63782 | 256.172 | 0.894341 | 220 | 220 | 13420 | 61 |
| small | sklearn_hgb | 50000 | 40 | 2.8553 | 0.0938855 | 2.96099 | 234.547 | 0.88762 | 220 | 220 | 13420 | 61 |


## Multi-thread scalability
| dataset_name | model | max_threads | fit_s_1_thread | fit_s_max_threads | speedup_vs_1_thread | parallel_efficiency |
| --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 4 | 4.11001 | 2.81186 | 1.46167 | 0.365417 |
| medium | lightgbm_hist | 4 | 4.08332 | 4.44555 | 0.918518 | 0.22963 |
| small | lightgbm_hist | 4 | 2.37759 | 1.87722 | 1.26655 | 0.316638 |
| large | sklearn_hgb | 4 | 5.16046 | 2.70223 | 1.90971 | 0.477426 |
| medium | sklearn_hgb | 4 | 4.72179 | 2.73961 | 1.72353 | 0.430882 |
| small | sklearn_hgb | 4 | 2.8553 | 1.52284 | 1.87498 | 0.468745 |
| large | sklearn_hgb_fixed | 4 | 4.56778 | 1.77362 | 2.5754 | 0.643851 |
| medium | sklearn_hgb_fixed | 4 | 4.55738 | 2.23254 | 2.04134 | 0.510336 |
| small | sklearn_hgb_fixed | 4 | 2.38758 | 1.57805 | 1.513 | 0.37825 |
| large | xgboost_hist | 4 | 5.8842 | 3.65509 | 1.60986 | 0.402466 |
| medium | xgboost_hist | 4 | 5.15926 | 2.94905 | 1.74946 | 0.437366 |
| small | xgboost_hist | 4 | 2.49817 | 2.56347 | 0.97453 | 0.243633 |


## Memory growth trend (thread=1)
| model | smallest_samples | largest_samples | peak_mb_smallest | peak_mb_largest | approx_mb_per_1k_samples |
| --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 40000 | 70000 | 366.938 | 376.094 | 0.305208 |
| sklearn_hgb | 40000 | 70000 | 331.328 | 328.688 | -0.0880208 |
| sklearn_hgb_fixed | 40000 | 70000 | 327.578 | 328.609 | 0.034375 |
| xgboost_hist | 40000 | 70000 | 414.094 | 377.297 | -1.22656 |


## Initial conclusion
- Best median runtime model: `sklearn_hgb_fixed`
- Least-performing median runtime model: `xgboost_hist`
- All scenarios report explicit `r2_spread_for_scenario` to verify score parity while keeping matched hyperparameter values.
