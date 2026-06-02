#!/usr/bin/env python
"""NumPy-only reproducer for suspected BLIS DGEMM issues on macOS arm64."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from typing import Any

import numpy as np


def _pairwise_via_gemm(x: np.ndarray) -> np.ndarray:
    """Squared Euclidean distances via GEMM (sklearn pairwise_distances pattern)."""
    x2 = np.einsum("ij,ij->i", x, x)
    d2 = x2[:, None] - 2.0 * (x @ x.T) + x2[None, :]
    np.maximum(d2, 0.0, out=d2)
    return np.sqrt(d2, out=d2)


def _pairwise_reference(x: np.ndarray) -> np.ndarray:
    diff = x[:, None, :] - x[None, :, :]
    return np.sqrt(np.sum(diff * diff, axis=2))


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
    """Return the conda-forge libblas build string (most reliable backend tag)."""
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


def run(
    seed: int,
    n_samples: int,
    n_features: int,
    repeats: int,
    atol: float,
    rtol: float,
) -> int:
    rng = np.random.default_rng(seed)
    x = rng.standard_normal((n_samples, n_features), dtype=np.float64)
    # Non-trivial memory layout to stress GEMM code paths.
    x = np.asfortranarray(x[:, ::-1])

    ref = _pairwise_reference(x)

    failures: list[str] = []
    digests: list[str] = []
    for i in range(repeats):
        d = _pairwise_via_gemm(x)
        digests.append(_digest(d))

        if not np.isfinite(d).all():
            failures.append(f"repeat={i}: non-finite values detected")
            continue

        if not np.allclose(d, ref, atol=atol, rtol=rtol):
            abs_err = float(np.max(np.abs(d - ref)))
            rel_err = float(np.max(np.abs(d - ref) / np.maximum(np.abs(ref), 1e-15)))
            failures.append(
                f"repeat={i}: mismatch (max_abs_err={abs_err:.6g}, "
                f"max_rel_err={rel_err:.6g})"
            )

    print(f"numpy={np.__version__}")
    print(f"detected_blas={_detected_blas_name() or 'unknown'}")
    print(f"conda_libblas_build={_conda_libblas_build() or 'unknown'}")
    print(f"BLIS_NUM_THREADS={os.getenv('BLIS_NUM_THREADS')}")
    print(f"OPENBLAS_NUM_THREADS={os.getenv('OPENBLAS_NUM_THREADS')}")
    print(f"VECLIB_MAXIMUM_THREADS={os.getenv('VECLIB_MAXIMUM_THREADS')}")
    print(f"unique_result_digests={len(set(digests))}/{len(digests)}")

    if failures:
        print("FAIL")
        for failure in failures[:10]:
            print(f"  - {failure}")
        return 1

    if len(set(digests)) != 1:
        print("FAIL")
        print("  - output changed across repeats")
        return 1

    print("PASS")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=123)
    parser.add_argument("--n-samples", type=int, default=384)
    parser.add_argument("--n-features", type=int, default=192)
    parser.add_argument("--repeats", type=int, default=20)
    parser.add_argument("--atol", type=float, default=1e-6)
    parser.add_argument("--rtol", type=float, default=1e-6)
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
            f"numpy='{detected_blas or 'unknown'}', conda_libblas='{conda_build or 'unknown'}'"
        )
        sys.exit(1)
    sys.exit(
        run(
            seed=args.seed,
            n_samples=args.n_samples,
            n_features=args.n_features,
            repeats=args.repeats,
            atol=args.atol,
            rtol=args.rtol,
        )
    )
