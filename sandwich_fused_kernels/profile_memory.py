#!/usr/bin/env python3
"""Memory-efficiency comparison for sandwich kernels."""

from __future__ import annotations

import argparse
import gc
import json
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
import psutil

from kernels import (
    sandwich_jax,
    sandwich_numba,
    sandwich_numpy_diag_matmul,
    sandwich_numpy_einsum,
    sandwich_numpy_weighted_gram,
    sandwich_tabmat,
    warmup_jax,
    warmup_numba,
)


BASE_DIR = Path(__file__).resolve().parent
DEFAULT_ARTIFACTS = BASE_DIR / "artifacts"


@dataclass
class MemoryRow:
    kernel: str
    n_rows: int
    n_cols: int
    dtype: str
    peak_rss_mb: float
    theoretical_extra_mb: float
    materializes_diag: bool
    materializes_weighted_x: bool


def _rss_mb() -> float:
    return psutil.Process().memory_info().rss / (1024 * 1024)


def _theoretical_extra_mb(
    n_rows: int,
    n_cols: int,
    dtype: str,
    *,
    materializes_diag: bool,
    materializes_weighted_x: bool,
) -> float:
    b = 4 if dtype == "float32" else 8
    extra = 0
    if materializes_diag:
        extra += n_rows * n_rows * b
    if materializes_weighted_x:
        extra += n_rows * n_cols * b
    return extra / (1024 * 1024)


def _measure(
    name: str,
    fn,
    X: np.ndarray,
    d: np.ndarray,
    *,
    materializes_diag: bool,
    materializes_weighted_x: bool,
) -> MemoryRow:
    gc.collect()
    rss0 = _rss_mb()
    fn(X, d)
    gc.collect()
    rss1 = _rss_mb()
    return MemoryRow(
        kernel=name,
        n_rows=X.shape[0],
        n_cols=X.shape[1],
        dtype=str(X.dtype),
        peak_rss_mb=max(0.0, rss1 - rss0),
        theoretical_extra_mb=_theoretical_extra_mb(
            X.shape[0],
            X.shape[1],
            str(X.dtype),
            materializes_diag=materializes_diag,
            materializes_weighted_x=materializes_weighted_x,
        ),
        materializes_diag=materializes_diag,
        materializes_weighted_x=materializes_weighted_x,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifacts-dir", type=Path, default=DEFAULT_ARTIFACTS)
    parser.add_argument("--n-rows", type=int, default=140_000)
    parser.add_argument("--n-cols", type=int, default=80)
    args = parser.parse_args()

    warmup_numba("blas_tiled")
    warmup_jax("scan_chunked")
    warmup_jax("einsum")

    rng = np.random.default_rng(0)
    for dtype_name in ("float64", "float32"):
        dtype = np.float64 if dtype_name == "float64" else np.float32
        X = np.ascontiguousarray(rng.standard_normal((args.n_rows, args.n_cols), dtype=dtype))
        d = np.ascontiguousarray(rng.random(args.n_rows, dtype=dtype) + 0.1)

        rows = [
            _measure(
                "numpy_diag_matmul",
                sandwich_numpy_diag_matmul,
                X,
                d,
                materializes_diag=True,
                materializes_weighted_x=True,
            ),
            _measure(
                "numpy_weighted_gram",
                sandwich_numpy_weighted_gram,
                X,
                d,
                materializes_diag=False,
                materializes_weighted_x=True,
            ),
            _measure(
                "numpy_einsum",
                sandwich_numpy_einsum,
                X,
                d,
                materializes_diag=False,
                materializes_weighted_x=False,
            ),
            _measure(
                "tabmat",
                sandwich_tabmat,
                X,
                d,
                materializes_diag=False,
                materializes_weighted_x=False,
            ),
            _measure(
                "numba_blas_tiled",
                lambda X, d: sandwich_numba(X, d, variant="blas_tiled"),
                X,
                d,
                materializes_diag=False,
                materializes_weighted_x=True,
            ),
            _measure(
                "jax_scan_chunked",
                lambda X, d: sandwich_jax(X, d, variant="scan_chunked"),
                X,
                d,
                materializes_diag=False,
                materializes_weighted_x=False,
            ),
            _measure(
                "jax_einsum",
                lambda X, d: sandwich_jax(X, d, variant="einsum"),
                X,
                d,
                materializes_diag=False,
                materializes_weighted_x=False,
            ),
        ]

        args.artifacts_dir.mkdir(parents=True, exist_ok=True)
        out = args.artifacts_dir / f"memory_profile_{dtype_name}.json"
        out.write_text(json.dumps([asdict(r) for r in rows], indent=2), encoding="utf-8")
        print(f"Wrote {out}")


if __name__ == "__main__":
    main()
