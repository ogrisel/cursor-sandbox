# Histogram GBDT Regressor Benchmark Report

## Experiment controls
- Timeout budget per individual run: `8.0 s`
- Adaptive reduction factor after timeout: `0.5`
- Threads tested: `[1, 2, 4]`
- Dataset templates: `[{'name': 'small', 'start_n_samples': 50000, 'n_features': 40}, {'name': 'medium', 'start_n_samples': 140000, 'n_features': 80}, {'name': 'large', 'start_n_samples': 320000, 'n_features': 120}]`

## Overall ranking (lower is faster)
| model | median_total_s | mean_total_s | geo_mean_total_s | mean_peak_rss_mb | mean_r2 | max_r2_spread_for_matched_scenario |
| --- | --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 1.87221 | 2.18712 | 2.02047 | 197.485 | 0.776581 | 0.0300294 |
| sklearn_hgb | 2.8175 | 3.0021 | 2.85758 | 197.052 | 0.760867 | 0.0300294 |
| sklearn_hgb_fixed | 2.84682 | 3.00198 | 2.85414 | 197.191 | 0.760867 | 0.0300294 |
| xgboost_hist | 3.39142 | 3.55592 | 3.38413 | 213.378 | 0.776342 | 0.0300294 |


## Single-thread behavior
| dataset_name | model | n_samples | n_features | fit_seconds | predict_seconds | total_seconds | peak_rss_mb | r2 | fitted_trees | expected_trees | total_nodes | avg_nodes_per_tree |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 10000 | 120 | 3.29911 | 0.0321273 | 3.34126 | 184.973 | 0.674331 | 220 | 220 | 13420 | 61 |
| large | sklearn_hgb_fixed | 10000 | 120 | 4.44576 | 0.0747416 | 4.52138 | 189.16 | 0.64901 | 220 | 220 | 13420 | 61 |
| large | sklearn_hgb | 10000 | 120 | 4.44231 | 0.0744715 | 4.52228 | 189.223 | 0.64901 | 220 | 220 | 13420 | 61 |
| large | xgboost_hist | 10000 | 120 | 5.23632 | 0.0088871 | 5.25097 | 205.641 | 0.679039 | 220 | 220 | 13420 | 61 |
| medium | lightgbm_hist | 35000 | 80 | 3.81927 | 0.109128 | 3.93592 | 213.031 | 0.762334 | 220 | 220 | 13420 | 61 |
| medium | sklearn_hgb | 35000 | 80 | 4.53009 | 0.205267 | 4.73986 | 208.812 | 0.745971 | 220 | 220 | 13420 | 61 |
| medium | sklearn_hgb_fixed | 35000 | 80 | 4.54663 | 0.208551 | 4.76102 | 209.141 | 0.745971 | 220 | 220 | 13420 | 61 |
| medium | xgboost_hist | 35000 | 80 | 5.51263 | 0.0268535 | 5.54364 | 237.484 | 0.761535 | 220 | 220 | 13420 | 61 |
| small | lightgbm_hist | 50000 | 40 | 2.45109 | 0.152988 | 2.61127 | 192.543 | 0.893078 | 220 | 220 | 13420 | 61 |
| small | sklearn_hgb | 50000 | 40 | 2.83918 | 0.273628 | 3.12071 | 192.238 | 0.88762 | 220 | 220 | 13420 | 61 |
| small | sklearn_hgb_fixed | 50000 | 40 | 2.83476 | 0.306662 | 3.14277 | 192.258 | 0.88762 | 220 | 220 | 13420 | 61 |
| small | xgboost_hist | 50000 | 40 | 3.44981 | 0.0354711 | 3.4908 | 201.43 | 0.893059 | 220 | 220 | 13420 | 61 |


## Multi-thread scalability
| dataset_name | model | max_threads | fit_s_1_thread | fit_s_max_threads | speedup_vs_1_thread | parallel_efficiency |
| --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 4 | 3.29911 | 1.34054 | 2.46104 | 0.615259 |
| medium | lightgbm_hist | 4 | 3.81927 | 1.62621 | 2.34858 | 0.587144 |
| small | lightgbm_hist | 4 | 2.45109 | 1.08832 | 2.25218 | 0.563045 |
| large | sklearn_hgb | 4 | 4.44231 | 2.59529 | 1.71168 | 0.42792 |
| medium | sklearn_hgb | 4 | 4.53009 | 2.49628 | 1.81474 | 0.453685 |
| small | sklearn_hgb | 4 | 2.83918 | 1.65259 | 1.71802 | 0.429504 |
| large | sklearn_hgb_fixed | 4 | 4.44576 | 2.59229 | 1.71499 | 0.428748 |
| medium | sklearn_hgb_fixed | 4 | 4.54663 | 2.47952 | 1.83367 | 0.458418 |
| small | sklearn_hgb_fixed | 4 | 2.83476 | 1.65419 | 1.71369 | 0.428422 |
| large | xgboost_hist | 4 | 5.23632 | 3.34737 | 1.56431 | 0.391076 |
| medium | xgboost_hist | 4 | 5.51263 | 3.26279 | 1.68955 | 0.422387 |
| small | xgboost_hist | 4 | 3.44981 | 1.96103 | 1.75918 | 0.439796 |


## Memory growth trend (thread=1)
| model | smallest_samples | largest_samples | peak_mb_smallest | peak_mb_largest | approx_mb_per_1k_samples |
| --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 10000 | 50000 | 184.973 | 192.543 | 0.189258 |
| sklearn_hgb | 10000 | 50000 | 189.223 | 192.238 | 0.0753906 |
| sklearn_hgb_fixed | 10000 | 50000 | 189.16 | 192.258 | 0.0774414 |
| xgboost_hist | 10000 | 50000 | 205.641 | 201.43 | -0.105273 |


## Initial conclusion
- Best median runtime model: `lightgbm_hist`
- Least-performing median runtime model: `xgboost_hist`
- All scenarios report explicit `r2_spread_for_scenario` to verify score parity while keeping matched hyperparameter values.
