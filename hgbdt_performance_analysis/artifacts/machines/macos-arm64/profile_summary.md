# Profiling snapshots

## sklearn_hgb
### Python-level (cProfile) top cumulative entries
| function | primitive_calls | total_calls | total_time_s | cumulative_time_s |
| --- | --- | --- | --- | --- |
| ~:0:<built-in method builtins.exec> | 1 | 1669 | 0.0239526 | 3.72685 |
| /Users/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:1:<module> | 1 | 1 | 6.2751e-05 | 3.72681 |
| <frozen importlib._bootstrap>:1165:_find_and_load | 11 | 1671 | 0.00658955 | 1.87503 |
| <frozen importlib._bootstrap>:1120:_find_and_load_unlocked | 11 | 1628 | 0.00487235 | 1.87488 |
| <frozen importlib._bootstrap>:666:_load_unlocked | 11 | 1575 | 0.00412354 | 1.87374 |
| <frozen importlib._bootstrap_external>:934:exec_module | 10 | 1329 | 0.00216138 | 1.87319 |
| <frozen importlib._bootstrap>:233:_call_with_frames_removed | 23 | 3831 | 0.00135004 | 1.87157 |
| /Users/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:450:main | 1 | 1 | 6.791e-06 | 1.8509 |
| /Users/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:408:_emit_single | 1 | 1 | 0.000450792 | 1.84906 |
| /Users/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:199:_single_run | 1 | 1 | 0.000430542 | 1.84856 |
| ~:0:<built-in method builtins.__import__> | 67 | 779 | 0.00085718 | 1.68731 |
| /Users/runner/work/_temp/setup-uv-cache/archive-v0/JdNFAmp9mGHtmPyA/lib/python3.11/site-packages/lightgbm/__init__.py:1:<module> | 1 | 1 | 3.1958e-05 | 1.61145 |

