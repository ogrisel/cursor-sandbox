# Sandwich benchmark report (single + multi threaded)

Threading: **single** (1 threads)

## glm_small

| kernel | median (ms) | vs numpy_einsum | vs tabmat | peak RSS Δ (MB) | max rel err |
|---|---:|---:|---:|---:|---:|
| tabmat | 2.45 | 6.57x | 1.00x | 0.00 | 5.34e-13 |
| numba_blas_tuned | 2.46 | 6.54x | 1.00x | 0.00 | 4.57e-13 |
| xsimd_tuned | 2.48 | 6.47x | 0.99x | 0.00 | 9.00e-13 |
| tabmat | 7.33 | 2.28x | 1.00x | 0.31 | 5.77e-13 |
| numba_blas_tiled | 7.94 | 2.02x | 0.31x | 0.00 | 4.92e-13 |
| numba_blas_kchunk_mt | 7.98 | 2.01x | 0.31x | 6.16 | 3.24e-13 |
| numba_fused_tuned | 9.76 | 1.65x | 0.25x | 0.00 | 3.26e-13 |
| jax_einsum | 11.24 | 1.49x | 0.65x | 57.04 | 7.23e-05 |
| jax_chunked_tuned | 12.93 | 1.24x | 0.19x | 1.05 | 1.55e-04 |
| jax_einsum | 13.34 | 1.20x | 0.18x | 22.79 | 7.23e-05 |
| numba_jblock_tuned | 13.67 | 1.18x | 0.18x | 0.00 | 1.66e-12 |
| jax_chunked_tuned | 13.86 | 1.21x | 0.53x | 35.53 | 1.16e-04 |
| numpy_weighted_gram | 15.41 | 1.04x | 0.16x | 0.00 | 0.00e+00 |
| numpy_weighted_gram | 15.94 | 1.05x | 0.46x | 0.00 | 3.16e-14 |
| numpy_einsum | 16.07 | 1.00x | 0.15x | 0.00 | 0.00e+00 |
| numba_blas_fused | 16.55 | 0.97x | 0.15x | 0.09 | 0.00e+00 |
| numpy_einsum | 16.76 | 1.00x | 0.44x | 0.00 | 3.16e-14 |
| numba_blas_fused | 17.92 | 0.93x | 0.41x | 0.32 | 3.16e-14 |
| numba_tabmat_style_mt | 19.50 | 0.82x | 0.13x | 0.00 | 1.66e-12 |
| numba_k_chunk_tabmat | 22.20 | 0.72x | 0.11x | 0.00 | 9.00e-13 |
| numba_rival_mt | 22.75 | 0.71x | 0.11x | 0.00 | 9.00e-13 |
| numba_fused_blocked | 26.24 | 0.61x | 0.09x | 0.00 | 1.62e-12 |
| numba_jblock_tuned | 38.49 | 0.44x | 0.19x | 0.00 | 1.66e-12 |
| numba_k_chunk_tabmat | 71.40 | 0.23x | 0.10x | 0.00 | 1.66e-12 |
| numba_fused_tuned | 78.30 | 0.21x | 0.09x | 0.00 | 1.66e-12 |
| numba_rival_st | 84.48 | 0.20x | 0.09x | 0.00 | 1.66e-12 |
| numba_tabmat_style_st | 84.75 | 0.20x | 0.09x | 0.00 | 1.66e-12 |

Best: **tabmat** (2.45 ms). tabmat: 7.33 ms (3.00x vs best).

## glm_medium

