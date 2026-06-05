# Sandwich product fused kernels (CPU)

Pure-Python exploration of fused `X.T @ diag(d) @ X` kernels on CPU, comparing **NumPy**, **tabmat**, **Numba**, and **JAX** backends.

## High-level objective

The sandwich (Gram) product `X.T @ diag(d) @ X` is a hot path in weighted least squares and GLM Hessians. [tabmat](https://github.com/Quantco/tabmat) implements a heavily optimized C++/Cython kernel (blocked, SIMD, OpenMP). This subfolder asks:

> Can pure Python compilers (Numba, JAX) reach similar performance without custom C extensions?

We benchmark latency, profile hot paths, and compare memory behavior against:

1. Naive NumPy baselines (`einsum`, explicit `diag`, weighted Gram)
2. tabmat `DenseMatrix.sandwich` (strong baseline)

## Implementation plan

| Phase | Status | Description |
|---|---|---|
| 1. Reference + baselines | done | `kernels/reference.py`, `numpy_baseline.py`, `tabmat_baseline.py` |
| 2. Compiler kernels | done | Numba fused loops + BLAS delegation; JAX `einsum` / `tensordot` / weighted Gram |
| 3. Benchmark harness | done | `benchmark_sandwich.py` — timing, RSS, tracemalloc, correctness |
| 4. Memory analysis | done | `profile_memory.py` — theoretical vs observed temporaries |
| 5. Iterative tuning | done | Three benchmark iterations (see log below) |

### Kernel families

- **NumPy**: `diag` matmul (materializes `diag(d)`), `einsum`, weighted Gram `(X*d).T @ X`
- **tabmat**: `DenseMatrix.sandwich` (C++ GotoBLAS-style blocked SIMD)
- **Numba**:
  - `serial` / `parallel` / `blocked` — fused scalar triple loops
  - `k_parallel` — row-block partials (race-free reduction)
  - `blas_fused` — single BLAS call on weighted `X`
  - `blas_chunked` — parallel row chunks + BLAS per chunk
- **JAX**: JIT `einsum`, `tensordot`, `weighted_gram`

## Running benchmarks

From the repo root:

```bash
uv run --python 3.11 --exclude-newer P7D \
  --with tabmat --with numba --with jax --with jaxlib --with psutil --with matplotlib \
  python hgbdt_performance_analysis/sandwich_fused_kernels/benchmark_sandwich.py \
  --repeats 5 --warmup 2
```

Memory profile (140k × 80 default):

```bash
uv run --python 3.11 --exclude-newer P7D \
  --with tabmat --with numba --with jax --with jaxlib --with psutil \
  python hgbdt_performance_analysis/sandwich_fused_kernels/profile_memory.py
```

Artifacts land in `artifacts/` (`benchmark_results.json`, `benchmark_report.md`, cProfile traces, memory JSON).

## Experimental log

### Iteration 1 — initial fused loops

- Numba `blocked` failed to compile (`prange` non-constant step); fixed with block-index loops.
- JAX `vmap_cols` allocated `O(m³)` workspace and OOM'd; removed.
- **Finding**: scalar fused Numba loops are 15–50× slower than NumPy/tabmat. tabmat leads on all shapes.

### Iteration 2 — BLAS delegation + race fixes

- Added `numba_blas_chunked`; fixed `k_parallel` races via per-chunk partial matrices.
- `blas_chunked` helped on tall/skinny shapes but regressed elsewhere due to chunk allocation overhead.
- **Finding**: JAX `tensordot` reached ~0.24× tabmat latency on `glm_small` while beating `numpy_einsum` by ~1.5×.

### Iteration 3 — final comparison (5 repeats, 2 warmup)

Machine: linux-amd64, 4 cores, Python 3.11, tabmat 4.2.1, numba 0.65.1, jax 0.10.1.

| Problem | Shape | tabmat (ms) | Best compiler | Best compiler (ms) | vs tabmat | vs numpy_einsum |
|---|---|---:|---|---:|---:|---:|
| glm_small | 50k × 40 f64 | 2.28 | jax_tensordot | 8.35 | 0.27× | 1.77× |
| glm_medium | 140k × 80 f64 | 17.81 | numpy_weighted_gram | 72.46 | 0.25× | 1.03× |
| glm_tall_skinny | 320k × 32 f64 | 18.24 | numba_blas_chunked | 65.31 | 0.28× | 1.16× |
| glm_square_cols | 80k × 120 f64 | 21.68 | numba_blas_chunked | 83.53 | 0.26× | 1.15× |
| glm_small_f32 | 50k × 40 f32 | 1.55 | numba_blas_fused | 11.25 | 0.14× | 1.62× |

#### Analysis

1. **tabmat remains the ceiling** (≈4–12× faster than NumPy `einsum` on these shapes). Its advantage comes from fused blocked micro-kernels with xsimd + OpenMP, avoiding both `diag(d)` and full weighted-`X` materialization.
2. **Pure fused Numba loops do not vectorize** to competitive code on this hardware; `blocked`/`parallel` variants are order-of-magnitude slower than BLAS-backed routes.
3. **BLAS-backed compiler paths** (`numba_blas_fused`, `jax_tensordot`) track NumPy weighted Gram but do not close the gap to tabmat because they still materialize an `n×m` weighted matrix (~85 MB for glm_medium f64).
4. **JAX** gives the best compiler speedups on smaller f64 problems (≈1.7× over `einsum`) via XLA fusion, but CPU XLA still trails tabmat by ~4×.
5. **Memory**: tabmat and `numpy_einsum` add negligible RSS; weighted Gram / JAX tensordot require an `n×m` scratch buffer; `numpy_diag_matmul` would need `O(n²)` if `diag(d)` were fully formed.

Full per-kernel tables: `artifacts/benchmark_report.md`.

## Best performance achieved so far

| Metric | Result |
|---|---|
| **Overall fastest** | tabmat — 1.55 ms (`glm_small_f32`, 50k×40) |
| **Best pure-Python compiler** | `jax_tensordot` — 8.35 ms on `glm_small` (**3.7× tabmat**, **1.77× numpy_einsum**) |
| **Best Numba variant** | `numba_k_parallel` on `glm_small` (12.96 ms); `numba_blas_fused` on `glm_small_f32` (11.25 ms) |
| **Closest to tabmat** | ~0.27–0.28× tabmat wall time (JAX/Numba BLAS paths on 50k×40 and 320k×32) |

**Conclusion:** Pure Python compilers can beat naive NumPy `einsum` by fusing the row weights into BLAS or XLA graphs, but matching tabmat on CPU requires hand-tuned blocked SIMD kernels (or calling tabmat). The recommended compiler-backed fallback is **`jax.jit` + `tensordot`** for smaller dense problems and **`numpy`/`numba` weighted Gram** for larger ones until a native fused kernel is available.

## Layout

```
sandwich_fused_kernels/
├── README.md
├── benchmark_sandwich.py
├── profile_memory.py
├── kernels/
│   ├── reference.py
│   ├── numpy_baseline.py
│   ├── tabmat_baseline.py
│   ├── numba_kernels.py
│   └── jax_kernels.py
└── artifacts/
    ├── benchmark_results.json
    ├── benchmark_report.md
    ├── memory_profile_float64.json
    └── profile_*.txt
```
