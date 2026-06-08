# Sandwich benchmark report (multi-threaded)

Threading: **multi** (4 threads)

## glm_small

| kernel | median (ms) | vs numpy_einsum | vs tabmat | peak RSS Δ (MB) | max rel err |
|---|---:|---:|---:|---:|---:|
| numba_blas_tuned | 2.40 | 5.90x | 1.04x | 0.00 | 4.57e-13 |
| tabmat | 2.50 | 5.66x | 1.00x | 0.00 | 5.19e-13 |
| xsimd_tuned | 3.33 | 4.24x | 0.75x | 0.00 | 9.00e-13 |
| torch_einsum | 6.45 | 2.19x | 0.39x | 0.00 | 1.83e-13 |
| numba_blas_kchunk_mt | 9.26 | 1.53x | 0.27x | 5.92 | 3.24e-13 |
| numba_blas_tiled | 9.52 | 1.48x | 0.26x | 0.00 | 4.92e-13 |
| torch_compile_einsum | 9.81 | 1.44x | 0.25x | 0.09 | 4.52e-13 |
| helion_eager | 10.95 | 1.29x | 0.23x | 0.00 | 1.83e-13 |
| numba_blas_fused | 11.98 | 1.18x | 0.21x | 0.00 | 0.00e+00 |
| jax_einsum | 12.64 | 1.12x | 0.20x | 0.00 | 7.23e-05 |
| numpy_weighted_gram | 13.31 | 1.06x | 0.19x | 0.00 | 0.00e+00 |
| numpy_einsum | 14.13 | 1.00x | 0.18x | 0.00 | 0.00e+00 |
| numba_fused_tuned | 14.28 | 0.99x | 0.17x | 0.00 | 3.26e-13 |
| torch_compile_tiled_tuned | 14.57 | 0.97x | 0.17x | 0.00 | 4.52e-13 |
| jax_chunked_tuned | 15.31 | 0.92x | 0.16x | 0.65 | 1.55e-04 |
| numba_jblock_tuned | 17.16 | 0.82x | 0.15x | 0.00 | 1.66e-12 |
| torch_tiled_tuned | 19.06 | 0.74x | 0.13x | 0.00 | 1.83e-13 |
| numba_tabmat_style_mt | 23.74 | 0.60x | 0.11x | 0.00 | 1.66e-12 |
| numba_k_chunk_tabmat | 27.98 | 0.51x | 0.09x | 0.00 | 9.00e-13 |
| numba_fused_blocked | 32.45 | 0.44x | 0.08x | 0.00 | 1.62e-12 |
| helion_tiled_tuned | 35.21 | 0.40x | 0.07x | 0.00 | 4.64e-13 |
| numba_rival_mt | 41.04 | 0.34x | 0.06x | 0.00 | 9.00e-13 |

Best: **numba_blas_tuned** (2.40 ms). tabmat: 2.50 ms (1.04x vs best).

## glm_medium

| kernel | median (ms) | vs numpy_einsum | vs tabmat | peak RSS Δ (MB) | max rel err |
|---|---:|---:|---:|---:|---:|
| numba_blas_tuned | 12.23 | 8.40x | 1.78x | 0.00 | 3.01e-12 |
| tabmat | 21.80 | 4.71x | 1.00x | 0.07 | 4.18e-12 |
| xsimd_tuned | 25.05 | 4.10x | 0.87x | 0.00 | 7.72e-12 |
| torch_compile_einsum | 49.27 | 2.08x | 0.44x | 0.15 | 2.90e-12 |
| torch_einsum | 49.40 | 2.08x | 0.44x | 0.00 | 2.90e-12 |
| numba_blas_tiled | 58.40 | 1.76x | 0.37x | 0.00 | 1.03e-12 |
| numba_blas_kchunk_mt | 63.90 | 1.61x | 0.34x | 37.11 | 1.67e-12 |
| helion_eager | 78.17 | 1.31x | 0.28x | 0.00 | 2.90e-12 |
| torch_compile_tiled_tuned | 86.91 | 1.18x | 0.25x | 0.00 | 1.94e-12 |
| numba_fused_tuned | 93.25 | 1.10x | 0.23x | 0.00 | 7.72e-12 |
| numpy_weighted_gram | 101.62 | 1.01x | 0.21x | 0.00 | 0.00e+00 |
| numpy_einsum | 102.71 | 1.00x | 0.21x | 0.00 | 0.00e+00 |
| numba_blas_fused | 111.20 | 0.92x | 0.20x | 0.01 | 0.00e+00 |
| jax_chunked_tuned | 117.00 | 0.88x | 0.19x | 42.71 | 1.79e-03 |
| jax_einsum | 122.40 | 0.84x | 0.18x | 42.81 | 1.35e-03 |
| helion_tiled_tuned | 125.67 | 0.82x | 0.17x | 0.00 | 2.52e-12 |
| numba_jblock_tuned | 126.84 | 0.81x | 0.17x | 0.00 | 1.74e-11 |
| numba_fused_blocked | 179.40 | 0.57x | 0.12x | 0.00 | 1.45e-11 |
| torch_tiled_tuned | 214.38 | 0.48x | 0.10x | 0.00 | 4.13e-12 |
| numba_tabmat_style_mt | 224.96 | 0.46x | 0.10x | 0.00 | 1.74e-11 |
| numba_k_chunk_tabmat | 276.27 | 0.37x | 0.08x | 0.00 | 1.55e-11 |
| numba_rival_mt | 284.03 | 0.36x | 0.08x | 0.00 | 1.55e-11 |

