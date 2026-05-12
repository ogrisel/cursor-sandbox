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
| sklearn_hgb | 1 | 8.6211 | 0.4764 | 9.5763 | 0.432733 | 599.46 | 120.0 |
| xgboost_hist | 1 | 10.3454 | 0.0489 | 10.8908 | 0.432821 | 621.41 | 120.0 |
| lightgbm_hist | 1 | 10.6211 | 0.2284 | 11.3122 | 0.432522 | 711.26 | 120.0 |
| sklearn_hgb | 2 | 4.2321 | 0.2034 | 4.8480 | 0.432733 | 613.11 | 120.0 |
| xgboost_hist | 2 | 5.2356 | 0.0252 | 5.7414 | 0.432821 | 621.50 | 120.0 |
| lightgbm_hist | 2 | 5.6208 | 0.1183 | 6.2155 | 0.432522 | 728.11 | 120.0 |
| sklearn_hgb | 4 | 3.8586 | 0.1851 | 4.4234 | 0.432733 | 624.07 | 120.0 |
| xgboost_hist | 4 | 4.8542 | 0.0293 | 5.3824 | 0.432821 | 622.36 | 120.0 |
| lightgbm_hist | 4 | 4.9211 | 0.0720 | 5.4296 | 0.432522 | 728.44 | 120.0 |

## Final comparability check
- R² spread across libraries at thread=1: `0.000299`
- Fitted trees at thread=1: `[120, 120, 120]`
