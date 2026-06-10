"""Sandwich product kernel implementations."""

from __future__ import annotations

from typing import Any

from .numpy_baseline import (
    sandwich_numpy_diag_matmul,
    sandwich_numpy_einsum,
    sandwich_numpy_weighted_gram,
)
from .numba_kernels import sandwich_numba, warmup_numba
from .reference import sandwich_reference
from .tabmat_baseline import sandwich_tabmat

__all__ = [
    "sandwich_reference",
    "sandwich_numpy_diag_matmul",
    "sandwich_numpy_einsum",
    "sandwich_numpy_weighted_gram",
    "sandwich_tabmat",
    "sandwich_numba",
    "warmup_numba",
    "sandwich_jax",
    "warmup_jax",
    "sandwich_helion_eager",
    "sandwich_torch_einsum",
    "sandwich_torch_compile_einsum",
    "helion_available",
    "warmup_helion",
    "warmup_torch_compile",
    "HELION_KERNEL_SOURCE",
    "triton_cpu_available",
    "sandwich_triton_cpu_native",
    "sandwich_helion_triton_cpu",
    "sandwich_torch_compile_triton_cpu",
    "warmup_triton_cpu_native",
    "warmup_helion_triton_cpu",
    "warmup_torch_compile_triton_cpu",
]


def __getattr__(name: str) -> Any:
    if name in ("sandwich_jax", "warmup_jax"):
        from .jax_kernels import sandwich_jax, warmup_jax

        return {"sandwich_jax": sandwich_jax, "warmup_jax": warmup_jax}[name]
    if name in (
        "sandwich_helion_eager",
        "sandwich_torch_einsum",
        "sandwich_torch_compile_einsum",
        "helion_available",
        "warmup_helion",
        "warmup_torch_compile",
        "HELION_KERNEL_SOURCE",
    ):
        from . import helion_baseline

        return {
            "sandwich_helion_eager": helion_baseline.sandwich_helion_eager,
            "sandwich_torch_einsum": helion_baseline.sandwich_torch_einsum,
            "sandwich_torch_compile_einsum": helion_baseline.sandwich_torch_compile_einsum,
            "helion_available": helion_baseline.helion_available,
            "warmup_helion": helion_baseline.warmup_helion,
            "warmup_torch_compile": helion_baseline.warmup_torch_compile,
            "HELION_KERNEL_SOURCE": helion_baseline.HELION_KERNEL_PATH,
        }[name]
    if name in (
        "triton_cpu_available",
        "sandwich_triton_cpu_native",
        "sandwich_helion_triton_cpu",
        "sandwich_torch_compile_triton_cpu",
        "warmup_triton_cpu_native",
        "warmup_helion_triton_cpu",
        "warmup_torch_compile_triton_cpu",
    ):
        from . import triton_cpu_kernel

        return {
            "triton_cpu_available": triton_cpu_kernel.triton_cpu_available,
            "sandwich_triton_cpu_native": triton_cpu_kernel.sandwich_triton_cpu_native,
            "sandwich_helion_triton_cpu": triton_cpu_kernel.sandwich_helion_triton_cpu,
            "sandwich_torch_compile_triton_cpu": triton_cpu_kernel.sandwich_torch_compile_triton_cpu,
            "warmup_triton_cpu_native": triton_cpu_kernel.warmup_triton_cpu_native,
            "warmup_helion_triton_cpu": triton_cpu_kernel.warmup_helion_triton_cpu,
            "warmup_torch_compile_triton_cpu": triton_cpu_kernel.warmup_torch_compile_triton_cpu,
        }[name]
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
