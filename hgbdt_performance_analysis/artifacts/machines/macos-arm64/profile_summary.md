# Profiling snapshots

## sklearn_hgb
### Python-level (cProfile) top cumulative entries
| function | primitive_calls | total_calls | total_time_s | cumulative_time_s |
| --- | --- | --- | --- | --- |
| ~:0:<built-in method builtins.exec> | 1 | 1669 | 0.0233886 | 3.04035 |
| /Users/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:1:<module> | 1 | 1 | 5.2291e-05 | 3.04031 |
| <frozen importlib._bootstrap>:1165:_find_and_load | 11 | 1671 | 0.00607775 | 1.62091 |
| <frozen importlib._bootstrap>:1120:_find_and_load_unlocked | 11 | 1628 | 0.00457015 | 1.62077 |
| <frozen importlib._bootstrap>:666:_load_unlocked | 11 | 1575 | 0.00374281 | 1.61969 |
| <frozen importlib._bootstrap_external>:934:exec_module | 10 | 1329 | 0.00188192 | 1.61914 |
| <frozen importlib._bootstrap>:233:_call_with_frames_removed | 23 | 3831 | 0.00128988 | 1.61787 |
| /Users/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:444:main | 1 | 1 | 5.417e-06 | 1.41863 |
| /Users/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:402:_emit_single | 1 | 1 | 0.00046775 | 1.41692 |
| /Users/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:199:_single_run | 1 | 1 | 0.000215204 | 1.41641 |
| ~:0:<built-in method builtins.__import__> | 67 | 779 | 0.000831473 | 1.41453 |
| /Users/runner/work/_temp/setup-uv-cache/archive-v0/o3Oaoq7W4qr0Wc2I/lib/python3.11/site-packages/lightgbm/__init__.py:1:<module> | 1 | 1 | 4.8961e-05 | 1.37623 |

