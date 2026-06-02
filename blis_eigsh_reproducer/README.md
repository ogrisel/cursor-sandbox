# macOS arm64 BLIS — `test_randomized_eigsh_reconst_low_rank` reproducer

Minimal reproducer for the macOS arm64 BLIS failure of
`sklearn/utils/tests/test_extmath.py::test_randomized_eigsh_reconst_low_rank`,
observed after [scikit-learn#34162](https://github.com/scikit-learn/scikit-learn/pull/34162#discussion_r3332644920)
flipped the conda `libblas` build to BLIS on macOS arm64.

The randomized eigendecomposition (`_randomized_eigsh`, built on
`randomized_svd` / `randomized_range_finder`) stops reconstructing an
exactly-low-rank PSD matrix to `decimal=6`. The whole pipeline is just
BLAS GEMM + LAPACK QR / LU / SVD, so it can be reproduced with **NumPy + SciPy
only**.

## Levels (largest → smallest sklearn surface)

| level | needs | what it runs |
| --- | --- | --- |
| `pytest` | scikit-learn, pytest | upstream `test_randomized_eigsh_reconst_low_rank` |
| `sklearn-eigsh` | scikit-learn | `sklearn.utils.extmath._randomized_eigsh` directly |
| `numpy-eigsh` | numpy, scipy | self-contained port of `_randomized_eigsh` (**primary gate**) |

Every level loops over the upstream `(n, rank)` grid
`(10,7) (100,10) (100,80) (500,10) (500,250) (500,400)` and fails as soon as one
case exceeds the `decimal=6` reconstruction tolerance.

`numpy-eigsh` is bit-for-bit identical to `sklearn._randomized_eigsh` on a
non-buggy BLAS (verified on Linux OpenBLAS: `max|ΔS| = max|Δ|V|| = 0`).

## Run locally

```bash
./blis_eigsh_reproducer/run_eigsh_blas_reproducer.sh blis     numpy-eigsh   # expected FAIL
./blis_eigsh_reproducer/run_eigsh_blas_reproducer.sh openblas numpy-eigsh   # expected PASS
```

Threading: BLIS must run multi-threaded (`BLIS_NUM_THREADS=8`); do not pin to a
single thread.

## CI

`.github/workflows/blis-eigsh-reproducer.yml`:

- `numpy-eigsh` matrix (`blis` / `openblas` / `newaccelerate`) — gate: BLIS must
  FAIL, others must PASS.
- `eigsh-level-probe-blis` — informational, runs all three levels on BLIS in one
  job to compare error magnitudes and drive further simplification.
