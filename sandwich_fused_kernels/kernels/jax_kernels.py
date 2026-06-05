"""JAX-compiled fused sandwich kernels for CPU."""

from __future__ import annotations

import numpy as np

import jax
import jax.numpy as jnp


@jax.jit
def _sandwich_jax_einsum(X: jnp.ndarray, d: jnp.ndarray) -> jnp.ndarray:
    """Fully fused contraction; no explicit weighted-X buffer in source."""
    return jnp.einsum("ki,k,kj->ij", X, d, X)


@jax.jit
def _sandwich_jax_weighted_gram(X: jnp.ndarray, d: jnp.ndarray) -> jnp.ndarray:
    weighted = X * d[:, None]
    return weighted.T @ X


@jax.jit
def _sandwich_jax_tensordot(X: jnp.ndarray, d: jnp.ndarray) -> jnp.ndarray:
    weighted = X * d[:, None]
    return jnp.tensordot(weighted, X, axes=([0], [0]))


@jax.jit
def _sandwich_jax_scan_chunked(X: jnp.ndarray, d: jnp.ndarray, chunk: int = 4096) -> jnp.ndarray:
    """Row-chunked Gram accumulation; peak workspace is O(chunk * m) not O(n * m)."""
    n_rows, n_cols = X.shape
    n_chunks = (n_rows + chunk - 1) // chunk
    pad_rows = n_chunks * chunk - n_rows
    Xp = jnp.pad(X, ((0, pad_rows), (0, 0)))
    dp = jnp.pad(d, (0, pad_rows))
    x_chunks = Xp.reshape(n_chunks, chunk, n_cols)
    d_chunks = dp.reshape(n_chunks, chunk)

    def body(carry: jnp.ndarray, xd: tuple[jnp.ndarray, jnp.ndarray]) -> tuple[jnp.ndarray, None]:
        xc, dc = xd
        return carry + jnp.dot((xc * dc[:, None]).T, xc), None

    init = jnp.zeros((n_cols, n_cols), dtype=X.dtype)
    out, _ = jax.lax.scan(body, init, (x_chunks, d_chunks))
    return out


@jax.jit
def _sandwich_jax_einsum_chunked(X: jnp.ndarray, d: jnp.ndarray, chunk: int = 4096) -> jnp.ndarray:
    """Chunked einsum accumulation without materializing full weighted X."""
    n_rows, n_cols = X.shape
    n_chunks = (n_rows + chunk - 1) // chunk
    pad_rows = n_chunks * chunk - n_rows
    Xp = jnp.pad(X, ((0, pad_rows), (0, 0)))
    dp = jnp.pad(d, (0, pad_rows))
    x_chunks = Xp.reshape(n_chunks, chunk, n_cols)
    d_chunks = dp.reshape(n_chunks, chunk)

    def body(carry: jnp.ndarray, xd: tuple[jnp.ndarray, jnp.ndarray]) -> tuple[jnp.ndarray, None]:
        xc, dc = xd
        return carry + jnp.einsum("ki,k,kj->ij", xc, dc, xc), None

    init = jnp.zeros((n_cols, n_cols), dtype=X.dtype)
    out, _ = jax.lax.scan(body, init, (x_chunks, d_chunks))
    return out


_VARIANTS = {
    "einsum": _sandwich_jax_einsum,
    "weighted_gram": _sandwich_jax_weighted_gram,
    "tensordot": _sandwich_jax_tensordot,
    "scan_chunked": _sandwich_jax_scan_chunked,
    "einsum_chunked": _sandwich_jax_einsum_chunked,
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

    X_sub = np.ascontiguousarray(X[np.ix_(rows, cols)], dtype=X.dtype)
    d_sub = np.ascontiguousarray(np.asarray(d, dtype=X.dtype)[rows], dtype=X.dtype)

    fn = _VARIANTS[variant]
    out = fn(jnp.asarray(X_sub), jnp.asarray(d_sub))
    return np.asarray(jax.device_get(out))


def warmup_jax(variant: str = "einsum") -> None:
    rng = np.random.default_rng(0)
    X = rng.standard_normal((128, 16), dtype=np.float64)
    d = rng.random(128, dtype=np.float64)
    sandwich_jax(X, d, variant=variant)
    jax.block_until_ready(_VARIANTS[variant](jnp.asarray(X), jnp.asarray(d)))
