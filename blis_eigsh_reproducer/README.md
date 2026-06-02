# macOS arm64 BLIS — `test_randomized_eigsh_reconst_low_rank` reproducer

Minimal reproducer for the macOS arm64 BLIS failure of
`sklearn/utils/tests/test_extmath.py::test_randomized_eigsh_reconst_low_rank`,
observed after [scikit-learn#34162](https://github.com/scikit-learn/scikit-learn/pull/34162#discussion_r3332644920)
flipped the conda `libblas` build to BLIS on macOS arm64.

The randomized eigendecomposition (`_randomized_eigsh`, built on
`randomized_svd` / `randomized_range_finder`) stops reconstructing an
exactly-low-rank PSD matrix to `decimal=6`. The whole pipeline is just BLAS GEMM
+ LAPACK QR / LU / SVD, so it reproduces with **NumPy + SciPy only**.

## Key findings (from CI on `macos-15`, conda `libblas 8_h886686a_blis`)

- The failure is a **catastrophic numerical corruption**, not a small rounding
  error: reconstruction error reaches `~1e+272` (`n=100, rank=10`) and `~1e+2`
  (`n=100, rank=80`). The other parametrized cases (`10-7`, `500-10`, `500-250`,
  `500-400`) pass.
- It is **deterministic and single-threaded**: it reproduces at
  `BLIS_NUM_THREADS=1` and `2`. The minimal reproducer therefore pins BLIS to a
  single thread for a clean, reproducible gate.
- A *separate* BLIS bug: with `BLIS_NUM_THREADS>=4` the same small matrices
  **deadlock** (hang). The `blis-thread-sweep` job documents this; the numerical
  corruption at 1–2 threads is the bug this reproducer targets.
- The NumPy+SciPy port is **bit-for-bit identical** to
  `sklearn._randomized_eigsh` on a non-buggy BLAS (Linux OpenBLAS:
  `max|ΔS| = max|Δ|V|| = 0`), and fails on the exact same `(n, rank)` cases as
  the upstream pytest on BLIS.

## Levels (largest → smallest sklearn surface)

| level | needs | what it runs |
| --- | --- | --- |
| `pytest` | scikit-learn, pytest | upstream `test_randomized_eigsh_reconst_low_rank` |
| `sklearn-eigsh` | scikit-learn | `sklearn.utils.extmath._randomized_eigsh` directly |
| `numpy-eigsh` | numpy, scipy | self-contained port of `_randomized_eigsh` (**primary gate**) |
| `numpy-kernels` | numpy, scipy | localizes the broken primitive: BLAS `A@Q` vs einsum, and LU/QR/SVD residuals |

`numpy-eigsh` and `numpy-kernels` loop over the failing-relevant `(n, rank)`
cases and fail as soon as one exceeds the `decimal=6` tolerance.

## Run locally

```bash
./blis_eigsh_reproducer/run_eigsh_blas_reproducer.sh blis     numpy-eigsh   # expected FAIL
./blis_eigsh_reproducer/run_eigsh_blas_reproducer.sh openblas numpy-eigsh   # expected PASS
./blis_eigsh_reproducer/run_eigsh_blas_reproducer.sh blis     numpy-kernels # localize primitive
```

## CI

`.github/workflows/blis-eigsh-reproducer.yml`:

- `numpy-eigsh` matrix (`blis` / `openblas` / `newaccelerate`) — gate: BLIS must
  FAIL, others must PASS.
- `blis-localize-and-cross-level` — informational: localizes the broken
  primitive and runs all levels on BLIS to show identical reproduction.
- `blis-thread-sweep` — informational: documents the secondary `>=4`-thread
  deadlock with a timeout guard.
