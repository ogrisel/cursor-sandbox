# Histogram GBDT Regressor Benchmark Report

## Experiment controls
- Timeout budget per individual run: `5.0 s`
- Adaptive reduction factor after timeout: `0.6`
- Threads tested: `[1, 2, 4, 8]`
- Dataset templates: `[{'name': 'small', 'start_n_samples': 12000, 'n_features': 24}, {'name': 'medium', 'start_n_samples': 180000, 'n_features': 120}]`

## Overall ranking (lower is faster)
| model | median_total_s | mean_total_s | geo_mean_total_s | mean_peak_rss_mb | mean_r2 | max_r2_spread_for_matched_scenario |
| --- | --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 0.819471 | 0.932159 | 0.765225 | 209.601 | 0.80576 | 0.0280657 |
| sklearn_hgb_fixed | 0.822554 | 0.98524 | 0.87805 | 207.472 | 0.788192 | 0.0280657 |
| xgboost_hist | 1.12985 | 1.36281 | 1.07944 | 224.797 | 0.805608 | 0.0280657 |
| sklearn_hgb | 1.16083 | 1.66878 | 1.29808 | 207.793 | 0.788192 | 0.0280657 |


## Single-thread behavior
| dataset_name | model | n_samples | n_features | fit_seconds | predict_seconds | total_seconds | peak_rss_mb | r2 | fitted_trees | expected_trees | total_nodes | avg_nodes_per_tree |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| medium | lightgbm_hist | 5038 | 120 | 1.87882 | 0.0117817 | 1.89137 | 216.84 | 0.66215 | 220 | 220 | 13326 | 60.5727 |
| medium | sklearn_hgb | 5038 | 120 | 2.22961 | 0.0134907 | 2.24694 | 215.051 | 0.634085 | 220 | 220 | 13402 | 60.9182 |
| medium | sklearn_hgb_fixed | 5038 | 120 | 2.2399 | 0.0136491 | 2.25695 | 215.059 | 0.634085 | 220 | 220 | 13402 | 60.9182 |
| medium | xgboost_hist | 5038 | 120 | 3.33726 | 0.00357511 | 3.34213 | 234.656 | 0.661463 | 220 | 220 | 13336 | 60.6182 |
| small | lightgbm_hist | 12000 | 24 | 0.537673 | 0.024245 | 0.571566 | 202.297 | 0.949369 | 220 | 220 | 13386 | 60.8455 |
| small | sklearn_hgb_fixed | 12000 | 24 | 0.725247 | 0.0206389 | 0.750095 | 198.148 | 0.942299 | 220 | 220 | 13414 | 60.9727 |
| small | sklearn_hgb | 12000 | 24 | 0.7267 | 0.0207567 | 0.750736 | 198.152 | 0.942299 | 220 | 220 | 13414 | 60.9727 |
| small | xgboost_hist | 12000 | 24 | 0.834146 | 0.00635172 | 0.84575 | 204.953 | 0.949753 | 220 | 220 | 13390 | 60.8636 |


## Multi-thread scalability
| dataset_name | model | max_threads | fit_s_1_thread | fit_s_max_threads | speedup_vs_1_thread | parallel_efficiency |
| --- | --- | --- | --- | --- | --- | --- |
| medium | lightgbm_hist | 8 | 1.87882 | 1.61393 | 1.16413 | 0.145517 |
| small | lightgbm_hist | 8 | 0.537673 | 1.07864 | 0.498475 | 0.0623093 |
| medium | sklearn_hgb | 8 | 2.22961 | 3.70485 | 0.601808 | 0.075226 |
| small | sklearn_hgb | 8 | 0.7267 | 3.15465 | 0.230359 | 0.0287948 |
| medium | sklearn_hgb_fixed | 8 | 2.2399 | 0.886324 | 2.52718 | 0.315898 |
| small | sklearn_hgb_fixed | 8 | 0.725247 | 0.555042 | 1.30665 | 0.163332 |
| medium | xgboost_hist | 8 | 3.33726 | 1.46424 | 2.27917 | 0.284897 |
| small | xgboost_hist | 8 | 0.834146 | 0.487439 | 1.71128 | 0.21391 |


## Memory growth trend (thread=1)
| model | smallest_samples | largest_samples | peak_mb_smallest | peak_mb_largest | approx_mb_per_1k_samples |
| --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 5038 | 12000 | 216.84 | 202.297 | -2.08891 |
| sklearn_hgb | 5038 | 12000 | 215.051 | 198.152 | -2.42724 |
| sklearn_hgb_fixed | 5038 | 12000 | 215.059 | 198.148 | -2.42892 |
| xgboost_hist | 5038 | 12000 | 234.656 | 204.953 | -4.26646 |


## Initial conclusion
- Best median runtime model: `lightgbm_hist`
- Least-performing median runtime model: `sklearn_hgb`
- All scenarios report explicit `r2_spread_for_scenario` to verify score parity while keeping matched hyperparameter values.
