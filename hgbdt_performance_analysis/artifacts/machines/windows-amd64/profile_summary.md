# Profiling snapshots

## sklearn_hgb
### Python-level (cProfile) top cumulative entries
| function | primitive_calls | total_calls | total_time_s | cumulative_time_s |
| --- | --- | --- | --- | --- |
| ~:0:<built-in method builtins.exec> | 1 | 1665 | 0.0425078 | 4.95638 |
| D:\a\cursor-sandbox\cursor-sandbox\hgbdt_performance_analysis\benchmark_gbdt_regressors.py:1:<module> | 1 | 1 | 0.0001001 | 4.95634 |
| <frozen importlib._bootstrap>:1165:_find_and_load | 11 | 1659 | 0.0126566 | 2.51379 |
| <frozen importlib._bootstrap>:1120:_find_and_load_unlocked | 11 | 1616 | 0.0084772 | 2.51343 |
| <frozen importlib._bootstrap>:666:_load_unlocked | 11 | 1567 | 0.0064908 | 2.5088 |
| <frozen importlib._bootstrap_external>:934:exec_module | 10 | 1325 | 0.0038957 | 2.50826 |
| <frozen importlib._bootstrap>:233:_call_with_frames_removed | 22 | 3790 | 0.0024249 | 2.50522 |
| D:\a\cursor-sandbox\cursor-sandbox\hgbdt_performance_analysis\benchmark_gbdt_regressors.py:444:main | 1 | 1 | 1.18e-05 | 2.44101 |
| D:\a\cursor-sandbox\cursor-sandbox\hgbdt_performance_analysis\benchmark_gbdt_regressors.py:402:_emit_single | 1 | 1 | 0.0004057 | 2.43826 |
| D:\a\cursor-sandbox\cursor-sandbox\hgbdt_performance_analysis\benchmark_gbdt_regressors.py:199:_single_run | 1 | 1 | 0.0002768 | 2.43776 |
| ~:0:<built-in method builtins.__import__> | 67 | 779 | 0.0014404 | 2.25694 |
| D:\a\_temp\setup-uv-cache\archive-v0\XVsamQM-j-UeMe9U\Lib\site-packages\sklearn\base.py:1319:wrapper | 1 | 1 | 0.0005391 | 2.25516 |

