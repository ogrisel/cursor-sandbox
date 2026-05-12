# Platform-specific benchmark conclusions

- Machines consolidated: **4**
- Most frequent top model: `lightgbm_hist`

## Per-machine ranking winner/loser
| machine_tag | system | architecture | top_model | slowest_model | native_profile_enabled |
| --- | --- | --- | --- | --- | --- |
| linux-amd64 | Linux | x86_64 | lightgbm_hist | xgboost_hist | True |
| linux-arm64 | Linux | aarch64 | lightgbm_hist | xgboost_hist | True |
| macos-arm64 | Darwin | arm64 | lightgbm_hist | xgboost_hist | True |
| windows-amd64 | Windows | AMD64 | lightgbm_hist | xgboost_hist | False |

## Cross-platform model runtime variation
| model | machines_seen | mean_median_total_s | best_median_total_s | worst_median_total_s | worst_to_best_ratio |
| --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 4 | 0.657714 | 0.319515 | 0.870259 | 2.724x |
| sklearn_hgb | 4 | 1.08641 | 0.582393 | 1.39908 | 2.402x |
| sklearn_hgb_fixed | 4 | 0.858205 | 0.457919 | 1.11476 | 2.434x |
| xgboost_hist | 4 | 1.19889 | 0.69058 | 1.53307 | 2.220x |

## Conclusion
- Current consolidated runs show a stable top-ranked model across platforms, but per-model runtime ratios still vary and should be tracked per machine.
