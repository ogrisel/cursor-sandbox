# AGENTS.md

## Repository overview

- Main project folder: `hgbdt_performance_analysis/`
- CI workflow: `.github/workflows/benchmark-profiling-matrix.yml`
- Bench/profiling outputs are machine-scoped under `hgbdt_performance_analysis/artifacts/machines/<machine-tag>/`

## Environment setup

Use `uv` with Python 3.11+ for local and CI execution.

Runtime dependencies used by benchmark/profiling scripts:

- `numpy`
- `psutil`
- `scikit-learn`
- `xgboost`
- `lightgbm`
- `matplotlib`
- `threadpoolctl`
- `py-spy` (required for native profiling on non-Windows workers)

Recommended uv execution pattern (no manual venv bootstrap required):

- `uv run --python 3.11 --exclude-newer P7D --with numpy --with psutil --with scikit-learn --with xgboost --with lightgbm --with matplotlib --with threadpoolctl --with py-spy python <script>.py`

Optional (for repeated local runs): create a persistent uv-managed venv.

- `uv venv --python 3.11 --exclude-newer P7D .venv`
- Activate `.venv` and install dependencies with `uv pip install ...` if you want a stable local environment.

## Cursor Cloud specific instructions

- Keep CI and local artifact paths machine-scoped; do not collapse outputs into a shared flat folder.
- For full benchmark + profiling smoke execution:
  - `uv run --python 3.11 --exclude-newer P7D --with numpy --with psutil --with scikit-learn --with xgboost --with lightgbm --with matplotlib --with threadpoolctl --with py-spy python hgbdt_performance_analysis/run_ci_benchmarks_profiles.py --machine-tag <tag> --artifacts-root hgbdt_performance_analysis/artifacts`
- To consolidate downloaded CI artifacts into repo subfolders and regenerate platform conclusions:
  - `uv run --python 3.11 --exclude-newer P7D python hgbdt_performance_analysis/consolidate_ci_results.py --downloaded-artifacts-root <download_dir> --artifacts-root hgbdt_performance_analysis/artifacts`

## CI artifact download + consolidation

Download artifacts for a run:

- `gh run download <run-id> --dir /tmp/hgbdt-ci-artifacts`

Consolidate and regenerate platform-specific reports:

- `uv run --python 3.11 --exclude-newer P7D python hgbdt_performance_analysis/consolidate_ci_results.py --downloaded-artifacts-root /tmp/hgbdt-ci-artifacts --artifacts-root hgbdt_performance_analysis/artifacts`

Expected consolidated outputs:

- `hgbdt_performance_analysis/artifacts/machines/<machine-tag>/...`
- `hgbdt_performance_analysis/artifacts/platform_specific_summary.json`
- `hgbdt_performance_analysis/artifacts/platform_specific_conclusions.md`
