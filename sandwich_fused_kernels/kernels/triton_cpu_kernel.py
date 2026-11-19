"""Triton-CPU sandwich kernels (native Triton + torch.compile CPU backend).

Requires the experimental CPU backend from https://github.com/triton-lang/triton-cpu
built into the active Python environment. Set ``TRITON_CPU_BACKEND=1`` at runtime.

Build: ``sandwich_fused_kernels/build_triton_cpu.sh``
"""

from __future__ import annotations

import math
import os
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from typing import Callable, Iterator

import numpy as np

_TRITON_CPU_ENV = "TRITON_CPU_BACKEND"
_TORCH_COMPILE_TRITON_EINSUM: Callable[..., object] | None = None
_TORCH_COMPILE_TRITON_TILED: dict[tuple[int, int, int], Callable[..., object]] = {}


def _ensure_triton_cpu_env() -> None:
    os.environ[_TRITON_CPU_ENV] = "1"


def triton_cpu_available() -> bool:
    """Return True when triton-cpu is installed (cpu backend registered)."""
    _ensure_triton_cpu_env()
    try:
        import triton.backends  # noqa: WPS433

        return "cpu" in triton.backends.backends
    except Exception:
        return False


@contextmanager
def triton_cpu_context() -> Iterator[None]:
    """Pin Triton to the CPU backend for the duration of a benchmark block."""
    _ensure_triton_cpu_env()
    prev_default = os.environ.get("TRITON_DEFAULT_BACKEND")
    os.environ["TRITON_DEFAULT_BACKEND"] = "cpu"
    try:
        yield
    finally:
        if prev_default is None:
            os.environ.pop("TRITON_DEFAULT_BACKEND", None)
        else:
            os.environ["TRITON_DEFAULT_BACKEND"] = prev_default


def _import_triton():
    import triton
    import triton.language as tl

    return triton, tl


try:
    _triton, _tl = _import_triton()

    @_triton.jit
    def _sandwich_accum_kernel(
        X_ptr,
        d_ptr,
        Out_ptr,
        stride_xk,
        stride_xm,
        stride_om,
        stride_on,
        k0,
        chunk_size,
        M: _tl.constexpr,
        BLOCK_M: _tl.constexpr,
        BLOCK_K: _tl.constexpr,
        ACC_DTYPE: _tl.constexpr,
    ):
        pid_i = _tl.program_id(0)
        pid_j = _tl.program_id(1)
        offs_i = pid_i * BLOCK_M + _tl.arange(0, BLOCK_M)
        offs_j = pid_j * BLOCK_M + _tl.arange(0, BLOCK_M)
        mask_i = offs_i < M
        mask_j = offs_j < M
        acc = _tl.zeros((BLOCK_M, BLOCK_M), dtype=ACC_DTYPE)
        for k in range(0, chunk_size, BLOCK_K):
            offs_k = k + _tl.arange(0, BLOCK_K)
            mask_k = offs_k < chunk_size
            row_idx = k0 + offs_k
            x_i = _tl.load(
                X_ptr + row_idx[:, None] * stride_xk + offs_i[None, :] * stride_xm,
                mask=mask_k[:, None] & mask_i[None, :],
                other=0.0,
            )
            d_v = _tl.load(d_ptr + row_idx, mask=mask_k, other=0.0)
            wx = x_i * d_v[:, None]
            x_j = _tl.load(
                X_ptr + row_idx[:, None] * stride_xk + offs_j[None, :] * stride_xm,
                mask=mask_k[:, None] & mask_j[None, :],
                other=0.0,
            )
            acc += _tl.sum(wx[:, :, None] * x_j[:, None, :], axis=0)
        out_ptrs = Out_ptr + offs_i[:, None] * stride_om + offs_j[None, :] * stride_on
        _tl.atomic_add(out_ptrs, acc, mask=mask_i[:, None] & mask_j[None, :])

    _TRITON_JIT_READY = True
except Exception:  # noqa: BLE001
    _sandwich_accum_kernel = None  # type: ignore[assignment,misc]
    _TRITON_JIT_READY = False


def _torch_threads(num_threads: int | None) -> int:
    import torch

    if num_threads is not None:
        return num_threads
    return max(1, torch.get_num_threads())


def _launch_row_chunk(
    Xt,
    dt,
    out,
    *,
    k0: int,
    chunk_size: int,
    n_cols: int,
    block_m: int,
    block_k: int,
    acc_tl,
) -> None:
    grid = (math.ceil(n_cols / block_m), math.ceil(n_cols / block_m))
    _sandwich_accum_kernel[grid](
        Xt,
        dt,
        out,
        Xt.stride(0),
        Xt.stride(1),
        out.stride(0),
        out.stride(1),
        k0,
        chunk_size,
        M=n_cols,
        BLOCK_M=block_m,
        BLOCK_K=block_k,
        ACC_DTYPE=acc_tl,
    )


