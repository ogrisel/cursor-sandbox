# Detailed platform analysis: linux-amd64

- System: `Linux`
- Architecture: `x86_64`
- CPU count (logical): `4`
- Thread grid: `[1, 2, 4, 8, 16]`
- Native profile enabled: `True`

## Setting: `baseline_default`

![scalability-baseline_default](scalability.png)

### Parity checks (thread=1)

| dataset | model | r2 | fitted_trees | expected_trees | trees_match | total_nodes | avg_nodes_per_tree |
| --- | --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 0.634649 | 220 | 220 | True | 12342 | 56.1 |
| large | sklearn_hgb | 0.603268 | 220 | 220 | True | 12804 | 58.2 |
| large | sklearn_hgb_fixed | 0.603268 | 220 | 220 | True | 12804 | 58.2 |
| large | xgboost_hist | 0.636891 | 220 | 220 | True | 12378 | 56.2636 |
| medium | lightgbm_hist | 0.720404 | 220 | 220 | True | 13190 | 59.9545 |
| medium | sklearn_hgb | 0.687753 | 220 | 220 | True | 13340 | 60.6364 |
| medium | sklearn_hgb_fixed | 0.687753 | 220 | 220 | True | 13340 | 60.6364 |
| medium | xgboost_hist | 0.719562 | 220 | 220 | True | 13198 | 59.9909 |
| small | lightgbm_hist | 0.89957 | 220 | 220 | True | 13420 | 61 |
| small | sklearn_hgb | 0.891404 | 220 | 220 | True | 13420 | 61 |
| small | sklearn_hgb_fixed | 0.891404 | 220 | 220 | True | 13420 | 61 |
| small | xgboost_hist | 0.900025 | 220 | 220 | True | 13420 | 61 |

### Scalability summary

| dataset | model | max_threads | fit_s_1_thread | fit_s_max_threads | speedup_1_to_max |
| --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 16 | 1.66456 | 3.65439 | 0.455495 |
| large | sklearn_hgb | 16 | 1.52587 | 9.22585 | 0.16539 |
| large | sklearn_hgb_fixed | 16 | 1.51083 | 0.980294 | 1.5412 |
| large | xgboost_hist | 16 | 2.9774 | 2.0446 | 1.45623 |
| medium | lightgbm_hist | 16 | 1.44101 | 3.85009 | 0.37428 |
| medium | sklearn_hgb | 16 | 1.33509 | 9.87433 | 0.135208 |
| medium | sklearn_hgb_fixed | 16 | 1.39866 | 0.914233 | 1.52988 |
| medium | xgboost_hist | 16 | 2.3957 | 1.7199 | 1.39293 |
| small | lightgbm_hist | 16 | 1.561 | 4.18671 | 0.372846 |
| small | sklearn_hgb | 16 | 1.41925 | 10.2818 | 0.138034 |
| small | sklearn_hgb_fixed | 16 | 1.42159 | 0.926503 | 1.53436 |
| small | xgboost_hist | 16 | 2.13201 | 1.35468 | 1.57381 |

### Oversubscription regime summary (`cores=4`, `2x`, `4x`)

| dataset | model | fit_s_cores | fit_s_2x_cores | fit_s_4x_cores | fit_ratio_2x_vs_cores | fit_ratio_4x_vs_cores |
| --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 0.647445 | 2.12662 | 3.65439 | 3.28463 | 5.64433 |
| large | sklearn_hgb | 0.977212 | 4.94601 | 9.22585 | 5.06134 | 9.441 |
| large | sklearn_hgb_fixed | 0.975032 | 0.979941 | 0.980294 | 1.00504 | 1.0054 |
| large | xgboost_hist | 1.92174 | 2.0076 | 2.0446 | 1.04468 | 1.06393 |
| medium | lightgbm_hist | 0.58209 | 2.1256 | 3.85009 | 3.65167 | 6.61425 |
| medium | sklearn_hgb | 0.883226 | 5.17011 | 9.87433 | 5.85366 | 11.1798 |
| medium | sklearn_hgb_fixed | 0.889742 | 0.885297 | 0.914233 | 0.995005 | 1.02753 |
| medium | xgboost_hist | 1.53404 | 1.63773 | 1.7199 | 1.06759 | 1.12115 |
| small | lightgbm_hist | 0.712824 | 2.3291 | 4.18671 | 3.26742 | 5.87342 |
| small | sklearn_hgb | 0.91583 | 5.38681 | 10.2818 | 5.88189 | 11.2268 |
| small | sklearn_hgb_fixed | 0.922943 | 0.928175 | 0.926503 | 1.00567 | 1.00386 |
| small | xgboost_hist | 1.30678 | 1.34342 | 1.35468 | 1.02804 | 1.03666 |

