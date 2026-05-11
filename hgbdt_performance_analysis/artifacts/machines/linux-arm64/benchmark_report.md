# Histogram GBDT Regressor Benchmark Report

## Experiment controls
- Timeout budget per individual run: `12.0 s`
- Adaptive reduction factor after timeout: `0.5`
- Threads tested: `[1, 2, 4, 8, 16]`
- Dataset templates: `[{'name': 'small', 'start_n_samples': 50000, 'n_features': 40}, {'name': 'medium', 'start_n_samples': 140000, 'n_features': 80}, {'name': 'large', 'start_n_samples': 320000, 'n_features': 120}]`

## Overall ranking (lower is faster)
| model | median_total_s | mean_total_s | geo_mean_total_s | mean_peak_rss_mb | mean_r2 | max_r2_spread_for_matched_scenario |
| --- | --- | --- | --- | --- | --- | --- |
| sklearn_hgb_fixed | 1.81815 | 2.28039 | 1.97275 | 268.837 | 0.782765 | 0.0177437 |
| lightgbm_hist | 2.5934 | 2.5759 | 2.26813 | 277.358 | 0.793002 | 0.0177437 |
| xgboost_hist | 2.6304 | 3.01534 | 2.55195 | 293.903 | 0.793637 | 0.0177437 |
| sklearn_hgb | 3.89908 | 3.93847 | 3.37202 | 273.439 | 0.782765 | 0.0177437 |


## Single-thread behavior
| dataset_name | model | n_samples | n_features | fit_seconds | predict_seconds | total_seconds | peak_rss_mb | r2 | fitted_trees | expected_trees | total_nodes | avg_nodes_per_tree |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 40000 | 120 | 4.96354 | 0.0837916 | 5.05014 | 278.715 | 0.692337 | 220 | 220 | 13420 | 61 |
| large | sklearn_hgb_fixed | 40000 | 120 | 5.28029 | 0.0947865 | 5.37545 | 278.5 | 0.675577 | 220 | 220 | 13420 | 61 |
| large | sklearn_hgb | 40000 | 120 | 5.37252 | 0.095904 | 5.4705 | 278.605 | 0.675577 | 220 | 220 | 13420 | 61 |
| large | xgboost_hist | 40000 | 120 | 7.49242 | 0.0201175 | 7.52196 | 319.324 | 0.69332 | 220 | 220 | 13420 | 61 |
| medium | lightgbm_hist | 70000 | 80 | 4.79567 | 0.143828 | 4.94366 | 296.742 | 0.79359 | 220 | 220 | 13420 | 61 |
| medium | sklearn_hgb_fixed | 70000 | 80 | 5.16941 | 0.143812 | 5.31872 | 287.316 | 0.785099 | 220 | 220 | 13420 | 61 |
| medium | sklearn_hgb | 70000 | 80 | 5.17056 | 0.143838 | 5.32284 | 287.074 | 0.785099 | 220 | 220 | 13420 | 61 |
| medium | xgboost_hist | 70000 | 80 | 6.53213 | 0.0328858 | 6.5727 | 315.594 | 0.793248 | 220 | 220 | 13420 | 61 |
| small | lightgbm_hist | 50000 | 40 | 1.92317 | 0.0998918 | 2.03354 | 234.801 | 0.893078 | 220 | 220 | 13420 | 61 |
| small | sklearn_hgb | 50000 | 40 | 2.20763 | 0.087049 | 2.30185 | 227.992 | 0.88762 | 220 | 220 | 13420 | 61 |
| small | sklearn_hgb_fixed | 50000 | 40 | 2.21866 | 0.0869531 | 2.30909 | 228.008 | 0.88762 | 220 | 220 | 13420 | 61 |
| small | xgboost_hist | 50000 | 40 | 2.60308 | 0.0233168 | 2.6304 | 240.82 | 0.894341 | 220 | 220 | 13420 | 61 |


## Multi-thread scalability
| dataset_name | model | max_threads | fit_s_1_thread | fit_s_max_threads | speedup_vs_1_thread | parallel_efficiency |
| --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 16 | 4.96354 | 3.45726 | 1.43569 | 0.0897303 |
| medium | lightgbm_hist | 16 | 4.79567 | 3.36004 | 1.42727 | 0.0892041 |
| small | lightgbm_hist | 16 | 1.92317 | 2.36159 | 0.814352 | 0.050897 |
| large | sklearn_hgb | 16 | 5.37252 | 6.77556 | 0.792927 | 0.0495579 |
| medium | sklearn_hgb | 16 | 5.17056 | 6.77116 | 0.763615 | 0.0477259 |
| small | sklearn_hgb | 16 | 2.20763 | 5.59956 | 0.394251 | 0.0246407 |
| large | sklearn_hgb_fixed | 16 | 5.28029 | 1.78273 | 2.96192 | 0.18512 |
| medium | sklearn_hgb_fixed | 16 | 5.16941 | 1.69812 | 3.0442 | 0.190263 |
| small | sklearn_hgb_fixed | 16 | 2.21866 | 0.93716 | 2.36743 | 0.147964 |
| large | xgboost_hist | 16 | 7.49242 | 2.7905 | 2.68498 | 0.167811 |
| medium | xgboost_hist | 16 | 6.53213 | 2.35846 | 2.76966 | 0.173104 |
| small | xgboost_hist | 16 | 2.60308 | 1.09323 | 2.38109 | 0.148818 |


## Memory growth trend (thread=1)
| model | smallest_samples | largest_samples | peak_mb_smallest | peak_mb_largest | approx_mb_per_1k_samples |
| --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 40000 | 70000 | 278.715 | 296.742 | 0.600911 |
| sklearn_hgb | 40000 | 70000 | 278.605 | 287.074 | 0.282292 |
| sklearn_hgb_fixed | 40000 | 70000 | 278.5 | 287.316 | 0.29388 |
| xgboost_hist | 40000 | 70000 | 319.324 | 315.594 | -0.124349 |


## Initial conclusion
- Best median runtime model: `sklearn_hgb_fixed`
- Least-performing median runtime model: `sklearn_hgb`
- All scenarios report explicit `r2_spread_for_scenario` to verify score parity while keeping matched hyperparameter values.
