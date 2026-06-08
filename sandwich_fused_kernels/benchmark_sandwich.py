#!/usr/bin/env python3
"""Benchmark sandwich-product kernels on CPU (single- and multi-threaded)."""

from __future__ import annotations

import argparse
import cProfile
import gc
import json
import os
import pstats
import statistics
import time
import tracemalloc
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Callable

import numpy as np
import psutil

from kernels import (
    helion_available,
    sandwich_helion_eager,
    sandwich_jax,
    sandwich_numba,
    sandwich_numpy_diag_matmul,
    sandwich_numpy_einsum,
    sandwich_numpy_weighted_gram,
    sandwich_reference,
    sandwich_tabmat,
    sandwich_torch_compile_einsum,
    sandwich_torch_einsum,
    warmup_helion,
    warmup_jax,
    warmup_numba,
    warmup_torch_compile,
)
from threading_utils import default_multi_thread_count, sandwich_threading

try:
    from kernels.tuned_kernels import (
        sandwich_jax_chunked_tuned,
        sandwich_numba_blas_tuned,
        sandwich_numba_fused_tuned,
        sandwich_numba_jblock_tuned,
        sandwich_xsimd_tuned,
        warmup_tuned,
    )

    _TUNED_AVAILABLE = True
except ImportError:
    _TUNED_AVAILABLE = False


BASE_DIR = Path(__file__).resolve().parent
DEFAULT_ARTIFACTS = BASE_DIR / "artifacts"


@dataclass
class ProblemSpec:
    name: str
    n_rows: int
    n_cols: int
    dtype: str


@dataclass
class KernelResult:
    kernel: str
    problem: str
    threading: str
    num_threads: int
    median_seconds: float
    min_seconds: float
    max_seconds: float
    peak_rss_delta_mb: float
    tracemalloc_peak_mb: float
    max_abs_error: float
    relative_error: float
    extra_alloc_estimate_mb: float
    speedup_vs_numpy_einsum: float
    speedup_vs_tabmat: float


def _make_problem(spec: ProblemSpec, seed: int) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    dtype = np.float32 if spec.dtype == "float32" else np.float64
    X = rng.standard_normal((spec.n_rows, spec.n_cols), dtype=dtype)
    d = rng.random(spec.n_rows, dtype=dtype) + 0.1
    return np.ascontiguousarray(X), np.ascontiguousarray(d)


def _rss_mb() -> float:
    return psutil.Process(os.getpid()).memory_info().rss / (1024 * 1024)


def _measure_kernel(
    fn: Callable[[], np.ndarray],
    reference: np.ndarray,
    *,
    repeats: int,
    warmup: int,
) -> tuple[list[float], float, float, float, float]:
    gc.collect()
    rss_before = _rss_mb()
    tracemalloc.start()
    timings: list[float] = []
    out: np.ndarray | None = None

    for _ in range(warmup):
        out = fn()

    for _ in range(repeats):
        gc.collect()
        t0 = time.perf_counter()
        out = fn()
        timings.append(time.perf_counter() - t0)

    _, peak_trace = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    rss_after = _rss_mb()

    assert out is not None
    diff = np.abs(out - reference)
    denom = np.maximum(np.abs(reference), 1e-12)
    max_abs_error = float(diff.max())
    relative_error = float((diff / denom).max())
    peak_rss_delta = max(0.0, rss_after - rss_before)
    tracemalloc_peak_mb = peak_trace / (1024 * 1024)
    return timings, peak_rss_delta, tracemalloc_peak_mb, max_abs_error, relative_error


