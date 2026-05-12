# Profiling snapshots

## sklearn_hgb
### Python-level (cProfile) top cumulative entries
| function | primitive_calls | total_calls | total_time_s | cumulative_time_s |
| --- | --- | --- | --- | --- |
| ~:0:<built-in method builtins.exec> | 1 | 1664 | 0.0301655 | 3.01899 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:1:<module> | 1 | 1 | 6.3326e-05 | 3.01895 |
| <frozen importlib._bootstrap>:1165:_find_and_load | 11 | 1666 | 0.00815937 | 1.70389 |
| <frozen importlib._bootstrap>:1120:_find_and_load_unlocked | 11 | 1623 | 0.00545748 | 1.70372 |
| <frozen importlib._bootstrap>:666:_load_unlocked | 11 | 1570 | 0.00436247 | 1.70251 |
| <frozen importlib._bootstrap_external>:934:exec_module | 10 | 1324 | 0.00276538 | 1.70222 |
| <frozen importlib._bootstrap>:233:_call_with_frames_removed | 22 | 3784 | 0.00160121 | 1.70059 |
| ~:0:<built-in method builtins.__import__> | 67 | 778 | 0.000992074 | 1.55742 |
| /home/runner/work/_temp/setup-uv-cache/archive-v0/fHEXX8b1ZrdFMf6H/lib/python3.11/site-packages/lightgbm/__init__.py:1:<module> | 1 | 1 | 3.8445e-05 | 1.46017 |
| /home/runner/work/_temp/setup-uv-cache/archive-v0/fHEXX8b1ZrdFMf6H/lib/python3.11/site-packages/lightgbm/basic.py:1:<module> | 1 | 1 | 0.000229879 | 1.44937 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:444:main | 1 | 1 | 7.421e-06 | 1.3141 |
| /home/runner/work/_temp/setup-uv-cache/archive-v0/fHEXX8b1ZrdFMf6H/lib/python3.11/site-packages/lightgbm/compat.py:1:<module> | 1 | 1 | 4.7099e-05 | 1.31382 |

### Native/C/C++/Cython-flavored stack leaf hotspots (py-spy --native)
| leaf_frame | sample_weight |
| --- | --- |
| _compute_best_split_and_push | 0.63 |
| split_next | 0.32 |
| __init__ | 0.12 |
| _call_with_frames_removed | 0.11 |
| <module> | 0.08 |
| lru_cache | 0.08 |
| _compile_bytecode | 0.07 |
| _fill_predictor_arrays | 0.07 |
| transform | 0.06 |
| dedent | 0.05 |
| _initialize_root | 0.05 |
| get_data | 0.04 |

