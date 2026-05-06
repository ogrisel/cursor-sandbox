# Profiling snapshots

## sklearn_hgb_aligned_t1
### Python-level (cProfile) top cumulative entries
| function | primitive_calls | total_calls | total_time_s | cumulative_time_s |
| --- | --- | --- | --- | --- |
| ~:0:<built-in method builtins.exec> | 1 | 1701 | 0.0309981 | 5.66437 |
| benchmark_gbdt_regressors.py:1:<module> | 1 | 1 | 4.0466e-05 | 5.66435 |
| benchmark_gbdt_regressors.py:369:main | 1 | 1 | 6.286e-06 | 4.19561 |
| benchmark_gbdt_regressors.py:331:_emit_single | 1 | 1 | 0.000502003 | 4.19325 |
| benchmark_gbdt_regressors.py:138:_single_run | 1 | 1 | 0.000351725 | 4.19268 |
| /usr/lib/python3.12/threading.py:1115:join | 1 | 1 | 8.002e-06 | 3.91872 |
| /usr/lib/python3.12/threading.py:1153:_wait_for_tstate_lock | 1 | 1 | 1.4604e-05 | 3.91864 |
| ~:0:<method 'acquire' of '_thread.lock' objects> | 6 | 8 | 0.000171287 | 3.91863 |
| /usr/lib/python3.12/threading.py:1016:_bootstrap | 1 | 1 | 0.000182494 | 3.91846 |
| /usr/lib/python3.12/threading.py:1056:_bootstrap_inner | 1 | 1 | 1.3025e-05 | 3.91828 |
| /usr/lib/python3.12/threading.py:999:run | 1 | 1 | 4.9345e-05 | 3.91826 |
| /root/.local/lib/python3.12/site-packages/sklearn/base.py:1319:wrapper | 1 | 1 | 0.000386397 | 3.68768 |
| /root/.local/lib/python3.12/site-packages/psutil/_common.py:367:wrapper | 387 | 387 | 0.037286 | 2.22204 |
| /root/.local/lib/python3.12/site-packages/sklearn/ensemble/_hist_gradient_boosting/grower.py:385:grow | 180 | 180 | 0.00228362 | 1.79229 |
| ~:0:<built-in method time.sleep> | 385 | 385 | 0.90782 | 1.77897 |

### Native/C/C++/Cython-flavored stack leaf hotspots (py-spy --native)
| leaf_frame | sample_weight |
| --- | --- |
| histogram__build_histogram_no_hessian.isra.0 | 1.78 |
| histogram__build_histogram_root_no_hessian.isra.0 | 1.18 |
| _binning__map_col_to_bins._omp_fn.0 | 0.68 |
| clock_nanosleep | 0.38 |
| split_indices._omp_fn.0 | 0.3 |
| Splitter__find_best_bin_to_split_left_to_right | 0.25 |
| _predictor__predict_from_raw_data._omp_fn.0 | 0.23 |
| 0x7fc9241a21ca | 0.14 |
| DOUBLE_isnan | 0.09 |
| _compile_bytecode | 0.08 |
| dedent | 0.07 |
| _aligned_strided_to_contig_size8 | 0.07 |
| brk | 0.06 |
| _mt19937_mt19937_double | 0.06 |
| legacy_gauss.part.0 | 0.06 |

## sklearn_hgb_aligned_t4
### Python-level (cProfile) top cumulative entries
| function | primitive_calls | total_calls | total_time_s | cumulative_time_s |
| --- | --- | --- | --- | --- |
| ~:0:<built-in method builtins.exec> | 1 | 1703 | 0.0305069 | 3.13273 |
| benchmark_gbdt_regressors.py:1:<module> | 1 | 1 | 4.7034e-05 | 3.13271 |
| benchmark_gbdt_regressors.py:369:main | 1 | 1 | 7.958e-06 | 1.65769 |
| benchmark_gbdt_regressors.py:331:_emit_single | 1 | 1 | 0.00077413 | 1.65473 |
| benchmark_gbdt_regressors.py:138:_single_run | 1 | 1 | 0.000494289 | 1.65387 |
| ~:0:<method 'acquire' of '_thread.lock' objects> | 282 | 302 | 0.000597554 | 1.54256 |
| /usr/lib/python3.12/threading.py:1115:join | 4 | 4 | 6.467e-05 | 1.54241 |
| /usr/lib/python3.12/threading.py:1153:_wait_for_tstate_lock | 13 | 13 | 2.7943e-05 | 1.54219 |
| <frozen importlib._bootstrap>:1349:_find_and_load | 12 | 1701 | 0.00686861 | 1.4747 |
| <frozen importlib._bootstrap>:1304:_find_and_load_unlocked | 12 | 1662 | 0.005657 | 1.47436 |
| <frozen importlib._bootstrap>:911:_load_unlocked | 12 | 1611 | 0.00436509 | 1.47289 |
| <frozen importlib._bootstrap_external>:989:exec_module | 11 | 1363 | 0.0026458 | 1.4725 |
| <frozen importlib._bootstrap>:480:_call_with_frames_removed | 24 | 3857 | 0.00296877 | 1.47054 |
| ~:0:<built-in method time.sleep> | 125 | 141 | 0.2451 | 1.46885 |
| /usr/lib/python3.12/threading.py:1016:_bootstrap | 1 | 8 | 0.000260346 | 1.35381 |

