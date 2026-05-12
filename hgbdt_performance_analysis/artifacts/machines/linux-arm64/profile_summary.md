# Profiling snapshots

## sklearn_hgb
### Python-level (cProfile) top cumulative entries
| function | primitive_calls | total_calls | total_time_s | cumulative_time_s |
| --- | --- | --- | --- | --- |
| ~:0:<built-in method builtins.exec> | 1 | 1664 | 0.0340685 | 3.40142 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:1:<module> | 1 | 1 | 7.9908e-05 | 3.4014 |
| <frozen importlib._bootstrap>:1165:_find_and_load | 11 | 1666 | 0.00944504 | 1.7724 |
| <frozen importlib._bootstrap>:1120:_find_and_load_unlocked | 11 | 1623 | 0.00688952 | 1.77219 |
| <frozen importlib._bootstrap>:666:_load_unlocked | 11 | 1570 | 0.00520902 | 1.77085 |
| <frozen importlib._bootstrap_external>:934:exec_module | 10 | 1324 | 0.00346735 | 1.77051 |
| <frozen importlib._bootstrap>:233:_call_with_frames_removed | 22 | 3784 | 0.00192019 | 1.76864 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:444:main | 1 | 1 | 8.888e-06 | 1.62794 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:402:_emit_single | 1 | 1 | 0.000146956 | 1.62553 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:199:_single_run | 1 | 1 | 0.000216488 | 1.62531 |
| ~:0:<built-in method builtins.__import__> | 67 | 778 | 0.00118426 | 1.60175 |
| /home/runner/work/_temp/setup-uv-cache/archive-v0/4QlqFk0IAmL4gVvv/lib/python3.11/site-packages/sklearn/base.py:1319:wrapper | 1 | 1 | 7.3394e-05 | 1.55137 |

### Native/C/C++/Cython-flavored stack leaf hotspots (py-spy --native)
| leaf_frame | sample_weight |
| --- | --- |
| _compute_best_split_and_push | 0.73 |
| split_next | 0.58 |
| _compile_bytecode | 0.11 |
| _call_with_frames_removed | 0.1 |
| _initialize_root | 0.09 |
| <module> | 0.08 |
| get_data | 0.07 |
| dedent | 0.06 |
| __init__ | 0.05 |
| _is_at_section | 0.05 |
| _fill_predictor_arrays | 0.04 |
| _path_stat | 0.03 |

