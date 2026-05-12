# Platform-specific benchmark conclusions

- Machines consolidated: **4**
- Most frequent top model: `lightgbm_hist`

## Per-machine ranking winner/loser
| machine_tag | system | architecture | top_model | slowest_model | native_profile_enabled |
| --- | --- | --- | --- | --- | --- |
| linux-amd64 | Linux | x86_64 | lightgbm_hist | xgboost_hist | True |
| linux-arm64 | Linux | aarch64 | lightgbm_hist | xgboost_hist | True |
| macos-arm64 | Darwin | arm64 | lightgbm_hist | sklearn_hgb | True |
| windows-amd64 | Windows | AMD64 | lightgbm_hist | xgboost_hist | False |

## Cross-platform model runtime variation
| model | machines_seen | mean_median_total_s | best_median_total_s | worst_median_total_s | worst_to_best_ratio |
| --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 4 | 0.764715 | 0.632248 | 0.904508 | 1.431x |
| sklearn_hgb | 4 | 1.14995 | 0.74547 | 1.44777 | 1.942x |
| sklearn_hgb_fixed | 4 | 0.958743 | 0.665418 | 1.26388 | 1.899x |
| xgboost_hist | 4 | 1.28459 | 1.06394 | 1.52707 | 1.435x |

## Conclusion
- Current consolidated runs show a stable top-ranked model across platforms, but per-model runtime ratios still vary and should be tracked per machine.