def _extra_alloc_estimate_mb(n_rows: int, n_cols: int, dtype: str, kernel: str) -> float:
    bytes_per = 4 if dtype == "float32" else 8
    if kernel in {"numpy_diag_matmul"}:
        return (n_rows * n_rows + n_rows * n_cols) * bytes_per / (1024 * 1024)
    chunk_rows = 4096
    if kernel in {
        "numpy_weighted_gram",
        "jax_weighted_gram",
        "jax_tensordot",
        "numba_blas_fused",
    }:
        return n_rows * n_cols * bytes_per / (1024 * 1024)
    if kernel in {
        "jax_scan_chunked",
        "jax_einsum_chunked",
        "numba_blas_tiled",
        "numba_blas_kchunk_mt",
        "numba_k_chunk_tabmat",
    }:
        return chunk_rows * n_cols * bytes_per / (1024 * 1024)
    if kernel in {"numpy_einsum", "jax_einsum", "helion_eager", "torch_einsum", "torch_compile_einsum"}:
        return n_cols * n_cols * bytes_per / (1024 * 1024)
    if kernel in {"numba_blas_chunked"}:
        return chunk_rows * n_cols * bytes_per / (1024 * 1024) + n_cols * n_cols * bytes_per
    return 0.0


def _xsimd_built() -> bool:
    lib_path = BASE_DIR / "xsimd_ext" / "libsandwich_xsimd.so"
    return lib_path.is_file()


def _tuned_registry(
    *,
    problem: str,
    threading_mode: str,
    num_threads: int,
) -> dict[str, Callable[..., np.ndarray]]:
    if not _TUNED_AVAILABLE:
        return {}
    return {
        "numba_fused_tuned": lambda X, d: sandwich_numba_fused_tuned(
            X, d, problem=problem, threading=threading_mode, num_threads=num_threads
        ),
        "numba_blas_tuned": lambda X, d: sandwich_numba_blas_tuned(
            X, d, problem=problem, threading=threading_mode, num_threads=num_threads
        ),
        "numba_jblock_tuned": lambda X, d: sandwich_numba_jblock_tuned(
            X, d, problem=problem, threading=threading_mode, num_threads=num_threads
        ),
        "jax_chunked_tuned": lambda X, d: sandwich_jax_chunked_tuned(
            X, d, problem=problem, threading=threading_mode, num_threads=num_threads
        ),
        "xsimd_tuned": lambda X, d: sandwich_xsimd_tuned(
            X, d, problem=problem, threading=threading_mode, num_threads=num_threads
        ),
    }


def _kernel_registry(*, include_helion: bool) -> dict[str, Callable[..., np.ndarray]]:
    registry: dict[str, Callable[..., np.ndarray]] = {
        "numpy_einsum": sandwich_numpy_einsum,
        "numpy_weighted_gram": sandwich_numpy_weighted_gram,
        "numpy_diag_matmul": sandwich_numpy_diag_matmul,
        "tabmat": sandwich_tabmat,
        "numba_rival_st": lambda X, d: sandwich_numba(X, d, variant="rival_st"),
        "numba_kouter_st": lambda X, d: sandwich_numba(X, d, variant="kouter_st"),
        "numba_tabmat_style_st": lambda X, d: sandwich_numba(X, d, variant="tabmat_style_st"),
        "numba_rival_mt": lambda X, d: sandwich_numba(X, d, variant="rival_mt"),
        "numba_tabmat_style_mt": lambda X, d: sandwich_numba(X, d, variant="tabmat_style_mt"),
        "numba_kchunk_kouter_mt": lambda X, d: sandwich_numba(X, d, variant="rival_mt"),
        "numba_k_chunk_tabmat": lambda X, d: sandwich_numba(X, d, variant="k_chunk_tabmat"),
        "numba_blas_kchunk_mt": lambda X, d: sandwich_numba(X, d, variant="blas_kchunk_mt"),
        "numba_fused_blocked": lambda X, d: sandwich_numba(X, d, variant="fused_blocked"),
        "numba_blas_fused": lambda X, d: sandwich_numba(X, d, variant="blas_fused"),
        "numba_blas_tiled": lambda X, d: sandwich_numba(X, d, variant="blas_tiled"),
        "jax_einsum": lambda X, d: sandwich_jax(X, d, variant="einsum"),
        "jax_tensordot": lambda X, d: sandwich_jax(X, d, variant="tensordot"),
    }
    if include_helion and helion_available():
        registry.update(
            {
                "helion_eager": sandwich_helion_eager,
                "torch_einsum": sandwich_torch_einsum,
                "torch_compile_einsum": sandwich_torch_compile_einsum,
            }
        )
    return registry


