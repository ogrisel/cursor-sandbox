# Platform-specific benchmark conclusions

- Machines consolidated: **4**
- Most frequent top model: `lightgbm_hist`

## Per-machine ranking winner/loser
| machine_tag | system | architecture | top_model | slowest_model | native_profile_enabled |
| --- | --- | --- | --- | --- | --- |
| linux-amd64 | Linux | x86_64 | lightgbm_hist | xgboost_hist | True |
| linux-arm64 | Linux | aarch64 | lightgbm_hist | sklearn_hgb | True |
| macos-arm64 | Darwin | arm64 | sklearn_hgb_fixed | sklearn_hgb | True |
| windows-amd64 | Windows | AMD64 | lightgbm_hist | xgboost_hist | False |

## Cross-platform model runtime variation
| model | machines_seen | mean_median_total_s | best_median_total_s | worst_median_total_s | worst_to_best_ratio |
| --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 4 | 3.70232 | 2.55487 | 4.76744 | 1.866x |
| sklearn_hgb | 4 | 5.02529 | 3.67579 | 7.02962 | 1.912x |
| sklearn_hgb_fixed | 4 | 3.81395 | 2.75804 | 4.52713 | 1.641x |
| xgboost_hist | 4 | 4.74492 | 3.44825 | 5.85475 | 1.698x |

## Conclusion
- Fastest model varies by platform; keep platform-specific benchmark snapshots in `artifacts/machines/<machine-tag>/` before drawing global conclusions.
- Use `model_variation.worst_to_best_ratio` from `platform_specific_summary.json` to track how sensitive each model is to OS/architecture changes.
