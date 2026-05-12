# Histogram GBDT Regressor Benchmark Report

## Experiment controls
- Timeout budget per individual run: `5.0 s`
- Adaptive reduction factor after timeout: `0.6`
- Threads tested: `[1, 3, 6]`
- Dataset templates: `[{'name': 'small', 'start_n_samples': 12000, 'n_features': 24}, {'name': 'medium', 'start_n_samples': 180000, 'n_features': 120}]`

## Overall ranking (lower is faster)
| model | median_total_s | mean_total_s | geo_mean_total_s | mean_peak_rss_mb | mean_r2 | max_r2_spread_for_matched_scenario |
| --- | --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 0.904508 | 0.888692 | 0.845025 | 181.367 | 0.768005 | 0.0567536 |
| sklearn_hgb_fixed | 1.09013 | 1.08224 | 0.982453 | 187.185 | 0.736093 | 0.0567536 |
| xgboost_hist | 1.41993 | 1.3431 | 1.26757 | 193.458 | 0.767544 | 0.0567536 |
| sklearn_hgb | 1.44777 | 1.70212 | 1.53396 | 185.526 | 0.736093 | 0.0567536 |


## Single-thread behavior
| dataset_name | model | n_samples | n_features | fit_seconds | predict_seconds | total_seconds | peak_rss_mb | r2 | fitted_trees | expected_trees | total_nodes | avg_nodes_per_tree |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| medium | lightgbm_hist | 1813 | 120 | 0.847115 | 0.00453771 | 0.869759 | 186.141 | 0.586641 | 220 | 220 | 11256 | 51.1636 |
| medium | sklearn_hgb_fixed | 1813 | 120 | 1.44706 | 0.00464792 | 1.45955 | 197.594 | 0.529888 | 220 | 220 | 12398 | 56.3545 |
| medium | sklearn_hgb | 1813 | 120 | 1.57084 | 0.004693 | 1.59735 | 197.703 | 0.529888 | 220 | 220 | 12398 | 56.3545 |
| medium | xgboost_hist | 1813 | 120 | 1.79577 | 0.00141383 | 1.81828 | 206.281 | 0.585335 | 220 | 220 | 11618 | 52.8091 |
| small | lightgbm_hist | 12000 | 24 | 0.437733 | 0.0258333 | 0.488822 | 177.531 | 0.949369 | 220 | 220 | 13386 | 60.8455 |
| small | sklearn_hgb_fixed | 12000 | 24 | 0.644883 | 0.0266417 | 0.672987 | 178.438 | 0.942299 | 220 | 220 | 13414 | 60.9727 |
| small | xgboost_hist | 12000 | 24 | 0.647777 | 0.00635971 | 0.679074 | 181.938 | 0.949753 | 220 | 220 | 13390 | 60.8636 |
| small | sklearn_hgb | 12000 | 24 | 0.848262 | 0.0310796 | 0.88089 | 178.734 | 0.942299 | 220 | 220 | 13414 | 60.9727 |


## Multi-thread scalability
| dataset_name | model | max_threads | fit_s_1_thread | fit_s_max_threads | speedup_vs_1_thread | parallel_efficiency |
| --- | --- | --- | --- | --- | --- | --- |
| medium | lightgbm_hist | 6 | 0.847115 | 0.9614 | 0.881126 | 0.146854 |
| small | lightgbm_hist | 6 | 0.437733 | 1.33852 | 0.327028 | 0.0545046 |
| medium | sklearn_hgb | 6 | 1.57084 | 2.59652 | 0.604978 | 0.10083 |
| small | sklearn_hgb | 6 | 0.848262 | 2.84402 | 0.298262 | 0.0497103 |
| medium | sklearn_hgb_fixed | 6 | 1.44706 | 1.67129 | 0.865834 | 0.144306 |
| small | sklearn_hgb_fixed | 6 | 0.644883 | 0.420936 | 1.53202 | 0.255337 |
| medium | xgboost_hist | 6 | 1.79577 | 1.75353 | 1.02409 | 0.170681 |
| small | xgboost_hist | 6 | 0.647777 | 0.916323 | 0.706931 | 0.117822 |


## Memory growth trend (thread=1)
| model | smallest_samples | largest_samples | peak_mb_smallest | peak_mb_largest | approx_mb_per_1k_samples |
| --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 1813 | 12000 | 186.141 | 177.531 | -0.845134 |
| sklearn_hgb | 1813 | 12000 | 197.703 | 178.734 | -1.86205 |
| sklearn_hgb_fixed | 1813 | 12000 | 197.594 | 178.438 | -1.88046 |
| xgboost_hist | 1813 | 12000 | 206.281 | 181.938 | -2.38969 |


## Initial conclusion
- Best median runtime model: `lightgbm_hist`
- Least-performing median runtime model: `sklearn_hgb`
- All scenarios report explicit `r2_spread_for_scenario` to verify score parity while keeping matched hyperparameter values.
