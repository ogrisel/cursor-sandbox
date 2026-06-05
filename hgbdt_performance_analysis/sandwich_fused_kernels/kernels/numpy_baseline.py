"""Naive NumPy sandwich product baselines."""

from __future__ import annotations

import numpy as np


def sandwich_numpy_diag_matmul(
    X: np.ndarray,
    d: np.ndarray,
    rows: np.ndarray | None = None,
    cols: np.ndarray | None = None,
) -> np.ndarray:
    """Materialize diag(d) and use two matmuls: X.T @ diag(d) @ X."""
    if rows is None:
        rows = np.arange(X.shape[0], dtype=np.int64)
    if cols is None:
        cols = np.arange(X.shape[1], dtype=np.int64)

    X_sub = X[np.ix_(rows, cols)]
    d_sub = np.asarray(d, dtype=X.dtype)[rows]
    return X_sub.T @ (d_sub[:, np.newaxis] * X_sub)


def sandwich_numpy_einsum(
    X: np.ndarray,
    d: np.ndarray,
    rows: np.ndarray | None = None,
    cols: np.ndarray | None = None,
) -> np.ndarray:
    """Fused einsum without explicit diag(d): sum_k X[k,i]*d[k]*X[k,j]."""
    if rows is None:
        rows = np.arange(X.shape[0], dtype=np.int64)
    if cols is None:
        cols = np.arange(X.shape[1], dtype=np.int64)

    X_sub = X[np.ix_(rows, cols)]
    d_sub = np.asarray(d, dtype=X.dtype)[rows]
    return np.einsum("ki,k,kj->ij", X_sub, d_sub, X_sub, optimize=True)


def sandwich_numpy_weighted_gram(
    X: np.ndarray,
    d: np.ndarray,
    rows: np.ndarray | None = None,
    cols: np.ndarray | None = None,
) -> np.ndarray:
    """Scale rows then Gram product: (sqrt(d)*X).T @ (sqrt(d)*X) style via row weights."""
    if rows is None:
        rows = np.arange(X.shape[0], dtype=np.int64)
    if cols is None:
        cols = np.arange(X.shape[1], dtype=np.int64)

    X_sub = X[np.ix_(rows, cols)]
    d_sub = np.asarray(d, dtype=X.dtype)[rows]
    weighted = X_sub * d_sub[:, np.newaxis]
    return weighted.T @ X_sub
