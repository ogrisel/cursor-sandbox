# Sandwich benchmark report

## glm_small

| kernel | median (ms) | vs numpy_einsum | vs tabmat | peak RSS Δ (MB) | max rel err |
|---|---:|---:|---:|---:|---:|
| tabmat | 2.45 | 5.91x | 1.00x | 0.77 | 5.26e-13 |
| numba_blas_fused | 9.31 | 1.56x | 0.26x | 12.89 | 0.00e+00 |
| jax_tensordot | 9.72 | 1.49x | 0.25x | 0.00 | 7.23e-05 |
| jax_weighted_gram | 10.70 | 1.35x | 0.23x | 23.38 | 7.23e-05 |
| jax_scan_chunked | 11.97 | 1.21x | 0.20x | 15.86 | 1.16e-04 |
| numpy_weighted_gram | 12.95 | 1.12x | 0.19x | 0.00 | 0.00e+00 |
| jax_einsum | 12.98 | 1.12x | 0.19x | 38.68 | 7.23e-05 |
| numba_k_parallel | 13.34 | 1.09x | 0.18x | 1.66 | 3.55e-13 |
| numpy_diag_matmul | 13.61 | 1.06x | 0.18x | 0.00 | 1.83e-13 |
| jax_einsum_chunked | 14.29 | 1.01x | 0.17x | 13.18 | 1.16e-04 |
| numpy_einsum | 14.49 | 1.00x | 0.17x | 0.06 | 0.00e+00 |
| numba_fused_blocked | 24.40 | 0.59x | 0.10x | 0.00 | 1.62e-12 |
| numba_blas_chunked | 50.87 | 0.28x | 0.05x | 5.98 | 4.18e-13 |
| numba_blas_tiled | 50.90 | 0.28x | 0.05x | 0.51 | 4.61e-13 |
| numba_parallel | 83.67 | 0.17x | 0.03x | 10.57 | 1.58e-12 |
| numba_k_inner | 100.32 | 0.14x | 0.02x | 0.00 | 1.62e-12 |
| numba_serial | 177.60 | 0.08x | 0.01x | 21.96 | 1.55e-12 |

Best: **tabmat** (2.45 ms). tabmat: 2.45 ms (1.00x vs best).

## glm_medium

| kernel | median (ms) | vs numpy_einsum | vs tabmat | peak RSS Δ (MB) | max rel err |
|---|---:|---:|---:|---:|---:|
| tabmat | 21.42 | 3.78x | 1.00x | 0.00 | 4.75e-12 |
| numpy_weighted_gram | 75.64 | 1.07x | 0.28x | 0.00 | 0.00e+00 |
| numpy_diag_matmul | 77.68 | 1.04x | 0.28x | 0.00 | 2.90e-12 |
| numpy_einsum | 80.98 | 1.00x | 0.26x | 0.00 | 0.00e+00 |
| numba_blas_chunked | 83.67 | 0.97x | 0.26x | 14.39 | 2.44e-12 |
| numba_blas_fused | 84.61 | 0.96x | 0.25x | 0.00 | 0.00e+00 |
| numba_blas_tiled | 95.12 | 0.85x | 0.23x | 0.00 | 1.03e-12 |
| jax_weighted_gram | 103.14 | 0.79x | 0.21x | 42.83 | 1.35e-03 |
| jax_einsum | 106.02 | 0.76x | 0.20x | 43.27 | 1.35e-03 |
| jax_tensordot | 108.50 | 0.75x | 0.20x | 42.58 | 1.35e-03 |
| jax_scan_chunked | 109.04 | 0.74x | 0.20x | 45.61 | 6.96e-04 |
| jax_einsum_chunked | 115.82 | 0.70x | 0.18x | 43.54 | 6.96e-04 |
| numba_fused_blocked | 152.85 | 0.53x | 0.14x | 0.00 | 1.45e-11 |
| numba_k_parallel | 156.50 | 0.52x | 0.14x | 3.86 | 2.50e-12 |
| numba_parallel | 1132.54 | 0.07x | 0.02x | 0.00 | 1.12e-11 |
| numba_k_inner | 1286.90 | 0.06x | 0.02x | 0.00 | 1.45e-11 |
| numba_serial | 3031.38 | 0.03x | 0.01x | 0.00 | 1.39e-11 |

Best: **tabmat** (21.42 ms). tabmat: 21.42 ms (1.00x vs best).

## glm_tall_skinny

| kernel | median (ms) | vs numpy_einsum | vs tabmat | peak RSS Δ (MB) | max rel err |
|---|---:|---:|---:|---:|---:|
| tabmat | 11.40 | 6.66x | 1.00x | 0.00 | 6.66e-13 |
| numba_blas_chunked | 65.62 | 1.16x | 0.17x | 0.00 | 2.14e-13 |
| numpy_weighted_gram | 71.28 | 1.07x | 0.16x | 0.00 | 0.00e+00 |
| numba_blas_tiled | 72.73 | 1.04x | 0.16x | 0.00 | 5.12e-13 |
| numpy_diag_matmul | 74.78 | 1.02x | 0.15x | 0.00 | 4.32e-13 |
| numpy_einsum | 75.96 | 1.00x | 0.15x | 0.00 | 0.00e+00 |
| numba_k_parallel | 81.68 | 0.93x | 0.14x | 0.00 | 3.43e-13 |
| jax_tensordot | 88.78 | 0.86x | 0.13x | 39.21 | 1.96e-04 |
| numba_blas_fused | 88.91 | 0.85x | 0.13x | 0.00 | 0.00e+00 |
| jax_weighted_gram | 90.84 | 0.84x | 0.13x | 38.95 | 1.96e-04 |
| jax_einsum | 91.56 | 0.83x | 0.12x | 38.95 | 1.96e-04 |
| jax_einsum_chunked | 104.47 | 0.73x | 0.11x | 38.95 | 6.18e-05 |
| jax_scan_chunked | 105.03 | 0.72x | 0.11x | 40.79 | 6.18e-05 |
| numba_fused_blocked | 133.38 | 0.57x | 0.09x | 0.00 | 1.68e-12 |
| numba_parallel | 364.60 | 0.21x | 0.03x | 0.00 | 1.68e-12 |
| numba_k_inner | 416.20 | 0.18x | 0.03x | 0.00 | 1.68e-12 |
| numba_serial | 960.35 | 0.08x | 0.01x | 0.00 | 1.62e-12 |

