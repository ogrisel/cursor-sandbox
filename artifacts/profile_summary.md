# Profiling snapshots

## sklearn_hgb
### Python-level (cProfile) top cumulative entries
| function | primitive_calls | total_calls | total_time_s | cumulative_time_s |
| --- | --- | --- | --- | --- |
| ~:0:<built-in method builtins.exec> | 1 | 1703 | 0.0308818 | 3.45094 |
| benchmark_gbdt_regressors.py:1:<module> | 1 | 1 | 4.5416e-05 | 3.45085 |
| benchmark_gbdt_regressors.py:342:main | 1 | 1 | 5.703e-06 | 1.97733 |
| benchmark_gbdt_regressors.py:308:_emit_single | 1 | 1 | 0.000701038 | 1.97505 |
| benchmark_gbdt_regressors.py:128:_single_run | 1 | 1 | 0.000279842 | 1.97425 |
| /usr/lib/python3.12/threading.py:1115:join | 4 | 4 | 4.3071e-05 | 1.96094 |
| ~:0:<method 'acquire' of '_thread.lock' objects> | 282 | 302 | 0.000242366 | 1.96083 |
| /usr/lib/python3.12/threading.py:1153:_wait_for_tstate_lock | 13 | 13 | 2.7376e-05 | 1.96079 |
| /usr/lib/python3.12/threading.py:1016:_bootstrap | 1 | 8 | 7.3627e-05 | 1.7787 |
| /usr/lib/python3.12/threading.py:1056:_bootstrap_inner | 1 | 8 | 7.424e-05 | 1.77865 |
| /usr/lib/python3.12/threading.py:999:run | 1 | 8 | 9.4905e-05 | 1.77863 |
| /root/.local/lib/python3.12/site-packages/sklearn/base.py:1319:wrapper | 1 | 1 | 0.000432669 | 1.71599 |

### Native/C/C++/Cython-flavored stack leaf hotspots (py-spy --native)
| leaf_frame | sample_weight |
| --- | --- |
| 0x7f259161e02a | 0.71 |
| 0x7f25b11b6d71 | 0.38 |
| histogram__build_histogram_no_hessian.isra.0 | 0.18 |
| histogram__build_histogram_root_no_hessian.isra.0 | 0.16 |
| clock_nanosleep | 0.15 |
| _compile_bytecode | 0.12 |
| _aligned_strided_to_contig_size8 | 0.11 |
| dedent | 0.1 |
| _binning__map_col_to_bins._omp_fn.0 | 0.1 |
| 0x7f259161e036 | 0.1 |
| 0x7f25b11481ca | 0.1 |
| 0x7f25b11ca51a | 0.08 |

## lightgbm_hist
### Python-level (cProfile) top cumulative entries
| function | primitive_calls | total_calls | total_time_s | cumulative_time_s |
| --- | --- | --- | --- | --- |
| ~:0:<built-in method builtins.exec> | 1 | 1701 | 0.0303233 | 7.17186 |
| benchmark_gbdt_regressors.py:1:<module> | 1 | 1 | 4.2792e-05 | 7.17182 |
| benchmark_gbdt_regressors.py:342:main | 1 | 1 | 6.493e-06 | 5.70479 |
| benchmark_gbdt_regressors.py:308:_emit_single | 1 | 1 | 0.000545054 | 5.70246 |
| benchmark_gbdt_regressors.py:128:_single_run | 1 | 1 | 0.000284861 | 5.70175 |
| /usr/lib/python3.12/threading.py:1115:join | 1 | 1 | 1.1309e-05 | 5.50699 |
| /usr/lib/python3.12/threading.py:1153:_wait_for_tstate_lock | 1 | 1 | 2.4046e-05 | 5.50691 |
| ~:0:<method 'acquire' of '_thread.lock' objects> | 6 | 8 | 0.000189333 | 5.50687 |
| /usr/lib/python3.12/threading.py:1016:_bootstrap | 1 | 1 | 4.3018e-05 | 5.50668 |
| /usr/lib/python3.12/threading.py:1056:_bootstrap_inner | 1 | 1 | 1.1956e-05 | 5.50664 |
| /usr/lib/python3.12/threading.py:999:run | 1 | 1 | 4.5116e-05 | 5.50662 |
| /root/.local/lib/python3.12/site-packages/lightgbm/sklearn.py:1381:fit | 1 | 1 | 1.3733e-05 | 5.27073 |

