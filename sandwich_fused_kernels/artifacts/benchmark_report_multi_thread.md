# Sandwich benchmark report (multi-threaded)

Threading: **multi** (4 threads)

## glm_small

| kernel | median (ms) | vs numpy_einsum | vs tabmat | peak RSS Δ (MB) | max rel err |
|---|---:|---:|---:|---:|---:|
| numba_blas_tuned | 2.23 | 7.16x | 1.27x | 0.00 | 4.57e-13 |
| xsimd_tuned | 2.48 | 6.44x | 1.14x | 0.00 | 9.00e-13 |
| tabmat | 2.83 | 5.65x | 1.00x | 0.00 | 5.82e-13 |
| torch_compile_triton_cpu | 5.36 | 2.99x | 0.53x | 0.00 | 4.52e-13 |
| torch_compile_einsum | 5.58 | 2.87x | 0.51x | 0.12 | 4.52e-13 |
| torch_einsum | 6.33 | 2.53x | 0.45x | 0.00 | 1.83e-13 |
| numba_blas_tiled | 7.45 | 2.15x | 0.38x | 0.00 | 4.92e-13 |
| numba_blas_kchunk_mt | 7.87 | 2.03x | 0.36x | 5.92 | 3.24e-13 |
| numba_fused_tuned | 11.20 | 1.43x | 0.25x | 0.00 | 3.26e-13 |
| helion_eager | 11.34 | 1.41x | 0.25x | 0.00 | 1.83e-13 |
| numba_blas_fused | 12.02 | 1.33x | 0.24x | 0.00 | 0.00e+00 |
| torch_compile_tiled_tuned | 12.24 | 1.31x | 0.23x | 0.00 | 4.52e-13 |
| jax_einsum | 13.61 | 1.18x | 0.21x | 5.67 | 7.23e-05 |
| jax_chunked_tuned | 14.43 | 1.11x | 0.20x | 0.70 | 1.55e-04 |
| numba_jblock_tuned | 14.47 | 1.11x | 0.20x | 0.00 | 1.66e-12 |
| torch_tiled_tuned | 14.51 | 1.10x | 0.19x | 0.00 | 1.83e-13 |
| numpy_einsum | 15.99 | 1.00x | 0.18x | 0.00 | 0.00e+00 |
| numpy_weighted_gram | 16.27 | 0.98x | 0.17x | 0.00 | 0.00e+00 |
| triton_cpu_native | 19.02 | 0.84x | 0.15x | 0.00 | 4.18e-13 |
| numba_tabmat_style_mt | 20.44 | 0.78x | 0.14x | 0.00 | 1.66e-12 |
| numba_k_chunk_tabmat | 24.09 | 0.66x | 0.12x | 0.00 | 9.00e-13 |
| numba_rival_mt | 24.32 | 0.66x | 0.12x | 0.00 | 9.00e-13 |
| numba_fused_blocked | 26.64 | 0.60x | 0.11x | 0.00 | 1.62e-12 |
| helion_tiled_tuned | 27.51 | 0.58x | 0.10x | 0.00 | 4.64e-13 |
| helion_triton_cpu | 34.85 | 0.46x | 0.08x | 0.00 | 4.18e-13 |

Best: **numba_blas_tuned** (2.23 ms). tabmat: 2.83 ms (1.27x vs best).

## glm_medium

