# Sandwich benchmark report

## glm_small

| kernel | median (ms) | vs numpy_einsum | vs tabmat | peak RSS Δ (MB) | max rel err |
|---|---:|---:|---:|---:|---:|
| tabmat | 2.28 | 6.46x | 1.00x | 0.14 | 5.63e-13 |
| jax_tensordot | 8.35 | 1.77x | 0.27x | 1.12 | 7.23e-05 |
| jax_weighted_gram | 8.45 | 1.75x | 0.27x | 22.94 | 7.23e-05 |
| jax_einsum | 8.89 | 1.66x | 0.26x | 78.45 | 7.23e-05 |
| numba_k_parallel | 12.96 | 1.14x | 0.18x | 2.39 | 3.55e-13 |
| numpy_weighted_gram | 14.08 | 1.05x | 0.16x | 0.00 | 0.00e+00 |
| numba_blas_fused | 14.22 | 1.04x | 0.16x | 0.00 | 0.00e+00 |
| numpy_diag_matmul | 14.33 | 1.03x | 0.16x | 0.00 | 1.83e-13 |
| numpy_einsum | 14.76 | 1.00x | 0.15x | 0.06 | 0.00e+00 |
| numba_blas_chunked | 43.79 | 0.34x | 0.05x | 5.63 | 4.18e-13 |
| numba_parallel | 72.67 | 0.20x | 0.03x | 0.00 | 1.58e-12 |
| numba_serial | 178.28 | 0.08x | 0.01x | 15.58 | 1.55e-12 |
| numba_blocked | 345.43 | 0.04x | 0.01x | 0.00 | 1.62e-12 |

Best: **tabmat** (2.28 ms). tabmat: 2.28 ms (1.00x vs best).

## glm_medium

| kernel | median (ms) | vs numpy_einsum | vs tabmat | peak RSS Δ (MB) | max rel err |
|---|---:|---:|---:|---:|---:|
| tabmat | 17.81 | 4.19x | 1.00x | 0.33 | 4.49e-12 |
| numpy_weighted_gram | 72.46 | 1.03x | 0.25x | 0.00 | 0.00e+00 |
| numpy_diag_matmul | 72.73 | 1.02x | 0.24x | 0.00 | 2.90e-12 |
| numpy_einsum | 74.53 | 1.00x | 0.24x | 0.00 | 0.00e+00 |
| numba_blas_chunked | 108.50 | 0.69x | 0.16x | 15.20 | 2.44e-12 |
| jax_tensordot | 109.53 | 0.68x | 0.16x | 42.66 | 1.35e-03 |
| jax_einsum | 111.92 | 0.67x | 0.16x | 43.98 | 1.35e-03 |
| jax_weighted_gram | 112.78 | 0.66x | 0.16x | 42.66 | 1.35e-03 |
| numba_blas_fused | 119.27 | 0.62x | 0.15x | 0.00 | 0.00e+00 |
| numba_k_parallel | 152.31 | 0.49x | 0.12x | 19.32 | 2.50e-12 |
| numba_parallel | 1351.44 | 0.06x | 0.01x | 0.00 | 1.12e-11 |
| numba_serial | 3101.96 | 0.02x | 0.01x | 0.00 | 1.39e-11 |
| numba_blocked | 3939.23 | 0.02x | 0.00x | 0.00 | 1.45e-11 |

Best: **tabmat** (17.81 ms). tabmat: 17.81 ms (1.00x vs best).

## glm_tall_skinny

| kernel | median (ms) | vs numpy_einsum | vs tabmat | peak RSS Δ (MB) | max rel err |
|---|---:|---:|---:|---:|---:|
| tabmat | 18.24 | 4.14x | 1.00x | 0.00 | 5.52e-13 |
| numba_blas_chunked | 65.31 | 1.16x | 0.28x | 0.00 | 2.14e-13 |
| numpy_weighted_gram | 74.29 | 1.02x | 0.25x | 0.00 | 0.00e+00 |
| numpy_einsum | 75.55 | 1.00x | 0.24x | 0.00 | 0.00e+00 |
| numba_blas_fused | 80.56 | 0.94x | 0.23x | 0.00 | 0.00e+00 |
| numba_k_parallel | 86.05 | 0.88x | 0.21x | 0.00 | 3.43e-13 |
| jax_einsum | 89.33 | 0.85x | 0.20x | 39.69 | 1.96e-04 |
| numpy_diag_matmul | 93.81 | 0.81x | 0.19x | 0.00 | 4.32e-13 |
| jax_weighted_gram | 96.96 | 0.78x | 0.19x | 39.45 | 1.96e-04 |
| jax_tensordot | 106.68 | 0.71x | 0.17x | 39.44 | 1.96e-04 |
| numba_parallel | 368.46 | 0.21x | 0.05x | 0.00 | 1.68e-12 |
| numba_serial | 958.19 | 0.08x | 0.02x | 0.00 | 1.62e-12 |
| numba_blocked | 1913.39 | 0.04x | 0.01x | 0.00 | 1.68e-12 |

