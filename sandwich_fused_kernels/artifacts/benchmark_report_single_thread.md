# Sandwich benchmark report (single-threaded)

Threading: **single** (1 threads)

## glm_small

| kernel | median (ms) | vs numpy_einsum | vs tabmat | peak RSS Δ (MB) | max rel err |
|---|---:|---:|---:|---:|---:|
| torch_compile_einsum | 4.41 | 3.42x | 1.53x | 1.78 | 4.52e-13 |
| torch_einsum | 4.67 | 3.23x | 1.45x | 0.00 | 1.83e-13 |
| torch_compile_triton_cpu | 5.94 | 2.54x | 1.14x | 0.53 | 4.52e-13 |
| helion_eager | 6.57 | 2.29x | 1.03x | 0.00 | 1.83e-13 |
| tabmat | 6.76 | 2.23x | 1.00x | 0.34 | 5.77e-13 |
| torch_compile_tiled_tuned | 8.08 | 1.86x | 0.84x | 3.18 | 4.52e-13 |
| triton_cpu_native | 9.01 | 1.67x | 0.75x | 0.06 | 2.43e-13 |
| torch_tiled_tuned | 10.59 | 1.42x | 0.64x | 0.00 | 1.83e-13 |
| jax_chunked_tuned | 12.96 | 1.16x | 0.52x | 42.54 | 1.16e-04 |
| numpy_weighted_gram | 14.38 | 1.05x | 0.47x | 0.00 | 3.16e-14 |
| numpy_einsum | 15.07 | 1.00x | 0.45x | 0.00 | 3.16e-14 |
| jax_einsum | 15.64 | 0.96x | 0.43x | 57.16 | 7.23e-05 |
| numba_blas_fused | 15.69 | 0.96x | 0.43x | 0.30 | 3.16e-14 |
| helion_tiled_tuned | 21.39 | 0.70x | 0.32x | 0.00 | 4.64e-13 |
| helion_triton_cpu | 21.87 | 0.69x | 0.31x | 0.51 | 2.43e-13 |
| numba_jblock_tuned | 37.13 | 0.41x | 0.18x | 0.00 | 1.66e-12 |
| numba_k_chunk_tabmat | 71.88 | 0.21x | 0.09x | 0.00 | 1.66e-12 |
| numba_fused_tuned | 75.33 | 0.20x | 0.09x | 0.00 | 1.66e-12 |
| numba_tabmat_style_st | 83.05 | 0.18x | 0.08x | 0.00 | 1.66e-12 |
| numba_rival_st | 83.12 | 0.18x | 0.08x | 0.00 | 1.66e-12 |

Best: **torch_compile_einsum** (4.41 ms). tabmat: 6.76 ms (1.53x vs best).

## glm_medium

| kernel | median (ms) | vs numpy_einsum | vs tabmat | peak RSS Δ (MB) | max rel err |
|---|---:|---:|---:|---:|---:|
| torch_einsum | 60.34 | 1.50x | 1.08x | 0.00 | 2.90e-12 |
| helion_eager | 62.51 | 1.45x | 1.05x | 0.02 | 2.90e-12 |
| tabmat | 65.41 | 1.39x | 1.00x | 0.00 | 4.59e-12 |
| torch_compile_triton_cpu | 67.82 | 1.34x | 0.96x | 0.50 | 2.70e-12 |
| torch_compile_einsum | 67.98 | 1.33x | 0.96x | 0.64 | 2.70e-12 |
| torch_compile_tiled_tuned | 76.50 | 1.19x | 0.85x | 244.59 | 1.94e-12 |
| numpy_weighted_gram | 88.99 | 1.02x | 0.73x | 0.00 | 0.00e+00 |
| numpy_einsum | 90.73 | 1.00x | 0.72x | 0.10 | 0.00e+00 |
| helion_tiled_tuned | 91.42 | 0.99x | 0.72x | 1.29 | 2.52e-12 |
| numba_blas_fused | 104.05 | 0.87x | 0.63x | 0.27 | 0.00e+00 |
| jax_einsum | 109.06 | 0.83x | 0.60x | 43.98 | 1.35e-03 |
| triton_cpu_native | 109.45 | 0.83x | 0.60x | 0.30 | 3.75e-12 |
| jax_chunked_tuned | 120.32 | 0.75x | 0.54x | 45.11 | 6.96e-04 |
| helion_triton_cpu | 120.66 | 0.75x | 0.54x | 0.51 | 3.75e-12 |
| torch_tiled_tuned | 157.70 | 0.58x | 0.41x | 0.26 | 4.13e-12 |
| numba_jblock_tuned | 403.04 | 0.23x | 0.16x | 0.00 | 1.74e-11 |
| numba_k_chunk_tabmat | 780.94 | 0.12x | 0.08x | 0.00 | 1.74e-11 |
| numba_fused_tuned | 861.28 | 0.11x | 0.08x | 0.00 | 1.74e-11 |
| numba_tabmat_style_st | 896.25 | 0.10x | 0.07x | 0.00 | 1.74e-11 |
| numba_rival_st | 896.59 | 0.10x | 0.07x | 0.05 | 1.74e-11 |

