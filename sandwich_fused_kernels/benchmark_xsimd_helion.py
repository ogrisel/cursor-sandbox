#!/usr/bin/env python3
"""Benchmark xsimd and Helion/torch.compile sandwich paths."""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import statistics
import sys
import time
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np

BASE_DIR = Path(__file__).resolve().parent


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


@dataclass
class BenchRow:
    kernel: str
    threading: str
    num_threads: int
    median_ms: float
    vs_tabmat: float
    max_rel_err: float
    notes: str = ""


def _median_timings(fn, repeats: int, warmup: int) -> float:
    for _ in range(warmup):
        fn()
    timings = []
    for _ in range(repeats):
        t0 = time.perf_counter()
        fn()
        timings.append(time.perf_counter() - t0)
    return statistics.median(timings) * 1000


def benchmark_numpy_xsimd(
    X: np.ndarray,
    d: np.ndarray,
    reference: np.ndarray,
    *,
    repeats: int,
    warmup: int,
) -> list[BenchRow]:
    ref_mod = _load_module("reference", BASE_DIR / "kernels/reference.py")
    xsimd_mod = _load_module("xsimd_kernel", BASE_DIR / "kernels/xsimd_kernel.py")
    tabmat = __import__("tabmat").DenseMatrix

    rows = np.arange(X.shape[0], dtype=np.int64)
    cols = np.arange(X.shape[1], dtype=np.int64)

    def tabmat_fn(num_threads: int):
        os.environ["OMP_NUM_THREADS"] = str(num_threads)
        return tabmat(X).sandwich(d, rows, cols)

    out_rows: list[BenchRow] = []
    tab_times: dict[str, float] = {}

    for threading, nt in (("single", 1), ("multi", os.cpu_count() or 4)):
        tab_ms = _median_timings(lambda nt=nt: tabmat_fn(nt), repeats, warmup)
        tab_times[threading] = tab_ms
        out_rows.append(
            BenchRow("tabmat", threading, nt, tab_ms, 1.0, 0.0, "reference native xsimd in tabmat")
        )

        for label, threads in [
            ("xsimd_ext", nt),
        ]:
            def run_xsimd(num_threads=threads):
                return xsimd_mod.sandwich_xsimd(X, d, num_threads=num_threads)

            out = run_xsimd()
            err = float(np.max(np.abs(out - reference) / np.maximum(np.abs(reference), 1e-12)))
            med = _median_timings(run_xsimd, repeats, warmup)
            out_rows.append(
                BenchRow(
                    label,
                    threading,
                    threads,
                    med,
                    tab_times[threading] / med,
                    err,
                    f"xsimd batch width={xsimd_mod.xsimd_batch_width()}",
                )
            )

    return out_rows


