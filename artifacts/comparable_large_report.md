# Comparable large-run benchmark

## Constraints enforced
- n_estimators >= 10
- num_leaves/max_leaf_nodes >= 31
- timeout per single run: 10.0s

## Calibration candidates (thread=1)
| candidate | n_estimators | num_leaves | n_samples | r2_spread | r2_mean | max_total_s |
| --- | --- | --- | --- | --- | --- | --- |
| cfg_a_balanced_120 | 120 | 31 | 176000 | 0.001381 | 0.420144 | 7.1461 |
| cfg_b_regularized_90 | 90 | 31 | 220000 | 0.001107 | 0.444624 | 7.2173 |
| cfg_c_shallow_160 | 160 | 31 | 176000 | 0.000191 | 0.365216 | 7.5658 |
| cfg_d_deeper_80 | 80 | 31 | 176000 | 0.003077 | 0.509644 | 7.2027 |
| cfg_e_more_leaves_100 | 100 | 63 | 176000 | 0.000634 | 0.477645 | 7.4263 |
| cfg_f_small_forest_40 | 40 | 31 | 220000 | 0.000513 | 0.378509 | 5.1922 |

Best calibrated candidate: `cfg_c_shallow_160`

## Final comparable timing table
(all runs on same dataset `n_samples=176000`, `n_features=120`, repeats=3)

| model | threads | fit_mean_s | predict_mean_s | total_mean_s | r2_mean | peak_rss_mean_mb |
| --- | --- | --- | --- | --- | --- | --- |
| sklearn_hgb | 1 | 5.0687 | 0.2703 | 5.3464 | 0.377683 | 499.08 |
| lightgbm_hist | 1 | 6.8487 | 0.1605 | 7.0111 | 0.377898 | 630.61 |
| xgboost_hist | 1 | 7.4122 | 0.0414 | 7.4625 | 0.377761 | 511.30 |
| sklearn_hgb | 2 | 2.7139 | 0.1483 | 2.8697 | 0.377683 | 507.51 |
| xgboost_hist | 2 | 3.8114 | 0.0202 | 3.8354 | 0.377761 | 511.54 |
| lightgbm_hist | 2 | 3.7729 | 0.0839 | 3.8613 | 0.377898 | 631.24 |
| sklearn_hgb | 4 | 1.6654 | 0.0940 | 1.7661 | 0.377683 | 518.14 |
| xgboost_hist | 4 | 2.0497 | 0.0124 | 2.0673 | 0.377761 | 510.81 |
| lightgbm_hist | 4 | 2.1875 | 0.0444 | 2.2361 | 0.377898 | 636.37 |

## Final comparability check
- R² spread across libraries at thread=1: `0.000215`
