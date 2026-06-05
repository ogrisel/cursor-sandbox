# Sandwich benchmark report (multi-threaded)

Threading: **multi** (4 threads)

## glm_small

| kernel | median (ms) | vs numpy_einsum | vs tabmat | peak RSS Δ (MB) | max rel err |
|---|---:|---:|---:|---:|---:|
| tabmat | 2.11 | 6.63x | 1.00x | 0.00 | 5.38e-13 |
| numba_blas_tiled | 6.34 | 2.21x | 0.33x | 0.00 | 4.92e-13 |
| numba_blas_kchunk_mt | 6.42 | 2.18x | 0.33x | 6.18 | 3.24e-13 |
| jax_einsum | 10.70 | 1.31x | 0.20x | 22.95 | 7.23e-05 |
| numba_blas_fused | 13.35 | 1.05x | 0.16x | 0.09 | 0.00e+00 |
| numpy_weighted_gram | 13.85 | 1.01x | 0.15x | 0.00 | 0.00e+00 |
| numpy_einsum | 14.02 | 1.00x | 0.15x | 0.00 | 0.00e+00 |
| numba_tabmat_style_mt | 18.77 | 0.75x | 0.11x | 0.00 | 1.66e-12 |
| numba_rival_mt | 21.24 | 0.66x | 0.10x | 0.00 | 9.00e-13 |
| numba_k_chunk_tabmat | 21.40 | 0.65x | 0.10x | 0.00 | 9.00e-13 |
| numba_fused_blocked | 23.99 | 0.58x | 0.09x | 0.00 | 1.62e-12 |

Best: **tabmat** (2.11 ms). tabmat: 2.11 ms (1.00x vs best).

## glm_medium

| kernel | median (ms) | vs numpy_einsum | vs tabmat | peak RSS Δ (MB) | max rel err |
|---|---:|---:|---:|---:|---:|
| tabmat | 21.77 | 3.43x | 1.00x | 0.00 | 3.89e-12 |
| numba_blas_tiled | 45.51 | 1.64x | 0.48x | 0.00 | 1.03e-12 |
| numba_blas_kchunk_mt | 48.92 | 1.53x | 0.45x | 37.47 | 1.67e-12 |
| numpy_einsum | 74.66 | 1.00x | 0.29x | 0.00 | 0.00e+00 |
| numpy_weighted_gram | 88.33 | 0.85x | 0.25x | 0.00 | 0.00e+00 |
| numba_blas_fused | 99.07 | 0.75x | 0.22x | 0.01 | 0.00e+00 |
| jax_einsum | 107.02 | 0.70x | 0.20x | 43.99 | 1.35e-03 |
| numba_fused_blocked | 142.31 | 0.52x | 0.15x | 0.00 | 1.45e-11 |
| numba_tabmat_style_mt | 197.13 | 0.38x | 0.11x | 0.00 | 1.74e-11 |
| numba_rival_mt | 258.81 | 0.29x | 0.08x | 0.00 | 1.55e-11 |
| numba_k_chunk_tabmat | 260.85 | 0.29x | 0.08x | 0.00 | 1.55e-11 |

Best: **tabmat** (21.77 ms). tabmat: 21.77 ms (1.00x vs best).

## glm_tall_skinny

