# macOS arm64 BLIS — `test_randomized_eigsh_reconst_low_rank` reproducer

Minimal reproducer for the macOS arm64 BLIS failure of
`sklearn/utils/tests/test_extmath.py::test_randomized_eigsh_reconst_low_rank`,
observed after [scikit-learn#34162](https://github.com/scikit-learn/scikit-learn/pull/34162#discussion_r3332644920)
flipped the conda `libblas` build to BLIS on macOS arm64.

The randomized eigendecomposition (`_randomized_eigsh`, built on
`randomized_svd` / `randomized_range_finder`) stops reconstructing an
exactly-low-rank PSD matrix to `decimal=6`. The whole pipeline is just BLAS GEMM
+ LAPACK QR / LU / SVD, so it reproduces with **NumPy + SciPy only**.

The failure has now been stripped further to a **single fixed-data GEMM**:

```text
C = (V @ diag(S)) @ V.T
```

where `V` is `100 x 10` and `S` has length `10`. The fixtures are stored as
plain ASCII files (`fixtures/V_100_10.txt`, `fixtures/S_100_10.txt`) whose first
line is `rows cols` followed by whitespace-separated double values, so they can
be parsed from C with `fscanf` and no external parser dependency.

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
- The **single fixed-data step** `V @ diag(S) @ V.T` reproduces on BLIS and passes
  on OpenBLAS when run from both Python and C (one `cblas_dgemm` call for the
  final multiply).
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

The full pipeline originally looked order / state dependent in-process, but
saving the exact `V` and `S` operands to disk makes the **single target GEMM**
fail in a fresh process with no prequel. Random small-inner-dimension GEMMs
(`numpy-gemm-min`) still pass, so the fixture values / layout are important, not
just the shape.

The smallest reproducer for BLIS maintainers is therefore the fixed-data C
program:

```bash
./blis_eigsh_reproducer/ci_minimal_gemm_c.sh blis      # expected FAIL
./blis_eigsh_reproducer/ci_minimal_gemm_c.sh openblas  # expected PASS
```

## Levels (largest → smallest sklearn surface)

| level | needs | what it runs |
| --- | --- | --- |
| `pytest` | scikit-learn, pytest | upstream `test_randomized_eigsh_reconst_low_rank` |
| `sklearn-eigsh` | scikit-learn | `sklearn.utils.extmath._randomized_eigsh` directly |
| `numpy-eigsh` | numpy, scipy | self-contained port of `_randomized_eigsh` (**primary gate**) |
| `numpy-kernels` | numpy, scipy | isolated `A@Q` (vs einsum) + LU/QR/SVD residuals on the initial data |
| `numpy-trace` | numpy, scipy | step-by-step pipeline trace; finds the first BLAS divergence |
| `minimal_gemm_repro.py` | numpy | fixed-data `V @ diag(S) @ V.T`; single variant fails on BLIS |
| `minimal_gemm_repro.c` | CBLAS | C fixed-data reproducer; parses ASCII fixtures with `fscanf` |
| `numpy-gemm-min` | numpy | pure-numpy small-inner-dim GEMM sequence (no scipy); does **not** repro |

`numpy-eigsh` loops over the upstream `(n, rank)` grid and fails as soon as one
case exceeds the `decimal=6` tolerance.

## Run locally

```bash
./blis_eigsh_reproducer/run_eigsh_blas_reproducer.sh blis     numpy-eigsh   # expected FAIL
./blis_eigsh_reproducer/run_eigsh_blas_reproducer.sh openblas numpy-eigsh   # expected PASS
./blis_eigsh_reproducer/run_eigsh_blas_reproducer.sh blis     numpy-kernels # localize primitive
./blis_eigsh_reproducer/ci_minimal_gemm_c.sh blis                           # fixed-data C repro
```

## CI

`.github/workflows/blis-eigsh-reproducer.yml`:

- `numpy-eigsh` matrix (`blis` / `openblas` / `newaccelerate`) — gate: BLIS must
  FAIL, others must PASS.
- `blis-localize-and-cross-level` — informational: localizes the broken
  primitive and runs all levels on BLIS to show identical reproduction.
- `trace-{blis,openblas}` — informational: full step-by-step pipeline trace.
- `minimal-gemm-c-{blis,openblas}` — fixed-data C reproducer, BLIS must FAIL and
  OpenBLAS must PASS.
- `minimal-gemm-{blis,openblas}` — fixed-data Python variants, including the
  single-step no-prequel reproducer.
- `gemm-min-{blis,openblas}` — informational: pure-numpy GEMM simplification
  attempt with random data (passes on both → arbitrary data is not enough).
- `blis-thread-sweep` — informational: documents the secondary `>=4`-thread
  deadlock with a timeout guard.
