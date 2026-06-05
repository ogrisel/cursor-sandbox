# Sandwich benchmark report

## glm_small

| kernel | median (ms) | vs numpy_einsum | vs tabmat | peak RSS Δ (MB) | max rel err |
|---|---:|---:|---:|---:|---:|
| tabmat | 2.32 | 8.88x | 1.00x | 0.11 | 5.26e-13 |
| jax_weighted_gram | 10.68 | 1.93x | 0.22x | 23.97 | 7.23e-05 |
| jax_tensordot | 11.55 | 1.79x | 0.20x | 15.07 | 7.23e-05 |
| jax_einsum | 11.81 | 1.75x | 0.20x | 15.42 | 7.23e-05 |
| jax_scan_chunked | 12.43 | 1.66x | 0.19x | 17.00 | 1.16e-04 |
| numba_blas_fused | 13.01 | 1.59x | 0.18x | 12.88 | 0.00e+00 |
| numba_k_parallel | 14.30 | 1.44x | 0.16x | 1.91 | 3.55e-13 |
| jax_einsum_chunked | 14.90 | 1.38x | 0.16x | 10.55 | 1.16e-04 |
| numpy_weighted_gram | 19.76 | 1.04x | 0.12x | 0.00 | 0.00e+00 |
| numpy_einsum | 20.63 | 1.00x | 0.11x | 0.06 | 0.00e+00 |
| numpy_diag_matmul | 20.97 | 0.98x | 0.11x | 0.00 | 1.83e-13 |
| numba_fused_blocked | 26.98 | 0.76x | 0.09x | 0.00 | 1.62e-12 |
| numba_blas_chunked | 46.05 | 0.45x | 0.05x | 5.62 | 4.18e-13 |
| numba_blas_tiled | 54.71 | 0.38x | 0.04x | 0.82 | 4.61e-13 |
| numba_parallel | 86.48 | 0.24x | 0.03x | 14.49 | 1.58e-12 |
| numba_serial | 180.87 | 0.11x | 0.01x | 21.44 | 1.55e-12 |

Best: **tabmat** (2.32 ms). tabmat: 2.32 ms (1.00x vs best).

## glm_medium

| kernel | median (ms) | vs numpy_einsum | vs tabmat | peak RSS Δ (MB) | max rel err |
|---|---:|---:|---:|---:|---:|
| tabmat | 20.48 | 5.77x | 1.00x | 0.32 | 4.40e-12 |
| numba_blas_fused | 81.56 | 1.45x | 0.25x | 0.00 | 0.00e+00 |
| jax_weighted_gram | 90.03 | 1.31x | 0.23x | 42.40 | 1.35e-03 |
| jax_einsum | 91.81 | 1.29x | 0.22x | 43.68 | 1.35e-03 |
| jax_tensordot | 92.73 | 1.27x | 0.22x | 42.92 | 1.35e-03 |
| numba_blas_chunked | 94.61 | 1.25x | 0.22x | 14.36 | 2.44e-12 |
| numpy_weighted_gram | 100.78 | 1.17x | 0.20x | 0.00 | 0.00e+00 |
| numpy_diag_matmul | 103.09 | 1.15x | 0.20x | 0.00 | 2.90e-12 |
| jax_einsum_chunked | 108.03 | 1.09x | 0.19x | 43.22 | 6.96e-04 |
| jax_scan_chunked | 111.08 | 1.06x | 0.18x | 45.18 | 6.96e-04 |
| numba_blas_tiled | 117.24 | 1.01x | 0.17x | 0.00 | 1.03e-12 |
| numpy_einsum | 118.07 | 1.00x | 0.17x | 0.00 | 0.00e+00 |
| numba_fused_blocked | 151.26 | 0.78x | 0.14x | 0.00 | 1.45e-11 |
| numba_k_parallel | 160.27 | 0.74x | 0.13x | 4.66 | 2.50e-12 |
| numba_parallel | 1255.46 | 0.09x | 0.02x | 0.00 | 1.12e-11 |
| numba_serial | 3084.94 | 0.04x | 0.01x | 0.00 | 1.39e-11 |

Best: **tabmat** (20.48 ms). tabmat: 20.48 ms (1.00x vs best).

## glm_tall_skinny

