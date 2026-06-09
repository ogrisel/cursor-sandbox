# Sandwich benchmark report (single-threaded)

Threading: **single** (1 threads)

## glm_small

| kernel | median (ms) | vs numpy_einsum | vs tabmat | peak RSS Δ (MB) | max rel err |
|---|---:|---:|---:|---:|---:|
| torch_compile_triton_cpu | 4.15 | 2.95x | 1.66x | 0.70 | 4.52e-13 |
| torch_compile_einsum | 4.53 | 2.70x | 1.52x | 1.71 | 4.52e-13 |
| torch_einsum | 4.78 | 2.56x | 1.44x | 0.00 | 1.83e-13 |
| helion_eager | 6.55 | 1.87x | 1.05x | 0.00 | 1.83e-13 |
| tabmat | 6.88 | 1.78x | 1.00x | 0.44 | 5.77e-13 |
| torch_compile_tiled_tuned | 7.08 | 1.73x | 0.97x | 9.20 | 4.52e-13 |
| jax_einsum | 9.82 | 1.25x | 0.70x | 17.14 | 7.23e-05 |
| torch_tiled_tuned | 9.93 | 1.24x | 0.69x | 0.00 | 1.83e-13 |
| numba_blas_fused | 10.15 | 1.21x | 0.68x | 0.00 | 3.16e-14 |
| numpy_weighted_gram | 10.82 | 1.13x | 0.64x | 0.00 | 3.16e-14 |
| jax_chunked_tuned | 11.20 | 1.09x | 0.61x | 18.48 | 1.16e-04 |
| numpy_einsum | 12.26 | 1.00x | 0.56x | 2.83 | 3.16e-14 |
| triton_cpu_native | 16.28 | 0.75x | 0.42x | 40.25 | 4.18e-13 |
| helion_tiled_tuned | 20.94 | 0.59x | 0.33x | 0.00 | 4.64e-13 |
| helion_triton_cpu | 30.86 | 0.40x | 0.22x | 0.51 | 4.18e-13 |
| numba_jblock_tuned | 36.82 | 0.33x | 0.19x | 0.00 | 1.66e-12 |
| numba_k_chunk_tabmat | 67.85 | 0.18x | 0.10x | 0.00 | 1.66e-12 |
| numba_fused_tuned | 74.97 | 0.16x | 0.09x | 0.00 | 1.66e-12 |
| numba_rival_st | 81.27 | 0.15x | 0.08x | 0.00 | 1.66e-12 |
| numba_tabmat_style_st | 81.58 | 0.15x | 0.08x | 0.00 | 1.66e-12 |

Best: **torch_compile_triton_cpu** (4.15 ms). tabmat: 6.88 ms (1.66x vs best).

## glm_medium

| kernel | median (ms) | vs numpy_einsum | vs tabmat | peak RSS Δ (MB) | max rel err |
|---|---:|---:|---:|---:|---:|
| torch_einsum | 60.11 | 1.51x | 1.09x | 0.00 | 2.90e-12 |
| torch_compile_triton_cpu | 61.80 | 1.47x | 1.06x | 0.51 | 2.70e-12 |
| helion_eager | 62.97 | 1.45x | 1.04x | 0.00 | 2.90e-12 |
| torch_compile_einsum | 64.75 | 1.41x | 1.01x | 4.49 | 2.70e-12 |
| tabmat | 65.41 | 1.39x | 1.00x | 0.00 | 4.59e-12 |
| numpy_weighted_gram | 88.72 | 1.03x | 0.74x | 0.00 | 0.00e+00 |
| numpy_einsum | 91.01 | 1.00x | 0.72x | 0.09 | 0.00e+00 |
| helion_tiled_tuned | 92.77 | 0.98x | 0.71x | 0.77 | 2.52e-12 |
| jax_einsum | 99.49 | 0.91x | 0.66x | 44.41 | 1.35e-03 |
| torch_compile_tiled_tuned | 100.10 | 0.91x | 0.65x | 345.96 | 1.94e-12 |
| numba_blas_fused | 102.86 | 0.88x | 0.64x | 0.27 | 0.00e+00 |
| jax_chunked_tuned | 109.81 | 0.83x | 0.60x | 45.97 | 6.96e-04 |
| triton_cpu_native | 128.12 | 0.71x | 0.51x | 19.36 | 3.26e-12 |
| helion_triton_cpu | 143.86 | 0.63x | 0.45x | 0.25 | 3.26e-12 |
| torch_tiled_tuned | 162.12 | 0.56x | 0.40x | 0.26 | 4.13e-12 |
| numba_jblock_tuned | 403.78 | 0.23x | 0.16x | 0.00 | 1.74e-11 |
| numba_k_chunk_tabmat | 795.40 | 0.11x | 0.08x | 0.00 | 1.74e-11 |
| numba_fused_tuned | 872.22 | 0.10x | 0.07x | 0.00 | 1.74e-11 |
| numba_tabmat_style_st | 903.44 | 0.10x | 0.07x | 0.00 | 1.74e-11 |
| numba_rival_st | 911.00 | 0.10x | 0.07x | 0.23 | 1.74e-11 |

