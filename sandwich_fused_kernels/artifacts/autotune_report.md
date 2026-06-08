# Autotune report

Threading: **single** (1 threads)

| problem | family | params | median (ms) | vs tabmat | max rel err |
|---|---|---|---:|---:|---:|
| glm_medium | helion_tiled | `{"block": 4, "n_chunks": 1, "jax_chunk": 4096, "xsimd_block": 4, "xsimd_chunk_factor": 4, "tile_m": 64, "tile_n": 64, "tile_k": 16384}` | 55.70 | 1.63x | 2.52e-12 |
| glm_medium | torch_tiled | `{"block": 4, "n_chunks": 1, "jax_chunk": 4096, "xsimd_block": 4, "xsimd_chunk_factor": 4, "tile_m": 64, "tile_n": 64, "tile_k": 4096}` | 69.54 | 1.30x | 4.13e-12 |
| glm_small | helion_tiled | `{"block": 4, "n_chunks": 1, "jax_chunk": 4096, "xsimd_block": 4, "xsimd_chunk_factor": 4, "tile_m": 32, "tile_n": 32, "tile_k": 32768}` | 13.94 | 0.55x | 4.64e-13 |
| glm_small | torch_tiled | `{"block": 4, "n_chunks": 1, "jax_chunk": 4096, "xsimd_block": 4, "xsimd_chunk_factor": 4, "tile_m": 32, "tile_n": 32, "tile_k": 50000}` | 12.89 | 0.60x | 1.83e-13 |
| glm_small_f32 | helion_tiled | `{"block": 4, "n_chunks": 1, "jax_chunk": 4096, "xsimd_block": 4, "xsimd_chunk_factor": 4, "tile_m": 32, "tile_n": 32, "tile_k": 50000}` | 6.22 | 0.75x | 1.32e-04 |
| glm_small_f32 | torch_tiled | `{"block": 4, "n_chunks": 1, "jax_chunk": 4096, "xsimd_block": 4, "xsimd_chunk_factor": 4, "tile_m": 32, "tile_n": 32, "tile_k": 50000}` | 4.88 | 0.96x | 1.32e-04 |
| glm_square_cols | helion_tiled | `{"block": 4, "n_chunks": 1, "jax_chunk": 4096, "xsimd_block": 4, "xsimd_chunk_factor": 4, "tile_m": 64, "tile_n": 64, "tile_k": 16384}` | 59.64 | 1.23x | 4.62e-12 |
| glm_square_cols | torch_tiled | `{"block": 4, "n_chunks": 1, "jax_chunk": 4096, "xsimd_block": 4, "xsimd_chunk_factor": 4, "tile_m": 64, "tile_n": 64, "tile_k": 32768}` | 49.35 | 1.48x | 8.77e-12 |
| glm_tall_skinny | helion_tiled | `{"block": 4, "n_chunks": 1, "jax_chunk": 4096, "xsimd_block": 4, "xsimd_chunk_factor": 4, "tile_m": 32, "tile_n": 32, "tile_k": 32768}` | 24.73 | 2.62x | 6.10e-13 |
| glm_tall_skinny | torch_tiled | `{"block": 4, "n_chunks": 1, "jax_chunk": 4096, "xsimd_block": 4, "xsimd_chunk_factor": 4, "tile_m": 32, "tile_n": 32, "tile_k": 32768}` | 19.29 | 3.36x | 6.10e-13 |