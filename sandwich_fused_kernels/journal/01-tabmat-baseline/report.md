# Iteration 01 — Tabmat baseline and root causes

## Goal

Establish a reproducible sandwich-product benchmark against tabmat and isolate *why* naive NumPy / compiler paths lose.

## Sources

| Piece | Link |
|---|---|
| Analysis script | [`analyze_tabmat.py`](https://github.com/ogrisel/cursor-sandbox/blob/cursor/sandwich-fused-kernels-000a/sandwich_fused_kernels/analyze_tabmat.py) |
| tabmat wrapper | [`kernels/tabmat_baseline.py`](https://github.com/ogrisel/cursor-sandbox/blob/cursor/sandwich-fused-kernels-000a/sandwich_fused_kernels/kernels/tabmat_baseline.py) |
| NumPy baselines | [`kernels/numpy_baseline.py`](https://github.com/ogrisel/cursor-sandbox/blob/cursor/sandwich-fused-kernels-000a/sandwich_fused_kernels/kernels/numpy_baseline.py#L25-L50) |
| JAX baselines | [`kernels/jax_kernels.py`](https://github.com/ogrisel/cursor-sandbox/blob/cursor/sandwich-fused-kernels-000a/sandwich_fused_kernels/kernels/jax_kernels.py) |
| Advantage JSON | [tabmat_advantage_analysis.json](tabmat_advantage_analysis.json) |

## Root causes (glm_small 50k×40 f64)

| Cause | tabmat | Typical NumPy / compiler path |
|---|---|---|
| Fused row weights | `d[k]` inside SIMD-blocked `k` loop | Materializes weighted `n×m` scratch |
| Specialized kernel | Direct sandwich micro-kernel | Generic `dgemm` / `einsum` |
| Cache / SIMD blocking | GotoBLAS-style 4×4 + xsimd | Scalar or wide GEMM with poor reuse |
| Symmetric structure | Lower-triangle then mirror | Full matrix |
| Memory traffic | ~0 extra RSS beyond `X` + output | 1–2× read/write of weighted rows |

On the analysis run, tabmat (~2 ms) was **~5–7.5×** faster than the best early compiler paths and **~7.5×** faster than `numpy.einsum`.

## Early baseline performance (order-of-magnitude)

Before autotuning / Triton work:

| Backend | Typical vs tabmat (MT) | Notes |
|---|---:|---|
| `numpy_einsum` | ~0.2× | Clear, slow |
| `jax_einsum` | ~0.2× | XLA fuses weights; still generic |
| Numba BLAS single GEMM | ~0.2× | Delegates to OpenBLAS |
| Numba fused blocked | ~0.1× | Correct algorithm, weak micro-kernel |

## Takeaway

Closing the tabmat gap needs either a **native fused SIMD kernel** or a **BLAS-backed chunked** path with careful threading — expressing the math in Python alone is not enough.
