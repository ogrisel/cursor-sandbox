#!/usr/bin/env python
"""Compare sklearn pairwise distance paths against a non-BLAS reference."""

from __future__ import annotations

import os
import sys

import numpy as np
from sklearn import config_context
from sklearn.impute import KNNImputer
from sklearn.metrics import pairwise_distances_chunked
from sklearn.metrics.pairwise import nan_euclidean_distances, pairwise_distances

from numpy_blis_reproducer import (
    _KNN_SIMPLE_EXAMPLE,
    _KNN_WEIGHT_DISTANCE,
    _conda_libblas_build,
    _nan_euclidean_reference,
)


def _check_distances(name: str, x: np.ndarray, missing_values: float) -> list[str]:
    ref = _nan_euclidean_reference(x, missing_values=missing_values)
    failures: list[str] = []

    for label, dist in (
        ("nan_euclidean_distances", nan_euclidean_distances(x, missing_values=missing_values)),
        (
            "pairwise_distances",
            pairwise_distances(
                x, metric="nan_euclidean", squared=False, missing_values=missing_values
            ),
        ),
    ):
        if not np.allclose(dist, ref, rtol=0, atol=0, equal_nan=True):
            err = float(np.nanmax(np.abs(dist - ref)))
            n_bad = int(np.sum(~np.isclose(dist, ref, rtol=0, atol=0, equal_nan=True)))
            failures.append(f"{name}/{label}: max_abs_err={err:.6g} n_bad={n_bad}")

    chunks: list[np.ndarray] = []
    with config_context(working_memory=0):
        for chunk in pairwise_distances_chunked(
            x,
            metric="nan_euclidean",
            squared=False,
            missing_values=missing_values,
        ):
            chunks.append(np.asarray(chunk))
    dist_chunked = np.vstack(chunks)
    if not np.allclose(dist_chunked, ref, rtol=0, atol=0, equal_nan=True):
        err = float(np.nanmax(np.abs(dist_chunked - ref)))
        n_bad = int(np.sum(~np.isclose(dist_chunked, ref, rtol=0, atol=0, equal_nan=True)))
        failures.append(f"{name}/pairwise_distances_chunked: max_abs_err={err:.6g} n_bad={n_bad}")

    return failures


def _check_knn_imputer(name: str, x: np.ndarray, missing_values: float) -> list[str]:
    failures: list[str] = []
    x = np.array(x, dtype=np.float64, copy=True)
    if not np.isnan(missing_values):
        x = np.where(np.isnan(x), missing_values, x)

    if name == "knn_simple" and np.isnan(missing_values):
        r0c1 = np.mean(x[1:6, 1])
        r0c3 = np.mean(x[2:-1, -1])
        r1c3 = np.mean(x[2:-1, -1])
        r2c2 = np.mean(x[[0, 1, 3, 4, 5], 2])
        r7c0 = np.mean(x[2:-1, 0])
        expected = np.array(
            [
                [0, r0c1, 0, r0c3],
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
        with config_context(working_memory=0):
            imputed = KNNImputer(missing_values=missing_values).fit_transform(x)
        if not np.allclose(imputed, expected, rtol=0, atol=0, equal_nan=True):
            err = float(np.max(np.abs(imputed - expected)))
            failures.append(f"{name}/KNNImputer: max_abs_err={err:.6g}")
            failures.append(f"  imputed[2,2]={imputed[2, 2]} expected[2,2]={expected[2, 2]}")
    return failures


def main() -> int:
    failures: list[str] = []
    for missing_values in (np.nan, -1.0):
        mv = "nan" if np.isnan(missing_values) else "minus1"
        x_simple = _KNN_SIMPLE_EXAMPLE.copy()
        x_weight = _KNN_WEIGHT_DISTANCE.copy()
        if not np.isnan(missing_values):
            x_simple = np.where(np.isnan(_KNN_SIMPLE_EXAMPLE), missing_values, x_simple)
            x_weight = np.where(np.isnan(_KNN_WEIGHT_DISTANCE), missing_values, x_weight)

        failures.extend(_check_distances(f"knn_simple[{mv}]", x_simple, missing_values))
        failures.extend(_check_distances(f"knn_weight[{mv}]", x_weight, missing_values))
        failures.extend(_check_knn_imputer("knn_simple", x_simple, missing_values))

    print(f"conda_libblas_build={_conda_libblas_build() or 'unknown'}")
    print(f"BLIS_NUM_THREADS={os.getenv('BLIS_NUM_THREADS')}")
    print(f"OMP_NUM_THREADS={os.getenv('OMP_NUM_THREADS')}")
    print(f"OPENBLAS_NUM_THREADS={os.getenv('OPENBLAS_NUM_THREADS')}")

    if failures:
        print("FAIL")
        for msg in failures[:30]:
            print(f"  - {msg}")
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
