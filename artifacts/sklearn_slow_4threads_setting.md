# Hyperparameter setting where sklearn is slower at 4 threads

## Selected setting
- Dataset: `n_samples=220000`, `n_features=8`
- Params:
  - `n_estimators=12`
  - `learning_rate=0.14`
  - `max_depth=12`
  - `num_leaves=255`
  - `min_samples_leaf=20`
  - `min_child_weight=20.0`
  - `l2_regularization=10.0`
  - `max_bin=255`
  - `subsample=1.0`
  - `min_split_gain=0.1`

## Parity checks
- Tree count parity (thread=1 and thread=4): passed for all seeds.
- Fitted-tree count equals expected `n_estimators` for all runs.
- Max cross-library R2 spread at thread=1 across seeds: `0.000467`.
- Max fit time observed in any run: `0.445s`.

## 4-thread slowdown result
- Slowdown metric: `sklearn_fit_4t / min(xgboost_fit_4t, lightgbm_fit_4t)`
- Mean over seeds: `1.367x`
- Min over seeds: `1.328x`
- Max over seeds: `1.409x`

This setting consistently makes sklearn slower than the best alternative at 4 threads while preserving R2 and tree-size parity constraints.