| kernel | median (ms) | vs numpy_einsum | vs tabmat | peak RSS Δ (MB) | max rel err |
|---|---:|---:|---:|---:|---:|
| tabmat | 10.61 | 6.46x | 1.00x | 0.00 | 2.63e-13 |
| numpy_weighted_gram | 67.62 | 1.01x | 0.16x | 0.00 | 0.00e+00 |
| numba_blas_tiled | 68.37 | 1.00x | 0.16x | 0.00 | 5.12e-13 |
| numpy_einsum | 68.56 | 1.00x | 0.15x | 0.00 | 0.00e+00 |
| numpy_diag_matmul | 68.67 | 1.00x | 0.15x | 0.00 | 4.32e-13 |
| numba_blas_chunked | 70.75 | 0.97x | 0.15x | 0.00 | 2.14e-13 |
| jax_tensordot | 80.74 | 0.85x | 0.13x | 38.93 | 1.96e-04 |
| jax_weighted_gram | 81.39 | 0.84x | 0.13x | 39.19 | 1.96e-04 |
| jax_einsum | 81.83 | 0.84x | 0.13x | 39.19 | 1.96e-04 |
| numba_k_parallel | 82.04 | 0.84x | 0.13x | 0.00 | 3.43e-13 |
| numba_blas_fused | 85.82 | 0.80x | 0.12x | 0.00 | 0.00e+00 |
| jax_scan_chunked | 91.81 | 0.75x | 0.12x | 41.06 | 6.18e-05 |
| jax_einsum_chunked | 96.23 | 0.71x | 0.11x | 39.21 | 6.18e-05 |
| numba_fused_blocked | 131.97 | 0.52x | 0.08x | 0.00 | 1.68e-12 |
| numba_parallel | 356.07 | 0.19x | 0.03x | 0.00 | 1.68e-12 |
| numba_serial | 940.24 | 0.07x | 0.01x | 0.00 | 1.62e-12 |

Best: **tabmat** (10.61 ms). tabmat: 10.61 ms (1.00x vs best).

## glm_square_cols

| kernel | median (ms) | vs numpy_einsum | vs tabmat | peak RSS Δ (MB) | max rel err |
|---|---:|---:|---:|---:|---:|
| tabmat | 20.63 | 3.94x | 1.00x | 0.13 | 5.62e-12 |
| numpy_einsum | 81.33 | 1.00x | 0.25x | 0.00 | 0.00e+00 |
| numpy_weighted_gram | 82.46 | 0.99x | 0.25x | 0.00 | 0.00e+00 |
| numpy_diag_matmul | 89.14 | 0.91x | 0.23x | 0.00 | 3.26e-12 |
| jax_weighted_gram | 94.11 | 0.86x | 0.22x | 36.51 | 3.43e-03 |
| numba_blas_fused | 94.50 | 0.86x | 0.22x | 0.00 | 1.03e-12 |
| numba_blas_chunked | 97.57 | 0.83x | 0.21x | 8.36 | 2.29e-12 |
| jax_tensordot | 100.76 | 0.81x | 0.20x | 37.29 | 3.43e-03 |
| jax_einsum | 102.68 | 0.79x | 0.20x | 38.24 | 3.43e-03 |
| jax_einsum_chunked | 103.10 | 0.79x | 0.20x | 38.14 | 2.03e-03 |
| numba_blas_tiled | 105.08 | 0.77x | 0.20x | 0.00 | 2.03e-12 |
| jax_scan_chunked | 105.34 | 0.77x | 0.20x | 36.55 | 2.03e-03 |
| numba_fused_blocked | 136.70 | 0.59x | 0.15x | 0.00 | 1.66e-11 |
| numba_k_parallel | 155.60 | 0.52x | 0.13x | 0.48 | 9.81e-12 |
| numba_parallel | 1086.20 | 0.07x | 0.02x | 0.00 | 1.56e-11 |
| numba_serial | 2793.61 | 0.03x | 0.01x | 0.00 | 1.57e-11 |

Best: **tabmat** (20.63 ms). tabmat: 20.63 ms (1.00x vs best).

## glm_small_f32

| kernel | median (ms) | vs numpy_einsum | vs tabmat | peak RSS Δ (MB) | max rel err |
|---|---:|---:|---:|---:|---:|
| tabmat | 2.46 | 5.15x | 1.00x | 0.77 | 1.57e-04 |
| jax_einsum | 8.06 | 1.57x | 0.31x | 7.73 | 1.04e-04 |
| jax_weighted_gram | 8.17 | 1.55x | 0.30x | 0.00 | 1.68e-04 |
| jax_tensordot | 8.26 | 1.53x | 0.30x | 5.41 | 1.68e-04 |
| numba_blas_fused | 9.41 | 1.35x | 0.26x | 5.93 | 0.00e+00 |
| jax_scan_chunked | 9.47 | 1.34x | 0.26x | 1.80 | 9.63e-05 |
| jax_einsum_chunked | 9.66 | 1.31x | 0.25x | 0.00 | 1.29e-04 |
| numba_k_parallel | 11.18 | 1.13x | 0.22x | 23.03 | 1.79e-04 |
| numpy_diag_matmul | 11.52 | 1.10x | 0.21x | 0.00 | 1.65e-04 |
| numpy_weighted_gram | 11.95 | 1.06x | 0.21x | 0.00 | 0.00e+00 |
| numpy_einsum | 12.66 | 1.00x | 0.19x | 0.00 | 0.00e+00 |
| numba_fused_blocked | 19.64 | 0.64x | 0.13x | 3.54 | 2.21e-03 |
| numba_blas_tiled | 43.18 | 0.29x | 0.06x | 18.88 | 2.01e-04 |
| numba_blas_chunked | 44.20 | 0.29x | 0.06x | 35.13 | 1.44e-04 |
| numba_parallel | 65.62 | 0.19x | 0.04x | 20.95 | 2.00e-03 |
| numba_serial | 144.19 | 0.09x | 0.02x | 0.17 | 1.93e-03 |

Best: **tabmat** (2.46 ms). tabmat: 2.46 ms (1.00x vs best).
