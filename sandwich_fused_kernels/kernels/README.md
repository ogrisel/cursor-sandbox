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
| `xsimd_kernel.py` | C++/xsimd extension | `sandwich_xsimd` (optional native build) |

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