Best: **tabmat** (11.40 ms). tabmat: 11.40 ms (1.00x vs best).

## glm_square_cols

| kernel | median (ms) | vs numpy_einsum | vs tabmat | peak RSS Δ (MB) | max rel err |
|---|---:|---:|---:|---:|---:|
| tabmat | 20.29 | 3.17x | 1.00x | 0.52 | 3.29e-12 |
| numpy_einsum | 64.22 | 1.00x | 0.32x | 0.00 | 0.00e+00 |
| numpy_weighted_gram | 64.37 | 1.00x | 0.32x | 0.00 | 0.00e+00 |
| numpy_diag_matmul | 65.28 | 0.98x | 0.31x | 0.00 | 3.26e-12 |
| numba_blas_chunked | 81.92 | 0.78x | 0.25x | 8.59 | 2.29e-12 |
| numba_blas_fused | 87.52 | 0.73x | 0.23x | 0.00 | 1.03e-12 |
| jax_einsum | 95.66 | 0.67x | 0.21x | 37.48 | 3.43e-03 |
| numba_blas_tiled | 97.54 | 0.66x | 0.21x | 0.00 | 2.03e-12 |
| jax_weighted_gram | 99.69 | 0.64x | 0.20x | 37.30 | 3.43e-03 |
| jax_tensordot | 102.31 | 0.63x | 0.20x | 36.52 | 3.43e-03 |
| jax_einsum_chunked | 111.42 | 0.58x | 0.18x | 36.98 | 2.03e-03 |
| jax_scan_chunked | 111.43 | 0.58x | 0.18x | 39.02 | 2.03e-03 |
| numba_fused_blocked | 129.90 | 0.49x | 0.16x | 0.00 | 1.66e-11 |
| numba_k_parallel | 161.00 | 0.40x | 0.13x | 0.02 | 9.81e-12 |
| numba_parallel | 1242.49 | 0.05x | 0.02x | 0.00 | 1.56e-11 |
| numba_k_inner | 1729.58 | 0.04x | 0.01x | 0.00 | 1.66e-11 |
| numba_serial | 2800.33 | 0.02x | 0.01x | 0.00 | 1.57e-11 |

Best: **tabmat** (20.29 ms). tabmat: 20.29 ms (1.00x vs best).

## glm_small_f32

| kernel | median (ms) | vs numpy_einsum | vs tabmat | peak RSS Δ (MB) | max rel err |
|---|---:|---:|---:|---:|---:|
| tabmat | 3.49 | 3.71x | 1.00x | 0.00 | 2.01e-04 |
| jax_weighted_gram | 8.28 | 1.57x | 0.42x | 0.00 | 1.68e-04 |
| numba_blas_fused | 8.31 | 1.56x | 0.42x | 6.45 | 0.00e+00 |
| jax_tensordot | 8.53 | 1.52x | 0.41x | 0.00 | 1.68e-04 |
| jax_scan_chunked | 9.61 | 1.35x | 0.36x | 3.61 | 9.63e-05 |
| jax_einsum_chunked | 9.84 | 1.32x | 0.35x | 0.00 | 1.29e-04 |
| jax_einsum | 10.14 | 1.28x | 0.34x | 0.00 | 1.04e-04 |
| numba_k_parallel | 11.56 | 1.12x | 0.30x | 32.91 | 1.79e-04 |
| numpy_diag_matmul | 12.63 | 1.03x | 0.28x | 0.00 | 1.65e-04 |
| numpy_weighted_gram | 12.65 | 1.02x | 0.28x | 0.00 | 0.00e+00 |
| numpy_einsum | 12.97 | 1.00x | 0.27x | 0.00 | 0.00e+00 |
| numba_fused_blocked | 19.68 | 0.66x | 0.18x | 3.26 | 2.21e-03 |
| numba_blas_tiled | 38.18 | 0.34x | 0.09x | 11.98 | 2.01e-04 |
| numba_blas_chunked | 39.96 | 0.32x | 0.09x | 33.95 | 1.44e-04 |
| numba_parallel | 75.42 | 0.17x | 0.05x | 21.09 | 2.00e-03 |
| numba_k_inner | 88.91 | 0.15x | 0.04x | 4.64 | 2.21e-03 |
| numba_serial | 151.13 | 0.09x | 0.02x | 0.11 | 1.93e-03 |

Best: **tabmat** (3.49 ms). tabmat: 3.49 ms (1.00x vs best).
