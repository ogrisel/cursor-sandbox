# Platform-specific benchmark conclusions

- Machines consolidated: **4**
- Most frequent top model: `sklearn_hgb_fixed`

## Per-machine ranking winner/loser
| machine_tag | system | architecture | top_model | slowest_model | native_profile_enabled |
| --- | --- | --- | --- | --- | --- |
| linux-amd64 | Linux | x86_64 | sklearn_hgb_fixed | xgboost_hist | True |
| linux-arm64 | Linux | aarch64 | lightgbm_hist | xgboost_hist | True |
| macos-arm64 | Darwin | arm64 | sklearn_hgb_fixed | xgboost_hist | True |
| windows-amd64 | Windows | AMD64 | lightgbm_hist | xgboost_hist | False |

## Cross-platform model runtime variation
| model | machines_seen | mean_median_total_s | best_median_total_s | worst_median_total_s | worst_to_best_ratio |
| --- | --- | --- | --- | --- | --- |
| lightgbm_hist | 4 | 2.08227 | 1.76539 | 2.56232 | 1.451x |
| sklearn_hgb | 4 | 2.48472 | 1.94402 | 3.22632 | 1.660x |
| sklearn_hgb_fixed | 4 | 2.42193 | 1.92313 | 3.15447 | 1.640x |
| xgboost_hist | 4 | 3.09257 | 2.60685 | 3.75925 | 1.442x |

## Conclusion
- Fastest model varies by platform; keep platform-specific benchmark snapshots in `artifacts/machines/<machine-tag>/` before drawing global conclusions.
- Use `model_variation.worst_to_best_ratio` from `platform_specific_summary.json` to track how sensitive each model is to OS/architecture changes.
