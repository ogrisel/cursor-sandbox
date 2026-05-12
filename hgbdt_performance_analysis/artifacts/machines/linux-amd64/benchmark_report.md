# Histogram GBDT Regressor Benchmark Report

## Experiment controls
- Timeout budget per individual run: `5.0 s`
- Adaptive reduction factor after timeout: `0.6`
- Threads tested: `[1, 2, 4, 8]`
- Dataset templates: `[{'name': 'small', 'start_n_samples': 12000, 'n_features': 24}, {'name': 'medium', 'start_n_samples': 180000, 'n_features': 120}]`

## Overall ranking (lower is faster)
| model | median_total_s | mean_total_s | geo_mean_total_s | mean_peak_rss_mb | mean_r2 | max_r2_spread_for_matched_scenario |
| --- | --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 0.319515 | 0.508408 | 0.396687 | 204.82 | 0.687688 | 0.0740629 |
| sklearn_hgb_fixed | 0.457919 | 0.486109 | 0.455315 | 198.346 | 0.636365 | 0.0740629 |
| sklearn_hgb | 0.582393 | 1.10441 | 0.732303 | 198.406 | 0.636365 | 0.0740629 |
| xgboost_hist | 0.69058 | 0.750351 | 0.655696 | 211.753 | 0.678003 | 0.0740629 |


## Single-thread behavior
| dataset_name | model | n_samples | n_features | fit_seconds | predict_seconds | total_seconds | peak_rss_mb | r2 | fitted_trees | expected_trees | total_nodes | avg_nodes_per_tree |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| medium | lightgbm_hist | 652 | 120 | 0.625528 | 0.00317862 | 0.629726 | 207.836 | 0.508565 | 220 | 220 | 6114 | 27.7909 |
| medium | sklearn_hgb | 652 | 120 | 0.835542 | 0.0036424 | 0.844141 | 199.652 | 0.434502 | 220 | 220 | 7040 | 32 |
| medium | sklearn_hgb_fixed | 652 | 120 | 0.842009 | 0.00375501 | 0.854263 | 199.848 | 0.434502 | 220 | 220 | 7040 | 32 |
| medium | xgboost_hist | 652 | 120 | 1.48416 | 0.00132439 | 1.49221 | 216.375 | 0.47647 | 220 | 220 | 6168 | 28.0364 |
| small | lightgbm_hist | 1555 | 24 | 0.278044 | 0.00558632 | 0.284227 | 200.5 | 0.866811 | 220 | 220 | 8348 | 37.9455 |
| small | sklearn_hgb_fixed | 1555 | 24 | 0.337427 | 0.00595519 | 0.347146 | 195.898 | 0.838229 | 220 | 220 | 9210 | 41.8636 |
| small | sklearn_hgb | 1555 | 24 | 0.337063 | 0.00603206 | 0.347597 | 196.195 | 0.838229 | 220 | 220 | 9210 | 41.8636 |
| small | xgboost_hist | 1555 | 24 | 0.459612 | 0.0018553 | 0.467026 | 205.52 | 0.879536 | 220 | 220 | 8248 | 37.4909 |


## Multi-thread scalability
| dataset_name | model | max_threads | fit_s_1_thread | fit_s_max_threads | speedup_vs_1_thread | parallel_efficiency |
| --- | --- | --- | --- | --- | --- | --- |
| medium | lightgbm_hist | 8 | 0.625528 | 1.04925 | 0.596166 | 0.0745207 |
| small | lightgbm_hist | 8 | 0.278044 | 1.11312 | 0.249788 | 0.0312236 |
| medium | sklearn_hgb | 8 | 0.835542 | 2.71647 | 0.307583 | 0.0384479 |
| small | sklearn_hgb | 8 | 0.337063 | 3.08024 | 0.109428 | 0.0136784 |
| medium | sklearn_hgb_fixed | 8 | 0.842009 | 0.566096 | 1.48739 | 0.185924 |
| small | sklearn_hgb_fixed | 8 | 0.337427 | 0.318119 | 1.06069 | 0.132587 |
| medium | xgboost_hist | 8 | 1.48416 | 0.994837 | 1.49186 | 0.186482 |
| small | xgboost_hist | 8 | 0.459612 | 0.451395 | 1.0182 | 0.127276 |


## Memory growth trend (thread=1)
| model | smallest_samples | largest_samples | peak_mb_smallest | peak_mb_largest | approx_mb_per_1k_samples |
| --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 652 | 1555 | 207.836 | 200.5 | -8.12396 |
| sklearn_hgb | 652 | 1555 | 199.652 | 196.195 | -3.82838 |
| sklearn_hgb_fixed | 652 | 1555 | 199.848 | 195.898 | -4.37344 |
| xgboost_hist | 652 | 1555 | 216.375 | 205.52 | -12.0216 |


## Initial conclusion
- Best median runtime model: `lightgbm_hist`
- Least-performing median runtime model: `xgboost_hist`
- All scenarios report explicit `r2_spread_for_scenario` to verify score parity while keeping matched hyperparameter values.
