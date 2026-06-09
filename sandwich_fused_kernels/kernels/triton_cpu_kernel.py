"""Triton-CPU sandwich kernels (native Triton + torch.compile CPU backend).

Requires the experimental CPU backend from https://github.com/triton-lang/triton-cpu
built into the active Python environment. Set ``TRITON_CPU_BACKEND=1`` at runtime.

Build: ``sandwich_fused_kernels/build_triton_cpu.sh``
"""

from __future__ import annotations

import math
import os
from contextlib import contextmanager
from typing import Callable, Iterator

import numpy as np

_TRITON_CPU_ENV = "TRITON_CPU_BACKEND"
_TORCH_COMPILE_TRITON_FN: Callable[..., object] | None = None
_TRITON_NATIVE_CHUNK = 4096
_TRITON_NATIVE_BLOCK_M = 16
_TRITON_NATIVE_BLOCK_K = 256


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


def _acc_dtype_name(dtype: str) -> str:
    return "tl.float64" if dtype == "float64" else "tl.float32"


def sandwich_triton_cpu_native(
    X: np.ndarray,
    d: np.ndarray,
    *,
    chunk: int = _TRITON_NATIVE_CHUNK,
    block_m: int = _TRITON_NATIVE_BLOCK_M,
    block_k: int = _TRITON_NATIVE_BLOCK_K,
) -> np.ndarray:
    """Hand-written Triton-CPU kernel: row-chunked weighted Gram accumulation."""
    if not triton_cpu_available() or not _TRITON_JIT_READY:
        raise RuntimeError("triton-cpu JIT kernel is not available")

    import torch

    torch.set_num_threads(1)
    dtype = torch.float32 if X.dtype == np.float32 else torch.float64
    acc_tl = _tl.float64 if dtype == torch.float64 else _tl.float32
    Xt = torch.as_tensor(X, dtype=dtype)
    dt = torch.as_tensor(d, dtype=dtype)
    n_rows, n_cols = Xt.shape
    out = torch.zeros((n_cols, n_cols), dtype=dtype)
    grid = (math.ceil(n_cols / block_m), math.ceil(n_cols / block_m))

    with triton_cpu_context():
        for k0 in range(0, n_rows, chunk):
            chunk_size = min(chunk, n_rows - k0)
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
    return out.detach().cpu().numpy()


def sandwich_helion_triton_cpu(X: np.ndarray, d: np.ndarray) -> np.ndarray:
    """Helion→Triton on triton-cpu (falls back to native Triton if Helion codegen fails)."""
    from . import helion_kernel

    if not helion_kernel.helion_available():
        return sandwich_triton_cpu_native(X, d)
    if not triton_cpu_available():
        raise RuntimeError(
            "triton-cpu backend not found. Build with build_triton_cpu.sh"
        )

    import torch

    torch.set_num_threads(1)
    dtype = torch.float32 if X.dtype == np.float32 else torch.float64
    Xt = torch.as_tensor(X, dtype=dtype)
    dt = torch.as_tensor(d, dtype=dtype)
    with triton_cpu_context():
        try:
            out = helion_kernel.sandwich_helion(Xt, dt, mode="triton")
            return out.detach().cpu().numpy()
        except Exception:
            return sandwich_triton_cpu_native(X, d)


def _get_torch_compile_triton_einsum() -> Callable[..., object]:
    global _TORCH_COMPILE_TRITON_FN
    if _TORCH_COMPILE_TRITON_FN is not None:
        return _TORCH_COMPILE_TRITON_FN

    import torch
    from torch._inductor import config as inductor_config

    from . import helion_kernel

    inductor_config.cpu_backend = "triton"

    def eager(X: torch.Tensor, d: torch.Tensor) -> torch.Tensor:
        return helion_kernel.sandwich_torch_einsum(X, d)

    if hasattr(torch, "compile"):
        _TORCH_COMPILE_TRITON_FN = torch.compile(eager, backend="inductor")
    else:
        _TORCH_COMPILE_TRITON_FN = eager
    return _TORCH_COMPILE_TRITON_FN


def sandwich_torch_compile_triton_cpu(X: np.ndarray, d: np.ndarray) -> np.ndarray:
    """torch.compile(einsum) with Inductor cpu_backend=triton (triton-cpu)."""
    if not triton_cpu_available():
        raise RuntimeError("triton-cpu backend not found")

    import torch

    torch.set_num_threads(1)
    dtype = torch.float32 if X.dtype == np.float32 else torch.float64
    Xt = torch.as_tensor(X, dtype=dtype)
    dt = torch.as_tensor(d, dtype=dtype)
    fn = _get_torch_compile_triton_einsum()
    with triton_cpu_context():
        out = fn(Xt, dt)
    return out.detach().cpu().numpy()


def warmup_triton_cpu_native() -> None:
    if not triton_cpu_available() or not _TRITON_JIT_READY:
        return
    import torch

    X = torch.randn(64, 8, dtype=torch.float64)
    d = torch.rand(64, dtype=torch.float64) + 0.1
    sandwich_triton_cpu_native(X.numpy(), d.numpy())


def warmup_helion_triton_cpu() -> None:
    if not triton_cpu_available():
        return
    import torch

    X = torch.randn(64, 8, dtype=torch.float64)
    d = torch.rand(64, dtype=torch.float64) + 0.1
    sandwich_helion_triton_cpu(X.numpy(), d.numpy())


def warmup_torch_compile_triton_cpu() -> None:
    if not triton_cpu_available():
        return
    import torch

    X = torch.randn(64, 8, dtype=torch.float64)
    d = torch.rand(64, dtype=torch.float64) + 0.1
    fn = _get_torch_compile_triton_einsum()
    with triton_cpu_context():
        fn(X, d)