Best: **torch_einsum** (60.34 ms). tabmat: 65.41 ms (1.08x vs best).

## glm_tall_skinny

| kernel | median (ms) | vs numpy_einsum | vs tabmat | peak RSS Δ (MB) | max rel err |
|---|---:|---:|---:|---:|---:|
| torch_compile_tiled_tuned | 22.63 | 3.29x | 1.77x | 29.13 | 4.45e-13 |
| torch_tiled_tuned | 30.50 | 2.44x | 1.32x | 0.00 | 6.10e-13 |
| helion_tiled_tuned | 36.14 | 2.06x | 1.11x | 0.51 | 6.10e-13 |
| triton_cpu_native | 37.78 | 1.97x | 1.06x | 0.72 | 4.90e-13 |
| tabmat | 40.13 | 1.85x | 1.00x | 0.00 | 4.63e-13 |
| helion_triton_cpu | 49.21 | 1.51x | 0.82x | 0.00 | 4.90e-13 |
| torch_einsum | 59.38 | 1.25x | 0.68x | 0.00 | 4.32e-13 |
| torch_compile_triton_cpu | 60.74 | 1.22x | 0.66x | 0.42 | 9.35e-13 |
| torch_compile_einsum | 61.38 | 1.21x | 0.65x | 0.42 | 9.35e-13 |
| helion_eager | 64.07 | 1.16x | 0.63x | 0.00 | 4.32e-13 |
| numpy_weighted_gram | 72.56 | 1.03x | 0.55x | 0.00 | 0.00e+00 |
| numpy_einsum | 74.40 | 1.00x | 0.54x | 0.00 | 0.00e+00 |
| numba_blas_fused | 84.87 | 0.88x | 0.47x | 0.00 | 0.00e+00 |
| jax_einsum | 101.27 | 0.73x | 0.40x | 39.28 | 1.96e-04 |
| jax_chunked_tuned | 102.06 | 0.73x | 0.39x | 45.09 | 6.18e-05 |
| numba_jblock_tuned | 154.92 | 0.48x | 0.26x | 0.00 | 1.75e-12 |
| numba_k_chunk_tabmat | 300.13 | 0.25x | 0.13x | 0.00 | 1.75e-12 |
| numba_fused_tuned | 309.70 | 0.24x | 0.13x | 0.00 | 1.75e-12 |
| numba_tabmat_style_st | 349.15 | 0.21x | 0.11x | 0.00 | 1.75e-12 |
| numba_rival_st | 349.87 | 0.21x | 0.11x | 0.25 | 1.75e-12 |

Best: **torch_compile_tiled_tuned** (22.63 ms). tabmat: 40.13 ms (1.77x vs best).

## glm_square_cols

