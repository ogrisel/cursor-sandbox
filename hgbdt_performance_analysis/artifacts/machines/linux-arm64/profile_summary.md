# Profiling snapshots

## sklearn_hgb
### Python-level (cProfile) top cumulative entries
| function | primitive_calls | total_calls | total_time_s | cumulative_time_s |
| --- | --- | --- | --- | --- |
| ~:0:<built-in method builtins.exec> | 1 | 1666 | 0.0341559 | 4.0774 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:1:<module> | 1 | 1 | 0.000114637 | 4.07737 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:447:main | 1 | 1 | 1.1184e-05 | 2.27603 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:405:_emit_single | 1 | 1 | 0.000189997 | 2.27359 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:195:_single_run | 1 | 1 | 0.000315192 | 2.2733 |
| /home/runner/work/_temp/setup-uv-cache/archive-v0/V_NtNyvpTlkMW5nT/lib/python3.11/site-packages/sklearn/base.py:1319:wrapper | 1 | 1 | 8.3508e-05 | 2.12107 |
| /home/runner/work/_temp/setup-uv-cache/archive-v0/V_NtNyvpTlkMW5nT/lib/python3.11/site-packages/sklearn/ensemble/_hist_gradient_boosting/gradient_boosting.py:512:fit | 1 | 1 | 0.0392621 | 2.1203 |
| <frozen importlib._bootstrap>:1165:_find_and_load | 12 | 1668 | 0.00903072 | 1.80085 |
| <frozen importlib._bootstrap>:1120:_find_and_load_unlocked | 12 | 1625 | 0.00640119 | 1.80061 |
| <frozen importlib._bootstrap>:666:_load_unlocked | 12 | 1572 | 0.00513725 | 1.79913 |
| <frozen importlib._bootstrap_external>:934:exec_module | 11 | 1326 | 0.00338957 | 1.79876 |
| <frozen importlib._bootstrap>:233:_call_with_frames_removed | 24 | 3788 | 0.00196395 | 1.79666 |

### Native/C/C++/Cython-flavored stack leaf hotspots (py-spy --native)
| leaf_frame | sample_weight |
| --- | --- |
| split_next | 0.82 |
| _compute_best_split_and_push | 0.7 |
| _initialize_root | 0.32 |
| _compile_bytecode | 0.14 |
| _call_with_frames_removed | 0.14 |
| <module> | 0.11 |
| dedent | 0.1 |
| make_regression | 0.09 |
| sort | 0.08 |
| _unique1d | 0.07 |
| get_data | 0.05 |
| full | 0.05 |

## lightgbm_hist
### Python-level (cProfile) top cumulative entries
| function | primitive_calls | total_calls | total_time_s | cumulative_time_s |
| --- | --- | --- | --- | --- |
| ~:0:<built-in method builtins.exec> | 1 | 1664 | 0.035892 | 3.764 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:1:<module> | 1 | 1 | 8.246e-05 | 3.76398 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:447:main | 1 | 1 | 8.496e-06 | 1.93523 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:405:_emit_single | 1 | 1 | 6.1852e-05 | 1.93281 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:195:_single_run | 1 | 1 | 0.000368163 | 1.93238 |
| <frozen importlib._bootstrap>:1165:_find_and_load | 11 | 1666 | 0.00900555 | 1.82759 |
| <frozen importlib._bootstrap>:1120:_find_and_load_unlocked | 11 | 1623 | 0.0065904 | 1.82739 |
| <frozen importlib._bootstrap>:666:_load_unlocked | 11 | 1570 | 0.00508536 | 1.82597 |
| <frozen importlib._bootstrap_external>:934:exec_module | 10 | 1324 | 0.00344513 | 1.82563 |
| <frozen importlib._bootstrap>:233:_call_with_frames_removed | 22 | 3784 | 0.00201329 | 1.82356 |
| /home/runner/work/_temp/setup-uv-cache/archive-v0/V_NtNyvpTlkMW5nT/lib/python3.11/site-packages/lightgbm/sklearn.py:1381:fit | 1 | 1 | 1.8447e-05 | 1.7023 |
| /home/runner/work/_temp/setup-uv-cache/archive-v0/V_NtNyvpTlkMW5nT/lib/python3.11/site-packages/lightgbm/sklearn.py:907:fit | 1 | 1 | 7.374e-05 | 1.70228 |

### Native/C/C++/Cython-flavored stack leaf hotspots (py-spy --native)
| leaf_frame | sample_weight |
| --- | --- |
| update | 1.68 |
| _call_with_frames_removed | 0.14 |
| make_regression | 0.14 |
| __init_from_np2d | 0.13 |
| dedent | 0.1 |
| _compile_bytecode | 0.07 |
| <module> | 0.06 |
| dump_model | 0.06 |
| raw_decode | 0.05 |
| cleandoc | 0.04 |
| get_data | 0.03 |
| _attach_argparser_methods | 0.03 |

