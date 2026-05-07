# Histogram GBDT Regressor Benchmark Report

## Experiment controls
- Timeout budget per individual run: `8.0 s`
- Adaptive reduction factor after timeout: `0.5`
- Threads tested: `[1, 2, 4]`
- Dataset templates: `[{'name': 'small', 'start_n_samples': 50000, 'n_features': 40}, {'name': 'medium', 'start_n_samples': 140000, 'n_features': 80}, {'name': 'large', 'start_n_samples': 320000, 'n_features': 120}]`

## Overall ranking (lower is faster)
| model | median_total_s | mean_total_s | geo_mean_total_s | mean_peak_rss_mb | mean_r2 | max_r2_spread_for_matched_scenario |
| --- | --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 1.96064 | 2.16358 | 2.02226 | 171.519 | 0.776581 | 0.0300294 |
| sklearn_hgb_fixed | 3.08023 | 3.27437 | 3.12182 | 170.756 | 0.760867 | 0.0300294 |
| sklearn_hgb | 3.10433 | 3.28681 | 3.13448 | 170.833 | 0.760867 | 0.0300294 |
| xgboost_hist | 3.69903 | 3.93402 | 3.77574 | 187.991 | 0.776342 | 0.0300294 |


## Single-thread behavior
| dataset_name | model | n_samples | n_features | fit_seconds | predict_seconds | total_seconds | peak_rss_mb | r2 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 10000 | 120 | 3.26007 | 0.0292399 | 3.29815 | 159.934 | 0.674331 |
| large | sklearn_hgb_fixed | 10000 | 120 | 4.84438 | 0.0656637 | 4.91651 | 163.273 | 0.64901 |
| large | sklearn_hgb | 10000 | 120 | 4.84924 | 0.0674357 | 4.92135 | 162.883 | 0.64901 |
| large | xgboost_hist | 10000 | 120 | 5.56495 | 0.0079615 | 5.58139 | 177.605 | 0.679039 |
| medium | lightgbm_hist | 35000 | 80 | 3.6372 | 0.0984437 | 3.74006 | 187.066 | 0.762334 |
| medium | sklearn_hgb_fixed | 35000 | 80 | 4.90111 | 0.202359 | 5.10431 | 182.172 | 0.745971 |
| medium | sklearn_hgb | 35000 | 80 | 4.91213 | 0.206811 | 5.11952 | 182.461 | 0.745971 |
| medium | xgboost_hist | 35000 | 80 | 5.91024 | 0.0239876 | 5.94181 | 210.883 | 0.761535 |
| small | lightgbm_hist | 50000 | 40 | 2.29376 | 0.135494 | 2.43011 | 166.453 | 0.893078 |
| small | sklearn_hgb | 50000 | 40 | 3.0147 | 0.244642 | 3.26055 | 165.953 | 0.88762 |
| small | sklearn_hgb_fixed | 50000 | 40 | 3.02428 | 0.239092 | 3.26939 | 166.355 | 0.88762 |
| small | xgboost_hist | 50000 | 40 | 3.55463 | 0.0324631 | 3.59044 | 175.117 | 0.893059 |


## Multi-thread scalability
| dataset_name | model | max_threads | fit_s_1_thread | fit_s_max_threads | speedup_vs_1_thread | parallel_efficiency |
| --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 4 | 3.26007 | 1.42855 | 2.28207 | 0.570518 |
| medium | lightgbm_hist | 4 | 3.6372 | 1.70159 | 2.13753 | 0.534383 |
| small | lightgbm_hist | 4 | 2.29376 | 1.11857 | 2.05063 | 0.512657 |
| large | sklearn_hgb | 4 | 4.84924 | 3.08992 | 1.56938 | 0.392344 |
| medium | sklearn_hgb | 4 | 4.91213 | 2.91818 | 1.68329 | 0.420821 |
| small | sklearn_hgb | 4 | 3.0147 | 1.86254 | 1.61859 | 0.404649 |
| large | sklearn_hgb_fixed | 4 | 4.84438 | 3.07273 | 1.57658 | 0.394144 |
| medium | sklearn_hgb_fixed | 4 | 4.90111 | 2.91314 | 1.68242 | 0.420604 |
| small | sklearn_hgb_fixed | 4 | 3.02428 | 1.88458 | 1.60475 | 0.401188 |
| large | xgboost_hist | 4 | 5.56495 | 3.74668 | 1.4853 | 0.371326 |
| medium | xgboost_hist | 4 | 5.91024 | 3.6473 | 1.62044 | 0.405111 |
| small | xgboost_hist | 4 | 3.55463 | 2.21174 | 1.60716 | 0.401791 |


## Memory growth trend (thread=1)
| model | smallest_samples | largest_samples | peak_mb_smallest | peak_mb_largest | approx_mb_per_1k_samples |
| --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 10000 | 50000 | 159.934 | 166.453 | 0.162988 |
| sklearn_hgb | 10000 | 50000 | 162.883 | 165.953 | 0.0767578 |
| sklearn_hgb_fixed | 10000 | 50000 | 163.273 | 166.355 | 0.0770508 |
| xgboost_hist | 10000 | 50000 | 177.605 | 175.117 | -0.062207 |


## Initial conclusion
- Best median runtime model: `lightgbm_hist`
- Least-performing median runtime model: `xgboost_hist`
- All scenarios report explicit `r2_spread_for_scenario` to verify score parity while keeping matched hyperparameter values.
