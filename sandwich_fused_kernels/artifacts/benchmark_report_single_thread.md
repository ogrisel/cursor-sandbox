# Sandwich benchmark report (single-threaded)

Threading: **single** (1 threads)

## glm_small

| kernel | median (ms) | vs numpy_einsum | vs tabmat | peak RSS Δ (MB) | max rel err |
|---|---:|---:|---:|---:|---:|
| torch_einsum | 6.20 | 2.40x | 1.15x | 0.00 | 1.83e-13 |
| torch_compile_einsum | 6.40 | 2.32x | 1.11x | 10.65 | 4.52e-13 |
| tabmat | 7.12 | 2.09x | 1.00x | 0.32 | 5.77e-13 |
| helion_eager | 7.20 | 2.07x | 0.99x | 0.43 | 1.83e-13 |
| jax_einsum | 11.19 | 1.33x | 0.64x | 70.18 | 7.23e-05 |
| numpy_einsum | 14.87 | 1.00x | 0.48x | 0.00 | 3.16e-14 |
| numpy_weighted_gram | 16.01 | 0.93x | 0.44x | 0.00 | 3.16e-14 |
| numba_blas_fused | 17.43 | 0.85x | 0.41x | 0.32 | 3.16e-14 |
| numba_k_chunk_tabmat | 73.33 | 0.20x | 0.10x | 0.00 | 1.66e-12 |
| numba_rival_st | 84.66 | 0.18x | 0.08x | 0.00 | 1.66e-12 |
| numba_tabmat_style_st | 85.20 | 0.17x | 0.08x | 0.00 | 1.66e-12 |

Best: **torch_einsum** (6.20 ms). tabmat: 7.12 ms (1.15x vs best).

## glm_medium

| kernel | median (ms) | vs numpy_einsum | vs tabmat | peak RSS Δ (MB) | max rel err |
|---|---:|---:|---:|---:|---:|
| torch_einsum | 66.66 | 1.69x | 1.02x | 0.00 | 2.90e-12 |
| tabmat | 68.31 | 1.65x | 1.00x | 0.00 | 4.59e-12 |
| helion_eager | 69.86 | 1.61x | 0.98x | 0.00 | 2.90e-12 |
| torch_compile_einsum | 71.09 | 1.59x | 0.96x | 0.26 | 2.70e-12 |
| numpy_weighted_gram | 102.89 | 1.10x | 0.66x | 0.00 | 0.00e+00 |
| jax_einsum | 105.99 | 1.06x | 0.64x | 44.29 | 1.35e-03 |
| numba_blas_fused | 111.82 | 1.01x | 0.61x | 0.27 | 0.00e+00 |
| numpy_einsum | 112.77 | 1.00x | 0.61x | 0.09 | 0.00e+00 |
| numba_k_chunk_tabmat | 836.78 | 0.13x | 0.08x | 0.00 | 1.74e-11 |
| numba_rival_st | 938.50 | 0.12x | 0.07x | 0.00 | 1.74e-11 |
| numba_tabmat_style_st | 943.39 | 0.12x | 0.07x | 0.00 | 1.74e-11 |

Best: **torch_einsum** (66.66 ms). tabmat: 68.31 ms (1.02x vs best).

## glm_tall_skinny

