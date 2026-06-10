#!/usr/bin/env python3
"""Autotune chunk/tile sizes for sandwich kernels to maximize MT throughput."""

from __future__ import annotations

import argparse
import gc
import json
import statistics
import sys
import time
from dataclasses import asdict
from pathlib import Path
from typing import Any, Callable, Iterator

import numpy as np

BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from autotune_config import (
    AutotuneCache,
    DEFAULT_CACHE_PATH,
    TuneParams,
    TuneResult,
    block_candidates,
    chunk_count_candidates,
    helion_row_tile_candidates,
    helion_tile_candidates,
    jax_chunk_candidates,
    triton_block_k_candidates,
    triton_block_m_candidates,
    triton_n_chunk_candidates,
    triton_row_chunk_candidates,
    xsimd_block_candidates,
    xsimd_chunk_factor_candidates,
)
from benchmark_sandwich import ProblemSpec, _default_problems, _make_problem
from kernels import sandwich_reference, sandwich_tabmat, warmup_numba
from kernels.tuned_kernels import reload_autotune_cache, warmup_tuned
from threading_utils import default_multi_thread_count, sandwich_threading


DEFAULT_ARTIFACTS = BASE_DIR / "artifacts"

TUNABLE_FAMILIES = (
    "numba_fused_mt",
    "numba_blas_mt",
    "numba_jblock_mt",
    "jax_chunked",
    "xsimd_mt",
    "helion_tiled",
    "torch_tiled",
    "triton_cpu_mt",
    "torch_compile_triton_mt",
)


def _helion_available() -> bool:
    try:
        from kernels.helion_baseline import helion_available

        return helion_available()
    except ImportError:
        return False


def _torch_available() -> bool:
    try:
        import torch  # noqa: F401

        return True
    except ImportError:
        return False


def _triton_cpu_available() -> bool:
    try:
        from kernels.triton_cpu_kernel import triton_cpu_available

        return triton_cpu_available()
    except ImportError:
        return False


def _time_kernel(
    fn: Callable[[], np.ndarray],
    reference: np.ndarray,
    *,
    warmup: int,
    repeats: int,
) -> tuple[float, float]:
    gc.collect()
    for _ in range(warmup):
        out = fn()
    timings: list[float] = []
    max_rel = 0.0
    for _ in range(repeats):
        gc.collect()
        t0 = time.perf_counter()
        out = fn()
        timings.append(time.perf_counter() - t0)
        diff = np.abs(out - reference)
        denom = np.maximum(np.abs(reference), 1e-12)
        max_rel = max(max_rel, float((diff / denom).max()))
    return statistics.median(timings), max_rel


def _iter_numba_fused_params(n_rows: int, n_cols: int, num_threads: int) -> Iterator[TuneParams]:
    for block in block_candidates(n_cols):
        for n_chunks in chunk_count_candidates(n_rows, num_threads):
            yield TuneParams(block=block, n_chunks=n_chunks)


def _iter_numba_blas_params(n_rows: int, num_threads: int) -> Iterator[TuneParams]:
    for n_chunks in chunk_count_candidates(n_rows, num_threads):
        yield TuneParams(n_chunks=n_chunks)


def _iter_numba_jblock_params(n_cols: int) -> Iterator[TuneParams]:
    for block in block_candidates(n_cols):
        yield TuneParams(block=block)


def _iter_jax_params(n_rows: int, num_threads: int) -> Iterator[TuneParams]:
    for chunk in jax_chunk_candidates(n_rows, num_threads):
        yield TuneParams(jax_chunk=chunk)


def _iter_xsimd_params(n_cols: int, num_threads: int) -> Iterator[TuneParams]:
    for block in xsimd_block_candidates(n_cols):
        for chunk_factor in xsimd_chunk_factor_candidates():
            yield TuneParams(xsimd_block=block, xsimd_chunk_factor=chunk_factor)


def _iter_helion_tile_params(n_rows: int, n_cols: int, *, symmetric: bool = True) -> Iterator[TuneParams]:
    tiles = helion_tile_candidates(n_cols)
    row_tiles = helion_row_tile_candidates(n_rows)
    for tile_m in tiles:
        tile_ns = [tile_m] if symmetric else tiles
        for tile_n in tile_ns:
            for tile_k in row_tiles:
                yield TuneParams(tile_m=tile_m, tile_n=tile_n, tile_k=tile_k)


