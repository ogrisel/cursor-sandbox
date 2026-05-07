# HGBDT performance analysis study

This folder contains the complete benchmarking, profiling, and analysis work for comparing:

- `scikit-learn` `HistGradientBoostingRegressor`
- `xgboost` histogram trees
- `lightgbm` histogram trees

under aligned hyperparameters, aligned fitted-tree counts, and controlled runtime budgets.

## Scope

- Build a reproducible benchmark harness with timeout-aware adaptive dataset sizing.
- Enforce cross-library comparability:
  - matched hyperparameters,
  - R² parity checks,
  - fitted-tree parity checks (early stopping disabled where needed).
- Measure scalability from 1 thread to oversubscription regimes.
- Profile hotspots at Python and native levels.
- Identify root causes for slowdowns and propose implementation strategies.

Core scripts:

- [`benchmark_gbdt_regressors.py`](benchmark_gbdt_regressors.py)
- [`aligned_large_comparison.py`](aligned_large_comparison.py)
- [`plot_scalability_curves.py`](plot_scalability_curves.py)
- [`calibrate_shared_hyperparams.py`](calibrate_shared_hyperparams.py)
- [`focused_sklearn_vs_lightgbm.py`](focused_sklearn_vs_lightgbm.py)
- [`analyze_benchmark_results.py`](analyze_benchmark_results.py)
- [`extract_profile_insights.py`](extract_profile_insights.py)

## Main conclusions

1. **With aligned constraints, relative rankings depend on regime, but oversubscription harms sklearn most without mitigation.**
   - Oversubscription validation and diagnostics:
     - [`artifacts/oversubscription_fix_validation.md`](artifacts/oversubscription_fix_validation.md)
     - [`artifacts/oversubscription_overhead_report.md`](artifacts/oversubscription_overhead_report.md)
     - [`artifacts/oversubscription_context_switches.json`](artifacts/oversubscription_context_switches.json)
     - [`artifacts/oversubscription_wait_policy_results.json`](artifacts/oversubscription_wait_policy_results.json)

2. **A simple thread-capping mitigation for sklearn avoids catastrophic oversubscription behavior.**
   - Patch and summary:
     - [`artifacts/sklearn_histgb_thread_cap.patch`](artifacts/sklearn_histgb_thread_cap.patch)
     - [`artifacts/oversubscription_fix_report.md`](artifacts/oversubscription_fix_report.md)

3. **A parity-compliant setting exists where sklearn is significantly slower than LightGBM at 4 threads.**
   - Confirmed setting and multi-seed evidence:
     - [`artifacts/sklearn_slow_4threads_setting.md`](artifacts/sklearn_slow_4threads_setting.md)
     - [`artifacts/sklearn_slow_4threads_setting.json`](artifacts/sklearn_slow_4threads_setting.json)
     - [`artifacts/sklearn_slow_4threads_top10_multiseed.json`](artifacts/sklearn_slow_4threads_top10_multiseed.json)

4. **For that setting, profiler evidence points to fine-grained per-node orchestration/synchronization overhead in sklearn.**
   - Profile summary and root-cause write-up:
     - [`artifacts/profile_slowdown_setting_summary.json`](artifacts/profile_slowdown_setting_summary.json)
     - [`artifacts/profile_slowdown_setting_root_cause.md`](artifacts/profile_slowdown_setting_root_cause.md)
   - Extended implementation comparison:
     - [`artifacts/oversubscription_xgboost_vs_sklearn_impl_analysis.md`](artifacts/oversubscription_xgboost_vs_sklearn_impl_analysis.md)

## Implementation strategy to improve sklearn efficiency (for the slow setting)

Priority plan:

1. **Adaptive per-node thread selection** in grow/split/hist paths to reduce short-region OpenMP overhead on small nodes.
2. **Small-node serial fast path** in `split_indices` to bypass two-phase `prange + memcpy` machinery when node work is tiny.
3. **Scratch-buffer reuse** in `split_indices` and `find_node_split` to avoid frequent allocations in hot loops.
4. **Optional phase 2:** mini-batch processing of multiple frontier nodes to increase task granularity.

Rationale and evidence links:

- Root cause from profiling:
  - [`artifacts/profile_slowdown_setting_root_cause.md`](artifacts/profile_slowdown_setting_root_cause.md)
  - [`artifacts/profile_slowdown_setting_summary.json`](artifacts/profile_slowdown_setting_summary.json)
- Existing oversubscription implementation analysis:
  - [`artifacts/oversubscription_xgboost_vs_sklearn_impl_analysis.md`](artifacts/oversubscription_xgboost_vs_sklearn_impl_analysis.md)

## Additional reports and data

- Comparable aligned large-run outputs:
  - [`artifacts/comparable_large_report.md`](artifacts/comparable_large_report.md)
  - [`artifacts/comparable_large_results.json`](artifacts/comparable_large_results.json)
  - [`artifacts/comparable_large_params.json`](artifacts/comparable_large_params.json)
- Deep-few-trees regime:
  - [`artifacts/deep_few_trees_report.md`](artifacts/deep_few_trees_report.md)
  - [`artifacts/deep_few_trees_analysis.md`](artifacts/deep_few_trees_analysis.md)
  - [`artifacts/deep_few_trees_results.json`](artifacts/deep_few_trees_results.json)
  - [`artifacts/deep_few_trees_scalability_data.json`](artifacts/deep_few_trees_scalability_data.json)
  - [`artifacts/deep_few_trees_scalability.png`](artifacts/deep_few_trees_scalability.png)
