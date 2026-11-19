# Iteration 02 — SIMD inspection and fused Numba rivals

## Goal

Check whether LLVM / XLA emit useful SIMD for fused sandwich loops, and whether tabmat-style Numba rivals can compete once bugs are fixed.

## Sources

| Piece | Link |
|---|---|
| SIMD inspector | [`inspect_simd.py`](https://github.com/ogrisel/cursor-sandbox/blob/cursor/sandwich-fused-kernels-000a/sandwich_fused_kernels/inspect_simd.py) |
| Inspection dump | [simd_inspection.json](simd_inspection.json) |
| Rival / fused Numba | [`kernels/numba_kernels.py`](https://github.com/ogrisel/cursor-sandbox/blob/cursor/sandwich-fused-kernels-000a/sandwich_fused_kernels/kernels/numba_kernels.py) |
| `rival_mt` | [`sandwich_numba_rival_mt`](https://github.com/ogrisel/cursor-sandbox/blob/cursor/sandwich-fused-kernels-000a/sandwich_fused_kernels/kernels/numba_kernels.py#L266-L269) |
| `blas_kchunk_mt` | [`_sandwich_kchunk_blas_impl`](https://github.com/ogrisel/cursor-sandbox/blob/cursor/sandwich-fused-kernels-000a/sandwich_fused_kernels/kernels/numba_kernels.py#L230-L258) |
| Thread pinning | [`threading_utils.py`](https://github.com/ogrisel/cursor-sandbox/blob/cursor/sandwich-fused-kernels-000a/sandwich_fused_kernels/threading_utils.py) |

## SIMD findings

| Backend | ISA | Useful for sandwich? |
|---|---|---|
| tabmat `dense_base` | SSE128 (`mulpd`/`addpd`) | **Yes** — hand-unrolled 4×4 |
| OpenBLAS / Numba BLAS | AVX2+FMA | **Yes** — via `dgemm` |
| Numba `fused_blocked` | AVX2 on block `acc` | Partial — not tabmat-level |
| Numba `k_inner` | AVX2 + **`vscatterqpd`** | **No** — scatter into `out[i,j]` |
| JAX fusion thunk | Scalar LLVM | No in fusion; matmul SIMD opaque in runtime |

## Rival kernel outcomes (glm_small MT, ~4 threads)

| Kernel | vs tabmat | Comment |
|---|---:|---|
| `rival_mt` / fused k-chunk | **~0.10×** | Algorithm ok; micro-kernel not |
| `blas_kchunk_mt` (untuned) | **~0.33×** | Best early Numba MT |
| `k_inner` | worse than fused_blocked | Rejected despite “having SIMD” |

## Bug fixed along the way

Off-diagonal blocks (`ib > jb`) were incorrectly skipped by a `gi > gj` filter meant only for diagonal blocks (symmetric flush). Fix lives in the Numba block accumulator path in [`numba_kernels.py`](https://github.com/ogrisel/cursor-sandbox/blob/cursor/sandwich-fused-kernels-000a/sandwich_fused_kernels/kernels/numba_kernels.py).

## Takeaway

**SIMD instructions ≠ performance.** Access pattern and reduction structure dominate. Pure fused Numba rivals validate tabmat’s *algorithm* but stay ~10× behind; BLAS delegation is the practical Numba path.
