# Sandwich fused kernels — experiment journal

Pure-Python (and a few native) explorations of fused `X^\top \operatorname{diag}(d) X` on CPU, compared against [tabmat](https://github.com/Quantco/tabmat).

**Question:** can Numba, JAX, Helion/PyTorch, Triton-CPU, or a small xsimd extension reach tabmat latency without shipping tabmat itself?

## Latest verdict (4-thread MT, linux-amd64)

| Problem | Winner | vs tabmat | Source |
|---|---|---:|---|
| glm_small f64 | `numba_blas_tuned` | **1.43×** | [tuned dispatch](https://github.com/ogrisel/cursor-sandbox/blob/cursor/sandwich-fused-kernels-000a/sandwich_fused_kernels/kernels/tuned_kernels.py#L87-L104) |
| glm_medium f64 | `numba_blas_tuned` | **1.94×** | same |
| glm_tall_skinny f64 | `torch_compile_triton_tuned` | **2.63×** | [tiled triton compile](https://github.com/ogrisel/cursor-sandbox/blob/cursor/sandwich-fused-kernels-000a/sandwich_fused_kernels/kernels/triton_cpu_kernel.py#L349-L372) |
| glm_square_cols f64 | `numba_blas_tuned` | **1.87×** | [tuned dispatch](https://github.com/ogrisel/cursor-sandbox/blob/cursor/sandwich-fused-kernels-000a/sandwich_fused_kernels/kernels/tuned_kernels.py#L87-L104) |
| glm_small f32 | tabmat / near-ties | ~1.0× | [tabmat wrapper](https://github.com/ogrisel/cursor-sandbox/blob/cursor/sandwich-fused-kernels-000a/sandwich_fused_kernels/kernels/tabmat_baseline.py) |

Full latest tables and plots: [05 — latest benchmarks](05-latest-benchmarks/report.md).

Overview plot: [complexity vs performance](00-overview/report.md).

## Chronological iterations

0. [Complexity vs performance](00-overview/report.md) — qualitative map of backends.
1. [Tabmat baseline & root causes](01-tabmat-baseline/report.md) — why tabmat wins; NumPy/JAX/Numba baselines.
2. [SIMD inspection & fused rivals](02-simd-and-rivals/report.md) — disassembly; rejected scatter-vectorized Numba; rival MT kernels.
3. [Chunk/tile autotuning](03-autotuning/report.md) — Numba BLAS / xsimd / Helion tile search; first kernels that beat tabmat MT.
4. [Helion, torch.compile & Triton-CPU](04-helion-triton/report.md) — PyTorch/Helion paths and experimental triton-cpu backend (ST + MT).
5. [Latest consolidated benchmarks](05-latest-benchmarks/report.md) — current ST/MT tables, plots, source map.

## Key source map

| Component | Path |
|---|---|
| Benchmark harness | [`benchmark_sandwich.py`](https://github.com/ogrisel/cursor-sandbox/blob/cursor/sandwich-fused-kernels-000a/sandwich_fused_kernels/benchmark_sandwich.py) |
| Autotuner | [`autotune_sandwich.py`](https://github.com/ogrisel/cursor-sandbox/blob/cursor/sandwich-fused-kernels-000a/sandwich_fused_kernels/autotune_sandwich.py) |
| Numba kernels | [`kernels/numba_kernels.py`](https://github.com/ogrisel/cursor-sandbox/blob/cursor/sandwich-fused-kernels-000a/sandwich_fused_kernels/kernels/numba_kernels.py) |
| Tuned dispatch | [`kernels/tuned_kernels.py`](https://github.com/ogrisel/cursor-sandbox/blob/cursor/sandwich-fused-kernels-000a/sandwich_fused_kernels/kernels/tuned_kernels.py) |
| xsimd C++ | [`xsimd_ext/sandwich_xsimd.cpp`](https://github.com/ogrisel/cursor-sandbox/blob/cursor/sandwich-fused-kernels-000a/sandwich_fused_kernels/xsimd_ext/sandwich_xsimd.cpp) |
| Helion / Torch | [`kernels/helion_kernel.py`](https://github.com/ogrisel/cursor-sandbox/blob/cursor/sandwich-fused-kernels-000a/sandwich_fused_kernels/kernels/helion_kernel.py) |
| Triton-CPU | [`kernels/triton_cpu_kernel.py`](https://github.com/ogrisel/cursor-sandbox/blob/cursor/sandwich-fused-kernels-000a/sandwich_fused_kernels/kernels/triton_cpu_kernel.py) |
| Narrative README | [`README.md`](https://github.com/ogrisel/cursor-sandbox/blob/cursor/sandwich-fused-kernels-000a/sandwich_fused_kernels/README.md) |

## Reproduce

```bash
# Core ST/MT benchmark (NumPy / tabmat / Numba / JAX)
uv run --python 3.11 --exclude-newer P7D \
  --with tabmat --with numba --with jax --with jaxlib --with scipy \
  --with threadpoolctl --with psutil \
  python sandwich_fused_kernels/benchmark_sandwich.py

# Helion + Triton-CPU (after build_triton_cpu.sh)
TRITON_CPU_BACKEND=1 sandwich_fused_kernels/.venv-helion/bin/python \
  sandwich_fused_kernels/benchmark_sandwich.py
```