def _accumulate_row_range(
    Xt,
    dt,
    out,
    *,
    row_start: int,
    row_end: int,
    chunk: int,
    n_cols: int,
    block_m: int,
    block_k: int,
    acc_tl,
) -> None:
    with triton_cpu_context():
        for k0 in range(row_start, row_end, chunk):
            chunk_size = min(chunk, row_end - k0)
            _launch_row_chunk(
                Xt,
                dt,
                out,
                k0=k0,
                chunk_size=chunk_size,
                n_cols=n_cols,
                block_m=block_m,
                block_k=block_k,
                acc_tl=acc_tl,
            )


def sandwich_triton_cpu_native(
    X: np.ndarray,
    d: np.ndarray,
    *,
    chunk: int = 4096,
    block_m: int = 8,
    block_k: int = 64,
    n_chunks: int = 1,
    num_threads: int | None = None,
) -> np.ndarray:
    """Hand-written Triton-CPU kernel with tunable tiles and optional row-band MT."""
    if not triton_cpu_available() or not _TRITON_JIT_READY:
        raise RuntimeError("triton-cpu JIT kernel is not available")

    import torch

    threads = _torch_threads(num_threads)
    torch.set_num_threads(1)
    dtype = torch.float32 if X.dtype == np.float32 else torch.float64
    acc_tl = _tl.float64 if dtype == torch.float64 else _tl.float32
    Xt = torch.as_tensor(X, dtype=dtype)
    dt = torch.as_tensor(d, dtype=dtype)
    n_rows, n_cols = Xt.shape

    if n_chunks <= 1:
        out = torch.zeros((n_cols, n_cols), dtype=dtype)
        _accumulate_row_range(
            Xt,
            dt,
            out,
            row_start=0,
            row_end=n_rows,
            chunk=chunk,
            n_cols=n_cols,
            block_m=block_m,
            block_k=block_k,
            acc_tl=acc_tl,
        )
        return out.detach().cpu().numpy()

    k_band = (n_rows + n_chunks - 1) // n_chunks
    partials = torch.zeros((n_chunks, n_cols, n_cols), dtype=dtype)
    workers = min(threads, n_chunks)

    def _worker(cb: int) -> int:
        row_start = cb * k_band
        row_end = min(row_start + k_band, n_rows)
        if row_start >= row_end:
            return cb
        _accumulate_row_range(
            Xt,
            dt,
            partials[cb],
            row_start=row_start,
            row_end=row_end,
            chunk=chunk,
            n_cols=n_cols,
            block_m=block_m,
            block_k=block_k,
            acc_tl=acc_tl,
        )
        return cb

    with ThreadPoolExecutor(max_workers=workers) as pool:
        list(pool.map(_worker, range(n_chunks)))
    return partials.sum(dim=0).detach().cpu().numpy()


def sandwich_helion_triton_cpu(
    X: np.ndarray,
    d: np.ndarray,
    *,
    num_threads: int | None = None,
    **triton_params: int,
) -> np.ndarray:
    """Helion→Triton on triton-cpu (falls back to native Triton if Helion codegen fails)."""
    from . import helion_kernel

    if not helion_kernel.helion_available():
        return sandwich_triton_cpu_native(X, d, num_threads=num_threads, **triton_params)
    if not triton_cpu_available():
        raise RuntimeError("triton-cpu backend not found. Build with build_triton_cpu.sh")

    import torch

    threads = _torch_threads(num_threads)
    torch.set_num_threads(threads)
    dtype = torch.float32 if X.dtype == np.float32 else torch.float64
    Xt = torch.as_tensor(X, dtype=dtype)
    dt = torch.as_tensor(d, dtype=dtype)
    with triton_cpu_context():
        try:
            out = helion_kernel.sandwich_helion(Xt, dt, mode="triton")
            return out.detach().cpu().numpy()
        except Exception:
            return sandwich_triton_cpu_native(X, d, num_threads=threads, **triton_params)


def _get_torch_compile_triton_einsum() -> Callable[..., object]:
    global _TORCH_COMPILE_TRITON_EINSUM
    if _TORCH_COMPILE_TRITON_EINSUM is not None:
        return _TORCH_COMPILE_TRITON_EINSUM

    import torch
    from torch._inductor import config as inductor_config

    from . import helion_kernel

    inductor_config.cpu_backend = "triton"

    def eager(X: torch.Tensor, d: torch.Tensor) -> torch.Tensor:
        return helion_kernel.sandwich_torch_einsum(X, d)

    if hasattr(torch, "compile"):
        _TORCH_COMPILE_TRITON_EINSUM = torch.compile(eager, backend="inductor")
    else:
        _TORCH_COMPILE_TRITON_EINSUM = eager
    return _TORCH_COMPILE_TRITON_EINSUM


