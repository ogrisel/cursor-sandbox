# Profiling snapshots

## sklearn_hgb
### Python-level (cProfile) top cumulative entries
| function | primitive_calls | total_calls | total_time_s | cumulative_time_s |
| --- | --- | --- | --- | --- |
| ~:0:<built-in method builtins.exec> | 1 | 1666 | 0.0331992 | 4.11324 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:1:<module> | 1 | 1 | 8.6867e-05 | 4.11322 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:447:main | 1 | 1 | 9.792e-06 | 2.31017 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:405:_emit_single | 1 | 1 | 0.000197592 | 2.30774 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:195:_single_run | 1 | 1 | 0.000249126 | 2.30747 |
| /home/runner/work/_temp/setup-uv-cache/archive-v0/-aQYbaf05GHOuNol/lib/python3.11/site-packages/sklearn/base.py:1319:wrapper | 1 | 1 | 8.4531e-05 | 2.15439 |
| /home/runner/work/_temp/setup-uv-cache/archive-v0/-aQYbaf05GHOuNol/lib/python3.11/site-packages/sklearn/ensemble/_hist_gradient_boosting/gradient_boosting.py:512:fit | 1 | 1 | 0.0412547 | 2.15363 |
| <frozen importlib._bootstrap>:1165:_find_and_load | 12 | 1668 | 0.0092632 | 1.80263 |
| <frozen importlib._bootstrap>:1120:_find_and_load_unlocked | 12 | 1625 | 0.00654206 | 1.80239 |
| <frozen importlib._bootstrap>:666:_load_unlocked | 12 | 1572 | 0.00511249 | 1.80085 |
| <frozen importlib._bootstrap_external>:934:exec_module | 11 | 1326 | 0.00329952 | 1.80047 |
| <frozen importlib._bootstrap>:233:_call_with_frames_removed | 24 | 3788 | 0.00191262 | 1.79845 |

### Native/C/C++/Cython-flavored stack leaf hotspots (py-spy --native)
| leaf_frame | sample_weight |
| --- | --- |
| split_next | 0.67 |
| _compute_best_split_and_push | 0.59 |
| _initialize_root | 0.32 |
| _call_with_frames_removed | 0.15 |
| _compile_bytecode | 0.12 |
| dedent | 0.06 |
| transform | 0.06 |
| get_data | 0.05 |
| __init__ | 0.05 |
| sort | 0.05 |
| <module> | 0.04 |
| _fill_predictor_arrays | 0.04 |

## lightgbm_hist
### Python-level (cProfile) top cumulative entries
| function | primitive_calls | total_calls | total_time_s | cumulative_time_s |
| --- | --- | --- | --- | --- |
| ~:0:<built-in method builtins.exec> | 1 | 1664 | 0.0348288 | 3.72126 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:1:<module> | 1 | 1 | 7.741e-05 | 3.72122 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:447:main | 1 | 1 | 9.377e-06 | 1.90564 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:405:_emit_single | 1 | 1 | 7.562e-05 | 1.90318 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:195:_single_run | 1 | 1 | 0.000238366 | 1.9028 |
| <frozen importlib._bootstrap>:1165:_find_and_load | 11 | 1666 | 0.0102191 | 1.81447 |
| <frozen importlib._bootstrap>:1120:_find_and_load_unlocked | 11 | 1623 | 0.00673717 | 1.81423 |
| <frozen importlib._bootstrap>:666:_load_unlocked | 11 | 1570 | 0.00535018 | 1.81286 |
| <frozen importlib._bootstrap_external>:934:exec_module | 10 | 1324 | 0.00347789 | 1.81253 |
| <frozen importlib._bootstrap>:233:_call_with_frames_removed | 22 | 3784 | 0.00202935 | 1.81062 |
| /home/runner/work/_temp/setup-uv-cache/archive-v0/-aQYbaf05GHOuNol/lib/python3.11/site-packages/lightgbm/sklearn.py:1381:fit | 1 | 1 | 1.84e-05 | 1.68417 |
| /home/runner/work/_temp/setup-uv-cache/archive-v0/-aQYbaf05GHOuNol/lib/python3.11/site-packages/lightgbm/sklearn.py:907:fit | 1 | 1 | 7.61e-05 | 1.68415 |

### Native/C/C++/Cython-flavored stack leaf hotspots (py-spy --native)
| leaf_frame | sample_weight |
| --- | --- |
| update | 1.5 |
| _compile_bytecode | 0.15 |
| __init_from_np2d | 0.15 |
| <module> | 0.12 |
| make_regression | 0.11 |
| dedent | 0.1 |
| _call_with_frames_removed | 0.09 |
| _path_stat | 0.08 |
| cleandoc | 0.07 |
| raw_decode | 0.07 |
| get_data | 0.05 |
| __init__ | 0.05 |

