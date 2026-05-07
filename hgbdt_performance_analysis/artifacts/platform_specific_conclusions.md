# Platform-specific benchmark conclusions

- Machines consolidated: **4**
- Most frequent top model: `lightgbm_hist`

## Per-machine ranking winner/loser
| machine_tag | system | architecture | top_model | slowest_model | native_profile_enabled |
| --- | --- | --- | --- | --- | --- |
| linux-amd64 | Linux | x86_64 | lightgbm_hist | xgboost_hist | True |
| linux-arm64 | Linux | aarch64 | lightgbm_hist | xgboost_hist | True |
| macos-arm64 | Darwin | arm64 | sklearn_hgb_fixed | xgboost_hist | True |
| windows-amd64 | Windows | AMD64 | lightgbm_hist | xgboost_hist | False |

## Cross-platform model runtime variation
| model | machines_seen | mean_median_total_s | best_median_total_s | worst_median_total_s | worst_to_best_ratio |
| --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 4 | 2.13842 | 1.75883 | 2.86357 | 1.628x |
| sklearn_hgb | 4 | 2.47776 | 2.09681 | 2.82736 | 1.348x |
| sklearn_hgb_fixed | 4 | 2.43294 | 2.10272 | 2.84682 | 1.354x |
| xgboost_hist | 4 | 3.16332 | 2.61357 | 3.72146 | 1.424x |

## Conclusion
- Fastest model varies by platform; keep platform-specific benchmark snapshots in `artifacts/machines/<machine-tag>/` before drawing global conclusions.
- Use `model_variation.worst_to_best_ratio` from `platform_specific_summary.json` to track how sensitive each model is to OS/architecture changes.
