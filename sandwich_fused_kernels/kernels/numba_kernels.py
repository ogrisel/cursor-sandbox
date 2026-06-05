"""Numba-compiled fused sandwich kernels for CPU."""

from __future__ import annotations

import numpy as np
from numba import njit, prange


@njit(cache=True)
def sandwich_numba_serial(X: np.ndarray, d: np.ndarray) -> np.ndarray:
    """Serial fused kernel: out[i,j] = sum_k X[k,i]*d[k]*X[k,j]."""
    n_rows, n_cols = X.shape
    out = np.zeros((n_cols, n_cols), dtype=X.dtype)
    for j in range(n_cols):
        for i in range(j, n_cols):
            acc = X.dtype.type(0.0)
            for k in range(n_rows):
                acc += X[k, i] * d[k] * X[k, j]
            out[i, j] = acc
            out[j, i] = acc
    return out


@njit(parallel=True, fastmath=True, cache=True)
def sandwich_numba_k_inner(X: np.ndarray, d: np.ndarray) -> np.ndarray:
    """Parallel over columns with k as innermost loop (LLVM emits AVX2 ymm)."""
    n_rows, n_cols = X.shape
    out = np.zeros((n_cols, n_cols), dtype=X.dtype)
    for j in prange(n_cols):
        for i in range(n_cols):
            acc = X.dtype.type(0.0)
            for k in range(n_rows):
                acc += X[k, i] * d[k] * X[k, j]
            out[i, j] = acc
    return out


@njit(parallel=True, fastmath=True, cache=True)
def sandwich_numba_parallel(X: np.ndarray, d: np.ndarray) -> np.ndarray:
    """Parallel over output columns; symmetric accumulation."""
    n_rows, n_cols = X.shape
    out = np.zeros((n_cols, n_cols), dtype=X.dtype)
    for j in prange(n_cols):
        for i in range(j, n_cols):
            acc = X.dtype.type(0.0)
            for k in range(n_rows):
                acc += X[k, i] * d[k] * X[k, j]
            out[i, j] = acc
            out[j, i] = acc
    return out


@njit(parallel=True, fastmath=True, cache=True)
def sandwich_numba_fused_blocked(X: np.ndarray, d: np.ndarray) -> np.ndarray:
    """Blocked fused kernel: no weighted-X buffer; k fused in inner accumulation."""
    n_rows, n_cols = X.shape
    block = 32
    out = np.zeros((n_cols, n_cols), dtype=X.dtype)
    n_blocks = (n_cols + block - 1) // block

    for jb in prange(n_blocks):
        j0 = jb * block
        j1 = j0 + block
        if j1 > n_cols:
            j1 = n_cols
        nj = j1 - j0
        for ib in range(n_blocks):
            i0 = ib * block
            i1 = i0 + block
            if i1 > n_cols:
                i1 = n_cols
            ni = i1 - i0
            acc = np.zeros((ni, nj), dtype=X.dtype)
            for k in range(n_rows):
                w = d[k]
                for li in range(ni):
                    xi = X[k, i0 + li] * w
                    for lj in range(nj):
                        acc[li, lj] += xi * X[k, j0 + lj]
            for li in range(ni):
                for lj in range(nj):
                    out[i0 + li, j0 + lj] += acc[li, lj]
    return out


@njit(cache=True)
def sandwich_numba_blas_fused(X: np.ndarray, d: np.ndarray) -> np.ndarray:
    """Single BLAS call: (X * d).T @ X (materializes weighted X)."""
    weighted = X * d.reshape(-1, 1)
    return weighted.T @ X