def _iter_torch_compile_triton_params(n_rows: int, n_cols: int) -> Iterator[TuneParams]:
    """Smaller tile grid than generic Helion search (each point triggers Inductor compile)."""
    del n_cols
    tiles = [8, 16, 32]
    row_tiles = [k for k in (4096, 8192, 16384, 32768) if k <= n_rows] or [4096]
    for tile_m in tiles:
        for tile_k in row_tiles:
            yield TuneParams(tile_m=tile_m, tile_n=tile_m, tile_k=tile_k)


def _iter_triton_cpu_params(n_rows: int, n_cols: int, num_threads: int) -> Iterator[TuneParams]:
    if num_threads <= 1:
        chunks = [c for c in (512, 1024, 2048, 4096, 8192) if c <= n_rows]
        n_chunks_list = [1]
        block_ks = [64, 128]
    else:
        chunks = [c for c in (2048, 4096, 8192, 16384) if c <= n_rows] or [4096]
        n_chunks_list = [num_threads * m for m in (1, 2, 4)]
        block_ks = [64, 128, 256]
    for chunk in chunks:
        for block_m in triton_block_m_candidates(n_cols):
            for block_k in block_ks:
                for n_chunks in n_chunks_list:
                    yield TuneParams(
                        triton_chunk=chunk,
                        triton_block_m=block_m,
                        triton_block_k=block_k,
                        triton_n_chunks=n_chunks,
                    )


def _param_grid(
    family: str,
    *,
    n_rows: int,
    n_cols: int,
    num_threads: int,
    quick: bool,
) -> list[TuneParams]:
    if family == "numba_fused_mt":
        params = list(_iter_numba_fused_params(n_rows, n_cols, num_threads))
    elif family == "numba_blas_mt":
        params = list(_iter_numba_blas_params(n_rows, num_threads))
    elif family == "numba_jblock_mt":
        params = list(_iter_numba_jblock_params(n_cols))
    elif family == "jax_chunked":
        params = list(_iter_jax_params(n_rows, num_threads))
    elif family == "xsimd_mt":
        params = list(_iter_xsimd_params(n_cols, num_threads))
    elif family in {"helion_tiled", "torch_tiled"}:
        params = list(_iter_helion_tile_params(n_rows, n_cols))
    elif family == "torch_compile_triton_mt":
        params = list(_iter_torch_compile_triton_params(n_rows, n_cols))
    elif family == "triton_cpu_mt":
        params = list(_iter_triton_cpu_params(n_rows, n_cols, num_threads))
    else:
        raise ValueError(f"unknown family: {family}")

    if quick:
        if family == "numba_fused_mt":
            return [TuneParams(block=4, n_chunks=num_threads * 4), TuneParams(block=8, n_chunks=num_threads * 8)]
        if family == "numba_blas_mt":
            return [TuneParams(n_chunks=num_threads * 2), TuneParams(n_chunks=num_threads * 8)]
        if family == "numba_jblock_mt":
            return [TuneParams(block=4), TuneParams(block=8)]
        if family == "jax_chunked":
            return [TuneParams(jax_chunk=2048), TuneParams(jax_chunk=8192)]
        if family == "xsimd_mt":
            return [
                TuneParams(xsimd_block=4, xsimd_chunk_factor=4),
                TuneParams(xsimd_block=8, xsimd_chunk_factor=8),
            ]
        if family in {"helion_tiled", "torch_tiled", "torch_compile_triton_mt"}:
            return [
                TuneParams(tile_m=4, tile_n=4, tile_k=512),
                TuneParams(tile_m=8, tile_n=8, tile_k=4096),
                TuneParams(tile_m=16, tile_n=16, tile_k=8192),
                TuneParams(tile_m=32, tile_n=32, tile_k=16384),
            ]
        if family == "triton_cpu_mt":
            return [
                TuneParams(triton_chunk=4096, triton_block_m=8, triton_block_k=64, triton_n_chunks=num_threads),
                TuneParams(triton_chunk=4096, triton_block_m=8, triton_block_k=64, triton_n_chunks=num_threads * 2),
                TuneParams(triton_chunk=4096, triton_block_m=8, triton_block_k=128, triton_n_chunks=num_threads * 2),
                TuneParams(triton_chunk=8192, triton_block_m=16, triton_block_k=64, triton_n_chunks=num_threads * 2),
            ]
    return params