| kernel | median (ms) | vs numpy_einsum | vs tabmat | peak RSS Δ (MB) | max rel err |
|---|---:|---:|---:|---:|---:|
| torch_einsum | 58.77 | 1.44x | 1.22x | 0.00 | 3.26e-12 |
| torch_tiled_tuned | 59.20 | 1.43x | 1.21x | 8.14 | 8.77e-12 |
| helion_eager | 62.99 | 1.34x | 1.14x | 0.02 | 3.26e-12 |
| torch_compile_tiled_tuned | 65.01 | 1.30x | 1.11x | 17.70 | 7.53e-12 |
| torch_compile_triton_cpu | 65.47 | 1.29x | 1.10x | 1.36 | 6.96e-12 |
| torch_compile_einsum | 66.22 | 1.28x | 1.09x | 1.62 | 6.96e-12 |
| tabmat | 71.89 | 1.18x | 1.00x | 0.00 | 2.25e-12 |
| helion_tiled_tuned | 77.67 | 1.09x | 0.93x | 0.51 | 4.62e-12 |
| numpy_weighted_gram | 82.18 | 1.03x | 0.87x | 0.00 | 0.00e+00 |
| numpy_einsum | 84.55 | 1.00x | 0.85x | 0.12 | 0.00e+00 |
| jax_einsum | 89.60 | 0.94x | 0.80x | 37.68 | 3.43e-03 |
| numba_blas_fused | 94.84 | 0.89x | 0.76x | 0.27 | 0.00e+00 |
| jax_chunked_tuned | 97.51 | 0.87x | 0.74x | 38.38 | 2.03e-03 |
| triton_cpu_native | 149.42 | 0.57x | 0.48x | 15.34 | 4.10e-12 |
| helion_triton_cpu | 160.71 | 0.53x | 0.45x | 0.51 | 4.10e-12 |
| numba_jblock_tuned | 592.27 | 0.14x | 0.12x | 0.00 | 1.74e-11 |
| numba_k_chunk_tabmat | 1134.45 | 0.07x | 0.06x | 0.00 | 1.74e-11 |
| numba_fused_tuned | 1271.46 | 0.07x | 0.06x | 0.00 | 1.74e-11 |
| numba_tabmat_style_st | 1297.39 | 0.07x | 0.06x | 0.00 | 1.74e-11 |
| numba_rival_st | 1299.01 | 0.07x | 0.06x | 0.02 | 1.74e-11 |

Best: **torch_einsum** (58.77 ms). tabmat: 71.89 ms (1.22x vs best).

## glm_small_f32

| kernel | median (ms) | vs numpy_einsum | vs tabmat | peak RSS Δ (MB) | max rel err |
|---|---:|---:|---:|---:|---:|
| torch_compile_einsum | 2.82 | 2.95x | 1.59x | 0.90 | 1.32e-04 |
| torch_compile_triton_cpu | 3.24 | 2.57x | 1.38x | 0.44 | 1.32e-04 |
| torch_einsum | 3.28 | 2.54x | 1.36x | 0.00 | 1.32e-04 |
| tabmat | 4.48 | 1.86x | 1.00x | 0.00 | 1.60e-04 |
| helion_eager | 5.23 | 1.59x | 0.86x | 0.90 | 1.32e-04 |
| torch_compile_tiled_tuned | 5.39 | 1.54x | 0.83x | 5.60 | 1.32e-04 |
| triton_cpu_native | 6.99 | 1.19x | 0.64x | 3.99 | 1.28e-04 |
| jax_einsum | 7.57 | 1.10x | 0.59x | 6.44 | 1.04e-04 |
| torch_tiled_tuned | 7.75 | 1.07x | 0.58x | 0.00 | 1.32e-04 |
| numpy_weighted_gram | 7.76 | 1.07x | 0.58x | 0.00 | 1.00e-05 |
| numba_blas_fused | 7.80 | 1.07x | 0.57x | 0.00 | 1.00e-05 |
| numpy_einsum | 8.32 | 1.00x | 0.54x | 0.00 | 1.00e-05 |
| jax_chunked_tuned | 9.22 | 0.90x | 0.49x | 8.51 | 9.63e-05 |
| helion_tiled_tuned | 13.75 | 0.61x | 0.33x | 0.00 | 1.32e-04 |
| helion_triton_cpu | 20.99 | 0.40x | 0.21x | 0.51 | 1.28e-04 |
| numba_jblock_tuned | 36.42 | 0.23x | 0.12x | 0.00 | 2.21e-03 |
| numba_k_chunk_tabmat | 66.64 | 0.12x | 0.07x | 0.00 | 2.21e-03 |
| numba_fused_tuned | 74.27 | 0.11x | 0.06x | 0.00 | 2.21e-03 |
| numba_tabmat_style_st | 78.96 | 0.11x | 0.06x | 0.00 | 2.21e-03 |
| numba_rival_st | 79.37 | 0.10x | 0.06x | 0.00 | 2.21e-03 |

Best: **torch_compile_einsum** (2.82 ms). tabmat: 4.48 ms (1.59x vs best).
