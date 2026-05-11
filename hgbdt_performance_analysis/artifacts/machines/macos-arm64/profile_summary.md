# Profiling snapshots

## sklearn_hgb
### Python-level (cProfile) top cumulative entries
| function | primitive_calls | total_calls | total_time_s | cumulative_time_s |
| --- | --- | --- | --- | --- |
| ~:0:<built-in method builtins.exec> | 1 | 1669 | 0.0244867 | 3.45944 |
| /Users/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:1:<module> | 1 | 1 | 7.8162e-05 | 3.45939 |
| <frozen importlib._bootstrap>:1165:_find_and_load | 11 | 1671 | 0.00765396 | 2.13525 |
| <frozen importlib._bootstrap>:1120:_find_and_load_unlocked | 11 | 1628 | 0.00555791 | 2.13504 |
| <frozen importlib._bootstrap>:666:_load_unlocked | 11 | 1575 | 0.00437055 | 2.13323 |
| <frozen importlib._bootstrap_external>:934:exec_module | 10 | 1329 | 0.00255145 | 2.13254 |
| <frozen importlib._bootstrap>:233:_call_with_frames_removed | 23 | 3831 | 0.0015085 | 2.12746 |
| ~:0:<built-in method builtins.__import__> | 67 | 779 | 0.000990303 | 1.8741 |
| /Users/runner/work/_temp/setup-uv-cache/archive-v0/PCBKLBIwyvEGhb7I/lib/python3.11/site-packages/lightgbm/__init__.py:1:<module> | 1 | 1 | 4.821e-05 | 1.79025 |
| /Users/runner/work/_temp/setup-uv-cache/archive-v0/PCBKLBIwyvEGhb7I/lib/python3.11/site-packages/lightgbm/basic.py:1:<module> | 1 | 1 | 0.00162424 | 1.77486 |
| /Users/runner/work/_temp/setup-uv-cache/archive-v0/PCBKLBIwyvEGhb7I/lib/python3.11/site-packages/lightgbm/compat.py:1:<module> | 1 | 1 | 5.5706e-05 | 1.60403 |
| /Users/runner/work/_temp/setup-uv-cache/archive-v0/PCBKLBIwyvEGhb7I/lib/python3.11/site-packages/sklearn/__init__.py:1:<module> | 1 | 1 | 2.1832e-05 | 1.40102 |

