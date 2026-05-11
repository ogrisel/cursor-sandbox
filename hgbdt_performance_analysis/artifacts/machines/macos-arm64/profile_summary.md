# Profiling snapshots

## sklearn_hgb
### Python-level (cProfile) top cumulative entries
| function | primitive_calls | total_calls | total_time_s | cumulative_time_s |
| --- | --- | --- | --- | --- |
| ~:0:<built-in method builtins.exec> | 1 | 1671 | 0.0267251 | 4.40088 |
| /Users/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:1:<module> | 1 | 1 | 8.8293e-05 | 4.40079 |
| /Users/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:447:main | 1 | 1 | 1.1709e-05 | 2.35504 |
| /Users/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:405:_emit_single | 1 | 1 | 0.00149358 | 2.35319 |
| /Users/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:195:_single_run | 1 | 1 | 0.000708751 | 2.35149 |
| /Users/runner/work/_temp/setup-uv-cache/archive-v0/lpEk1bogHRqOkVwO/lib/python3.11/site-packages/sklearn/base.py:1319:wrapper | 1 | 1 | 0.000838542 | 2.16051 |
| /Users/runner/work/_temp/setup-uv-cache/archive-v0/lpEk1bogHRqOkVwO/lib/python3.11/site-packages/sklearn/ensemble/_hist_gradient_boosting/gradient_boosting.py:512:fit | 1 | 1 | 0.0582979 | 2.15909 |
| <frozen importlib._bootstrap>:1165:_find_and_load | 12 | 1673 | 0.0083137 | 2.04741 |
| <frozen importlib._bootstrap>:1120:_find_and_load_unlocked | 12 | 1630 | 0.00593917 | 2.04701 |
| <frozen importlib._bootstrap>:666:_load_unlocked | 12 | 1577 | 0.00462817 | 2.04497 |
| <frozen importlib._bootstrap_external>:934:exec_module | 11 | 1331 | 0.00263285 | 2.0436 |
| <frozen importlib._bootstrap>:233:_call_with_frames_removed | 25 | 3835 | 0.00165103 | 2.04136 |

## lightgbm_hist
### Python-level (cProfile) top cumulative entries
| function | primitive_calls | total_calls | total_time_s | cumulative_time_s |
| --- | --- | --- | --- | --- |
| ~:0:<built-in method builtins.exec> | 1 | 1669 | 0.027495 | 4.7688 |
| /Users/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:1:<module> | 1 | 1 | 5.6291e-05 | 4.76876 |
| /Users/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:447:main | 1 | 1 | 6.708e-06 | 2.67852 |
| /Users/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:405:_emit_single | 1 | 1 | 0.000822168 | 2.67665 |
| /Users/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:195:_single_run | 1 | 1 | 0.000624918 | 2.67565 |
| /Users/runner/work/_temp/setup-uv-cache/archive-v0/lpEk1bogHRqOkVwO/lib/python3.11/site-packages/lightgbm/sklearn.py:1381:fit | 1 | 1 | 1.2583e-05 | 2.33061 |
| /Users/runner/work/_temp/setup-uv-cache/archive-v0/lpEk1bogHRqOkVwO/lib/python3.11/site-packages/lightgbm/sklearn.py:907:fit | 1 | 1 | 8.4499e-05 | 2.3306 |
| /Users/runner/work/_temp/setup-uv-cache/archive-v0/lpEk1bogHRqOkVwO/lib/python3.11/site-packages/lightgbm/engine.py:109:train | 1 | 1 | 0.00344869 | 2.32874 |
| /Users/runner/work/_temp/setup-uv-cache/archive-v0/lpEk1bogHRqOkVwO/lib/python3.11/site-packages/lightgbm/basic.py:4092:update | 220 | 220 | 2.11798 | 2.11884 |
| <frozen importlib._bootstrap>:1165:_find_and_load | 11 | 1671 | 0.00796457 | 2.08925 |
| <frozen importlib._bootstrap>:1120:_find_and_load_unlocked | 11 | 1628 | 0.00544522 | 2.0891 |
| <frozen importlib._bootstrap>:666:_load_unlocked | 11 | 1575 | 0.00463097 | 2.08786 |

