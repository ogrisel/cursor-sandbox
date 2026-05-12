# Profiling snapshots

## sklearn_hgb
### Python-level (cProfile) top cumulative entries
| function | primitive_calls | total_calls | total_time_s | cumulative_time_s |
| --- | --- | --- | --- | --- |
| ~:0:<built-in method builtins.exec> | 1 | 1664 | 0.0336662 | 3.35593 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:1:<module> | 1 | 1 | 0.000103623 | 3.3559 |
| <frozen importlib._bootstrap>:1165:_find_and_load | 11 | 1666 | 0.00969961 | 1.75741 |
| <frozen importlib._bootstrap>:1120:_find_and_load_unlocked | 11 | 1623 | 0.00643077 | 1.75721 |
| <frozen importlib._bootstrap>:666:_load_unlocked | 11 | 1570 | 0.00512407 | 1.75589 |
| <frozen importlib._bootstrap_external>:934:exec_module | 10 | 1324 | 0.00330834 | 1.75556 |
| <frozen importlib._bootstrap>:233:_call_with_frames_removed | 22 | 3784 | 0.00192204 | 1.75372 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:444:main | 1 | 1 | 8.176e-06 | 1.59741 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:402:_emit_single | 1 | 1 | 0.000174877 | 1.59502 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:199:_single_run | 1 | 1 | 0.00024207 | 1.59478 |
| ~:0:<built-in method builtins.__import__> | 67 | 778 | 0.00120076 | 1.59255 |
| /home/runner/work/_temp/setup-uv-cache/archive-v0/jCP1SPBFHKjR61sf/lib/python3.11/site-packages/sklearn/base.py:1319:wrapper | 1 | 1 | 7.6171e-05 | 1.51287 |