def _blas_threads_for_kernel(kernel_name: str, threading_mode: str, num_threads: int) -> int:
    """Chunked BLAS kernels use single-thread GEMM inside each prange worker."""
    if threading_mode == "multi" and kernel_name in {
        "numba_blas_kchunk_mt",
        "numba_blas_tiled",
        "numba_blas_chunked",
        "numba_blas_tuned",
    }:
        return 1
    return num_threads


def _helion_kernels() -> list[str]:
    if not helion_available():
        return []
    return ["helion_eager", "torch_einsum", "torch_compile_einsum"]


def _kernels_for_threading(
    threading_mode: str,
    *,
    include_helion: bool,
    include_tuned: bool,
) -> list[str]:
    """Pick kernel variants appropriate for each threading regime."""
    common = [
        "numpy_einsum",
        "numpy_weighted_gram",
        "tabmat",
        "numba_blas_fused",
        "jax_einsum",
    ]
    if include_helion:
        common.extend(_helion_kernels())
    if threading_mode == "single":
        kernels = common + [
            "numba_rival_st",
            "numba_tabmat_style_st",
            "numba_k_chunk_tabmat",
        ]
    else:
        kernels = common + [
            "numba_rival_mt",
            "numba_blas_kchunk_mt",
            "numba_tabmat_style_mt",
            "numba_k_chunk_tabmat",
            "numba_blas_tiled",
            "numba_fused_blocked",
        ]
    if include_tuned and _TUNED_AVAILABLE:
        if threading_mode == "multi":
            kernels.extend(
                [
                    "numba_fused_tuned",
                    "numba_blas_tuned",
                    "numba_jblock_tuned",
                    "jax_chunked_tuned",
                ]
            )
            if _xsimd_built():
                kernels.append("xsimd_tuned")
        else:
            kernels.extend(["numba_fused_tuned", "numba_jblock_tuned", "jax_chunked_tuned"])
    return kernels


def _default_problems() -> list[ProblemSpec]:
    return [
        ProblemSpec("glm_small", 50_000, 40, "float64"),
        ProblemSpec("glm_medium", 140_000, 80, "float64"),
        ProblemSpec("glm_tall_skinny", 320_000, 32, "float64"),
        ProblemSpec("glm_square_cols", 80_000, 120, "float64"),
        ProblemSpec("glm_small_f32", 50_000, 40, "float32"),
    ]


