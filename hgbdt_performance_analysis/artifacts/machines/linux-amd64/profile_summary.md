# Profiling snapshots

## sklearn_hgb
### Python-level (cProfile) top cumulative entries
| function | primitive_calls | total_calls | total_time_s | cumulative_time_s |
| --- | --- | --- | --- | --- |
| ~:0:<built-in method builtins.exec> | 1 | 1666 | 0.0304683 | 3.58036 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:1:<module> | 1 | 1 | 6.0051e-05 | 3.58033 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:447:main | 1 | 1 | 8.332e-06 | 1.85853 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:405:_emit_single | 1 | 1 | 0.000162516 | 1.85637 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:195:_single_run | 1 | 1 | 0.000306199 | 1.85616 |
| <frozen importlib._bootstrap>:1165:_find_and_load | 12 | 1668 | 0.00871882 | 1.72162 |
| <frozen importlib._bootstrap>:1120:_find_and_load_unlocked | 12 | 1625 | 0.00544113 | 1.72141 |
| <frozen importlib._bootstrap>:666:_load_unlocked | 12 | 1572 | 0.00435447 | 1.71992 |
| <frozen importlib._bootstrap_external>:934:exec_module | 11 | 1326 | 0.00275897 | 1.7196 |
| <frozen importlib._bootstrap>:233:_call_with_frames_removed | 24 | 3788 | 0.00155847 | 1.7179 |
| /home/runner/work/_temp/setup-uv-cache/archive-v0/vvn4iEY1KdAAt1bt/lib/python3.11/site-packages/sklearn/base.py:1319:wrapper | 1 | 1 | 8.6138e-05 | 1.69757 |
| /home/runner/work/_temp/setup-uv-cache/archive-v0/vvn4iEY1KdAAt1bt/lib/python3.11/site-packages/sklearn/ensemble/_hist_gradient_boosting/gradient_boosting.py:512:fit | 1 | 1 | 0.0205917 | 1.69669 |

### Native/C/C++/Cython-flavored stack leaf hotspots (py-spy --native)
| leaf_frame | sample_weight |
| --- | --- |
| _compute_best_split_and_push | 0.58 |
| split_next | 0.46 |
| _initialize_root | 0.23 |
| _call_with_frames_removed | 0.14 |
| _compile_bytecode | 0.13 |
| get_data | 0.11 |
| transform | 0.11 |
| dedent | 0.1 |
| make_regression | 0.08 |
| sort | 0.08 |
| _unique1d | 0.07 |
| predict | 0.06 |

## lightgbm_hist
### Python-level (cProfile) top cumulative entries
| function | primitive_calls | total_calls | total_time_s | cumulative_time_s |
| --- | --- | --- | --- | --- |
| ~:0:<built-in method builtins.exec> | 1 | 1664 | 0.0304437 | 3.6368 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:1:<module> | 1 | 1 | 6.583e-05 | 3.63676 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:447:main | 1 | 1 | 7.641e-06 | 1.93569 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:405:_emit_single | 1 | 1 | 3.6355e-05 | 1.93356 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:195:_single_run | 1 | 1 | 0.000334183 | 1.93332 |
| <frozen importlib._bootstrap>:1165:_find_and_load | 11 | 1666 | 0.00888167 | 1.70007 |
| <frozen importlib._bootstrap>:1120:_find_and_load_unlocked | 11 | 1623 | 0.00549645 | 1.69986 |
| <frozen importlib._bootstrap>:666:_load_unlocked | 11 | 1570 | 0.00452342 | 1.69863 |
| <frozen importlib._bootstrap_external>:934:exec_module | 10 | 1324 | 0.00277658 | 1.69832 |
| /home/runner/work/_temp/setup-uv-cache/archive-v0/vvn4iEY1KdAAt1bt/lib/python3.11/site-packages/lightgbm/sklearn.py:1381:fit | 1 | 1 | 1.9179e-05 | 1.69814 |
| /home/runner/work/_temp/setup-uv-cache/archive-v0/vvn4iEY1KdAAt1bt/lib/python3.11/site-packages/lightgbm/sklearn.py:907:fit | 1 | 1 | 8.8895e-05 | 1.69812 |
| <frozen importlib._bootstrap>:233:_call_with_frames_removed | 22 | 3784 | 0.00160813 | 1.6966 |

### Native/C/C++/Cython-flavored stack leaf hotspots (py-spy --native)
| leaf_frame | sample_weight |
| --- | --- |
| update | 1.53 |
| __init_from_np2d | 0.23 |
| _compile_bytecode | 0.11 |
| make_regression | 0.11 |
| dedent | 0.08 |
| <module> | 0.08 |
| get_data | 0.06 |
| _monitor_peak_rss | 0.06 |
| _is_at_section | 0.05 |
| raw_decode | 0.05 |
| cleandoc | 0.04 |
| __init__ | 0.04 |

