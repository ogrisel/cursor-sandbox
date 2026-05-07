# Comparable large-run benchmark

## Constraints enforced
- n_estimators >= 10
- num_leaves/max_leaf_nodes >= 31
- timeout per single run: 10.0s

## Calibration candidates (thread=1)
| candidate | n_estimators | num_leaves | n_samples | r2_spread | r2_mean | max_total_s |
| --- | --- | --- | --- | --- | --- | --- |
| cfg_a_balanced_120 | 120 | 31 | 176000 | 0.001381 | 0.420144 | 7.2838 |
| cfg_b_regularized_90 | 90 | 31 | 220000 | 0.001107 | 0.444624 | 7.2585 |
| cfg_c_shallow_160 | 160 | 31 | 176000 | 0.000191 | 0.365216 | 7.4470 |
| cfg_d_deeper_80 | 80 | 31 | 176000 | 0.003077 | 0.509644 | 7.1432 |
| cfg_e_more_leaves_100 | 100 | 63 | 176000 | 0.000634 | 0.477645 | 7.5747 |
| cfg_f_small_forest_40 | 40 | 31 | 220000 | 0.000513 | 0.378509 | 5.2270 |

Best calibrated candidate: `cfg_c_shallow_160`

## Final comparable timing table
(all runs on same dataset `n_samples=176000`, `n_features=120`, repeats=3)

| model | threads | fit_mean_s | predict_mean_s | total_mean_s | r2_mean | peak_rss_mean_mb | fitted_trees_mean |
| --- | --- | --- | --- | --- | --- | --- | --- |
| sklearn_hgb | 1 | 5.0540 | 0.2675 | 5.3280 | 0.377683 | 509.98 | 160.0 |
| lightgbm_hist | 1 | 6.8619 | 0.1590 | 7.0253 | 0.377898 | 640.66 | 160.0 |
| xgboost_hist | 1 | 7.3142 | 0.0357 | 7.3541 | 0.377761 | 523.71 | 160.0 |
| sklearn_hgb | 2 | 2.7295 | 0.1454 | 2.8812 | 0.377683 | 522.06 | 160.0 |
| xgboost_hist | 2 | 3.7936 | 0.0194 | 3.8165 | 0.377761 | 523.30 | 160.0 |
| lightgbm_hist | 2 | 3.8219 | 0.0833 | 3.9138 | 0.377898 | 643.19 | 160.0 |
| sklearn_hgb | 4 | 1.5227 | 0.0792 | 1.6068 | 0.377683 | 531.88 | 160.0 |
| xgboost_hist | 4 | 2.0521 | 0.0109 | 2.0661 | 0.377761 | 522.85 | 160.0 |
| lightgbm_hist | 4 | 2.2297 | 0.0445 | 2.2796 | 0.377898 | 645.28 | 160.0 |

## Final comparability check
- R² spread across libraries at thread=1: `0.000215`
- Fitted trees at thread=1: `[160, 160, 160]`