def _run_with_params(
    family: str,
    X: np.ndarray,
    d: np.ndarray,
    params: TuneParams,
    *,
    problem: str,
    threading: str,
    num_threads: int,
) -> np.ndarray:
    if family == "numba_fused_mt":
        from kernels import numba_kernels as nk

        if num_threads <= 1:
            out = np.zeros((X.shape[1], X.shape[1]), dtype=X.dtype)
            nk._accumulate_tabmat_blocks(X, d, out, params.block)
            return out
        return nk._sandwich_kchunk_fused_impl(X, d, params.n_chunks, params.block)
    if family == "numba_blas_mt":
        from kernels import numba_kernels as nk

        if num_threads <= 1:
            return nk.sandwich_numba_blas_fused(X, d)
        return nk._sandwich_kchunk_blas_impl(X, d, params.n_chunks)
    if family == "numba_jblock_mt":
        from kernels import numba_kernels as nk

        return nk._tabmat_style_mt_impl(X, d, params.block)
    if family == "jax_chunked":
        from kernels.jax_kernels import sandwich_jax_chunked

        return sandwich_jax_chunked(X, d, chunk=params.jax_chunk)
    if family == "xsimd_mt":
        from kernels import xsimd_kernel as xk

        return xk.sandwich_xsimd(
            X,
            d,
            num_threads=num_threads,
            block=params.xsimd_block,
            chunk_factor=params.xsimd_chunk_factor,
        )
    if family == "helion_tiled":
        from kernels import helion_baseline as hb

        return hb.sandwich_helion_tiled(
            X, d, tile_m=params.tile_m, tile_n=params.tile_n, tile_k=params.tile_k
        )
    if family == "torch_tiled":
        from kernels import helion_baseline as hb

        return hb.sandwich_torch_tiled(
            X, d, tile_m=params.tile_m, tile_n=params.tile_n, tile_k=params.tile_k
        )
    if family == "triton_cpu_mt":
        from kernels.triton_cpu_kernel import sandwich_triton_cpu_native

        return sandwich_triton_cpu_native(
            X,
            d,
            chunk=params.triton_chunk,
            block_m=params.triton_block_m,
            block_k=params.triton_block_k,
            n_chunks=params.triton_n_chunks,
            num_threads=num_threads,
        )
    if family == "torch_compile_triton_mt":
        from kernels.triton_cpu_kernel import sandwich_torch_compile_triton_tiled

        return sandwich_torch_compile_triton_tiled(
            X,
            d,
            tile_m=params.tile_m,
            tile_n=params.tile_n,
            tile_k=params.tile_k,
            num_threads=num_threads,
        )
    raise ValueError(f"unknown family: {family}")


def _blas_threads_for_family(family: str, threading: str, num_threads: int) -> int:
    if threading == "multi" and family == "numba_blas_mt":
        return 1
    return num_threads


def _warmup_family(family: str, num_threads: int) -> None:
    if family.startswith("numba"):
        warmup_numba("blas_kchunk_mt")
        warmup_numba("tabmat_style_mt")
    if family == "jax_chunked":
        from kernels.jax_kernels import sandwich_jax_chunked

        rng = np.random.default_rng(0)
        X = rng.standard_normal((256, 16))
        d = rng.random(256) + 0.1
        sandwich_jax_chunked(X, d, chunk=4096)
    if family == "xsimd_mt":
        from kernels.xsimd_kernel import warmup_xsimd

        warmup_xsimd(num_threads=num_threads)
    if family == "helion_tiled":
        from kernels import helion_kernel

        helion_kernel.warmup_helion("tiled")
    if family in {"torch_tiled", "torch_compile_tiled"}:
        from kernels import helion_kernel

        helion_kernel.warmup_torch_tiled()
    if family == "triton_cpu_mt":
        from kernels.triton_cpu_kernel import warmup_triton_cpu_native

        warmup_triton_cpu_native(num_threads=num_threads)
    if family == "torch_compile_triton_mt":
        from kernels.triton_cpu_kernel import warmup_torch_compile_triton_tiled

        warmup_torch_compile_triton_tiled(num_threads=num_threads)