Best: **torch_einsum** (60.11 ms). tabmat: 65.41 ms (1.09x vs best).

## glm_tall_skinny

| kernel | median (ms) | vs numpy_einsum | vs tabmat | peak RSS Δ (MB) | max rel err |
|---|---:|---:|---:|---:|---:|
| torch_compile_tiled_tuned | 29.42 | 2.94x | 1.46x | 15.58 | 4.45e-13 |
| torch_tiled_tuned | 42.44 | 2.04x | 1.01x | 0.00 | 6.10e-13 |
| tabmat | 42.98 | 2.01x | 1.00x | 0.00 | 4.63e-13 |
| torch_compile_triton_cpu | 53.05 | 1.63x | 0.81x | 0.30 | 9.35e-13 |
| torch_compile_einsum | 53.21 | 1.62x | 0.81x | 2.76 | 9.35e-13 |
| triton_cpu_native | 54.16 | 1.59x | 0.79x | 38.30 | 2.18e-13 |
| helion_tiled_tuned | 54.96 | 1.57x | 0.78x | 0.00 | 6.10e-13 |
| torch_einsum | 56.80 | 1.52x | 0.76x | 0.00 | 4.32e-13 |
| helion_eager | 57.10 | 1.51x | 0.75x | 0.00 | 4.32e-13 |
| numpy_weighted_gram | 84.82 | 1.02x | 0.51x | 0.00 | 0.00e+00 |
| numpy_einsum | 86.38 | 1.00x | 0.50x | 0.00 | 0.00e+00 |
| helion_triton_cpu | 90.74 | 0.95x | 0.47x | 0.00 | 2.18e-13 |
| numba_blas_fused | 96.81 | 0.89x | 0.44x | 0.00 | 0.00e+00 |
| jax_einsum | 101.56 | 0.85x | 0.42x | 39.73 | 1.96e-04 |
| jax_chunked_tuned | 136.34 | 0.63x | 0.32x | 40.62 | 6.18e-05 |
| numba_jblock_tuned | 250.83 | 0.34x | 0.17x | 0.00 | 1.75e-12 |
| numba_k_chunk_tabmat | 471.00 | 0.18x | 0.09x | 0.00 | 1.75e-12 |
| numba_fused_tuned | 530.99 | 0.16x | 0.08x | 0.00 | 1.75e-12 |
| numba_rival_st | 589.82 | 0.15x | 0.07x | 0.00 | 1.75e-12 |
| numba_tabmat_style_st | 591.62 | 0.15x | 0.07x | 0.00 | 1.75e-12 |

Best: **torch_compile_tiled_tuned** (29.42 ms). tabmat: 42.98 ms (1.46x vs best).

## glm_square_cols

