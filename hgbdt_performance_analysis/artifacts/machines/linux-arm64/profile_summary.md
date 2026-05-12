# Profiling snapshots

## sklearn_hgb
### Python-level (cProfile) top cumulative entries
| function | primitive_calls | total_calls | total_time_s | cumulative_time_s |
| --- | --- | --- | --- | --- |
| ~:0:<built-in method builtins.exec> | 1 | 1664 | 0.0328553 | 3.38484 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:1:<module> | 1 | 1 | 8.2747e-05 | 3.38481 |
| <frozen importlib._bootstrap>:1165:_find_and_load | 11 | 1666 | 0.00895188 | 1.78313 |
| <frozen importlib._bootstrap>:1120:_find_and_load_unlocked | 11 | 1623 | 0.00636001 | 1.78293 |
| <frozen importlib._bootstrap>:666:_load_unlocked | 11 | 1570 | 0.0050239 | 1.78159 |
| <frozen importlib._bootstrap_external>:934:exec_module | 10 | 1324 | 0.00332687 | 1.78124 |
| <frozen importlib._bootstrap>:233:_call_with_frames_removed | 22 | 3784 | 0.00183644 | 1.77923 |
| ~:0:<built-in method builtins.__import__> | 67 | 778 | 0.00117027 | 1.61347 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:444:main | 1 | 1 | 8.312e-06 | 1.60055 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:402:_emit_single | 1 | 1 | 0.000164724 | 1.59819 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:199:_single_run | 1 | 1 | 0.000228529 | 1.59796 |
| /home/runner/work/_temp/setup-uv-cache/archive-v0/UlO_M_8TnqiNRQ77/lib/python3.11/site-packages/lightgbm/__init__.py:1:<module> | 1 | 1 | 5.1773e-05 | 1.52465 |

