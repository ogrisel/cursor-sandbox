# Profiling snapshots

## sklearn_hgb
### Python-level (cProfile) top cumulative entries
| function | primitive_calls | total_calls | total_time_s | cumulative_time_s |
| --- | --- | --- | --- | --- |
| ~:0:<built-in method builtins.exec> | 1 | 1664 | 0.0385127 | 4.24631 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:1:<module> | 1 | 1 | 9.4586e-05 | 4.24628 |
| <frozen importlib._bootstrap>:1165:_find_and_load | 11 | 1666 | 0.0109876 | 2.21631 |
| <frozen importlib._bootstrap>:1120:_find_and_load_unlocked | 11 | 1623 | 0.0077351 | 2.21607 |
| <frozen importlib._bootstrap>:666:_load_unlocked | 11 | 1570 | 0.00602771 | 2.21459 |
| <frozen importlib._bootstrap_external>:934:exec_module | 10 | 1324 | 0.00378693 | 2.21422 |
| <frozen importlib._bootstrap>:233:_call_with_frames_removed | 22 | 3784 | 0.00226531 | 2.2122 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:450:main | 1 | 1 | 9.417e-06 | 2.0287 |
| ~:0:<built-in method builtins.__import__> | 67 | 778 | 0.00143695 | 2.02799 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:408:_emit_single | 1 | 1 | 0.000146106 | 2.02563 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:199:_single_run | 1 | 1 | 0.000351506 | 2.02543 |
| /home/runner/work/_temp/setup-uv-cache/archive-v0/u531Hn8hww0WHVJL/lib/python3.11/site-packages/lightgbm/__init__.py:1:<module> | 1 | 1 | 4.6326e-05 | 1.90305 |

