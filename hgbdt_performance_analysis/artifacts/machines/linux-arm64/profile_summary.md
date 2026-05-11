# Profiling snapshots

## sklearn_hgb
### Python-level (cProfile) top cumulative entries
| function | primitive_calls | total_calls | total_time_s | cumulative_time_s |
| --- | --- | --- | --- | --- |
| ~:0:<built-in method builtins.exec> | 1 | 1664 | 0.033127 | 3.40273 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:1:<module> | 1 | 1 | 8.9101e-05 | 3.40268 |
| <frozen importlib._bootstrap>:1165:_find_and_load | 11 | 1666 | 0.00927884 | 1.79226 |
| <frozen importlib._bootstrap>:1120:_find_and_load_unlocked | 11 | 1623 | 0.00658647 | 1.79205 |
| <frozen importlib._bootstrap>:666:_load_unlocked | 11 | 1570 | 0.00499421 | 1.79064 |
| <frozen importlib._bootstrap_external>:934:exec_module | 10 | 1324 | 0.00328196 | 1.79032 |
| <frozen importlib._bootstrap>:233:_call_with_frames_removed | 22 | 3784 | 0.00193102 | 1.78853 |
| ~:0:<built-in method builtins.__import__> | 67 | 778 | 0.00126259 | 1.62165 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:496:main | 1 | 1 | 9.854e-06 | 1.60933 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:452:_emit_single | 1 | 1 | 0.000163021 | 1.60679 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:209:_single_run | 1 | 1 | 0.00024121 | 1.60656 |
| /home/runner/work/_temp/setup-uv-cache/archive-v0/PGt0dK6RpSio3qTJ/lib/python3.11/site-packages/lightgbm/__init__.py:1:<module> | 1 | 1 | 5.3102e-05 | 1.53387 |

### Native/C/C++/Cython-flavored stack leaf hotspots (py-spy --native)
| leaf_frame | sample_weight |
| --- | --- |
| _compute_best_split_and_push | 0.56 |
| split_next | 0.39 |
| _initialize_root | 0.1 |
| _compile_bytecode | 0.09 |
| _call_with_frames_removed | 0.09 |
| dedent | 0.07 |
| __init__ | 0.05 |
| cleandoc | 0.04 |
| _is_at_section | 0.04 |
| _find_spec | 0.03 |
| _unique1d | 0.03 |
| _fill_predictor_arrays | 0.03 |

