# Comparable large-run benchmark

## Constraints enforced
- n_estimators >= 10
- num_leaves/max_leaf_nodes >= 31
- timeout per single run: 20.0s
- candidate preset: `balanced`
- calibration mode: `reuse`
- calibration config: `precalibrated\comparable_large_balanced.json`

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
| sklearn_hgb | 1 | 9.1992 | 1.8017 | 11.0048 | 0.432733 | 553.06 | 120.0 |
| lightgbm_hist | 1 | 11.6926 | 0.2599 | 12.2136 | 0.432522 | 624.83 | 120.0 |
| xgboost_hist | 1 | 12.1195 | 0.0795 | 12.6811 | 0.432821 | 536.37 | 120.0 |
| sklearn_hgb | 2 | 5.2176 | 0.8404 | 6.0591 | 0.432733 | 553.52 | 120.0 |
| lightgbm_hist | 2 | 7.0060 | 0.1414 | 7.5736 | 0.432522 | 628.57 | 120.0 |
| xgboost_hist | 2 | 7.6467 | 0.0420 | 8.1564 | 0.432821 | 534.55 | 120.0 |
| sklearn_hgb | 4 | 4.2019 | 0.4187 | 5.0439 | 0.432733 | 553.65 | 120.0 |
| lightgbm_hist | 4 | 4.9857 | 0.0870 | 5.5160 | 0.432522 | 628.20 | 120.0 |
| xgboost_hist | 4 | 6.3433 | 0.0368 | 6.8679 | 0.432821 | 535.07 | 120.0 |

## Final comparability check
- R² spread across libraries at thread=1: `0.000299`
- Fitted trees at thread=1: `[120, 120, 120]`
