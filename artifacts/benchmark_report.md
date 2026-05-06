# Histogram GBDT Regressor Benchmark Report

## Experiment controls
- Timeout budget per individual run: `10.0 s`
- Adaptive reduction factor after timeout: `0.72`
- Threads tested: `[1, 2, 4]`
- Dataset templates: `[{'name': 'small', 'start_n_samples': 50000, 'n_features': 40}, {'name': 'medium', 'start_n_samples': 140000, 'n_features': 80}, {'name': 'large', 'start_n_samples': 320000, 'n_features': 120}]`

## Overall ranking (lower is faster)
| model | median_total_s | mean_total_s | geo_mean_total_s | mean_peak_rss_mb | mean_r2 | max_r2_spread_for_matched_scenario |
| --- | --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 1.71717 | 2.61641 | 2.08921 | 301.768 | 0.7772 | 0.031585 |
| sklearn_hgb | 1.73392 | 1.42702 | 1.33515 | 286.072 | 0.768255 | 0.031585 |
| xgboost_hist | 2.85852 | 3.91468 | 3.12293 | 307.75 | 0.789119 | 0.031585 |


## Single-thread behavior
| dataset_name | model | n_samples | n_features | fit_seconds | predict_seconds | total_seconds | peak_rss_mb | r2 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| large | sklearn_hgb | 61917 | 120 | 1.74484 | 0.041366 | 1.79086 | 312.809 | 0.658936 |
| large | lightgbm_hist | 61917 | 120 | 5.40303 | 0.140132 | 5.54884 | 324.039 | 0.671273 |
| large | xgboost_hist | 61917 | 120 | 8.81728 | 0.0273871 | 8.8512 | 357.496 | 0.690521 |
| medium | sklearn_hgb | 100800 | 80 | 1.71564 | 0.0573106 | 1.78236 | 323.23 | 0.758211 |
| medium | lightgbm_hist | 100800 | 80 | 5.30792 | 0.225681 | 5.53393 | 346.426 | 0.76725 |
| medium | xgboost_hist | 100800 | 80 | 7.44774 | 0.0463557 | 7.49816 | 332.07 | 0.782466 |
| small | sklearn_hgb | 50000 | 40 | 0.73046 | 0.0263509 | 0.761486 | 221.176 | 0.88762 |
| small | lightgbm_hist | 50000 | 40 | 1.59721 | 0.111646 | 1.71717 | 222.738 | 0.893078 |
| small | xgboost_hist | 50000 | 40 | 2.58434 | 0.0213944 | 2.6115 | 229.434 | 0.894369 |


## Multi-thread scalability
| dataset_name | model | max_threads | fit_s_1_thread | fit_s_max_threads | speedup_vs_1_thread | parallel_efficiency |
| --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 4 | 5.40303 | 1.5738 | 3.43311 | 0.858276 |
| medium | lightgbm_hist | 4 | 5.30792 | 1.58981 | 3.33871 | 0.834676 |
| small | lightgbm_hist | 4 | 1.59721 | 0.584863 | 2.73091 | 0.682726 |
| large | sklearn_hgb | 4 | 1.74484 | 1.73629 | 1.00493 | 0.251231 |
| medium | sklearn_hgb | 4 | 1.71564 | 1.63521 | 1.04919 | 0.262297 |
| small | sklearn_hgb | 4 | 0.73046 | 0.725501 | 1.00683 | 0.251709 |
| large | xgboost_hist | 4 | 8.81728 | 2.84504 | 3.09918 | 0.774794 |
| medium | xgboost_hist | 4 | 7.44774 | 2.26321 | 3.29078 | 0.822696 |
| small | xgboost_hist | 4 | 2.58434 | 0.885271 | 2.91927 | 0.729817 |


## Memory growth trend (thread=1)
| model | smallest_samples | largest_samples | peak_mb_smallest | peak_mb_largest | approx_mb_per_1k_samples |
| --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 50000 | 100800 | 222.738 | 346.426 | 2.43479 |
| sklearn_hgb | 50000 | 100800 | 221.176 | 323.23 | 2.00895 |
| xgboost_hist | 50000 | 100800 | 229.434 | 332.07 | 2.02041 |


## Initial conclusion
- Best median runtime model: `lightgbm_hist`
- Least-performing median runtime model: `xgboost_hist`
- All scenarios report explicit `r2_spread_for_scenario` to verify score parity while keeping matched hyperparameter values.
