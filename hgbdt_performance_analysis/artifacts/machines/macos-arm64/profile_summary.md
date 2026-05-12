# Profiling snapshots

## sklearn_hgb
### Python-level (cProfile) top cumulative entries
| function | primitive_calls | total_calls | total_time_s | cumulative_time_s |
| --- | --- | --- | --- | --- |
| ~:0:<built-in method builtins.exec> | 1 | 1669 | 0.0192522 | 2.59457 |
| /Users/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:1:<module> | 1 | 1 | 4.1998e-05 | 2.59453 |
| <frozen importlib._bootstrap>:1165:_find_and_load | 11 | 1671 | 0.00503148 | 1.39563 |
| <frozen importlib._bootstrap>:1120:_find_and_load_unlocked | 11 | 1628 | 0.0038396 | 1.39551 |
| <frozen importlib._bootstrap>:666:_load_unlocked | 11 | 1575 | 0.00309609 | 1.39456 |
| <frozen importlib._bootstrap_external>:934:exec_module | 10 | 1329 | 0.00164215 | 1.39407 |
| <frozen importlib._bootstrap>:233:_call_with_frames_removed | 23 | 3831 | 0.00107473 | 1.39302 |
| ~:0:<built-in method builtins.__import__> | 67 | 779 | 0.000618684 | 1.26031 |
| /Users/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:444:main | 1 | 1 | 5.874e-06 | 1.19821 |
| /Users/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:402:_emit_single | 1 | 1 | 0.000445168 | 1.19656 |
| /Users/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:199:_single_run | 1 | 1 | 0.000188835 | 1.19607 |
| /Users/runner/work/_temp/setup-uv-cache/archive-v0/UO9ktdZ2yjI6-dqg/lib/python3.11/site-packages/lightgbm/__init__.py:1:<module> | 1 | 1 | 2.4293e-05 | 1.18254 |

