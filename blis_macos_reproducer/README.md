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

## Files

| File | Role |
|------|------|
| `minimal_blis_reproducer.py` | Progressive minimal reproducer (all levels, self-contained) |
| `run_minimal_blas_reproducer.sh` | Create a mamba env for a backend + run one level |
| `ci_verify_minimal_reproducer.sh` | CI gate: BLIS must fail, openblas/newaccelerate must pass |
| `ci_probe_minimal_levels.sh` | Run every level on BLIS (diagnostics) |
| `build_and_run_c_blis_reproducer.sh` + `blis_gemm_reproducer.c` | Pure C `cblas_dgemm` against upstream BLIS 2.0 (microkernel control; passes) |

## CI

`.github/workflows/blis-macos-arm64-reproducer.yml`:

- `minimal-reproducer` (matrix `blis` / `openblas` / `newaccelerate`): gates `scalar-vs-imputer` — **fails** on BLIS, **passes** on openblas/newaccelerate.
- `minimal-level-probe-blis`: runs every level on BLIS for diagnostics.
- `pure-c-blis`: builds BLIS 2.0 and runs the C `dgemm` control.
