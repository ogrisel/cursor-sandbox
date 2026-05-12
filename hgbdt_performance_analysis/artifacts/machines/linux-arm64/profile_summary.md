# Profiling snapshots

## sklearn_hgb
### Python-level (cProfile) top cumulative entries
| function | primitive_calls | total_calls | total_time_s | cumulative_time_s |
| --- | --- | --- | --- | --- |
| ~:0:<built-in method builtins.exec> | 1 | 1664 | 0.0346606 | 3.97086 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:1:<module> | 1 | 1 | 8.815e-05 | 3.97083 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:450:main | 1 | 1 | 7.647e-06 | 2.12774 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:408:_emit_single | 1 | 1 | 0.000210556 | 2.12532 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:199:_single_run | 1 | 1 | 0.000386669 | 2.12504 |
| <frozen importlib._bootstrap>:1165:_find_and_load | 11 | 1666 | 0.00940553 | 1.84198 |
| <frozen importlib._bootstrap>:1120:_find_and_load_unlocked | 11 | 1623 | 0.00684822 | 1.84175 |
| <frozen importlib._bootstrap>:666:_load_unlocked | 11 | 1570 | 0.00531163 | 1.8404 |
| <frozen importlib._bootstrap_external>:934:exec_module | 10 | 1324 | 0.00358949 | 1.84007 |
| <frozen importlib._bootstrap>:233:_call_with_frames_removed | 22 | 3784 | 0.0019526 | 1.83821 |
| ~:0:<built-in method builtins.__import__> | 67 | 778 | 0.00122326 | 1.66855 |
| /home/runner/work/_temp/setup-uv-cache/archive-v0/eKWd0qp0A6Gjx0TI/lib/python3.11/site-packages/lightgbm/__init__.py:1:<module> | 1 | 1 | 5.5309e-05 | 1.57789 |

### Native/C/C++/Cython-flavored stack leaf hotspots (py-spy --native)
| leaf_frame | sample_weight |
| --- | --- |
| split_next | 0.6 |
| _compute_best_split_and_push | 0.57 |
| predict | 0.46 |
| _compile_bytecode | 0.2 |
| _initialize_root | 0.18 |
| _call_with_frames_removed | 0.17 |
| __init__ | 0.09 |
| <module> | 0.08 |
| __new__ | 0.07 |
| dedent | 0.06 |
| full | 0.04 |
| _monitor_peak_rss | 0.04 |

