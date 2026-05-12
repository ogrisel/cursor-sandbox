# Profiling snapshots

## sklearn_hgb
### Python-level (cProfile) top cumulative entries
| function | primitive_calls | total_calls | total_time_s | cumulative_time_s |
| --- | --- | --- | --- | --- |
| ~:0:<built-in method builtins.exec> | 1 | 1665 | 0.0413646 | 4.92486 |
| D:\a\cursor-sandbox\cursor-sandbox\hgbdt_performance_analysis\benchmark_gbdt_regressors.py:1:<module> | 1 | 1 | 7.61e-05 | 4.92483 |
| <frozen importlib._bootstrap>:1165:_find_and_load | 11 | 1659 | 0.0132193 | 2.48894 |
| <frozen importlib._bootstrap>:1120:_find_and_load_unlocked | 11 | 1616 | 0.0083657 | 2.48865 |
| <frozen importlib._bootstrap>:666:_load_unlocked | 11 | 1567 | 0.0064376 | 2.48402 |
| <frozen importlib._bootstrap_external>:934:exec_module | 10 | 1325 | 0.0037211 | 2.48351 |
| <frozen importlib._bootstrap>:233:_call_with_frames_removed | 22 | 3790 | 0.0027132 | 2.48057 |
| D:\a\cursor-sandbox\cursor-sandbox\hgbdt_performance_analysis\benchmark_gbdt_regressors.py:444:main | 1 | 1 | 1.04e-05 | 2.43451 |
| D:\a\cursor-sandbox\cursor-sandbox\hgbdt_performance_analysis\benchmark_gbdt_regressors.py:402:_emit_single | 1 | 1 | 0.0005061 | 2.43192 |
| D:\a\cursor-sandbox\cursor-sandbox\hgbdt_performance_analysis\benchmark_gbdt_regressors.py:199:_single_run | 1 | 1 | 0.0003008 | 2.43133 |
| D:\a\_temp\setup-uv-cache\archive-v0\SypOPbL1BIi3nX8Q\Lib\site-packages\sklearn\base.py:1319:wrapper | 1 | 1 | 0.000585 | 2.2705 |
| D:\a\_temp\setup-uv-cache\archive-v0\SypOPbL1BIi3nX8Q\Lib\site-packages\sklearn\ensemble\_hist_gradient_boosting\gradient_boosting.py:512:fit | 1 | 1 | 0.0764282 | 2.26924 |

