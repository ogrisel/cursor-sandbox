# Profiling snapshots

## sklearn_hgb
### Python-level (cProfile) top cumulative entries
| function | primitive_calls | total_calls | total_time_s | cumulative_time_s |
| --- | --- | --- | --- | --- |
| ~:0:<built-in method builtins.exec> | 1 | 1665 | 0.0416524 | 5.49944 |
| D:\a\cursor-sandbox\cursor-sandbox\hgbdt_performance_analysis\benchmark_gbdt_regressors.py:1:<module> | 1 | 1 | 9.19e-05 | 5.4994 |
| D:\a\cursor-sandbox\cursor-sandbox\hgbdt_performance_analysis\benchmark_gbdt_regressors.py:450:main | 1 | 1 | 1.09e-05 | 2.93868 |
| D:\a\cursor-sandbox\cursor-sandbox\hgbdt_performance_analysis\benchmark_gbdt_regressors.py:408:_emit_single | 1 | 1 | 0.0005235 | 2.9358 |
| D:\a\cursor-sandbox\cursor-sandbox\hgbdt_performance_analysis\benchmark_gbdt_regressors.py:199:_single_run | 1 | 1 | 0.0003402 | 2.93519 |
| <frozen importlib._bootstrap>:1165:_find_and_load | 11 | 1659 | 0.0137533 | 2.55916 |
| <frozen importlib._bootstrap>:1120:_find_and_load_unlocked | 11 | 1616 | 0.0085619 | 2.55886 |
| <frozen importlib._bootstrap>:666:_load_unlocked | 11 | 1567 | 0.0068528 | 2.55374 |
| <frozen importlib._bootstrap_external>:934:exec_module | 10 | 1325 | 0.0041582 | 2.5532 |
| <frozen importlib._bootstrap>:233:_call_with_frames_removed | 22 | 3790 | 0.0025603 | 2.5501 |
| D:\a\_temp\setup-uv-cache\archive-v0\8Ekvtja0k40DJDvI\Lib\site-packages\sklearn\base.py:1319:wrapper | 1 | 1 | 0.0005143 | 2.29228 |
| D:\a\_temp\setup-uv-cache\archive-v0\8Ekvtja0k40DJDvI\Lib\site-packages\sklearn\ensemble\_hist_gradient_boosting\gradient_boosting.py:512:fit | 1 | 1 | 0.0937544 | 2.29082 |

