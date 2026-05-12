# Profiling snapshots

## sklearn_hgb
### Python-level (cProfile) top cumulative entries
| function | primitive_calls | total_calls | total_time_s | cumulative_time_s |
| --- | --- | --- | --- | --- |
| ~:0:<built-in method builtins.exec> | 1 | 1665 | 0.0421725 | 4.93742 |
| D:\a\cursor-sandbox\cursor-sandbox\hgbdt_performance_analysis\benchmark_gbdt_regressors.py:1:<module> | 1 | 1 | 8.52e-05 | 4.93739 |
| <frozen importlib._bootstrap>:1165:_find_and_load | 11 | 1659 | 0.0133888 | 2.55277 |
| <frozen importlib._bootstrap>:1120:_find_and_load_unlocked | 11 | 1616 | 0.008689 | 2.55247 |
| <frozen importlib._bootstrap>:666:_load_unlocked | 11 | 1567 | 0.0070074 | 2.54744 |
| <frozen importlib._bootstrap_external>:934:exec_module | 10 | 1325 | 0.0040677 | 2.5469 |
| <frozen importlib._bootstrap>:233:_call_with_frames_removed | 22 | 3790 | 0.0027299 | 2.54379 |
| D:\a\cursor-sandbox\cursor-sandbox\hgbdt_performance_analysis\benchmark_gbdt_regressors.py:444:main | 1 | 1 | 1.04e-05 | 2.38318 |
| D:\a\cursor-sandbox\cursor-sandbox\hgbdt_performance_analysis\benchmark_gbdt_regressors.py:402:_emit_single | 1 | 1 | 0.0005078 | 2.38038 |
| D:\a\cursor-sandbox\cursor-sandbox\hgbdt_performance_analysis\benchmark_gbdt_regressors.py:199:_single_run | 1 | 1 | 0.0002567 | 2.37979 |
| ~:0:<built-in method builtins.__import__> | 67 | 779 | 0.0014397 | 2.28585 |
| D:\a\_temp\setup-uv-cache\archive-v0\ihy8LU9nqlKIBdNq\Lib\site-packages\sklearn\base.py:1319:wrapper | 1 | 1 | 0.0004359 | 2.20487 |

