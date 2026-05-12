# Comparable large-run benchmark

## Constraints enforced
- n_estimators >= 10
- num_leaves/max_leaf_nodes >= 31
- timeout per single run: 20.0s
- candidate preset: `balanced`
- calibration mode: `reuse`
- calibration config: `precalibrated/comparable_large_balanced.json`

## Calibration candidates (thread=1)
| candidate | n_estimators | num_leaves | n_samples | r2_spread | r2_mean | max_total_s |
| --- | --- | --- | --- | --- | --- | --- |
| cfg_a_balanced_120 | 120 | 31 | 220000 | 0.000299 | 0.432692 | 9.1830 |
| cfg_b_regularized_90 | 90 | 31 | 220000 | 0.001107 | 0.444624 | 7.6821 |
| cfg_c_shallow_160 | 160 | 31 | 220000 | 0.000718 | 0.377509 | 9.4759 |
| cfg_d_deeper_80 | 80 | 31 | 220000 | 0.000701 | 0.524291 | 9.0696 |
| cfg_e_more_leaves_100 | 100 | 63 | 220000 | 0.001214 | 0.490284 | 9.4452 |
| cfg_f_small_forest_40 | 40 | 31 | 220000 | 0.000513 | 0.378509 | 5.6626 |

Best calibrated candidate: `cfg_a_balanced_120`

## Final comparable timing table
(all runs on same dataset `n_samples=220000`, `n_features=120`, repeats=1)

| model | threads | fit_mean_s | predict_mean_s | total_mean_s | r2_mean | peak_rss_mean_mb | fitted_trees_mean |
| --- | --- | --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 1 | 8.0822 | 0.1274 | 8.5987 | 0.432522 | 808.70 | 120.0 |
| xgboost_hist | 1 | 8.2206 | 0.0350 | 8.7651 | 0.432821 | 635.03 | 120.0 |
| sklearn_hgb | 1 | 8.5885 | 0.5205 | 9.6300 | 0.432733 | 606.67 | 120.0 |
| sklearn_hgb | 2 | 4.3836 | 0.2634 | 4.9239 | 0.432733 | 607.52 | 120.0 |
| xgboost_hist | 2 | 4.3425 | 0.0184 | 4.9341 | 0.432821 | 644.58 | 120.0 |
| lightgbm_hist | 2 | 4.5362 | 0.0688 | 5.0988 | 0.432522 | 758.53 | 120.0 |
| xgboost_hist | 4 | 3.0864 | 0.0120 | 3.5980 | 0.432821 | 633.28 | 120.0 |
| lightgbm_hist | 4 | 4.0410 | 0.0458 | 4.5579 | 0.432522 | 770.22 | 120.0 |
| sklearn_hgb | 4 | 4.0237 | 0.2557 | 4.5606 | 0.432733 | 600.94 | 120.0 |

## Final comparability check
- R² spread across libraries at thread=1: `0.000299`
- Fitted trees at thread=1: `[120, 120, 120]`