| kernel | median (ms) | vs numpy_einsum | vs tabmat | peak RSS Δ (MB) | max rel err |
|---|---:|---:|---:|---:|---:|
| torch_einsum | 63.72 | 1.47x | 1.17x | 0.00 | 3.26e-12 |
| helion_eager | 67.59 | 1.38x | 1.11x | 0.00 | 3.26e-12 |
| torch_compile_tiled_tuned | 69.19 | 1.35x | 1.08x | 0.00 | 7.53e-12 |
| tabmat | 74.77 | 1.25x | 1.00x | 0.00 | 2.25e-12 |
| torch_compile_einsum | 76.70 | 1.22x | 0.97x | 4.65 | 6.96e-12 |
| torch_tiled_tuned | 79.05 | 1.18x | 0.95x | 0.00 | 8.77e-12 |
| helion_tiled_tuned | 89.13 | 1.05x | 0.84x | 0.00 | 4.62e-12 |
| jax_einsum | 90.30 | 1.04x | 0.83x | 37.67 | 3.43e-03 |
| numpy_weighted_gram | 92.04 | 1.02x | 0.81x | 0.00 | 0.00e+00 |
| numpy_einsum | 93.47 | 1.00x | 0.80x | 0.12 | 0.00e+00 |
| jax_chunked_tuned | 100.42 | 0.93x | 0.74x | 38.56 | 2.03e-03 |
| numba_blas_fused | 101.57 | 0.92x | 0.74x | 0.27 | 0.00e+00 |
| torch_compile_triton_cpu | 107.01 | 0.87x | 0.70x | 0.34 | 6.96e-12 |
| triton_cpu_native | 261.48 | 0.36x | 0.29x | 51.36 | 6.52e-12 |
| helion_triton_cpu | 318.79 | 0.29x | 0.23x | 0.00 | 6.52e-12 |
| numba_jblock_tuned | 625.32 | 0.15x | 0.12x | 0.00 | 1.74e-11 |
| numba_k_chunk_tabmat | 1236.66 | 0.08x | 0.06x | 0.00 | 1.74e-11 |
| numba_fused_tuned | 1301.66 | 0.07x | 0.06x | 0.00 | 1.74e-11 |
| numba_tabmat_style_st | 2074.09 | 0.05x | 0.04x | 0.00 | 1.74e-11 |
| numba_rival_st | 2200.14 | 0.04x | 0.03x | 0.00 | 1.74e-11 |

Best: **torch_einsum** (63.72 ms). tabmat: 74.77 ms (1.17x vs best).

## glm_small_f32

| kernel | median (ms) | vs numpy_einsum | vs tabmat | peak RSS Δ (MB) | max rel err |
|---|---:|---:|---:|---:|---:|
| tabmat | 5.17 | 1.81x | 1.00x | 0.00 | 1.60e-04 |
| torch_einsum | 6.08 | 1.54x | 0.85x | 0.00 | 1.32e-04 |
| torch_compile_triton_cpu | 6.45 | 1.45x | 0.80x | 0.44 | 1.32e-04 |
| torch_compile_einsum | 6.52 | 1.43x | 0.79x | 2.11 | 1.32e-04 |
| torch_compile_tiled_tuned | 8.17 | 1.14x | 0.63x | 4.13 | 1.32e-04 |
| numpy_weighted_gram | 9.04 | 1.03x | 0.57x | 0.00 | 1.00e-05 |
| numpy_einsum | 9.33 | 1.00x | 0.55x | 0.00 | 1.00e-05 |
| helion_eager | 9.91 | 0.94x | 0.52x | 0.00 | 1.32e-04 |
| numba_blas_fused | 10.41 | 0.90x | 0.50x | 0.00 | 1.00e-05 |
| torch_tiled_tuned | 11.88 | 0.79x | 0.44x | 0.00 | 1.32e-04 |
| triton_cpu_native | 13.48 | 0.69x | 0.38x | 21.14 | 1.73e-04 |
| jax_chunked_tuned | 15.07 | 0.62x | 0.34x | 11.09 | 9.63e-05 |
| jax_einsum | 16.72 | 0.56x | 0.31x | 28.87 | 1.04e-04 |
| helion_tiled_tuned | 22.20 | 0.42x | 0.23x | 0.00 | 1.32e-04 |
| helion_triton_cpu | 37.69 | 0.25x | 0.14x | 0.00 | 1.73e-04 |
| numba_jblock_tuned | 58.37 | 0.16x | 0.09x | 0.00 | 2.21e-03 |
| numba_k_chunk_tabmat | 112.62 | 0.08x | 0.05x | 0.00 | 2.21e-03 |
| numba_fused_tuned | 134.39 | 0.07x | 0.04x | 0.00 | 2.21e-03 |
| numba_tabmat_style_st | 139.41 | 0.07x | 0.04x | 0.00 | 2.21e-03 |
| numba_rival_st | 140.65 | 0.07x | 0.04x | 0.00 | 2.21e-03 |

Best: **tabmat** (5.17 ms). tabmat: 5.17 ms (1.00x vs best).
