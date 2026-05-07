# Oversubscription root-cause validation

## Large dataset scalability

dataset: n_samples=176000 n_features=120

| model | t1_fit_s | t4_fit_s | t16_fit_s | speedup_t4 | speedup_t16 | r2_t1 | fitted_trees_t1 | effective_t16 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| lightgbm_hist | 6.8702 | 2.3818 | 3.3312 | 2.885 | 2.062 | 0.377898 | 160.0 | 16.0 |
| sklearn_hgb | 5.1773 | 1.6977 | 3.3867 | 3.050 | 1.529 | 0.377683 | 160.0 | 16.0 |
| sklearn_hgb_fixed | 5.0553 | 1.7317 | 1.7271 | 2.919 | 2.927 | 0.377683 | 160.0 | 4.0 |
| xgboost_hist | 7.4339 | 2.1679 | 2.2963 | 3.429 | 3.237 | 0.377761 | 160.0 | 16.0 |

r2_spread_t1_reference=0.000215
fitted_tree_spread_t1_reference=0.0


## Small dataset scalability

dataset: n_samples=60000 n_features=80

| model | t1_fit_s | t4_fit_s | t16_fit_s | speedup_t4 | speedup_t16 | r2_t1 | fitted_trees_t1 | effective_t16 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| lightgbm_hist | 1.6036 | 0.5430 | 1.0123 | 2.953 | 1.584 | 0.474927 | 160.0 | 16.0 |
| sklearn_hgb | 1.2986 | 0.5638 | 1.6283 | 2.303 | 0.798 | 0.475270 | 160.0 | 16.0 |
| sklearn_hgb_fixed | 1.3258 | 0.5445 | 0.5494 | 2.435 | 2.413 | 0.475270 | 160.0 | 4.0 |
| xgboost_hist | 1.8112 | 0.6637 | 0.7616 | 2.729 | 2.378 | 0.475644 | 160.0 | 16.0 |

r2_spread_t1_reference=0.000717
fitted_tree_spread_t1_reference=0.0


## OMP_WAIT_POLICY sensitivity at 16 threads (large dataset)

| model | fit_default_s | fit_passive_s | passive_over_default | r2_default | fitted_trees_default |
| --- | ---: | ---: | ---: | ---: | ---: |
| sklearn_hgb | 3.1054 | 3.6911 | 1.189 | 0.377683 | 160.0 |
| xgboost_hist | 2.3298 | 2.4213 | 1.039 | 0.377761 | 160.0 |
| lightgbm_hist | 3.4380 | 3.3962 | 0.988 | 0.377898 | 160.0 |

## Context-switch evidence (large dataset)

| model | requested_threads | fit_mean_s | fitted_trees_mean | voluntary_ctx_switches_mean | involuntary_ctx_switches_mean | cpu_time_over_wall |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| sklearn_hgb | 4 | 1.7040 | 160.0 | 49.3 | 260.0 | 3.344 |
| sklearn_hgb | 16 | 3.4528 | 160.0 | 16799.3 | 430.3 | 2.327 |
| sklearn_hgb_fixed | 16 | 1.7021 | 160.0 | 47.3 | 258.7 | 3.364 |
| xgboost_hist | 16 | 2.1708 | 160.0 | 110.3 | 94.3 | 3.514 |
| lightgbm_hist | 16 | 3.1916 | 160.0 | 7528.0 | 573.0 | 2.580 |
