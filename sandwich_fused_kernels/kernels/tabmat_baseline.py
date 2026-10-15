"""tabmat DenseMatrix.sandwich baseline."""

from __future__ import annotations

import numpy as np
import tabmat


def sandwich_tabmat(
    X: np.ndarray,
    d: np.ndarray,
    rows: np.ndarray | None = None,
    cols: np.ndarray | None = None,
) -> np.ndarray:
    """Call tabmat's C++/Cython dense sandwich kernel."""
    matrix = tabmat.DenseMatrix(np.ascontiguousarray(X))
    return matrix.sandwich(d, rows=rows, cols=cols)
