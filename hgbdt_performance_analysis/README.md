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

CI matrix jobs use a runtime-bounded profile (`benchmark_execution_mode=inprocess`, `dataset_profile=ci_balanced`, thread regimes `1/cores/4x-cores`, and `--skip-alt-hparams`) to keep each machine run under ~5 minutes while still producing parity, scalability, and oversubscription diagnostics.

## Collecting CI outputs into the repo

Download artifacts from a run:

- `gh run download <run-id> --dir /tmp/hgbdt-ci-artifacts`

Consolidate:

- `uv run --python 3.11 --exclude-newer P7D python consolidate_ci_results.py --downloaded-artifacts-root /tmp/hgbdt-ci-artifacts --artifacts-root artifacts`

Generate detailed reports:

- `uv run --python 3.11 --exclude-newer P7D python generate_platform_detailed_analysis.py --artifacts-root artifacts`

## Main conclusions

1. No single model dominates every platform and every threading regime.
2. `lightgbm_hist` leads most often for mono-thread runtime and regular `1 -> cores` scaling, while `sklearn_hgb_fixed` is strongest in oversubscribed `4x cores` robustness.
3. Platform-specific diagnostics remain mandatory before declaring a global winner.

### Per-platform benchmark plots

These plots show median total runtime ranking (lower is better):

- **linux-amd64** (winner: `sklearn_hgb_fixed`)
  - ![linux-amd64 ranking](artifacts/machines/linux-amd64/benchmark_ranked_models.png)
- **linux-arm64** (winner: `sklearn_hgb_fixed`)
  - ![linux-arm64 ranking](artifacts/machines/linux-arm64/benchmark_ranked_models.png)
- **macos-arm64** (winner: `sklearn_hgb_fixed`)
  - ![macos-arm64 ranking](artifacts/machines/macos-arm64/benchmark_ranked_models.png)
- **windows-amd64** (winner: `lightgbm_hist`)
  - ![windows-amd64 ranking](artifacts/machines/windows-amd64/benchmark_ranked_models.png)

### Cross-platform contrast and platform-specific variations

From `artifacts/platform_specific_summary.json`:

- Winner split:
  - `sklearn_hgb_fixed`: 3/4 platforms
  - `lightgbm_hist`: 1/4 platforms
- Slowest model:
  - `xgboost_hist`: 2/4 platforms
  - `sklearn_hgb`: 2/4 platforms
- Worst/best median runtime ratio by model:
  - `lightgbm_hist`: `1.911x`
  - `sklearn_hgb`: `1.144x`
  - `sklearn_hgb_fixed`: `1.866x`
  - `xgboost_hist`: `2.021x`
- Profiling coverage note:
  - Windows artifacts are generated without native py-spy (`native_profile_enabled=false`), while Linux/macOS include native profile snapshots.

### Cross-platform comparison by performance regime

Regime summaries below are computed from all datasets (`small`, `medium`, `large`) and both hyperparameter settings (`baseline_default`, `deep_few_trees`) in the consolidated artifacts committed in this repository. CI matrix jobs now run a faster baseline-only profile (`--skip-alt-hparams`) to stay within runtime budget, while preserving the same mono-thread/scalability/oversubscription measurement structure.

#### 1) Mono-thread performance (`threads=1`, lower `total_seconds` is better)

- Most frequent winner by platform: `lightgbm_hist` (3/4 platforms), with `sklearn_hgb` leading on linux-amd64.
- Global median `total_seconds` across all runs:
  - `lightgbm_hist`: `5.3195s`
  - `sklearn_hgb`: `5.4498s`
  - `sklearn_hgb_fixed`: `5.4821s`
  - `xgboost_hist`: `7.0055s`

#### 2) Regular-regime scalability (`1 -> cores`, higher `fit_speedup` is better)

- Most frequent winner by platform: `lightgbm_hist` (3/4 platforms), with `sklearn_hgb_fixed` leading on macos-arm64.
- Global median `fit_speedup(1->cores)`:
  - `lightgbm_hist`: `2.2608x`
  - `sklearn_hgb_fixed`: `1.9872x`
  - `sklearn_hgb`: `1.9519x`
  - `xgboost_hist`: `1.6619x`

#### 3) Oversubscription robustness (`4x cores / cores`, lower fit-time ratio is better)

- Most frequent winner by platform: `sklearn_hgb_fixed` (3/4 platforms), with `xgboost_hist` leading on windows-amd64.
- Global median `fit_time_ratio(4x_vs_cores)`:
  - `xgboost_hist`: `1.0150x`
  - `sklearn_hgb_fixed`: `1.0163x`
  - `lightgbm_hist`: `1.6208x`
  - `sklearn_hgb`: `3.1016x`

Interpretation: `lightgbm_hist` usually wins in non-oversubscribed throughput, while `sklearn_hgb_fixed` and `xgboost_hist` are substantially more resilient than `lightgbm_hist` and especially `sklearn_hgb` under heavy oversubscription.

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
- Absolute fit-time plots for both settings:
  - `baseline_default` (`fit_time_threads.png`)
  - `deep_few_trees` (`fit_time_threads_deep_few_trees.png`)
  - Vertical markers annotate `cores`, `2x cores`, and `4x cores` regimes.
- Oversubscription regime tables at `cores`, `2x cores`, and `4x cores`.
- Measured per-model `r2` parity tables.
- Effective tree-count and node-per-tree parity checks (`fitted_trees`, `expected_trees`, `total_nodes`, `avg_nodes_per_tree`).
- Machine metadata (`logical/physical` CPU counts, core-type breakdown, hyper-threading flag, CFS quota, and cpuset when available).
- Root-cause diagnostics for sklearn single-thread/scalability underperformance when detected, plus implementation plans for each issue.
