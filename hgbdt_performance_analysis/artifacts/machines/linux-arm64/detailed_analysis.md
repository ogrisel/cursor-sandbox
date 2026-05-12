# Detailed platform analysis: linux-arm64

- System: `Linux`
- Architecture: `aarch64`
- CPU count (logical): `4`
- CPU count (physical): `4`
- Hyper-threading enabled: `False`
- CPU model: `Neoverse-N2`
- Core type counts: `{'performance': 4, 'efficiency': None, 'low_power': None}`
- CFS/CPU quota: `n/a`
- CPU set: `0-3`
- Thread grid: `[1, 2, 4, 8]`
- Native profile enabled: `True`

## Setting: `baseline_default`

![scalability-baseline_default](scalability.png)

![absolute-fit-time-baseline_default](fit_time_threads.png)

_Vertical markers denote `cores=4` and `2x=8` thread regimes._

### Parity checks (thread=1)

| dataset | model | r2 | fitted_trees | expected_trees | trees_match | total_nodes | avg_nodes_per_tree |
| --- | --- | --- | --- | --- | --- | --- | --- |
| medium | lightgbm_hist | 0.586641 | 220 | 220 | True | 11256 | 51.1636 |
| medium | sklearn_hgb | 0.529888 | 220 | 220 | True | 12398 | 56.3545 |
| medium | sklearn_hgb_fixed | 0.529888 | 220 | 220 | True | 12398 | 56.3545 |
| medium | xgboost_hist | 0.585335 | 220 | 220 | True | 11618 | 52.8091 |
| small | lightgbm_hist | 0.949369 | 220 | 220 | True | 13386 | 60.8455 |
| small | sklearn_hgb | 0.942299 | 220 | 220 | True | 13414 | 60.9727 |
| small | sklearn_hgb_fixed | 0.942299 | 220 | 220 | True | 13414 | 60.9727 |
| small | xgboost_hist | 0.949753 | 220 | 220 | True | 13390 | 60.8636 |

### Scalability summary (`1 -> cores=4`)

| dataset | model | max_regular_threads | fit_s_1_thread | fit_s_regular_max_threads | speedup_1_to_regular_max |
| --- | --- | --- | --- | --- | --- |
| medium | lightgbm_hist | 4 | 1.10252 | 0.365664 | 3.01512 |
| medium | sklearn_hgb | 4 | 1.47773 | 0.7138 | 2.07024 |
| medium | sklearn_hgb_fixed | 4 | 1.41 | 0.701933 | 2.00874 |
| medium | xgboost_hist | 4 | 2.01045 | 0.933167 | 2.15443 |
| small | lightgbm_hist | 4 | 0.538086 | 0.212916 | 2.52722 |
| small | sklearn_hgb | 4 | 0.721377 | 0.516931 | 1.3955 |
| small | sklearn_hgb_fixed | 4 | 0.713696 | 0.508048 | 1.40478 |
| small | xgboost_hist | 4 | 0.82913 | 0.420298 | 1.97272 |

### Oversubscription regime summary (`cores=4`, `2x`)

| dataset | model | fit_s_cores | fit_s_2x_cores | fit_ratio_2x_vs_cores |
| --- | --- | --- | --- | --- |
| medium | lightgbm_hist | 0.365664 | 1.18558 | 3.24226 |
| medium | sklearn_hgb | 0.7138 | 3.03858 | 4.2569 |
| medium | sklearn_hgb_fixed | 0.701933 | 0.700618 | 0.998126 |
| medium | xgboost_hist | 0.933167 | 0.93006 | 0.996671 |
| small | lightgbm_hist | 0.212916 | 1.30255 | 6.11765 |
| small | sklearn_hgb | 0.516931 | 3.05519 | 5.91024 |
| small | sklearn_hgb_fixed | 0.508048 | 0.501788 | 0.987679 |
| small | xgboost_hist | 0.420298 | 0.410092 | 0.975718 |

### Underperformance findings and root cause analysis

- Root cause signal: Python-level dispatch/orchestration contributes meaningfully to sklearn runtime.
- Issue (single_thread, dataset `medium`): Best sklearn total is 1.192x slower than best alternative at thread=1.
  - Implementation plan:
    - Move short-lived orchestration loops to Cython/C-level helpers.
    - Preallocate and reuse temporary buffers in split and histogram kernels.
    - Add lightweight fast paths for small-node splits to bypass heavy orchestration.
- Issue (single_thread, dataset `small`): Best sklearn total is 1.206x slower than best alternative at thread=1.
  - Implementation plan:
    - Move short-lived orchestration loops to Cython/C-level helpers.
    - Preallocate and reuse temporary buffers in split and histogram kernels.
    - Add lightweight fast paths for small-node splits to bypass heavy orchestration.
- Issue (scalability, dataset `medium`): Best sklearn speedup trails best alternative by 0.945 (1->regular max threads).
  - Implementation plan:
    - Move short-lived orchestration loops to Cython/C-level helpers.
    - Preallocate and reuse temporary buffers in split and histogram kernels.
    - Add lightweight fast paths for small-node splits to bypass heavy orchestration.
- Issue (scalability, dataset `small`): Best sklearn speedup trails best alternative by 1.122 (1->regular max threads).
  - Implementation plan:
    - Move short-lived orchestration loops to Cython/C-level helpers.
    - Preallocate and reuse temporary buffers in split and histogram kernels.
    - Add lightweight fast paths for small-node splits to bypass heavy orchestration.

