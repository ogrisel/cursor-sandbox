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
