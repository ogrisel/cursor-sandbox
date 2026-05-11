# Profiling snapshots

## sklearn_hgb
### Python-level (cProfile) top cumulative entries
| function | primitive_calls | total_calls | total_time_s | cumulative_time_s |
| --- | --- | --- | --- | --- |
| ~:0:<built-in method builtins.exec> | 1 | 1666 | 0.037141 | 4.30395 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:1:<module> | 1 | 1 | 9.4636e-05 | 4.30392 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:447:main | 1 | 1 | 9.552e-06 | 2.38296 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:405:_emit_single | 1 | 1 | 0.000201627 | 2.38045 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:195:_single_run | 1 | 1 | 0.000414236 | 2.38018 |
| /home/runner/work/_temp/setup-uv-cache/archive-v0/d0K4tb5aZoLwkeaA/lib/python3.11/site-packages/sklearn/base.py:1319:wrapper | 1 | 1 | 9.22e-05 | 2.2206 |
| /home/runner/work/_temp/setup-uv-cache/archive-v0/d0K4tb5aZoLwkeaA/lib/python3.11/site-packages/sklearn/ensemble/_hist_gradient_boosting/gradient_boosting.py:512:fit | 1 | 1 | 0.0466991 | 2.21971 |
| <frozen importlib._bootstrap>:1165:_find_and_load | 12 | 1668 | 0.0109075 | 1.92049 |
| <frozen importlib._bootstrap>:1120:_find_and_load_unlocked | 12 | 1625 | 0.0070637 | 1.92025 |
| <frozen importlib._bootstrap>:666:_load_unlocked | 12 | 1572 | 0.00552966 | 1.91863 |
| <frozen importlib._bootstrap_external>:934:exec_module | 11 | 1326 | 0.00380772 | 1.91823 |
| <frozen importlib._bootstrap>:233:_call_with_frames_removed | 24 | 3788 | 0.00216678 | 1.91601 |

### Native/C/C++/Cython-flavored stack leaf hotspots (py-spy --native)
| leaf_frame | sample_weight |
| --- | --- |
| split_next | 0.92 |
| _compute_best_split_and_push | 0.7 |
| _initialize_root | 0.28 |
| _compile_bytecode | 0.19 |
| _call_with_frames_removed | 0.11 |
| <module> | 0.1 |
| __init__ | 0.1 |
| get_data | 0.09 |
| dedent | 0.09 |
| fit | 0.09 |
| _fill_predictor_arrays | 0.07 |
| _monitor_peak_rss | 0.07 |

## lightgbm_hist
### Python-level (cProfile) top cumulative entries
| function | primitive_calls | total_calls | total_time_s | cumulative_time_s |
| --- | --- | --- | --- | --- |
| ~:0:<built-in method builtins.exec> | 1 | 1664 | 0.0357514 | 3.8632 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:1:<module> | 1 | 1 | 8.9753e-05 | 3.86317 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:447:main | 1 | 1 | 8.672e-06 | 1.97174 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:405:_emit_single | 1 | 1 | 7.1477e-05 | 1.96925 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:195:_single_run | 1 | 1 | 0.000345032 | 1.96882 |
| <frozen importlib._bootstrap>:1165:_find_and_load | 11 | 1666 | 0.00964612 | 1.89025 |
| <frozen importlib._bootstrap>:1120:_find_and_load_unlocked | 11 | 1623 | 0.00701713 | 1.89004 |
| <frozen importlib._bootstrap>:666:_load_unlocked | 11 | 1570 | 0.00533252 | 1.88862 |
| <frozen importlib._bootstrap_external>:934:exec_module | 10 | 1324 | 0.00367253 | 1.88824 |
| <frozen importlib._bootstrap>:233:_call_with_frames_removed | 22 | 3784 | 0.00202541 | 1.88611 |
| /home/runner/work/_temp/setup-uv-cache/archive-v0/d0K4tb5aZoLwkeaA/lib/python3.11/site-packages/lightgbm/sklearn.py:1381:fit | 1 | 1 | 1.9239e-05 | 1.73658 |
| /home/runner/work/_temp/setup-uv-cache/archive-v0/d0K4tb5aZoLwkeaA/lib/python3.11/site-packages/lightgbm/sklearn.py:907:fit | 1 | 1 | 7.9947e-05 | 1.73656 |

### Native/C/C++/Cython-flavored stack leaf hotspots (py-spy --native)
| leaf_frame | sample_weight |
| --- | --- |
| update | 1.54 |
| __init_from_np2d | 0.23 |
| _compile_bytecode | 0.16 |
| _call_with_frames_removed | 0.1 |
| get_data | 0.09 |
| raw_decode | 0.08 |
| <module> | 0.07 |
| dedent | 0.07 |
| make_regression | 0.06 |
| __inner_predict_np2d | 0.05 |
| _path_stat | 0.04 |
| _monitor_peak_rss | 0.04 |

