# Profiling snapshots

## sklearn_hgb
### Python-level (cProfile) top cumulative entries
| function | primitive_calls | total_calls | total_time_s | cumulative_time_s |
| --- | --- | --- | --- | --- |
| ~:0:<built-in method builtins.exec> | 1 | 1665 | 0.0423307 | 4.89642 |
| D:\a\cursor-sandbox\cursor-sandbox\hgbdt_performance_analysis\benchmark_gbdt_regressors.py:1:<module> | 1 | 1 | 8.65e-05 | 4.89638 |
| <frozen importlib._bootstrap>:1165:_find_and_load | 11 | 1659 | 0.0126035 | 2.46347 |
| <frozen importlib._bootstrap>:1120:_find_and_load_unlocked | 11 | 1616 | 0.0082921 | 2.46317 |
| <frozen importlib._bootstrap>:666:_load_unlocked | 11 | 1567 | 0.0066444 | 2.45854 |
| <frozen importlib._bootstrap_external>:934:exec_module | 10 | 1325 | 0.0038678 | 2.45792 |
| <frozen importlib._bootstrap>:233:_call_with_frames_removed | 22 | 3790 | 0.0025838 | 2.45518 |
| D:\a\cursor-sandbox\cursor-sandbox\hgbdt_performance_analysis\benchmark_gbdt_regressors.py:496:main | 1 | 1 | 1.11e-05 | 2.43146 |
| D:\a\cursor-sandbox\cursor-sandbox\hgbdt_performance_analysis\benchmark_gbdt_regressors.py:452:_emit_single | 1 | 1 | 0.0005644 | 2.42877 |
| D:\a\cursor-sandbox\cursor-sandbox\hgbdt_performance_analysis\benchmark_gbdt_regressors.py:209:_single_run | 1 | 1 | 0.0003104 | 2.42811 |
| D:\a\_temp\setup-uv-cache\archive-v0\djBQVQiU7HQmT2ZA\Lib\site-packages\sklearn\base.py:1319:wrapper | 1 | 1 | 0.000511 | 2.25115 |
| D:\a\_temp\setup-uv-cache\archive-v0\djBQVQiU7HQmT2ZA\Lib\site-packages\sklearn\ensemble\_hist_gradient_boosting\gradient_boosting.py:512:fit | 1 | 1 | 0.0609641 | 2.24968 |

