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
| lightgbm_hist | 4 | 0.709619 | 0.290214 | 1.1158 | 3.845x |
| sklearn_hgb | 4 | 1.06239 | 0.597897 | 1.41754 | 2.371x |
| sklearn_hgb_fixed | 4 | 0.935663 | 0.460821 | 1.2494 | 2.711x |
| xgboost_hist | 4 | 1.19059 | 0.686316 | 1.52589 | 2.223x |

## Conclusion
- Current consolidated runs show a stable top-ranked model across platforms, but per-model runtime ratios still vary and should be tracked per machine.
