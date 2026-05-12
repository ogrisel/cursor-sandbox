# Histogram GBDT Regressor Benchmark Report

## Experiment controls
- Timeout budget per individual run: `5.0 s`
- Adaptive reduction factor after timeout: `0.6`
- Threads tested: `[1, 2, 4, 8]`
- Dataset templates: `[{'name': 'small', 'start_n_samples': 12000, 'n_features': 24}, {'name': 'medium', 'start_n_samples': 180000, 'n_features': 120}]`

## Overall ranking (lower is faster)
| model | median_total_s | mean_total_s | geo_mean_total_s | mean_peak_rss_mb | mean_r2 | max_r2_spread_for_matched_scenario |
| --- | --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 1.86864 | 1.81754 | 1.81006 | 171.775 | 0.751436 | 0.073199 |
| sklearn_hgb_fixed | 1.87477 | 1.88051 | 1.86606 | 165.32 | 0.720734 | 0.073199 |
| sklearn_hgb | 1.88915 | 1.97556 | 1.95838 | 165.903 | 0.720734 | 0.073199 |
| xgboost_hist | 2.0327 | 2.09543 | 2.0768 | 185.888 | 0.749837 | 0.073199 |


## Single-thread behavior
| dataset_name | model | n_samples | n_features | fit_seconds | predict_seconds | total_seconds | peak_rss_mb | r2 | fitted_trees | expected_trees | total_nodes | avg_nodes_per_tree |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| medium | lightgbm_hist | 1087 | 120 | 1.23696 | 0.00375181 | 1.74082 | 174.801 | 0.553503 | 220 | 220 | 8646 | 39.3 |
| medium | sklearn_hgb | 1087 | 120 | 1.57912 | 0.00800966 | 2.09269 | 165.875 | 0.499169 | 220 | 220 | 9918 | 45.0818 |
| medium | sklearn_hgb_fixed | 1087 | 120 | 1.60684 | 0.00816564 | 2.11581 | 166.059 | 0.499169 | 220 | 220 | 9918 | 45.0818 |
| medium | xgboost_hist | 1087 | 120 | 2.2539 | 0.00145475 | 2.76471 | 196.652 | 0.549615 | 220 | 220 | 8638 | 39.2636 |
| small | xgboost_hist | 12000 | 24 | 1.16996 | 0.00850157 | 1.67405 | 169.723 | 0.948866 | 220 | 220 | 13394 | 60.8818 |
| small | lightgbm_hist | 12000 | 24 | 0.726625 | 0.0353767 | 1.98768 | 165.305 | 0.949369 | 220 | 220 | 13386 | 60.8455 |
| small | sklearn_hgb_fixed | 12000 | 24 | 0.893914 | 0.0671319 | 2.32551 | 164.105 | 0.942299 | 220 | 220 | 13414 | 60.9727 |
| small | sklearn_hgb | 12000 | 24 | 0.893799 | 0.068416 | 2.33686 | 164.332 | 0.942299 | 220 | 220 | 13414 | 60.9727 |


## Multi-thread scalability
| dataset_name | model | max_threads | fit_s_1_thread | fit_s_max_threads | speedup_vs_1_thread | parallel_efficiency |
| --- | --- | --- | --- | --- | --- | --- |
| medium | lightgbm_hist | 8 | 1.23696 | 0.540367 | 2.28911 | 0.286139 |
| small | lightgbm_hist | 8 | 0.726625 | 0.430999 | 1.68591 | 0.210739 |
| medium | sklearn_hgb | 8 | 1.57912 | 1.30508 | 1.20998 | 0.151247 |
| small | sklearn_hgb | 8 | 0.893799 | 0.952779 | 0.938097 | 0.117262 |
| medium | sklearn_hgb_fixed | 8 | 1.60684 | 1.1239 | 1.4297 | 0.178713 |
| small | sklearn_hgb_fixed | 8 | 0.893914 | 0.720475 | 1.24073 | 0.155091 |
| medium | xgboost_hist | 8 | 2.2539 | 1.442 | 1.56304 | 0.195379 |
| small | xgboost_hist | 8 | 1.16996 | 0.754889 | 1.54984 | 0.193731 |


## Memory growth trend (thread=1)
| model | smallest_samples | largest_samples | peak_mb_smallest | peak_mb_largest | approx_mb_per_1k_samples |
| --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 1087 | 12000 | 174.801 | 165.305 | -0.870163 |
| sklearn_hgb | 1087 | 12000 | 165.875 | 164.332 | -0.141388 |
| sklearn_hgb_fixed | 1087 | 12000 | 166.059 | 164.105 | -0.178972 |
| xgboost_hist | 1087 | 12000 | 196.652 | 169.723 | -2.46767 |


## Initial conclusion
- Best median runtime model: `lightgbm_hist`
- Least-performing median runtime model: `xgboost_hist`
- All scenarios report explicit `r2_spread_for_scenario` to verify score parity while keeping matched hyperparameter values.