@njit(parallel=True, fastmath=True, cache=True)
def sandwich_numba_blas_chunked(X: np.ndarray, d: np.ndarray) -> np.ndarray:
    """Chunk rows and delegate each chunk to BLAS (weighted Gram), then reduce."""
    n_rows, n_cols = X.shape
    chunk = 8192
    n_chunks = (n_rows + chunk - 1) // chunk
    partial = np.zeros((n_chunks, n_cols, n_cols), dtype=X.dtype)

    for cb in prange(n_chunks):
        k0 = cb * chunk
        k1 = k0 + chunk
        if k1 > n_rows:
            k1 = n_rows
        Xc = X[k0:k1]
        dc = d[k0:k1]
        weighted = Xc * dc.reshape(-1, 1)
        partial[cb] = weighted.T @ Xc
    return np.sum(partial, axis=0)


@njit(parallel=True, fastmath=True, cache=True)
def sandwich_numba_blas_tiled(X: np.ndarray, d: np.ndarray) -> np.ndarray:
    """Smaller row chunks (2048) to improve cache locality vs blas_chunked."""
    n_rows, n_cols = X.shape
    chunk = 2048
    n_chunks = (n_rows + chunk - 1) // chunk
    partial = np.zeros((n_chunks, n_cols, n_cols), dtype=X.dtype)

    for cb in prange(n_chunks):
        k0 = cb * chunk
        k1 = k0 + chunk
        if k1 > n_rows:
            k1 = n_rows
        Xc = X[k0:k1]
        dc = d[k0:k1]
        weighted = Xc * dc.reshape(-1, 1)
        partial[cb] = weighted.T @ Xc
    return np.sum(partial, axis=0)


@njit(parallel=True, fastmath=True, cache=True)
def sandwich_numba_k_parallel(X: np.ndarray, d: np.ndarray) -> np.ndarray:
    """Parallel over row blocks; each block writes to a private partial matrix."""
    n_rows, n_cols = X.shape
    k_block = 256
    n_k_blocks = (n_rows + k_block - 1) // k_block
    partial = np.zeros((n_k_blocks, n_cols, n_cols), dtype=X.dtype)

    for kb in prange(n_k_blocks):
        k0 = kb * k_block
        k1 = k0 + k_block
        if k1 > n_rows:
            k1 = n_rows
        for j in range(n_cols):
            for i in range(j, n_cols):
                acc = X.dtype.type(0.0)
                for k in range(k0, k1):
                    acc += X[k, i] * d[k] * X[k, j]
                partial[kb, i, j] = acc
                partial[kb, j, i] = acc
    return np.sum(partial, axis=0)


_VARIANTS = {
    "serial": sandwich_numba_serial,
    "parallel": sandwich_numba_parallel,
    "k_inner": sandwich_numba_k_inner,
    "fused_blocked": sandwich_numba_fused_blocked,
    "blas_fused": sandwich_numba_blas_fused,
    "blas_chunked": sandwich_numba_blas_chunked,
    "blas_tiled": sandwich_numba_blas_tiled,
    "k_parallel": sandwich_numba_k_parallel,
    # Legacy aliases kept for benchmark continuity.
    "blocked": sandwich_numba_fused_blocked,
}


def sandwich_numba(
    X: np.ndarray,
    d: np.ndarray,
    rows: np.ndarray | None = None,
    cols: np.ndarray | None = None,
    variant: str = "fused_blocked",
) -> np.ndarray:
    """Dispatch to a compiled numba kernel on contiguous row/column subsets."""
    if rows is None:
        rows = np.arange(X.shape[0], dtype=np.int64)
    if cols is None:
        cols = np.arange(X.shape[1], dtype=np.int64)

    X_sub = np.ascontiguousarray(X[np.ix_(rows, cols)])
    d_sub = np.ascontiguousarray(np.asarray(d, dtype=X.dtype)[rows])
    fn = _VARIANTS[variant]
    return fn(X_sub, d_sub)


def warmup_numba(variant: str = "fused_blocked") -> None:
    """Trigger JIT compilation before timed runs."""
    rng = np.random.default_rng(0)
    X = rng.standard_normal((128, 16), dtype=np.float64)
    d = rng.random(128, dtype=np.float64)
    sandwich_numba(X, d, variant=variant)
