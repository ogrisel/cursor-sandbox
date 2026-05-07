# Comparable large-run benchmark (floor-constrained)

## Constraints enforced
- n_estimators >= 10
- num_leaves/max_leaf_nodes >= 31

## Shared aligned parameters
- n_estimators: 120
- learning_rate: 0.1
- max_depth: 5
- num_leaves: 31
- max_bin: 255
- subsample: 1.0
- l2_regularization: 0.0
- min_samples_leaf: 20
- min_child_weight: 20.0
- min_split_gain: 0.0
- random_state: 42
- loss: squared_error

## Parameter-name validation
- Validation method: sklearn/xgboost via `get_params`; lightgbm via `_ConfigAliases` registry
- sklearn kwargs valid: True
- xgboost kwargs valid: True
- lightgbm kwargs valid: True

## R2 floor check (thread=1)
- sklearn default r2 floor: 0.639393
- min aligned r2 across libraries: 0.650715
- all aligned models >= floor: True
- aligned r2 spread across libraries (t1): 0.001756

## Final comparable timing table
| model | threads | fit_mean_s | predict_mean_s | total_mean_s | r2_mean |
| --- | --- | --- | --- | --- | --- |
| sklearn_hgb | 1 | 1.8776 | 0.0725 | 1.9501 | 0.650715 |
| lightgbm_hist | 1 | 7.4870 | 0.1889 | 7.6760 | 0.652471 |
| xgboost_hist | 1 | 8.0348 | 0.0397 | 8.0745 | 0.652319 |
| sklearn_hgb | 2 | 1.8774 | 0.0742 | 1.9516 | 0.650715 |
| lightgbm_hist | 2 | 4.1939 | 0.0972 | 4.2912 | 0.652471 |
| xgboost_hist | 2 | 4.4489 | 0.0231 | 4.4720 | 0.652319 |
| sklearn_hgb | 4 | 1.8830 | 0.0734 | 1.9565 | 0.650715 |
| xgboost_hist | 4 | 2.5666 | 0.0140 | 2.5805 | 0.652319 |
| lightgbm_hist | 4 | 2.6341 | 0.0530 | 2.6871 | 0.652471 |
