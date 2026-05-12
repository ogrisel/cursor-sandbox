# Profiling snapshots

## sklearn_hgb
### Python-level (cProfile) top cumulative entries
| function | primitive_calls | total_calls | total_time_s | cumulative_time_s |
| --- | --- | --- | --- | --- |
| ~:0:<built-in method builtins.exec> | 1 | 1664 | 0.0342531 | 3.96152 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:1:<module> | 1 | 1 | 8.0089e-05 | 3.96149 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:450:main | 1 | 1 | 7.52e-06 | 2.16382 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:408:_emit_single | 1 | 1 | 0.000151038 | 2.16145 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:199:_single_run | 1 | 1 | 0.000332364 | 2.16124 |
| <frozen importlib._bootstrap>:1165:_find_and_load | 11 | 1666 | 0.0102376 | 1.79659 |
| <frozen importlib._bootstrap>:1120:_find_and_load_unlocked | 11 | 1623 | 0.00685613 | 1.79638 |
| <frozen importlib._bootstrap>:666:_load_unlocked | 11 | 1570 | 0.00549507 | 1.79507 |
| <frozen importlib._bootstrap_external>:934:exec_module | 10 | 1324 | 0.00355377 | 1.79473 |
| <frozen importlib._bootstrap>:233:_call_with_frames_removed | 22 | 3784 | 0.00208519 | 1.79283 |
| ~:0:<built-in method builtins.__import__> | 67 | 778 | 0.00136517 | 1.62566 |
| /home/runner/work/_temp/setup-uv-cache/archive-v0/VYTQM6T-BL7mOjKA/lib/python3.11/site-packages/sklearn/base.py:1319:wrapper | 1 | 1 | 7.5139e-05 | 1.58902 |