def run_benchmarks(
    *,
    problems: list[ProblemSpec],
    kernels: list[str],
    threading_mode: str,
    num_threads: int,
    repeats: int,
    warmup: int,
    seed: int,
    include_helion: bool,
    include_tuned: bool,
) -> list[KernelResult]:
    registry = _kernel_registry(include_helion=include_helion)
    for variant in (
        "rival_st",
        "tabmat_style_st",
        "rival_mt",
        "blas_kchunk_mt",
        "tabmat_style_mt",
        "k_chunk_tabmat",
        "fused_blocked",
        "blas_tiled",
        "blas_fused",
    ):
        warmup_numba(variant)
    for variant in ("einsum", "tensordot"):
        warmup_jax(variant)
    if include_helion and helion_available():
        warmup_helion("eager")
        warmup_torch_compile()

    if include_tuned and _TUNED_AVAILABLE:
        warmup_tuned(num_threads=num_threads)

    results: list[KernelResult] = []
    baseline_times: dict[str, float] = {}
    tabmat_times: dict[str, float] = {}

    for spec in problems:
        X, d = _make_problem(spec, seed)
        reference = sandwich_reference(X, d)

        for kernel_name in kernels:
            if kernel_name == "xsimd_tuned" and spec.dtype != "float64":
                continue
            if kernel_name.endswith("_tuned"):
                fn = _tuned_registry(
                    problem=spec.name,
                    threading_mode=threading_mode,
                    num_threads=num_threads,
                ).get(kernel_name)
                if fn is None:
                    continue
            else:
                fn = registry[kernel_name]
            blas_threads = _blas_threads_for_kernel(kernel_name, threading_mode, num_threads)
            with sandwich_threading(num_threads, blas_threads=blas_threads):
                timings, rss_delta, trace_peak, max_err, rel_err = _measure_kernel(
                    lambda X=X, d=d, fn=fn: fn(X, d),
                    reference,
                    repeats=repeats,
                    warmup=warmup,
                )
            median = statistics.median(timings)
            results.append(
                KernelResult(
                    kernel=kernel_name,
                    problem=spec.name,
                    threading=threading_mode,
                    num_threads=num_threads,
                    median_seconds=median,
                    min_seconds=min(timings),
                    max_seconds=max(timings),
                    peak_rss_delta_mb=rss_delta,
                    tracemalloc_peak_mb=trace_peak,
                    max_abs_error=max_err,
                    relative_error=rel_err,
                    extra_alloc_estimate_mb=_extra_alloc_estimate_mb(
                        spec.n_rows, spec.n_cols, spec.dtype, kernel_name
                    ),
                    speedup_vs_numpy_einsum=0.0,
                    speedup_vs_tabmat=0.0,
                )
            )
            if kernel_name == "numpy_einsum":
                baseline_times[spec.name] = median
            if kernel_name == "tabmat":
                tabmat_times[spec.name] = median

        for row in results:
            if row.problem != spec.name or row.threading != threading_mode:
                continue
            base = baseline_times.get(spec.name)
            tab = tabmat_times.get(spec.name)
            if base:
                row.speedup_vs_numpy_einsum = base / row.median_seconds
            if tab:
                row.speedup_vs_tabmat = tab / row.median_seconds

    return results


def _write_markdown_report(results: list[KernelResult], path: Path, title: str) -> None:
    by_problem: dict[str, list[KernelResult]] = {}
    for row in results:
        by_problem.setdefault(row.problem, []).append(row)

    lines = [f"# {title}", ""]
    if results:
        lines.append(f"Threading: **{results[0].threading}** ({results[0].num_threads} threads)")
        lines.append("")

    for problem, rows in by_problem.items():
        rows_sorted = sorted(rows, key=lambda r: r.median_seconds)
        lines.append(f"## {problem}")
        lines.append("")
        lines.append(
            "| kernel | median (ms) | vs numpy_einsum | vs tabmat | peak RSS Δ (MB) | max rel err |"
        )
        lines.append("|---|---:|---:|---:|---:|---:|")
        for row in rows_sorted:
            lines.append(
                f"| {row.kernel} | {row.median_seconds * 1000:.2f} | "
                f"{row.speedup_vs_numpy_einsum:.2f}x | {row.speedup_vs_tabmat:.2f}x | "
                f"{row.peak_rss_delta_mb:.2f} | {row.relative_error:.2e} |"
            )
        best = rows_sorted[0]
        tab = next((r for r in rows if r.kernel == "tabmat"), None)
        lines.append("")
        if tab:
            lines.append(
                f"Best: **{best.kernel}** ({best.median_seconds * 1000:.2f} ms). "
                f"tabmat: {tab.median_seconds * 1000:.2f} ms "
                f"({tab.median_seconds / best.median_seconds:.2f}x vs best)."
            )
        lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")


