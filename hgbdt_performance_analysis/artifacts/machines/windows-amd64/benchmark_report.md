# Histogram GBDT Regressor Benchmark Report

## Experiment controls
- Timeout budget per individual run: `5.0 s`
- Adaptive reduction factor after timeout: `0.6`
- Threads tested: `[1, 2, 4, 8]`
- Dataset templates: `[{'name': 'small', 'start_n_samples': 12000, 'n_features': 24}, {'name': 'medium', 'start_n_samples': 180000, 'n_features': 120}]`

## Overall ranking (lower is faster)
| model | median_total_s | mean_total_s | geo_mean_total_s | mean_peak_rss_mb | mean_r2 | max_r2_spread_for_matched_scenario |
| --- | --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 0.631206 | 0.674357 | 0.643079 | 170.756 | 0.751436 | 0.073199 |
| sklearn_hgb_fixed | 1.11476 | 1.14124 | 1.08031 | 165.229 | 0.720734 | 0.073199 |
| sklearn_hgb | 1.2468 | 1.2324 | 1.17569 | 165.566 | 0.720734 | 0.073199 |
| xgboost_hist | 1.44334 | 1.4362 | 1.34847 | 183.207 | 0.749837 | 0.073199 |


## Single-thread behavior
| dataset_name | model | n_samples | n_features | fit_seconds | predict_seconds | total_seconds | peak_rss_mb | r2 | fitted_trees | expected_trees | total_nodes | avg_nodes_per_tree |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| medium | lightgbm_hist | 1087 | 120 | 1.19091 | 0.0049719 | 1.20348 | 175.863 | 0.553503 | 220 | 220 | 8646 | 39.3 |
| medium | sklearn_hgb_fixed | 1087 | 120 | 1.87375 | 0.0067245 | 1.88325 | 166.219 | 0.499169 | 220 | 220 | 9918 | 45.0818 |
| medium | sklearn_hgb | 1087 | 120 | 1.87901 | 0.0067353 | 1.8871 | 165.648 | 0.499169 | 220 | 220 | 9918 | 45.0818 |
| medium | xgboost_hist | 1087 | 120 | 2.34752 | 0.0020982 | 2.35137 | 194.094 | 0.549615 | 220 | 220 | 8638 | 39.2636 |
| small | lightgbm_hist | 12000 | 24 | 0.657158 | 0.0336549 | 0.699659 | 166.477 | 0.949369 | 220 | 220 | 13386 | 60.8455 |
| small | sklearn_hgb_fixed | 12000 | 24 | 0.910566 | 0.0553619 | 0.96881 | 164.117 | 0.942299 | 220 | 220 | 13414 | 60.9727 |
| small | sklearn_hgb | 12000 | 24 | 0.902712 | 0.0593259 | 0.97086 | 164.102 | 0.942299 | 220 | 220 | 13414 | 60.9727 |
| small | xgboost_hist | 12000 | 24 | 1.17107 | 0.0084785 | 1.18966 | 170.91 | 0.948866 | 220 | 220 | 13394 | 60.8818 |


## Multi-thread scalability
| dataset_name | model | max_threads | fit_s_1_thread | fit_s_max_threads | speedup_vs_1_thread | parallel_efficiency |
| --- | --- | --- | --- | --- | --- | --- |
| medium | lightgbm_hist | 8 | 1.19091 | 0.670917 | 1.77506 | 0.221882 |
| small | lightgbm_hist | 8 | 0.657158 | 0.513196 | 1.28052 | 0.160065 |
| medium | sklearn_hgb | 8 | 1.87901 | 1.63109 | 1.15199 | 0.143999 |
| small | sklearn_hgb | 8 | 0.902712 | 1.18291 | 0.76313 | 0.0953913 |
| medium | sklearn_hgb_fixed | 8 | 1.87375 | 1.37738 | 1.36037 | 0.170046 |
| small | sklearn_hgb_fixed | 8 | 0.910566 | 0.751893 | 1.21103 | 0.151379 |
| medium | xgboost_hist | 8 | 2.34752 | 1.71176 | 1.37141 | 0.171426 |
| small | xgboost_hist | 8 | 1.17107 | 0.863801 | 1.35571 | 0.169464 |


## Memory growth trend (thread=1)
| model | smallest_samples | largest_samples | peak_mb_smallest | peak_mb_largest | approx_mb_per_1k_samples |
| --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 1087 | 12000 | 175.863 | 166.477 | -0.860141 |
| sklearn_hgb | 1087 | 12000 | 165.648 | 164.102 | -0.141746 |
| sklearn_hgb_fixed | 1087 | 12000 | 166.219 | 164.117 | -0.192574 |
| xgboost_hist | 1087 | 12000 | 194.094 | 170.91 | -2.1244 |


## Initial conclusion
- Best median runtime model: `lightgbm_hist`
- Least-performing median runtime model: `xgboost_hist`
- All scenarios report explicit `r2_spread_for_scenario` to verify score parity while keeping matched hyperparameter values.
