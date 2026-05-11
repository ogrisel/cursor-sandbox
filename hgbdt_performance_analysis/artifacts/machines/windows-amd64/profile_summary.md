# Profiling snapshots

## sklearn_hgb
### Python-level (cProfile) top cumulative entries
| function | primitive_calls | total_calls | total_time_s | cumulative_time_s |
| --- | --- | --- | --- | --- |
| ~:0:<built-in method builtins.exec> | 1 | 1665 | 0.0435291 | 5.00921 |
| D:\a\cursor-sandbox\cursor-sandbox\hgbdt_performance_analysis\benchmark_gbdt_regressors.py:1:<module> | 1 | 1 | 9.06e-05 | 5.0092 |
| <frozen importlib._bootstrap>:1165:_find_and_load | 11 | 1659 | 0.0134518 | 2.58616 |
| <frozen importlib._bootstrap>:1120:_find_and_load_unlocked | 11 | 1616 | 0.0087106 | 2.58586 |
| <frozen importlib._bootstrap>:666:_load_unlocked | 11 | 1567 | 0.006971 | 2.58065 |
| <frozen importlib._bootstrap_external>:934:exec_module | 10 | 1325 | 0.0041711 | 2.58009 |
| <frozen importlib._bootstrap>:233:_call_with_frames_removed | 22 | 3790 | 0.0028411 | 2.57709 |
| D:\a\cursor-sandbox\cursor-sandbox\hgbdt_performance_analysis\benchmark_gbdt_regressors.py:447:main | 1 | 1 | 1.01e-05 | 2.42158 |
| D:\a\cursor-sandbox\cursor-sandbox\hgbdt_performance_analysis\benchmark_gbdt_regressors.py:405:_emit_single | 1 | 1 | 0.0004602 | 2.41878 |
| D:\a\cursor-sandbox\cursor-sandbox\hgbdt_performance_analysis\benchmark_gbdt_regressors.py:199:_single_run | 1 | 1 | 0.0002702 | 2.41824 |
| ~:0:<built-in method builtins.__import__> | 67 | 779 | 0.001519 | 2.31469 |
| D:\a\_temp\setup-uv-cache\archive-v0\91l2juAw7gYAmxcz\Lib\site-packages\sklearn\base.py:1319:wrapper | 1 | 1 | 0.0005025 | 2.23425 |

