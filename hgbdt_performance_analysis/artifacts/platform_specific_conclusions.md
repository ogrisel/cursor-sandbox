# Platform-specific benchmark conclusions

- Machines consolidated: **4**
- Most frequent top model: `sklearn_hgb_fixed`

## Per-machine ranking winner/loser
| machine_tag | system | architecture | top_model | slowest_model | native_profile_enabled |
| --- | --- | --- | --- | --- | --- |
| linux-amd64 | Linux | x86_64 | sklearn_hgb_fixed | lightgbm_hist | True |
| linux-arm64 | Linux | aarch64 | sklearn_hgb_fixed | sklearn_hgb | True |
| macos-arm64 | Darwin | arm64 | sklearn_hgb_fixed | sklearn_hgb | True |
| windows-amd64 | Windows | AMD64 | lightgbm_hist | sklearn_hgb | False |

## Cross-platform model runtime variation
| model | machines_seen | mean_median_total_s | best_median_total_s | worst_median_total_s | worst_to_best_ratio |
| --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 4 | 1.93426 | 1.30443 | 3.11945 | 2.391x |
| sklearn_hgb | 4 | 2.82616 | 2.07859 | 4.19703 | 2.019x |
| sklearn_hgb_fixed | 4 | 1.31789 | 0.880118 | 1.5764 | 1.791x |
| xgboost_hist | 4 | 1.73725 | 1.02713 | 2.21382 | 2.155x |

## Conclusion
- Fastest model varies by platform; keep platform-specific benchmark snapshots in `artifacts/machines/<machine-tag>/` before drawing global conclusions.
- Use `model_variation.worst_to_best_ratio` from `platform_specific_summary.json` to track how sensitive each model is to OS/architecture changes.
