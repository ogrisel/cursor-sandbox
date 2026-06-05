# Sandwich benchmark report (single-threaded)

Threading: **single** (1 threads)

## glm_small

| kernel | median (ms) | vs numpy_einsum | vs tabmat | peak RSS Δ (MB) | max rel err |
|---|---:|---:|---:|---:|---:|
| tabmat | 6.59 | 2.54x | 1.00x | 0.35 | 5.77e-13 |
| jax_einsum | 9.87 | 1.70x | 0.67x | 59.49 | 7.23e-05 |
| numpy_weighted_gram | 12.70 | 1.32x | 0.52x | 0.06 | 3.16e-14 |
| numba_blas_fused | 14.35 | 1.17x | 0.46x | 0.32 | 3.16e-14 |
| numpy_einsum | 16.75 | 1.00x | 0.39x | 0.00 | 3.16e-14 |
| numba_k_chunk_tabmat | 69.07 | 0.24x | 0.10x | 0.00 | 1.66e-12 |
| numba_tabmat_style_st | 94.36 | 0.18x | 0.07x | 0.00 | 1.66e-12 |
| numba_rival_st | 94.53 | 0.18x | 0.07x | 0.00 | 1.66e-12 |

Best: **tabmat** (6.59 ms). tabmat: 6.59 ms (1.00x vs best).

## glm_medium

| kernel | median (ms) | vs numpy_einsum | vs tabmat | peak RSS Δ (MB) | max rel err |
|---|---:|---:|---:|---:|---:|
| tabmat | 65.87 | 1.36x | 1.00x | 0.00 | 4.59e-12 |
| numpy_weighted_gram | 86.40 | 1.04x | 0.76x | 0.00 | 0.00e+00 |
| numpy_einsum | 89.84 | 1.00x | 0.73x | 0.09 | 0.00e+00 |
| jax_einsum | 98.72 | 0.91x | 0.67x | 45.52 | 1.35e-03 |
| numba_blas_fused | 101.64 | 0.88x | 0.65x | 0.27 | 0.00e+00 |
| numba_k_chunk_tabmat | 847.07 | 0.11x | 0.08x | 0.00 | 1.74e-11 |
| numba_rival_st | 946.41 | 0.09x | 0.07x | 0.00 | 1.74e-11 |
| numba_tabmat_style_st | 946.95 | 0.09x | 0.07x | 0.00 | 1.74e-11 |

Best: **tabmat** (65.87 ms). tabmat: 65.87 ms (1.00x vs best).

## glm_tall_skinny

| kernel | median (ms) | vs numpy_einsum | vs tabmat | peak RSS Δ (MB) | max rel err |
|---|---:|---:|---:|---:|---:|
| tabmat | 38.62 | 1.78x | 1.00x | 0.00 | 4.63e-13 |
| numpy_weighted_gram | 67.31 | 1.02x | 0.57x | 0.00 | 0.00e+00 |
| numpy_einsum | 68.88 | 1.00x | 0.56x | 0.00 | 0.00e+00 |
| numba_blas_fused | 79.01 | 0.87x | 0.49x | 0.00 | 0.00e+00 |
| jax_einsum | 83.37 | 0.83x | 0.46x | 40.29 | 1.96e-04 |
| numba_k_chunk_tabmat | 299.59 | 0.23x | 0.13x | 0.00 | 1.75e-12 |
| numba_rival_st | 353.01 | 0.20x | 0.11x | 0.00 | 1.75e-12 |
| numba_tabmat_style_st | 361.50 | 0.19x | 0.11x | 0.00 | 1.75e-12 |

Best: **tabmat** (38.62 ms). tabmat: 38.62 ms (1.00x vs best).

## glm_square_cols

| kernel | median (ms) | vs numpy_einsum | vs tabmat | peak RSS Δ (MB) | max rel err |
|---|---:|---:|---:|---:|---:|
| tabmat | 71.29 | 1.17x | 1.00x | 0.00 | 2.25e-12 |
| numpy_weighted_gram | 78.59 | 1.06x | 0.91x | 0.00 | 0.00e+00 |
| numpy_einsum | 83.37 | 1.00x | 0.86x | 0.12 | 0.00e+00 |
| numba_blas_fused | 91.85 | 0.91x | 0.78x | 0.27 | 0.00e+00 |
| jax_einsum | 98.68 | 0.84x | 0.72x | 37.98 | 3.43e-03 |
| numba_k_chunk_tabmat | 1300.92 | 0.06x | 0.05x | 0.00 | 1.74e-11 |
| numba_rival_st | 1390.10 | 0.06x | 0.05x | 0.00 | 1.74e-11 |
| numba_tabmat_style_st | 1397.45 | 0.06x | 0.05x | 0.00 | 1.74e-11 |

Best: **tabmat** (71.29 ms). tabmat: 71.29 ms (1.00x vs best).

## glm_small_f32

| kernel | median (ms) | vs numpy_einsum | vs tabmat | peak RSS Δ (MB) | max rel err |
|---|---:|---:|---:|---:|---:|
| tabmat | 4.33 | 1.83x | 1.00x | 0.00 | 1.60e-04 |
| numpy_weighted_gram | 7.43 | 1.07x | 0.58x | 0.00 | 1.00e-05 |
| numba_blas_fused | 7.44 | 1.06x | 0.58x | 15.93 | 1.00e-05 |
| numpy_einsum | 7.92 | 1.00x | 0.55x | 0.00 | 1.00e-05 |
| jax_einsum | 8.56 | 0.93x | 0.51x | 13.92 | 1.04e-04 |
| numba_k_chunk_tabmat | 67.88 | 0.12x | 0.06x | 31.29 | 2.21e-03 |
| numba_tabmat_style_st | 80.27 | 0.10x | 0.05x | 0.00 | 2.21e-03 |
| numba_rival_st | 80.70 | 0.10x | 0.05x | 0.07 | 2.21e-03 |

Best: **tabmat** (4.33 ms). tabmat: 4.33 ms (1.00x vs best).
