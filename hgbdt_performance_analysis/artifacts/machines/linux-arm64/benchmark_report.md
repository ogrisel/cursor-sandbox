# Histogram GBDT Regressor Benchmark Report

## Experiment controls
- Timeout budget per individual run: `20.0 s`
- Adaptive reduction factor after timeout: `0.6`
- Threads tested: `[1, 2, 4, 8]`
- Dataset templates: `[{'name': 'small', 'start_n_samples': 12000, 'n_features': 24}, {'name': 'medium', 'start_n_samples': 180000, 'n_features': 120}]`

## Overall ranking (lower is faster)
| model | median_total_s | mean_total_s | geo_mean_total_s | mean_peak_rss_mb | mean_r2 | max_r2_spread_for_matched_scenario |
| --- | --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 2.55487 | 3.89945 | 3.0462 | 332.24 | 0.817217 | 0.0120533 |
| sklearn_hgb_fixed | 2.75804 | 3.91245 | 3.07142 | 304.708 | 0.807714 | 0.0120533 |
| xgboost_hist | 3.44825 | 4.81936 | 3.60699 | 319.972 | 0.817468 | 0.0120533 |
| sklearn_hgb | 3.67579 | 4.65887 | 3.75368 | 306.064 | 0.807714 | 0.0120533 |


## Single-thread behavior
| dataset_name | model | n_samples | n_features | fit_seconds | predict_seconds | total_seconds | peak_rss_mb | r2 | fitted_trees | expected_trees | total_nodes | avg_nodes_per_tree |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| medium | lightgbm_hist | 108000 | 120 | 10.1683 | 0.223739 | 10.8408 | 452.41 | 0.685065 | 220 | 220 | 13420 | 61 |
| medium | sklearn_hgb_fixed | 108000 | 120 | 10.4794 | 0.299043 | 11.0781 | 401.656 | 0.673129 | 220 | 220 | 13420 | 61 |
| medium | sklearn_hgb | 108000 | 120 | 10.6328 | 0.254208 | 11.1497 | 401.668 | 0.673129 | 220 | 220 | 13420 | 61 |
| medium | xgboost_hist | 108000 | 120 | 13.2869 | 0.0510262 | 13.8064 | 426.797 | 0.685182 | 220 | 220 | 13420 | 61 |
| small | lightgbm_hist | 12000 | 24 | 0.532713 | 0.0237731 | 1.5963 | 202.914 | 0.949369 | 220 | 220 | 13386 | 60.8455 |
| small | sklearn_hgb_fixed | 12000 | 24 | 0.722317 | 0.02068 | 1.96263 | 198.617 | 0.942299 | 220 | 220 | 13414 | 60.9727 |
| small | sklearn_hgb | 12000 | 24 | 0.725291 | 0.0206514 | 1.97711 | 198.559 | 0.942299 | 220 | 220 | 13414 | 60.9727 |
| small | xgboost_hist | 12000 | 24 | 0.840391 | 0.00592082 | 2.18567 | 211.551 | 0.949753 | 220 | 220 | 13390 | 60.8636 |


## Multi-thread scalability
| dataset_name | model | max_threads | fit_s_1_thread | fit_s_max_threads | speedup_vs_1_thread | parallel_efficiency |
| --- | --- | --- | --- | --- | --- | --- |
| medium | lightgbm_hist | 8 | 10.1683 | 3.9777 | 2.55633 | 0.319541 |
| small | lightgbm_hist | 8 | 0.532713 | 1.24848 | 0.426688 | 0.053336 |
| medium | sklearn_hgb | 8 | 10.6328 | 6.75509 | 1.57405 | 0.196756 |
| small | sklearn_hgb | 8 | 0.725291 | 3.12294 | 0.232246 | 0.0290308 |
| medium | sklearn_hgb_fixed | 8 | 10.4794 | 3.03019 | 3.45833 | 0.432291 |
| small | sklearn_hgb_fixed | 8 | 0.722317 | 0.505851 | 1.42792 | 0.17849 |
| medium | xgboost_hist | 8 | 13.2869 | 4.20944 | 3.15646 | 0.394558 |
| small | xgboost_hist | 8 | 0.840391 | 0.435928 | 1.92782 | 0.240978 |


## Memory growth trend (thread=1)
| model | smallest_samples | largest_samples | peak_mb_smallest | peak_mb_largest | approx_mb_per_1k_samples |
| --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 12000 | 108000 | 202.914 | 452.41 | 2.59892 |
| sklearn_hgb | 12000 | 108000 | 198.559 | 401.668 | 2.11572 |
| sklearn_hgb_fixed | 12000 | 108000 | 198.617 | 401.656 | 2.11499 |
| xgboost_hist | 12000 | 108000 | 211.551 | 426.797 | 2.24215 |


## Initial conclusion
- Best median runtime model: `lightgbm_hist`
- Least-performing median runtime model: `sklearn_hgb`
- All scenarios report explicit `r2_spread_for_scenario` to verify score parity while keeping matched hyperparameter values.
