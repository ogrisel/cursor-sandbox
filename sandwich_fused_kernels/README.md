# Sandwich product fused kernels (CPU)

Pure-Python exploration of fused `X.T @ diag(d) @ X` kernels on CPU, comparing **NumPy**, **tabmat**, **Numba**, and **JAX** backends.

## High-level objective

The sandwich (Gram) product `X.T @ diag(d) @ X` is a hot path in weighted least squares and GLM Hessians. [tabmat](https://github.com/Quantco/tabmat) implements a heavily optimized C++/Cython kernel (blocked, SIMD, OpenMP). This project asks:

> Can pure Python compilers (Numba, JAX) reach similar performance without custom C extensions?

We benchmark latency, profile hot paths, and compare memory behavior against naive NumPy baselines and tabmat.

## Why tabmat is faster (root-cause analysis)

Profiling and controlled comparisons (`analyze_tabmat.py`, `artifacts/tabmat_advantage_analysis.md`) isolate five dominant causes on `glm_small` (50k×40 f64):

| Cause | tabmat | Typical NumPy / compiler path |
|---|---|---|
| **Fused row weights** | `d[k]` applied inside SIMD-blocked `k` loop | weighted Gram materializes full `n×m` scratch (~15 MB here) |
| **Specialized kernel** | Direct sandwich micro-kernel | Generic `dgemm` / `einsum` lowering with dispatch overhead |
| **Cache/SIMD blocking** | GotoBLAS-style 4×4 blocks, xsimd on inner `k` | Scalar or wide GEMM with poor reuse for this operation shape |
| **Symmetric structure** | Lower-triangle blocks, then mirror | Full matrix computed even when symmetric |
| **Memory traffic** | ~0 extra RSS beyond `X` and output | weighted paths add 1–2× read/write of `n×m` data |

On the analysis run, tabmat at **2.08 ms** was **4.9–7.5× faster** than the best compiler paths and **7.5× faster** than `numpy.einsum`.

## Speed-up strategies (planned → tested)

| Strategy | Hypothesis | Iteration 4 outcome |
|---|---|---|
| **JAX `einsum` fusion** | XLA fuses `d` into contraction without `n×m` buffer | **1.75–1.93×** vs `numpy_einsum` on `glm_small`; still **~0.20× tabmat** |
| **JAX row-chunked `scan`** | Peak memory `O(chunk×m)`; better cache | Correct, similar speed to `einsum`; no tabmat-level gain |
| **Numba BLAS single GEMM** | Delegate to OpenBLAS | **1.45–1.59×** vs `numpy_einsum`; **0.18–0.25× tabmat** |
| **Numba BLAS row chunks** | Parallel chunk GEMMs | `blas_tiled` matches NumPy on tall/skinny; chunk overhead hurts small problems |
| **Numba fused blocked loops** | Mimic tabmat without scratch buffer | **~10× faster** than old scalar loops but still **~0.09–0.14× tabmat** — LLVM does not emit competitive SIMD |

**Conclusion from experiments:** closing the tabmat gap requires either (a) a native fused SIMD kernel like tabmat's, or (b) accepting BLAS-backed paths that trade ~85 MB scratch (at glm_medium scale) for moderate speedups over `einsum`.

## Memory efficiency summary

Measured at **140k×80 float64** (`profile_memory.py`):

| Kernel | Peak RSS Δ | Materializes weighted `X` | Notes |
|---|---:|---|---|
| tabmat | 0.6 MB | No | Fused in-place accumulation |
| numpy_einsum | 0 MB | No | Best memory among naive baselines |
| jax_einsum | 1.8 MB | No | Small XLA workspace |
| jax_scan_chunked | 20 MB | No (chunk only) | Peak ∝ chunk size (4096×80×8 B ≈ 2.5 MB theoretical) |
| numba_blas_tiled | 7.6 MB | Per chunk (~2.5 MB) | Partial reduction buffers |
| numpy_weighted_gram | 0 MB* | Yes (~85 MB theoretical) | *In-place overwrite; still 2× data traffic |

**Trade-off:** tabmat is both fastest and most memory-efficient. Compiler backends that approach NumPy speed either materialize weighted row blocks (BLAS) or rely on XLA fusion (`einsum`) without reaching tabmat latency.

## SIMD inspection (iteration 5)

`inspect_simd.py` disassembles generated machine code (or dumps XLA/LLVM artifacts) and classifies SIMD families. Artifacts: `artifacts/simd_inspection.md`.

| Backend | Variant | SIMD ISA | Instructions (sample) | Vectorizes successfully? |
|---|---|---|---|---|
| **tabmat** | `dense_base` micro-kernel | **SSE128** (`xmm`) | `mulpd`, `addpd`, `movapd` | **Yes** — hand-unrolled 4×4 blocks, no gather/scatter |
| **tabmat** | `_denseC_sandwich` OpenMP | Scalar | `movsd`, `mulsd` | Setup loops only; compute is in `dense_base` |
| **NumPy/BLAS** | `dgemm_kernel_HASWELL` | **AVX2+FMA** (`ymm`) | `vfmadd231pd`, `vbroadcastsd` | **Yes** — via OpenBLAS when weighted Gram calls `dgemm` |
| **Numba** | `blas_fused` | **AVX2** (`ymm`) | `vmulpd`, `vbroadcastsd` | **Yes** — delegates to same BLAS stack |
| **Numba** | `fused_blocked` | **AVX2** (`ymm`) | `vmulpd`, `vaddpd` on block `acc` | **Partially** — SIMD on contiguous `acc`, not on full `out` |
| **Numba** | `k_inner` + `prange` | **AVX2** (`ymm`) | **`vscatterqpd`** | **No (harmful)** — auto-vectorization scatters into strided `out[i,j]` |
| **JAX** | `einsum` fusion thunk | Scalar LLVM | `fmul float` (unrolled) | **No** in fusion kernel; matmul SIMD is in XLA/Eigen **runtime** |

### Why some compilers fail to get useful SIMD

1. **Numba `k_inner`**: LLVM vectorizes the `j`/`prange` loop but stores through **gather/scatter** into the dense output matrix — more SIMD instructions, much worse performance (100 ms vs 24 ms `fused_blocked` on glm_small).
2. **Numba `fused_blocked`**: SIMD applies to **stack/block accumulators** with contiguous stores; lacks tabmat's manual 4×4 structure and still misses BLAS-level throughput.
3. **JAX `einsum`**: XLA emits a **scalar-unrolled** `broadcast_multiply_fusion` thunk; the contraction itself is lowered to runtime libraries where SIMD is opaque to our dump.
4. **tabmat vs AVX2 Numba**: tabmat uses **narrower SSE** but **better access patterns**; wider AVX2 does not help when memory patterns are wrong.

### Iteration 5 outcome

- Added `inspect_simd.py` and `numba_k_inner` experiment.
- **Rejected** `k_inner` for production: SIMD present but `vscatterqpd` makes it ~4× slower than `fused_blocked` despite fewer flops in theory.
- **Retained** `fused_blocked` and BLAS paths as best Numba options; **retained** JAX `einsum` (runtime matmul SIMD).

### Iteration 6 — single- vs multi-threaded benchmarks + rival Numba kernels

Benchmarks now report **single-threaded (1 thread)** and **multi-threaded (4 threads)** results separately via `threading_utils.sandwich_threading`, which pins Numba, OpenMP, and BLAS pools. Chunked BLAS kernels use `blas_threads=1` inside each `prange` worker to avoid oversubscription.

**New Numba kernels** (`kernels/numba_kernels.py`):

| Kernel | Threading | Strategy |
|---|---|---|
| `rival_st` / `tabmat_style_st` | Single | Block-outer 4×4 fused rank-1 updates, symmetric flush |
| `rival_mt` / `k_chunk_tabmat` | Multi | `prange` over row chunks → block-outer fused partials → sum |
| `blas_kchunk_mt` | Multi | `prange` over row chunks → single-thread `(Xc*dc).T @ Xc` per worker |
| `kouter_st` | Single | K-outer block buffers (tested; slower than block-outer on these shapes) |

**Symmetric flush bug fixed:** off-diagonal blocks (`ib > jb`) were incorrectly skipped by a `gi > gj` filter meant only for diagonal blocks.

**Rival-kernel outcome:** pure fused `rival_mt` reaches **~0.10× tabmat** on `glm_small` MT (21 ms vs 2.1 ms). The best Numba MT path is **`blas_kchunk_mt`** at **~0.33× tabmat** (6.4 ms) — still ~3× behind tabmat's fused OpenMP+SSE micro-kernel, but **~3× faster than the fused rival** and **~2× faster than `blas_fused`** on the same problem.

## Running benchmarks

From the repo root:

```bash
uv run --python 3.11 --exclude-newer P7D \
  --with tabmat --with numba --with jax --with jaxlib --with scipy --with threadpoolctl --with psutil \
  python sandwich_fused_kernels/benchmark_sandwich.py \
  --repeats 5 --warmup 2
```

Outputs:

- `artifacts/benchmark_report_single_thread.md`
- `artifacts/benchmark_report_multi_thread.md`
- `artifacts/benchmark_report.md` (combined)

Tabmat advantage analysis:

```bash
uv run --python 3.11 --exclude-newer P7D \
  --with tabmat --with numba --with jax --with jaxlib --with psutil \
  python sandwich_fused_kernels/analyze_tabmat.py
```

Memory profile:

```bash
uv run --python 3.11 --exclude-newer P7D \
  --with tabmat --with numba --with jax --with jaxlib --with psutil \
  python sandwich_fused_kernels/profile_memory.py
```

SIMD inspection:

```bash
uv run --python 3.11 --exclude-newer P7D \
  --with tabmat --with numba --with jax --with jaxlib --with scipy \
  python sandwich_fused_kernels/inspect_simd.py
```

Artifacts land in `sandwich_fused_kernels/artifacts/`.

## Experimental log

### Iterations 1–3 (initial exploration)

See git history. Key findings: scalar Numba loops uncompetitive; tabmat leads all shapes; JAX `tensordot` best compiler on small f64.

### Iteration 5 — SIMD disassembly

- Added `inspect_simd.py`; disassembled tabmat `.so`, Numba `inspect_asm()`, JAX XLA dumps, OpenBLAS `dgemm_kernel_HASWELL`.
- tabmat uses **SSE128 `mulpd`/`addpd`**; OpenBLAS/Numba BLAS use **AVX2 `vfmadd231pd`**.
- Numba `k_inner` auto-vectorization emits **`vscatterqpd`** → rejected (slower despite SIMD).
- JAX fusion thunk is **scalar LLVM**; matmul SIMD is in linked XLA/Eigen runtime.

### Iteration 4 — move to repo root + tabmat analysis + refined kernels

- Moved from `hgbdt_performance_analysis/sandwich_fused_kernels/` to top-level `sandwich_fused_kernels/`.
- Added `analyze_tabmat.py` with cProfile + memory/algorithm tagging.
- Added `numba_fused_blocked` (corrected symmetric bug), `numba_blas_tiled` (2048-row chunks), `jax_scan_chunked`, `jax_einsum_chunked`.
- **Profiling validated assumptions:** fused blocked Numba still 10× behind tabmat; BLAS chunking helps medium/tall shapes; chunked JAX does not beat fused `einsum` on CPU.

### Iteration 6 results (linux-amd64, 4 cores, 5 repeats)

#### Single-threaded (1 thread)

| Problem | tabmat | Best Numba | `rival_st` | Best Numba vs tabmat |
|---|---:|---|---:|---:|
| glm_small 50k×40 f64 | 6.59 ms | blas_fused 14.35 ms | 94.5 ms | 0.46× |
| glm_medium 140k×80 f64 | 65.87 ms | blas_fused 101.6 ms | 946 ms | 0.65× |
| glm_tall_skinny 320k×32 f64 | 38.62 ms | blas_fused 79.0 ms | 353 ms | 0.49× |
| glm_small_f32 50k×40 | 4.33 ms | blas_fused 7.44 ms | 80.7 ms | 0.58× |

#### Multi-threaded (4 threads)

| Problem | tabmat | Best Numba | `rival_mt` | `blas_kchunk_mt` | Best Numba vs tabmat |
|---|---:|---|---:|---:|---:|
| glm_small 50k×40 f64 | 2.11 ms | blas_tiled 6.34 ms | 21.2 ms | 6.42 ms | **0.33×** |
| glm_medium 140k×80 f64 | 21.77 ms | blas_tiled 45.5 ms | 259 ms | 48.9 ms | **0.48×** |
| glm_tall_skinny 320k×32 f64 | 13.36 ms | blas_kchunk 39.8 ms | 109 ms | 39.8 ms | **0.34×** |
| glm_small_f32 50k×40 | 1.61 ms | blas_kchunk 5.64 ms | 20.9 ms | 5.64 ms | **0.28×** |

Full tables: `artifacts/benchmark_report_single_thread.md`, `artifacts/benchmark_report_multi_thread.md`.

## Best performance achieved so far

| Metric | Single-threaded | Multi-threaded |
|---|---|---|
| **Overall fastest** | tabmat — 4.33 ms (`glm_small_f32`) | tabmat — 1.61 ms (`glm_small_f32`) |
| **Best Numba vs tabmat** | `blas_fused` — **0.58×** (`glm_small_f32`) | `blas_tiled` / `blas_kchunk_mt` — **0.33×** (`glm_small` f64) |
| **Best fused rival vs tabmat** | `rival_st` — 0.07× (`glm_small` f64) | `rival_mt` — 0.10× (`glm_small` f64) |
| **Best compiler vs numpy_einsum (MT)** | — | `blas_tiled` — **2.21×** (`glm_small` f64) |

**Practical recommendation:**

- Use **tabmat** when available (fastest ST and MT; lowest memory).
- **Best Numba MT:** `blas_kchunk_mt` or `blas_tiled` with `blas_threads=1` per worker (~3× slower than tabmat on small GLM shapes).
- **Best Numba ST:** `blas_fused` (~0.5–0.6× tabmat).
- **Fused `rival_*` kernels** validate tabmat's algorithmic choices (fused weights, symmetric blocks) but LLVM cannot match hand-tuned SSE micro-kernels; they remain **~10× behind tabmat**.
- Avoid `k_inner` and scatter-vectorized output updates.

## Layout

```
sandwich_fused_kernels/
├── README.md
├── analyze_tabmat.py
├── inspect_simd.py
├── benchmark_sandwich.py
├── threading_utils.py
├── profile_memory.py
├── kernels/
│   ├── reference.py
│   ├── numpy_baseline.py
│   ├── tabmat_baseline.py
│   ├── numba_kernels.py
│   └── jax_kernels.py
└── artifacts/
    ├── benchmark_results.json
    ├── benchmark_report.md
    ├── benchmark_report_single_thread.md
    ├── benchmark_report_multi_thread.md
    ├── tabmat_advantage_analysis.md
    ├── simd_inspection.md
    ├── tabmat_dense.so.asm
    ├── numba_*.asm
    ├── memory_profile_float64.json
    └── profile_*.txt
```
