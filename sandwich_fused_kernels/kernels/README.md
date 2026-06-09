# Sandwich kernels

| File | Backend | Entry point |
|---|---|---|
| `reference.py` | NumPy | `sandwich_reference` — exact reference |
| `numpy_baseline.py` | NumPy | `sandwich_numpy_einsum`, `sandwich_numpy_weighted_gram` |
| `tabmat_baseline.py` | tabmat (C++/xsimd) | `sandwich_tabmat` |
| `numba_kernels.py` | Numba | `sandwich_numba(..., variant=...)` |
| `jax_kernels.py` | JAX | `sandwich_jax(..., variant=...)` |
| **`helion_kernel.py`** | **Helion DSL** | **`sandwich_helion_eager`** (CPU ref tiles) |
| `helion_baseline.py` | Helion + PyTorch | NumPy wrappers for benchmark harness |
| `xsimd_kernel.py` | C++/xsimd extension | `sandwich_xsimd(..., block=, chunk_factor=)` |
| `tuned_kernels.py` | Autotuned dispatch | `sandwich_*_tuned` (reads `artifacts/autotune_cache.json`) |
| `triton_cpu_kernel.py` | triton-cpu (optional build) | `sandwich_triton_cpu_native`, `sandwich_torch_compile_triton_cpu` |

## Autotuned kernels

Run `autotune_sandwich.py` to populate `artifacts/autotune_cache.json`, then call e.g.
`sandwich_numba_blas_tuned(X, d, problem="glm_small", threading="multi", num_threads=4)` or
`sandwich_helion_tiled_tuned(X, d, problem="glm_small", threading="single")`.
Benchmark harness includes `*_tuned` variants when `--include-tuned` (default).

## Helion sandwich kernel

The Helion kernel lives in **`helion_kernel.py`**:

```python
@helion.kernel(autotune_effort="none", ref_mode=helion.RefMode.EAGER)
def sandwich_helion_eager(X: torch.Tensor, d: torch.Tensor) -> torch.Tensor:
    n, m = X.shape
    out = torch.zeros((m, m), dtype=X.dtype, device=X.device)
    for tile_i, tile_j in hl.tile([m, m]):
        acc = hl.zeros([tile_i, tile_j], dtype=X.dtype)
        for tile_k in hl.tile(n):
            w = d[tile_k]
            Xi = X[tile_k, tile_i]
            Xj = X[tile_k, tile_j]
            acc = acc + torch.einsum("ki,k,kj->ij", Xi, w, Xj)
        out[tile_i, tile_j] = acc
    return out
```

Use from NumPy benchmarks via `helion_baseline.sandwich_helion_eager(X, d)`.

Requires: `pip install torch helion packaging setuptools`
