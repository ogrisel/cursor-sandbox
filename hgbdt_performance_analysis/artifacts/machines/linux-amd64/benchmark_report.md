# Histogram GBDT Regressor Benchmark Report

## Experiment controls
- Timeout budget per individual run: `12.0 s`
- Adaptive reduction factor after timeout: `0.5`
- Threads tested: `[1, 2, 4, 8, 16]`
- Dataset templates: `[{'name': 'small', 'start_n_samples': 50000, 'n_features': 40}, {'name': 'medium', 'start_n_samples': 140000, 'n_features': 80}, {'name': 'large', 'start_n_samples': 320000, 'n_features': 120}]`

## Overall ranking (lower is faster)
| model | median_total_s | mean_total_s | geo_mean_total_s | mean_peak_rss_mb | mean_r2 | max_r2_spread_for_matched_scenario |
| --- | --- | --- | --- | --- | --- | --- |
| sklearn_hgb_fixed | 2.7326 | 2.7068 | 2.47516 | 278.613 | 0.782765 | 0.0177437 |
| lightgbm_hist | 2.84473 | 3.17289 | 2.87039 | 287.045 | 0.793002 | 0.0177437 |
| xgboost_hist | 3.96522 | 3.89101 | 3.51851 | 303.793 | 0.793637 | 0.0177437 |
| sklearn_hgb | 4.43259 | 4.59825 | 3.90818 | 282.822 | 0.782765 | 0.0177437 |


## Single-thread behavior
| dataset_name | model | n_samples | n_features | fit_seconds | predict_seconds | total_seconds | peak_rss_mb | r2 | fitted_trees | expected_trees | total_nodes | avg_nodes_per_tree |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| large | sklearn_hgb | 40000 | 120 | 5.30422 | 0.118184 | 5.42668 | 288.086 | 0.675577 | 220 | 220 | 13420 | 61 |
| large | sklearn_hgb_fixed | 40000 | 120 | 5.35296 | 0.117591 | 5.47094 | 288.207 | 0.675577 | 220 | 220 | 13420 | 61 |
| large | lightgbm_hist | 40000 | 120 | 5.40205 | 0.107754 | 5.51416 | 288.719 | 0.692337 | 220 | 220 | 13420 | 61 |
| large | xgboost_hist | 40000 | 120 | 7.51141 | 0.0225822 | 7.54421 | 328.645 | 0.69332 | 220 | 220 | 13420 | 61 |
| medium | sklearn_hgb | 70000 | 80 | 4.96071 | 0.174257 | 5.1351 | 296.695 | 0.785099 | 220 | 220 | 13420 | 61 |
| medium | sklearn_hgb_fixed | 70000 | 80 | 4.97149 | 0.17361 | 5.15258 | 296.723 | 0.785099 | 220 | 220 | 13420 | 61 |
| medium | lightgbm_hist | 70000 | 80 | 5.13426 | 0.193961 | 5.3318 | 306.688 | 0.79359 | 220 | 220 | 13420 | 61 |
| medium | xgboost_hist | 70000 | 80 | 6.43017 | 0.0374286 | 6.47045 | 324.926 | 0.793248 | 220 | 220 | 13420 | 61 |
| small | lightgbm_hist | 50000 | 40 | 2.15228 | 0.131876 | 2.29245 | 243.84 | 0.893078 | 220 | 220 | 13420 | 61 |
| small | sklearn_hgb_fixed | 50000 | 40 | 2.17447 | 0.10975 | 2.29307 | 237.641 | 0.88762 | 220 | 220 | 13420 | 61 |
| small | sklearn_hgb | 50000 | 40 | 2.19558 | 0.109261 | 2.31199 | 237.859 | 0.88762 | 220 | 220 | 13420 | 61 |
| small | xgboost_hist | 50000 | 40 | 2.66919 | 0.0264168 | 2.70024 | 250.277 | 0.894341 | 220 | 220 | 13420 | 61 |


## Multi-thread scalability
| dataset_name | model | max_threads | fit_s_1_thread | fit_s_max_threads | speedup_vs_1_thread | parallel_efficiency |
| --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 16 | 5.40205 | 4.62645 | 1.16765 | 0.0729778 |
| medium | lightgbm_hist | 16 | 5.13426 | 4.65214 | 1.10364 | 0.0689772 |
| small | lightgbm_hist | 16 | 2.15228 | 3.2482 | 0.662606 | 0.0414129 |
| large | sklearn_hgb | 16 | 5.30422 | 8.99255 | 0.589846 | 0.0368654 |
| medium | sklearn_hgb | 16 | 4.96071 | 8.77341 | 0.565425 | 0.0353391 |
| small | sklearn_hgb | 16 | 2.19558 | 7.28174 | 0.301519 | 0.0188449 |
| large | sklearn_hgb_fixed | 16 | 5.35296 | 2.73026 | 1.9606 | 0.122538 |
| medium | sklearn_hgb_fixed | 16 | 4.97149 | 2.62308 | 1.89529 | 0.118455 |
| small | sklearn_hgb_fixed | 16 | 2.17447 | 1.30003 | 1.67263 | 0.104539 |
| large | xgboost_hist | 16 | 7.51141 | 4.99765 | 1.50299 | 0.0939368 |
| medium | xgboost_hist | 16 | 6.43017 | 3.96195 | 1.62298 | 0.101436 |
| small | xgboost_hist | 16 | 2.66919 | 1.83202 | 1.45697 | 0.0910604 |


## Memory growth trend (thread=1)
| model | smallest_samples | largest_samples | peak_mb_smallest | peak_mb_largest | approx_mb_per_1k_samples |
| --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 40000 | 70000 | 288.719 | 306.688 | 0.598958 |
| sklearn_hgb | 40000 | 70000 | 288.086 | 296.695 | 0.286979 |
| sklearn_hgb_fixed | 40000 | 70000 | 288.207 | 296.723 | 0.283854 |
| xgboost_hist | 40000 | 70000 | 328.645 | 324.926 | -0.123958 |


## Initial conclusion
- Best median runtime model: `sklearn_hgb_fixed`
- Least-performing median runtime model: `sklearn_hgb`
- All scenarios report explicit `r2_spread_for_scenario` to verify score parity while keeping matched hyperparameter values.
