# Profiling snapshots

## sklearn_hgb
### Python-level (cProfile) top cumulative entries
| function | primitive_calls | total_calls | total_time_s | cumulative_time_s |
| --- | --- | --- | --- | --- |
| ~:0:<built-in method builtins.exec> | 1 | 1381 | 0.0325318 | 3.97914 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:1:<module> | 1 | 1 | 8.9314e-05 | 3.97911 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:418:main | 1 | 1 | 8.921e-06 | 2.33827 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:374:_emit_single | 1 | 1 | 0.000240894 | 2.33557 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:168:_single_run | 1 | 1 | 0.000347272 | 2.33526 |
| /home/runner/work/_temp/setup-uv-cache/archive-v0/sHjkcerKmD2m1V7T/lib/python3.11/site-packages/sklearn/base.py:1319:wrapper | 1 | 1 | 8.5947e-05 | 2.18064 |
| /home/runner/work/_temp/setup-uv-cache/archive-v0/sHjkcerKmD2m1V7T/lib/python3.11/site-packages/sklearn/ensemble/_hist_gradient_boosting/gradient_boosting.py:512:fit | 1 | 1 | 0.043463 | 2.1799 |
| <frozen importlib._bootstrap>:1165:_find_and_load | 13 | 1347 | 0.00694796 | 1.64063 |
| <frozen importlib._bootstrap>:1120:_find_and_load_unlocked | 13 | 1305 | 0.00531242 | 1.64038 |
| <frozen importlib._bootstrap>:666:_load_unlocked | 13 | 1261 | 0.00417197 | 1.63875 |
| <frozen importlib._bootstrap_external>:934:exec_module | 12 | 1061 | 0.00271275 | 1.63832 |
| <frozen importlib._bootstrap>:233:_call_with_frames_removed | 26 | 3060 | 0.00165147 | 1.63614 |

### Native/C/C++/Cython-flavored stack leaf hotspots (py-spy --native)
| leaf_frame | sample_weight |
| --- | --- |
| split_next | 0.77 |
| _compute_best_split_and_push | 0.57 |
| _initialize_root | 0.32 |
| _compile_bytecode | 0.15 |
| _unique1d | 0.13 |
| <module> | 0.1 |
| _call_with_frames_removed | 0.08 |
| make_regression | 0.07 |
| _fill_predictor_arrays | 0.06 |
| sort | 0.06 |
| _signature_from_callable | 0.05 |
| dedent | 0.05 |

## lightgbm_hist
### Python-level (cProfile) top cumulative entries
| function | primitive_calls | total_calls | total_time_s | cumulative_time_s |
| --- | --- | --- | --- | --- |
| ~:0:<built-in method builtins.exec> | 1 | 1379 | 0.0319472 | 3.50485 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:1:<module> | 1 | 1 | 8.742e-05 | 3.50482 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:418:main | 1 | 1 | 1.0329e-05 | 1.86428 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:374:_emit_single | 1 | 1 | 4.8834e-05 | 1.86162 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:168:_single_run | 1 | 1 | 0.000366469 | 1.8612 |
| /home/runner/work/_temp/setup-uv-cache/archive-v0/sHjkcerKmD2m1V7T/lib/python3.11/site-packages/lightgbm/sklearn.py:1381:fit | 1 | 1 | 1.9688e-05 | 1.70847 |
| /home/runner/work/_temp/setup-uv-cache/archive-v0/sHjkcerKmD2m1V7T/lib/python3.11/site-packages/lightgbm/sklearn.py:907:fit | 1 | 1 | 0.000101795 | 1.70845 |
| /home/runner/work/_temp/setup-uv-cache/archive-v0/sHjkcerKmD2m1V7T/lib/python3.11/site-packages/lightgbm/engine.py:109:train | 1 | 1 | 0.00378915 | 1.70632 |
| <frozen importlib._bootstrap>:1165:_find_and_load | 12 | 1345 | 0.00723658 | 1.63939 |
| <frozen importlib._bootstrap>:1120:_find_and_load_unlocked | 12 | 1303 | 0.00526052 | 1.63916 |
| <frozen importlib._bootstrap>:666:_load_unlocked | 12 | 1259 | 0.00414877 | 1.63769 |
| <frozen importlib._bootstrap_external>:934:exec_module | 11 | 1059 | 0.00280139 | 1.63732 |

### Native/C/C++/Cython-flavored stack leaf hotspots (py-spy --native)
| leaf_frame | sample_weight |
| --- | --- |
| update | 1.45 |
| __init_from_np2d | 0.21 |
| _call_with_frames_removed | 0.12 |
| dedent | 0.08 |
| make_regression | 0.08 |
| _compile_bytecode | 0.07 |
| <module> | 0.06 |
| __init__ | 0.05 |
| __inner_predict_np2d | 0.05 |
| sub | 0.03 |
| _path_stat | 0.03 |
| get_data | 0.03 |

