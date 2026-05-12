# Profiling snapshots

## sklearn_hgb
### Python-level (cProfile) top cumulative entries
| function | primitive_calls | total_calls | total_time_s | cumulative_time_s |
| --- | --- | --- | --- | --- |
| ~:0:<built-in method builtins.exec> | 1 | 1664 | 0.0392245 | 3.78319 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:1:<module> | 1 | 1 | 7.6557e-05 | 3.78316 |
| <frozen importlib._bootstrap>:1165:_find_and_load | 11 | 1666 | 0.0109242 | 2.13793 |
| <frozen importlib._bootstrap>:1120:_find_and_load_unlocked | 11 | 1623 | 0.00705301 | 2.13772 |
| <frozen importlib._bootstrap>:666:_load_unlocked | 11 | 1570 | 0.00569246 | 2.13621 |
| <frozen importlib._bootstrap_external>:934:exec_module | 10 | 1324 | 0.00350853 | 2.13584 |
| <frozen importlib._bootstrap>:233:_call_with_frames_removed | 22 | 3784 | 0.00203552 | 2.13385 |
| ~:0:<built-in method builtins.__import__> | 67 | 778 | 0.00139721 | 1.95367 |
| /home/runner/work/_temp/setup-uv-cache/archive-v0/-EULsVxLDjCgRQs0/lib/python3.11/site-packages/lightgbm/__init__.py:1:<module> | 1 | 1 | 4.731e-05 | 1.83136 |
| /home/runner/work/_temp/setup-uv-cache/archive-v0/-EULsVxLDjCgRQs0/lib/python3.11/site-packages/lightgbm/basic.py:1:<module> | 1 | 1 | 0.000284545 | 1.81753 |
| /home/runner/work/_temp/setup-uv-cache/archive-v0/-EULsVxLDjCgRQs0/lib/python3.11/site-packages/lightgbm/compat.py:1:<module> | 1 | 1 | 5.7818e-05 | 1.64907 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:444:main | 1 | 1 | 1.1157e-05 | 1.64399 |

