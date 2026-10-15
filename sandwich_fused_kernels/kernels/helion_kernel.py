"""Helion and torch.compile sandwich kernels (PyTorch 2.9+).

Location: ``sandwich_fused_kernels/kernels/helion_kernel.py``

NumPy-facing wrapper: ``sandwich_fused_kernels/kernels/helion_baseline.py``

The Helion sandwich product kernel is ``sandwich_helion_eager`` below — it tiles
the output (m×m) and reduces over rows with fused ``d[k]`` inside ``hl.tile`` loops.
"""

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

    @helion.kernel(autotune_effort="none", ref_mode=helion.RefMode.EAGER)
    def sandwich_helion_tiled(
        X: torch.Tensor,
        d: torch.Tensor,
        tile_m: int = 8,
        tile_n: int = 8,
        tile_k: int = 4096,
    ) -> torch.Tensor:
        """Helion eager kernel with explicit output/row tile sizes (for autotuning)."""
        n, m = X.shape
        out = torch.zeros((m, m), dtype=X.dtype, device=X.device)
        for tile_i, tile_j in hl.tile([m, m], block_size=[tile_m, tile_n]):
            acc = hl.zeros([tile_i, tile_j], dtype=X.dtype)
            for tile_kr in hl.tile(n, block_size=tile_k):
                w = d[tile_kr]
                Xi = X[tile_kr, tile_i]
                Xj = X[tile_kr, tile_j]
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


def sandwich_torch_tiled(
    X: torch.Tensor,
    d: torch.Tensor,
    tile_m: int = 8,
    tile_n: int = 8,
    tile_k: int = 4096,
) -> torch.Tensor:
    """PyTorch tiled sandwich (mirrors Helion structure; tunable tile sizes on CPU)."""
    n, m = X.shape
    out = torch.zeros((m, m), dtype=X.dtype, device=X.device)
    for i0 in range(0, m, tile_m):
        i1 = min(i0 + tile_m, m)
        for j0 in range(0, m, tile_n):
            j1 = min(j0 + tile_n, m)
            acc = torch.zeros((i1 - i0, j1 - j0), dtype=X.dtype, device=X.device)
            for k0 in range(0, n, tile_k):
                k1 = min(k0 + tile_k, n)
                w = d[k0:k1]
                Xi = X[k0:k1, i0:i1]
                Xj = X[k0:k1, j0:j1]
                acc = acc + torch.einsum("ki,k,kj->ij", Xi, w, Xj)
            out[i0:i1, j0:j1] = acc
    return out


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

_TORCH_COMPILE_TILED: dict[tuple[int, int, int], Callable[..., torch.Tensor]] = {}


def _get_torch_compile_tiled(
    tile_m: int,
    tile_n: int,
    tile_k: int,
) -> Callable[..., torch.Tensor]:
    key = (tile_m, tile_n, tile_k)
    if key not in _TORCH_COMPILE_TILED:

        def fn(X: torch.Tensor, d: torch.Tensor) -> torch.Tensor:
            return sandwich_torch_tiled(X, d, tile_m, tile_n, tile_k)

        _TORCH_COMPILE_TILED[key] = _compile_if_available(fn)
    return _TORCH_COMPILE_TILED[key]


def sandwich_torch_compile_tiled(
    X: torch.Tensor,
    d: torch.Tensor,
    tile_m: int = 8,
    tile_n: int = 8,
    tile_k: int = 4096,
) -> torch.Tensor:
    """torch.compile wrapper around the tiled PyTorch kernel."""
    return _get_torch_compile_tiled(tile_m, tile_n, tile_k)(X, d)


def helion_available() -> bool:
    return _HELION_AVAILABLE


def sandwich_helion(
    X: torch.Tensor,
    d: torch.Tensor,
    *,
    mode: str = "eager",
    tile_m: int = 8,
    tile_n: int = 8,
    tile_k: int = 4096,
) -> torch.Tensor:
    """Dispatch to Helion eager (CPU ref) or Triton compilation path."""
    if not _HELION_AVAILABLE:
        raise ImportError("helion is not installed")
    if mode == "eager":
        return sandwich_helion_eager(X, d)
    if mode == "tiled":
        return sandwich_helion_tiled(X, d, tile_m, tile_n, tile_k)
    if mode == "triton":
        return sandwich_helion_triton(X, d)
    raise ValueError(f"unknown helion mode: {mode}")


def warmup_helion(mode: str = "eager") -> None:
    if not _HELION_AVAILABLE:
        return
    X = torch.randn(64, 8, dtype=torch.float64)
    d = torch.rand(64, dtype=torch.float64) + 0.1
    if mode == "tiled":
        sandwich_helion_tiled(X, d, 4, 4, 32)
    else:
        sandwich_helion(X, d, mode=mode)


def warmup_torch_tiled() -> None:
    X = torch.randn(64, 8, dtype=torch.float64)
    d = torch.rand(64, dtype=torch.float64) + 0.1
    sandwich_torch_tiled(X, d, 4, 4, 32)
    sandwich_torch_compile_tiled(X, d, 4, 4, 32)


def warmup_torch_compile() -> None:
    X = torch.randn(64, 8, dtype=torch.float64)
    d = torch.rand(64, dtype=torch.float64) + 0.1
    sandwich_torch_compile_einsum(X, d)
    sandwich_torch_compile_weighted_gram(X, d)