| kernel | median (ms) | vs numpy_einsum | vs tabmat | peak RSS Δ (MB) | max rel err |
|---|---:|---:|---:|---:|---:|
| numba_blas_tuned | 10.30 | 8.43x | 1.84x | 0.00 | 3.01e-12 |
| tabmat | 18.91 | 4.59x | 1.00x | 0.07 | 5.45e-12 |
| xsimd_tuned | 20.06 | 4.33x | 0.94x | 0.00 | 7.72e-12 |
| numba_blas_tiled | 52.59 | 1.65x | 0.36x | 0.00 | 1.03e-12 |
| numba_blas_kchunk_mt | 54.68 | 1.59x | 0.35x | 42.63 | 1.67e-12 |
| tabmat | 67.48 | 1.48x | 1.00x | 0.00 | 4.59e-12 |
| numba_fused_tuned | 78.28 | 1.11x | 0.24x | 0.00 | 7.72e-12 |
| numpy_weighted_gram | 85.67 | 1.01x | 0.22x | 0.00 | 0.00e+00 |
| numpy_einsum | 86.83 | 1.00x | 0.22x | 0.00 | 0.00e+00 |
| numba_blas_fused | 90.49 | 0.96x | 0.21x | 0.01 | 0.00e+00 |
| numpy_weighted_gram | 98.67 | 1.01x | 0.68x | 0.00 | 0.00e+00 |
| numpy_einsum | 100.10 | 1.00x | 0.67x | 0.09 | 0.00e+00 |
| jax_einsum | 104.95 | 0.83x | 0.18x | 43.00 | 1.35e-03 |
| numba_jblock_tuned | 106.00 | 0.82x | 0.18x | 0.00 | 1.74e-11 |
| numba_blas_fused | 107.60 | 0.93x | 0.63x | 0.27 | 0.00e+00 |
| jax_chunked_tuned | 107.65 | 0.81x | 0.18x | 42.71 | 1.79e-03 |
| jax_einsum | 113.25 | 0.88x | 0.60x | 43.45 | 1.35e-03 |
| jax_chunked_tuned | 120.96 | 0.83x | 0.56x | 44.95 | 6.96e-04 |
| numba_fused_blocked | 153.60 | 0.57x | 0.12x | 0.00 | 1.45e-11 |
| numba_tabmat_style_mt | 195.00 | 0.45x | 0.10x | 0.00 | 1.74e-11 |
| numba_rival_mt | 245.86 | 0.35x | 0.08x | 0.00 | 1.55e-11 |
| numba_k_chunk_tabmat | 253.44 | 0.34x | 0.07x | 0.00 | 1.55e-11 |
| numba_jblock_tuned | 427.90 | 0.23x | 0.16x | 0.00 | 1.74e-11 |
| numba_k_chunk_tabmat | 877.23 | 0.11x | 0.08x | 0.00 | 1.74e-11 |
| numba_fused_tuned | 931.66 | 0.11x | 0.07x | 0.00 | 1.74e-11 |
| numba_rival_st | 969.53 | 0.10x | 0.07x | 0.00 | 1.74e-11 |
| numba_tabmat_style_st | 971.78 | 0.10x | 0.07x | 0.00 | 1.74e-11 |

Best: **numba_blas_tuned** (10.30 ms). tabmat: 67.48 ms (6.55x vs best).

## glm_tall_skinny

