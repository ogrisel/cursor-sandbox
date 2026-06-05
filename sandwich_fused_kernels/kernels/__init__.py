"""Sandwich product kernel implementations."""

from .jax_kernels import sandwich_jax, warmup_jax
from .numba_kernels import sandwich_numba, warmup_numba
from .numpy_baseline import (
    sandwich_numpy_diag_matmul,
    sandwich_numpy_einsum,
    sandwich_numpy_weighted_gram,
)
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
]
