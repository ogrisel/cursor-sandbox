# Platform-specific benchmark conclusions

- Machines consolidated: **4**
- Most frequent top model: `sklearn_hgb_fixed`

## Per-machine ranking winner/loser
| machine_tag | system | architecture | top_model | slowest_model | native_profile_enabled |
| --- | --- | --- | --- | --- | --- |
| linux-amd64 | Linux | x86_64 | sklearn_hgb_fixed | sklearn_hgb | True |
| linux-arm64 | Linux | aarch64 | sklearn_hgb_fixed | sklearn_hgb | True |
| macos-arm64 | Darwin | arm64 | sklearn_hgb_fixed | xgboost_hist | True |
| windows-amd64 | Windows | AMD64 | lightgbm_hist | xgboost_hist | False |

## Cross-platform model runtime variation
| model | machines_seen | mean_median_total_s | best_median_total_s | worst_median_total_s | worst_to_best_ratio |
| --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 4 | 3.26646 | 2.55131 | 4.87682 | 1.911x |
| sklearn_hgb | 4 | 4.3267 | 4.06037 | 4.64392 | 1.144x |
| sklearn_hgb_fixed | 4 | 3.07018 | 2.17079 | 4.05138 | 1.866x |
| xgboost_hist | 4 | 4.082 | 2.62888 | 5.31234 | 2.021x |

## Conclusion
- Fastest model varies by platform; keep platform-specific benchmark snapshots in `artifacts/machines/<machine-tag>/` before drawing global conclusions.
- Use `model_variation.worst_to_best_ratio` from `platform_specific_summary.json` to track how sensitive each model is to OS/architecture changes.
