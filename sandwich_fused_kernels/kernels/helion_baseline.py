"""NumPy-facing Helion sandwich baseline (PyTorch + helion; no tabmat/xsimd).

The Helion kernel definition lives in ``helion_kernel.py``:

    sandwich_fused_kernels/kernels/helion_kernel.py

Helion compiles ``@helion.kernel`` + ``hl.tile`` loops to Triton on GPU.
On CPU we use ``ref_mode=EAGER`` (tile reference interpreter).
"""

from __future__ import annotations

import numpy as np

from . import helion_kernel

HELION_KERNEL_PATH = helion_kernel.__file__


def helion_available() -> bool:
    return helion_kernel.helion_available()


def sandwich_helion(
    X: np.ndarray,
    d: np.ndarray,
    *,
    mode: str = "eager",
) -> np.ndarray:
    """Compute X.T @ diag(d) @ X via Helion (returns NumPy array)."""
    import torch

    torch.set_num_threads(1)
    dtype = torch.float32 if X.dtype == np.float32 else torch.float64
    Xt = torch.as_tensor(X, dtype=dtype)
    dt = torch.as_tensor(d, dtype=dtype)
    out = helion_kernel.sandwich_helion(Xt, dt, mode=mode)
    return out.detach().cpu().numpy()


def sandwich_helion_eager(X: np.ndarray, d: np.ndarray) -> np.ndarray:
    """Helion CPU reference kernel (ref_mode=EAGER)."""
    return sandwich_helion(X, d, mode="eager")


def sandwich_torch_einsum(X: np.ndarray, d: np.ndarray) -> np.ndarray:
    """Pure PyTorch einsum baseline (no Helion DSL)."""
    import torch

    dtype = torch.float32 if X.dtype == np.float32 else torch.float64
    Xt = torch.as_tensor(X, dtype=dtype)
    dt = torch.as_tensor(d, dtype=dtype)
    out = helion_kernel.sandwich_torch_einsum(Xt, dt)
    return out.detach().cpu().numpy()


def sandwich_torch_compile_einsum(X: np.ndarray, d: np.ndarray) -> np.ndarray:
    """torch.compile(einsum) baseline (no Helion DSL)."""
    import torch

    dtype = torch.float32 if X.dtype == np.float32 else torch.float64
    Xt = torch.as_tensor(X, dtype=dtype)
    dt = torch.as_tensor(d, dtype=dtype)
    out = helion_kernel.sandwich_torch_compile_einsum(Xt, dt)
    return out.detach().cpu().numpy()


def warmup_helion(mode: str = "eager") -> None:
    helion_kernel.warmup_helion(mode=mode)


def warmup_torch_compile() -> None:
    helion_kernel.warmup_torch_compile()