Best: **numba_blas_tuned** (12.23 ms). tabmat: 21.80 ms (1.78x vs best).

## glm_tall_skinny

| kernel | median (ms) | vs numpy_einsum | vs tabmat | peak RSS Δ (MB) | max rel err |
|---|---:|---:|---:|---:|---:|
| numba_blas_tuned | 6.40 | 14.39x | 1.81x | 0.00 | 5.83e-13 |
| xsimd_tuned | 9.83 | 9.37x | 1.18x | 0.00 | 7.83e-13 |
| tabmat | 11.56 | 7.97x | 1.00x | 0.00 | 4.14e-13 |
| torch_compile_tiled_tuned | 29.60 | 3.11x | 0.39x | 0.00 | 4.45e-13 |
| torch_einsum | 31.41 | 2.93x | 0.37x | 0.00 | 4.32e-13 |
| torch_compile_einsum | 31.60 | 2.91x | 0.37x | 0.22 | 4.32e-13 |
| torch_tiled_tuned | 35.80 | 2.57x | 0.32x | 0.00 | 6.10e-13 |
| numba_fused_tuned | 36.79 | 2.50x | 0.31x | 0.00 | 7.83e-13 |
| helion_tiled_tuned | 40.42 | 2.28x | 0.29x | 0.00 | 6.10e-13 |
| numba_blas_tiled | 44.95 | 2.05x | 0.26x | 0.00 | 5.12e-13 |
| numba_blas_kchunk_mt | 47.86 | 1.92x | 0.24x | 0.00 | 3.65e-13 |
| helion_eager | 55.56 | 1.66x | 0.21x | 0.00 | 4.32e-13 |
| numba_jblock_tuned | 66.69 | 1.38x | 0.17x | 0.00 | 1.75e-12 |
| numba_blas_fused | 88.39 | 1.04x | 0.13x | 0.00 | 0.00e+00 |
| numpy_weighted_gram | 90.80 | 1.01x | 0.13x | 0.00 | 0.00e+00 |
| numpy_einsum | 92.12 | 1.00x | 0.13x | 0.00 | 0.00e+00 |
| jax_chunked_tuned | 93.32 | 0.99x | 0.12x | 38.97 | 1.00e-04 |
| jax_einsum | 96.58 | 0.95x | 0.12x | 39.21 | 1.96e-04 |
| numba_rival_mt | 104.45 | 0.88x | 0.11x | 0.00 | 7.83e-13 |
| numba_tabmat_style_mt | 106.44 | 0.87x | 0.11x | 0.00 | 1.75e-12 |
| numba_k_chunk_tabmat | 106.96 | 0.86x | 0.11x | 0.00 | 7.83e-13 |
| numba_fused_blocked | 138.94 | 0.66x | 0.08x | 0.00 | 1.68e-12 |

Best: **numba_blas_tuned** (6.40 ms). tabmat: 11.56 ms (1.81x vs best).

## glm_square_cols

