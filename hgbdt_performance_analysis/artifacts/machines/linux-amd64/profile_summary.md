# Profiling snapshots

## sklearn_hgb
### Python-level (cProfile) top cumulative entries
| function | primitive_calls | total_calls | total_time_s | cumulative_time_s |
| --- | --- | --- | --- | --- |
| ~:0:<built-in method builtins.exec> | 1 | 1666 | 0.0389232 | 4.4186 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:1:<module> | 1 | 1 | 7.769e-05 | 4.41857 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:447:main | 1 | 1 | 1.0708e-05 | 2.37342 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:405:_emit_single | 1 | 1 | 0.000192694 | 2.3707 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:195:_single_run | 1 | 1 | 0.000327907 | 2.37044 |
| /home/runner/work/_temp/setup-uv-cache/archive-v0/dCKCz3jmxz15Aov5/lib/python3.11/site-packages/sklearn/base.py:1319:wrapper | 1 | 1 | 0.000100388 | 2.14864 |
| /home/runner/work/_temp/setup-uv-cache/archive-v0/dCKCz3jmxz15Aov5/lib/python3.11/site-packages/sklearn/ensemble/_hist_gradient_boosting/gradient_boosting.py:512:fit | 1 | 1 | 0.0365196 | 2.14764 |
| <frozen importlib._bootstrap>:1165:_find_and_load | 12 | 1668 | 0.00983592 | 2.04459 |
| <frozen importlib._bootstrap>:1120:_find_and_load_unlocked | 12 | 1625 | 0.00702679 | 2.04434 |
| <frozen importlib._bootstrap>:666:_load_unlocked | 12 | 1572 | 0.00570706 | 2.04287 |
| <frozen importlib._bootstrap_external>:934:exec_module | 11 | 1326 | 0.00321433 | 2.04246 |
| <frozen importlib._bootstrap>:233:_call_with_frames_removed | 24 | 3788 | 0.00208408 | 2.04045 |

### Native/C/C++/Cython-flavored stack leaf hotspots (py-spy --native)
| leaf_frame | sample_weight |
| --- | --- |
| _compute_best_split_and_push | 0.67 |
| split_next | 0.66 |
| _initialize_root | 0.26 |
| dedent | 0.12 |
| _compile_bytecode | 0.11 |
| _monitor_peak_rss | 0.11 |
| make_regression | 0.07 |
| <module> | 0.06 |
| __init__ | 0.06 |
| _fill_predictor_arrays | 0.06 |
| predict | 0.06 |
| _is_at_section | 0.04 |

## lightgbm_hist
### Python-level (cProfile) top cumulative entries
| function | primitive_calls | total_calls | total_time_s | cumulative_time_s |
| --- | --- | --- | --- | --- |
| ~:0:<built-in method builtins.exec> | 1 | 1664 | 0.0390851 | 4.17857 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:1:<module> | 1 | 1 | 7.301e-05 | 4.17854 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:447:main | 1 | 1 | 1.1298e-05 | 2.15122 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:405:_emit_single | 1 | 1 | 5.076e-05 | 2.14851 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:195:_single_run | 1 | 1 | 0.000316574 | 2.14822 |
| <frozen importlib._bootstrap>:1165:_find_and_load | 11 | 1666 | 0.0105514 | 2.02614 |
| <frozen importlib._bootstrap>:1120:_find_and_load_unlocked | 11 | 1623 | 0.00697854 | 2.02591 |
| <frozen importlib._bootstrap>:666:_load_unlocked | 11 | 1570 | 0.00541151 | 2.02456 |
| <frozen importlib._bootstrap_external>:934:exec_module | 10 | 1324 | 0.00316373 | 2.02419 |
| <frozen importlib._bootstrap>:233:_call_with_frames_removed | 22 | 3784 | 0.00204471 | 2.02213 |
| /home/runner/work/_temp/setup-uv-cache/archive-v0/dCKCz3jmxz15Aov5/lib/python3.11/site-packages/lightgbm/sklearn.py:1381:fit | 1 | 1 | 2.53e-05 | 1.84873 |
| /home/runner/work/_temp/setup-uv-cache/archive-v0/dCKCz3jmxz15Aov5/lib/python3.11/site-packages/lightgbm/sklearn.py:907:fit | 1 | 1 | 0.000105352 | 1.8487 |

### Native/C/C++/Cython-flavored stack leaf hotspots (py-spy --native)
| leaf_frame | sample_weight |
| --- | --- |
| update | 1.45 |
| __init_from_np2d | 0.23 |
| _compile_bytecode | 0.16 |
| make_regression | 0.11 |
| dedent | 0.1 |
| _call_with_frames_removed | 0.09 |
| raw_decode | 0.08 |
| __init__ | 0.06 |
| cleandoc | 0.05 |
| dump_model | 0.05 |
| <module> | 0.04 |
| get_data | 0.04 |

