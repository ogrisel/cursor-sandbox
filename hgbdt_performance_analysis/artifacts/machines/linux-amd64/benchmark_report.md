# Histogram GBDT Regressor Benchmark Report

## Experiment controls
- Timeout budget per individual run: `20.0 s`
- Adaptive reduction factor after timeout: `0.6`
- Threads tested: `[1, 2, 4, 8]`
- Dataset templates: `[{'name': 'small', 'start_n_samples': 12000, 'n_features': 24}, {'name': 'medium', 'start_n_samples': 180000, 'n_features': 120}]`

## Overall ranking (lower is faster)
| model | median_total_s | mean_total_s | geo_mean_total_s | mean_peak_rss_mb | mean_r2 | max_r2_spread_for_matched_scenario |
| --- | --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 3.64099 | 4.58109 | 3.4874 | 338.991 | 0.817217 | 0.0120533 |
| sklearn_hgb_fixed | 3.77181 | 4.37362 | 3.3844 | 311.631 | 0.807714 | 0.0120533 |
| sklearn_hgb | 4.77289 | 5.04672 | 3.97738 | 312.808 | 0.807714 | 0.0120533 |
| xgboost_hist | 4.96634 | 5.60449 | 4.15744 | 326.783 | 0.817468 | 0.0120533 |


## Single-thread behavior
| dataset_name | model | n_samples | n_features | fit_seconds | predict_seconds | total_seconds | peak_rss_mb | r2 | fitted_trees | expected_trees | total_nodes | avg_nodes_per_tree |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| medium | sklearn_hgb_fixed | 108000 | 120 | 10.0283 | 0.32626 | 10.6838 | 411.66 | 0.673129 | 220 | 220 | 13420 | 61 |
| medium | sklearn_hgb | 108000 | 120 | 10.1744 | 0.345745 | 10.8737 | 411.402 | 0.673129 | 220 | 220 | 13420 | 61 |
| medium | lightgbm_hist | 108000 | 120 | 10.8823 | 0.288887 | 11.4646 | 462.727 | 0.685065 | 220 | 220 | 13420 | 61 |
| medium | xgboost_hist | 108000 | 120 | 12.9392 | 0.0583979 | 13.466 | 436.328 | 0.685182 | 220 | 220 | 13420 | 61 |
| small | lightgbm_hist | 12000 | 24 | 0.568576 | 0.0317106 | 1.652 | 206.531 | 0.949369 | 220 | 220 | 13386 | 60.8455 |
| small | sklearn_hgb_fixed | 12000 | 24 | 0.690888 | 0.0265258 | 1.8955 | 202.344 | 0.942299 | 220 | 220 | 13414 | 60.9727 |
| small | sklearn_hgb | 12000 | 24 | 0.695147 | 0.0257058 | 1.91119 | 202.336 | 0.942299 | 220 | 220 | 13414 | 60.9727 |
| small | xgboost_hist | 12000 | 24 | 0.866713 | 0.00642383 | 2.23573 | 215.004 | 0.949753 | 220 | 220 | 13390 | 60.8636 |


## Multi-thread scalability
| dataset_name | model | max_threads | fit_s_1_thread | fit_s_max_threads | speedup_vs_1_thread | parallel_efficiency |
| --- | --- | --- | --- | --- | --- | --- |
| medium | lightgbm_hist | 8 | 10.8823 | 6.01795 | 1.80831 | 0.226039 |
| small | lightgbm_hist | 8 | 0.568576 | 1.35543 | 0.419479 | 0.0524349 |
| medium | sklearn_hgb | 8 | 10.1744 | 8.11518 | 1.25375 | 0.156719 |
| small | sklearn_hgb | 8 | 0.695147 | 3.43328 | 0.202473 | 0.0253091 |
| medium | sklearn_hgb_fixed | 8 | 10.0283 | 5.03006 | 1.99368 | 0.249209 |
| small | sklearn_hgb_fixed | 8 | 0.690888 | 0.564677 | 1.22351 | 0.152939 |
| medium | xgboost_hist | 8 | 12.9392 | 7.43705 | 1.73983 | 0.217479 |
| small | xgboost_hist | 8 | 0.866713 | 0.719384 | 1.2048 | 0.1506 |


## Memory growth trend (thread=1)
| model | smallest_samples | largest_samples | peak_mb_smallest | peak_mb_largest | approx_mb_per_1k_samples |
| --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 12000 | 108000 | 206.531 | 462.727 | 2.6687 |
| sklearn_hgb | 12000 | 108000 | 202.336 | 411.402 | 2.17778 |
| sklearn_hgb_fixed | 12000 | 108000 | 202.344 | 411.66 | 2.18038 |
| xgboost_hist | 12000 | 108000 | 215.004 | 436.328 | 2.30546 |


## Initial conclusion
- Best median runtime model: `lightgbm_hist`
- Least-performing median runtime model: `xgboost_hist`
- All scenarios report explicit `r2_spread_for_scenario` to verify score parity while keeping matched hyperparameter values.
