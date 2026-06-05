"""JAX-compiled fused sandwich kernels for CPU."""

from __future__ import annotations

import numpy as np

import jax
import jax.numpy as jnp


@jax.jit
def _sandwich_jax_einsum(X: jnp.ndarray, d: jnp.ndarray) -> jnp.ndarray:
    return jnp.einsum("ki,k,kj->ij", X, d, X)


@jax.jit
def _sandwich_jax_weighted_gram(X: jnp.ndarray, d: jnp.ndarray) -> jnp.ndarray:
    weighted = X * d[:, None]
    return weighted.T @ X


@jax.jit
def _sandwich_jax_tensordot(X: jnp.ndarray, d: jnp.ndarray) -> jnp.ndarray:
    """Fused row-weighted Gram via tensordot (avoids explicit diag)."""
    weighted = X * d[:, None]
    return jnp.tensordot(weighted, X, axes=([0], [0]))


_VARIANTS = {
    "einsum": _sandwich_jax_einsum,
    "weighted_gram": _sandwich_jax_weighted_gram,
    "tensordot": _sandwich_jax_tensordot,
}


def sandwich_jax(
    X: np.ndarray,
    d: np.ndarray,
    rows: np.ndarray | None = None,
    cols: np.ndarray | None = None,
    variant: str = "einsum",
) -> np.ndarray:
    if rows is None:
        rows = np.arange(X.shape[0], dtype=np.int64)
    if cols is None:
        cols = np.arange(X.shape[1], dtype=np.int64)

    X_sub = np.ascontiguousarray(X[np.ix_(rows, cols)], dtype=np.float64)
    d_sub = np.ascontiguousarray(np.asarray(d, dtype=X.dtype)[rows], dtype=np.float64)

    fn = _VARIANTS[variant]
    out = fn(jnp.asarray(X_sub), jnp.asarray(d_sub))
    return np.asarray(jax.device_get(out))


def warmup_jax(variant: str = "einsum") -> None:
    rng = np.random.default_rng(0)
    X = rng.standard_normal((128, 16), dtype=np.float64)
    d = rng.random(128, dtype=np.float64)
    sandwich_jax(X, d, variant=variant)
    jax.block_until_ready(_VARIANTS[variant](jnp.asarray(X), jnp.asarray(d)))
