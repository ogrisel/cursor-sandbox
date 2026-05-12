# Profiling snapshots

## sklearn_hgb
### Python-level (cProfile) top cumulative entries
| function | primitive_calls | total_calls | total_time_s | cumulative_time_s |
| --- | --- | --- | --- | --- |
| ~:0:<built-in method builtins.exec> | 1 | 1669 | 0.0211036 | 2.80442 |
| /Users/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:1:<module> | 1 | 1 | 5.0419e-05 | 2.80439 |
| <frozen importlib._bootstrap>:1165:_find_and_load | 11 | 1671 | 0.00506723 | 1.5358 |
| <frozen importlib._bootstrap>:1120:_find_and_load_unlocked | 11 | 1628 | 0.00420283 | 1.53566 |
| <frozen importlib._bootstrap>:666:_load_unlocked | 11 | 1575 | 0.00335371 | 1.53456 |
| <frozen importlib._bootstrap_external>:934:exec_module | 10 | 1329 | 0.00176774 | 1.53402 |
| <frozen importlib._bootstrap>:233:_call_with_frames_removed | 23 | 3831 | 0.00116592 | 1.53275 |
| ~:0:<built-in method builtins.__import__> | 67 | 779 | 0.000707895 | 1.35822 |
| /Users/runner/work/_temp/setup-uv-cache/archive-v0/R3R749F2Nm8rMPrJ/lib/python3.11/site-packages/lightgbm/__init__.py:1:<module> | 1 | 1 | 3.0375e-05 | 1.30368 |
| /Users/runner/work/_temp/setup-uv-cache/archive-v0/R3R749F2Nm8rMPrJ/lib/python3.11/site-packages/lightgbm/basic.py:1:<module> | 1 | 1 | 0.00149217 | 1.29465 |
| /Users/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:444:main | 1 | 1 | 5.833e-06 | 1.26783 |
| /Users/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:402:_emit_single | 1 | 1 | 0.000449043 | 1.26613 |

