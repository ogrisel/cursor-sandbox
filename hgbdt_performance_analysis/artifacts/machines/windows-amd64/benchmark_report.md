# Histogram GBDT Regressor Benchmark Report

## Experiment controls
- Timeout budget per individual run: `20.0 s`
- Adaptive reduction factor after timeout: `0.6`
- Threads tested: `[1, 2, 4, 8]`
- Dataset templates: `[{'name': 'small', 'start_n_samples': 12000, 'n_features': 24}, {'name': 'medium', 'start_n_samples': 180000, 'n_features': 120}]`

## Overall ranking (lower is faster)
| model | median_total_s | mean_total_s | geo_mean_total_s | mean_peak_rss_mb | mean_r2 | max_r2_spread_for_matched_scenario |
| --- | --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 3.84599 | 4.98353 | 3.71133 | 278.416 | 0.817217 | 0.0119361 |
| sklearn_hgb_fixed | 4.52713 | 5.44128 | 4.10436 | 265.093 | 0.807714 | 0.0119361 |
| sklearn_hgb | 4.62287 | 5.6038 | 4.26807 | 265.477 | 0.807714 | 0.0119361 |
| xgboost_hist | 5.85475 | 6.86067 | 4.74741 | 282.155 | 0.816535 | 0.0119361 |


## Single-thread behavior
| dataset_name | model | n_samples | n_features | fit_seconds | predict_seconds | total_seconds | peak_rss_mb | r2 | fitted_trees | expected_trees | total_nodes | avg_nodes_per_tree |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| medium | lightgbm_hist | 108000 | 120 | 12.3364 | 0.332884 | 13.0084 | 384.773 | 0.685065 | 220 | 220 | 13420 | 61 |
| medium | sklearn_hgb_fixed | 108000 | 120 | 12.714 | 1.38846 | 14.1072 | 365.281 | 0.673129 | 220 | 220 | 13420 | 61 |
| medium | sklearn_hgb | 108000 | 120 | 12.7535 | 1.67357 | 14.4312 | 364.957 | 0.673129 | 220 | 220 | 13420 | 61 |
| medium | xgboost_hist | 108000 | 120 | 15.6394 | 0.0848702 | 16.157 | 396.836 | 0.684843 | 220 | 220 | 13420 | 61 |
| small | xgboost_hist | 12000 | 24 | 1.1664 | 0.00847667 | 1.67293 | 166.781 | 0.948866 | 220 | 220 | 13394 | 60.8818 |
| small | lightgbm_hist | 12000 | 24 | 0.723327 | 0.0366882 | 1.9692 | 166.156 | 0.949369 | 220 | 220 | 13386 | 60.8455 |
| small | sklearn_hgb | 12000 | 24 | 0.893586 | 0.0679236 | 2.33895 | 164.422 | 0.942299 | 220 | 220 | 13414 | 60.9727 |
| small | sklearn_hgb_fixed | 12000 | 24 | 0.902376 | 0.0674681 | 2.34793 | 164.57 | 0.942299 | 220 | 220 | 13414 | 60.9727 |


## Multi-thread scalability
| dataset_name | model | max_threads | fit_s_1_thread | fit_s_max_threads | speedup_vs_1_thread | parallel_efficiency |
| --- | --- | --- | --- | --- | --- | --- |
| medium | lightgbm_hist | 8 | 12.3364 | 5.39866 | 2.28508 | 0.285635 |
| small | lightgbm_hist | 8 | 0.723327 | 0.431244 | 1.6773 | 0.209663 |
| medium | sklearn_hgb | 8 | 12.7535 | 6.45909 | 1.97451 | 0.246813 |
| small | sklearn_hgb | 8 | 0.893586 | 0.948828 | 0.941778 | 0.117722 |
| medium | sklearn_hgb_fixed | 8 | 12.714 | 6.23939 | 2.0377 | 0.254713 |
| small | sklearn_hgb_fixed | 8 | 0.902376 | 0.697777 | 1.29322 | 0.161652 |
| medium | xgboost_hist | 8 | 15.6394 | 9.02686 | 1.73254 | 0.216567 |
| small | xgboost_hist | 8 | 1.1664 | 0.756086 | 1.54268 | 0.192835 |


## Memory growth trend (thread=1)
| model | smallest_samples | largest_samples | peak_mb_smallest | peak_mb_largest | approx_mb_per_1k_samples |
| --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 12000 | 108000 | 166.156 | 384.773 | 2.27726 |
| sklearn_hgb | 12000 | 108000 | 164.422 | 364.957 | 2.08891 |
| sklearn_hgb_fixed | 12000 | 108000 | 164.57 | 365.281 | 2.09074 |
| xgboost_hist | 12000 | 108000 | 166.781 | 396.836 | 2.3964 |


## Initial conclusion
- Best median runtime model: `lightgbm_hist`
- Least-performing median runtime model: `xgboost_hist`
- All scenarios report explicit `r2_spread_for_scenario` to verify score parity while keeping matched hyperparameter values.
