# Sandwich benchmark report (single-threaded)

Threading: **single** (1 threads)

## glm_small

| kernel | median (ms) | vs numpy_einsum | vs tabmat | peak RSS Δ (MB) | max rel err |
|---|---:|---:|---:|---:|---:|
| torch_einsum | 7.92 | 2.74x | 1.02x | 0.00 | 1.83e-13 |
| tabmat | 8.10 | 2.67x | 1.00x | 0.33 | 5.77e-13 |
| torch_compile_einsum | 8.85 | 2.45x | 0.92x | 1.35 | 4.52e-13 |
| helion_eager | 10.12 | 2.14x | 0.80x | 0.00 | 1.83e-13 |
| jax_chunked_tuned | 13.01 | 1.67x | 0.62x | 19.61 | 1.16e-04 |
| torch_compile_tiled_tuned | 13.96 | 1.55x | 0.58x | 8.66 | 4.52e-13 |
| jax_einsum | 15.45 | 1.40x | 0.52x | 73.10 | 7.23e-05 |
| torch_tiled_tuned | 17.15 | 1.26x | 0.47x | 0.00 | 1.83e-13 |
| numpy_weighted_gram | 21.08 | 1.03x | 0.38x | 0.00 | 3.16e-14 |
| numpy_einsum | 21.68 | 1.00x | 0.37x | 0.00 | 3.16e-14 |
| numba_blas_fused | 22.30 | 0.97x | 0.36x | 0.32 | 3.16e-14 |
| helion_tiled_tuned | 28.21 | 0.77x | 0.29x | 0.00 | 4.64e-13 |
| numba_jblock_tuned | 39.00 | 0.56x | 0.21x | 0.00 | 1.66e-12 |
| numba_k_chunk_tabmat | 70.13 | 0.31x | 0.12x | 0.00 | 1.66e-12 |
| numba_fused_tuned | 77.27 | 0.28x | 0.10x | 0.00 | 1.66e-12 |
| numba_rival_st | 85.95 | 0.25x | 0.09x | 0.00 | 1.66e-12 |
| numba_tabmat_style_st | 89.85 | 0.24x | 0.09x | 0.00 | 1.66e-12 |

Best: **torch_einsum** (7.92 ms). tabmat: 8.10 ms (1.02x vs best).

## glm_medium

| kernel | median (ms) | vs numpy_einsum | vs tabmat | peak RSS Δ (MB) | max rel err |
|---|---:|---:|---:|---:|---:|
| torch_einsum | 67.54 | 1.58x | 1.05x | 0.00 | 2.90e-12 |
| tabmat | 70.59 | 1.51x | 1.00x | 0.00 | 4.59e-12 |
| helion_eager | 70.82 | 1.51x | 1.00x | 0.00 | 2.90e-12 |
| torch_compile_einsum | 78.19 | 1.37x | 0.90x | 0.04 | 2.70e-12 |
| torch_compile_tiled_tuned | 86.36 | 1.24x | 0.82x | 81.26 | 1.94e-12 |
| numpy_einsum | 106.82 | 1.00x | 0.66x | 0.09 | 0.00e+00 |
| numpy_weighted_gram | 108.96 | 0.98x | 0.65x | 0.00 | 0.00e+00 |
| jax_einsum | 109.12 | 0.98x | 0.65x | 43.05 | 1.35e-03 |
| helion_tiled_tuned | 110.59 | 0.97x | 0.64x | 0.00 | 2.52e-12 |
| jax_chunked_tuned | 122.32 | 0.87x | 0.58x | 44.16 | 6.96e-04 |
| numba_blas_fused | 122.64 | 0.87x | 0.58x | 0.27 | 0.00e+00 |
| torch_tiled_tuned | 173.69 | 0.62x | 0.41x | 0.00 | 4.13e-12 |
| numba_jblock_tuned | 429.28 | 0.25x | 0.16x | 0.00 | 1.74e-11 |
| numba_k_chunk_tabmat | 855.03 | 0.12x | 0.08x | 0.00 | 1.74e-11 |
| numba_fused_tuned | 885.40 | 0.12x | 0.08x | 0.00 | 1.74e-11 |
| numba_tabmat_style_st | 946.88 | 0.11x | 0.07x | 0.00 | 1.74e-11 |
| numba_rival_st | 987.53 | 0.11x | 0.07x | 0.00 | 1.74e-11 |

Best: **torch_einsum** (67.54 ms). tabmat: 70.59 ms (1.05x vs best).

## glm_tall_skinny

| kernel | median (ms) | vs numpy_einsum | vs tabmat | peak RSS Δ (MB) | max rel err |
|---|---:|---:|---:|---:|---:|
| torch_tiled_tuned | 39.59 | 2.23x | 1.39x | 0.00 | 6.10e-13 |
| helion_tiled_tuned | 45.76 | 1.93x | 1.20x | 5.41 | 6.10e-13 |
| torch_compile_tiled_tuned | 52.42 | 1.68x | 1.05x | 0.46 | 4.45e-13 |
| tabmat | 55.02 | 1.60x | 1.00x | 0.00 | 4.63e-13 |
| torch_einsum | 70.84 | 1.25x | 0.78x | 0.00 | 4.32e-13 |
| torch_compile_einsum | 84.48 | 1.04x | 0.65x | 0.03 | 9.35e-13 |
| numpy_einsum | 88.20 | 1.00x | 0.62x | 0.00 | 0.00e+00 |
| numpy_weighted_gram | 89.80 | 0.98x | 0.61x | 0.00 | 0.00e+00 |
| helion_eager | 90.20 | 0.98x | 0.61x | 0.00 | 4.32e-13 |
| jax_chunked_tuned | 118.35 | 0.75x | 0.46x | 42.92 | 6.18e-05 |
| numba_blas_fused | 142.34 | 0.62x | 0.39x | 0.00 | 0.00e+00 |
| numba_jblock_tuned | 197.15 | 0.45x | 0.28x | 0.00 | 1.75e-12 |
| jax_einsum | 212.58 | 0.41x | 0.26x | 39.14 | 1.96e-04 |
| numba_fused_tuned | 394.11 | 0.22x | 0.14x | 0.00 | 1.75e-12 |
| numba_k_chunk_tabmat | 471.92 | 0.19x | 0.12x | 0.00 | 1.75e-12 |
| numba_tabmat_style_st | 606.50 | 0.15x | 0.09x | 0.00 | 1.75e-12 |
| numba_rival_st | 679.71 | 0.13x | 0.08x | 0.00 | 1.75e-12 |

