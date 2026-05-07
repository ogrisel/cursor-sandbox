# AGENTS.md

## Repository overview

- Main project folder: `hgbdt_performance_analysis/`
- CI workflow: `.github/workflows/benchmark-profiling-matrix.yml`
- Bench/profiling outputs are machine-scoped under `hgbdt_performance_analysis/artifacts/machines/<machine-tag>/`

## Environment setup

Use Python 3.11+.

Install required Python dependencies:

- `numpy`
- `psutil`
- `scikit-learn`
- `xgboost`
- `lightgbm`
- `matplotlib`
- `threadpoolctl`
- `py-spy` (required for native profiling on non-Windows workers)

Recommended bootstrap command:

- `python3 -m pip install numpy psutil scikit-learn xgboost lightgbm matplotlib threadpoolctl py-spy`

If `py-spy` is installed to `~/.local/bin`, add it to `PATH`:

- `export PATH="$HOME/.local/bin:$PATH"`

## Cursor Cloud specific instructions

- Keep CI and local artifact paths machine-scoped; do not collapse outputs into a shared flat folder.
- For full benchmark + profiling smoke execution:
  - `python3 hgbdt_performance_analysis/run_ci_benchmarks_profiles.py --machine-tag <tag> --artifacts-root hgbdt_performance_analysis/artifacts`
- To consolidate downloaded CI artifacts into repo subfolders and regenerate platform conclusions:
  - `python3 hgbdt_performance_analysis/consolidate_ci_results.py --downloaded-artifacts-root <download_dir> --artifacts-root hgbdt_performance_analysis/artifacts`

## CI artifact download + consolidation

Download artifacts for a run:

- `gh run download <run-id> --dir /tmp/hgbdt-ci-artifacts`

Consolidate and regenerate platform-specific reports:

- `python3 hgbdt_performance_analysis/consolidate_ci_results.py --downloaded-artifacts-root /tmp/hgbdt-ci-artifacts --artifacts-root hgbdt_performance_analysis/artifacts`

Expected consolidated outputs:

- `hgbdt_performance_analysis/artifacts/machines/<machine-tag>/...`
- `hgbdt_performance_analysis/artifacts/platform_specific_summary.json`
- `hgbdt_performance_analysis/artifacts/platform_specific_conclusions.md`
