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

## Where the corruption is (root-cause localization)

`numpy-trace` instruments **every** GEMM (vs a non-BLAS `einsum` reference) and
every LU/QR/SVD residual through the whole pipeline. On BLIS:

- Every GEMM in the power iterations / projection / SVD is **bit-exact**
  (`max_abs = 0.0` vs einsum), every factorization residual is `~1e-13`, and the
  singular values are normal (`max ≈ 141`).
- The **only** divergent step is the final reconstruction GEMM
  `(V @ diag(S)) @ V.T` (shape `(n,rank) @ (rank,n)`, i.e. small contraction
  dimension), which BLAS returns as `~1e+296` garbage while the einsum reference
  gives `~5e-14`.

It is **order / state dependent**: the trace that starts at `(100,10)` sees *no*
divergence, but iterating the full grid in order (so `(10,7)` runs first)
reproduces it at the `n=100` cases — exactly matching `numpy-eigsh` / `pytest`.

A pure-NumPy sequence of the same `(n,rank) @ (rank,n)` GEMMs with random data
(`numpy-gemm-min`, no SciPy / no SVD) does **not** reproduce it. So the bug
requires the SciPy/LAPACK SVD pipeline to set up the state, and then surfaces in
the next small-inner-dim GEMM. **The minimal reliable reproducer is therefore
NumPy + SciPy `_randomized_eigsh` (`numpy-eigsh`)**, not a bare GEMM.

## Levels (largest → smallest sklearn surface)

| level | needs | what it runs |
| --- | --- | --- |
| `pytest` | scikit-learn, pytest | upstream `test_randomized_eigsh_reconst_low_rank` |
| `sklearn-eigsh` | scikit-learn | `sklearn.utils.extmath._randomized_eigsh` directly |
| `numpy-eigsh` | numpy, scipy | self-contained port of `_randomized_eigsh` (**primary gate**) |
| `numpy-kernels` | numpy, scipy | isolated `A@Q` (vs einsum) + LU/QR/SVD residuals on the initial data |
| `numpy-trace` | numpy, scipy | step-by-step pipeline trace; finds the first BLAS divergence |
| `numpy-gemm-min` | numpy | pure-numpy small-inner-dim GEMM sequence (no scipy); does **not** repro |

`numpy-eigsh` loops over the upstream `(n, rank)` grid and fails as soon as one
case exceeds the `decimal=6` tolerance.

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
- `trace-{blis,openblas}` — informational: full step-by-step pipeline trace.
- `gemm-min-{blis,openblas}` — informational: pure-numpy GEMM simplification
  attempt (passes on both → bare GEMM is not enough).
- `blis-thread-sweep` — informational: documents the secondary `>=4`-thread
  deadlock with a timeout guard.