def benchmark_helion_torch(
    X: np.ndarray,
    d: np.ndarray,
    reference: np.ndarray,
    *,
    repeats: int,
    warmup: int,
) -> list[BenchRow]:
    try:
        import torch
    except ImportError:
        return [
            BenchRow(
                "helion/torch",
                "n/a",
                0,
                0.0,
                0.0,
                0.0,
                "torch not installed",
            )
        ]

    helion_mod = _load_module("helion_kernel", BASE_DIR / "kernels/helion_kernel.py")
    Xt = torch.as_tensor(X, dtype=torch.float64)
    dt = torch.as_tensor(d, dtype=torch.float64)
    ref_t = torch.as_tensor(reference, dtype=torch.float64)

    out_rows: list[BenchRow] = []

    eager_ms = _median_timings(
        lambda: helion_mod.sandwich_torch_einsum(Xt, dt),
        repeats,
        warmup,
    )
    out = helion_mod.sandwich_torch_einsum(Xt, dt)
    err = float((out - ref_t).abs().max().item() / ref_t.abs().clamp_min(1e-12).max().item())
    out_rows.append(
        BenchRow("torch_einsum", "single", 1, eager_ms, 0.0, err, "eager PyTorch")
    )

    helion_mod.warmup_torch_compile()
    for label, fn in [
        ("torch_compile_einsum", helion_mod.sandwich_torch_compile_einsum),
        ("torch_compile_weighted_gram", helion_mod.sandwich_torch_compile_weighted_gram),
    ]:
        med = _median_timings(lambda fn=fn: fn(Xt, dt), repeats, warmup)
        out = fn(Xt, dt)
        err = float((out - ref_t).abs().max().item() / ref_t.abs().clamp_min(1e-12).max().item())
        out_rows.append(
            BenchRow(label, "single", 1, med, 0.0, err, "torch.compile CPU inductor")
        )

    if helion_mod.helion_available():
        helion_mod.warmup_helion("eager")
        med = _median_timings(
            lambda: helion_mod.sandwich_helion(Xt, dt, mode="eager"),
            repeats,
            warmup,
        )
        out = helion_mod.sandwich_helion(Xt, dt, mode="eager")
        err = float((out - ref_t).abs().max().item() / ref_t.abs().clamp_min(1e-12).max().item())
        out_rows.append(
            BenchRow(
                "helion_eager",
                "single",
                1,
                med,
                0.0,
                err,
                "Helion ref_mode=EAGER (CPU reference tiles)",
            )
        )

        if torch.cuda.is_available():
            Xg = Xt.cuda()
            dg = dt.cuda()
            helion_mod.warmup_helion("triton")
            med = _median_timings(
                lambda: helion_mod.sandwich_helion(Xg, dg, mode="triton"),
                repeats,
                warmup,
            )
            out = helion_mod.sandwich_helion(Xg, dg, mode="triton").cpu()
            err = float((out - ref_t).abs().max().item() / ref_t.abs().clamp_min(1e-12).max().item())
            out_rows.append(
                BenchRow(
                    "helion_triton",
                    "single",
                    1,
                    med,
                    0.0,
                    err,
                    "Helion compiled Triton kernel on GPU",
                )
            )
        else:
            out_rows.append(
                BenchRow(
                    "helion_triton",
                    "n/a",
                    0,
                    0.0,
                    0.0,
                    0.0,
                    "skipped: no CUDA GPU in this environment",
                )
            )

        triton_cpu_mod = _load_module("triton_cpu_kernel", BASE_DIR / "kernels/triton_cpu_kernel.py")
        os.environ["TRITON_CPU_BACKEND"] = "1"
        if triton_cpu_mod.triton_cpu_available():
            triton_cpu_mod.warmup_triton_cpu_native()
            med = _median_timings(
                lambda: triton_cpu_mod.sandwich_triton_cpu_native(X, d),
                repeats,
                warmup,
            )
            out = triton_cpu_mod.sandwich_triton_cpu_native(X, d)
            err = float(np.max(np.abs(out - reference) / np.maximum(np.abs(reference), 1e-12)))
            out_rows.append(
                BenchRow(
                    "triton_cpu_native",
                    "single",
                    1,
                    med,
                    0.0,
                    err,
                    "Hand-written Triton row-chunked weighted Gram (triton-cpu)",
                )
            )

            triton_cpu_mod.warmup_helion_triton_cpu()
            med = _median_timings(
                lambda: triton_cpu_mod.sandwich_helion_triton_cpu(
                    X.astype(np.float64), d.astype(np.float64)
                ),
                repeats,
                warmup,
            )
            out = triton_cpu_mod.sandwich_helion_triton_cpu(X, d)
            err = float(np.max(np.abs(out - reference) / np.maximum(np.abs(reference), 1e-12)))
            out_rows.append(
                BenchRow(
                    "helion_triton_cpu",
                    "single",
                    1,
                    med,
                    0.0,
                    err,
                    "Helion Triton via triton-cpu backend (TRITON_CPU_BACKEND=1)",
                )
            )

            triton_cpu_mod.warmup_torch_compile_triton_cpu()
            med = _median_timings(
                lambda: triton_cpu_mod.sandwich_torch_compile_triton_cpu(X, d),
                repeats,
                warmup,
            )
            out = triton_cpu_mod.sandwich_torch_compile_triton_cpu(X, d)
            err = float(np.max(np.abs(out - reference) / np.maximum(np.abs(reference), 1e-12)))
            out_rows.append(
                BenchRow(
                    "torch_compile_triton_cpu",
                    "single",
                    1,
                    med,
                    0.0,
                    err,
                    "torch.compile Inductor cpu_backend=triton (triton-cpu)",
                )
            )
        else:
            skip_note = "skipped: triton-cpu not built (run build_triton_cpu.sh)"
            for label in ("triton_cpu_native", "helion_triton_cpu", "torch_compile_triton_cpu"):
                out_rows.append(
                    BenchRow(label, "n/a", 0, 0.0, 0.0, 0.0, skip_note)
                )
    else:
        out_rows.append(
            BenchRow(
                "helion_eager",
                "n/a",
                0,
                0.0,
                0.0,
                0.0,
                "helion not installed",
            )
        )

    return out_rows


def _write_report(rows: list[BenchRow], path: Path, title: str) -> None:
    lines = [f"# {title}", ""]
    lines.append("| kernel | threading | threads | median (ms) | vs tabmat | max rel err | notes |")
    lines.append("|---|---|---:|---:|---:|---:|---|")
    for row in rows:
        vs = f"{row.vs_tabmat:.2f}x" if row.vs_tabmat else "n/a"
        lines.append(
            f"| {row.kernel} | {row.threading} | {row.num_threads} | "
            f"{row.median_ms:.2f} | {vs} | {row.max_rel_err:.2e} | {row.notes} |"
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repeats", type=int, default=5)
    parser.add_argument("--warmup", type=int, default=2)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--n-rows", type=int, default=50_000)
    parser.add_argument("--n-cols", type=int, default=40)
    args = parser.parse_args()

    rng = np.random.default_rng(args.seed)
    X = np.ascontiguousarray(rng.standard_normal((args.n_rows, args.n_cols), dtype=np.float64))
    d = np.ascontiguousarray(rng.random(args.n_rows, dtype=np.float64) + 0.1)
    ref_mod = _load_module("reference", BASE_DIR / "kernels/reference.py")
    reference = ref_mod.sandwich_reference(X, d)

    xsimd_rows = benchmark_numpy_xsimd(X, d, reference, repeats=args.repeats, warmup=args.warmup)
    helion_rows = benchmark_helion_torch(X, d, reference, repeats=args.repeats, warmup=args.warmup)

    artifacts = BASE_DIR / "artifacts"
    artifacts.mkdir(parents=True, exist_ok=True)
    _write_report(xsimd_rows, artifacts / "benchmark_xsimd_report.md", "xsimd extension benchmark")
    _write_report(helion_rows, artifacts / "benchmark_helion_report.md", "Helion / torch.compile benchmark")

    payload = {
        "problem": {"n_rows": args.n_rows, "n_cols": args.n_cols, "dtype": "float64"},
        "xsimd": [asdict(r) for r in xsimd_rows],
        "helion_torch": [asdict(r) for r in helion_rows],
    }
    (artifacts / "benchmark_xsimd_helion.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
