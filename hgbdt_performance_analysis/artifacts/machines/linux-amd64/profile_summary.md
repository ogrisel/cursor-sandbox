# Profiling snapshots

## sklearn_hgb
### Python-level (cProfile) top cumulative entries
| function | primitive_calls | total_calls | total_time_s | cumulative_time_s |
| --- | --- | --- | --- | --- |
| ~:0:<built-in method builtins.exec> | 1 | 1664 | 0.0406406 | 4.11976 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:1:<module> | 1 | 1 | 0.000122971 | 4.11973 |
| <frozen importlib._bootstrap>:1165:_find_and_load | 11 | 1666 | 0.0291557 | 2.43607 |
| <frozen importlib._bootstrap>:1120:_find_and_load_unlocked | 11 | 1623 | 0.00831542 | 2.43582 |
| <frozen importlib._bootstrap>:666:_load_unlocked | 11 | 1570 | 0.00673981 | 2.43416 |
| <frozen importlib._bootstrap_external>:934:exec_module | 10 | 1324 | 0.00422431 | 2.43371 |
| <frozen importlib._bootstrap>:233:_call_with_frames_removed | 22 | 3784 | 0.00256362 | 2.43129 |
| ~:0:<built-in method builtins.__import__> | 67 | 778 | 0.00159593 | 2.21967 |
| /home/runner/work/_temp/setup-uv-cache/archive-v0/9ejP7QONfwesAijg/lib/python3.11/site-packages/lightgbm/__init__.py:1:<module> | 1 | 1 | 7.0282e-05 | 2.06393 |
| /home/runner/work/_temp/setup-uv-cache/archive-v0/9ejP7QONfwesAijg/lib/python3.11/site-packages/lightgbm/basic.py:1:<module> | 1 | 1 | 0.000363159 | 2.04787 |
| /home/runner/work/_temp/setup-uv-cache/archive-v0/9ejP7QONfwesAijg/lib/python3.11/site-packages/lightgbm/compat.py:1:<module> | 1 | 1 | 8.4647e-05 | 1.86063 |
| /home/runner/work/_temp/setup-uv-cache/archive-v0/9ejP7QONfwesAijg/lib/python3.11/site-packages/sklearn/__init__.py:1:<module> | 1 | 1 | 2.8304e-05 | 1.68513 |

