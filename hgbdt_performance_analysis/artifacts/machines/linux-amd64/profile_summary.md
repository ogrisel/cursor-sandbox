# Profiling snapshots

## sklearn_hgb
### Python-level (cProfile) top cumulative entries
| function | primitive_calls | total_calls | total_time_s | cumulative_time_s |
| --- | --- | --- | --- | --- |
| ~:0:<built-in method builtins.exec> | 1 | 1664 | 0.039769 | 4.16207 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:1:<module> | 1 | 1 | 7.7936e-05 | 4.16204 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:450:main | 1 | 1 | 1.0861e-05 | 2.09657 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:408:_emit_single | 1 | 1 | 0.000193339 | 2.09387 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:199:_single_run | 1 | 1 | 0.000375765 | 2.09362 |
| <frozen importlib._bootstrap>:1165:_find_and_load | 11 | 1666 | 0.0106855 | 2.06428 |
| <frozen importlib._bootstrap>:1120:_find_and_load_unlocked | 11 | 1623 | 0.00703218 | 2.06406 |
| <frozen importlib._bootstrap>:666:_load_unlocked | 11 | 1570 | 0.00558437 | 2.0627 |
| <frozen importlib._bootstrap_external>:934:exec_module | 10 | 1324 | 0.00331771 | 2.06232 |
| <frozen importlib._bootstrap>:233:_call_with_frames_removed | 22 | 3784 | 0.00209208 | 2.06035 |
| ~:0:<built-in method builtins.__import__> | 67 | 778 | 0.00148845 | 1.88123 |
| /home/runner/work/_temp/setup-uv-cache/archive-v0/1S4rddcAenOC_BQa/lib/python3.11/site-packages/lightgbm/__init__.py:1:<module> | 1 | 1 | 5.7617e-05 | 1.74714 |

### Native/C/C++/Cython-flavored stack leaf hotspots (py-spy --native)
| leaf_frame | sample_weight |
| --- | --- |
| _compute_best_split_and_push | 0.77 |
| predict | 0.63 |
| split_next | 0.48 |
| _initialize_root | 0.14 |
| _call_with_frames_removed | 0.11 |
| dedent | 0.09 |
| transform | 0.08 |
| cleandoc | 0.07 |
| _fill_predictor_arrays | 0.07 |
| _compile_bytecode | 0.06 |
| get_data | 0.06 |
| <module> | 0.06 |