### Native/C/C++/Cython-flavored stack leaf hotspots (py-spy --native)
| leaf_frame | sample_weight |
| --- | --- |
| 0x7f867d698d71 | 1.54 |
| 0x7f867d698f70 | 0.68 |
| clock_nanosleep | 0.59 |
| histogram__build_histogram_no_hessian.isra.0 | 0.28 |
| _binning__map_col_to_bins._omp_fn.0 | 0.24 |
| 0x7f865da1e02a | 0.18 |
| introselect_<npy::double_tag, false, double> | 0.18 |
| histogram__build_histogram_root_no_hessian.isra.0 | 0.16 |
| _compile_bytecode | 0.15 |
| pthread_cond_signal | 0.15 |
| DOUBLE_isnan | 0.15 |
| _aligned_strided_to_contig_size8 | 0.14 |
| partition_unrolled<zmm_vector<double>, Comparator<zmm_vector<double>, false>, 8, double> | 0.13 |
| 0x7f867d62a1ca | 0.12 |
| dedent | 0.09 |

## lightgbm_hist_aligned_t1
### Python-level (cProfile) top cumulative entries
| function | primitive_calls | total_calls | total_time_s | cumulative_time_s |
| --- | --- | --- | --- | --- |
| ~:0:<built-in method builtins.exec> | 1 | 1701 | 0.0301507 | 6.39949 |
| benchmark_gbdt_regressors.py:1:<module> | 1 | 1 | 5.1219e-05 | 6.39947 |
| ~:0:<built-in method time.sleep> | 460 | 460 | 3.66021 | 5.05485 |
| benchmark_gbdt_regressors.py:369:main | 1 | 1 | 6.088e-06 | 4.95255 |
| benchmark_gbdt_regressors.py:331:_emit_single | 1 | 1 | 0.000516665 | 4.95021 |
| benchmark_gbdt_regressors.py:138:_single_run | 1 | 1 | 0.000323494 | 4.94955 |
| /usr/lib/python3.12/threading.py:1115:join | 1 | 1 | 7.86e-06 | 4.67977 |
| ~:0:<method 'acquire' of '_thread.lock' objects> | 6 | 8 | 0.000210873 | 4.6797 |
| /usr/lib/python3.12/threading.py:1153:_wait_for_tstate_lock | 1 | 1 | 1.1597e-05 | 4.6797 |
| /usr/lib/python3.12/threading.py:1016:_bootstrap | 1 | 1 | 0.000166646 | 4.67949 |
| /usr/lib/python3.12/threading.py:1056:_bootstrap_inner | 1 | 1 | 1.1094e-05 | 4.67932 |
| /usr/lib/python3.12/threading.py:999:run | 1 | 1 | 6.0832e-05 | 4.67931 |
| /root/.local/lib/python3.12/site-packages/lightgbm/sklearn.py:1381:fit | 1 | 1 | 1.3812e-05 | 4.48654 |
| /root/.local/lib/python3.12/site-packages/lightgbm/sklearn.py:907:fit | 1 | 1 | 5.3992e-05 | 4.48653 |
| /root/.local/lib/python3.12/site-packages/lightgbm/engine.py:109:train | 1 | 1 | 0.00273467 | 4.48516 |

