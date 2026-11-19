# Iteration 04 — Helion, torch.compile, and Triton-CPU

## Goal

Bring PyTorch/Helion into the main harness, then add the experimental [triton-cpu](https://github.com/triton-lang/triton-cpu) backend and MT tile/chunk tuning for Triton-based paths.

## Sources

| Piece | Link |
|---|---|
| Helion kernel DSL | [`kernels/helion_kernel.py`](https://github.com/ogrisel/cursor-sandbox/blob/cursor/sandwich-fused-kernels-000a/sandwich_fused_kernels/kernels/helion_kernel.py) |
| NumPy entry points | [`kernels/helion_baseline.py`](https://github.com/ogrisel/cursor-sandbox/blob/cursor/sandwich-fused-kernels-000a/sandwich_fused_kernels/kernels/helion_baseline.py) |
| Triton-CPU module | [`kernels/triton_cpu_kernel.py`](https://github.com/ogrisel/cursor-sandbox/blob/cursor/sandwich-fused-kernels-000a/sandwich_fused_kernels/kernels/triton_cpu_kernel.py) |
| `torch_compile_triton_cpu` | [`L326–L346`](https://github.com/ogrisel/cursor-sandbox/blob/cursor/sandwich-fused-kernels-000a/sandwich_fused_kernels/kernels/triton_cpu_kernel.py#L326-L346) |
| `torch_compile_triton_tiled` | [`L349–L372`](https://github.com/ogrisel/cursor-sandbox/blob/cursor/sandwich-fused-kernels-000a/sandwich_fused_kernels/kernels/triton_cpu_kernel.py#L349-L372) |
| Tuned wrappers | [`sandwich_torch_compile_triton_tuned`](https://github.com/ogrisel/cursor-sandbox/blob/cursor/sandwich-fused-kernels-000a/sandwich_fused_kernels/kernels/tuned_kernels.py#L250-L273) |
| Build script | [`build_triton_cpu.sh`](https://github.com/ogrisel/cursor-sandbox/blob/cursor/sandwich-fused-kernels-000a/sandwich_fused_kernels/build_triton_cpu.sh) |

## Helion / Torch (CPU)

Helion’s Triton path targets GPU; on CPU we mostly use eager / tiled PyTorch and `torch.compile`.

| Path | Complexity | Role |
|---|---|---|
| `helion_eager` | Low | Correctness / reference tile interpreter |
| `torch_einsum` / `torch_compile_einsum` | Low | Often competitive ST vs tabmat |
| `helion_tiled_tuned` / `torch_tiled_tuned` | Medium | Big ST wins on tall/skinny after tile search |

## Triton-CPU paths

| Kernel | Strategy |
|---|---|
| `triton_cpu_native` | Hand-written `@triton.jit` row-chunked Gram; optional ThreadPool row bands |
| `helion_triton_cpu` | Helion→Triton; falls back to native on codegen failure |
| `torch_compile_triton_cpu` | `torch.compile(einsum)` + Inductor `cpu_backend=triton` |
| `torch_compile_triton_tuned` | Autotuned tiled compile on the same backend |

### Single-thread highlight (glm_small f64, earlier ST run)

| Kernel | median (ms) | vs tabmat |
|---|---:|---:|
| tabmat | 6.88 | 1.00× |
| **torch_compile_triton_cpu** | **4.15** | **1.66×** |
| triton_cpu_native | 16.28 | 0.42× |

### Multi-thread highlight (glm_tall_skinny f64, latest)

| Kernel | median (ms) | vs tabmat |
|---|---:|---:|
| **torch_compile_triton_tuned** | **7.63** | **2.63×** |
| triton_cpu_tuned | 15.54 | 1.29× |
| torch_compile_triton_cpu | 18.34 | 1.09× |
| tabmat | 20.07 | 1.00× |

On **glm_small** MT, the *untuned* einsum path (`torch_compile_triton_cpu`, ~1.03× tabmat) still beat the tiled autotuned variant — more tuning infrastructure does not always win every shape.

## Ops cost

- Build experimental triton-cpu into a dedicated venv.
- Set `TRITON_CPU_BACKEND=1`.
- Manage Inductor / Dynamo recompile limits across shapes and tiles.
- Persist per-problem tile params in `autotune_cache.json`.

## Takeaway

Triton-CPU is the **highest complexity** stack in this experiment, but it uniquely **wins tall/skinny MT** via tiled `torch.compile`. For most GLM shapes, `numba_blas_tuned` remains the better ROI.
