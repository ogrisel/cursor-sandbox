# Profiling snapshots

## sklearn_hgb
### Python-level (cProfile) top cumulative entries
| function | primitive_calls | total_calls | total_time_s | cumulative_time_s |
| --- | --- | --- | --- | --- |
| ~:0:<built-in method builtins.exec> | 1 | 1669 | 0.0232015 | 2.99901 |
| /Users/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:1:<module> | 1 | 1 | 5.537e-05 | 2.99897 |
| <frozen importlib._bootstrap>:1165:_find_and_load | 11 | 1671 | 0.00559865 | 1.64174 |
| <frozen importlib._bootstrap>:1120:_find_and_load_unlocked | 11 | 1628 | 0.00478105 | 1.64161 |
| <frozen importlib._bootstrap>:666:_load_unlocked | 11 | 1575 | 0.00361834 | 1.64054 |
| <frozen importlib._bootstrap_external>:934:exec_module | 10 | 1329 | 0.00193886 | 1.64 |
| <frozen importlib._bootstrap>:233:_call_with_frames_removed | 23 | 3831 | 0.00125329 | 1.63885 |
| ~:0:<built-in method builtins.__import__> | 67 | 779 | 0.000783895 | 1.45064 |
| /Users/runner/work/_temp/setup-uv-cache/archive-v0/8TEkotzwvXy--wiy/lib/python3.11/site-packages/lightgbm/__init__.py:1:<module> | 1 | 1 | 3.5249e-05 | 1.38133 |
| /Users/runner/work/_temp/setup-uv-cache/archive-v0/8TEkotzwvXy--wiy/lib/python3.11/site-packages/lightgbm/basic.py:1:<module> | 1 | 1 | 0.00158688 | 1.37156 |
| /Users/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:444:main | 1 | 1 | 7.125e-06 | 1.35625 |
| /Users/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:402:_emit_single | 1 | 1 | 0.000601375 | 1.3544 |

