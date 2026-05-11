# Platform-specific benchmark conclusions

- Machines consolidated: **4**
- Most frequent top model: `lightgbm_hist`

## Per-machine ranking winner/loser
| machine_tag | system | architecture | top_model | slowest_model | native_profile_enabled |
| --- | --- | --- | --- | --- | --- |
| linux-amd64 | Linux | x86_64 | lightgbm_hist | xgboost_hist | True |
| linux-arm64 | Linux | aarch64 | sklearn_hgb_fixed | sklearn_hgb | True |
| macos-arm64 | Darwin | arm64 | lightgbm_hist | sklearn_hgb_fixed | True |
| windows-amd64 | Windows | AMD64 | lightgbm_hist | xgboost_hist | False |

## Cross-platform model runtime variation
| model | machines_seen | mean_median_total_s | best_median_total_s | worst_median_total_s | worst_to_best_ratio |
| --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 4 | 0.772793 | 0.429723 | 0.993305 | 2.311x |
| sklearn_hgb | 4 | 1.18383 | 0.735086 | 1.40902 | 1.917x |
| sklearn_hgb_fixed | 4 | 1.04534 | 0.490232 | 1.67468 | 3.416x |
| xgboost_hist | 4 | 1.17106 | 0.744253 | 1.52545 | 2.050x |

## Conclusion
- Fastest model varies by platform; keep platform-specific benchmark snapshots in `artifacts/machines/<machine-tag>/` before drawing global conclusions.
- Use `model_variation.worst_to_best_ratio` from `platform_specific_summary.json` to track how sensitive each model is to OS/architecture changes.
