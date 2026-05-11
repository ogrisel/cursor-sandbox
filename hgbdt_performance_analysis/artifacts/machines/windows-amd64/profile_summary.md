# Profiling snapshots

## sklearn_hgb
### Python-level (cProfile) top cumulative entries
| function | primitive_calls | total_calls | total_time_s | cumulative_time_s |
| --- | --- | --- | --- | --- |
| ~:0:<built-in method builtins.exec> | 1 | 1667 | 0.0413557 | 5.8303 |
| D:\a\cursor-sandbox\cursor-sandbox\hgbdt_performance_analysis\benchmark_gbdt_regressors.py:1:<module> | 1 | 1 | 7.5e-05 | 5.83027 |
| D:\a\cursor-sandbox\cursor-sandbox\hgbdt_performance_analysis\benchmark_gbdt_regressors.py:447:main | 1 | 1 | 1.01e-05 | 3.37573 |
| D:\a\cursor-sandbox\cursor-sandbox\hgbdt_performance_analysis\benchmark_gbdt_regressors.py:405:_emit_single | 1 | 1 | 0.0008814 | 3.37308 |
| D:\a\cursor-sandbox\cursor-sandbox\hgbdt_performance_analysis\benchmark_gbdt_regressors.py:195:_single_run | 1 | 1 | 0.0006441 | 3.37213 |
| D:\a\_temp\setup-uv-cache\archive-v0\bj2fNAOTfYnBM4kA\Lib\site-packages\sklearn\base.py:1319:wrapper | 1 | 1 | 0.001029 | 3.08245 |
| D:\a\_temp\setup-uv-cache\archive-v0\bj2fNAOTfYnBM4kA\Lib\site-packages\sklearn\ensemble\_hist_gradient_boosting\gradient_boosting.py:512:fit | 1 | 1 | 0.117027 | 3.0805 |
| <frozen importlib._bootstrap>:1165:_find_and_load | 12 | 1661 | 0.0126997 | 2.45437 |
| <frozen importlib._bootstrap>:1120:_find_and_load_unlocked | 12 | 1618 | 0.0084096 | 2.45405 |
| <frozen importlib._bootstrap>:666:_load_unlocked | 12 | 1569 | 0.0066271 | 2.44876 |
| <frozen importlib._bootstrap_external>:934:exec_module | 11 | 1327 | 0.0040898 | 2.44816 |
| <frozen importlib._bootstrap>:233:_call_with_frames_removed | 24 | 3794 | 0.0027371 | 2.44499 |

## lightgbm_hist
### Python-level (cProfile) top cumulative entries
| function | primitive_calls | total_calls | total_time_s | cumulative_time_s |
| --- | --- | --- | --- | --- |
| ~:0:<built-in method builtins.exec> | 1 | 1665 | 0.0409563 | 5.06124 |
| D:\a\cursor-sandbox\cursor-sandbox\hgbdt_performance_analysis\benchmark_gbdt_regressors.py:1:<module> | 1 | 1 | 7.29e-05 | 5.0612 |
| D:\a\cursor-sandbox\cursor-sandbox\hgbdt_performance_analysis\benchmark_gbdt_regressors.py:447:main | 1 | 1 | 1.04e-05 | 2.6079 |
| D:\a\cursor-sandbox\cursor-sandbox\hgbdt_performance_analysis\benchmark_gbdt_regressors.py:405:_emit_single | 1 | 1 | 0.0005589 | 2.60523 |
| D:\a\cursor-sandbox\cursor-sandbox\hgbdt_performance_analysis\benchmark_gbdt_regressors.py:195:_single_run | 1 | 1 | 0.0006449 | 2.60445 |
| <frozen importlib._bootstrap>:1165:_find_and_load | 11 | 1659 | 0.0128565 | 2.45191 |
| <frozen importlib._bootstrap>:1120:_find_and_load_unlocked | 11 | 1616 | 0.0085038 | 2.45163 |
| <frozen importlib._bootstrap>:666:_load_unlocked | 11 | 1567 | 0.0067369 | 2.44668 |
| <frozen importlib._bootstrap_external>:934:exec_module | 10 | 1325 | 0.0040958 | 2.44615 |
| <frozen importlib._bootstrap>:233:_call_with_frames_removed | 22 | 3790 | 0.0026443 | 2.44327 |
| ~:0:<built-in method builtins.__import__> | 67 | 779 | 0.0013723 | 2.19872 |
| D:\a\_temp\setup-uv-cache\archive-v0\bj2fNAOTfYnBM4kA\Lib\site-packages\lightgbm\sklearn.py:1381:fit | 1 | 1 | 2.12e-05 | 2.19483 |

