# Profiling snapshots

## sklearn_hgb
### Python-level (cProfile) top cumulative entries
| function | primitive_calls | total_calls | total_time_s | cumulative_time_s |
| --- | --- | --- | --- | --- |
| ~:0:<built-in method builtins.exec> | 1 | 1666 | 0.0397528 | 4.41117 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:1:<module> | 1 | 1 | 7.2936e-05 | 4.41115 |
| <frozen importlib._bootstrap>:1165:_find_and_load | 12 | 1668 | 0.0113319 | 2.21988 |
| <frozen importlib._bootstrap>:1120:_find_and_load_unlocked | 12 | 1625 | 0.00788622 | 2.21962 |
| <frozen importlib._bootstrap>:666:_load_unlocked | 12 | 1572 | 0.00635719 | 2.21787 |
| <frozen importlib._bootstrap_external>:934:exec_module | 11 | 1326 | 0.00397496 | 2.21744 |
| <frozen importlib._bootstrap>:233:_call_with_frames_removed | 24 | 3788 | 0.00248716 | 2.21527 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:447:main | 1 | 1 | 9.107e-06 | 2.19101 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:405:_emit_single | 1 | 1 | 0.000141775 | 2.18806 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:195:_single_run | 1 | 1 | 0.000503472 | 2.18786 |
| ~:0:<built-in method builtins.__import__> | 67 | 778 | 0.00151778 | 2.02474 |
| /home/runner/work/_temp/setup-uv-cache/archive-v0/g32Gm-gcomvofoOe/lib/python3.11/site-packages/sklearn/base.py:1319:wrapper | 1 | 1 | 8.8906e-05 | 1.99055 |

### Native/C/C++/Cython-flavored stack leaf hotspots (py-spy --native)
| leaf_frame | sample_weight |
| --- | --- |
| split_next | 0.74 |
| _compute_best_split_and_push | 0.62 |
| _initialize_root | 0.27 |
| _compile_bytecode | 0.18 |
| dedent | 0.17 |
| _call_with_frames_removed | 0.13 |
| <module> | 0.1 |
| transform | 0.1 |
| __init__ | 0.08 |
| _unique1d | 0.08 |
| cleandoc | 0.07 |
| _is_at_section | 0.06 |

## lightgbm_hist
### Python-level (cProfile) top cumulative entries
| function | primitive_calls | total_calls | total_time_s | cumulative_time_s |
| --- | --- | --- | --- | --- |
| ~:0:<built-in method builtins.exec> | 1 | 1664 | 0.040272 | 4.60864 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:1:<module> | 1 | 1 | 7.2635e-05 | 4.6086 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:447:main | 1 | 1 | 9.427e-06 | 2.34544 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:405:_emit_single | 1 | 1 | 4.0226e-05 | 2.34246 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:195:_single_run | 1 | 1 | 0.000505245 | 2.3422 |
| <frozen importlib._bootstrap>:1165:_find_and_load | 11 | 1666 | 0.0113899 | 2.26194 |
| <frozen importlib._bootstrap>:1120:_find_and_load_unlocked | 11 | 1623 | 0.00801498 | 2.26172 |
| <frozen importlib._bootstrap>:666:_load_unlocked | 11 | 1570 | 0.00649316 | 2.26006 |
| <frozen importlib._bootstrap_external>:934:exec_module | 10 | 1324 | 0.00400111 | 2.25966 |
| <frozen importlib._bootstrap>:233:_call_with_frames_removed | 22 | 3784 | 0.00253256 | 2.25758 |
| ~:0:<built-in method builtins.__import__> | 67 | 778 | 0.00143932 | 2.06856 |
| /home/runner/work/_temp/setup-uv-cache/archive-v0/g32Gm-gcomvofoOe/lib/python3.11/site-packages/lightgbm/sklearn.py:1381:fit | 1 | 1 | 2.3303e-05 | 2.04531 |

### Native/C/C++/Cython-flavored stack leaf hotspots (py-spy --native)
| leaf_frame | sample_weight |
| --- | --- |
| update | 1.87 |
| __init_from_np2d | 0.36 |
| _compile_bytecode | 0.17 |
| _call_with_frames_removed | 0.16 |
| raw_decode | 0.12 |
| __init__ | 0.1 |
| <module> | 0.09 |
| make_regression | 0.09 |
| get_data | 0.07 |
| dedent | 0.07 |
| __inner_predict_np2d | 0.07 |
| _is_at_section | 0.06 |

