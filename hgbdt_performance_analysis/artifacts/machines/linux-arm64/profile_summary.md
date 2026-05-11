# Profiling snapshots

## sklearn_hgb
### Python-level (cProfile) top cumulative entries
| function | primitive_calls | total_calls | total_time_s | cumulative_time_s |
| --- | --- | --- | --- | --- |
| ~:0:<built-in method builtins.exec> | 1 | 1664 | 0.035227 | 3.45339 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:1:<module> | 1 | 1 | 8.3229e-05 | 3.45336 |
| <frozen importlib._bootstrap>:1165:_find_and_load | 11 | 1666 | 0.00938816 | 1.79573 |
| <frozen importlib._bootstrap>:1120:_find_and_load_unlocked | 11 | 1623 | 0.00668717 | 1.7955 |
| <frozen importlib._bootstrap>:666:_load_unlocked | 11 | 1570 | 0.00527183 | 1.79409 |
| <frozen importlib._bootstrap_external>:934:exec_module | 10 | 1324 | 0.00373386 | 1.79366 |
| <frozen importlib._bootstrap>:233:_call_with_frames_removed | 22 | 3784 | 0.00201083 | 1.79181 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:447:main | 1 | 1 | 9.472e-06 | 1.65653 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:405:_emit_single | 1 | 1 | 0.000178429 | 1.65408 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:199:_single_run | 1 | 1 | 0.000221064 | 1.65384 |
| ~:0:<built-in method builtins.__import__> | 67 | 778 | 0.00121469 | 1.62627 |
| /home/runner/work/_temp/setup-uv-cache/archive-v0/o-bcoRCcI4uSlwty/lib/python3.11/site-packages/sklearn/base.py:1319:wrapper | 1 | 1 | 7.7204e-05 | 1.57375 |

