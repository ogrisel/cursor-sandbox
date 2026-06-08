# Sandwich benchmark report (multi-threaded)

Threading: **multi** (4 threads)

## glm_small

| kernel | median (ms) | vs numpy_einsum | vs tabmat | peak RSS Δ (MB) | max rel err |
|---|---:|---:|---:|---:|---:|
| tabmat | 2.22 | 6.70x | 1.00x | 0.00 | 5.82e-13 |
| torch_einsum | 5.38 | 2.76x | 0.41x | 0.00 | 1.83e-13 |
| torch_compile_einsum | 6.65 | 2.24x | 0.33x | 0.07 | 4.52e-13 |
| numba_blas_tiled | 6.89 | 2.16x | 0.32x | 0.00 | 4.92e-13 |
| numba_blas_kchunk_mt | 7.68 | 1.94x | 0.29x | 5.91 | 3.24e-13 |
| helion_eager | 8.61 | 1.73x | 0.26x | 0.00 | 1.83e-13 |
| jax_einsum | 11.16 | 1.33x | 0.20x | 15.07 | 7.23e-05 |
| numpy_weighted_gram | 12.95 | 1.15x | 0.17x | 0.00 | 0.00e+00 |
| numpy_einsum | 14.88 | 1.00x | 0.15x | 0.00 | 0.00e+00 |
| numba_blas_fused | 16.11 | 0.92x | 0.14x | 0.16 | 0.00e+00 |
| numba_tabmat_style_mt | 19.15 | 0.78x | 0.12x | 0.00 | 1.66e-12 |
| numba_rival_mt | 22.85 | 0.65x | 0.10x | 0.00 | 9.00e-13 |
| numba_k_chunk_tabmat | 23.31 | 0.64x | 0.10x | 0.00 | 9.00e-13 |
| numba_fused_blocked | 24.89 | 0.60x | 0.09x | 0.00 | 1.62e-12 |

Best: **tabmat** (2.22 ms). tabmat: 2.22 ms (1.00x vs best).

## glm_medium

| kernel | median (ms) | vs numpy_einsum | vs tabmat | peak RSS Δ (MB) | max rel err |
|---|---:|---:|---:|---:|---:|
| tabmat | 18.86 | 4.39x | 1.00x | 0.00 | 4.58e-12 |
| torch_einsum | 41.98 | 1.97x | 0.45x | 0.00 | 2.90e-12 |
| numba_blas_tiled | 53.78 | 1.54x | 0.35x | 0.00 | 1.03e-12 |
| numba_blas_kchunk_mt | 54.74 | 1.51x | 0.34x | 37.75 | 1.67e-12 |
| helion_eager | 69.73 | 1.19x | 0.27x | 0.00 | 2.90e-12 |
| torch_compile_einsum | 74.19 | 1.12x | 0.25x | 0.00 | 2.70e-12 |
| numpy_weighted_gram | 80.70 | 1.03x | 0.23x | 0.00 | 0.00e+00 |
| numpy_einsum | 82.76 | 1.00x | 0.23x | 0.00 | 0.00e+00 |
| numba_blas_fused | 86.65 | 0.96x | 0.22x | 0.01 | 0.00e+00 |
| jax_einsum | 100.27 | 0.83x | 0.19x | 42.64 | 1.35e-03 |
| numba_fused_blocked | 151.00 | 0.55x | 0.12x | 0.00 | 1.45e-11 |
| numba_tabmat_style_mt | 190.85 | 0.43x | 0.10x | 0.00 | 1.74e-11 |
| numba_rival_mt | 246.10 | 0.34x | 0.08x | 0.00 | 1.55e-11 |
| numba_k_chunk_tabmat | 246.12 | 0.34x | 0.08x | 0.00 | 1.55e-11 |

Best: **tabmat** (18.86 ms). tabmat: 18.86 ms (1.00x vs best).

## glm_tall_skinny