def tune_family(
    family: str,
    spec: ProblemSpec,
    *,
    threading: str,
    num_threads: int,
    seed: int,
    warmup: int,
    repeats: int,
    quick: bool,
    tabmat_seconds: float | None = None,
) -> TuneResult:
    X, d = _make_problem(spec, seed)
    reference = sandwich_reference(X, d)
    _warmup_family(family, num_threads)

    best_params = TuneParams()
    best_time = float("inf")
    best_rel = 0.0
    blas_threads = _blas_threads_for_family(family, threading, num_threads)

    for params in _param_grid(
        family,
        n_rows=spec.n_rows,
        n_cols=spec.n_cols,
        num_threads=num_threads,
        quick=quick,
    ):
        with sandwich_threading(num_threads, blas_threads=blas_threads):
            try:
                _run_with_params(
                    family,
                    X,
                    d,
                    params,
                    problem=spec.name,
                    threading=threading,
                    num_threads=num_threads,
                )
                median, rel = _time_kernel(
                    lambda p=params: _run_with_params(
                        family,
                        X,
                        d,
                        p,
                        problem=spec.name,
                        threading=threading,
                        num_threads=num_threads,
                    ),
                    reference,
                    warmup=warmup,
                    repeats=repeats,
                )
            except FileNotFoundError:
                raise
            except Exception as exc:  # noqa: BLE001
                print(f"  skip {family} {params.to_dict()}: {exc}", flush=True)
                continue

        if median < best_time:
            best_time = median
            best_params = params
            best_rel = rel

    if best_time == float("inf"):
        raise RuntimeError(f"no valid parameter grid point for {family} on {spec.name}")

    vs_tabmat = tabmat_seconds / best_time if tabmat_seconds else 0.0
    return TuneResult(
        family=family,
        problem=spec.name,
        threading=threading,
        num_threads=num_threads,
        params=best_params,
        median_seconds=best_time,
        vs_tabmat=vs_tabmat,
        max_rel_error=best_rel,
    )


def run_autotune(
    *,
    problems: list[ProblemSpec],
    families: list[str],
    threading: str,
    num_threads: int,
    seed: int,
    warmup: int,
    repeats: int,
    quick: bool,
    cache_path: Path,
) -> tuple[list[TuneResult], AutotuneCache]:
    cache = AutotuneCache.load(cache_path)
    results: list[TuneResult] = []

    for spec in problems:
        X, d = _make_problem(spec, seed)
        with sandwich_threading(num_threads):
            tabmat_seconds, _ = _time_kernel(
                lambda: sandwich_tabmat(X, d),
                sandwich_reference(X, d),
                warmup=warmup,
                repeats=repeats,
            )
        print(
            f"\n{spec.name} ({threading}, {num_threads} threads) tabmat baseline: "
            f"{tabmat_seconds * 1000:.2f} ms",
            flush=True,
        )

        for family in families:
            if family == "xsimd_mt" and spec.dtype != "float64":
                print(f"  skip {family}: float64 only", flush=True)
                continue
            if family == "helion_tiled" and not _helion_available():
                print(f"  skip {family}: helion/torch not installed", flush=True)
                continue
            if family in {"torch_tiled", "torch_compile_tiled"} and not _torch_available():
                print(f"  skip {family}: torch not installed", flush=True)
                continue
            if family in {"triton_cpu_mt", "torch_compile_triton_mt"} and not _triton_cpu_available():
                print(f"  skip {family}: triton-cpu not installed", flush=True)
                continue
            print(f"  tuning {family}...", flush=True)
            try:
                row = tune_family(
                    family,
                    spec,
                    threading=threading,
                    num_threads=num_threads,
                    seed=seed,
                    warmup=warmup,
                    repeats=repeats,
                    quick=quick,
                    tabmat_seconds=tabmat_seconds,
                )
            except FileNotFoundError as exc:
                print(f"  skip {family}: {exc}", flush=True)
                continue
            except RuntimeError as exc:
                print(f"  skip {family}: {exc}", flush=True)
                continue

            cache.set(spec.name, threading, num_threads, family, row.params)
            if family == "torch_tiled":
                cache.set(spec.name, threading, num_threads, "torch_compile_tiled", row.params)
            if family == "torch_compile_triton_mt":
                cache.set(spec.name, threading, num_threads, "torch_compile_triton_tuned", row.params)
            cache.save(cache_path)
            results.append(row)
            print(
                f"    best {row.params.to_dict()} -> {row.median_seconds * 1000:.2f} ms "
                f"({row.vs_tabmat:.2f}x tabmat, rel err {row.max_rel_error:.2e})",
                flush=True,
            )

    cache.save(cache_path)
    reload_autotune_cache(cache_path)
    return results, cache


