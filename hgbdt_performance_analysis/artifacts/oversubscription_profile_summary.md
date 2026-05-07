# Profiling snapshots

## sklearn_t4
### Python-level (cProfile) top cumulative entries
| function | primitive_calls | total_calls | total_time_s | cumulative_time_s |
| --- | --- | --- | --- | --- |
| ~:0:<built-in method builtins.exec> | 1 | 1764 | 0.0316611 | 4.29321 |
| benchmark_gbdt_regressors.py:1:<module> | 1 | 1 | 4.397e-05 | 4.29317 |
| benchmark_gbdt_regressors.py:369:main | 1 | 1 | 8.408e-06 | 2.72976 |
| benchmark_gbdt_regressors.py:331:_emit_single | 1 | 1 | 0.00129602 | 2.72739 |
| benchmark_gbdt_regressors.py:138:_single_run | 1 | 1 | 0.000500601 | 2.726 |
| ~:0:<built-in method time.sleep> | 205 | 233 | 0.544151 | 2.66811 |
| ~:0:<method 'acquire' of '_thread.lock' objects> | 402 | 422 | 0.000663059 | 2.37754 |
| /usr/lib/python3.12/threading.py:1115:join | 4 | 4 | 2.4127e-05 | 2.37748 |
| /usr/lib/python3.12/threading.py:1153:_wait_for_tstate_lock | 13 | 13 | 4.1287e-05 | 2.37737 |
| /usr/lib/python3.12/threading.py:1016:_bootstrap | 1 | 8 | 0.000297016 | 2.22736 |
| /usr/lib/python3.12/threading.py:1056:_bootstrap_inner | 1 | 8 | 0.000555489 | 2.2271 |
| /usr/lib/python3.12/threading.py:999:run | 1 | 8 | 0.000115456 | 2.22707 |

### Native/C/C++/Cython-flavored stack leaf hotspots (py-spy --native)
| leaf_frame | sample_weight |
| --- | --- |
| 0x7febeef04d71 | 1.26 |
| histogram__build_histogram_no_hessian.isra.0 | 0.55 |
| 0x7febcf41e02a | 0.5 |
| clock_nanosleep | 0.45 |
| _binning__map_col_to_bins._omp_fn.0 | 0.29 |
| 0x7febeee961ca | 0.26 |
| introselect_<npy::double_tag, false, double> | 0.25 |
| 0x7febeef04f70 | 0.23 |
| _aligned_strided_to_contig_size8 | 0.19 |
| histogram__build_histogram_root_no_hessian.isra.0 | 0.19 |
| _compile_bytecode | 0.18 |
| DOUBLE_isnan | 0.17 |

## sklearn_t16
### Python-level (cProfile) top cumulative entries
| function | primitive_calls | total_calls | total_time_s | cumulative_time_s |
| --- | --- | --- | --- | --- |
| ~:0:<built-in method builtins.exec> | 1 | 1764 | 0.0312029 | 7.01666 |
| benchmark_gbdt_regressors.py:1:<module> | 1 | 1 | 4.3261e-05 | 7.01663 |
| benchmark_gbdt_regressors.py:369:main | 1 | 1 | 1.1253e-05 | 5.4343 |
| benchmark_gbdt_regressors.py:331:_emit_single | 1 | 1 | 0.000839198 | 5.43184 |
| benchmark_gbdt_regressors.py:138:_single_run | 1 | 1 | 0.000785384 | 5.43089 |
| ~:0:<method 'acquire' of '_thread.lock' objects> | 462 | 518 | 0.00122765 | 5.27648 |
| /usr/lib/python3.12/threading.py:1115:join | 4 | 4 | 5.7907e-05 | 5.27593 |
| /usr/lib/python3.12/threading.py:1153:_wait_for_tstate_lock | 37 | 37 | 7.6236e-05 | 5.27571 |
| /usr/lib/python3.12/threading.py:1016:_bootstrap | 1 | 20 | 0.0109926 | 4.86489 |
| /usr/lib/python3.12/threading.py:1056:_bootstrap_inner | 1 | 20 | 0.000246968 | 4.86471 |
| /usr/lib/python3.12/threading.py:999:run | 1 | 20 | 0.000234252 | 4.86469 |
| /root/.local/lib/python3.12/site-packages/sklearn/base.py:1319:wrapper | 1 | 1 | 0.00111066 | 4.69772 |

