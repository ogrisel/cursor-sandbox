# SIMD inspection report

| backend | variant | SIMD | AVX2 ymm | AVX512 zmm | SSE xmm | FMA | notes |
|---|---|---:|---:|---:|---:|---:|---|
| tabmat | dense.so_total | 921 | 0 | 0 | 921 | 0 | uses SSE128 xmm mulpd/addpd in micro-kernel |
| tabmat | dense_base_microkernel | 84 | 0 | 0 | 84 | 0 | uses SSE128 xmm mulpd/addpd in micro-kernel |
| tabmat | denseC_sandwich_omp | 0 | 0 | 0 | 0 | 0 | OpenMP row setup; scalar movsd in places |
| numba | k_inner | 82 | 35 | 0 | 47 | 0 | LLVM vector types in IR: 6; AVX2 ymm detected |
| numba | fused_blocked | 104 | 42 | 0 | 62 | 0 | LLVM vector types in IR: 51; AVX2 ymm detected |
| numba | blas_fused | 672 | 205 | 0 | 467 | 0 | LLVM vector types in IR: 304; AVX2 ymm detected |
| jax | einsum | 0 | 0 | 0 | 0 | 0 | fusion/thunk object is scalar or delegated to runtime |
| jax | scan_chunked | 0 | 0 | 0 | 0 | 0 | fusion/thunk object is scalar or delegated to runtime |
| numpy | openblas_dgemm | 845 | 670 | 0 | 175 | 455 | weighted Gram routes here; dgemm_kernel_HASWELL uses AVX2 vfmadd231pd |

## Key findings

- **tabmat** micro-kernel (`dense_base`) emits **SSE128 `mulpd`/`addpd`** (2-wide) with manual 4×4 unrolling.
- **Numba `k_inner`** and **`blas_fused`** emit **AVX2 `ymm`** (`vmulpd`, `vfmadd213pd`).
- **Numba `fused_blocked`** may vectorize inner loops but pays for `prange`/block overhead.
- **JAX `einsum` fusion** LLVM IR is **scalar-unrolled `fmul float`** for broadcast weighting.
- **NumPy/BLAS** `dgemm_kernel_HASWELL` uses **AVX2 FMA** (`vfmadd231pd ymm`).
- **JAX** fusion thunks are scalar LLVM; matmul SIMD is in XLA/Eigen runtime (not in dumped `.o`).
- **Numba `k_inner`**: LLVM emits **`vscatterqpd`** when `prange` vectorizes strided `out[i,j]` updates — SIMD hurts.