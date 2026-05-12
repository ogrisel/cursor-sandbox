# Histogram GBDT Regressor Benchmark Report

## Experiment controls
- Timeout budget per individual run: `5.0 s`
- Adaptive reduction factor after timeout: `0.6`
- Threads tested: `[1, 2, 4, 8]`
- Dataset templates: `[{'name': 'small', 'start_n_samples': 12000, 'n_features': 24}, {'name': 'medium', 'start_n_samples': 180000, 'n_features': 120}]`

## Overall ranking (lower is faster)
| model | median_total_s | mean_total_s | geo_mean_total_s | mean_peak_rss_mb | mean_r2 | max_r2_spread_for_matched_scenario |
| --- | --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 0.319695 | 0.506457 | 0.397057 | 204.988 | 0.687688 | 0.0740629 |
| sklearn_hgb_fixed | 0.453763 | 0.485276 | 0.453662 | 198.333 | 0.636365 | 0.0740629 |
| sklearn_hgb | 0.580966 | 1.1069 | 0.734011 | 198.367 | 0.636365 | 0.0740629 |
| xgboost_hist | 0.677548 | 0.752096 | 0.65913 | 211.232 | 0.678003 | 0.0740629 |


## Single-thread behavior
| dataset_name | model | n_samples | n_features | fit_seconds | predict_seconds | total_seconds | peak_rss_mb | r2 | fitted_trees | expected_trees | total_nodes | avg_nodes_per_tree |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| medium | lightgbm_hist | 652 | 120 | 0.624825 | 0.00314157 | 0.629661 | 208.332 | 0.508565 | 220 | 220 | 6114 | 27.7909 |
| medium | sklearn_hgb_fixed | 652 | 120 | 0.84884 | 0.00369764 | 0.854447 | 200.797 | 0.434502 | 220 | 220 | 7040 | 32 |
| medium | sklearn_hgb | 652 | 120 | 0.842367 | 0.00375292 | 0.855179 | 199.941 | 0.434502 | 220 | 220 | 7040 | 32 |
| medium | xgboost_hist | 652 | 120 | 1.49388 | 0.00137844 | 1.50436 | 216.363 | 0.47647 | 220 | 220 | 6168 | 28.0364 |
| small | lightgbm_hist | 1555 | 24 | 0.278534 | 0.00569125 | 0.284842 | 200.445 | 0.866811 | 220 | 220 | 8348 | 37.9455 |
| small | sklearn_hgb | 1555 | 24 | 0.335843 | 0.00598256 | 0.347323 | 195.828 | 0.838229 | 220 | 220 | 9210 | 41.8636 |
| small | sklearn_hgb_fixed | 1555 | 24 | 0.338279 | 0.00600387 | 0.34768 | 195.957 | 0.838229 | 220 | 220 | 9210 | 41.8636 |
| small | xgboost_hist | 1555 | 24 | 0.460707 | 0.00181535 | 0.46744 | 205.441 | 0.879536 | 220 | 220 | 8248 | 37.4909 |


## Multi-thread scalability
| dataset_name | model | max_threads | fit_s_1_thread | fit_s_max_threads | speedup_vs_1_thread | parallel_efficiency |
| --- | --- | --- | --- | --- | --- | --- |
| medium | lightgbm_hist | 8 | 0.624825 | 1.03176 | 0.605594 | 0.0756992 |
| small | lightgbm_hist | 8 | 0.278534 | 1.10956 | 0.251032 | 0.0313789 |
| medium | sklearn_hgb | 8 | 0.842367 | 2.69961 | 0.312033 | 0.0390041 |
| small | sklearn_hgb | 8 | 0.335843 | 3.1021 | 0.108263 | 0.0135329 |
| medium | sklearn_hgb_fixed | 8 | 0.84884 | 0.567147 | 1.49668 | 0.187085 |
| small | sklearn_hgb_fixed | 8 | 0.338279 | 0.317314 | 1.06607 | 0.133259 |
| medium | xgboost_hist | 8 | 1.49388 | 0.994838 | 1.50163 | 0.187704 |
| small | xgboost_hist | 8 | 0.460707 | 0.449968 | 1.02387 | 0.127983 |


## Memory growth trend (thread=1)
| model | smallest_samples | largest_samples | peak_mb_smallest | peak_mb_largest | approx_mb_per_1k_samples |
| --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 652 | 1555 | 208.332 | 200.445 | -8.73391 |
| sklearn_hgb | 652 | 1555 | 199.941 | 195.828 | -4.55513 |
| sklearn_hgb_fixed | 652 | 1555 | 200.797 | 195.957 | -5.35974 |
| xgboost_hist | 652 | 1555 | 216.363 | 205.441 | -12.0951 |


## Initial conclusion
- Best median runtime model: `lightgbm_hist`
- Least-performing median runtime model: `xgboost_hist`
- All scenarios report explicit `r2_spread_for_scenario` to verify score parity while keeping matched hyperparameter values.