| kernel | median (ms) | vs numpy_einsum | vs tabmat | peak RSS Δ (MB) | max rel err |
|---|---:|---:|---:|---:|---:|
| numba_blas_tuned | 17.03 | 5.21x | 1.29x | 0.00 | 3.01e-12 |
| tabmat | 21.99 | 4.04x | 1.00x | 0.07 | 5.03e-12 |
| xsimd_tuned | 29.49 | 3.01x | 0.75x | 0.00 | 7.72e-12 |
| torch_einsum | 49.23 | 1.80x | 0.45x | 0.00 | 2.90e-12 |
| numba_blas_kchunk_mt | 52.58 | 1.69x | 0.42x | 37.23 | 1.67e-12 |
| torch_compile_einsum | 53.77 | 1.65x | 0.41x | 0.15 | 2.90e-12 |
| numba_blas_tiled | 62.09 | 1.43x | 0.35x | 0.00 | 1.03e-12 |
| torch_compile_triton_cpu | 78.11 | 1.14x | 0.28x | 0.00 | 2.70e-12 |
| helion_eager | 79.01 | 1.12x | 0.28x | 0.00 | 2.90e-12 |
| numpy_einsum | 88.74 | 1.00x | 0.25x | 0.00 | 0.00e+00 |
| numpy_weighted_gram | 90.47 | 0.98x | 0.24x | 0.00 | 0.00e+00 |
| numba_blas_fused | 100.08 | 0.89x | 0.22x | 0.01 | 0.00e+00 |
| jax_einsum | 120.74 | 0.73x | 0.18x | 43.44 | 1.35e-03 |
| torch_compile_tiled_tuned | 124.79 | 0.71x | 0.18x | 0.00 | 1.94e-12 |
| numba_fused_tuned | 131.41 | 0.68x | 0.17x | 0.00 | 7.72e-12 |
| jax_chunked_tuned | 137.22 | 0.65x | 0.16x | 42.46 | 1.79e-03 |
| helion_tiled_tuned | 138.01 | 0.64x | 0.16x | 0.00 | 2.52e-12 |
| helion_triton_cpu | 151.06 | 0.59x | 0.15x | 0.00 | 3.26e-12 |
| numba_jblock_tuned | 171.88 | 0.52x | 0.13x | 0.00 | 1.74e-11 |
| numba_tabmat_style_mt | 184.00 | 0.48x | 0.12x | 0.00 | 1.74e-11 |
| triton_cpu_native | 185.63 | 0.48x | 0.12x | 0.00 | 3.26e-12 |
| torch_tiled_tuned | 228.49 | 0.39x | 0.10x | 0.00 | 4.13e-12 |
| numba_k_chunk_tabmat | 233.38 | 0.38x | 0.09x | 0.00 | 1.55e-11 |
| numba_rival_mt | 234.77 | 0.38x | 0.09x | 0.00 | 1.55e-11 |
| numba_fused_blocked | 248.35 | 0.36x | 0.09x | 0.00 | 1.45e-11 |

Best: **numba_blas_tuned** (17.03 ms). tabmat: 21.99 ms (1.29x vs best).

## glm_tall_skinny

