# Profiling snapshots

## sklearn_hgb
### Python-level (cProfile) top cumulative entries
| function | primitive_calls | total_calls | total_time_s | cumulative_time_s |
| --- | --- | --- | --- | --- |
| ~:0:<built-in method builtins.exec> | 1 | 1669 | 0.0340442 | 3.99893 |
| /Users/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:1:<module> | 1 | 1 | 7.9836e-05 | 3.99887 |
| <frozen importlib._bootstrap>:1165:_find_and_load | 11 | 1671 | 0.0107556 | 2.20576 |
| <frozen importlib._bootstrap>:1120:_find_and_load_unlocked | 11 | 1628 | 0.00714282 | 2.20557 |
| <frozen importlib._bootstrap>:666:_load_unlocked | 11 | 1575 | 0.00547475 | 2.20381 |
| <frozen importlib._bootstrap_external>:934:exec_module | 10 | 1329 | 0.00342851 | 2.20317 |
| <frozen importlib._bootstrap>:233:_call_with_frames_removed | 23 | 3831 | 0.00205933 | 2.2012 |
| ~:0:<built-in method builtins.__import__> | 67 | 779 | 0.00157578 | 1.94185 |
| /Users/runner/work/_temp/setup-uv-cache/archive-v0/WesuAB0RgYQAkmrO/lib/python3.11/site-packages/lightgbm/__init__.py:1:<module> | 1 | 1 | 6.0877e-05 | 1.87802 |
| /Users/runner/work/_temp/setup-uv-cache/archive-v0/WesuAB0RgYQAkmrO/lib/python3.11/site-packages/lightgbm/basic.py:1:<module> | 1 | 1 | 0.00192067 | 1.86667 |
| /Users/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:444:main | 1 | 1 | 6.293e-06 | 1.79214 |
| /Users/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:402:_emit_single | 1 | 1 | 0.000605373 | 1.79012 |

