"""Helion and torch.compile sandwich kernels (PyTorch 2.9+)."""

from __future__ import annotations

from typing import Callable

import torch

try:
    import helion
    import helion.language as hl

    _HELION_AVAILABLE = True
except ImportError:  # pragma: no cover - optional dependency
    helion = None  # type: ignore[assignment]
    hl = None  # type: ignore[assignment]
    _HELION_AVAILABLE = False


if _HELION_AVAILABLE:

    @helion.kernel(autotune_effort="none", ref_mode=helion.RefMode.EAGER)
    def sandwich_helion_eager(X: torch.Tensor, d: torch.Tensor) -> torch.Tensor:
        """Reference/eager Helion kernel: tiles output (m,m) and reduces over rows."""
        n, m = X.shape
        out = torch.zeros((m, m), dtype=X.dtype, device=X.device)
        for tile_i, tile_j in hl.tile([m, m]):
            acc = hl.zeros([tile_i, tile_j], dtype=X.dtype)
            for tile_k in hl.tile(n):
                w = d[tile_k]
                Xi = X[tile_k, tile_i]
                Xj = X[tile_k, tile_j]
                acc = acc + torch.einsum("ki,k,kj->ij", Xi, w, Xj)
            out[tile_i, tile_j] = acc
        return out

    @helion.kernel(autotune_effort="none")
    def sandwich_helion_triton(X: torch.Tensor, d: torch.Tensor) -> torch.Tensor:
        """Triton-target Helion kernel (requires GPU or TRITON_INTERPRET=1)."""
        n, m = X.shape
        out = torch.zeros((m, m), dtype=X.dtype, device=X.device)
        for tile_i, tile_j in hl.tile([m, m]):
            acc = hl.zeros([tile_i, tile_j], dtype=X.dtype)
            for tile_k in hl.tile(n):
                w = d[tile_k]
                Xi = X[tile_k, tile_i]
                Xj = X[tile_k, tile_j]
                acc = acc + torch.einsum("ki,k,kj->ij", Xi, w, Xj)
            out[tile_i, tile_j] = acc
        return out


def sandwich_torch_einsum(X: torch.Tensor, d: torch.Tensor) -> torch.Tensor:
    """Eager PyTorch baseline."""
    return torch.einsum("ki,k,kj->ij", X, d, X)


def sandwich_torch_weighted_gram(X: torch.Tensor, d: torch.Tensor) -> torch.Tensor:
    """BLAS-backed weighted Gram in PyTorch."""
    weighted = X * d.unsqueeze(1)
    return weighted.T @ X


def _compile_if_available(fn: Callable[..., torch.Tensor]) -> Callable[..., torch.Tensor]:
    if not hasattr(torch, "compile"):
        return fn
    try:
        return torch.compile(fn, backend="inductor")
    except Exception:
        return fn


sandwich_torch_compile_einsum = _compile_if_available(sandwich_torch_einsum)
sandwich_torch_compile_weighted_gram = _compile_if_available(sandwich_torch_weighted_gram)


def helion_available() -> bool:
    return _HELION_AVAILABLE


def sandwich_helion(
    X: torch.Tensor,
    d: torch.Tensor,
    *,
    mode: str = "eager",
) -> torch.Tensor:
    """Dispatch to Helion eager (CPU ref) or Triton compilation path."""
    if not _HELION_AVAILABLE:
        raise ImportError("helion is not installed")
    if mode == "eager":
        return sandwich_helion_eager(X, d)
    if mode == "triton":
        return sandwich_helion_triton(X, d)
    raise ValueError(f"unknown helion mode: {mode}")


def warmup_helion(mode: str = "eager") -> None:
    if not _HELION_AVAILABLE:
        return
    X = torch.randn(64, 8, dtype=torch.float64)
    d = torch.rand(64, dtype=torch.float64) + 0.1
    sandwich_helion(X, d, mode=mode)


def warmup_torch_compile() -> None:
    X = torch.randn(64, 8, dtype=torch.float64)
    d = torch.rand(64, dtype=torch.float64) + 0.1
    sandwich_torch_compile_einsum(X, d)
    sandwich_torch_compile_weighted_gram(X, d)
