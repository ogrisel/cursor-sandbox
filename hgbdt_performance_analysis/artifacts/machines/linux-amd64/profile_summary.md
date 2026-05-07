# Profiling snapshots

## sklearn_hgb
### Python-level (cProfile) top cumulative entries
| function | primitive_calls | total_calls | total_time_s | cumulative_time_s |
| --- | --- | --- | --- | --- |
| ~:0:<built-in method builtins.exec> | 1 | 1381 | 0.0361953 | 4.13072 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:1:<module> | 1 | 1 | 8.2965e-05 | 4.1307 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:418:main | 1 | 1 | 1.051e-05 | 2.18467 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:374:_emit_single | 1 | 1 | 0.000204814 | 2.18162 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:168:_single_run | 1 | 1 | 0.000447696 | 2.18136 |
| /home/runner/work/_temp/setup-uv-cache/archive-v0/zrhr8eTcfHYHQpTz/lib/python3.11/site-packages/sklearn/base.py:1319:wrapper | 1 | 1 | 9.2811e-05 | 1.9911 |
| /home/runner/work/_temp/setup-uv-cache/archive-v0/zrhr8eTcfHYHQpTz/lib/python3.11/site-packages/sklearn/ensemble/_hist_gradient_boosting/gradient_boosting.py:512:fit | 1 | 1 | 0.0236628 | 1.99022 |
| <frozen importlib._bootstrap>:1165:_find_and_load | 13 | 1347 | 0.00808504 | 1.94587 |
| <frozen importlib._bootstrap>:1120:_find_and_load_unlocked | 13 | 1305 | 0.00608295 | 1.9456 |
| <frozen importlib._bootstrap>:666:_load_unlocked | 13 | 1261 | 0.00498677 | 1.94385 |
| <frozen importlib._bootstrap_external>:934:exec_module | 12 | 1061 | 0.00315842 | 1.94339 |
| <frozen importlib._bootstrap>:233:_call_with_frames_removed | 26 | 3060 | 0.00188293 | 1.94124 |

### Native/C/C++/Cython-flavored stack leaf hotspots (py-spy --native)
| leaf_frame | sample_weight |
| --- | --- |
| _compute_best_split_and_push | 0.79 |
| split_next | 0.63 |
| _initialize_root | 0.16 |
| dedent | 0.12 |
| _compile_bytecode | 0.1 |
| _call_with_frames_removed | 0.09 |
| transform | 0.09 |
| __init__ | 0.08 |
| get_data | 0.06 |
| cleandoc | 0.06 |
| fit | 0.06 |
| make_regression | 0.05 |

## lightgbm_hist
### Python-level (cProfile) top cumulative entries
| function | primitive_calls | total_calls | total_time_s | cumulative_time_s |
| --- | --- | --- | --- | --- |
| ~:0:<built-in method builtins.exec> | 1 | 1379 | 0.0363002 | 4.17664 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:1:<module> | 1 | 1 | 7.6414e-05 | 4.17661 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:418:main | 1 | 1 | 9.217e-06 | 2.25958 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:374:_emit_single | 1 | 1 | 4.1759e-05 | 2.25668 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:168:_single_run | 1 | 1 | 0.000493151 | 2.25647 |
| /home/runner/work/_temp/setup-uv-cache/archive-v0/zrhr8eTcfHYHQpTz/lib/python3.11/site-packages/lightgbm/sklearn.py:1381:fit | 1 | 1 | 2.2201e-05 | 2.05537 |
| /home/runner/work/_temp/setup-uv-cache/archive-v0/zrhr8eTcfHYHQpTz/lib/python3.11/site-packages/lightgbm/sklearn.py:907:fit | 1 | 1 | 9.6812e-05 | 2.05534 |
| /home/runner/work/_temp/setup-uv-cache/archive-v0/zrhr8eTcfHYHQpTz/lib/python3.11/site-packages/lightgbm/engine.py:109:train | 1 | 1 | 0.00150363 | 2.05271 |
| <frozen importlib._bootstrap>:1165:_find_and_load | 12 | 1345 | 0.00797676 | 1.91585 |
| <frozen importlib._bootstrap>:1120:_find_and_load_unlocked | 12 | 1303 | 0.00607425 | 1.9156 |
| <frozen importlib._bootstrap>:666:_load_unlocked | 12 | 1259 | 0.00494693 | 1.91403 |
| <frozen importlib._bootstrap_external>:934:exec_module | 11 | 1059 | 0.00304323 | 1.91361 |

### Native/C/C++/Cython-flavored stack leaf hotspots (py-spy --native)
| leaf_frame | sample_weight |
| --- | --- |
| update | 1.82 |
| __init_from_np2d | 0.19 |
| _compile_bytecode | 0.17 |
| __init__ | 0.15 |
| __inner_predict_np2d | 0.09 |
| dedent | 0.08 |
| <module> | 0.07 |
| _path_stat | 0.06 |
| make_regression | 0.06 |
| _is_at_section | 0.05 |
| _monitor_peak_rss | 0.05 |
| _call_with_frames_removed | 0.04 |

