# Profiling snapshots

## sklearn_hgb
### Python-level (cProfile) top cumulative entries
| function | primitive_calls | total_calls | total_time_s | cumulative_time_s |
| --- | --- | --- | --- | --- |
| ~:0:<built-in method builtins.exec> | 1 | 1664 | 0.0394155 | 3.87386 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:1:<module> | 1 | 1 | 7.8147e-05 | 3.87382 |
| <frozen importlib._bootstrap>:1165:_find_and_load | 11 | 1666 | 0.0111954 | 2.27324 |
| <frozen importlib._bootstrap>:1120:_find_and_load_unlocked | 11 | 1623 | 0.00790939 | 2.27302 |
| <frozen importlib._bootstrap>:666:_load_unlocked | 11 | 1570 | 0.00619615 | 2.27142 |
| <frozen importlib._bootstrap_external>:934:exec_module | 10 | 1324 | 0.00392399 | 2.27104 |
| <frozen importlib._bootstrap>:233:_call_with_frames_removed | 22 | 3784 | 0.00239147 | 2.269 |
| ~:0:<built-in method builtins.__import__> | 67 | 778 | 0.00141915 | 2.07521 |
| /home/runner/work/_temp/setup-uv-cache/archive-v0/6I8s83tJxRFMh7hh/lib/python3.11/site-packages/lightgbm/__init__.py:1:<module> | 1 | 1 | 5.2126e-05 | 1.93703 |
| /home/runner/work/_temp/setup-uv-cache/archive-v0/6I8s83tJxRFMh7hh/lib/python3.11/site-packages/lightgbm/basic.py:1:<module> | 1 | 1 | 0.000273507 | 1.92259 |
| /home/runner/work/_temp/setup-uv-cache/archive-v0/6I8s83tJxRFMh7hh/lib/python3.11/site-packages/lightgbm/compat.py:1:<module> | 1 | 1 | 6.343e-05 | 1.74228 |
| /home/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:444:main | 1 | 1 | 9.888e-06 | 1.59933 |

### Native/C/C++/Cython-flavored stack leaf hotspots (py-spy --native)
| leaf_frame | sample_weight |
| --- | --- |
| _compute_best_split_and_push | 0.8 |
| split_next | 0.37 |
| _call_with_frames_removed | 0.17 |
| dedent | 0.15 |
| _initialize_root | 0.14 |
| <module> | 0.13 |
| transform | 0.12 |
| get_data | 0.11 |
| _monitor_peak_rss | 0.09 |
| _joinrealpath | 0.08 |
| _is_at_section | 0.07 |
| _compile_bytecode | 0.06 |