| kernel | median (ms) | vs numpy_einsum | vs tabmat | peak RSS Δ (MB) | max rel err |
|---|---:|---:|---:|---:|---:|
| numba_blas_tuned | 5.86 | 14.40x | 1.99x | 0.00 | 5.83e-13 |
| xsimd_tuned | 9.12 | 9.25x | 1.28x | 0.00 | 7.83e-13 |
| tabmat | 11.64 | 7.25x | 1.00x | 0.00 | 2.98e-13 |
| numba_fused_tuned | 35.49 | 2.38x | 0.33x | 0.00 | 7.83e-13 |
| tabmat | 42.22 | 1.99x | 1.00x | 0.00 | 4.63e-13 |
| numba_blas_tiled | 44.74 | 1.89x | 0.26x | 0.00 | 5.12e-13 |
| numba_blas_kchunk_mt | 48.06 | 1.76x | 0.24x | 0.00 | 3.65e-13 |
| numba_jblock_tuned | 66.09 | 1.28x | 0.18x | 0.00 | 1.75e-12 |
| numpy_weighted_gram | 81.35 | 1.04x | 0.14x | 0.00 | 0.00e+00 |
| numpy_weighted_gram | 82.92 | 1.01x | 0.51x | 0.00 | 0.00e+00 |
| numpy_einsum | 84.12 | 1.00x | 0.50x | 0.00 | 0.00e+00 |
| numpy_einsum | 84.35 | 1.00x | 0.14x | 0.00 | 0.00e+00 |
| numba_blas_fused | 88.14 | 0.96x | 0.13x | 0.00 | 0.00e+00 |
| jax_chunked_tuned | 90.08 | 0.94x | 0.13x | 40.17 | 1.00e-04 |
| numba_blas_fused | 90.73 | 0.93x | 0.47x | 0.00 | 0.00e+00 |
| jax_einsum | 98.15 | 0.86x | 0.12x | 38.95 | 1.96e-04 |
| jax_einsum | 103.32 | 0.81x | 0.41x | 39.80 | 1.96e-04 |
| numba_tabmat_style_mt | 106.59 | 0.79x | 0.11x | 0.00 | 1.75e-12 |
| jax_chunked_tuned | 107.25 | 0.78x | 0.39x | 40.38 | 6.18e-05 |
| numba_k_chunk_tabmat | 107.41 | 0.79x | 0.11x | 0.00 | 7.83e-13 |
| numba_rival_mt | 107.55 | 0.78x | 0.11x | 0.00 | 7.83e-13 |
| numba_fused_blocked | 135.33 | 0.62x | 0.09x | 0.00 | 1.68e-12 |
| numba_jblock_tuned | 162.17 | 0.52x | 0.26x | 0.00 | 1.75e-12 |
| numba_k_chunk_tabmat | 306.53 | 0.27x | 0.14x | 0.00 | 1.75e-12 |
| numba_fused_tuned | 327.08 | 0.26x | 0.13x | 0.00 | 1.75e-12 |
| numba_tabmat_style_st | 361.86 | 0.23x | 0.12x | 0.00 | 1.75e-12 |
| numba_rival_st | 363.98 | 0.23x | 0.12x | 0.00 | 1.75e-12 |

Best: **numba_blas_tuned** (5.86 ms). tabmat: 42.22 ms (7.21x vs best).

## glm_square_cols

| kernel | median (ms) | vs numpy_einsum | vs tabmat | peak RSS Δ (MB) | max rel err |
|---|---:|---:|---:|---:|---:|
| numba_blas_tuned | 10.83 | 6.73x | 1.88x | 0.00 | 2.59e-12 |
| tabmat | 20.33 | 3.58x | 1.00x | 0.00 | 4.63e-12 |
| xsimd_tuned | 21.79 | 3.34x | 0.93x | 0.00 | 2.11e-11 |
| numba_blas_tiled | 44.98 | 1.62x | 0.45x | 0.00 | 3.86e-12 |
| numba_blas_kchunk_mt | 47.02 | 1.55x | 0.43x | 0.25 | 4.99e-12 |
| numpy_weighted_gram | 72.75 | 1.00x | 0.28x | 0.00 | 0.00e+00 |
| numpy_einsum | 72.86 | 1.00x | 0.28x | 0.00 | 0.00e+00 |
| tabmat | 79.32 | 1.63x | 1.00x | 0.00 | 2.25e-12 |
| numba_blas_fused | 79.57 | 0.92x | 0.26x | 0.76 | 1.03e-12 |
| jax_einsum | 91.56 | 0.80x | 0.22x | 36.52 | 3.43e-03 |
| jax_chunked_tuned | 92.87 | 0.78x | 0.22x | 41.11 | 2.89e-03 |
| numba_fused_tuned | 94.40 | 0.77x | 0.22x | 0.00 | 1.68e-11 |
| jax_chunked_tuned | 97.72 | 1.32x | 0.81x | 40.25 | 2.03e-03 |
| jax_einsum | 111.79 | 1.16x | 0.71x | 37.73 | 3.43e-03 |
| numba_blas_fused | 121.11 | 1.07x | 0.65x | 0.27 | 0.00e+00 |
| numba_jblock_tuned | 125.24 | 0.58x | 0.16x | 0.00 | 1.74e-11 |
| numba_fused_blocked | 128.49 | 0.57x | 0.16x | 0.00 | 1.66e-11 |
| numpy_einsum | 129.32 | 1.00x | 0.61x | 0.12 | 0.00e+00 |
| numpy_weighted_gram | 138.53 | 0.93x | 0.57x | 0.00 | 0.00e+00 |
| numba_tabmat_style_mt | 247.49 | 0.29x | 0.08x | 0.00 | 1.74e-11 |
| numba_k_chunk_tabmat | 292.67 | 0.25x | 0.07x | 0.00 | 1.95e-11 |
| numba_rival_mt | 294.12 | 0.25x | 0.07x | 0.00 | 1.95e-11 |
| numba_jblock_tuned | 607.16 | 0.21x | 0.13x | 0.00 | 1.74e-11 |
| numba_k_chunk_tabmat | 1223.21 | 0.11x | 0.06x | 0.00 | 1.74e-11 |
| numba_fused_tuned | 1304.80 | 0.10x | 0.06x | 0.00 | 1.74e-11 |
| numba_rival_st | 1325.19 | 0.10x | 0.06x | 0.00 | 1.74e-11 |
| numba_tabmat_style_st | 1327.57 | 0.10x | 0.06x | 0.00 | 1.74e-11 |

