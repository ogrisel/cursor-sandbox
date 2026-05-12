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
| lightgbm_hist | 4 | 0.706778 | 0.319695 | 0.972857 | 3.043x |
| sklearn_hgb | 4 | 1.16679 | 0.580966 | 1.57563 | 2.712x |
| sklearn_hgb_fixed | 4 | 0.985038 | 0.453763 | 1.39535 | 3.075x |
| xgboost_hist | 4 | 1.19118 | 0.677548 | 1.57674 | 2.327x |

## Conclusion
- Current consolidated runs show a stable top-ranked model across platforms, but per-model runtime ratios still vary and should be tracked per machine.
