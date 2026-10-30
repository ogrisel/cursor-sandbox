#!/usr/bin/env python3
"""Profile tabmat vs compiler backends to isolate dominant performance gaps."""

from __future__ import annotations

import argparse
import cProfile
import json
import pstats
import statistics
import time
import tracemalloc
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
import psutil

from kernels import (
    sandwich_jax,
    sandwich_numba,
    sandwich_numpy_einsum,
    sandwich_numpy_weighted_gram,
    sandwich_tabmat,
    warmup_jax,
    warmup_numba,
)


BASE_DIR = Path(__file__).resolve().parent
DEFAULT_ARTIFACTS = BASE_DIR / "artifacts"


@dataclass
class ProfileRow:
    kernel: str
    median_ms: float
    tracemalloc_peak_mb: float
    rss_delta_mb: float
    materializes_weighted_x: bool
    uses_blas_gemm: bool
    uses_fused_k_loop: bool


def _rss_mb() -> float:
    return psutil.Process().memory_info().rss / (1024 * 1024)


def _time_kernel(fn, *, repeats: int = 5, warmup: int = 2) -> tuple[float, float, float]:
    for _ in range(warmup):
        fn()
    timings: list[float] = []
    tracemalloc.start()
    rss0 = _rss_mb()
    for _ in range(repeats):
        t0 = time.perf_counter()
        fn()
        timings.append(time.perf_counter() - t0)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    rss1 = _rss_mb()
    return statistics.median(timings) * 1000, peak / (1024 * 1024), max(0.0, rss1 - rss0)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifacts-dir", type=Path, default=DEFAULT_ARTIFACTS)
    parser.add_argument("--n-rows", type=int, default=50_000)
    parser.add_argument("--n-cols", type=int, default=40)
    args = parser.parse_args()

    warmup_numba("blas_tiled")
    warmup_numba("fused_blocked")
    warmup_jax("einsum")
    warmup_jax("scan_chunked")

    rng = np.random.default_rng(42)
    X = np.ascontiguousarray(rng.standard_normal((args.n_rows, args.n_cols)))
    d = np.ascontiguousarray(rng.random(args.n_rows) + 0.1)

    candidates: list[tuple[str, object, bool, bool, bool]] = [
        ("tabmat", lambda: sandwich_tabmat(X, d), False, False, True),
        ("numpy_einsum", lambda: sandwich_numpy_einsum(X, d), False, False, True),
        ("numpy_weighted_gram", lambda: sandwich_numpy_weighted_gram(X, d), True, True, False),
        ("numba_fused_blocked", lambda: sandwich_numba(X, d, variant="fused_blocked"), False, False, True),
        ("numba_blas_tiled", lambda: sandwich_numba(X, d, variant="blas_tiled"), True, True, False),
        ("jax_einsum", lambda: sandwich_jax(X, d, variant="einsum"), False, False, True),
        ("jax_scan_chunked", lambda: sandwich_jax(X, d, variant="scan_chunked"), False, True, False),
    ]

    rows: list[ProfileRow] = []
    for name, fn, mat_wx, blas, fused_k in candidates:
        med, trace_peak, rss_delta = _time_kernel(fn)
        rows.append(
            ProfileRow(
                kernel=name,
                median_ms=med,
                tracemalloc_peak_mb=trace_peak,
                rss_delta_mb=rss_delta,
                materializes_weighted_x=mat_wx,
                uses_blas_gemm=blas,
                uses_fused_k_loop=fused_k,
            )
        )

    args.artifacts_dir.mkdir(parents=True, exist_ok=True)
    out_json = args.artifacts_dir / "tabmat_advantage_analysis.json"
    out_json.write_text(json.dumps([asdict(r) for r in rows], indent=2), encoding="utf-8")

    tab = next(r for r in rows if r.kernel == "tabmat")
    lines = [
        "# tabmat advantage analysis",
        "",
        f"Problem: {args.n_rows} x {args.n_cols} float64",
        "",
        "| kernel | median (ms) | vs tabmat | trace peak (MB) | weighted-X | BLAS | fused-k |",
        "|---|---:|---:|---:|---|---|---|",
    ]
    for row in sorted(rows, key=lambda r: r.median_ms):
        lines.append(
            f"| {row.kernel} | {row.median_ms:.2f} | {tab.median_ms / row.median_ms:.2f}x | "
            f"{row.tracemalloc_peak_mb:.1f} | {row.materializes_weighted_x} | "
            f"{row.uses_blas_gemm} | {row.uses_fused_k_loop} |"
        )
    lines.extend(
        [
            "",
            "## Interpreted causes",
            "",
            "1. **Fused k-loop without n×m scratch**: tabmat multiplies `d[k]` inside SIMD-blocked micro-kernels.",
            "2. **No BLAS GEMM dispatch overhead**: tabmat calls a specialized sandwich kernel, not generic `dgemm`.",
            "3. **Cache/SIMD blocking**: GotoBLAS-style 4×4 blocks with xsimd on the inner `k` dimension.",
            "4. **Symmetric write pattern**: tabmat accumulates lower-triangle blocks then mirrors.",
            "5. **Memory traffic**: weighted-Gram paths read/write an extra `n×m` buffer (~"
            f"{args.n_rows * args.n_cols * 8 / 2**20:.1f} MB here).",
        ]
    )
    out_md = args.artifacts_dir / "tabmat_advantage_analysis.md"
    out_md.write_text("\n".join(lines), encoding="utf-8")

    profiler = cProfile.Profile()
    profiler.enable()
    sandwich_tabmat(X, d)
    profiler.disable()
    with (args.artifacts_dir / "profile_tabmat_glm_small.txt").open("w", encoding="utf-8") as handle:
        stats = pstats.Stats(profiler, stream=handle)
        stats.sort_stats("cumtime")
        stats.print_stats(30)

    print(f"Wrote {out_json}")
    print(f"Wrote {out_md}")


if __name__ == "__main__":
    main()
