# Profiling snapshots

## sklearn_hgb
### Python-level (cProfile) top cumulative entries
| function | primitive_calls | total_calls | total_time_s | cumulative_time_s |
| --- | --- | --- | --- | --- |
| ~:0:<built-in method builtins.exec> | 1 | 1667 | 0.0421234 | 6.05654 |
| D:\a\cursor-sandbox\cursor-sandbox\hgbdt_performance_analysis\benchmark_gbdt_regressors.py:1:<module> | 1 | 1 | 8.78e-05 | 6.05648 |
| D:\a\cursor-sandbox\cursor-sandbox\hgbdt_performance_analysis\benchmark_gbdt_regressors.py:447:main | 1 | 1 | 1.11e-05 | 3.55189 |
| D:\a\cursor-sandbox\cursor-sandbox\hgbdt_performance_analysis\benchmark_gbdt_regressors.py:405:_emit_single | 1 | 1 | 0.0014648 | 3.54901 |
| D:\a\cursor-sandbox\cursor-sandbox\hgbdt_performance_analysis\benchmark_gbdt_regressors.py:195:_single_run | 1 | 1 | 0.0007601 | 3.54744 |
| D:\a\_temp\setup-uv-cache\archive-v0\yl6BH6003gZc31wu\Lib\site-packages\sklearn\base.py:1319:wrapper | 1 | 1 | 0.0018304 | 3.22014 |
| D:\a\_temp\setup-uv-cache\archive-v0\yl6BH6003gZc31wu\Lib\site-packages\sklearn\ensemble\_hist_gradient_boosting\gradient_boosting.py:512:fit | 1 | 1 | 0.169207 | 3.2175 |
| <frozen importlib._bootstrap>:1165:_find_and_load | 12 | 1661 | 0.0127053 | 2.5043 |
| <frozen importlib._bootstrap>:1120:_find_and_load_unlocked | 12 | 1618 | 0.0084343 | 2.50397 |
| <frozen importlib._bootstrap>:666:_load_unlocked | 12 | 1569 | 0.0064324 | 2.49904 |
| <frozen importlib._bootstrap_external>:934:exec_module | 11 | 1327 | 0.0038345 | 2.49845 |
| <frozen importlib._bootstrap>:233:_call_with_frames_removed | 24 | 3794 | 0.0024907 | 2.49523 |

## lightgbm_hist
### Python-level (cProfile) top cumulative entries
| function | primitive_calls | total_calls | total_time_s | cumulative_time_s |
| --- | --- | --- | --- | --- |
| ~:0:<built-in method builtins.exec> | 1 | 1665 | 0.0420424 | 5.38341 |
| D:\a\cursor-sandbox\cursor-sandbox\hgbdt_performance_analysis\benchmark_gbdt_regressors.py:1:<module> | 1 | 1 | 8.29e-05 | 5.38336 |
| D:\a\cursor-sandbox\cursor-sandbox\hgbdt_performance_analysis\benchmark_gbdt_regressors.py:447:main | 1 | 1 | 1.15e-05 | 2.87653 |
| D:\a\cursor-sandbox\cursor-sandbox\hgbdt_performance_analysis\benchmark_gbdt_regressors.py:405:_emit_single | 1 | 1 | 0.0006683 | 2.87393 |
| D:\a\cursor-sandbox\cursor-sandbox\hgbdt_performance_analysis\benchmark_gbdt_regressors.py:195:_single_run | 1 | 1 | 0.0007907 | 2.87281 |
| <frozen importlib._bootstrap>:1165:_find_and_load | 11 | 1659 | 0.0126353 | 2.50533 |
| <frozen importlib._bootstrap>:1120:_find_and_load_unlocked | 11 | 1616 | 0.0083349 | 2.50504 |
| <frozen importlib._bootstrap>:666:_load_unlocked | 11 | 1567 | 0.0064572 | 2.50043 |
| <frozen importlib._bootstrap_external>:934:exec_module | 10 | 1325 | 0.0038584 | 2.49991 |
| <frozen importlib._bootstrap>:233:_call_with_frames_removed | 22 | 3790 | 0.0025163 | 2.49683 |
| D:\a\_temp\setup-uv-cache\archive-v0\yl6BH6003gZc31wu\Lib\site-packages\lightgbm\sklearn.py:1381:fit | 1 | 1 | 2.45e-05 | 2.43191 |
| D:\a\_temp\setup-uv-cache\archive-v0\yl6BH6003gZc31wu\Lib\site-packages\lightgbm\sklearn.py:907:fit | 1 | 1 | 9.94e-05 | 2.43188 |

