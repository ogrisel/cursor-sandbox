# Profiling snapshots

## sklearn_hgb
### Python-level (cProfile) top cumulative entries
| function | primitive_calls | total_calls | total_time_s | cumulative_time_s |
| --- | --- | --- | --- | --- |
| ~:0:<built-in method builtins.exec> | 1 | 1665 | 0.0416588 | 4.85656 |
| D:\a\cursor-sandbox\cursor-sandbox\hgbdt_performance_analysis\benchmark_gbdt_regressors.py:1:<module> | 1 | 1 | 8.38e-05 | 4.85655 |
| <frozen importlib._bootstrap>:1165:_find_and_load | 11 | 1659 | 0.0128945 | 2.50064 |
| <frozen importlib._bootstrap>:1120:_find_and_load_unlocked | 11 | 1616 | 0.0086377 | 2.50035 |
| <frozen importlib._bootstrap>:666:_load_unlocked | 11 | 1567 | 0.006819 | 2.49533 |
| <frozen importlib._bootstrap_external>:934:exec_module | 10 | 1325 | 0.004106 | 2.49477 |
| <frozen importlib._bootstrap>:233:_call_with_frames_removed | 22 | 3790 | 0.002678 | 2.49172 |
| D:\a\cursor-sandbox\cursor-sandbox\hgbdt_performance_analysis\benchmark_gbdt_regressors.py:444:main | 1 | 1 | 1.05e-05 | 2.35443 |
| D:\a\cursor-sandbox\cursor-sandbox\hgbdt_performance_analysis\benchmark_gbdt_regressors.py:402:_emit_single | 1 | 1 | 0.0004887 | 2.35168 |
| D:\a\cursor-sandbox\cursor-sandbox\hgbdt_performance_analysis\benchmark_gbdt_regressors.py:199:_single_run | 1 | 1 | 0.0002412 | 2.35111 |
| ~:0:<built-in method builtins.__import__> | 67 | 779 | 0.0014479 | 2.23593 |
| D:\a\_temp\setup-uv-cache\archive-v0\qYI0tlrp7MNOHLnb\Lib\site-packages\sklearn\base.py:1319:wrapper | 1 | 1 | 0.0004217 | 2.1754 |

