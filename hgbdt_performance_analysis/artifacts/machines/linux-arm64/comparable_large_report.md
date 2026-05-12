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
| sklearn_hgb | 1 | 8.4838 | 0.3356 | 9.1648 | 0.432733 | 589.98 | 120.0 |
| lightgbm_hist | 1 | 9.4689 | 0.1900 | 10.0471 | 0.432522 | 701.93 | 120.0 |
| xgboost_hist | 1 | 10.2135 | 0.0433 | 10.7395 | 0.432821 | 611.75 | 120.0 |
| sklearn_hgb | 2 | 4.3154 | 0.1408 | 4.8854 | 0.432733 | 603.26 | 120.0 |
| lightgbm_hist | 2 | 4.9690 | 0.0980 | 5.5590 | 0.432522 | 705.82 | 120.0 |
| xgboost_hist | 2 | 6.7089 | 0.0222 | 7.2217 | 0.432821 | 611.77 | 120.0 |
| sklearn_hgb | 4 | 2.3205 | 0.0741 | 2.8416 | 0.432733 | 611.99 | 120.0 |
| lightgbm_hist | 4 | 2.7180 | 0.0498 | 3.2704 | 0.432522 | 721.52 | 120.0 |
| xgboost_hist | 4 | 2.8158 | 0.0116 | 3.3304 | 0.432821 | 612.56 | 120.0 |

## Final comparability check
- R² spread across libraries at thread=1: `0.000299`
- Fitted trees at thread=1: `[120, 120, 120]`
