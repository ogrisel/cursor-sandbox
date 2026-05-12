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
| lightgbm_hist | 4 | 1.74509 | 1.6172 | 1.86864 | 1.155x |
| sklearn_hgb | 4 | 1.89253 | 1.77116 | 1.96387 | 1.109x |
| sklearn_hgb_fixed | 4 | 1.84176 | 1.69627 | 1.91473 | 1.129x |
| xgboost_hist | 4 | 1.9671 | 1.82611 | 2.08795 | 1.143x |

## Conclusion
- Current consolidated runs show a stable top-ranked model across platforms, but per-model runtime ratios still vary and should be tracked per machine.
