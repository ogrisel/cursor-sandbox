# Deep-few-trees regime analysis

## Setup
- candidate preset: `deep_few_trees`
- selected candidate: `cfg_deep_f_24x127`
- dataset: n_samples=420000, n_features=32
- aligned params: n_estimators=24, max_depth=12, num_leaves=127

## Parity checks before performance analysis
- R2 spread at thread=1 (reference libs): 0.000137
- fitted-tree spread at thread=1 (reference libs): 0.0
- all calibration candidates have zero fitted-tree spread: True

## Efficiency ranking by thread (total_mean_s)
| threads | fastest | second | third |
| --- | --- | --- | --- |
| 1 | sklearn_hgb (2.8525s) | xgboost_hist (2.8538s) | lightgbm_hist (2.9054s) |
| 2 | sklearn_hgb (1.5637s) | lightgbm_hist (1.5694s) | xgboost_hist (1.6412s) |
| 4 | lightgbm_hist (0.8822s) | sklearn_hgb (0.9098s) | xgboost_hist (0.9758s) |

## Scalability snapshot (fit speedup vs 1-thread)
| model | speedup@4 | speedup@16 |
| --- | ---: | ---: |
| sklearn_hgb | 3.116 | 0.906 |
| xgboost_hist | 2.981 | 2.560 |
| lightgbm_hist | 3.284 | 1.636 |

## Answer
- No. In this regime, sklearn is marginally fastest at 1 and 2 threads, but LightGBM is fastest at 4 threads (best on-core wall-clock time).
