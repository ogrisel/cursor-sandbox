# Platform-specific benchmark conclusions

- Machines consolidated: **4**
- Most frequent top model: `lightgbm_hist`

## Per-machine ranking winner/loser
| machine_tag | system | architecture | top_model | slowest_model | native_profile_enabled |
| --- | --- | --- | --- | --- | --- |
| linux-amd64 | Linux | x86_64 | lightgbm_hist | xgboost_hist | True |
| linux-arm64 | Linux | aarch64 | lightgbm_hist | sklearn_hgb | True |
| macos-arm64 | Darwin | arm64 | lightgbm_hist | sklearn_hgb | True |
| windows-amd64 | Windows | AMD64 | lightgbm_hist | xgboost_hist | False |

## Cross-platform model runtime variation
| model | machines_seen | mean_median_total_s | best_median_total_s | worst_median_total_s | worst_to_best_ratio |
| --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 4 | 0.741669 | 0.28993 | 1.09495 | 3.777x |
| sklearn_hgb | 4 | 1.24396 | 0.578606 | 2.04006 | 3.526x |
| sklearn_hgb_fixed | 4 | 0.9561 | 0.457611 | 1.32755 | 2.901x |
| xgboost_hist | 4 | 1.21707 | 0.672669 | 1.58443 | 2.355x |

## Conclusion
- Current consolidated runs show a stable top-ranked model across platforms, but per-model runtime ratios still vary and should be tracked per machine.
