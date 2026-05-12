# Profiling snapshots

## sklearn_hgb
### Python-level (cProfile) top cumulative entries
| function | primitive_calls | total_calls | total_time_s | cumulative_time_s |
| --- | --- | --- | --- | --- |
| ~:0:<built-in method builtins.exec> | 1 | 1669 | 0.0280892 | 4.05189 |
| /Users/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:1:<module> | 1 | 1 | 9.6998e-05 | 4.05177 |
| <frozen importlib._bootstrap>:1165:_find_and_load | 11 | 1671 | 0.0108093 | 2.14229 |
| <frozen importlib._bootstrap>:1120:_find_and_load_unlocked | 11 | 1628 | 0.00569176 | 2.14212 |
| <frozen importlib._bootstrap>:666:_load_unlocked | 11 | 1575 | 0.00535261 | 2.1405 |
| <frozen importlib._bootstrap_external>:934:exec_module | 10 | 1329 | 0.00282457 | 2.13974 |
| <frozen importlib._bootstrap>:233:_call_with_frames_removed | 23 | 3831 | 0.00158389 | 2.13697 |
| /Users/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:450:main | 1 | 1 | 7.708e-06 | 1.90843 |
| ~:0:<built-in method builtins.__import__> | 67 | 779 | 0.00108648 | 1.90649 |
| /Users/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:408:_emit_single | 1 | 1 | 0.000518416 | 1.90551 |
| /Users/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:199:_single_run | 1 | 1 | 0.000563874 | 1.90489 |
| /Users/runner/work/_temp/setup-uv-cache/archive-v0/96d_5tiwLoriFw0y/lib/python3.11/site-packages/lightgbm/__init__.py:1:<module> | 1 | 1 | 4.4497e-05 | 1.78852 |