def _get_torch_compile_triton_tiled(
    tile_m: int,
    tile_n: int,
    tile_k: int,
) -> Callable[..., object]:
    key = (tile_m, tile_n, tile_k)
    if key in _TORCH_COMPILE_TRITON_TILED:
        return _TORCH_COMPILE_TRITON_TILED[key]

    import torch
    from torch._inductor import config as inductor_config

    from . import helion_kernel

    inductor_config.cpu_backend = "triton"

    def eager(X: torch.Tensor, d: torch.Tensor) -> torch.Tensor:
        return helion_kernel.sandwich_torch_tiled(X, d, tile_m, tile_n, tile_k)

    if hasattr(torch, "compile"):
        _TORCH_COMPILE_TRITON_TILED[key] = torch.compile(eager, backend="inductor")
    else:
        _TORCH_COMPILE_TRITON_TILED[key] = eager
    return _TORCH_COMPILE_TRITON_TILED[key]


def sandwich_torch_compile_triton_cpu(
    X: np.ndarray,
    d: np.ndarray,
    *,
    num_threads: int | None = None,
) -> np.ndarray:
    """torch.compile(einsum) with Inductor cpu_backend=triton (triton-cpu)."""
    if not triton_cpu_available():
        raise RuntimeError("triton-cpu backend not found")

    import torch

    threads = _torch_threads(num_threads)
    torch.set_num_threads(threads)
    dtype = torch.float32 if X.dtype == np.float32 else torch.float64
    Xt = torch.as_tensor(X, dtype=dtype)
    dt = torch.as_tensor(d, dtype=dtype)
    fn = _get_torch_compile_triton_einsum()
    with triton_cpu_context():
        out = fn(Xt, dt)
    return out.detach().cpu().numpy()


def sandwich_torch_compile_triton_tiled(
    X: np.ndarray,
    d: np.ndarray,
    *,
    tile_m: int = 16,
    tile_n: int = 16,
    tile_k: int = 8192,
    num_threads: int | None = None,
) -> np.ndarray:
    """torch.compile(tiled) with Inductor cpu_backend=triton (triton-cpu)."""
    if not triton_cpu_available():
        raise RuntimeError("triton-cpu backend not found")

    import torch

    threads = _torch_threads(num_threads)
    torch.set_num_threads(threads)
    dtype = torch.float32 if X.dtype == np.float32 else torch.float64
    Xt = torch.as_tensor(X, dtype=dtype)
    dt = torch.as_tensor(d, dtype=dtype)
    fn = _get_torch_compile_triton_tiled(tile_m, tile_n, tile_k)
    with triton_cpu_context():
        out = fn(Xt, dt)
    return out.detach().cpu().numpy()


def warmup_triton_cpu_native(num_threads: int = 1) -> None:
    if not triton_cpu_available() or not _TRITON_JIT_READY:
        return
    import torch

    X = torch.randn(64, 8, dtype=torch.float64)
    d = torch.rand(64, dtype=torch.float64) + 0.1
    sandwich_triton_cpu_native(
        X.numpy(),
        d.numpy(),
        chunk=256,
        block_m=4,
        block_k=64,
        n_chunks=max(1, num_threads),
        num_threads=num_threads,
    )


def warmup_helion_triton_cpu(num_threads: int = 1) -> None:
    if not triton_cpu_available():
        return
    import torch

    X = torch.randn(64, 8, dtype=torch.float64)
    d = torch.rand(64, dtype=torch.float64) + 0.1
    sandwich_helion_triton_cpu(X.numpy(), d.numpy(), num_threads=num_threads)


def warmup_torch_compile_triton_cpu(num_threads: int = 1) -> None:
    if not triton_cpu_available():
        return
    import torch

    X = torch.randn(64, 8, dtype=torch.float64)
    d = torch.rand(64, dtype=torch.float64) + 0.1
    fn = _get_torch_compile_triton_einsum()
    torch.set_num_threads(num_threads)
    with triton_cpu_context():
        fn(X, d)


def warmup_torch_compile_triton_tiled(num_threads: int = 1) -> None:
    if not triton_cpu_available():
        return
    import torch

    X = torch.randn(64, 8, dtype=torch.float64)
    d = torch.rand(64, dtype=torch.float64) + 0.1
    fn = _get_torch_compile_triton_tiled(4, 4, 32)
    torch.set_num_threads(num_threads)
    with triton_cpu_context():
        fn(X, d)