| kernel | median (ms) | vs numpy_einsum | vs tabmat | peak RSS Δ (MB) | max rel err |
|---|---:|---:|---:|---:|---:|
| numba_blas_tuned | 12.34 | 6.07x | 1.69x | 0.00 | 2.59e-12 |
| tabmat | 20.86 | 3.59x | 1.00x | 0.00 | 2.59e-12 |
| xsimd_tuned | 24.07 | 3.11x | 0.87x | 0.00 | 2.11e-11 |
| torch_compile_einsum | 44.18 | 1.69x | 0.47x | 0.00 | 3.26e-12 |
| torch_einsum | 44.42 | 1.69x | 0.47x | 0.00 | 3.26e-12 |
| numba_blas_tiled | 47.36 | 1.58x | 0.44x | 0.00 | 3.86e-12 |
| numba_blas_kchunk_mt | 48.05 | 1.56x | 0.43x | 0.12 | 4.99e-12 |
| helion_eager | 67.99 | 1.10x | 0.31x | 0.00 | 3.26e-12 |
| torch_compile_tiled_tuned | 72.10 | 1.04x | 0.29x | 15.98 | 7.53e-12 |
| numpy_weighted_gram | 74.25 | 1.01x | 0.28x | 0.00 | 0.00e+00 |
| numpy_einsum | 74.88 | 1.00x | 0.28x | 0.00 | 0.00e+00 |
| torch_tiled_tuned | 77.62 | 0.96x | 0.27x | 5.15 | 8.77e-12 |
| numba_blas_fused | 81.11 | 0.92x | 0.26x | 0.76 | 1.03e-12 |
| helion_tiled_tuned | 94.98 | 0.79x | 0.22x | 0.00 | 4.62e-12 |
| jax_einsum | 96.43 | 0.78x | 0.22x | 37.04 | 3.43e-03 |
| jax_chunked_tuned | 96.78 | 0.77x | 0.22x | 56.34 | 2.89e-03 |
| numba_fused_tuned | 105.94 | 0.71x | 0.20x | 0.00 | 1.68e-11 |
| numba_jblock_tuned | 136.66 | 0.55x | 0.15x | 0.00 | 1.74e-11 |
| numba_fused_blocked | 140.77 | 0.53x | 0.15x | 0.00 | 1.66e-11 |
| numba_tabmat_style_mt | 251.02 | 0.30x | 0.08x | 0.00 | 1.74e-11 |
| numba_rival_mt | 295.94 | 0.25x | 0.07x | 0.00 | 1.95e-11 |
| numba_k_chunk_tabmat | 299.00 | 0.25x | 0.07x | 0.00 | 1.95e-11 |

Best: **numba_blas_tuned** (12.34 ms). tabmat: 20.86 ms (1.69x vs best).

## glm_small_f32

| kernel | median (ms) | vs numpy_einsum | vs tabmat | peak RSS Δ (MB) | max rel err |
|---|---:|---:|---:|---:|---:|
| tabmat | 1.71 | 6.43x | 1.00x | 0.77 | 1.28e-04 |
| numba_blas_tuned | 2.48 | 4.43x | 0.69x | 0.57 | 2.61e-04 |
| torch_einsum | 3.73 | 2.94x | 0.46x | 0.00 | 1.32e-04 |
| torch_compile_einsum | 3.85 | 2.86x | 0.44x | 0.00 | 1.32e-04 |
| torch_compile_tiled_tuned | 5.45 | 2.02x | 0.31x | 0.00 | 1.32e-04 |
| numba_blas_kchunk_mt | 7.02 | 1.57x | 0.24x | 0.25 | 1.95e-04 |
| numba_blas_tiled | 7.10 | 1.55x | 0.24x | 0.00 | 2.06e-04 |
| helion_eager | 7.11 | 1.54x | 0.24x | 0.00 | 1.32e-04 |
| jax_einsum | 9.35 | 1.17x | 0.18x | 0.00 | 1.04e-04 |
| numba_blas_fused | 9.50 | 1.16x | 0.18x | 0.00 | 0.00e+00 |
| numba_fused_tuned | 9.76 | 1.13x | 0.17x | 0.00 | 8.88e-04 |
| jax_chunked_tuned | 9.78 | 1.12x | 0.17x | 1.54 | 1.29e-04 |
| torch_tiled_tuned | 10.10 | 1.09x | 0.17x | 0.00 | 1.32e-04 |
| numpy_weighted_gram | 10.66 | 1.03x | 0.16x | 0.00 | 0.00e+00 |
| numpy_einsum | 10.99 | 1.00x | 0.16x | 0.00 | 0.00e+00 |
| numba_jblock_tuned | 14.22 | 0.77x | 0.12x | 0.00 | 2.21e-03 |
| helion_tiled_tuned | 15.71 | 0.70x | 0.11x | 0.00 | 1.32e-04 |
| numba_tabmat_style_mt | 20.01 | 0.55x | 0.09x | 0.00 | 2.21e-03 |
| numba_fused_blocked | 22.29 | 0.49x | 0.08x | 0.00 | 2.21e-03 |
| numba_k_chunk_tabmat | 23.82 | 0.46x | 0.07x | 0.00 | 6.43e-04 |
| numba_rival_mt | 24.00 | 0.46x | 0.07x | 0.00 | 6.43e-04 |

Best: **tabmat** (1.71 ms). tabmat: 1.71 ms (1.00x vs best).
