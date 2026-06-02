#!/usr/bin/env python
"""
Progressive minimal reproducers for the macOS arm64 BLIS / KNN imputer failure.

Levels strip sklearn piece by piece (run with --level <name>; see --list-levels).

Smallest sklearn surface: ``knn-imputer-only`` (``KNNImputer`` vs golden ``2.3``).
Primary CI gate: ``scalar-vs-imputer`` (scalar ``nan_euclidean`` for row 2 vs
``KNNImputer`` at ``[2,2]`` only — no ``pairwise_distances``, no pytest).
"""

from __future__ import annotations

import argparse
import subprocess
import sys

import numpy as np

# 8×4 block from sklearn/impute/tests/test_knn.py::test_knn_imputer_weight_distance
X_WEIGHT_8X4 = np.array(
    [
        [0, 0, 0, np.nan],
        [1, 1, 1, np.nan],
        [2, 2, np.nan, 2],
        [3, 3, 3, 3],
        [4, 4, 4, 4],
        [5, 5, 5, 5],
        [6, 6, 6, 6],
        [np.nan, 7, 7, 7],
    ],
    dtype=np.float64,
)

# Ordered from smallest sklearn surface to largest (plus numpy-gemm control).
LEVELS = (
    "knn-imputer-only",
    "scalar-vs-imputer",
    "scalar-full-matrix",
    "sklearn-dist-vs-imputer",
    "pytest",
    "numpy-gemm",
)


def _missing_mask(x: np.ndarray, missing_values: float) -> np.ndarray:
    if np.isnan(missing_values):
        return np.isnan(x)
    return x == missing_values


def _nan_euclidean_pair(
    x: np.ndarray,
    i: int,
    j: int,
    *,
    miss: np.ndarray | None = None,
    missing_values: float = np.nan,
) -> float:
    """One nan_euclidean distance (pure Python/NumPy dot, no GEMM)."""
    if miss is None:
        miss = _missing_mask(x, missing_values)
    mask = ~(miss[i] | miss[j])
    n_present = int(mask.sum())
    if n_present == 0:
        return float("nan")
    diff = x[i, mask] - x[j, mask]
    sq = float(np.dot(diff, diff))
    return float(np.sqrt(x.shape[1] / n_present * sq))


def _nan_euclidean_scalar(x: np.ndarray, missing_values: float = np.nan) -> np.ndarray:
    """Full distance matrix via scalar loops (reference for matrix-level checks)."""
    miss = _missing_mask(x, missing_values)
    n = x.shape[0]
    out = np.empty((n, n), dtype=np.float64)
    for i in range(n):
        for j in range(n):
            out[i, j] = _nan_euclidean_pair(x, i, j, miss=miss)
    return out


def _nan_euclidean_gemm(x: np.ndarray, missing_values: float = np.nan) -> np.ndarray:
    from numpy_blis_reproducer import _nan_euclidean_via_gemm

    return _nan_euclidean_via_gemm(x, missing_values=missing_values)


def _expected_8x4_from_dist(x: np.ndarray, dist: np.ndarray) -> np.ndarray:
    """Weighted-average imputation expected values (test_knn_imputer_weight_distance)."""
    r0c3 = np.average(x[2:-1, -1], weights=1.0 / dist[0, 2:-1])
    r1c3 = np.average(x[2:-1, -1], weights=1.0 / dist[1, 2:-1])
    r2c2 = np.average(x[(0, 1, 3, 4, 5), 2], weights=1.0 / dist[2, (0, 1, 3, 4, 5)])
    r7c0 = np.average(x[2:7, 0], weights=1.0 / dist[7, 2:7])
    return np.array(
        [
            [0, 0, 0, r0c3],
            [1, 1, 1, r1c3],
            [2, 2, r2c2, 2],
            [3, 3, 3, 3],
            [4, 4, 4, 4],
            [5, 5, 5, 5],
            [6, 6, 6, 6],
            [r7c0, 7, 7, 7],
        ],
        dtype=np.float64,
    )


_LEVEL = "scalar-vs-imputer"


def _fail(msg: str) -> int:
    print(f"FAIL [{_LEVEL}]: {msg}")
    return 1


def _pass() -> int:
    print(f"PASS [{_LEVEL}]")
    return 0


def run_numpy_gemm() -> int:
    """NumPy GEMM nan_euclidean vs scalar loop (control; usually passes on BLIS)."""
    global _LEVEL
    _LEVEL = "numpy-gemm"
    dist_ref = _nan_euclidean_scalar(X_WEIGHT_8X4)
    dist_gemm = _nan_euclidean_gemm(X_WEIGHT_8X4)
    if not np.allclose(dist_gemm, dist_ref, rtol=0, atol=1e-12, equal_nan=True):
        err = float(np.nanmax(np.abs(dist_gemm - dist_ref)))
        return _fail(f"GEMM vs scalar distance max_abs_err={err:.6g}")
    return _pass()


