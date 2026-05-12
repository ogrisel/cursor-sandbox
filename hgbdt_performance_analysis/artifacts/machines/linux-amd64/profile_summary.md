# Profiling snapshots

## sklearn_hgb
### Python-level (cProfile) top cumulative entries
| function | primitive_calls | total_calls | total_time_s | cumulative_time_s |
| --- | --- | --- | --- | --- |
| ~:0:<built-in method builtins.exec> | 1 | 1664 | 0.0394859 | 3.85593 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:1:<module> | 1 | 1 | 9.952e-05 | 3.8559 |
| <frozen importlib._bootstrap>:1165:_find_and_load | 11 | 1666 | 0.0114462 | 2.19179 |
| <frozen importlib._bootstrap>:1120:_find_and_load_unlocked | 11 | 1623 | 0.00700782 | 2.19155 |
| <frozen importlib._bootstrap>:666:_load_unlocked | 11 | 1570 | 0.00583621 | 2.19005 |
| <frozen importlib._bootstrap_external>:934:exec_module | 10 | 1324 | 0.0035912 | 2.18968 |
| <frozen importlib._bootstrap>:233:_call_with_frames_removed | 22 | 3784 | 0.00198672 | 2.18757 |
| ~:0:<built-in method builtins.__import__> | 67 | 778 | 0.00159986 | 2.0031 |
| /home/runner/work/_temp/setup-uv-cache/archive-v0/oOoapjdDSA3N7RiM/lib/python3.11/site-packages/lightgbm/__init__.py:1:<module> | 1 | 1 | 5.4573e-05 | 1.87979 |
| /home/runner/work/_temp/setup-uv-cache/archive-v0/oOoapjdDSA3N7RiM/lib/python3.11/site-packages/lightgbm/basic.py:1:<module> | 1 | 1 | 0.000285912 | 1.86561 |
| /home/runner/work/_temp/setup-uv-cache/archive-v0/oOoapjdDSA3N7RiM/lib/python3.11/site-packages/lightgbm/compat.py:1:<module> | 1 | 1 | 6.6344e-05 | 1.68864 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:444:main | 1 | 1 | 1.1017e-05 | 1.66285 |

