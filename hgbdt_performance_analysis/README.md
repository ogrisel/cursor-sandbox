# HGBDT performance analysis study

This project benchmarks and profiles:

- `scikit-learn` `HistGradientBoostingRegressor`
- `xgboost` histogram trees
- `lightgbm` histogram trees

with aligned constraints and machine-scoped artifact collection.

## Scope

- Reproducible benchmark harness with timeout-aware adaptive dataset sizing.
- Cross-library comparability checks (R² spread, fitted-tree parity, and node-count parity).
- Thread scalability analysis and profile extraction.
- CI matrix reruns across Linux/macOS/Windows with artifact consolidation.

Core scripts:

- `benchmark_gbdt_regressors.py`
- `analyze_benchmark_results.py`
- `run_ci_benchmarks_profiles.py`
- `consolidate_ci_results.py`
- `generate_platform_detailed_analysis.py`

## Artifact layout

Per-machine outputs are consolidated under:

- `artifacts/machines/linux-amd64/`
- `artifacts/machines/linux-arm64/`
- `artifacts/machines/macos-arm64/`
- `artifacts/machines/windows-amd64/`

Cross-platform summaries:

- `artifacts/platform_specific_summary.json`
- `artifacts/platform_specific_conclusions.md`
- `artifacts/platform_detailed_analysis_index.md`

## CI workflow

Workflow file: `.github/workflows/benchmark-profiling-matrix.yml`

The matrix uploads:

- per-machine artifacts: `benchmark-profiles-<machine-tag>`
- consolidated bundle: `benchmark-profiles-consolidated`

## Collecting CI outputs into the repo

Download artifacts from a run:

- `gh run download <run-id> --dir /tmp/hgbdt-ci-artifacts`

Consolidate:

- `uv run --python 3.11 --exclude-newer P7D python consolidate_ci_results.py --downloaded-artifacts-root /tmp/hgbdt-ci-artifacts --artifacts-root artifacts`

Generate detailed reports:

- `uv run --python 3.11 --exclude-newer P7D python generate_platform_detailed_analysis.py --artifacts-root artifacts`

## Main conclusions

1. Relative runtime ranking is regime-dependent and not globally stable across platforms.
2. `xgboost_hist` remains the slowest model on all four CI platforms in this benchmark regime.
3. Platform-specific conclusions are required before claiming a global winner.

### Per-platform benchmark plots (CI run `25525901055`)

These plots show median total runtime ranking (lower is better):

- **linux-amd64** (winner: `lightgbm_hist`)
  - ![linux-amd64 ranking](artifacts/machines/linux-amd64/benchmark_ranked_models.png)
- **linux-arm64** (winner: `lightgbm_hist`)
  - ![linux-arm64 ranking](artifacts/machines/linux-arm64/benchmark_ranked_models.png)
- **macos-arm64** (winner: `sklearn_hgb_fixed`)
  - ![macos-arm64 ranking](artifacts/machines/macos-arm64/benchmark_ranked_models.png)
- **windows-amd64** (winner: `lightgbm_hist`)
  - ![windows-amd64 ranking](artifacts/machines/windows-amd64/benchmark_ranked_models.png)

### Cross-platform contrast and platform-specific variations

From `artifacts/platform_specific_summary.json`:

- Winner split:
  - `lightgbm_hist`: 3/4 platforms
  - `sklearn_hgb_fixed`: 1/4 platforms
- Slowest model:
  - `xgboost_hist`: 4/4 platforms
- Worst/best median runtime ratio by model:
  - `lightgbm_hist`: `1.628x`
  - `sklearn_hgb`: `1.348x`
  - `sklearn_hgb_fixed`: `1.354x`
  - `xgboost_hist`: `1.424x`
- Profiling coverage note:
  - Windows artifacts are generated without native py-spy (`native_profile_enabled=false`), while Linux/macOS include native profile snapshots.

## Per-platform detailed analysis (root causes + implementation plans)

- Index: [platform detailed analysis index](artifacts/platform_detailed_analysis_index.md)
- linux-amd64: [detailed analysis](artifacts/machines/linux-amd64/detailed_analysis.md)
- linux-arm64: [detailed analysis](artifacts/machines/linux-arm64/detailed_analysis.md)
- macos-arm64: [detailed analysis](artifacts/machines/macos-arm64/detailed_analysis.md)
- windows-amd64: [detailed analysis](artifacts/machines/windows-amd64/detailed_analysis.md)

Each detailed report includes:

- Scalability plots for both settings:
  - `baseline_default` (`scalability.png`)
  - `deep_few_trees` (`scalability_deep_few_trees.png`)
- Measured per-model `r2` parity tables.
- Effective tree-count and node-per-tree parity checks (`fitted_trees`, `expected_trees`, `total_nodes`, `avg_nodes_per_tree`).
- Root-cause diagnostics for sklearn single-thread/scalability underperformance when detected, plus implementation plans for each issue.
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
