# Sandwich benchmark report (single-threaded)

Threading: **single** (1 threads)

## glm_small

| kernel | median (ms) | vs numpy_einsum | vs tabmat | peak RSS Δ (MB) | max rel err |
|---|---:|---:|---:|---:|---:|
| tabmat | 7.33 | 2.28x | 1.00x | 0.31 | 5.77e-13 |
| jax_einsum | 11.24 | 1.49x | 0.65x | 57.04 | 7.23e-05 |
| jax_chunked_tuned | 13.86 | 1.21x | 0.53x | 35.53 | 1.16e-04 |
| numpy_weighted_gram | 15.94 | 1.05x | 0.46x | 0.00 | 3.16e-14 |
| numpy_einsum | 16.76 | 1.00x | 0.44x | 0.00 | 3.16e-14 |
| numba_blas_fused | 17.92 | 0.93x | 0.41x | 0.32 | 3.16e-14 |
| numba_jblock_tuned | 38.49 | 0.44x | 0.19x | 0.00 | 1.66e-12 |
| numba_k_chunk_tabmat | 71.40 | 0.23x | 0.10x | 0.00 | 1.66e-12 |
| numba_fused_tuned | 78.30 | 0.21x | 0.09x | 0.00 | 1.66e-12 |
| numba_rival_st | 84.48 | 0.20x | 0.09x | 0.00 | 1.66e-12 |
| numba_tabmat_style_st | 84.75 | 0.20x | 0.09x | 0.00 | 1.66e-12 |

Best: **tabmat** (7.33 ms). tabmat: 7.33 ms (1.00x vs best).

## glm_medium

| kernel | median (ms) | vs numpy_einsum | vs tabmat | peak RSS Δ (MB) | max rel err |
|---|---:|---:|---:|---:|---:|
| tabmat | 67.48 | 1.48x | 1.00x | 0.00 | 4.59e-12 |
| numpy_weighted_gram | 98.67 | 1.01x | 0.68x | 0.00 | 0.00e+00 |
| numpy_einsum | 100.10 | 1.00x | 0.67x | 0.09 | 0.00e+00 |
| numba_blas_fused | 107.60 | 0.93x | 0.63x | 0.27 | 0.00e+00 |
| jax_einsum | 113.25 | 0.88x | 0.60x | 43.45 | 1.35e-03 |
| jax_chunked_tuned | 120.96 | 0.83x | 0.56x | 44.95 | 6.96e-04 |
| numba_jblock_tuned | 427.90 | 0.23x | 0.16x | 0.00 | 1.74e-11 |
| numba_k_chunk_tabmat | 877.23 | 0.11x | 0.08x | 0.00 | 1.74e-11 |
| numba_fused_tuned | 931.66 | 0.11x | 0.07x | 0.00 | 1.74e-11 |
| numba_rival_st | 969.53 | 0.10x | 0.07x | 0.00 | 1.74e-11 |
| numba_tabmat_style_st | 971.78 | 0.10x | 0.07x | 0.00 | 1.74e-11 |

Best: **tabmat** (67.48 ms). tabmat: 67.48 ms (1.00x vs best).

## glm_tall_skinny

| kernel | median (ms) | vs numpy_einsum | vs tabmat | peak RSS Δ (MB) | max rel err |
|---|---:|---:|---:|---:|---:|
| tabmat | 42.22 | 1.99x | 1.00x | 0.00 | 4.63e-13 |
| numpy_weighted_gram | 82.92 | 1.01x | 0.51x | 0.00 | 0.00e+00 |
| numpy_einsum | 84.12 | 1.00x | 0.50x | 0.00 | 0.00e+00 |
| numba_blas_fused | 90.73 | 0.93x | 0.47x | 0.00 | 0.00e+00 |
| jax_einsum | 103.32 | 0.81x | 0.41x | 39.80 | 1.96e-04 |
| jax_chunked_tuned | 107.25 | 0.78x | 0.39x | 40.38 | 6.18e-05 |
| numba_jblock_tuned | 162.17 | 0.52x | 0.26x | 0.00 | 1.75e-12 |
| numba_k_chunk_tabmat | 306.53 | 0.27x | 0.14x | 0.00 | 1.75e-12 |
| numba_fused_tuned | 327.08 | 0.26x | 0.13x | 0.00 | 1.75e-12 |
| numba_tabmat_style_st | 361.86 | 0.23x | 0.12x | 0.00 | 1.75e-12 |
| numba_rival_st | 363.98 | 0.23x | 0.12x | 0.00 | 1.75e-12 |

Best: **tabmat** (42.22 ms). tabmat: 42.22 ms (1.00x vs best).

## glm_square_cols

| kernel | median (ms) | vs numpy_einsum | vs tabmat | peak RSS Δ (MB) | max rel err |
|---|---:|---:|---:|---:|---:|
| tabmat | 79.32 | 1.63x | 1.00x | 0.00 | 2.25e-12 |
| jax_chunked_tuned | 97.72 | 1.32x | 0.81x | 40.25 | 2.03e-03 |
| jax_einsum | 111.79 | 1.16x | 0.71x | 37.73 | 3.43e-03 |
| numba_blas_fused | 121.11 | 1.07x | 0.65x | 0.27 | 0.00e+00 |
| numpy_einsum | 129.32 | 1.00x | 0.61x | 0.12 | 0.00e+00 |
| numpy_weighted_gram | 138.53 | 0.93x | 0.57x | 0.00 | 0.00e+00 |
| numba_jblock_tuned | 607.16 | 0.21x | 0.13x | 0.00 | 1.74e-11 |
| numba_k_chunk_tabmat | 1223.21 | 0.11x | 0.06x | 0.00 | 1.74e-11 |
| numba_fused_tuned | 1304.80 | 0.10x | 0.06x | 0.00 | 1.74e-11 |
| numba_rival_st | 1325.19 | 0.10x | 0.06x | 0.00 | 1.74e-11 |
| numba_tabmat_style_st | 1327.57 | 0.10x | 0.06x | 0.00 | 1.74e-11 |

Best: **tabmat** (79.32 ms). tabmat: 79.32 ms (1.00x vs best).

## glm_small_f32

| kernel | median (ms) | vs numpy_einsum | vs tabmat | peak RSS Δ (MB) | max rel err |
|---|---:|---:|---:|---:|---:|
| tabmat | 5.02 | 1.78x | 1.00x | 0.00 | 1.60e-04 |
| numpy_weighted_gram | 8.31 | 1.07x | 0.60x | 0.00 | 1.00e-05 |
| numba_blas_fused | 8.80 | 1.01x | 0.57x | 14.03 | 1.00e-05 |
| numpy_einsum | 8.92 | 1.00x | 0.56x | 0.00 | 1.00e-05 |
| jax_einsum | 9.23 | 0.97x | 0.54x | 13.66 | 1.04e-04 |
| jax_chunked_tuned | 11.72 | 0.76x | 0.43x | 8.51 | 9.63e-05 |
| numba_jblock_tuned | 37.30 | 0.24x | 0.13x | 0.00 | 2.21e-03 |
| numba_k_chunk_tabmat | 72.76 | 0.12x | 0.07x | 0.00 | 2.21e-03 |
| numba_fused_tuned | 77.75 | 0.11x | 0.06x | 0.00 | 2.21e-03 |
| numba_rival_st | 82.48 | 0.11x | 0.06x | 0.37 | 2.21e-03 |
| numba_tabmat_style_st | 83.64 | 0.11x | 0.06x | 0.00 | 2.21e-03 |

Best: **tabmat** (5.02 ms). tabmat: 5.02 ms (1.00x vs best).
