# Oversubscription root-cause validation

## Large dataset scalability

dataset: n_samples=176000 n_features=120

| model | t1_fit_s | t4_fit_s | t16_fit_s | speedup_t4 | speedup_t16 | r2_t1 | effective_t16 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| lightgbm_hist | 7.4662 | 2.5470 | 4.4857 | 2.931 | 1.664 | 0.667387 | 16.0 |
| sklearn_hgb | 5.9361 | 2.1565 | 5.7580 | 2.753 | 1.031 | 0.666439 | 16.0 |
| sklearn_hgb_fixed | 5.9037 | 2.0515 | 1.9842 | 2.878 | 2.975 | 0.666439 | 4.0 |
| xgboost_hist | 8.0732 | 2.6057 | 2.8901 | 3.098 | 2.793 | 0.667537 | 16.0 |

r2_spread_t1_reference=0.001098


## Small dataset scalability

dataset: n_samples=60000 n_features=80

| model | t1_fit_s | t4_fit_s | t16_fit_s | speedup_t4 | speedup_t16 | r2_t1 | effective_t16 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| lightgbm_hist | 1.8785 | 0.6895 | 1.8818 | 2.724 | 0.998 | 0.762142 | 16.0 |
| sklearn_hgb | 1.7310 | 0.6270 | 2.4730 | 2.761 | 0.700 | 0.761806 | 16.0 |
| sklearn_hgb_fixed | 1.6720 | 0.6306 | 0.6283 | 2.652 | 2.661 | 0.761806 | 4.0 |
| xgboost_hist | 2.3327 | 0.8400 | 0.9461 | 2.777 | 2.466 | 0.763135 | 16.0 |

r2_spread_t1_reference=0.001329


## OMP_WAIT_POLICY sensitivity at 16 threads (large dataset)

| model | fit_default_s | fit_passive_s | passive_over_default | r2_default | r2_passive |
| --- | ---: | ---: | ---: | ---: | ---: |
| sklearn_hgb | 4.7808 | 5.9438 | 1.243 | 0.666439 | 0.666439 |
| xgboost_hist | 2.5732 | 3.2477 | 1.262 | 0.667537 | 0.667537 |
| lightgbm_hist | 4.1871 | 4.6209 | 1.104 | 0.667387 | 0.667387 |

## Context-switch evidence (large dataset)

| model | requested_threads | fit_mean_s | voluntary_ctx_switches_mean | involuntary_ctx_switches_mean | cpu_time_over_wall |
| --- | ---: | ---: | ---: | ---: | ---: |
| sklearn_hgb | 4 | 1.9658 | 54.7 | 290.0 | 3.343 |
| sklearn_hgb | 16 | 6.5500 | 50412.0 | 332.0 | 2.095 |
| sklearn_hgb_fixed | 16 | 2.0381 | 55.0 | 313.3 | 3.366 |
| xgboost_hist | 16 | 2.6468 | 204.3 | 180.0 | 3.548 |
| lightgbm_hist | 16 | 4.6997 | 19797.7 | 291.7 | 2.321 |
