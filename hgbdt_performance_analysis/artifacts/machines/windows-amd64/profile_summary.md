# Profiling snapshots

## sklearn_hgb
### Python-level (cProfile) top cumulative entries
| function | primitive_calls | total_calls | total_time_s | cumulative_time_s |
| --- | --- | --- | --- | --- |
| ~:0:<built-in method builtins.exec> | 1 | 1382 | 0.0380557 | 6.19001 |
| D:\a\cursor-sandbox\cursor-sandbox\hgbdt_performance_analysis\benchmark_gbdt_regressors.py:1:<module> | 1 | 1 | 0.0001023 | 6.18998 |
| D:\a\cursor-sandbox\cursor-sandbox\hgbdt_performance_analysis\benchmark_gbdt_regressors.py:418:main | 1 | 1 | 1.02e-05 | 3.87204 |
| D:\a\cursor-sandbox\cursor-sandbox\hgbdt_performance_analysis\benchmark_gbdt_regressors.py:374:_emit_single | 1 | 1 | 0.0012036 | 3.86925 |
| D:\a\cursor-sandbox\cursor-sandbox\hgbdt_performance_analysis\benchmark_gbdt_regressors.py:168:_single_run | 1 | 1 | 0.000859 | 3.86795 |
| D:\a\_temp\setup-uv-cache\archive-v0\9srrFDN-ct8RDTfk\Lib\site-packages\sklearn\base.py:1319:wrapper | 1 | 1 | 0.0013955 | 3.556 |
| D:\a\_temp\setup-uv-cache\archive-v0\9srrFDN-ct8RDTfk\Lib\site-packages\sklearn\ensemble\_hist_gradient_boosting\gradient_boosting.py:512:fit | 1 | 1 | 0.177496 | 3.55387 |
| D:\a\_temp\setup-uv-cache\archive-v0\9srrFDN-ct8RDTfk\Lib\site-packages\sklearn\ensemble\_hist_gradient_boosting\grower.py:385:grow | 220 | 220 | 0.004882 | 2.69442 |
| D:\a\_temp\setup-uv-cache\archive-v0\9srrFDN-ct8RDTfk\Lib\site-packages\sklearn\ensemble\_hist_gradient_boosting\grower.py:488:split_next | 6600 | 6600 | 1.65959 | 2.6879 |
| <frozen importlib._bootstrap>:1165:_find_and_load | 14 | 1341 | 0.0112369 | 2.3186 |
| <frozen importlib._bootstrap>:1120:_find_and_load_unlocked | 14 | 1299 | 0.0068937 | 2.31812 |
| <frozen importlib._bootstrap>:666:_load_unlocked | 14 | 1258 | 0.0053123 | 2.31262 |

## lightgbm_hist
### Python-level (cProfile) top cumulative entries
| function | primitive_calls | total_calls | total_time_s | cumulative_time_s |
| --- | --- | --- | --- | --- |
| ~:0:<built-in method builtins.exec> | 1 | 1380 | 0.0382209 | 4.97543 |
| D:\a\cursor-sandbox\cursor-sandbox\hgbdt_performance_analysis\benchmark_gbdt_regressors.py:1:<module> | 1 | 1 | 8.49e-05 | 4.9754 |
| D:\a\cursor-sandbox\cursor-sandbox\hgbdt_performance_analysis\benchmark_gbdt_regressors.py:418:main | 1 | 1 | 1.17e-05 | 2.67293 |
| D:\a\cursor-sandbox\cursor-sandbox\hgbdt_performance_analysis\benchmark_gbdt_regressors.py:374:_emit_single | 1 | 1 | 0.0008532 | 2.66717 |
| D:\a\cursor-sandbox\cursor-sandbox\hgbdt_performance_analysis\benchmark_gbdt_regressors.py:168:_single_run | 1 | 1 | 0.0008559 | 2.66593 |
| D:\a\_temp\setup-uv-cache\archive-v0\9srrFDN-ct8RDTfk\Lib\site-packages\lightgbm\sklearn.py:1381:fit | 1 | 1 | 2.07e-05 | 2.42208 |
| D:\a\_temp\setup-uv-cache\archive-v0\9srrFDN-ct8RDTfk\Lib\site-packages\lightgbm\sklearn.py:907:fit | 1 | 1 | 9.42e-05 | 2.42206 |
| D:\a\_temp\setup-uv-cache\archive-v0\9srrFDN-ct8RDTfk\Lib\site-packages\lightgbm\engine.py:109:train | 1 | 1 | 0.0035168 | 2.41931 |
| <frozen importlib._bootstrap>:1165:_find_and_load | 13 | 1339 | 0.0110803 | 2.30206 |
| <frozen importlib._bootstrap>:1120:_find_and_load_unlocked | 13 | 1297 | 0.0094309 | 2.30168 |
| <frozen importlib._bootstrap>:666:_load_unlocked | 13 | 1256 | 0.0051775 | 2.29656 |
| <frozen importlib._bootstrap_external>:934:exec_module | 12 | 1060 | 0.0031293 | 2.29593 |

