# Histogram GBDT Regressor Benchmark Report

## Experiment controls
- Timeout budget per individual run: `5.0 s`
- Adaptive reduction factor after timeout: `0.6`
- Threads tested: `[1, 4, 8]`
- Dataset templates: `[{'name': 'small', 'start_n_samples': 12000, 'n_features': 24}, {'name': 'large', 'start_n_samples': 180000, 'n_features': 120}]`

## Overall ranking (lower is faster)
| model | median_total_s | mean_total_s | geo_mean_total_s | mean_peak_rss_mb | mean_r2 | max_r2_spread_for_matched_scenario |
| --- | --- | --- | --- | --- | --- | --- |
| sklearn_hgb_fixed | 0.784539 | 0.895512 | 0.815959 | 204.729 | 0.760875 | 0.0405318 |
| lightgbm_hist | 0.993305 | 0.978585 | 0.809715 | 208.86 | 0.784676 | 0.0405318 |
| xgboost_hist | 1.04584 | 1.18574 | 0.976932 | 223.012 | 0.782729 | 0.0405318 |
| sklearn_hgb | 1.34421 | 1.83178 | 1.41194 | 205.079 | 0.760875 | 0.0405318 |


## Single-thread behavior
| dataset_name | model | n_samples | n_features | fit_seconds | predict_seconds | total_seconds | peak_rss_mb | r2 | fitted_trees | expected_trees | total_nodes | avg_nodes_per_tree |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 3022 | 120 | 1.5134 | 0.00833926 | 1.52688 | 214.633 | 0.619983 | 220 | 220 | 12996 | 59.0727 |
| large | sklearn_hgb | 3022 | 120 | 1.83221 | 0.0081221 | 1.84945 | 209.645 | 0.579451 | 220 | 220 | 13266 | 60.3 |
| large | sklearn_hgb_fixed | 3022 | 120 | 1.83425 | 0.00865356 | 1.84993 | 209.66 | 0.579451 | 220 | 220 | 13266 | 60.3 |
| large | xgboost_hist | 3022 | 120 | 2.74285 | 0.00266197 | 2.74792 | 232.832 | 0.615705 | 220 | 220 | 13032 | 59.2364 |
| small | lightgbm_hist | 12000 | 24 | 0.545134 | 0.0243342 | 0.569643 | 202.305 | 0.949369 | 220 | 220 | 13386 | 60.8455 |
| small | sklearn_hgb_fixed | 12000 | 24 | 0.735239 | 0.0208935 | 0.762432 | 198.195 | 0.942299 | 220 | 220 | 13414 | 60.9727 |
| small | sklearn_hgb | 12000 | 24 | 0.74301 | 0.0209545 | 0.773738 | 198.141 | 0.942299 | 220 | 220 | 13414 | 60.9727 |
| small | xgboost_hist | 12000 | 24 | 0.843572 | 0.00646467 | 0.855307 | 206.738 | 0.949753 | 220 | 220 | 13390 | 60.8636 |


## Multi-thread scalability
| dataset_name | model | max_threads | fit_s_1_thread | fit_s_max_threads | speedup_vs_1_thread | parallel_efficiency |
| --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 8 | 1.5134 | 1.54175 | 0.981611 | 0.122701 |
| small | lightgbm_hist | 8 | 0.545134 | 1.40649 | 0.387584 | 0.048448 |
| large | sklearn_hgb | 8 | 1.83221 | 3.73475 | 0.490585 | 0.0613232 |
| small | sklearn_hgb | 8 | 0.74301 | 3.19952 | 0.232225 | 0.0290282 |
| large | sklearn_hgb_fixed | 8 | 1.83425 | 0.79912 | 2.29534 | 0.286917 |
| small | sklearn_hgb_fixed | 8 | 0.735239 | 0.548217 | 1.34115 | 0.167643 |
| large | xgboost_hist | 8 | 2.74285 | 1.31694 | 2.08275 | 0.260344 |
| small | xgboost_hist | 8 | 0.843572 | 0.487713 | 1.72965 | 0.216206 |


## Memory growth trend (thread=1)
| model | smallest_samples | largest_samples | peak_mb_smallest | peak_mb_largest | approx_mb_per_1k_samples |
| --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 3022 | 12000 | 214.633 | 202.305 | -1.37315 |
| sklearn_hgb | 3022 | 12000 | 209.645 | 198.141 | -1.28134 |
| sklearn_hgb_fixed | 3022 | 12000 | 209.66 | 198.195 | -1.27699 |
| xgboost_hist | 3022 | 12000 | 232.832 | 206.738 | -2.90641 |


## Initial conclusion
- Best median runtime model: `sklearn_hgb_fixed`
- Least-performing median runtime model: `sklearn_hgb`
- All scenarios report explicit `r2_spread_for_scenario` to verify score parity while keeping matched hyperparameter values.
