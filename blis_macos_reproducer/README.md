# BLIS macOS arm64 minimal reproducers

Minimal reproducers for macOS arm64 BLAS regressions seen when conda-forge switched the default `libblas` implementation to BLIS (see [scikit-learn#34162 discussion](https://github.com/scikit-learn/scikit-learn/pull/34162#discussion_r3332644920)).

The NumPy reproducer ports `sklearn.metrics.pairwise.nan_euclidean_distances` using only NumPy (the code path behind failing `KNNImputer` tests on macOS arm64 with conda-forge BLIS). It compares GEMM-based distance matrices (`X @ X.T` and related products) against a scalar reference loop on fixed inputs from `sklearn/impute/tests/test_knn.py`.

## Contents

| File | Role |
|------|------|
| `numpy_blis_reproducer.py` | NumPy-only check (no SciPy) |
| `blis_gemm_reproducer.c` | Pure C `cblas_dgemm` vs long-double reference |
| `run_numpy_blas_reproducer.sh` | Creates a mamba env and runs the Python reproducer |
| `build_and_run_c_blis_reproducer.sh` | Builds upstream BLIS from source and runs the C reproducer |
| `ci_verify_numpy_reproducer.sh` | CI helper: BLIS must fail, other backends must pass |
| `sklearn_knn_blis_reproducer.py` | Runs failing `pytest` KNN imputer tests via conda sklearn |
| `sklearn_pairwise_blis_reproducer.py` | sklearn `nan_euclidean` / chunked / `KNNImputer` vs scalar reference |
| `run_sklearn_blas_reproducer.sh` | Mamba env with scikit-learn + chosen `libblas` |
| `ci_verify_sklearn_reproducer.sh` | CI helper for sklearn reproducers |

Threading note: for BLIS reproducers we **do not** set `OMP_NUM_THREADS=1` (that masked the bug). Use `BLIS_NUM_THREADS=8` like sklearn macOS CI.

## Local runs (macOS arm64)

Create one env per BLAS backend (recreate when switching):

```bash
mamba create -y -n blis-repro numpy "libblas=*=*_blis"
./blis_macos_reproducer/run_numpy_blas_reproducer.sh blis

mamba create -y -n blis-repro numpy "libblas=*=*_openblas"
./blis_macos_reproducer/run_numpy_blas_reproducer.sh openblas

mamba create -y -n blis-repro numpy "libblas=*=*_newaccelerate"
./blis_macos_reproducer/run_numpy_blas_reproducer.sh newaccelerate
```

Pure C reproducer (links against BLIS built from the latest release tag):

```bash
./blis_macos_reproducer/build_and_run_c_blis_reproducer.sh
```

Definitive reproducer (matches scikit-learn macOS CI):

```bash
./blis_macos_reproducer/run_sklearn_blas_reproducer.sh blis pytest
./blis_macos_reproducer/run_sklearn_blas_reproducer.sh openblas pytest   # should pass
```

Optional diagnostic (`sklearn_pairwise_blis_reproducer.py`): compares `nan_euclidean` implementations to a scalar reference.

## CI

`.github/workflows/blis-macos-arm64-reproducer.yml` runs on `macos-15` (arm64). Use **workflow_dispatch** to re-run experiments without pushing.

Expected outcomes while the BLIS bug is present:

- **`run_sklearn_blas_reproducer.sh blis pytest`**: KNN imputer tests fail (primary reproducer)
- **`run_sklearn_blas_reproducer.sh blis pairwise`**: chunked vs full `pairwise_distances` diverge on the 8×4 case
- **NumPy + OpenBLAS / newaccelerate**: reproducers pass
- **Pure C + source BLIS 2.0**: isolated `dgemm` micro-kernel passes (bug is in sklearn calling pattern, not this kernel)
