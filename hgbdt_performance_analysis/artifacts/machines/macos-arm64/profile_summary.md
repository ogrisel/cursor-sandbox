# Profiling snapshots

## sklearn_hgb
### Python-level (cProfile) top cumulative entries
| function | primitive_calls | total_calls | total_time_s | cumulative_time_s |
| --- | --- | --- | --- | --- |
| ~:0:<built-in method builtins.exec> | 1 | 1671 | 0.020766 | 3.19703 |
| /Users/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:1:<module> | 1 | 1 | 4.5668e-05 | 3.197 |
| /Users/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:447:main | 1 | 1 | 5.708e-06 | 1.74508 |
| /Users/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:405:_emit_single | 1 | 1 | 0.000597875 | 1.74345 |
| /Users/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:195:_single_run | 1 | 1 | 0.00052175 | 1.7428 |
| /Users/runner/work/_temp/setup-uv-cache/archive-v0/mwYn6DhJ69njP1Ko/lib/python3.11/site-packages/sklearn/base.py:1319:wrapper | 1 | 1 | 0.000553167 | 1.60252 |
| /Users/runner/work/_temp/setup-uv-cache/archive-v0/mwYn6DhJ69njP1Ko/lib/python3.11/site-packages/sklearn/ensemble/_hist_gradient_boosting/gradient_boosting.py:512:fit | 1 | 1 | 0.0311247 | 1.60159 |
| <frozen importlib._bootstrap>:1165:_find_and_load | 12 | 1673 | 0.00466519 | 1.45211 |
| <frozen importlib._bootstrap>:1120:_find_and_load_unlocked | 12 | 1630 | 0.00399049 | 1.45187 |
| <frozen importlib._bootstrap>:666:_load_unlocked | 12 | 1577 | 0.00322845 | 1.45067 |
| <frozen importlib._bootstrap_external>:934:exec_module | 11 | 1331 | 0.00171581 | 1.45011 |
| <frozen importlib._bootstrap>:233:_call_with_frames_removed | 25 | 3835 | 0.00113161 | 1.44866 |

## lightgbm_hist
### Python-level (cProfile) top cumulative entries
| function | primitive_calls | total_calls | total_time_s | cumulative_time_s |
| --- | --- | --- | --- | --- |
| ~:0:<built-in method builtins.exec> | 1 | 1669 | 0.0185545 | 3.39871 |
| /Users/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:1:<module> | 1 | 1 | 3.8461e-05 | 3.39868 |
| /Users/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:447:main | 1 | 1 | 5.667e-06 | 2.07759 |
| /Users/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:405:_emit_single | 1 | 1 | 0.000717874 | 2.07594 |
| /Users/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:195:_single_run | 1 | 1 | 0.000501874 | 2.07509 |
| /Users/runner/work/_temp/setup-uv-cache/archive-v0/mwYn6DhJ69njP1Ko/lib/python3.11/site-packages/lightgbm/sklearn.py:1381:fit | 1 | 1 | 8.833e-06 | 1.79491 |
| /Users/runner/work/_temp/setup-uv-cache/archive-v0/mwYn6DhJ69njP1Ko/lib/python3.11/site-packages/lightgbm/sklearn.py:907:fit | 1 | 1 | 4.4876e-05 | 1.7949 |
| /Users/runner/work/_temp/setup-uv-cache/archive-v0/mwYn6DhJ69njP1Ko/lib/python3.11/site-packages/lightgbm/engine.py:109:train | 1 | 1 | 0.00111862 | 1.79376 |
| /Users/runner/work/_temp/setup-uv-cache/archive-v0/mwYn6DhJ69njP1Ko/lib/python3.11/site-packages/lightgbm/basic.py:4092:update | 220 | 220 | 1.625 | 1.62527 |
| <frozen importlib._bootstrap>:1165:_find_and_load | 11 | 1671 | 0.00463401 | 1.3204 |
| <frozen importlib._bootstrap>:1120:_find_and_load_unlocked | 11 | 1628 | 0.00374294 | 1.32028 |
| <frozen importlib._bootstrap>:666:_load_unlocked | 11 | 1575 | 0.00295438 | 1.31938 |

