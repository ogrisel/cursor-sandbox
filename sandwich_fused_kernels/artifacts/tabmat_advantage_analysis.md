# tabmat advantage analysis

Problem: 50000 x 40 float64

| kernel | median (ms) | vs tabmat | trace peak (MB) | weighted-X | BLAS | fused-k |
|---|---:|---:|---:|---|---|---|
| tabmat | 2.08 | 1.00x | 0.2 | False | False | True |
| jax_einsum | 11.08 | 0.19x | 23.8 | False | False | True |
| jax_scan_chunked | 13.40 | 0.16x | 23.8 | False | True | False |
| numpy_weighted_gram | 15.06 | 0.14x | 31.3 | True | True | False |
| numpy_einsum | 15.53 | 0.13x | 31.3 | False | False | True |
| numba_fused_blocked | 20.36 | 0.10x | 16.0 | False | False | True |
| numba_blas_tiled | 49.75 | 0.04x | 18.6 | True | True | False |

## Interpreted causes

1. **Fused k-loop without n×m scratch**: tabmat multiplies `d[k]` inside SIMD-blocked micro-kernels.
2. **No BLAS GEMM dispatch overhead**: tabmat calls a specialized sandwich kernel, not generic `dgemm`.
3. **Cache/SIMD blocking**: GotoBLAS-style 4×4 blocks with xsimd on the inner `k` dimension.
4. **Symmetric write pattern**: tabmat accumulates lower-triangle blocks then mirrors.
5. **Memory traffic**: weighted-Gram paths read/write an extra `n×m` buffer (~15.3 MB here).