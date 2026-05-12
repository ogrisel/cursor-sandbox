# Profiling snapshots

## sklearn_hgb
### Python-level (cProfile) top cumulative entries
| function | primitive_calls | total_calls | total_time_s | cumulative_time_s |
| --- | --- | --- | --- | --- |
| ~:0:<built-in method builtins.exec> | 1 | 1665 | 0.0474042 | 5.40641 |
| D:\a\cursor-sandbox\cursor-sandbox\hgbdt_performance_analysis\benchmark_gbdt_regressors.py:1:<module> | 1 | 1 | 0.0001042 | 5.40634 |
| <frozen importlib._bootstrap>:1165:_find_and_load | 11 | 1659 | 0.015954 | 2.72872 |
| <frozen importlib._bootstrap>:1120:_find_and_load_unlocked | 11 | 1616 | 0.0086714 | 2.72841 |
| <frozen importlib._bootstrap>:666:_load_unlocked | 11 | 1567 | 0.0069227 | 2.72359 |
| <frozen importlib._bootstrap_external>:934:exec_module | 10 | 1325 | 0.0041071 | 2.72305 |
| <frozen importlib._bootstrap>:233:_call_with_frames_removed | 22 | 3790 | 0.0027813 | 2.71968 |
| D:\a\cursor-sandbox\cursor-sandbox\hgbdt_performance_analysis\benchmark_gbdt_regressors.py:444:main | 1 | 1 | 1.18e-05 | 2.676 |
| D:\a\cursor-sandbox\cursor-sandbox\hgbdt_performance_analysis\benchmark_gbdt_regressors.py:402:_emit_single | 1 | 1 | 0.0006006 | 2.67321 |
| D:\a\cursor-sandbox\cursor-sandbox\hgbdt_performance_analysis\benchmark_gbdt_regressors.py:199:_single_run | 1 | 1 | 0.0003911 | 2.6725 |
| D:\a\_temp\setup-uv-cache\archive-v0\ccpljEO9Ea8zGI4e\Lib\site-packages\sklearn\base.py:1319:wrapper | 1 | 1 | 0.0006802 | 2.50627 |
| D:\a\_temp\setup-uv-cache\archive-v0\ccpljEO9Ea8zGI4e\Lib\site-packages\sklearn\ensemble\_hist_gradient_boosting\gradient_boosting.py:512:fit | 1 | 1 | 0.108308 | 2.50461 |