### Native/C/C++/Cython-flavored stack leaf hotspots (py-spy --native)
| leaf_frame | sample_weight |
| --- | --- |
| 0x7f5274de2d71 | 3.54 |
| 0x7f5274de2f70 | 1.7 |
| 0x7f525521e073 | 1.34 |
| clock_nanosleep | 0.37 |
| pthread_cond_signal | 0.27 |
| 0x7f5274de5440 | 0.24 |
| introselect_<npy::double_tag, false, double> | 0.22 |
| legacy_gauss.part.0 | 0.17 |
| _binning__map_col_to_bins._omp_fn.0 | 0.16 |
| _aligned_contig_cast_float_to_double | 0.14 |
| histogram__build_histogram_no_hessian.isra.0 | 0.14 |
| dedent | 0.13 |

## xgb_t4
### Python-level (cProfile) top cumulative entries
| function | primitive_calls | total_calls | total_time_s | cumulative_time_s |
| --- | --- | --- | --- | --- |
| ~:0:<built-in method builtins.exec> | 1 | 1762 | 0.0313371 | 4.6558 |
| benchmark_gbdt_regressors.py:1:<module> | 1 | 1 | 5.4126e-05 | 4.65566 |
| benchmark_gbdt_regressors.py:369:main | 1 | 1 | 1.5444e-05 | 3.07893 |
| benchmark_gbdt_regressors.py:331:_emit_single | 1 | 1 | 0.000871403 | 3.07561 |
| benchmark_gbdt_regressors.py:138:_single_run | 1 | 1 | 0.000644683 | 3.07444 |
| /usr/lib/python3.12/threading.py:1115:join | 1 | 1 | 1.6652e-05 | 2.53138 |
| /usr/lib/python3.12/threading.py:1153:_wait_for_tstate_lock | 1 | 1 | 2.6138e-05 | 2.53128 |
| ~:0:<method 'acquire' of '_thread.lock' objects> | 6 | 8 | 0.00019675 | 2.53124 |
| /usr/lib/python3.12/threading.py:1016:_bootstrap | 1 | 1 | 0.000260057 | 2.53104 |
| /usr/lib/python3.12/threading.py:1056:_bootstrap_inner | 1 | 1 | 2.3695e-05 | 2.53078 |
| /usr/lib/python3.12/threading.py:999:run | 1 | 1 | 0.000113921 | 2.53074 |
| /root/.local/lib/python3.12/site-packages/xgboost/core.py:732:inner_f | 3 | 15 | 0.00023905 | 2.50803 |