| kernel | median (ms) | vs numpy_einsum | vs tabmat | peak RSS Δ (MB) | max rel err |
|---|---:|---:|---:|---:|---:|
| tabmat | 13.36 | 5.21x | 1.00x | 0.13 | 4.32e-13 |
| numba_blas_kchunk_mt | 39.78 | 1.75x | 0.34x | 0.00 | 3.65e-13 |
| numba_blas_tiled | 40.91 | 1.70x | 0.33x | 0.00 | 5.12e-13 |
| numpy_weighted_gram | 69.45 | 1.00x | 0.19x | 0.00 | 0.00e+00 |
| numpy_einsum | 69.61 | 1.00x | 0.19x | 0.00 | 0.00e+00 |
| numba_blas_fused | 76.77 | 0.91x | 0.17x | 0.00 | 0.00e+00 |
| jax_einsum | 99.80 | 0.70x | 0.13x | 39.78 | 1.96e-04 |
| numba_tabmat_style_mt | 108.17 | 0.64x | 0.12x | 0.00 | 1.75e-12 |
| numba_rival_mt | 108.59 | 0.64x | 0.12x | 0.00 | 7.83e-13 |
| numba_k_chunk_tabmat | 123.55 | 0.56x | 0.11x | 0.00 | 7.83e-13 |
| numba_fused_blocked | 144.32 | 0.48x | 0.09x | 0.00 | 1.68e-12 |

Best: **tabmat** (13.36 ms). tabmat: 13.36 ms (1.00x vs best).

## glm_square_cols

| kernel | median (ms) | vs numpy_einsum | vs tabmat | peak RSS Δ (MB) | max rel err |
|---|---:|---:|---:|---:|---:|
| tabmat | 20.85 | 4.55x | 1.00x | 0.14 | 3.79e-12 |
| numba_blas_tiled | 44.25 | 2.14x | 0.47x | 0.00 | 3.86e-12 |
| numba_blas_kchunk_mt | 47.28 | 2.01x | 0.44x | 0.37 | 4.99e-12 |
| numpy_einsum | 94.85 | 1.00x | 0.22x | 0.00 | 0.00e+00 |
| numpy_weighted_gram | 96.35 | 0.98x | 0.22x | 0.00 | 0.00e+00 |
| numba_blas_fused | 99.62 | 0.95x | 0.21x | 0.76 | 1.03e-12 |
| jax_einsum | 100.56 | 0.94x | 0.21x | 37.29 | 3.43e-03 |
| numba_fused_blocked | 144.41 | 0.66x | 0.14x | 0.00 | 1.66e-11 |
| numba_tabmat_style_mt | 270.15 | 0.35x | 0.08x | 0.00 | 1.74e-11 |
| numba_k_chunk_tabmat | 310.19 | 0.31x | 0.07x | 0.00 | 1.95e-11 |
| numba_rival_mt | 324.05 | 0.29x | 0.06x | 0.00 | 1.95e-11 |

Best: **tabmat** (20.85 ms). tabmat: 20.85 ms (1.00x vs best).

## glm_small_f32

| kernel | median (ms) | vs numpy_einsum | vs tabmat | peak RSS Δ (MB) | max rel err |
|---|---:|---:|---:|---:|---:|
| tabmat | 1.61 | 7.86x | 1.00x | 0.00 | 1.84e-04 |
| numba_blas_kchunk_mt | 5.64 | 2.24x | 0.28x | 12.12 | 1.95e-04 |
| numba_blas_tiled | 5.86 | 2.15x | 0.27x | 28.27 | 2.06e-04 |
| numba_blas_fused | 7.91 | 1.60x | 0.20x | 0.00 | 0.00e+00 |
| jax_einsum | 9.84 | 1.28x | 0.16x | 18.56 | 1.04e-04 |
| numpy_weighted_gram | 11.88 | 1.06x | 0.14x | 0.00 | 0.00e+00 |
| numpy_einsum | 12.63 | 1.00x | 0.13x | 0.00 | 0.00e+00 |
| numba_tabmat_style_mt | 18.40 | 0.69x | 0.09x | 1.55 | 2.21e-03 |
| numba_fused_blocked | 19.60 | 0.64x | 0.08x | 3.86 | 2.21e-03 |
| numba_rival_mt | 20.90 | 0.60x | 0.08x | 0.00 | 6.43e-04 |
| numba_k_chunk_tabmat | 21.00 | 0.60x | 0.08x | 0.00 | 6.43e-04 |

Best: **tabmat** (1.61 ms). tabmat: 1.61 ms (1.00x vs best).
