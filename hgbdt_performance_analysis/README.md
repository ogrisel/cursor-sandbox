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
- [`run_ci_benchmarks_profiles.py`](run_ci_benchmarks_profiles.py)
- [`consolidate_ci_results.py`](consolidate_ci_results.py)

## Machine-scoped artifact layout

Benchmark and profiling outputs are now written to machine-specific folders by default:

- `artifacts/machines/linux-amd64/`
- `artifacts/machines/linux-arm64/`
- `artifacts/machines/macos-arm64/`
- `artifacts/machines/windows-amd64/`

Each script accepts:

- `--artifacts-root` (base output directory, defaults to `artifacts/`)
- `--machine-tag` (override machine subfolder; otherwise auto-detected from OS + arch)

This lets reruns from heterogeneous workers coexist without clobbering each other.

## CI matrix reruns (macOS/Linux/Windows)

Workflow: [`.github/workflows/benchmark-profiling-matrix.yml`](../.github/workflows/benchmark-profiling-matrix.yml)

It runs benchmark + profiling collection on:

- Linux amd64 (`ubuntu-24.04`)
- Linux arm64 (`ubuntu-24.04-arm`)
- macOS arm64 (`macos-14`)
- Windows amd64 (`windows-2022`)

The workflow executes `run_ci_benchmarks_profiles.py` and uploads machine-scoped artifacts per runner.
Native py-spy collection is enabled on non-Windows runners; Windows keeps cProfile-based summaries.
After matrix completion, a consolidation job downloads all per-machine artifacts, rebuilds
`artifacts/machines/<machine-tag>/`, generates platform-specific conclusions, and uploads a
consolidated downloadable bundle (`benchmark-profiles-consolidated`).

## Consolidating downloadable CI artifacts into the repo

Download artifacts from a workflow run:

- `gh run download <run-id> --dir /tmp/hgbdt-ci-artifacts`

Consolidate and regenerate platform conclusions:

- `python consolidate_ci_results.py --downloaded-artifacts-root /tmp/hgbdt-ci-artifacts --artifacts-root artifacts`

This updates:

- `artifacts/machines/<machine-tag>/...`
- `artifacts/platform_specific_summary.json`
- `artifacts/platform_specific_conclusions.md`

## Main conclusions

1. **With aligned constraints, relative rankings depend on regime, but oversubscription harms sklearn most without mitigation.**
   - Oversubscription validation and diagnostics:
     - [`artifacts/oversubscription_fix_validation.md`](artifacts/oversubscription_fix_validation.md)
     - [`artifacts/oversubscription_overhead_report.md`](artifacts/oversubscription_overhead_report.md)
     - [`artifacts/oversubscription_context_switches.json`](artifacts/oversubscription_context_switches.json)
     - [`artifacts/oversubscription_wait_policy_results.json`](artifacts/oversubscription_wait_policy_results.json)
   - Main scalability view (1..16 threads):

     ![Scalability curves 1 to 16 threads](artifacts/scalability_curves_1_to_16_threads.png)

2. **A simple thread-capping mitigation for sklearn avoids catastrophic oversubscription behavior.**
   - Patch and summary:
     - [`artifacts/sklearn_histgb_thread_cap.patch`](artifacts/sklearn_histgb_thread_cap.patch)
     - [`artifacts/oversubscription_fix_report.md`](artifacts/oversubscription_fix_report.md)
   - Large-dataset comparison with and without sklearn fix:

     ![Large dataset scalability with sklearn fixed variant](artifacts/scalability_large_with_fix.png)

   - Small-dataset comparison with and without sklearn fix:

     ![Small dataset scalability with sklearn fixed variant](artifacts/scalability_small_with_fix.png)

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

5. **In the deep-few-trees regime, sklearn leads at 1-2 threads while LightGBM is fastest at 4 threads.**
   - Regime analysis and data:
     - [`artifacts/deep_few_trees_report.md`](artifacts/deep_few_trees_report.md)
     - [`artifacts/deep_few_trees_analysis.md`](artifacts/deep_few_trees_analysis.md)
     - [`artifacts/deep_few_trees_results.json`](artifacts/deep_few_trees_results.json)
     - [`artifacts/deep_few_trees_scalability_data.json`](artifacts/deep_few_trees_scalability_data.json)

     ![Deep few trees scalability plot](artifacts/deep_few_trees_scalability.png)

6. **Cross-platform conclusions are now explicitly scoped by machine.**
   - Consolidated platform summary and conclusion report:
     - [`artifacts/platform_specific_summary.json`](artifacts/platform_specific_summary.json)
     - [`artifacts/platform_specific_conclusions.md`](artifacts/platform_specific_conclusions.md)
   - Interpretation rule:
     - if top model differs by machine tag, conclusions must remain platform-specific.

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
   - Main scalability view (1..16 threads):

     ![Scalability curves 1 to 16 threads](artifacts/scalability_curves_1_to_16_threads.png)

2. **A simple thread-capping mitigation for sklearn avoids catastrophic oversubscription behavior.**
   - Patch and summary:
     - [`artifacts/sklearn_histgb_thread_cap.patch`](artifacts/sklearn_histgb_thread_cap.patch)
     - [`artifacts/oversubscription_fix_report.md`](artifacts/oversubscription_fix_report.md)
   - Large-dataset comparison with and without sklearn fix:

     ![Large dataset scalability with sklearn fixed variant](artifacts/scalability_large_with_fix.png)

   - Small-dataset comparison with and without sklearn fix:

     ![Small dataset scalability with sklearn fixed variant](artifacts/scalability_small_with_fix.png)

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

5. **In the deep-few-trees regime, sklearn leads at 1-2 threads while LightGBM is fastest at 4 threads.**
   - Regime analysis and data:
     - [`artifacts/deep_few_trees_report.md`](artifacts/deep_few_trees_report.md)
     - [`artifacts/deep_few_trees_analysis.md`](artifacts/deep_few_trees_analysis.md)
     - [`artifacts/deep_few_trees_results.json`](artifacts/deep_few_trees_results.json)
     - [`artifacts/deep_few_trees_scalability_data.json`](artifacts/deep_few_trees_scalability_data.json)

     ![Deep few trees scalability plot](artifacts/deep_few_trees_scalability.png)

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
