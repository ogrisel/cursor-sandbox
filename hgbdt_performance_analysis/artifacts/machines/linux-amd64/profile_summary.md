# Profiling snapshots

## sklearn_hgb
### Python-level (cProfile) top cumulative entries
| function | primitive_calls | total_calls | total_time_s | cumulative_time_s |
| --- | --- | --- | --- | --- |
| ~:0:<built-in method builtins.exec> | 1 | 1381 | 0.0358306 | 4.1635 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:1:<module> | 1 | 1 | 7.7864e-05 | 4.16348 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:418:main | 1 | 1 | 1.0459e-05 | 2.19953 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:374:_emit_single | 1 | 1 | 0.000185326 | 2.1966 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:168:_single_run | 1 | 1 | 0.000481998 | 2.19636 |
| /home/runner/work/_temp/setup-uv-cache/archive-v0/ba3nAfDraag9wGUS/lib/python3.11/site-packages/sklearn/base.py:1319:wrapper | 1 | 1 | 9.4706e-05 | 2.00531 |
| /home/runner/work/_temp/setup-uv-cache/archive-v0/ba3nAfDraag9wGUS/lib/python3.11/site-packages/sklearn/ensemble/_hist_gradient_boosting/gradient_boosting.py:512:fit | 1 | 1 | 0.0268324 | 2.00436 |
| <frozen importlib._bootstrap>:1165:_find_and_load | 13 | 1347 | 0.00949898 | 1.96361 |
| <frozen importlib._bootstrap>:1120:_find_and_load_unlocked | 13 | 1305 | 0.00618134 | 1.96333 |
| <frozen importlib._bootstrap>:666:_load_unlocked | 13 | 1261 | 0.00519143 | 1.9615 |
| <frozen importlib._bootstrap_external>:934:exec_module | 12 | 1061 | 0.00312241 | 1.96103 |
| <frozen importlib._bootstrap>:233:_call_with_frames_removed | 26 | 3060 | 0.001882 | 1.95871 |

### Native/C/C++/Cython-flavored stack leaf hotspots (py-spy --native)
| leaf_frame | sample_weight |
| --- | --- |
| _compute_best_split_and_push | 0.82 |
| split_next | 0.63 |
| _initialize_root | 0.18 |
| _compile_bytecode | 0.16 |
| transform | 0.13 |
| _monitor_peak_rss | 0.13 |
| make_regression | 0.11 |
| dedent | 0.1 |
| __init__ | 0.08 |
| <module> | 0.06 |
| get_data | 0.06 |
| _call_with_frames_removed | 0.06 |

## lightgbm_hist
### Python-level (cProfile) top cumulative entries
| function | primitive_calls | total_calls | total_time_s | cumulative_time_s |
| --- | --- | --- | --- | --- |
| ~:0:<built-in method builtins.exec> | 1 | 1379 | 0.0359617 | 4.25633 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:1:<module> | 1 | 1 | 7.9421e-05 | 4.25632 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:418:main | 1 | 1 | 1.019e-05 | 2.29282 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:374:_emit_single | 1 | 1 | 7.1551e-05 | 2.28997 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:168:_single_run | 1 | 1 | 0.000480856 | 2.28973 |
| /home/runner/work/_temp/setup-uv-cache/archive-v0/ba3nAfDraag9wGUS/lib/python3.11/site-packages/lightgbm/sklearn.py:1381:fit | 1 | 1 | 2.5157e-05 | 2.08693 |
| /home/runner/work/_temp/setup-uv-cache/archive-v0/ba3nAfDraag9wGUS/lib/python3.11/site-packages/lightgbm/sklearn.py:907:fit | 1 | 1 | 0.000106557 | 2.0869 |
| /home/runner/work/_temp/setup-uv-cache/archive-v0/ba3nAfDraag9wGUS/lib/python3.11/site-packages/lightgbm/engine.py:109:train | 1 | 1 | 0.00268048 | 2.08411 |
| <frozen importlib._bootstrap>:1165:_find_and_load | 12 | 1345 | 0.00836996 | 1.96222 |
| <frozen importlib._bootstrap>:1120:_find_and_load_unlocked | 12 | 1303 | 0.00613447 | 1.96197 |
| <frozen importlib._bootstrap>:666:_load_unlocked | 12 | 1259 | 0.00498534 | 1.96038 |
| <frozen importlib._bootstrap_external>:934:exec_module | 11 | 1059 | 0.00309715 | 1.95997 |

### Native/C/C++/Cython-flavored stack leaf hotspots (py-spy --native)
| leaf_frame | sample_weight |
| --- | --- |
| update | 2.13 |
| __init_from_np2d | 0.3 |
| _compile_bytecode | 0.14 |
| _call_with_frames_removed | 0.12 |
| make_regression | 0.09 |
| get_data | 0.06 |
| <module> | 0.05 |
| __init__ | 0.04 |
| namedtuple | 0.04 |
| dedent | 0.04 |
| dedent_lines | 0.04 |
| _monitor_peak_rss | 0.04 |

