# BLIS macOS arm64 minimal reproducers

Minimal reproducers for macOS arm64 BLAS regressions when conda-forge defaults to BLIS ([scikit-learn#34162 discussion](https://github.com/scikit-learn/scikit-learn/pull/34162#discussion_r3332644920)).

Threading: do **not** set `OMP_NUM_THREADS=1` for BLIS runs (`BLIS_NUM_THREADS=8`).

## Progressive minimal levels (`minimal_blis_reproducer.py`)

Levels are ordered from **smallest** sklearn surface to largest (`--list-levels`):

| Level | sklearn used | What fails on BLIS |
|-------|----------------|-------------------|
| `knn-imputer-only` | `KNNImputer` only | `[2,2]` vs literal `2.3` |
| **`scalar-vs-imputer`** | **`KNNImputer` only** | **Primary CI gate** — `[2,2]` vs scalar `nan_euclidean` |
| `scalar-full-matrix` | `KNNImputer` | Full 8×4 vs scalar-reference distances |
| `sklearn-dist-vs-imputer` | `pairwise_distances` + `KNNImputer` | Full matrix (chunked imputer vs full dist) |
| `pytest` | full test module | `test_knn_imputer_weight_distance[nan]` |
| `numpy-gemm` | none | Usually **passes** (GEMM vs scalar loop) |

```bash
./blis_macos_reproducer/run_minimal_blas_reproducer.sh blis scalar-vs-imputer
./blis_macos_reproducer/run_minimal_blas_reproducer.sh openblas scalar-vs-imputer
python blis_macos_reproducer/minimal_blis_reproducer.py --list-levels
```

### Primary reproducer (`scalar-vs-imputer`)

- **Expected** `imputed[2,2]`: weighted average using **NumPy scalar** `nan_euclidean` (no BLAS GEMM).
- **Actual** `imputed[2,2]`: `sklearn.impute.KNNImputer` with default config (same as upstream pytest).

This is the smallest check that still fails on BLIS (~`0.5` vs ~`2.3`).

## Other scripts

| File | Role |
|------|------|
| `numpy_blis_reproducer.py` | NumPy GEMM `nan_euclidean` vs scalar loop |
| `run_numpy_blas_reproducer.sh` | NumPy-only mamba env |
| `build_and_run_c_blis_reproducer.sh` | Pure C `cblas_dgemm` + upstream BLIS 2.0 |
| `ci_probe_minimal_levels.sh` | Run all levels on BLIS (diagnostics) |

## CI

`.github/workflows/blis-macos-arm64-reproducer.yml` gates on `scalar-vs-imputer` for each `libblas` backend.