Best: **tabmat** (18.24 ms). tabmat: 18.24 ms (1.00x vs best).

## glm_square_cols

| kernel | median (ms) | vs numpy_einsum | vs tabmat | peak RSS Δ (MB) | max rel err |
|---|---:|---:|---:|---:|---:|
| tabmat | 21.68 | 4.44x | 1.00x | 0.13 | 5.27e-12 |
| numba_blas_chunked | 83.53 | 1.15x | 0.26x | 8.35 | 2.29e-12 |
| numpy_weighted_gram | 94.29 | 1.02x | 0.23x | 0.00 | 0.00e+00 |
| numba_blas_fused | 95.16 | 1.01x | 0.23x | 0.00 | 1.03e-12 |
| numpy_diag_matmul | 95.53 | 1.01x | 0.23x | 0.00 | 3.26e-12 |
| numpy_einsum | 96.34 | 1.00x | 0.23x | 0.00 | 0.00e+00 |
| jax_tensordot | 97.13 | 0.99x | 0.22x | 36.51 | 3.43e-03 |
| jax_weighted_gram | 98.30 | 0.98x | 0.22x | 37.02 | 3.43e-03 |
| jax_einsum | 101.92 | 0.95x | 0.21x | 38.48 | 3.43e-03 |
| numba_k_parallel | 153.19 | 0.63x | 0.14x | 0.07 | 9.81e-12 |
| numba_parallel | 1215.71 | 0.08x | 0.02x | 0.00 | 1.56e-11 |
| numba_serial | 2839.50 | 0.03x | 0.01x | 0.00 | 1.57e-11 |
| numba_blocked | 3235.56 | 0.03x | 0.01x | 0.00 | 1.66e-11 |

Best: **tabmat** (21.68 ms). tabmat: 21.68 ms (1.00x vs best).

## glm_small_f32

| kernel | median (ms) | vs numpy_einsum | vs tabmat | peak RSS Δ (MB) | max rel err |
|---|---:|---:|---:|---:|---:|
| tabmat | 1.55 | 11.77x | 1.00x | 0.77 | 2.01e-04 |
| numba_blas_fused | 11.25 | 1.62x | 0.14x | 0.00 | 0.00e+00 |
| numba_k_parallel | 11.50 | 1.59x | 0.13x | 25.45 | 1.79e-04 |
| jax_einsum | 12.30 | 1.48x | 0.13x | 29.77 | 1.04e-04 |
| jax_tensordot | 12.37 | 1.47x | 0.13x | 0.00 | 1.68e-04 |
| jax_weighted_gram | 13.45 | 1.36x | 0.12x | 0.26 | 1.68e-04 |
| numpy_diag_matmul | 17.53 | 1.04x | 0.09x | 0.00 | 1.65e-04 |
| numpy_weighted_gram | 17.55 | 1.04x | 0.09x | 0.00 | 0.00e+00 |
| numpy_einsum | 18.23 | 1.00x | 0.08x | 0.00 | 0.00e+00 |
| numba_blas_chunked | 52.89 | 0.34x | 0.03x | 35.82 | 1.44e-04 |
| numba_parallel | 57.59 | 0.32x | 0.03x | 12.04 | 2.00e-03 |
| numba_serial | 149.90 | 0.12x | 0.01x | 0.10 | 1.93e-03 |
| numba_blocked | 286.35 | 0.06x | 0.01x | 0.00 | 2.21e-03 |

Best: **tabmat** (1.55 ms). tabmat: 1.55 ms (1.00x vs best).
