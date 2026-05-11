# Profiling snapshots

## sklearn_hgb
### Python-level (cProfile) top cumulative entries
| function | primitive_calls | total_calls | total_time_s | cumulative_time_s |
| --- | --- | --- | --- | --- |
| ~:0:<built-in method builtins.exec> | 1 | 1664 | 0.0409149 | 4.14098 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:1:<module> | 1 | 1 | 0.000105768 | 4.14093 |
| <frozen importlib._bootstrap>:1165:_find_and_load | 11 | 1666 | 0.0116341 | 2.39155 |
| <frozen importlib._bootstrap>:1120:_find_and_load_unlocked | 11 | 1623 | 0.007611 | 2.39132 |
| <frozen importlib._bootstrap>:666:_load_unlocked | 11 | 1570 | 0.0062859 | 2.38962 |
| <frozen importlib._bootstrap_external>:934:exec_module | 10 | 1324 | 0.00382647 | 2.38924 |
| <frozen importlib._bootstrap>:233:_call_with_frames_removed | 22 | 3784 | 0.00229984 | 2.38699 |
| ~:0:<built-in method builtins.__import__> | 67 | 778 | 0.00147157 | 2.18698 |
| /home/runner/work/_temp/setup-uv-cache/archive-v0/PMIWYruplpXCCjuL/lib/python3.11/site-packages/lightgbm/__init__.py:1:<module> | 1 | 1 | 6.5318e-05 | 2.02618 |
| /home/runner/work/_temp/setup-uv-cache/archive-v0/PMIWYruplpXCCjuL/lib/python3.11/site-packages/lightgbm/basic.py:1:<module> | 1 | 1 | 0.000360047 | 2.01044 |
| /home/runner/work/_temp/setup-uv-cache/archive-v0/PMIWYruplpXCCjuL/lib/python3.11/site-packages/lightgbm/compat.py:1:<module> | 1 | 1 | 7.6644e-05 | 1.83249 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:496:main | 1 | 1 | 1.36e-05 | 1.74801 |

