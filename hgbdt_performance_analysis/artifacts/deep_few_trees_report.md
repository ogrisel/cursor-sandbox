# Comparable large-run benchmark

## Constraints enforced
- n_estimators >= 10
- num_leaves/max_leaf_nodes >= 31
- timeout per single run: 10.0s
- candidate preset: `deep_few_trees`

## Calibration candidates (thread=1)
| candidate | n_estimators | num_leaves | n_samples | r2_spread | r2_mean | max_total_s |
| --- | --- | --- | --- | --- | --- | --- |
| cfg_deep_a_48x127 | 48 | 127 | 420000 | 0.000718 | 0.828658 | 4.4613 |
| cfg_deep_b_40x127 | 40 | 127 | 420000 | 0.000738 | 0.817841 | 4.0417 |
| cfg_deep_c_32x127 | 32 | 127 | 420000 | 0.001400 | 0.811077 | 3.4306 |
| cfg_deep_d_64x63 | 64 | 63 | 420000 | 0.001088 | 0.795512 | 4.6071 |
| cfg_deep_e_56x63 | 56 | 63 | 420000 | 0.001175 | 0.791656 | 3.9655 |
| cfg_deep_f_24x127 | 24 | 127 | 420000 | 0.000477 | 0.798157 | 3.0551 |

Best calibrated candidate: `cfg_deep_f_24x127`

## Final comparable timing table
(all runs on same dataset `n_samples=420000`, `n_features=32`, repeats=3)

| model | threads | fit_mean_s | predict_mean_s | total_mean_s | r2_mean | peak_rss_mean_mb | fitted_trees_mean |
| --- | --- | --- | --- | --- | --- | --- | --- |
| sklearn_hgb | 1 | 2.7226 | 0.1254 | 2.8525 | 0.807828 | 436.68 | 24.0 |
| xgboost_hist | 1 | 2.7889 | 0.0602 | 2.8538 | 0.807706 | 375.32 | 24.0 |
| lightgbm_hist | 1 | 2.7382 | 0.1599 | 2.9054 | 0.807691 | 395.90 | 24.0 |
| sklearn_hgb | 2 | 1.4914 | 0.0666 | 1.5637 | 0.807828 | 445.49 | 24.0 |
| lightgbm_hist | 2 | 1.4782 | 0.0845 | 1.5694 | 0.807691 | 404.23 | 24.0 |
| xgboost_hist | 2 | 1.6046 | 0.0318 | 1.6412 | 0.807706 | 381.39 | 24.0 |
| lightgbm_hist | 4 | 0.8314 | 0.0467 | 0.8822 | 0.807691 | 409.10 | 24.0 |
| sklearn_hgb | 4 | 0.8669 | 0.0370 | 0.9098 | 0.807828 | 458.03 | 24.0 |
| xgboost_hist | 4 | 0.9557 | 0.0163 | 0.9758 | 0.807706 | 390.65 | 24.0 |

## Final comparability check
- R² spread across libraries at thread=1: `0.000137`
- Fitted trees at thread=1: `[24, 24, 24]`