def _write_report(results: list[TuneResult], path: Path) -> None:
    lines = ["# Autotune report", ""]
    if not results:
        lines.append("No results.")
        path.write_text("\n".join(lines), encoding="utf-8")
        return

    lines.append(f"Threading: **{results[0].threading}** ({results[0].num_threads} threads)")
    lines.append("")
    lines.append("| problem | family | params | median (ms) | vs tabmat | max rel err |")
    lines.append("|---|---|---|---:|---:|---:|")
    for row in sorted(results, key=lambda r: (r.problem, r.family)):
        lines.append(
            f"| {row.problem} | {row.family} | `{json.dumps(row.params.to_dict())}` | "
            f"{row.median_seconds * 1000:.2f} | {row.vs_tabmat:.2f}x | {row.max_rel_error:.2e} |"
        )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifacts-dir", type=Path, default=DEFAULT_ARTIFACTS)
    parser.add_argument("--cache-path", type=Path, default=DEFAULT_CACHE_PATH)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--warmup", type=int, default=1)
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--quick", action="store_true", help="Search a reduced parameter grid")
    parser.add_argument(
        "--problems",
        nargs="*",
        default=None,
        help="Problem names to tune (default: all benchmark problems)",
    )
    parser.add_argument(
        "--families",
        nargs="*",
        default=list(TUNABLE_FAMILIES),
        choices=TUNABLE_FAMILIES,
        help="Kernel families to autotune",
    )
    parser.add_argument(
        "--threading",
        choices=("single", "multi", "both"),
        default="multi",
        help="Threading regime to tune (default: multi)",
    )
    parser.add_argument("--num-threads", type=int, default=None, help="Override thread count for multi")
    args = parser.parse_args()

    all_problems = _default_problems()
    if args.problems:
        names = set(args.problems)
        problems = [p for p in all_problems if p.name in names]
        missing = names - {p.name for p in problems}
        if missing:
            raise SystemExit(f"Unknown problems: {sorted(missing)}")
    else:
        problems = all_problems if not args.quick else [all_problems[0]]

    mt_threads = args.num_threads or default_multi_thread_count()
    regimes: list[tuple[str, int]] = []
    if args.threading in ("single", "both"):
        regimes.append(("single", 1))
    if args.threading in ("multi", "both"):
        regimes.append(("multi", mt_threads))

    all_results: list[TuneResult] = []
    for threading, num_threads in regimes:
        results, _ = run_autotune(
            problems=problems,
            families=list(args.families),
            threading=threading,
            num_threads=num_threads,
            seed=args.seed,
            warmup=args.warmup,
            repeats=args.repeats,
            quick=args.quick,
            cache_path=args.cache_path,
        )
        all_results.extend(results)

    args.artifacts_dir.mkdir(parents=True, exist_ok=True)
    report_path = args.artifacts_dir / "autotune_report.md"
    _write_report(all_results, report_path)
    json_path = args.artifacts_dir / "autotune_results.json"
    json_path.write_text(
        json.dumps([asdict(r) for r in all_results], indent=2, default=str),
        encoding="utf-8",
    )

    warmup_tuned(num_threads=mt_threads)
    print(
        json.dumps(
            {
                "cache_path": str(args.cache_path),
                "report_path": str(report_path),
                "results_path": str(json_path),
                "best_vs_tabmat": max((r.vs_tabmat for r in all_results), default=0.0),
            },
            indent=2,
        ),
        flush=True,
    )


if __name__ == "__main__":
    main()
