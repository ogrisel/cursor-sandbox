# Profiling snapshots

## sklearn_hgb
### Python-level (cProfile) top cumulative entries
| function | primitive_calls | total_calls | total_time_s | cumulative_time_s |
| --- | --- | --- | --- | --- |
| ~:0:<built-in method builtins.exec> | 1 | 1669 | 0.0264135 | 2.93586 |
| /Users/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:1:<module> | 1 | 1 | 4.6416e-05 | 2.93582 |
| <frozen importlib._bootstrap>:1165:_find_and_load | 11 | 1671 | 0.00591914 | 1.63499 |
| <frozen importlib._bootstrap>:1120:_find_and_load_unlocked | 11 | 1628 | 0.00439791 | 1.63486 |
| <frozen importlib._bootstrap>:666:_load_unlocked | 11 | 1575 | 0.00348699 | 1.63365 |
| <frozen importlib._bootstrap_external>:934:exec_module | 10 | 1329 | 0.00188584 | 1.63309 |
| <frozen importlib._bootstrap>:233:_call_with_frames_removed | 23 | 3831 | 0.00125866 | 1.63191 |
| ~:0:<built-in method builtins.__import__> | 67 | 779 | 0.000742662 | 1.47561 |
| /Users/runner/work/_temp/setup-uv-cache/archive-v0/d3x85T84mKWOYtJB/lib/python3.11/site-packages/lightgbm/__init__.py:1:<module> | 1 | 1 | 2.6503e-05 | 1.37663 |
| /Users/runner/work/_temp/setup-uv-cache/archive-v0/d3x85T84mKWOYtJB/lib/python3.11/site-packages/lightgbm/basic.py:1:<module> | 1 | 1 | 0.00136175 | 1.36721 |
| /Users/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:447:main | 1 | 1 | 6.083e-06 | 1.30005 |
| /Users/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:405:_emit_single | 1 | 1 | 0.000367583 | 1.29829 |

