"""Autotuned sandwich kernel dispatch (loads params from autotune cache)."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from autotune_config import AutotuneCache, DEFAULT_CACHE_PATH, TuneParams

from . import numba_kernels as nk
from . import xsimd_kernel as xk

_CACHE: AutotuneCache | None = None


def _cache() -> AutotuneCache:
    global _CACHE
    if _CACHE is None:
        _CACHE = AutotuneCache.load(DEFAULT_CACHE_PATH)
    return _CACHE


def reload_autotune_cache(path: Path = DEFAULT_CACHE_PATH) -> None:
    global _CACHE
    _CACHE = AutotuneCache.load(path)


def _params(
    family: str,
    *,
    problem: str | None,
    threading: str,
    num_threads: int,
    fallback: TuneParams,
) -> TuneParams:
    if problem is None:
        return fallback
    cached = _cache().get(problem, threading, num_threads, family)
    if cached is not None:
        return cached
    if family in {"helion_tiled", "torch_tiled", "torch_compile_tiled"} and threading == "multi":
        cached = _cache().get(problem, "single", 1, family)
        if cached is not None:
            return cached
    if family == "torch_compile_tiled":
        cached = _cache().get(problem, threading, num_threads, "torch_tiled")
        if cached is None and threading == "multi":
            cached = _cache().get(problem, "single", 1, "torch_tiled")
        if cached is not None:
            return cached
    if family == "torch_compile_triton_tuned":
        cached = _cache().get(problem, threading, num_threads, "torch_compile_triton_mt")
        if cached is None:
            cached = _cache().get(problem, threading, num_threads, "torch_tiled")
        if cached is None and threading == "multi":
            cached = _cache().get(problem, "single", 1, "torch_compile_triton_mt")
            if cached is None:
                cached = _cache().get(problem, "single", 1, "torch_tiled")
        if cached is not None:
            return cached
    return fallback


def sandwich_numba_fused_tuned(
    X: np.ndarray,
    d: np.ndarray,
    *,
    problem: str | None = None,
    threading: str = "multi",
    num_threads: int = 1,
) -> np.ndarray:
    p = _params(
        "numba_fused_mt",
        problem=problem,
        threading=threading,
        num_threads=num_threads,
        fallback=TuneParams(block=4, n_chunks=max(num_threads * 4, 1)),
    )
    if num_threads <= 1:
        out = np.zeros((X.shape[1], X.shape[1]), dtype=X.dtype)
        nk._accumulate_tabmat_blocks(X, d, out, p.block)
        return out
    return nk._sandwich_kchunk_fused_impl(X, d, p.n_chunks, p.block)


def sandwich_numba_blas_tuned(
    X: np.ndarray,
    d: np.ndarray,
    *,
    problem: str | None = None,
    threading: str = "multi",
    num_threads: int = 1,
) -> np.ndarray:
    p = _params(
        "numba_blas_mt",
        problem=problem,
        threading=threading,
        num_threads=num_threads,
        fallback=TuneParams(n_chunks=max(num_threads * 2, 1)),
    )
    if num_threads <= 1:
        return nk.sandwich_numba_blas_fused(X, d)
    return nk._sandwich_kchunk_blas_impl(X, d, p.n_chunks)


def sandwich_numba_jblock_tuned(
    X: np.ndarray,
    d: np.ndarray,
    *,
    problem: str | None = None,
    threading: str = "multi",
    num_threads: int = 1,
) -> np.ndarray:
    p = _params(
        "numba_jblock_mt",
        problem=problem,
        threading=threading,
        num_threads=num_threads,
        fallback=TuneParams(block=8),
    )
    return nk._tabmat_style_mt_impl(X, d, p.block)


def sandwich_jax_chunked_tuned(
    X: np.ndarray,
    d: np.ndarray,
    *,
    problem: str | None = None,
    threading: str = "multi",
    num_threads: int = 1,
) -> np.ndarray:
    from .jax_kernels import sandwich_jax_chunked

    p = _params(
        "jax_chunked",
        problem=problem,
        threading=threading,
        num_threads=num_threads,
        fallback=TuneParams(jax_chunk=4096),
    )
    return sandwich_jax_chunked(X, d, chunk=p.jax_chunk)


def sandwich_xsimd_tuned(
    X: np.ndarray,
    d: np.ndarray,
    *,
    problem: str | None = None,
    threading: str = "multi",
    num_threads: int = 1,
) -> np.ndarray:
    p = _params(
        "xsimd_mt",
        problem=problem,
        threading=threading,
        num_threads=num_threads,
        fallback=TuneParams(xsimd_block=4, xsimd_chunk_factor=4),
    )
    return xk.sandwich_xsimd(
        X,
        d,
        num_threads=num_threads,
        block=p.xsimd_block,
        chunk_factor=p.xsimd_chunk_factor,
    )


def _helion_tile_fallback() -> TuneParams:
    return TuneParams(tile_m=16, tile_n=16, tile_k=8192)


def sandwich_helion_tiled_tuned(
    X: np.ndarray,
    d: np.ndarray,
    *,
    problem: str | None = None,
    threading: str = "single",
    num_threads: int = 1,
) -> np.ndarray:
    from . import helion_baseline as hb

    p = _params(
        "helion_tiled",
        problem=problem,
        threading=threading,
        num_threads=num_threads,
        fallback=_helion_tile_fallback(),
    )
    return hb.sandwich_helion_tiled(X, d, tile_m=p.tile_m, tile_n=p.tile_n, tile_k=p.tile_k)


def sandwich_torch_tiled_tuned(
    X: np.ndarray,
    d: np.ndarray,
    *,
    problem: str | None = None,
    threading: str = "single",
    num_threads: int = 1,
) -> np.ndarray:
    from . import helion_baseline as hb

    p = _params(
        "torch_tiled",
        problem=problem,
        threading=threading,
        num_threads=num_threads,
        fallback=_helion_tile_fallback(),
    )
    return hb.sandwich_torch_tiled(X, d, tile_m=p.tile_m, tile_n=p.tile_n, tile_k=p.tile_k)


def _triton_fallback(num_threads: int) -> TuneParams:
    return TuneParams(
        triton_chunk=4096,
        triton_block_m=8,
        triton_block_k=64,
        triton_n_chunks=max(num_threads, 1),
    )


def sandwich_triton_cpu_tuned(
    X: np.ndarray,
    d: np.ndarray,
    *,
    problem: str | None = None,
    threading: str = "multi",
    num_threads: int = 1,
) -> np.ndarray:
    from .triton_cpu_kernel import sandwich_triton_cpu_native

    p = _params(
        "triton_cpu_mt",
        problem=problem,
        threading=threading,
        num_threads=num_threads,
        fallback=_triton_fallback(num_threads),
    )
    return sandwich_triton_cpu_native(
        X,
        d,
        chunk=p.triton_chunk,
        block_m=p.triton_block_m,
        block_k=p.triton_block_k,
        n_chunks=p.triton_n_chunks,
        num_threads=num_threads,
    )


def sandwich_torch_compile_triton_tuned(
    X: np.ndarray,
    d: np.ndarray,
    *,
    problem: str | None = None,
    threading: str = "multi",
    num_threads: int = 1,
) -> np.ndarray:
    from .triton_cpu_kernel import sandwich_torch_compile_triton_tiled

    p = _params(
        "torch_compile_triton_tuned",
        problem=problem,
        threading=threading,
        num_threads=num_threads,
        fallback=_helion_tile_fallback(),
    )
    return sandwich_torch_compile_triton_tiled(
        X,
        d,
        tile_m=p.tile_m,
        tile_n=p.tile_n,
        tile_k=p.tile_k,
        num_threads=num_threads,
    )


def sandwich_helion_triton_cpu_tuned(
    X: np.ndarray,
    d: np.ndarray,
    *,
    problem: str | None = None,
    threading: str = "multi",
    num_threads: int = 1,
) -> np.ndarray:
    from .triton_cpu_kernel import sandwich_helion_triton_cpu

    p = _params(
        "triton_cpu_mt",
        problem=problem,
        threading=threading,
        num_threads=num_threads,
        fallback=_triton_fallback(num_threads),
    )
    return sandwich_helion_triton_cpu(
        X,
        d,
        num_threads=num_threads,
        chunk=p.triton_chunk,
        block_m=p.triton_block_m,
        block_k=p.triton_block_k,
        n_chunks=p.triton_n_chunks,
    )


def sandwich_torch_compile_tiled_tuned(
    X: np.ndarray,
    d: np.ndarray,
    *,
    problem: str | None = None,
    threading: str = "single",
    num_threads: int = 1,
) -> np.ndarray:
    from . import helion_baseline as hb

    p = _params(
        "torch_compile_tiled",
        problem=problem,
        threading=threading,
        num_threads=num_threads,
        fallback=_helion_tile_fallback(),
    )
    return hb.sandwich_torch_compile_tiled(
        X, d, tile_m=p.tile_m, tile_n=p.tile_n, tile_k=p.tile_k
    )


def warmup_tuned(num_threads: int = 1) -> None:
    rng = np.random.default_rng(0)
    X = rng.standard_normal((256, 16), dtype=np.float64)
    d = rng.random(256, dtype=np.float64) + 0.1
    sandwich_numba_fused_tuned(X, d, num_threads=num_threads)
    sandwich_numba_blas_tuned(X, d, num_threads=num_threads)
    sandwich_numba_jblock_tuned(X, d, num_threads=num_threads)
    try:
        sandwich_xsimd_tuned(X, d, num_threads=num_threads)
    except FileNotFoundError:
        pass
    try:
        from . import helion_baseline as hb

        if hb.helion_available():
            sandwich_helion_tiled_tuned(X, d, num_threads=num_threads)
        sandwich_torch_tiled_tuned(X, d, num_threads=num_threads)
        sandwich_torch_compile_tiled_tuned(X, d, num_threads=num_threads)
    except ImportError:
        pass
    try:
        from .triton_cpu_kernel import triton_cpu_available

        if triton_cpu_available():
            sandwich_triton_cpu_tuned(X, d, num_threads=num_threads)
            sandwich_torch_compile_triton_tuned(X, d, num_threads=num_threads)
    except (ImportError, RuntimeError):
        pass
