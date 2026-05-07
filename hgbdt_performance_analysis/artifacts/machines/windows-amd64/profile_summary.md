# Profiling snapshots

## sklearn_hgb
### Python-level (cProfile) top cumulative entries
| function | primitive_calls | total_calls | total_time_s | cumulative_time_s |
| --- | --- | --- | --- | --- |
| ~:0:<built-in method builtins.exec> | 1 | 1667 | 0.0406169 | 5.76742 |
| D:\a\cursor-sandbox\cursor-sandbox\hgbdt_performance_analysis\benchmark_gbdt_regressors.py:1:<module> | 1 | 1 | 7.47e-05 | 5.76737 |
| D:\a\cursor-sandbox\cursor-sandbox\hgbdt_performance_analysis\benchmark_gbdt_regressors.py:447:main | 1 | 1 | 1.02e-05 | 3.30237 |
| D:\a\cursor-sandbox\cursor-sandbox\hgbdt_performance_analysis\benchmark_gbdt_regressors.py:405:_emit_single | 1 | 1 | 0.0011563 | 3.29958 |
| D:\a\cursor-sandbox\cursor-sandbox\hgbdt_performance_analysis\benchmark_gbdt_regressors.py:195:_single_run | 1 | 1 | 0.0006542 | 3.29835 |
| D:\a\_temp\setup-uv-cache\archive-v0\s-6Qj9V_YFmnwZZM\Lib\site-packages\sklearn\base.py:1319:wrapper | 1 | 1 | 0.0009402 | 3.00352 |
| D:\a\_temp\setup-uv-cache\archive-v0\s-6Qj9V_YFmnwZZM\Lib\site-packages\sklearn\ensemble\_hist_gradient_boosting\gradient_boosting.py:512:fit | 1 | 1 | 0.1184 | 3.00189 |
| <frozen importlib._bootstrap>:1165:_find_and_load | 12 | 1661 | 0.012949 | 2.46486 |
| <frozen importlib._bootstrap>:1120:_find_and_load_unlocked | 12 | 1618 | 0.0085585 | 2.46453 |
| <frozen importlib._bootstrap>:666:_load_unlocked | 12 | 1569 | 0.0067674 | 2.45924 |
| <frozen importlib._bootstrap_external>:934:exec_module | 11 | 1327 | 0.0039975 | 2.45865 |
| <frozen importlib._bootstrap>:233:_call_with_frames_removed | 24 | 3794 | 0.0026837 | 2.45559 |

## lightgbm_hist
### Python-level (cProfile) top cumulative entries
| function | primitive_calls | total_calls | total_time_s | cumulative_time_s |
| --- | --- | --- | --- | --- |
| ~:0:<built-in method builtins.exec> | 1 | 1665 | 0.0411411 | 5.24117 |
| D:\a\cursor-sandbox\cursor-sandbox\hgbdt_performance_analysis\benchmark_gbdt_regressors.py:1:<module> | 1 | 1 | 7.32e-05 | 5.24115 |
| D:\a\cursor-sandbox\cursor-sandbox\hgbdt_performance_analysis\benchmark_gbdt_regressors.py:447:main | 1 | 1 | 9.8e-06 | 2.75339 |
| D:\a\cursor-sandbox\cursor-sandbox\hgbdt_performance_analysis\benchmark_gbdt_regressors.py:405:_emit_single | 1 | 1 | 0.0006175 | 2.7507 |
| D:\a\cursor-sandbox\cursor-sandbox\hgbdt_performance_analysis\benchmark_gbdt_regressors.py:195:_single_run | 1 | 1 | 0.0006649 | 2.7498 |
| <frozen importlib._bootstrap>:1165:_find_and_load | 11 | 1659 | 0.0127428 | 2.48638 |
| <frozen importlib._bootstrap>:1120:_find_and_load_unlocked | 11 | 1616 | 0.0085042 | 2.48609 |
| <frozen importlib._bootstrap>:666:_load_unlocked | 11 | 1567 | 0.0066696 | 2.48118 |
| <frozen importlib._bootstrap_external>:934:exec_module | 10 | 1325 | 0.0040613 | 2.48065 |
| <frozen importlib._bootstrap>:233:_call_with_frames_removed | 22 | 3790 | 0.0026154 | 2.47765 |
| D:\a\_temp\setup-uv-cache\archive-v0\s-6Qj9V_YFmnwZZM\Lib\site-packages\lightgbm\sklearn.py:1381:fit | 1 | 1 | 1.94e-05 | 2.31811 |
| D:\a\_temp\setup-uv-cache\archive-v0\s-6Qj9V_YFmnwZZM\Lib\site-packages\lightgbm\sklearn.py:907:fit | 1 | 1 | 9.29e-05 | 2.31809 |

