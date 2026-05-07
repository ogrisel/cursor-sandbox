# Profiling snapshots

## sklearn_hgb
### Python-level (cProfile) top cumulative entries
| function | primitive_calls | total_calls | total_time_s | cumulative_time_s |
| --- | --- | --- | --- | --- |
| ~:0:<built-in method builtins.exec> | 1 | 1671 | 0.0249798 | 4.1725 |
| /Users/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:1:<module> | 1 | 1 | 5.1751e-05 | 4.17247 |
| /Users/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:447:main | 1 | 1 | 8.125e-06 | 2.37744 |
| /Users/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:405:_emit_single | 1 | 1 | 0.000664124 | 2.37555 |
| /Users/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:195:_single_run | 1 | 1 | 0.000604707 | 2.37484 |
| /Users/runner/work/_temp/setup-uv-cache/archive-v0/IAWbRp1XpcBQ_Twc/lib/python3.11/site-packages/sklearn/base.py:1319:wrapper | 1 | 1 | 0.00058004 | 2.19197 |
| /Users/runner/work/_temp/setup-uv-cache/archive-v0/IAWbRp1XpcBQ_Twc/lib/python3.11/site-packages/sklearn/ensemble/_hist_gradient_boosting/gradient_boosting.py:512:fit | 1 | 1 | 0.0648116 | 2.19088 |
| <frozen importlib._bootstrap>:1165:_find_and_load | 12 | 1673 | 0.00638945 | 1.79591 |
| <frozen importlib._bootstrap>:1120:_find_and_load_unlocked | 12 | 1630 | 0.00511577 | 1.79568 |
| <frozen importlib._bootstrap>:666:_load_unlocked | 12 | 1577 | 0.00416316 | 1.79423 |
| <frozen importlib._bootstrap_external>:934:exec_module | 11 | 1331 | 0.00291238 | 1.79365 |
| <frozen importlib._bootstrap>:233:_call_with_frames_removed | 25 | 3835 | 0.00166622 | 1.7917 |

## lightgbm_hist
### Python-level (cProfile) top cumulative entries
| function | primitive_calls | total_calls | total_time_s | cumulative_time_s |
| --- | --- | --- | --- | --- |
| ~:0:<built-in method builtins.exec> | 1 | 1669 | 0.0232462 | 3.97581 |
| /Users/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:1:<module> | 1 | 1 | 4.9791e-05 | 3.97573 |
| /Users/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:447:main | 1 | 1 | 7.709e-06 | 2.42487 |
| /Users/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:405:_emit_single | 1 | 1 | 0.00100017 | 2.42308 |
| /Users/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:195:_single_run | 1 | 1 | 0.000586459 | 2.42188 |
| /Users/runner/work/_temp/setup-uv-cache/archive-v0/IAWbRp1XpcBQ_Twc/lib/python3.11/site-packages/lightgbm/sklearn.py:1381:fit | 1 | 1 | 1.7208e-05 | 2.13742 |
| /Users/runner/work/_temp/setup-uv-cache/archive-v0/IAWbRp1XpcBQ_Twc/lib/python3.11/site-packages/lightgbm/sklearn.py:907:fit | 1 | 1 | 0.000156873 | 2.1374 |
| /Users/runner/work/_temp/setup-uv-cache/archive-v0/IAWbRp1XpcBQ_Twc/lib/python3.11/site-packages/lightgbm/engine.py:109:train | 1 | 1 | 0.00272725 | 2.13587 |
| /Users/runner/work/_temp/setup-uv-cache/archive-v0/IAWbRp1XpcBQ_Twc/lib/python3.11/site-packages/lightgbm/basic.py:4092:update | 220 | 220 | 1.9468 | 1.9477 |
| <frozen importlib._bootstrap>:1165:_find_and_load | 11 | 1671 | 0.00532697 | 1.55001 |
| <frozen importlib._bootstrap>:1120:_find_and_load_unlocked | 11 | 1628 | 0.00446101 | 1.54987 |
| <frozen importlib._bootstrap>:666:_load_unlocked | 11 | 1575 | 0.00357669 | 1.54871 |