### Native/C/C++/Cython-flavored stack leaf hotspots (py-spy --native)
| leaf_frame | sample_weight |
| --- | --- |
| LightGBM::DenseBin<unsigned char, false>::ConstructHistogram | 2.94 |
| clock_nanosleep | 0.87 |
| std::_Function_handler<void (double, double, int, LightGBM::FeatureConstraint const*, double, LightGBM::SplitInfo*), LightGBM::FeatureHistogram::FuncForNumricalL3<false, false, false, false, false>()::{lambda(double, double, int, LightGBM::FeatureConstraint const*, double, LightGBM::SplitInfo*)#7}>::_M_invoke | 0.85 |
| LGBM_DatasetCreateFromMats._omp_fn.0 | 0.49 |
| std::__merge_sort_loop<double*, double*, long, __gnu_cxx::__ops::_Iter_less_iter> | 0.41 |
| LightGBM::DenseBin<unsigned char, false>::Split | 0.4 |
| LightGBM::GBDT::PredictRaw | 0.3 |
| LightGBM::Dataset::FixHistogram | 0.29 |
| 0x7f0238cef1ca | 0.17 |
| LightGBM::Dataset::ConstructHistogramsInner<true, false, false, 0> | 0.16 |
| _compile_bytecode | 0.11 |
| dedent | 0.09 |

## xgboost_hist
### Python-level (cProfile) top cumulative entries
| function | primitive_calls | total_calls | total_time_s | cumulative_time_s |
| --- | --- | --- | --- | --- |
| ~:0:<built-in method builtins.exec> | 1 | 1701 | 0.0301124 | 9.18817 |
| benchmark_gbdt_regressors.py:1:<module> | 1 | 1 | 4.0829e-05 | 9.18813 |
| benchmark_gbdt_regressors.py:342:main | 1 | 1 | 6.718e-06 | 7.71369 |
| benchmark_gbdt_regressors.py:308:_emit_single | 1 | 1 | 0.00139067 | 7.71136 |
| benchmark_gbdt_regressors.py:128:_single_run | 1 | 1 | 0.000287642 | 7.70979 |
| /usr/lib/python3.12/threading.py:1115:join | 1 | 1 | 7.887e-06 | 7.50698 |
| /usr/lib/python3.12/threading.py:1153:_wait_for_tstate_lock | 1 | 1 | 1.3944e-05 | 7.50691 |
| ~:0:<method 'acquire' of '_thread.lock' objects> | 6 | 8 | 0.000153883 | 7.50688 |
| /usr/lib/python3.12/threading.py:1016:_bootstrap | 1 | 1 | 4.9108e-05 | 7.50672 |
| /usr/lib/python3.12/threading.py:1056:_bootstrap_inner | 1 | 1 | 9.331e-06 | 7.50667 |
| /usr/lib/python3.12/threading.py:999:run | 1 | 1 | 2.204e-05 | 7.50666 |
| /root/.local/lib/python3.12/site-packages/xgboost/core.py:732:inner_f | 3 | 15 | 0.000192583 | 7.45039 |

### Native/C/C++/Cython-flavored stack leaf hotspots (py-spy --native)
| leaf_frame | sample_weight |
| --- | --- |
| xgboost::tree::TreeEvaluator::SplitEvaluator<xgboost::tree::TrainParam>::CalcSplitGain<xgboost::tree::GradStats> | 2.29 |
| xgboost::common::GHistBuildingManager<false, true, false, unsigned char>::DispatchAndExecute<xgboost::common::BuildHist<false>(xgboost::common::Span<xgboost::detail::GradientPairInternal<float> const, (unsigned long)18446744073709551615>, xgboost::common::Span<unsigned long const, (unsigned long)18446744073709551615>, xgboost::GHistIndexMatrix const&, xgboost::common::Span<xgboost::detail::GradientPairInternal<double>, (unsigned long)18446744073709551615>, bool)::{lambda(auto:1)#1}> | 1.89 |
| xgboost::common::RowsWiseBuildHistKernel<false, xgboost::common::GHistBuildingManager<false, true, false, unsigned char> > | 1.69 |
| xgboost::tree::HistEvaluator::EnumerateSplit<1> | 1.29 |
| clock_nanosleep | 1.11 |
| xgboost::common::PartitionBuilder<(unsigned long)2048>::Partition<unsigned char, false, false, xgboost::tree::CPUExpandEntry, xgboost::tree::ScalarTreeView> | 0.44 |
| xgboost::common::HistogramCuts::SearchBin | 0.34 |
| std::__introsort_loop<__gnu_cxx::__normal_iterator<xgboost::common::WQSummary<float, float>::Queue::QEntry*, std::vector<xgboost::common::WQSummary<float, float>::Queue::QEntry, std::allocator<xgboost::common::WQSummary<float, float>::Queue::QEntry> > >, long, __gnu_cxx::__ops::_Iter_less_iter> | 0.32 |
| xgboost::common::SubtractionHist | 0.26 |
| 0x7fa0149e31ca | 0.19 |
| xgboost::data::cpu_impl::GetDataShape(xgboost::Context const*, xgboost::data::DMatrixProxy*, xgboost::data::DataIterProxy<void (void*), int (void*)>*, float, xgboost::data::ExternalDataInfo*)::{lambda()#1}::operator()() const::{lambda(auto:1 const&)#1}::operator()<xgboost::data::ArrayAdapterBatch>(xgboost::data::ArrayAdapterBatch const&) const::{lambda(auto:1)#1}::operator()<unsigned long> const | 0.15 |
| xgboost::tree::cpu_impl::UniformSample | 0.13 |

