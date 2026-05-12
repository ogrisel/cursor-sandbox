# Profiling snapshots

## sklearn_hgb
### Python-level (cProfile) top cumulative entries
| function | primitive_calls | total_calls | total_time_s | cumulative_time_s |
| --- | --- | --- | --- | --- |
| ~:0:<built-in method builtins.exec> | 1 | 1664 | 0.0330625 | 3.36975 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:1:<module> | 1 | 1 | 8.7602e-05 | 3.36973 |
| <frozen importlib._bootstrap>:1165:_find_and_load | 11 | 1666 | 0.00873688 | 1.74485 |
| <frozen importlib._bootstrap>:1120:_find_and_load_unlocked | 11 | 1623 | 0.00646153 | 1.74465 |
| <frozen importlib._bootstrap>:666:_load_unlocked | 11 | 1570 | 0.00496832 | 1.74333 |
| <frozen importlib._bootstrap_external>:934:exec_module | 10 | 1324 | 0.00343894 | 1.74298 |
| <frozen importlib._bootstrap>:233:_call_with_frames_removed | 22 | 3784 | 0.00186318 | 1.74121 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:444:main | 1 | 1 | 8.128e-06 | 1.62382 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:402:_emit_single | 1 | 1 | 0.00017254 | 1.62141 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:199:_single_run | 1 | 1 | 0.000229622 | 1.62117 |
| ~:0:<built-in method builtins.__import__> | 67 | 778 | 0.00112951 | 1.58234 |
| /home/runner/work/_temp/setup-uv-cache/archive-v0/wAeAChjs_3vWaQl5/lib/python3.11/site-packages/sklearn/base.py:1319:wrapper | 1 | 1 | 7.5649e-05 | 1.54019 |

### Native/C/C++/Cython-flavored stack leaf hotspots (py-spy --native)
| leaf_frame | sample_weight |
| --- | --- |
| _compute_best_split_and_push | 0.64 |
| split_next | 0.45 |
| _compile_bytecode | 0.1 |
| _initialize_root | 0.09 |
| _call_with_frames_removed | 0.08 |
| dedent | 0.06 |
| _fill_predictor_arrays | 0.06 |
| <module> | 0.05 |
| _is_at_section | 0.04 |
| __init__ | 0.04 |
| get_data | 0.03 |
| _deepcopy_dict | 0.03 |