| kernel | median (ms) | vs numpy_einsum | vs tabmat | peak RSS Δ (MB) | max rel err |
|---|---:|---:|---:|---:|---:|
| tabmat | 17.43 | 4.64x | 1.00x | 0.14 | 2.40e-13 |
| torch_compile_einsum | 29.97 | 2.70x | 0.58x | 0.00 | 4.32e-13 |
| torch_einsum | 30.73 | 2.63x | 0.57x | 0.25 | 4.32e-13 |
| numba_blas_tiled | 44.56 | 1.81x | 0.39x | 0.00 | 5.12e-13 |
| numba_blas_kchunk_mt | 47.23 | 1.71x | 0.37x | 0.00 | 3.65e-13 |
| helion_eager | 57.55 | 1.40x | 0.30x | 0.00 | 4.32e-13 |
| numpy_weighted_gram | 77.92 | 1.04x | 0.22x | 0.00 | 0.00e+00 |
| numpy_einsum | 80.83 | 1.00x | 0.22x | 0.00 | 0.00e+00 |
| numba_blas_fused | 85.62 | 0.94x | 0.20x | 0.00 | 0.00e+00 |
| jax_einsum | 94.03 | 0.86x | 0.19x | 39.18 | 1.96e-04 |
| numba_rival_mt | 106.17 | 0.76x | 0.16x | 0.00 | 7.83e-13 |
| numba_k_chunk_tabmat | 107.88 | 0.75x | 0.16x | 0.00 | 7.83e-13 |
| numba_tabmat_style_mt | 119.95 | 0.67x | 0.15x | 0.00 | 1.75e-12 |
| numba_fused_blocked | 137.68 | 0.59x | 0.13x | 0.00 | 1.68e-12 |

Best: **tabmat** (17.43 ms). tabmat: 17.43 ms (1.00x vs best).

## glm_square_cols

| kernel | median (ms) | vs numpy_einsum | vs tabmat | peak RSS Δ (MB) | max rel err |
|---|---:|---:|---:|---:|---:|
| tabmat | 21.20 | 3.46x | 1.00x | 0.13 | 4.21e-12 |
| torch_compile_einsum | 43.49 | 1.68x | 0.49x | 0.09 | 3.26e-12 |
| torch_einsum | 44.10 | 1.66x | 0.48x | 0.09 | 3.26e-12 |
| numba_blas_tiled | 44.85 | 1.63x | 0.47x | 0.00 | 3.86e-12 |
| numba_blas_kchunk_mt | 47.44 | 1.54x | 0.45x | 0.26 | 4.99e-12 |
| helion_eager | 65.49 | 1.12x | 0.32x | 0.00 | 3.26e-12 |
| numpy_weighted_gram | 72.65 | 1.01x | 0.29x | 0.00 | 0.00e+00 |
| numpy_einsum | 73.26 | 1.00x | 0.29x | 0.00 | 0.00e+00 |
| numba_blas_fused | 79.15 | 0.93x | 0.27x | 0.76 | 1.03e-12 |
| jax_einsum | 89.36 | 0.82x | 0.24x | 37.54 | 3.43e-03 |
| numba_fused_blocked | 128.05 | 0.57x | 0.17x | 0.00 | 1.66e-11 |
| numba_tabmat_style_mt | 251.06 | 0.29x | 0.08x | 0.00 | 1.74e-11 |
| numba_rival_mt | 295.31 | 0.25x | 0.07x | 0.00 | 1.95e-11 |
| numba_k_chunk_tabmat | 295.70 | 0.25x | 0.07x | 0.00 | 1.95e-11 |

Best: **tabmat** (21.20 ms). tabmat: 21.20 ms (1.00x vs best).

## glm_small_f32

| kernel | median (ms) | vs numpy_einsum | vs tabmat | peak RSS Δ (MB) | max rel err |
|---|---:|---:|---:|---:|---:|
| tabmat | 1.54 | 6.38x | 1.00x | 0.00 | 2.67e-04 |
| torch_einsum | 2.79 | 3.53x | 0.55x | 0.00 | 1.32e-04 |
| torch_compile_einsum | 3.16 | 3.11x | 0.49x | 0.00 | 1.32e-04 |
| helion_eager | 5.67 | 1.74x | 0.27x | 0.00 | 1.32e-04 |
| numba_blas_tiled | 6.17 | 1.59x | 0.25x | 28.39 | 2.06e-04 |
| numba_blas_kchunk_mt | 6.57 | 1.50x | 0.23x | 19.12 | 1.95e-04 |
| numba_blas_fused | 8.14 | 1.21x | 0.19x | 0.00 | 0.00e+00 |
| jax_einsum | 8.23 | 1.20x | 0.19x | 0.00 | 1.04e-04 |
| numpy_weighted_gram | 8.87 | 1.11x | 0.17x | 0.00 | 0.00e+00 |
| numpy_einsum | 9.85 | 1.00x | 0.16x | 0.00 | 0.00e+00 |
| numba_tabmat_style_mt | 17.66 | 0.56x | 0.09x | 1.55 | 2.21e-03 |
| numba_fused_blocked | 19.71 | 0.50x | 0.08x | 3.96 | 2.21e-03 |
| numba_rival_mt | 20.96 | 0.47x | 0.07x | 0.00 | 6.43e-04 |
| numba_k_chunk_tabmat | 21.46 | 0.46x | 0.07x | 0.00 | 6.43e-04 |

Best: **tabmat** (1.54 ms). tabmat: 1.54 ms (1.00x vs best).