def run_scalar_vs_imputer() -> int:
    """Minimal: one cell — scalar pair distances vs KNNImputer (only sklearn call)."""
    global _LEVEL
    _LEVEL = "scalar-vs-imputer"
    from sklearn import config_context
    from sklearn.impute import KNNImputer

    neighbors = (0, 1, 3, 4, 5)
    miss = _missing_mask(X_WEIGHT_8X4, np.nan)
    inv_dist = np.array(
        [
            1.0 / _nan_euclidean_pair(X_WEIGHT_8X4, 2, j, miss=miss)
            for j in neighbors
        ],
        dtype=np.float64,
    )
    expected_r2c2 = float(
        np.average(X_WEIGHT_8X4[list(neighbors), 2], weights=inv_dist)
    )
    with config_context(working_memory=0):
        actual = KNNImputer(missing_values=np.nan, weights="distance").fit_transform(
            X_WEIGHT_8X4
        )
    actual_r2c2 = float(actual[2, 2])
    if not np.isclose(actual_r2c2, expected_r2c2, rtol=0, atol=0):
        return _fail(
            f"imputed[2,2]={actual_r2c2} expected={expected_r2c2} "
            f"(upstream CI: ~0.5 vs ~2.3 on BLIS)"
        )
    return _pass()


def run_scalar_full_matrix() -> int:
    """Full 8×4 — expected from scalar distances, actual from KNNImputer."""
    global _LEVEL
    _LEVEL = "scalar-full-matrix"
    from sklearn import config_context
    from sklearn.impute import KNNImputer

    dist = _nan_euclidean_scalar(X_WEIGHT_8X4)
    expected = _expected_8x4_from_dist(X_WEIGHT_8X4, dist)
    with config_context(working_memory=0):
        actual = KNNImputer(missing_values=np.nan, weights="distance").fit_transform(
            X_WEIGHT_8X4
        )
    if not np.allclose(actual, expected, rtol=0, atol=0, equal_nan=True):
        err = float(np.max(np.abs(actual - expected)))
        return _fail(f"full matrix max_abs_err={err:.6g} (imputed[2,2]={actual[2, 2]})")
    return _pass()


def run_sklearn_dist_vs_imputer() -> int:
    """Expected from sklearn ``pairwise_distances`` (full) vs ``KNNImputer`` (chunked)."""
    global _LEVEL
    _LEVEL = "sklearn-dist-vs-imputer"
    from sklearn import config_context
    from sklearn.impute import KNNImputer
    from sklearn.metrics.pairwise import pairwise_distances

    dist = pairwise_distances(
        X_WEIGHT_8X4,
        metric="nan_euclidean",
        squared=False,
        missing_values=np.nan,
    )
    expected = _expected_8x4_from_dist(X_WEIGHT_8X4, dist)
    with config_context(working_memory=0):
        actual = KNNImputer(missing_values=np.nan, weights="distance").fit_transform(
            X_WEIGHT_8X4
        )
    if not np.allclose(actual, expected, rtol=0, atol=0, equal_nan=True):
        err = float(np.max(np.abs(actual - expected)))
        return _fail(f"sklearn full-dist vs imputer max_abs_err={err:.6g}")
    return _pass()


def run_knn_imputer_only() -> int:
    """Smallest sklearn surface: only ``KNNImputer``, literal golden ``[2,2]``."""
    global _LEVEL
    _LEVEL = "knn-imputer-only"
    from sklearn import config_context
    from sklearn.impute import KNNImputer

    # Analytic value from the test recipe with correct distances (≈2.3).
    golden_r2c2 = 2.3
    with config_context(working_memory=0):
        actual_r2c2 = float(
            KNNImputer(missing_values=np.nan, weights="distance").fit_transform(
                X_WEIGHT_8X4
            )[2, 2]
        )
    if not np.isclose(actual_r2c2, golden_r2c2, rtol=0, atol=0):
        return _fail(f"imputed[2,2]={actual_r2c2} golden={golden_r2c2}")
    return _pass()


def run_pytest() -> int:
    """Full upstream pytest subset (largest sklearn surface)."""
    global _LEVEL
    _LEVEL = "pytest"
    cmd = [
        sys.executable,
        "-m",
        "pytest",
        "-xvs",
        "--tb=short",
        "--pyargs",
        "sklearn.impute.tests.test_knn",
        "-k",
        "test_knn_imputer_weight_distance and nan",
    ]
    print("Running:", " ".join(cmd), flush=True)
    return subprocess.call(cmd)


_RUNNERS = {
    "knn-imputer-only": run_knn_imputer_only,
    "scalar-vs-imputer": run_scalar_vs_imputer,
    "scalar-full-matrix": run_scalar_full_matrix,
    "sklearn-dist-vs-imputer": run_sklearn_dist_vs_imputer,
    "pytest": run_pytest,
    "numpy-gemm": run_numpy_gemm,
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--level",
        choices=LEVELS,
        default="scalar-vs-imputer",
        help="Reproducer level (default: scalar-vs-imputer)",
    )
    parser.add_argument(
        "--list-levels",
        action="store_true",
        help="Print available levels and exit",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.list_levels:
        descriptions = {
            "knn-imputer-only": "KNNImputer only vs literal 2.3",
            "scalar-vs-imputer": "KNNImputer vs scalar nan_euclidean for [2,2]",
            "scalar-full-matrix": "KNNImputer vs scalar distances (8x4)",
            "sklearn-dist-vs-imputer": "KNNImputer vs pairwise_distances (full)",
            "pytest": "upstream test_knn_imputer_weight_distance[nan]",
            "numpy-gemm": "NumPy GEMM nan_euclidean vs scalar (no sklearn)",
        }
        for name in LEVELS:
            print(f"  {name}: {descriptions[name]}")
        return 0
    return _RUNNERS[args.level]()


if __name__ == "__main__":
    sys.exit(main())
