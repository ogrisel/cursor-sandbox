# Profiling snapshots

## sklearn_hgb
### Python-level (cProfile) top cumulative entries
| function | primitive_calls | total_calls | total_time_s | cumulative_time_s |
| --- | --- | --- | --- | --- |
| ~:0:<built-in method builtins.exec> | 1 | 1381 | 0.0310131 | 3.87818 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:1:<module> | 1 | 1 | 8.2492e-05 | 3.87816 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:418:main | 1 | 1 | 8.176e-06 | 2.27492 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:374:_emit_single | 1 | 1 | 0.000240697 | 2.27225 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:168:_single_run | 1 | 1 | 0.00033205 | 2.27194 |
| /home/runner/work/_temp/setup-uv-cache/archive-v0/3oqpvhxl9nm_HPyp/lib/python3.11/site-packages/sklearn/base.py:1319:wrapper | 1 | 1 | 8.6388e-05 | 2.12146 |
| /home/runner/work/_temp/setup-uv-cache/archive-v0/3oqpvhxl9nm_HPyp/lib/python3.11/site-packages/sklearn/ensemble/_hist_gradient_boosting/gradient_boosting.py:512:fit | 1 | 1 | 0.0387704 | 2.12075 |
| <frozen importlib._bootstrap>:1165:_find_and_load | 13 | 1347 | 0.00697979 | 1.60298 |
| <frozen importlib._bootstrap>:1120:_find_and_load_unlocked | 13 | 1305 | 0.00519539 | 1.60272 |
| <frozen importlib._bootstrap>:666:_load_unlocked | 13 | 1261 | 0.00409497 | 1.60114 |
| <frozen importlib._bootstrap_external>:934:exec_module | 12 | 1061 | 0.00270307 | 1.60072 |
| <frozen importlib._bootstrap>:233:_call_with_frames_removed | 26 | 3060 | 0.00155421 | 1.5986 |

### Native/C/C++/Cython-flavored stack leaf hotspots (py-spy --native)
| leaf_frame | sample_weight |
| --- | --- |
| split_next | 0.67 |
| _compute_best_split_and_push | 0.55 |
| _initialize_root | 0.19 |
| _compile_bytecode | 0.14 |
| _call_with_frames_removed | 0.12 |
| <module> | 0.09 |
| transform | 0.07 |
| _fill_predictor_arrays | 0.06 |
| _find_binning_thresholds | 0.06 |
| _unique1d | 0.06 |
| __init__ | 0.05 |
| cleandoc | 0.04 |

## lightgbm_hist
### Python-level (cProfile) top cumulative entries
| function | primitive_calls | total_calls | total_time_s | cumulative_time_s |
| --- | --- | --- | --- | --- |
| ~:0:<built-in method builtins.exec> | 1 | 1379 | 0.0313231 | 3.42649 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:1:<module> | 1 | 1 | 8.378e-05 | 3.42646 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:418:main | 1 | 1 | 9.216e-06 | 1.83227 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:374:_emit_single | 1 | 1 | 3.5897e-05 | 1.82969 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:168:_single_run | 1 | 1 | 0.000235737 | 1.82932 |
| /home/runner/work/_temp/setup-uv-cache/archive-v0/3oqpvhxl9nm_HPyp/lib/python3.11/site-packages/lightgbm/sklearn.py:1381:fit | 1 | 1 | 1.8162e-05 | 1.68137 |
| /home/runner/work/_temp/setup-uv-cache/archive-v0/3oqpvhxl9nm_HPyp/lib/python3.11/site-packages/lightgbm/sklearn.py:907:fit | 1 | 1 | 7.8452e-05 | 1.68136 |
| /home/runner/work/_temp/setup-uv-cache/archive-v0/3oqpvhxl9nm_HPyp/lib/python3.11/site-packages/lightgbm/engine.py:109:train | 1 | 1 | 0.00321657 | 1.67936 |
| <frozen importlib._bootstrap>:1165:_find_and_load | 12 | 1345 | 0.00688549 | 1.59309 |
| <frozen importlib._bootstrap>:1120:_find_and_load_unlocked | 12 | 1303 | 0.00523883 | 1.59287 |
| <frozen importlib._bootstrap>:666:_load_unlocked | 12 | 1259 | 0.00399619 | 1.59142 |
| <frozen importlib._bootstrap_external>:934:exec_module | 11 | 1059 | 0.00261246 | 1.59106 |

### Native/C/C++/Cython-flavored stack leaf hotspots (py-spy --native)
| leaf_frame | sample_weight |
| --- | --- |
| update | 1.47 |
| __init_from_np2d | 0.19 |
| _compile_bytecode | 0.11 |
| dedent | 0.09 |
| _call_with_frames_removed | 0.08 |
| make_regression | 0.08 |
| get_data | 0.07 |
| __inner_predict_np2d | 0.06 |
| _monitor_peak_rss | 0.06 |
| cleandoc | 0.05 |
| update_wrapper | 0.04 |
| __init__ | 0.04 |