### Native/C/C++/Cython-flavored stack leaf hotspots (py-spy --native)
| leaf_frame | sample_weight |
| --- | --- |
| LightGBM::DenseBin<unsigned char, false>::ConstructHistogram | 3.3 |
| clock_nanosleep | 0.77 |
| LGBM_DatasetCreateFromMats._omp_fn.0 | 0.74 |
| std::__merge_sort_loop<double*, double*, long, __gnu_cxx::__ops::_Iter_less_iter> | 0.47 |
| LightGBM::DenseBin<unsigned char, false>::Split | 0.32 |
| std::_Function_handler<void (double, double, int, LightGBM::FeatureConstraint const*, double, LightGBM::SplitInfo*), LightGBM::FeatureHistogram::FuncForNumricalL3<false, false, false, false, false>()::{lambda(double, double, int, LightGBM::FeatureConstraint const*, double, LightGBM::SplitInfo*)#7}>::_M_invoke | 0.3 |
| LightGBM::GBDT::PredictRaw | 0.24 |
| _aligned_strided_to_contig_size8 | 0.16 |
| 0x7f3e6306a1ca | 0.14 |
| _compile_bytecode | 0.12 |
| legacy_gauss.part.0 | 0.11 |
| LGBM_DatasetCreateFromMats | 0.11 |
| std::vector<int, std::allocator<int> >::emplace_back<int> | 0.11 |
| docformat | 0.07 |
| __init__ | 0.06 |

## lightgbm_hist_aligned_t4
### Python-level (cProfile) top cumulative entries
| function | primitive_calls | total_calls | total_time_s | cumulative_time_s |
| --- | --- | --- | --- | --- |
| ~:0:<built-in method builtins.exec> | 1 | 1701 | 0.0304646 | 3.2374 |
| benchmark_gbdt_regressors.py:1:<module> | 1 | 1 | 5.0153e-05 | 3.23737 |
| benchmark_gbdt_regressors.py:369:main | 1 | 1 | 7.595e-06 | 1.77884 |
| benchmark_gbdt_regressors.py:331:_emit_single | 1 | 1 | 0.000653559 | 1.77647 |
| benchmark_gbdt_regressors.py:138:_single_run | 1 | 1 | 0.000283535 | 1.77563 |
| /usr/lib/python3.12/threading.py:1115:join | 1 | 1 | 7.561e-06 | 1.5009 |
| /usr/lib/python3.12/threading.py:1153:_wait_for_tstate_lock | 1 | 1 | 1.064e-05 | 1.50082 |
| ~:0:<method 'acquire' of '_thread.lock' objects> | 6 | 8 | 0.000154183 | 1.50082 |
| /usr/lib/python3.12/threading.py:1016:_bootstrap | 1 | 1 | 0.000173617 | 1.50067 |
| /usr/lib/python3.12/threading.py:1056:_bootstrap_inner | 1 | 1 | 1.3718e-05 | 1.50049 |
| /usr/lib/python3.12/threading.py:999:run | 1 | 1 | 5.5405e-05 | 1.50047 |
| <frozen importlib._bootstrap>:1349:_find_and_load | 11 | 1699 | 0.00679632 | 1.4577 |
| <frozen importlib._bootstrap>:1304:_find_and_load_unlocked | 11 | 1660 | 0.00550254 | 1.45741 |
| <frozen importlib._bootstrap>:911:_load_unlocked | 11 | 1609 | 0.00431031 | 1.45644 |
| <frozen importlib._bootstrap_external>:989:exec_module | 10 | 1361 | 0.00272441 | 1.45617 |

### Native/C/C++/Cython-flavored stack leaf hotspots (py-spy --native)
| leaf_frame | sample_weight |
| --- | --- |
| LightGBM::DenseBin<unsigned char, false>::ConstructHistogram | 0.55 |
| std::__merge_sort_loop<double*, double*, long, __gnu_cxx::__ops::_Iter_less_iter> | 0.27 |
| 0x7f077c2cf8a2 | 0.26 |
| clock_nanosleep | 0.23 |
| _compile_bytecode | 0.16 |
| LightGBM::GBDT::PredictRaw | 0.13 |
| LGBM_DatasetCreateFromMats._omp_fn.0 | 0.12 |
| 0x7f077f5ff1ca | 0.12 |
| std::vector<int, std::allocator<int> >::emplace_back<int> | 0.11 |
| _aligned_strided_to_contig_size8 | 0.1 |
| <module> | 0.07 |
| dedent | 0.07 |
| 0x7f077c2cf8af | 0.07 |
| legacy_gauss.part.0 | 0.06 |
| 0x7f077f7766d2 | 0.06 |