Best: **torch_tiled_tuned** (39.59 ms). tabmat: 55.02 ms (1.39x vs best).

## glm_square_cols

| kernel | median (ms) | vs numpy_einsum | vs tabmat | peak RSS Δ (MB) | max rel err |
|---|---:|---:|---:|---:|---:|
| torch_einsum | 86.64 | 1.80x | 1.29x | 0.00 | 3.26e-12 |
| helion_eager | 97.54 | 1.60x | 1.15x | 0.00 | 3.26e-12 |
| torch_compile_einsum | 101.06 | 1.55x | 1.11x | 0.03 | 6.96e-12 |
| tabmat | 112.11 | 1.39x | 1.00x | 0.00 | 2.25e-12 |
| jax_einsum | 123.56 | 1.26x | 0.91x | 37.73 | 3.43e-03 |
| torch_compile_tiled_tuned | 126.97 | 1.23x | 0.88x | 0.00 | 7.53e-12 |
| torch_tiled_tuned | 135.08 | 1.16x | 0.83x | 7.99 | 8.77e-12 |
| numpy_weighted_gram | 137.89 | 1.13x | 0.81x | 0.00 | 0.00e+00 |
| numba_blas_fused | 146.63 | 1.07x | 0.76x | 0.27 | 0.00e+00 |
| helion_tiled_tuned | 148.38 | 1.05x | 0.76x | 0.00 | 4.62e-12 |
| numpy_einsum | 156.22 | 1.00x | 0.72x | 0.12 | 0.00e+00 |
| jax_chunked_tuned | 159.53 | 0.98x | 0.70x | 39.12 | 2.03e-03 |
| numba_jblock_tuned | 913.07 | 0.17x | 0.12x | 0.00 | 1.74e-11 |
| numba_k_chunk_tabmat | 1158.57 | 0.13x | 0.10x | 0.00 | 1.74e-11 |
| numba_fused_tuned | 1371.42 | 0.11x | 0.08x | 0.00 | 1.74e-11 |
| numba_tabmat_style_st | 2104.29 | 0.07x | 0.05x | 0.00 | 1.74e-11 |
| numba_rival_st | 2121.39 | 0.07x | 0.05x | 0.00 | 1.74e-11 |

Best: **torch_einsum** (86.64 ms). tabmat: 112.11 ms (1.29x vs best).

## glm_small_f32

| kernel | median (ms) | vs numpy_einsum | vs tabmat | peak RSS Δ (MB) | max rel err |
|---|---:|---:|---:|---:|---:|
| torch_compile_einsum | 5.15 | 3.11x | 1.70x | 1.36 | 1.32e-04 |
| torch_einsum | 6.44 | 2.49x | 1.36x | 0.00 | 1.32e-04 |
| torch_compile_tiled_tuned | 6.60 | 2.43x | 1.32x | 0.51 | 1.32e-04 |
| tabmat | 8.74 | 1.83x | 1.00x | 0.00 | 1.60e-04 |
| helion_eager | 9.95 | 1.61x | 0.88x | 0.00 | 1.32e-04 |
| torch_tiled_tuned | 11.42 | 1.40x | 0.77x | 0.00 | 1.32e-04 |
| jax_chunked_tuned | 12.11 | 1.32x | 0.72x | 0.00 | 9.63e-05 |
| numpy_weighted_gram | 15.28 | 1.05x | 0.57x | 0.00 | 1.00e-05 |
| numba_blas_fused | 15.76 | 1.02x | 0.55x | 0.00 | 1.00e-05 |
| numpy_einsum | 16.02 | 1.00x | 0.55x | 0.00 | 1.00e-05 |
| jax_einsum | 16.80 | 0.95x | 0.52x | 0.00 | 1.04e-04 |
| helion_tiled_tuned | 19.79 | 0.81x | 0.44x | 0.00 | 1.32e-04 |
| numba_jblock_tuned | 44.25 | 0.36x | 0.20x | 0.00 | 2.21e-03 |
| numba_fused_tuned | 97.24 | 0.16x | 0.09x | 0.00 | 2.21e-03 |
| numba_k_chunk_tabmat | 108.18 | 0.15x | 0.08x | 0.00 | 2.21e-03 |
| numba_rival_st | 144.28 | 0.11x | 0.06x | 0.00 | 2.21e-03 |
| numba_tabmat_style_st | 149.58 | 0.11x | 0.06x | 0.00 | 2.21e-03 |

Best: **torch_compile_einsum** (5.15 ms). tabmat: 8.74 ms (1.70x vs best).