| kernel | median (ms) | vs numpy_einsum | vs tabmat | peak RSS Δ (MB) | max rel err |
|---|---:|---:|---:|---:|---:|
| numba_blas_tuned | 5.91 | 16.09x | 2.06x | 0.00 | 5.83e-13 |
| xsimd_tuned | 9.15 | 10.40x | 1.33x | 0.00 | 7.83e-13 |
| tabmat | 12.15 | 7.83x | 1.00x | 0.00 | 5.21e-13 |
| torch_compile_tiled_tuned | 29.54 | 3.22x | 0.41x | 0.00 | 4.45e-13 |
| torch_compile_einsum | 30.64 | 3.10x | 0.40x | 0.22 | 4.32e-13 |
| torch_einsum | 31.72 | 3.00x | 0.38x | 0.00 | 4.32e-13 |
| torch_tiled_tuned | 31.80 | 2.99x | 0.38x | 0.00 | 6.10e-13 |
| numba_fused_tuned | 34.98 | 2.72x | 0.35x | 0.00 | 7.83e-13 |
| helion_tiled_tuned | 36.81 | 2.58x | 0.33x | 0.00 | 6.10e-13 |
| numba_blas_tiled | 45.26 | 2.10x | 0.27x | 0.00 | 5.12e-13 |
| numba_blas_kchunk_mt | 47.95 | 1.98x | 0.25x | 0.00 | 3.65e-13 |
| torch_compile_triton_cpu | 54.54 | 1.74x | 0.22x | 0.00 | 9.35e-13 |
| triton_cpu_native | 54.59 | 1.74x | 0.22x | 0.00 | 2.18e-13 |
| helion_eager | 55.66 | 1.71x | 0.22x | 0.00 | 4.32e-13 |
| numba_jblock_tuned | 64.73 | 1.47x | 0.19x | 0.00 | 1.75e-12 |
| helion_triton_cpu | 67.86 | 1.40x | 0.18x | 0.00 | 2.18e-13 |
| numpy_weighted_gram | 84.84 | 1.12x | 0.14x | 0.00 | 0.00e+00 |
| numba_blas_fused | 88.72 | 1.07x | 0.14x | 0.00 | 0.00e+00 |
| jax_chunked_tuned | 92.42 | 1.03x | 0.13x | 38.98 | 1.00e-04 |
| numpy_einsum | 95.12 | 1.00x | 0.13x | 0.00 | 0.00e+00 |
| jax_einsum | 96.86 | 0.98x | 0.13x | 39.21 | 1.96e-04 |
| numba_k_chunk_tabmat | 102.79 | 0.93x | 0.12x | 0.00 | 7.83e-13 |
| numba_tabmat_style_mt | 104.66 | 0.91x | 0.12x | 0.00 | 1.75e-12 |
| numba_rival_mt | 104.68 | 0.91x | 0.12x | 0.00 | 7.83e-13 |
| numba_fused_blocked | 137.80 | 0.69x | 0.09x | 0.00 | 1.68e-12 |

Best: **numba_blas_tuned** (5.91 ms). tabmat: 12.15 ms (2.06x vs best).

## glm_square_cols

| kernel | median (ms) | vs numpy_einsum | vs tabmat | peak RSS Δ (MB) | max rel err |
|---|---:|---:|---:|---:|---:|
| numba_blas_tuned | 12.52 | 5.64x | 1.62x | 0.00 | 2.59e-12 |
| tabmat | 20.24 | 3.49x | 1.00x | 0.00 | 4.49e-12 |
| xsimd_tuned | 21.08 | 3.35x | 0.96x | 0.00 | 2.11e-11 |
| torch_einsum | 43.25 | 1.63x | 0.47x | 0.00 | 3.26e-12 |
| torch_compile_einsum | 45.50 | 1.55x | 0.44x | 0.00 | 3.26e-12 |
| numba_blas_tiled | 54.64 | 1.29x | 0.37x | 0.00 | 3.86e-12 |
| numba_blas_kchunk_mt | 58.58 | 1.21x | 0.35x | 0.26 | 4.99e-12 |
| torch_compile_tiled_tuned | 60.42 | 1.17x | 0.33x | 15.98 | 7.53e-12 |
| torch_tiled_tuned | 65.07 | 1.09x | 0.31x | 5.15 | 8.77e-12 |
| helion_eager | 65.13 | 1.08x | 0.31x | 0.00 | 3.26e-12 |
| numpy_einsum | 70.64 | 1.00x | 0.29x | 0.00 | 0.00e+00 |
| numpy_weighted_gram | 75.04 | 0.94x | 0.27x | 0.00 | 0.00e+00 |
| numba_blas_fused | 78.12 | 0.90x | 0.26x | 0.76 | 1.03e-12 |
| jax_einsum | 86.83 | 0.81x | 0.23x | 36.78 | 3.43e-03 |
| torch_compile_triton_cpu | 87.43 | 0.81x | 0.23x | 0.00 | 6.96e-12 |
| helion_tiled_tuned | 94.30 | 0.75x | 0.21x | 0.00 | 4.62e-12 |
| jax_chunked_tuned | 97.44 | 0.72x | 0.21x | 40.86 | 2.89e-03 |
| numba_fused_tuned | 109.31 | 0.65x | 0.19x | 0.00 | 1.68e-11 |
| numba_jblock_tuned | 144.71 | 0.49x | 0.14x | 0.00 | 1.74e-11 |
| numba_fused_blocked | 156.67 | 0.45x | 0.13x | 0.00 | 1.66e-11 |
| triton_cpu_native | 238.64 | 0.30x | 0.08x | 0.00 | 6.52e-12 |
| helion_triton_cpu | 275.20 | 0.26x | 0.07x | 0.00 | 6.52e-12 |
| numba_tabmat_style_mt | 298.30 | 0.24x | 0.07x | 0.00 | 1.74e-11 |
| numba_k_chunk_tabmat | 325.48 | 0.22x | 0.06x | 0.00 | 1.95e-11 |
| numba_rival_mt | 342.32 | 0.21x | 0.06x | 0.11 | 1.95e-11 |

