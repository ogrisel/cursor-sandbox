# Profiling snapshots

## sklearn_hgb
### Python-level (cProfile) top cumulative entries
| function | primitive_calls | total_calls | total_time_s | cumulative_time_s |
| --- | --- | --- | --- | --- |
| ~:0:<built-in method builtins.exec> | 1 | 1386 | 0.019523 | 3.65139 |
| /Users/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:1:<module> | 1 | 1 | 6.1207e-05 | 3.65131 |
| /Users/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:418:main | 1 | 1 | 1.0958e-05 | 2.28451 |
| /Users/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:374:_emit_single | 1 | 1 | 0.00129862 | 2.28241 |
| /Users/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:168:_single_run | 1 | 1 | 0.000628832 | 2.28102 |
| /Users/runner/work/_temp/setup-uv-cache/archive-v0/bTWVFWCyB77-l4Gz/lib/python3.11/site-packages/sklearn/base.py:1319:wrapper | 1 | 1 | 0.000740583 | 2.094 |
| /Users/runner/work/_temp/setup-uv-cache/archive-v0/bTWVFWCyB77-l4Gz/lib/python3.11/site-packages/sklearn/ensemble/_hist_gradient_boosting/gradient_boosting.py:512:fit | 1 | 1 | 0.0557797 | 2.09276 |
| /Users/runner/work/_temp/setup-uv-cache/archive-v0/bTWVFWCyB77-l4Gz/lib/python3.11/site-packages/sklearn/ensemble/_hist_gradient_boosting/grower.py:385:grow | 220 | 220 | 0.00263681 | 1.48244 |
| /Users/runner/work/_temp/setup-uv-cache/archive-v0/bTWVFWCyB77-l4Gz/lib/python3.11/site-packages/sklearn/ensemble/_hist_gradient_boosting/grower.py:488:split_next | 6600 | 6600 | 0.799099 | 1.47849 |
| <frozen importlib._bootstrap>:1165:_find_and_load | 13 | 1352 | 0.00409796 | 1.36752 |
| <frozen importlib._bootstrap>:1120:_find_and_load_unlocked | 13 | 1310 | 0.00339469 | 1.36728 |
| <frozen importlib._bootstrap>:666:_load_unlocked | 13 | 1266 | 0.00273624 | 1.36595 |

## lightgbm_hist
### Python-level (cProfile) top cumulative entries
| function | primitive_calls | total_calls | total_time_s | cumulative_time_s |
| --- | --- | --- | --- | --- |
| ~:0:<built-in method builtins.exec> | 1 | 1384 | 0.0212621 | 3.60352 |
| /Users/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:1:<module> | 1 | 1 | 5.0666e-05 | 3.60349 |
| /Users/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:418:main | 1 | 1 | 6.749e-06 | 2.22725 |
| /Users/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:374:_emit_single | 1 | 1 | 0.00080571 | 2.22531 |
| /Users/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:168:_single_run | 1 | 1 | 0.000570913 | 2.22435 |
| /Users/runner/work/_temp/setup-uv-cache/archive-v0/bTWVFWCyB77-l4Gz/lib/python3.11/site-packages/lightgbm/sklearn.py:1381:fit | 1 | 1 | 1.3543e-05 | 2.02831 |
| /Users/runner/work/_temp/setup-uv-cache/archive-v0/bTWVFWCyB77-l4Gz/lib/python3.11/site-packages/lightgbm/sklearn.py:907:fit | 1 | 1 | 0.000186252 | 2.0283 |
| /Users/runner/work/_temp/setup-uv-cache/archive-v0/bTWVFWCyB77-l4Gz/lib/python3.11/site-packages/lightgbm/engine.py:109:train | 1 | 1 | 0.0023609 | 2.02694 |
| /Users/runner/work/_temp/setup-uv-cache/archive-v0/bTWVFWCyB77-l4Gz/lib/python3.11/site-packages/lightgbm/basic.py:4092:update | 220 | 220 | 1.83967 | 1.84021 |
| <frozen importlib._bootstrap>:1165:_find_and_load | 12 | 1350 | 0.00428142 | 1.37532 |
| <frozen importlib._bootstrap>:1120:_find_and_load_unlocked | 12 | 1308 | 0.00355809 | 1.37517 |
| <frozen importlib._bootstrap>:666:_load_unlocked | 12 | 1264 | 0.00285243 | 1.37406 |