Best: **numba_blas_tuned** (10.83 ms). tabmat: 79.32 ms (7.32x vs best).

## glm_small_f32

| kernel | median (ms) | vs numpy_einsum | vs tabmat | peak RSS Δ (MB) | max rel err |
|---|---:|---:|---:|---:|---:|
| numba_blas_tuned | 1.46 | 6.72x | 1.10x | 0.00 | 2.61e-04 |
| tabmat | 1.61 | 6.13x | 1.00x | 0.77 | 1.90e-04 |
| tabmat | 5.02 | 1.78x | 1.00x | 0.00 | 1.60e-04 |
| numba_blas_kchunk_mt | 6.15 | 1.60x | 0.26x | 0.50 | 1.95e-04 |
| numba_blas_tiled | 6.30 | 1.56x | 0.25x | 40.89 | 2.06e-04 |
| numpy_weighted_gram | 8.31 | 1.07x | 0.60x | 0.00 | 1.00e-05 |
| jax_einsum | 8.42 | 1.17x | 0.19x | 0.00 | 1.04e-04 |
| numba_fused_tuned | 8.60 | 1.14x | 0.19x | 0.00 | 8.88e-04 |
| numba_blas_fused | 8.80 | 1.01x | 0.57x | 14.03 | 1.00e-05 |
| numpy_einsum | 8.92 | 1.00x | 0.56x | 0.00 | 1.00e-05 |
| numba_blas_fused | 8.94 | 1.10x | 0.18x | 0.00 | 0.00e+00 |
| jax_chunked_tuned | 9.13 | 1.08x | 0.18x | 0.33 | 1.29e-04 |
| jax_einsum | 9.23 | 0.97x | 0.54x | 13.66 | 1.04e-04 |
| numpy_weighted_gram | 9.48 | 1.04x | 0.17x | 0.00 | 0.00e+00 |
| numpy_einsum | 9.84 | 1.00x | 0.16x | 0.00 | 0.00e+00 |
| jax_chunked_tuned | 11.72 | 0.76x | 0.43x | 8.51 | 9.63e-05 |
| numba_jblock_tuned | 12.87 | 0.76x | 0.12x | 0.00 | 2.21e-03 |
| numba_tabmat_style_mt | 18.07 | 0.54x | 0.09x | 6.49 | 2.21e-03 |
| numba_fused_blocked | 21.39 | 0.46x | 0.08x | 6.14 | 2.21e-03 |
| numba_rival_mt | 21.41 | 0.46x | 0.08x | 0.00 | 6.43e-04 |
| numba_k_chunk_tabmat | 21.55 | 0.46x | 0.07x | 0.00 | 6.43e-04 |
| numba_jblock_tuned | 37.30 | 0.24x | 0.13x | 0.00 | 2.21e-03 |
| numba_k_chunk_tabmat | 72.76 | 0.12x | 0.07x | 0.00 | 2.21e-03 |
| numba_fused_tuned | 77.75 | 0.11x | 0.06x | 0.00 | 2.21e-03 |
| numba_rival_st | 82.48 | 0.11x | 0.06x | 0.37 | 2.21e-03 |
| numba_tabmat_style_st | 83.64 | 0.11x | 0.06x | 0.00 | 2.21e-03 |

Best: **numba_blas_tuned** (1.46 ms). tabmat: 5.02 ms (3.43x vs best).
