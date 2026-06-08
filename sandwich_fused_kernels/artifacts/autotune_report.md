# Autotune report

Threading: **multi** (4 threads)

| problem | family | params | median (ms) | vs tabmat | max rel err |
|---|---|---|---:|---:|---:|
| glm_medium | jax_chunked | `{"block": 4, "n_chunks": 1, "jax_chunk": 4375, "xsimd_block": 4, "xsimd_chunk_factor": 4}` | 102.56 | 0.18x | 1.79e-03 |
| glm_medium | numba_blas_mt | `{"block": 4, "n_chunks": 128, "jax_chunk": 4096, "xsimd_block": 4, "xsimd_chunk_factor": 4}` | 10.10 | 1.82x | 3.01e-12 |
| glm_medium | numba_fused_mt | `{"block": 16, "n_chunks": 64, "jax_chunk": 4096, "xsimd_block": 4, "xsimd_chunk_factor": 4}` | 78.38 | 0.23x | 7.72e-12 |
| glm_medium | numba_jblock_mt | `{"block": 16, "n_chunks": 1, "jax_chunk": 4096, "xsimd_block": 4, "xsimd_chunk_factor": 4}` | 105.81 | 0.17x | 1.74e-11 |
| glm_medium | xsimd_mt | `{"block": 4, "n_chunks": 1, "jax_chunk": 4096, "xsimd_block": 32, "xsimd_chunk_factor": 16}` | 18.93 | 0.97x | 7.72e-12 |
| glm_small | jax_chunked | `{"block": 4, "n_chunks": 1, "jax_chunk": 3125, "xsimd_block": 4, "xsimd_chunk_factor": 4}` | 12.18 | 0.19x | 1.55e-04 |
| glm_small | numba_blas_mt | `{"block": 4, "n_chunks": 128, "jax_chunk": 4096, "xsimd_block": 4, "xsimd_chunk_factor": 4}` | 1.73 | 1.35x | 4.57e-13 |
| glm_small | numba_fused_mt | `{"block": 32, "n_chunks": 32, "jax_chunk": 4096, "xsimd_block": 4, "xsimd_chunk_factor": 4}` | 9.56 | 0.24x | 3.26e-13 |
| glm_small | numba_jblock_mt | `{"block": 8, "n_chunks": 1, "jax_chunk": 4096, "xsimd_block": 4, "xsimd_chunk_factor": 4}` | 12.93 | 0.18x | 1.66e-12 |
| glm_small | xsimd_mt | `{"block": 4, "n_chunks": 1, "jax_chunk": 4096, "xsimd_block": 32, "xsimd_chunk_factor": 4}` | 2.28 | 1.02x | 9.00e-13 |
| glm_small_f32 | jax_chunked | `{"block": 4, "n_chunks": 1, "jax_chunk": 6250, "xsimd_block": 4, "xsimd_chunk_factor": 4}` | 9.14 | 0.18x | 1.29e-04 |
| glm_small_f32 | numba_blas_mt | `{"block": 4, "n_chunks": 128, "jax_chunk": 4096, "xsimd_block": 4, "xsimd_chunk_factor": 4}` | 0.93 | 1.78x | 2.61e-04 |
| glm_small_f32 | numba_fused_mt | `{"block": 16, "n_chunks": 8, "jax_chunk": 4096, "xsimd_block": 4, "xsimd_chunk_factor": 4}` | 8.52 | 0.19x | 8.88e-04 |
| glm_small_f32 | numba_jblock_mt | `{"block": 8, "n_chunks": 1, "jax_chunk": 4096, "xsimd_block": 4, "xsimd_chunk_factor": 4}` | 12.78 | 0.13x | 2.21e-03 |
| glm_small_f32 | xsimd_mt | `{"block": 4, "n_chunks": 1, "jax_chunk": 4096, "xsimd_block": 4, "xsimd_chunk_factor": 4}` | inf | 0.00x | 0.00e+00 |
| glm_square_cols | jax_chunked | `{"block": 4, "n_chunks": 1, "jax_chunk": 20000, "xsimd_block": 4, "xsimd_chunk_factor": 4}` | 88.82 | 0.23x | 2.89e-03 |
| glm_square_cols | numba_blas_mt | `{"block": 4, "n_chunks": 32, "jax_chunk": 4096, "xsimd_block": 4, "xsimd_chunk_factor": 4}` | 11.76 | 1.74x | 2.59e-12 |
| glm_square_cols | numba_fused_mt | `{"block": 32, "n_chunks": 32, "jax_chunk": 4096, "xsimd_block": 4, "xsimd_chunk_factor": 4}` | 94.17 | 0.22x | 1.68e-11 |
| glm_square_cols | numba_jblock_mt | `{"block": 32, "n_chunks": 1, "jax_chunk": 4096, "xsimd_block": 4, "xsimd_chunk_factor": 4}` | 125.34 | 0.16x | 1.74e-11 |
| glm_square_cols | xsimd_mt | `{"block": 4, "n_chunks": 1, "jax_chunk": 4096, "xsimd_block": 64, "xsimd_chunk_factor": 2}` | 20.85 | 0.98x | 2.11e-11 |
| glm_tall_skinny | jax_chunked | `{"block": 4, "n_chunks": 1, "jax_chunk": 5000, "xsimd_block": 4, "xsimd_chunk_factor": 4}` | 91.70 | 0.13x | 1.00e-04 |
| glm_tall_skinny | numba_blas_mt | `{"block": 4, "n_chunks": 128, "jax_chunk": 4096, "xsimd_block": 4, "xsimd_chunk_factor": 4}` | 6.02 | 1.98x | 5.83e-13 |
| glm_tall_skinny | numba_fused_mt | `{"block": 16, "n_chunks": 16, "jax_chunk": 4096, "xsimd_block": 4, "xsimd_chunk_factor": 4}` | 35.47 | 0.34x | 7.83e-13 |
| glm_tall_skinny | numba_jblock_mt | `{"block": 8, "n_chunks": 1, "jax_chunk": 4096, "xsimd_block": 4, "xsimd_chunk_factor": 4}` | 68.30 | 0.17x | 1.75e-12 |
| glm_tall_skinny | xsimd_mt | `{"block": 4, "n_chunks": 1, "jax_chunk": 4096, "xsimd_block": 32, "xsimd_chunk_factor": 4}` | 8.88 | 1.34x | 7.83e-13 |