### Underperformance findings

- No material sklearn underperformance flags detected for this setting under current thresholds.

## Setting: `deep_few_trees`

![scalability-deep_few_trees](scalability_deep_few_trees.png)

### Parity checks (thread=1)

| dataset | model | r2 | fitted_trees | expected_trees | trees_match | total_nodes | avg_nodes_per_tree |
| --- | --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 0.460974 | 48 | 48 | True | 12072 | 251.5 |
| large | sklearn_hgb | 0.443827 | 48 | 48 | True | 12032 | 250.667 |
| large | sklearn_hgb_fixed | 0.443827 | 48 | 48 | True | 12032 | 250.667 |
| large | xgboost_hist | 0.459013 | 48 | 48 | True | 12126 | 252.625 |
| medium | lightgbm_hist | 0.571939 | 48 | 48 | True | 12144 | 253 |
| medium | sklearn_hgb | 0.570187 | 48 | 48 | True | 12144 | 253 |
| medium | sklearn_hgb_fixed | 0.570187 | 48 | 48 | True | 12144 | 253 |
| medium | xgboost_hist | 0.571463 | 48 | 48 | True | 12144 | 253 |
| small | lightgbm_hist | 0.777653 | 48 | 48 | True | 12144 | 253 |
| small | sklearn_hgb | 0.775221 | 48 | 48 | True | 12144 | 253 |
| small | sklearn_hgb_fixed | 0.775221 | 48 | 48 | True | 12144 | 253 |
| small | xgboost_hist | 0.777123 | 48 | 48 | True | 12144 | 253 |

### Scalability summary

| dataset | model | max_threads | fit_s_1_thread | fit_s_max_threads | speedup_1_to_max |
| --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 16 | 1.70401 | 3.51771 | 0.48441 |
| large | sklearn_hgb | 16 | 1.59812 | 8.91853 | 0.179191 |
| large | sklearn_hgb_fixed | 16 | 1.60073 | 0.942795 | 1.69785 |
| large | xgboost_hist | 16 | 3.19278 | 2.06746 | 1.5443 |
| medium | lightgbm_hist | 16 | 1.60739 | 4.51889 | 0.355705 |
| medium | sklearn_hgb | 16 | 1.40911 | 10.1689 | 0.138571 |
| medium | sklearn_hgb_fixed | 16 | 1.41421 | 0.914895 | 1.54576 |
| medium | xgboost_hist | 16 | 2.61238 | 1.76894 | 1.4768 |
| small | lightgbm_hist | 16 | 1.17734 | 3.73819 | 0.314949 |
| small | sklearn_hgb | 16 | 1.1537 | 10.5815 | 0.10903 |
| small | sklearn_hgb_fixed | 16 | 1.16427 | 0.806397 | 1.44379 |
| small | xgboost_hist | 16 | 1.79014 | 1.22706 | 1.45889 |

### Oversubscription regime summary (`cores=4`, `2x`, `4x`)

| dataset | model | fit_s_cores | fit_s_2x_cores | fit_s_4x_cores | fit_ratio_2x_vs_cores | fit_ratio_4x_vs_cores |
| --- | --- | --- | --- | --- | --- | --- |
| large | lightgbm_hist | 0.812334 | 2.50235 | 3.51771 | 3.08045 | 4.33038 |
| large | sklearn_hgb | 1.05904 | 4.87771 | 8.91853 | 4.60578 | 8.42133 |
| large | sklearn_hgb_fixed | 0.945235 | 0.924751 | 0.942795 | 0.978329 | 0.997419 |
| large | xgboost_hist | 2.03168 | 2.06961 | 2.06746 | 1.01867 | 1.01762 |
| medium | lightgbm_hist | 0.671995 | 2.17251 | 4.51889 | 3.23292 | 6.72459 |
| medium | sklearn_hgb | 0.934299 | 5.32943 | 10.1689 | 5.7042 | 10.884 |
| medium | sklearn_hgb_fixed | 0.941859 | 0.924977 | 0.914895 | 0.982076 | 0.971371 |
| medium | xgboost_hist | 1.71346 | 1.73125 | 1.76894 | 1.01038 | 1.03238 |
| small | lightgbm_hist | 0.527079 | 1.97316 | 3.73819 | 3.74357 | 7.09227 |
| small | sklearn_hgb | 0.824036 | 5.45968 | 10.5815 | 6.62553 | 12.841 |
| small | sklearn_hgb_fixed | 0.809638 | 0.816946 | 0.806397 | 1.00903 | 0.995997 |
| small | xgboost_hist | 1.16677 | 1.227 | 1.22706 | 1.05163 | 1.05167 |

### Underperformance findings

- No material sklearn underperformance flags detected for this setting under current thresholds.

