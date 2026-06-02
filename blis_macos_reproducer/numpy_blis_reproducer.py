#!/usr/bin/env python
"""NumPy-only reproducer for BLIS DGEMM issues seen in sklearn KNN imputer CI."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import os
from concurrent.futures import ThreadPoolExecutor
from typing import Any

import numpy as np

# Fixed inputs from sklearn/impute/tests/test_knn.py (macOS BLIS CI failures).
_KNN_SIMPLE_EXAMPLE = np.array(
    [
        [0, np.nan, 0, np.nan],
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

_KNN_WEIGHT_DISTANCE = np.array(
    [
        [np.nan, 0, 0],
        [2, 1, 2],
        [3, 2, 3],
        [4, 5, 5],
    ],
    dtype=np.float64,
)


def _missing_mask(x: np.ndarray, missing_values: float) -> np.ndarray:
    if np.isnan(missing_values):
        return np.isnan(x)
    return x == missing_values


def _nan_euclidean_via_gemm(x: np.ndarray, missing_values: float = np.nan) -> np.ndarray:
    """Port of sklearn.metrics.pairwise.nan_euclidean_distances (uses X @ X.T GEMM)."""
    x = np.array(x, dtype=np.float64, copy=True)
    missing_x = _missing_mask(x, missing_values)
    missing_y = missing_x
    x[missing_x] = 0.0
    y = x

    # euclidean_distances(..., squared=True) core
    distances = -2.0 * (x @ y.T)
    row_sq = np.sum(x * x, axis=1, keepdims=True)
    distances += row_sq
    distances += row_sq.T
    np.maximum(distances, 0.0, out=distances)

    xx = x * x
    yy = y * y
    distances -= xx @ missing_y.T
    distances -= missing_x @ yy.T
    np.clip(distances, 0.0, None, out=distances)
    np.fill_diagonal(distances, 0.0)

    # Match sklearn.metrics.pairwise.nan_euclidean_distances exactly.
    present_x = 1 - missing_x
    present_y = present_x if missing_y is missing_x else ~missing_y
    present_count = np.dot(present_x, present_y.T)
    distances[present_count == 0] = np.nan
    np.maximum(1, present_count, out=present_count)
    distances /= present_count
    distances *= x.shape[1]
    return np.sqrt(distances, out=distances)


def _nan_euclidean_reference(x: np.ndarray, missing_values: float = np.nan) -> np.ndarray:
    """Scalar reference without BLAS GEMM."""
    n = x.shape[0]
    out = np.empty((n, n), dtype=np.float64)
    for i in range(n):
        for j in range(n):
            mask = ~(_missing_mask(x[i : i + 1], missing_values)[0] |
                     _missing_mask(x[j : j + 1], missing_values)[0])
            n_present = int(mask.sum())
            if n_present == 0:
                out[i, j] = np.nan
                continue
            diff = x[i, mask] - x[j, mask]
            sq = float(np.dot(diff, diff))
            weight = x.shape[1] / n_present
            out[i, j] = np.sqrt(weight * sq)
    return out


def _digest(a: np.ndarray) -> str:
    return hashlib.sha256(np.ascontiguousarray(a).view(np.uint8)).hexdigest()


def _detected_blas_name() -> str:
    if hasattr(np.__config__, "show"):
        try:
            cfg: dict[str, Any] = np.__config__.show(mode="dicts")
            return str(
                cfg.get("Build Dependencies", {}).get("blas", {}).get("name", "")
            ).lower()
        except TypeError:
            pass
    return ""


def _conda_libblas_build() -> str:
    for exe in ("mamba", "micromamba", "conda"):
        try:
            out = subprocess.check_output(
                [exe, "list", "--json", "libblas"],
                text=True,
                stderr=subprocess.DEVNULL,
            )
        except (FileNotFoundError, subprocess.CalledProcessError):
            continue
        for pkg in json.loads(out):
            return str(pkg.get("build_string", "")).lower()
    return ""


def _backend_matches(expected: str, numpy_name: str, conda_build: str) -> bool:
    fragment = "newaccelerate" if expected == "newaccelerate" else expected
    if fragment in conda_build:
        return True
    if expected == "newaccelerate" and "accelerate" in numpy_name:
        return True
    return fragment in numpy_name


def _fork_stress(
    x: np.ndarray,
    missing_values: float,
    processes: int,
    iterations: int,
    ref: np.ndarray,
    atol: float,
    rtol: float,
) -> list[str]:
    """Fork workers to stress BLIS (macOS sklearn CI uses fork + threaded BLAS)."""
    failures: list[str] = []
    digests: list[str] = []
    x_c = np.ascontiguousarray(x)
    mv = float("nan") if np.isnan(missing_values) else float(missing_values)

    for _ in range(iterations):
        kids: list[int] = []
        for _p in range(processes):
            pid = os.fork()
            if pid == 0:
                _nan_euclidean_via_gemm(
                    np.array(x_c, copy=True), missing_values=mv
                )
                os._exit(0)
            kids.append(pid)
        for pid in kids:
            os.waitpid(pid, 0)
        digests.append(_digest(_nan_euclidean_via_gemm(x, missing_values=mv)))

    if len(set(digests)) != 1:
        failures.append(
            f"fork_stress: non-deterministic digests "
            f"({len(set(digests))}/{len(digests)} unique)"
        )
    if not np.allclose(
        _nan_euclidean_via_gemm(x, missing_values=missing_values),
        ref,
        atol=atol,
        rtol=rtol,
        equal_nan=True,
    ):
        failures.append("fork_stress: final matrix mismatches reference")
    return failures


def _threaded_stress(
    x: np.ndarray,
    missing_values: float,
    workers: int,
    iterations: int,
    ref: np.ndarray,
    atol: float,
    rtol: float,
) -> list[str]:
    """Hammer GEMM from multiple threads (catches threaded BLIS races)."""

    def _once(_: int) -> str:
        return _digest(_nan_euclidean_via_gemm(x, missing_values=missing_values))

    failures: list[str] = []
    with ThreadPoolExecutor(max_workers=workers) as pool:
        digests = list(pool.map(_once, range(iterations)))

    if len(set(digests)) != 1:
        failures.append(
            f"threaded_stress: non-deterministic digests "
            f"({len(set(digests))}/{len(digests)} unique)"
        )
        return failures

    dist = _nan_euclidean_via_gemm(x, missing_values=missing_values)
    if not np.allclose(dist, ref, atol=atol, rtol=rtol, equal_nan=True):
        failures.append("threaded_stress: final matrix mismatches reference")
    return failures


def _check_case(
    name: str,
    x: np.ndarray,
    missing_values: float,
    repeats: int,
    stress_workers: int,
    stress_iterations: int,
    fork_processes: int,
    fork_iterations: int,
    atol: float,
    rtol: float,
) -> list[str]:
    ref = _nan_euclidean_reference(x, missing_values=missing_values)
    failures: list[str] = []
    digests: list[str] = []

    for i in range(repeats):
        dist = _nan_euclidean_via_gemm(x, missing_values=missing_values)
        digests.append(_digest(dist))

        if not np.allclose(dist, ref, atol=atol, rtol=rtol, equal_nan=True):
            bad = ~np.isclose(dist, ref, atol=atol, rtol=rtol, equal_nan=True)
            abs_err = float(np.nanmax(np.abs(dist - ref)))
            failures.append(
                f"{name} repeat={i}: mismatch (max_abs_err={abs_err:.6g}, "
                f"n_bad={int(bad.sum())})"
            )

    print(f"{name}: unique_digests={len(set(digests))}/{len(digests)}")
    if stress_workers > 0 and stress_iterations > 0:
        failures.extend(
            _threaded_stress(
                x,
                missing_values,
                stress_workers,
                stress_iterations,
                ref,
                atol,
                rtol,
            )
        )
    if fork_processes > 0 and fork_iterations > 0:
        failures.extend(
            _fork_stress(
                x,
                missing_values,
                fork_processes,
                fork_iterations,
                ref,
                atol,
                rtol,
            )
        )
    return failures


def run(
    repeats: int,
    stress_workers: int,
    stress_iterations: int,
    fork_processes: int,
    fork_iterations: int,
    atol: float,
    rtol: float,
) -> int:
    failures: list[str] = []
    for missing_values in (np.nan, -1.0):
        mv_label = "nan" if np.isnan(missing_values) else "minus1"
        x_simple = _KNN_SIMPLE_EXAMPLE.copy()
        x_weight = _KNN_WEIGHT_DISTANCE.copy()
        if not np.isnan(missing_values):
            x_simple = np.where(np.isnan(_KNN_SIMPLE_EXAMPLE), missing_values, x_simple)
            x_weight = np.where(np.isnan(_KNN_WEIGHT_DISTANCE), missing_values, x_weight)

        failures.extend(
            _check_case(
                f"knn_simple[{mv_label}]",
                x_simple,
                missing_values,
                repeats,
                stress_workers,
                stress_iterations,
                fork_processes,
                fork_iterations,
                atol,
                rtol,
            )
        )
        failures.extend(
            _check_case(
                f"knn_weight_distance[{mv_label}]",
                x_weight,
                missing_values,
                repeats,
                stress_workers,
                stress_iterations,
                fork_processes,
                fork_iterations,
                atol,
                rtol,
            )
        )

    print(f"numpy={np.__version__}")
    print(f"detected_blas={_detected_blas_name() or 'unknown'}")
    print(f"conda_libblas_build={_conda_libblas_build() or 'unknown'}")
    print(f"BLIS_NUM_THREADS={os.getenv('BLIS_NUM_THREADS')}")
    print(f"OPENBLAS_NUM_THREADS={os.getenv('OPENBLAS_NUM_THREADS')}")
    print(f"VECLIB_MAXIMUM_THREADS={os.getenv('VECLIB_MAXIMUM_THREADS')}")

    if failures:
        print("FAIL")
        for failure in failures[:20]:
            print(f"  - {failure}")
        return 1

    print("PASS")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repeats", type=int, default=20)
    parser.add_argument(
        "--stress-workers",
        type=int,
        default=8,
        help="Thread pool size for threaded GEMM stress (0 disables)",
    )
    parser.add_argument(
        "--stress-iterations",
        type=int,
        default=200,
        help="Number of parallel GEMM calls in threaded stress",
    )
    parser.add_argument(
        "--fork-processes",
        type=int,
        default=4,
        help="Process count for fork-based stress (0 disables)",
    )
    parser.add_argument(
        "--fork-iterations",
        type=int,
        default=40,
        help="Iterations per fork stress pool",
    )
    parser.add_argument("--atol", type=float, default=1e-12)
    parser.add_argument("--rtol", type=float, default=1e-12)
    parser.add_argument(
        "--expected-blas",
        choices=["blis", "openblas", "newaccelerate"],
        default=None,
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    detected_blas = _detected_blas_name()
    conda_build = _conda_libblas_build()
    if args.expected_blas is not None and not _backend_matches(
        args.expected_blas, detected_blas, conda_build
    ):
        print(
            f"FAIL: requested BLAS '{args.expected_blas}' but environment reports "
            f"numpy='{detected_blas or 'unknown'}', "
            f"conda_libblas='{conda_build or 'unknown'}'"
        )
        sys.exit(1)
    sys.exit(
        run(
            repeats=args.repeats,
            stress_workers=args.stress_workers,
            stress_iterations=args.stress_iterations,
            fork_processes=args.fork_processes,
            fork_iterations=args.fork_iterations,
            atol=args.atol,
            rtol=args.rtol,
        )
    )
