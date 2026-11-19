# Iteration 03 — Chunk / tile autotuning

## Goal

Treat block size, row-chunk count, and Helion/PyTorch tiles as searchable hyperparameters so compiler / native kernels can beat untuned defaults (and, where possible, tabmat MT).

## Sources

| Piece | Link |
|---|---|
| Autotuner | [`autotune_sandwich.py`](https://github.com/ogrisel/cursor-sandbox/blob/cursor/sandwich-fused-kernels-000a/sandwich_fused_kernels/autotune_sandwich.py) |
| Param cache helpers | [`autotune_config.py`](https://github.com/ogrisel/cursor-sandbox/blob/cursor/sandwich-fused-kernels-000a/sandwich_fused_kernels/autotune_config.py) |
| Tuned dispatch | [`kernels/tuned_kernels.py`](https://github.com/ogrisel/cursor-sandbox/blob/cursor/sandwich-fused-kernels-000a/sandwich_fused_kernels/kernels/tuned_kernels.py) |
| Autotune results | [autotune_results.json](autotune_results.json) |
| Cache | [`artifacts/autotune_cache.json`](https://github.com/ogrisel/cursor-sandbox/blob/cursor/sandwich-fused-kernels-000a/sandwich_fused_kernels/artifacts/autotune_cache.json) |
| xsimd extension | [`xsimd_ext/sandwich_xsimd.cpp`](https://github.com/ogrisel/cursor-sandbox/blob/cursor/sandwich-fused-kernels-000a/sandwich_fused_kernels/xsimd_ext/sandwich_xsimd.cpp) |

## Families tuned

| Family | Tunables | Kernel entry |
|---|---|---|
| `numba_blas_mt` | `n_chunks` | [`sandwich_numba_blas_tuned`](https://github.com/ogrisel/cursor-sandbox/blob/cursor/sandwich-fused-kernels-000a/sandwich_fused_kernels/kernels/tuned_kernels.py#L87-L104) |
| `numba_fused_mt` | `block`, `n_chunks` | [`sandwich_numba_fused_tuned`](https://github.com/ogrisel/cursor-sandbox/blob/cursor/sandwich-fused-kernels-000a/sandwich_fused_kernels/kernels/tuned_kernels.py#L65-L84) |
| `xsimd_mt` | `block`, `chunk_factor` | [`sandwich_xsimd_tuned`](https://github.com/ogrisel/cursor-sandbox/blob/cursor/sandwich-fused-kernels-000a/sandwich_fused_kernels/kernels/tuned_kernels.py#L145-L166) |
| `helion_tiled` / `torch_tiled` | `tile_m/n/k` | [`sandwich_helion_tiled_tuned`](https://github.com/ogrisel/cursor-sandbox/blob/cursor/sandwich-fused-kernels-000a/sandwich_fused_kernels/kernels/tuned_kernels.py#L173-L190) |
| `triton_cpu_mt` | `chunk`, `block_m/k`, `n_chunks` | [`sandwich_triton_cpu_tuned`](https://github.com/ogrisel/cursor-sandbox/blob/cursor/sandwich-fused-kernels-000a/sandwich_fused_kernels/kernels/tuned_kernels.py#L222-L247) |
| `torch_compile_triton_mt` | tiles | [`sandwich_torch_compile_triton_tuned`](https://github.com/ogrisel/cursor-sandbox/blob/cursor/sandwich-fused-kernels-000a/sandwich_fused_kernels/kernels/tuned_kernels.py#L250-L273) |

## Headline MT results after Numba/xsimd tune (earlier sweep)

| Problem | tabmat | Best tuned | vs tabmat |
|---|---:|---|---:|
| glm_small f64 | 2.32 ms | **numba_blas_tuned** 1.73 ms | **1.35×** |
| glm_medium f64 | 18.36 ms | **numba_blas_tuned** 10.10 ms | **1.82×** |
| glm_tall_skinny f64 | 11.91 ms | **numba_blas_tuned** 6.02 ms | **1.98×** |
| glm_square_cols f64 | 20.50 ms | **numba_blas_tuned** 11.76 ms | **1.74×** |

Often-winning recipe: **many small row chunks** (`n_chunks≈128`) with **single-thread GEMM per OpenMP worker** (`blas_threads=1`) to avoid oversubscription.

## Helion / Torch tile ST (selected)

| Problem | Best tiled vs tabmat |
|---|---:|
| glm_tall_skinny f64 | **~3.4×** (`torch_tiled_tuned`) |
| glm_medium f64 | **~1.6×** (`helion_tiled_tuned`) |

Large output tiles (32×32 / 64×64) + large row tiles cut interpreter overhead vs eager Helion.

## Takeaway

Autotuning is a **meta-complexity** tax (~offline search + per-shape cache) but is what turns “mediocre” BLAS/xsimd/torch paths into **tabmat-beating** ones on these GLM shapes. Fused Numba still does not catch up even after tile search.
