# Profiling snapshots

## sklearn_hgb
### Python-level (cProfile) top cumulative entries
| function | primitive_calls | total_calls | total_time_s | cumulative_time_s |
| --- | --- | --- | --- | --- |
| ~:0:<built-in method builtins.exec> | 1 | 1665 | 0.0421886 | 5.58059 |
| D:\a\cursor-sandbox\cursor-sandbox\hgbdt_performance_analysis\benchmark_gbdt_regressors.py:1:<module> | 1 | 1 | 9.07e-05 | 5.58058 |
| D:\a\cursor-sandbox\cursor-sandbox\hgbdt_performance_analysis\benchmark_gbdt_regressors.py:450:main | 1 | 1 | 1.12e-05 | 2.86224 |
| D:\a\cursor-sandbox\cursor-sandbox\hgbdt_performance_analysis\benchmark_gbdt_regressors.py:408:_emit_single | 1 | 1 | 0.0004332 | 2.85938 |
| D:\a\cursor-sandbox\cursor-sandbox\hgbdt_performance_analysis\benchmark_gbdt_regressors.py:199:_single_run | 1 | 1 | 0.000309 | 2.85887 |
| <frozen importlib._bootstrap>:1165:_find_and_load | 11 | 1659 | 0.0141001 | 2.71682 |
| <frozen importlib._bootstrap>:1120:_find_and_load_unlocked | 11 | 1616 | 0.0091838 | 2.71651 |
| <frozen importlib._bootstrap>:666:_load_unlocked | 11 | 1567 | 0.0073125 | 2.71102 |
| <frozen importlib._bootstrap_external>:934:exec_module | 10 | 1325 | 0.0042892 | 2.71044 |
| <frozen importlib._bootstrap>:233:_call_with_frames_removed | 22 | 3790 | 0.0028556 | 2.70723 |
| ~:0:<built-in method builtins.__import__> | 67 | 779 | 0.0015575 | 2.44825 |
| D:\a\_temp\setup-uv-cache\archive-v0\CMFCN_wH4Ou9CwfD\Lib\site-packages\lightgbm\__init__.py:1:<module> | 1 | 1 | 5.48e-05 | 2.32526 |

