# Profiling snapshots

## sklearn_hgb
### Python-level (cProfile) top cumulative entries
| function | primitive_calls | total_calls | total_time_s | cumulative_time_s |
| --- | --- | --- | --- | --- |
| ~:0:<built-in method builtins.exec> | 1 | 1382 | 0.0376943 | 5.9206 |
| D:\a\cursor-sandbox\cursor-sandbox\hgbdt_performance_analysis\benchmark_gbdt_regressors.py:1:<module> | 1 | 1 | 8.14e-05 | 5.92059 |
| D:\a\cursor-sandbox\cursor-sandbox\hgbdt_performance_analysis\benchmark_gbdt_regressors.py:418:main | 1 | 1 | 8.6e-06 | 3.67213 |
| D:\a\cursor-sandbox\cursor-sandbox\hgbdt_performance_analysis\benchmark_gbdt_regressors.py:374:_emit_single | 1 | 1 | 0.0010844 | 3.66932 |
| D:\a\cursor-sandbox\cursor-sandbox\hgbdt_performance_analysis\benchmark_gbdt_regressors.py:168:_single_run | 1 | 1 | 0.0008297 | 3.66816 |
| D:\a\_temp\setup-uv-cache\archive-v0\d_QDoaatFVx0YDYI\Lib\site-packages\sklearn\base.py:1319:wrapper | 1 | 1 | 0.0012623 | 3.37063 |
| D:\a\_temp\setup-uv-cache\archive-v0\d_QDoaatFVx0YDYI\Lib\site-packages\sklearn\ensemble\_hist_gradient_boosting\gradient_boosting.py:512:fit | 1 | 1 | 0.150364 | 3.36865 |
| D:\a\_temp\setup-uv-cache\archive-v0\d_QDoaatFVx0YDYI\Lib\site-packages\sklearn\ensemble\_hist_gradient_boosting\grower.py:385:grow | 220 | 220 | 0.0046459 | 2.54035 |
| D:\a\_temp\setup-uv-cache\archive-v0\d_QDoaatFVx0YDYI\Lib\site-packages\sklearn\ensemble\_hist_gradient_boosting\grower.py:488:split_next | 6600 | 6600 | 1.56768 | 2.53436 |
| <frozen importlib._bootstrap>:1165:_find_and_load | 14 | 1341 | 0.010414 | 2.24921 |
| <frozen importlib._bootstrap>:1120:_find_and_load_unlocked | 14 | 1299 | 0.0066713 | 2.24879 |
| <frozen importlib._bootstrap>:666:_load_unlocked | 14 | 1258 | 0.0050499 | 2.2435 |

## lightgbm_hist
### Python-level (cProfile) top cumulative entries
| function | primitive_calls | total_calls | total_time_s | cumulative_time_s |
| --- | --- | --- | --- | --- |
| ~:0:<built-in method builtins.exec> | 1 | 1380 | 0.0369705 | 4.7532 |
| D:\a\cursor-sandbox\cursor-sandbox\hgbdt_performance_analysis\benchmark_gbdt_regressors.py:1:<module> | 1 | 1 | 8.66e-05 | 4.75317 |
| D:\a\cursor-sandbox\cursor-sandbox\hgbdt_performance_analysis\benchmark_gbdt_regressors.py:418:main | 1 | 1 | 8.8e-06 | 2.51069 |
| D:\a\cursor-sandbox\cursor-sandbox\hgbdt_performance_analysis\benchmark_gbdt_regressors.py:374:_emit_single | 1 | 1 | 0.0008146 | 2.50802 |
| D:\a\cursor-sandbox\cursor-sandbox\hgbdt_performance_analysis\benchmark_gbdt_regressors.py:168:_single_run | 1 | 1 | 0.0008283 | 2.50694 |
| D:\a\_temp\setup-uv-cache\archive-v0\d_QDoaatFVx0YDYI\Lib\site-packages\lightgbm\sklearn.py:1381:fit | 1 | 1 | 2e-05 | 2.28008 |
| D:\a\_temp\setup-uv-cache\archive-v0\d_QDoaatFVx0YDYI\Lib\site-packages\lightgbm\sklearn.py:907:fit | 1 | 1 | 9.06e-05 | 2.28006 |
| D:\a\_temp\setup-uv-cache\archive-v0\d_QDoaatFVx0YDYI\Lib\site-packages\lightgbm\engine.py:109:train | 1 | 1 | 0.0026002 | 2.27733 |
| <frozen importlib._bootstrap>:1165:_find_and_load | 13 | 1339 | 0.010446 | 2.24208 |
| <frozen importlib._bootstrap>:1120:_find_and_load_unlocked | 13 | 1297 | 0.0065724 | 2.24172 |
| <frozen importlib._bootstrap>:666:_load_unlocked | 13 | 1256 | 0.0050742 | 2.23663 |
| <frozen importlib._bootstrap_external>:934:exec_module | 12 | 1060 | 0.0030702 | 2.236 |

