# Profiling snapshots

## sklearn_hgb
### Python-level (cProfile) top cumulative entries
| function | primitive_calls | total_calls | total_time_s | cumulative_time_s |
| --- | --- | --- | --- | --- |
| ~:0:<built-in method builtins.exec> | 1 | 1386 | 0.0196154 | 3.36363 |
| /Users/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:1:<module> | 1 | 1 | 5.7792e-05 | 3.36359 |
| /Users/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:418:main | 1 | 1 | 9.541e-06 | 1.91411 |
| /Users/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:374:_emit_single | 1 | 1 | 0.000645334 | 1.91217 |
| /Users/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:168:_single_run | 1 | 1 | 0.000545293 | 1.91148 |
| /Users/runner/work/_temp/setup-uv-cache/archive-v0/c8I0ajD6kxAP2HbI/lib/python3.11/site-packages/sklearn/base.py:1319:wrapper | 1 | 1 | 0.000672792 | 1.69143 |
| /Users/runner/work/_temp/setup-uv-cache/archive-v0/c8I0ajD6kxAP2HbI/lib/python3.11/site-packages/sklearn/ensemble/_hist_gradient_boosting/gradient_boosting.py:512:fit | 1 | 1 | 0.0394006 | 1.69035 |
| <frozen importlib._bootstrap>:1165:_find_and_load | 13 | 1352 | 0.00409827 | 1.44963 |
| <frozen importlib._bootstrap>:1120:_find_and_load_unlocked | 13 | 1310 | 0.00343867 | 1.44942 |
| <frozen importlib._bootstrap>:666:_load_unlocked | 13 | 1266 | 0.0028038 | 1.44811 |
| <frozen importlib._bootstrap_external>:934:exec_module | 12 | 1066 | 0.00153915 | 1.44755 |
| <frozen importlib._bootstrap>:233:_call_with_frames_removed | 27 | 3105 | 0.000989379 | 1.446 |

## lightgbm_hist
### Python-level (cProfile) top cumulative entries
| function | primitive_calls | total_calls | total_time_s | cumulative_time_s |
| --- | --- | --- | --- | --- |
| ~:0:<built-in method builtins.exec> | 1 | 1384 | 0.0199725 | 3.40467 |
| /Users/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:1:<module> | 1 | 1 | 4.1708e-05 | 3.40462 |
| /Users/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:418:main | 1 | 1 | 5.875e-06 | 2.07791 |
| /Users/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:374:_emit_single | 1 | 1 | 0.00126492 | 2.07616 |
| /Users/runner/work/cursor-sandbox/cursor-sandbox/hgbdt_performance_analysis/benchmark_gbdt_regressors.py:168:_single_run | 1 | 1 | 0.000601164 | 2.07477 |
| /Users/runner/work/_temp/setup-uv-cache/archive-v0/c8I0ajD6kxAP2HbI/lib/python3.11/site-packages/lightgbm/sklearn.py:1381:fit | 1 | 1 | 1.275e-05 | 1.90673 |
| /Users/runner/work/_temp/setup-uv-cache/archive-v0/c8I0ajD6kxAP2HbI/lib/python3.11/site-packages/lightgbm/sklearn.py:907:fit | 1 | 1 | 6.825e-05 | 1.90672 |
| /Users/runner/work/_temp/setup-uv-cache/archive-v0/c8I0ajD6kxAP2HbI/lib/python3.11/site-packages/lightgbm/engine.py:109:train | 1 | 1 | 0.00231242 | 1.90537 |
| /Users/runner/work/_temp/setup-uv-cache/archive-v0/c8I0ajD6kxAP2HbI/lib/python3.11/site-packages/lightgbm/basic.py:4092:update | 220 | 220 | 1.72436 | 1.72489 |
| <frozen importlib._bootstrap>:1165:_find_and_load | 12 | 1350 | 0.00460217 | 1.32598 |
| <frozen importlib._bootstrap>:1120:_find_and_load_unlocked | 12 | 1308 | 0.00340109 | 1.32584 |
| <frozen importlib._bootstrap>:666:_load_unlocked | 12 | 1264 | 0.00276108 | 1.32475 |