Best: **numba_blas_tuned** (12.52 ms). tabmat: 20.24 ms (1.62x vs best).

## glm_small_f32

| kernel | median (ms) | vs numpy_einsum | vs tabmat | peak RSS Δ (MB) | max rel err |
|---|---:|---:|---:|---:|---:|
| tabmat | 1.49 | 6.56x | 1.00x | 0.77 | 1.68e-04 |
| numba_blas_tuned | 1.50 | 6.49x | 0.99x | 0.00 | 2.61e-04 |
| torch_einsum | 3.02 | 3.23x | 0.49x | 0.00 | 1.32e-04 |
| torch_compile_einsum | 3.41 | 2.86x | 0.44x | 0.00 | 1.32e-04 |
| torch_compile_triton_cpu | 3.75 | 2.60x | 0.40x | 0.00 | 1.32e-04 |
| torch_compile_tiled_tuned | 5.35 | 1.82x | 0.28x | 0.00 | 1.32e-04 |
| helion_eager | 5.94 | 1.64x | 0.25x | 0.00 | 1.32e-04 |
| numba_blas_tiled | 6.52 | 1.50x | 0.23x | 0.00 | 2.06e-04 |
| numba_blas_kchunk_mt | 6.63 | 1.47x | 0.22x | 0.31 | 1.95e-04 |
| numba_fused_tuned | 8.57 | 1.14x | 0.17x | 0.00 | 8.88e-04 |
| numba_blas_fused | 8.62 | 1.13x | 0.17x | 0.00 | 0.00e+00 |
| jax_einsum | 8.67 | 1.13x | 0.17x | 0.00 | 1.04e-04 |
| numpy_weighted_gram | 9.14 | 1.07x | 0.16x | 0.00 | 0.00e+00 |
| triton_cpu_native | 9.63 | 1.01x | 0.15x | 0.00 | 1.73e-04 |
| numpy_einsum | 9.76 | 1.00x | 0.15x | 0.00 | 0.00e+00 |
| jax_chunked_tuned | 9.89 | 0.99x | 0.15x | 1.98 | 1.29e-04 |
| torch_tiled_tuned | 11.60 | 0.84x | 0.13x | 0.00 | 1.32e-04 |
| numba_jblock_tuned | 12.62 | 0.77x | 0.12x | 0.00 | 2.21e-03 |
| helion_tiled_tuned | 14.24 | 0.69x | 0.10x | 0.00 | 1.32e-04 |
| numba_tabmat_style_mt | 19.58 | 0.50x | 0.08x | 0.00 | 2.21e-03 |
| numba_fused_blocked | 20.68 | 0.47x | 0.07x | 0.00 | 2.21e-03 |
| numba_k_chunk_tabmat | 21.04 | 0.46x | 0.07x | 0.00 | 6.43e-04 |
| numba_rival_mt | 21.34 | 0.46x | 0.07x | 0.00 | 6.43e-04 |
| helion_triton_cpu | 25.25 | 0.39x | 0.06x | 0.00 | 1.73e-04 |

Best: **tabmat** (1.49 ms). tabmat: 1.49 ms (1.00x vs best).