### Native/C/C++/Cython-flavored stack leaf hotspots (py-spy --native)
| leaf_frame | sample_weight |
| --- | --- |
| xgboost::common::RowsWiseBuildHistKernel<false, xgboost::common::GHistBuildingManager<false, true, false, unsigned char> > | 0.7 |
| xgboost::common::GHistBuildingManager<false, true, false, unsigned char>::DispatchAndExecute<xgboost::common::BuildHist<false>(xgboost::common::Span<xgboost::detail::GradientPairInternal<float> const, (unsigned long)18446744073709551615>, xgboost::common::Span<unsigned long const, (unsigned long)18446744073709551615>, xgboost::GHistIndexMatrix const&, xgboost::common::Span<xgboost::detail::GradientPairInternal<double>, (unsigned long)18446744073709551615>, bool)::{lambda(auto:1)#1}> | 0.51 |
| 0x7fc4b861e02a | 0.27 |
| xgboost::common::ParallelFor<unsigned long, xgboost::data::cpu_impl::GetDataShape(xgboost::Context const*, xgboost::data::DMatrixProxy*, xgboost::data::DataIterProxy<void (void*), int (void*)>*, float, xgboost::data::ExternalDataInfo*)::{lambda()#1}::operator()() const::{lambda(auto:1 const&)#1}::operator()<xgboost::data::ArrayAdapterBatch>(xgboost::data::ArrayAdapterBatch const&) const::{lambda(auto:1)#1}> | 0.2 |
| xgboost::common::HistogramCuts::SearchBin | 0.2 |
| _aligned_strided_to_contig_size8 | 0.18 |
| _mt19937_mt19937_double | 0.17 |
| 0x7fc4d80c21ca | 0.17 |
| legacy_gauss.part.0 | 0.15 |
| std::__introsort_loop<__gnu_cxx::__normal_iterator<xgboost::common::WQSummary<float, float>::Queue::QEntry*, std::vector<xgboost::common::WQSummary<float, float>::Queue::QEntry, std::allocator<xgboost::common::WQSummary<float, float>::Queue::QEntry> > >, long, __gnu_cxx::__ops::_Iter_less_iter> | 0.15 |
| _compile_bytecode | 0.14 |
| clock_nanosleep | 0.12 |

## xgb_t16
### Python-level (cProfile) top cumulative entries
| function | primitive_calls | total_calls | total_time_s | cumulative_time_s |
| --- | --- | --- | --- | --- |
| ~:0:<built-in method builtins.exec> | 1 | 1762 | 0.0319958 | 4.98491 |
| benchmark_gbdt_regressors.py:1:<module> | 1 | 1 | 5.5751e-05 | 4.98487 |
| benchmark_gbdt_regressors.py:369:main | 1 | 1 | 1.2127e-05 | 3.34161 |
| benchmark_gbdt_regressors.py:331:_emit_single | 1 | 1 | 0.00221819 | 3.33833 |
| benchmark_gbdt_regressors.py:138:_single_run | 1 | 1 | 0.000575117 | 3.33586 |
| /usr/lib/python3.12/threading.py:1115:join | 1 | 1 | 1.4429e-05 | 2.75071 |
| /usr/lib/python3.12/threading.py:1153:_wait_for_tstate_lock | 1 | 1 | 2.3842e-05 | 2.7506 |
| ~:0:<method 'acquire' of '_thread.lock' objects> | 6 | 8 | 0.000221224 | 2.75057 |
| /usr/lib/python3.12/threading.py:1016:_bootstrap | 1 | 1 | 0.000256966 | 2.75035 |
| /usr/lib/python3.12/threading.py:1056:_bootstrap_inner | 1 | 1 | 2.5728e-05 | 2.75009 |
| /usr/lib/python3.12/threading.py:999:run | 1 | 1 | 7.3379e-05 | 2.75006 |
| /root/.local/lib/python3.12/site-packages/xgboost/core.py:732:inner_f | 3 | 15 | 0.000217942 | 2.70359 |

### Native/C/C++/Cython-flavored stack leaf hotspots (py-spy --native)
| leaf_frame | sample_weight |
| --- | --- |
| xgboost::common::RowsWiseBuildHistKernel<false, xgboost::common::GHistBuildingManager<false, true, false, unsigned char> > | 0.63 |
| 0x7f2c6e01e02a | 0.63 |
| xgboost::common::GHistBuildingManager<false, true, false, unsigned char>::DispatchAndExecute<xgboost::common::BuildHist<false>(xgboost::common::Span<xgboost::detail::GradientPairInternal<float> const, (unsigned long)18446744073709551615>, xgboost::common::Span<unsigned long const, (unsigned long)18446744073709551615>, xgboost::GHistIndexMatrix const&, xgboost::common::Span<xgboost::detail::GradientPairInternal<double>, (unsigned long)18446744073709551615>, bool)::{lambda(auto:1)#1}> | 0.62 |
| clock_nanosleep | 0.39 |
| xgboost::common::ParallelFor<unsigned long, xgboost::data::cpu_impl::GetDataShape(xgboost::Context const*, xgboost::data::DMatrixProxy*, xgboost::data::DataIterProxy<void (void*), int (void*)>*, float, xgboost::data::ExternalDataInfo*)::{lambda()#1}::operator()() const::{lambda(auto:1 const&)#1}::operator()<xgboost::data::ArrayAdapterBatch>(xgboost::data::ArrayAdapterBatch const&) const::{lambda(auto:1)#1}> | 0.36 |
| 0x7f2c8da3e1ca | 0.23 |
| 0x7f2c6e01de62 | 0.23 |
| _aligned_strided_to_contig_size8 | 0.15 |
| xgboost::common::HistogramCuts::SearchBin | 0.15 |
| std::__introsort_loop<__gnu_cxx::__normal_iterator<xgboost::common::WQSummary<float, float>::Queue::QEntry*, std::vector<xgboost::common::WQSummary<float, float>::Queue::QEntry, std::allocator<xgboost::common::WQSummary<float, float>::Queue::QEntry> > >, long, __gnu_cxx::__ops::_Iter_less_iter> | 0.12 |
| 0x7f2c6e01e02e | 0.1 |
| 0x7f2c6e01e036 | 0.09 |

## lgbm_t4
### Python-level (cProfile) top cumulative entries
| function | primitive_calls | total_calls | total_time_s | cumulative_time_s |
| --- | --- | --- | --- | --- |
| ~:0:<built-in method builtins.exec> | 1 | 1762 | 0.0320351 | 4.76973 |
| benchmark_gbdt_regressors.py:1:<module> | 1 | 1 | 4.332e-05 | 4.76966 |
| benchmark_gbdt_regressors.py:369:main | 1 | 1 | 6.642e-06 | 3.1418 |
| benchmark_gbdt_regressors.py:331:_emit_single | 1 | 1 | 0.00198529 | 3.13942 |
| benchmark_gbdt_regressors.py:138:_single_run | 1 | 1 | 0.000501482 | 3.13725 |
| ~:0:<built-in method time.sleep> | 250 | 250 | 1.86172 | 2.89253 |
| /usr/lib/python3.12/threading.py:1115:join | 1 | 1 | 1.0601e-05 | 2.53567 |
| /usr/lib/python3.12/threading.py:1153:_wait_for_tstate_lock | 1 | 1 | 1.7469e-05 | 2.53555 |
| ~:0:<method 'acquire' of '_thread.lock' objects> | 6 | 8 | 0.000209225 | 2.53553 |
| /usr/lib/python3.12/threading.py:1016:_bootstrap | 1 | 1 | 0.000181796 | 2.53531 |
| /usr/lib/python3.12/threading.py:1056:_bootstrap_inner | 1 | 1 | 1.8719e-05 | 2.53513 |
| /usr/lib/python3.12/threading.py:999:run | 1 | 1 | 6.5438e-05 | 2.53511 |

### Native/C/C++/Cython-flavored stack leaf hotspots (py-spy --native)
| leaf_frame | sample_weight |
| --- | --- |
| LightGBM::DenseBin<unsigned char, false>::ConstructHistogram | 0.91 |
| LGBM_DatasetCreateFromMats._omp_fn.0 | 0.31 |
| clock_nanosleep | 0.29 |
| 0x7f11940698a2 | 0.27 |
| legacy_gauss.part.0 | 0.18 |
| 0x7f119750a6d2 | 0.17 |
| std::__merge_sort_loop<double*, double*, long, __gnu_cxx::__ops::_Iter_less_iter> | 0.17 |
| _compile_bytecode | 0.11 |
| _aligned_strided_to_contig_size8 | 0.11 |
| std::vector<int, std::allocator<int> >::emplace_back<int> | 0.11 |
| LightGBM::GBDT::PredictRaw | 0.11 |
| LightGBM::MarkUsed | 0.1 |

## lgbm_t16
### Python-level (cProfile) top cumulative entries
| function | primitive_calls | total_calls | total_time_s | cumulative_time_s |
| --- | --- | --- | --- | --- |
| ~:0:<built-in method builtins.exec> | 1 | 1762 | 0.0307744 | 5.5507 |
| benchmark_gbdt_regressors.py:1:<module> | 1 | 1 | 3.9495e-05 | 5.55067 |
| benchmark_gbdt_regressors.py:369:main | 1 | 1 | 6.417e-06 | 3.97298 |
| benchmark_gbdt_regressors.py:331:_emit_single | 1 | 1 | 0.000708279 | 3.97058 |
| benchmark_gbdt_regressors.py:138:_single_run | 1 | 1 | 0.000594293 | 3.96968 |
| ~:0:<built-in method time.sleep> | 341 | 341 | 2.79101 | 3.88799 |
| /usr/lib/python3.12/threading.py:1115:join | 1 | 1 | 1.0106e-05 | 3.47041 |
| /usr/lib/python3.12/threading.py:1153:_wait_for_tstate_lock | 1 | 1 | 1.3009e-05 | 3.47026 |
| ~:0:<method 'acquire' of '_thread.lock' objects> | 6 | 8 | 0.000212998 | 3.47026 |
| /usr/lib/python3.12/threading.py:1016:_bootstrap | 1 | 1 | 0.000236621 | 3.47004 |
| /usr/lib/python3.12/threading.py:1056:_bootstrap_inner | 1 | 1 | 1.634e-05 | 3.46981 |
| /usr/lib/python3.12/threading.py:999:run | 1 | 1 | 6.695e-05 | 3.46979 |

### Native/C/C++/Cython-flavored stack leaf hotspots (py-spy --native)
| leaf_frame | sample_weight |
| --- | --- |
| clock_nanosleep | 0.83 |
| 0x7fef6bc696ee | 0.52 |
| 0x7fef6bc698f3 | 0.51 |
| LightGBM::MultiValDenseBin<unsigned char>::ConstructHistogram | 0.41 |
| std::__merge_sort_loop<double*, double*, long, __gnu_cxx::__ops::_Iter_less_iter> | 0.38 |
| LGBM_DatasetCreateFromMats._omp_fn.0 | 0.31 |
| std::vector<int, std::allocator<int> >::emplace_back<int> | 0.26 |
| LGBM_DatasetCreateFromMats | 0.25 |
| 0x7fef6f1fa6d2 | 0.19 |
| 0x7fef6f0831ca | 0.19 |
| dedent | 0.16 |
| legacy_gauss.part.0 | 0.12 |