| kernel | median (ms) | vs numpy_einsum | vs tabmat | peak RSS Δ (MB) | max rel err |
|---|---:|---:|---:|---:|---:|
| tabmat | 43.07 | 1.94x | 1.00x | 0.00 | 4.63e-13 |
| torch_einsum | 53.96 | 1.55x | 0.80x | 0.00 | 4.32e-13 |
| helion_eager | 55.71 | 1.50x | 0.77x | 0.00 | 4.32e-13 |
| torch_compile_einsum | 68.17 | 1.23x | 0.63x | 0.23 | 9.35e-13 |
| numpy_weighted_gram | 81.00 | 1.03x | 0.53x | 0.00 | 0.00e+00 |
| numpy_einsum | 83.63 | 1.00x | 0.51x | 0.00 | 0.00e+00 |
| numba_blas_fused | 90.50 | 0.92x | 0.48x | 0.00 | 0.00e+00 |
| jax_einsum | 95.58 | 0.88x | 0.45x | 39.71 | 1.96e-04 |
| numba_k_chunk_tabmat | 308.43 | 0.27x | 0.14x | 0.00 | 1.75e-12 |
| numba_tabmat_style_st | 373.00 | 0.22x | 0.12x | 0.00 | 1.75e-12 |
| numba_rival_st | 377.62 | 0.22x | 0.11x | 0.00 | 1.75e-12 |

Best: **tabmat** (43.07 ms). tabmat: 43.07 ms (1.00x vs best).

## glm_square_cols

| kernel | median (ms) | vs numpy_einsum | vs tabmat | peak RSS Δ (MB) | max rel err |
|---|---:|---:|---:|---:|---:|
| torch_einsum | 64.86 | 1.42x | 1.14x | 0.00 | 3.26e-12 |
| torch_compile_einsum | 66.72 | 1.38x | 1.11x | 0.23 | 6.96e-12 |
| helion_eager | 68.20 | 1.35x | 1.09x | 0.01 | 3.26e-12 |
| tabmat | 74.10 | 1.24x | 1.00x | 0.00 | 2.25e-12 |
| numpy_einsum | 92.18 | 1.00x | 0.80x | 0.12 | 0.00e+00 |
| jax_einsum | 93.53 | 0.99x | 0.79x | 39.20 | 3.43e-03 |
| numpy_weighted_gram | 96.69 | 0.95x | 0.77x | 0.00 | 0.00e+00 |
| numba_blas_fused | 100.73 | 0.92x | 0.74x | 0.27 | 0.00e+00 |
| numba_k_chunk_tabmat | 1311.30 | 0.07x | 0.06x | 0.00 | 1.74e-11 |
| numba_rival_st | 1390.02 | 0.07x | 0.05x | 0.00 | 1.74e-11 |
| numba_tabmat_style_st | 1400.28 | 0.07x | 0.05x | 0.00 | 1.74e-11 |

Best: **torch_einsum** (64.86 ms). tabmat: 74.10 ms (1.14x vs best).

## glm_small_f32

| kernel | median (ms) | vs numpy_einsum | vs tabmat | peak RSS Δ (MB) | max rel err |
|---|---:|---:|---:|---:|---:|
| torch_compile_einsum | 3.80 | 2.47x | 1.32x | 1.28 | 1.32e-04 |
| torch_einsum | 4.97 | 1.89x | 1.01x | 0.00 | 1.32e-04 |
| tabmat | 5.04 | 1.87x | 1.00x | 0.00 | 1.60e-04 |
| helion_eager | 5.91 | 1.59x | 0.85x | 0.00 | 1.32e-04 |
| numba_blas_fused | 8.87 | 1.06x | 0.57x | 23.23 | 1.00e-05 |
| jax_einsum | 9.30 | 1.01x | 0.54x | 7.47 | 1.04e-04 |
| numpy_weighted_gram | 9.36 | 1.00x | 0.54x | 0.00 | 1.00e-05 |
| numpy_einsum | 9.40 | 1.00x | 0.54x | 0.00 | 1.00e-05 |
| numba_k_chunk_tabmat | 67.95 | 0.14x | 0.07x | 35.90 | 2.21e-03 |
| numba_tabmat_style_st | 81.74 | 0.11x | 0.06x | 0.00 | 2.21e-03 |
| numba_rival_st | 81.74 | 0.11x | 0.06x | 1.38 | 2.21e-03 |

Best: **torch_compile_einsum** (3.80 ms). tabmat: 5.04 ms (1.32x vs best).
