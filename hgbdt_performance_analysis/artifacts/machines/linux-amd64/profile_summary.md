# Profiling snapshots

## sklearn_hgb
### Python-level (cProfile) top cumulative entries
| function | primitive_calls | total_calls | total_time_s | cumulative_time_s |
| --- | --- | --- | --- | --- |
| ~:0:<built-in method builtins.exec> | 1 | 1664 | 0.0409107 | 4.15295 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:1:<module> | 1 | 1 | 8.7321e-05 | 4.15292 |
| <frozen importlib._bootstrap>:1165:_find_and_load | 11 | 1666 | 0.0125765 | 2.47153 |
| <frozen importlib._bootstrap>:1120:_find_and_load_unlocked | 11 | 1623 | 0.00869788 | 2.47129 |
| <frozen importlib._bootstrap>:666:_load_unlocked | 11 | 1570 | 0.00680103 | 2.46964 |
| <frozen importlib._bootstrap_external>:934:exec_module | 10 | 1324 | 0.00431998 | 2.46918 |
| <frozen importlib._bootstrap>:233:_call_with_frames_removed | 22 | 3784 | 0.00262204 | 2.46707 |
| ~:0:<built-in method builtins.__import__> | 67 | 778 | 0.00158294 | 2.25711 |
| /home/runner/work/_temp/setup-uv-cache/archive-v0/hTS44etkslFrvLmu/lib/python3.11/site-packages/lightgbm/__init__.py:1:<module> | 1 | 1 | 6.6746e-05 | 2.11803 |
| /home/runner/work/_temp/setup-uv-cache/archive-v0/hTS44etkslFrvLmu/lib/python3.11/site-packages/lightgbm/basic.py:1:<module> | 1 | 1 | 0.000336159 | 2.10277 |
| /home/runner/work/_temp/setup-uv-cache/archive-v0/hTS44etkslFrvLmu/lib/python3.11/site-packages/lightgbm/compat.py:1:<module> | 1 | 1 | 8.8504e-05 | 1.90554 |
| /home/runner/work/_temp/setup-uv-cache/archive-v0/hTS44etkslFrvLmu/lib/python3.11/site-packages/sklearn/__init__.py:1:<module> | 1 | 1 | 2.7391e-05 | 1.73109 |

