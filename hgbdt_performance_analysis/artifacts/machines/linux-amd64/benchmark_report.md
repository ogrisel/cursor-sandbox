# Histogram GBDT Regressor Benchmark Report

## Experiment controls
- Timeout budget per individual run: `5.0 s`
- Adaptive reduction factor after timeout: `0.6`
- Threads tested: `[1, 2, 4, 8]`
- Dataset templates: `[{'name': 'small', 'start_n_samples': 12000, 'n_features': 24}, {'name': 'medium', 'start_n_samples': 180000, 'n_features': 120}]`

## Overall ranking (lower is faster)
| model | median_total_s | mean_total_s | geo_mean_total_s | mean_peak_rss_mb | mean_r2 | max_r2_spread_for_matched_scenario |
| --- | --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 0.290214 | 0.465517 | 0.360442 | 204.615 | 0.687688 | 0.0740629 |
| sklearn_hgb_fixed | 0.460821 | 0.486091 | 0.458859 | 198.246 | 0.636365 | 0.0740629 |
| sklearn_hgb | 0.597897 | 1.07604 | 0.730485 | 198.398 | 0.636365 | 0.0740629 |
| xgboost_hist | 0.686316 | 0.743738 | 0.640036 | 211.475 | 0.678003 | 0.0740629 |


## Single-thread behavior
| dataset_name | model | n_samples | n_features | fit_seconds | predict_seconds | total_seconds | peak_rss_mb | r2 | fitted_trees | expected_trees | total_nodes | avg_nodes_per_tree |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| medium | lightgbm_hist | 652 | 120 | 0.57473 | 0.00303233 | 0.583002 | 209.422 | 0.508565 | 220 | 220 | 6114 | 27.7909 |
| medium | sklearn_hgb | 652 | 120 | 0.798943 | 0.00342071 | 0.807078 | 199.852 | 0.434502 | 220 | 220 | 7040 | 32 |
| medium | sklearn_hgb_fixed | 652 | 120 | 0.803315 | 0.00349947 | 0.808818 | 199.793 | 0.434502 | 220 | 220 | 7040 | 32 |
| medium | xgboost_hist | 652 | 120 | 1.47242 | 0.00158509 | 1.47414 | 216.414 | 0.47647 | 220 | 220 | 6168 | 28.0364 |
| small | lightgbm_hist | 1555 | 24 | 0.25025 | 0.00532831 | 0.264187 | 202.094 | 0.866811 | 220 | 220 | 8348 | 37.9455 |
| small | sklearn_hgb_fixed | 1555 | 24 | 0.338387 | 0.00525871 | 0.347948 | 195.957 | 0.838229 | 220 | 220 | 9210 | 41.8636 |
| small | sklearn_hgb | 1555 | 24 | 0.341173 | 0.00524331 | 0.348237 | 195.988 | 0.838229 | 220 | 220 | 9210 | 41.8636 |
| small | xgboost_hist | 1555 | 24 | 0.436161 | 0.00177416 | 0.446614 | 205.32 | 0.879536 | 220 | 220 | 8248 | 37.4909 |


## Multi-thread scalability
| dataset_name | model | max_threads | fit_s_1_thread | fit_s_max_threads | speedup_vs_1_thread | parallel_efficiency |
| --- | --- | --- | --- | --- | --- | --- |
| medium | lightgbm_hist | 8 | 0.57473 | 0.971291 | 0.591718 | 0.0739647 |
| small | lightgbm_hist | 8 | 0.25025 | 1.02318 | 0.244581 | 0.0305726 |
| medium | sklearn_hgb | 8 | 0.798943 | 2.64794 | 0.301722 | 0.0377153 |
| small | sklearn_hgb | 8 | 0.341173 | 2.90503 | 0.117442 | 0.0146803 |
| medium | sklearn_hgb_fixed | 8 | 0.803315 | 0.57366 | 1.40033 | 0.175041 |
| small | sklearn_hgb_fixed | 8 | 0.338387 | 0.332696 | 1.01711 | 0.127138 |
| medium | xgboost_hist | 8 | 1.47242 | 1.03096 | 1.4282 | 0.178525 |
| small | xgboost_hist | 8 | 0.436161 | 0.439698 | 0.991956 | 0.123994 |


## Memory growth trend (thread=1)
| model | smallest_samples | largest_samples | peak_mb_smallest | peak_mb_largest | approx_mb_per_1k_samples |
| --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 652 | 1555 | 209.422 | 202.094 | -8.11531 |
| sklearn_hgb | 652 | 1555 | 199.852 | 195.988 | -4.27827 |
| sklearn_hgb_fixed | 652 | 1555 | 199.793 | 195.957 | -4.24799 |
| xgboost_hist | 652 | 1555 | 216.414 | 205.32 | -12.2854 |


## Initial conclusion
- Best median runtime model: `lightgbm_hist`
- Least-performing median runtime model: `xgboost_hist`
- All scenarios report explicit `r2_spread_for_scenario` to verify score parity while keeping matched hyperparameter values.
