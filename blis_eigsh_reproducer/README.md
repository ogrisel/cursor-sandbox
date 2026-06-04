# macOS arm64 BLIS fixed-data GEMM reproducer

Minimal fixed-data reproducer for the BLIS corruption behind the
`sklearn/utils/tests/test_extmath.py::test_randomized_eigsh_reconst_low_rank`
failure observed after [scikit-learn#34162](https://github.com/scikit-learn/scikit-learn/pull/34162#discussion_r3332644920)
flipped the conda `libblas` build to BLIS on macOS arm64.

The original expression is:

```text
C = (V @ diag(S)) @ V.T
```

`V` is `100 x 10` and `S` has length `10`. The first operation
`V @ diag(S)` is not faulty and is eliminated: both reproducers form `V * S`
by direct column scaling. The only BLAS call is therefore the second/final GEMM:

```text
C = (V * S) @ V.T
```

with shape `(100, 10) @ (10, 100)`.

## Fixed data format

The fixtures are plain ASCII files:

- `fixtures/V_100_10.txt`
- `fixtures/S_100_10.txt`

Format:

```text
rows cols
value_00 value_01 ...
...
```

Values are row-major decimal `double` literals. The C program parses them with
`fscanf` and has no external parser dependency.

## Reproducers

- `minimal_gemm_repro.py`: Python/NumPy version, forms `V * S` by broadcasting,
  then compares the single BLAS-backed `@` against a non-BLAS `einsum` reference.
- `minimal_gemm_repro.c`: C/CBLAS version, forms `V * S` by column scaling and
  calls one `cblas_dgemm` for `(V * S) @ V.T`; compares against a simple triple
  loop reference.

On macOS arm64 with conda-forge BLIS (`libblas 8_h886686a_blis`), both
reproducers return catastrophic garbage (`~8e+272` or larger). OpenBLAS and
newaccelerate pass.

## BLAS architecture reported by threadpoolctl

The CI wrappers print:

```bash
python -m threadpoolctl -i numpy
```

Latest run checked: `26963580867`.

| backend | conda `libblas` build | threadpoolctl `internal_api` | version | threading | architecture |
| --- | --- | --- | --- | --- | --- |
| BLIS | `8_h886686a_blis` | `blis` | `2.0` | `pthreads` | `firestorm` |
| OpenBLAS | `8_h51639a9_openblas` | `openblas` | `0.3.33` | `openmp` | `VORTEX` |
| newaccelerate | `8_h280a802_newaccelerate` | not reported (`[]`) | - | - | - |

The BLIS `firestorm` path reproduces the corruption; OpenBLAS `VORTEX` and
newaccelerate pass.

## Run locally

```bash
./blis_eigsh_reproducer/ci_minimal_gemm_python.sh blis      # expected FAIL
./blis_eigsh_reproducer/ci_minimal_gemm_python.sh openblas  # expected PASS
./blis_eigsh_reproducer/ci_minimal_gemm_c.sh blis           # expected FAIL
./blis_eigsh_reproducer/ci_minimal_gemm_c.sh openblas       # expected PASS
```

## CI

`.github/workflows/blis-eigsh-reproducer.yml`:

- `python-fixed-data-{blis,openblas,newaccelerate}`
- `c-fixed-data-{blis,openblas,newaccelerate}`

The BLIS jobs are expected to fail internally and are inverted by the wrappers;
OpenBLAS and newaccelerate must pass. Each job prints the `threadpoolctl` report
before running the reproducer.
