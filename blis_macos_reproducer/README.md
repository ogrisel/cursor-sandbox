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

## CI

`.github/workflows/blis-macos-arm64-reproducer.yml` runs on `macos-15` (arm64). Use **workflow_dispatch** to re-run experiments without pushing.

Expected outcomes while the BLIS bug is present:

- **NumPy + conda BLIS**: reproducer exits non-zero
- **NumPy + OpenBLAS / newaccelerate**: reproducer exits zero
- **Pure C + source BLIS**: reproducer exits non-zero
