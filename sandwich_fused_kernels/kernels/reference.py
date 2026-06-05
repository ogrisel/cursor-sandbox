"""Reference sandwich product for correctness checks."""

from __future__ import annotations

import numpy as np


def sandwich_reference(
    X: np.ndarray,
    d: np.ndarray,
    rows: np.ndarray | None = None,
    cols: np.ndarray | None = None,
) -> np.ndarray:
    """Compute X[rows, cols].T @ diag(d[rows]) @ X[rows, cols] in pure Python."""
    if rows is None:
        rows = np.arange(X.shape[0], dtype=np.int64)
    if cols is None:
        cols = np.arange(X.shape[1], dtype=np.int64)

    X_sub = np.ascontiguousarray(X[np.ix_(rows, cols)])
    d_sub = np.asarray(d, dtype=X.dtype)[rows]
    weighted = X_sub * d_sub[:, np.newaxis]
    return weighted.T @ X_sub
