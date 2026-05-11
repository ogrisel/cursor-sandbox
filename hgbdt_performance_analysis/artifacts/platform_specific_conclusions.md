# Platform-specific benchmark conclusions

- Machines consolidated: **4**
- Most frequent top model: `sklearn_hgb_fixed`

## Per-machine ranking winner/loser
| machine_tag | system | architecture | top_model | slowest_model | native_profile_enabled |
| --- | --- | --- | --- | --- | --- |
| linux-amd64 | Linux | x86_64 | sklearn_hgb_fixed | xgboost_hist | True |
| linux-arm64 | Linux | aarch64 | sklearn_hgb_fixed | sklearn_hgb | True |
| macos-arm64 | Darwin | arm64 | sklearn_hgb_fixed | sklearn_hgb | True |
| windows-amd64 | Windows | AMD64 | lightgbm_hist | xgboost_hist | False |

## Cross-platform model runtime variation
| model | machines_seen | mean_median_total_s | best_median_total_s | worst_median_total_s | worst_to_best_ratio |
| --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 4 | 2.61664 | 1.64637 | 3.55344 | 2.158x |
| sklearn_hgb | 4 | 3.39081 | 1.48579 | 4.42875 | 2.981x |
| sklearn_hgb_fixed | 4 | 2.24257 | 0.960876 | 3.45566 | 3.596x |
| xgboost_hist | 4 | 3.12863 | 1.73268 | 4.55244 | 2.627x |

## Conclusion
- Fastest model varies by platform; keep platform-specific benchmark snapshots in `artifacts/machines/<machine-tag>/` before drawing global conclusions.
- Use `model_variation.worst_to_best_ratio` from `platform_specific_summary.json` to track how sensitive each model is to OS/architecture changes.