def profile_kernel(
    kernel_name: str,
    spec: ProblemSpec,
    *,
    seed: int,
    out_path: Path,
    num_threads: int,
) -> None:
    registry = _kernel_registry(include_helion=helion_available())
    X, d = _make_problem(spec, seed)
    fn = registry[kernel_name]

    if kernel_name.startswith("numba"):
        variant = kernel_name.removeprefix("numba_")
        if variant.endswith("_st"):
            variant = variant.replace("_st", "_st")
        warmup_numba(variant.replace("tabmat_style_mt", "tabmat_style_mt").replace("tabmat_style_st", "tabmat_style_st"))
    if kernel_name.startswith("jax"):
        warmup_jax("einsum")

    with sandwich_threading(num_threads):
        profiler = cProfile.Profile()
        profiler.enable()
        fn(X, d)
        profiler.disable()

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as handle:
        stats = pstats.Stats(profiler, stream=handle)
        stats.sort_stats("cumtime")
        stats.print_stats(40)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifacts-dir", type=Path, default=DEFAULT_ARTIFACTS)
    parser.add_argument("--repeats", type=int, default=5)
    parser.add_argument("--warmup", type=int, default=2)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--profile-kernel", type=str, default="numba_tabmat_style_mt")
    parser.add_argument("--profile-problem", type=str, default="glm_medium")
    parser.add_argument(
        "--include-helion",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Include Helion/PyTorch kernels when torch+helion are installed (default: true)",
    )
    parser.add_argument(
        "--include-tuned",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Include autotuned kernel variants when cache exists (default: true)",
    )
    args = parser.parse_args()

    include_helion = args.include_helion and helion_available()
    if args.include_helion and not include_helion:
        print(
            "Warning: --include-helion set but helion/torch not installed; "
            "install with: pip install torch helion packaging setuptools",
            flush=True,
        )

    problems = _default_problems()
    mt_threads = default_multi_thread_count()

    all_results: list[KernelResult] = []
    for threading_mode, num_threads in (("single", 1), ("multi", mt_threads)):
        kernels = _kernels_for_threading(
            threading_mode,
            include_helion=include_helion,
            include_tuned=args.include_tuned,
        )
        all_results.extend(
            run_benchmarks(
                problems=problems,
                kernels=kernels,
                threading_mode=threading_mode,
                num_threads=num_threads,
                repeats=args.repeats,
                warmup=args.warmup,
                seed=args.seed,
                include_helion=include_helion,
                include_tuned=args.include_tuned,
            )
        )

    args.artifacts_dir.mkdir(parents=True, exist_ok=True)
    json_path = args.artifacts_dir / "benchmark_results.json"
    json_path.write_text(
        json.dumps([asdict(r) for r in all_results], indent=2),
        encoding="utf-8",
    )

    single = [r for r in all_results if r.threading == "single"]
    multi = [r for r in all_results if r.threading == "multi"]
    _write_markdown_report(
        single,
        args.artifacts_dir / "benchmark_report_single_thread.md",
        "Sandwich benchmark report (single-threaded)",
    )
    _write_markdown_report(
        multi,
        args.artifacts_dir / "benchmark_report_multi_thread.md",
        "Sandwich benchmark report (multi-threaded)",
    )
    _write_markdown_report(
        all_results,
        args.artifacts_dir / "benchmark_report.md",
        "Sandwich benchmark report (single + multi threaded)",
    )

    profile_spec = next(p for p in problems if p.name == args.profile_problem)
    profile_kernel(
        args.profile_kernel,
        profile_spec,
        seed=args.seed,
        out_path=args.artifacts_dir / f"profile_{args.profile_kernel}_{args.profile_problem}.txt",
        num_threads=mt_threads,
    )

    best_single = min(single, key=lambda r: r.median_seconds)
    best_multi = min(multi, key=lambda r: r.median_seconds)
    print(
        json.dumps(
            {
                "results_path": str(json_path),
                "single_thread_best": {
                    "kernel": best_single.kernel,
                    "problem": best_single.problem,
                    "median_ms": best_single.median_seconds * 1000,
                    "vs_tabmat": best_single.speedup_vs_tabmat,
                },
                "multi_thread_best": {
                    "kernel": best_multi.kernel,
                    "problem": best_multi.problem,
                    "median_ms": best_multi.median_seconds * 1000,
                    "vs_tabmat": best_multi.speedup_vs_tabmat,
                },
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
