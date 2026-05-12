# Profiling snapshots

## sklearn_hgb
### Python-level (cProfile) top cumulative entries
| function | primitive_calls | total_calls | total_time_s | cumulative_time_s |
| --- | --- | --- | --- | --- |
| ~:0:<built-in method builtins.exec> | 1 | 1664 | 0.033725 | 3.4127 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:1:<module> | 1 | 1 | 0.000107659 | 3.41266 |
| <frozen importlib._bootstrap>:1165:_find_and_load | 11 | 1666 | 0.0098678 | 1.78383 |
| <frozen importlib._bootstrap>:1120:_find_and_load_unlocked | 11 | 1623 | 0.00657124 | 1.78363 |
| <frozen importlib._bootstrap>:666:_load_unlocked | 11 | 1570 | 0.00517187 | 1.78227 |
| <frozen importlib._bootstrap_external>:934:exec_module | 10 | 1324 | 0.00334262 | 1.7819 |
| <frozen importlib._bootstrap>:233:_call_with_frames_removed | 22 | 3784 | 0.00191563 | 1.78006 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:444:main | 1 | 1 | 8.73e-06 | 1.62771 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:402:_emit_single | 1 | 1 | 0.000166895 | 1.62526 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:199:_single_run | 1 | 1 | 0.000238592 | 1.62503 |
| ~:0:<built-in method builtins.__import__> | 67 | 778 | 0.00129299 | 1.61507 |
| /home/runner/work/_temp/setup-uv-cache/archive-v0/XqYSj26hlwGZzFAO/lib/python3.11/site-packages/sklearn/base.py:1319:wrapper | 1 | 1 | 7.594e-05 | 1.54209 |

