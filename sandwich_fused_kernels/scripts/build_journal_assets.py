#!/usr/bin/env python3
"""Build journal plots and summary JSON from benchmark artifacts."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT / "artifacts"
JOURNAL = ROOT / "journal"
BRANCH = "cursor/sandwich-fused-kernels-000a"
GH = f"https://github.com/ogrisel/cursor-sandbox/blob/{BRANCH}/sandwich_fused_kernels"

# Highlight kernels for comparison plots (order = legend preference).
HIGHLIGHT = [
    "tabmat",
    "numba_blas_tuned",
    "xsimd_tuned",
    "torch_compile_triton_cpu",
    "torch_compile_triton_tuned",
    "triton_cpu_tuned",
    "torch_compile_einsum",
    "helion_tiled_tuned",
    "numba_rival_mt",
    "numpy_einsum",
]

COLORS = {
    "tabmat": "#8c3a2f",
    "numba_blas_tuned": "#1f6f4a",
    "xsimd_tuned": "#2c5aa0",
    "torch_compile_triton_cpu": "#6b4c9a",
    "torch_compile_triton_tuned": "#9a4c6b",
    "triton_cpu_tuned": "#b36b1a",
    "torch_compile_einsum": "#4a708b",
    "helion_tiled_tuned": "#5a7a3a",
    "numba_rival_mt": "#888888",
    "numpy_einsum": "#bbbbbb",
}


def load_rows() -> list[dict]:
    return json.loads((ARTIFACTS / "benchmark_results.json").read_text(encoding="utf-8"))


def by_threading(rows: list[dict], mode: str) -> list[dict]:
    return [r for r in rows if r["threading"] == mode]


def plot_vs_tabmat(rows: list[dict], mode: str, out: Path) -> None:
    subset = by_threading(rows, mode)
    problems = sorted({r["problem"] for r in subset})
    kernels = [k for k in HIGHLIGHT if any(r["kernel"] == k for r in subset)]
    x = np.arange(len(problems))
    width = 0.8 / max(len(kernels), 1)
    fig, ax = plt.subplots(figsize=(11, 5.2))
    for i, kernel in enumerate(kernels):
        vals = []
        for problem in problems:
            hit = next((r for r in subset if r["problem"] == problem and r["kernel"] == kernel), None)
            vals.append(hit["speedup_vs_tabmat"] if hit else np.nan)
        ax.bar(
            x + i * width - 0.4 + width / 2,
            vals,
            width,
            label=kernel,
            color=COLORS.get(kernel, "#666"),
        )
    ax.axhline(1.0, color="#8c3a2f", linestyle="--", linewidth=1, label="tabmat = 1×")
    ax.set_xticks(x)
    ax.set_xticklabels(problems, rotation=15, ha="right")
    ax.set_ylabel("Speedup vs tabmat (higher is better)")
    ax.set_title(f"Sandwich kernels vs tabmat ({mode}-threaded)")
    ax.legend(fontsize=8, ncol=2, loc="upper left")
    ax.set_ylim(0, None)
    fig.tight_layout()
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=140)
    plt.close(fig)


def plot_latency_heatmap(rows: list[dict], mode: str, out: Path) -> None:
    subset = by_threading(rows, mode)
    problems = sorted({r["problem"] for r in subset})
    # Pick a compact set present across problems.
    kernels = [
        k
        for k in [
            "tabmat",
            "numba_blas_tuned",
            "xsimd_tuned",
            "torch_compile_triton_cpu",
            "torch_compile_triton_tuned",
            "triton_cpu_tuned",
            "torch_compile_einsum",
            "numpy_einsum",
        ]
        if any(r["kernel"] == k for r in subset)
    ]
    data = np.full((len(kernels), len(problems)), np.nan)
    for i, kernel in enumerate(kernels):
        for j, problem in enumerate(problems):
            hit = next((r for r in subset if r["problem"] == problem and r["kernel"] == kernel), None)
            if hit:
                data[i, j] = hit["median_seconds"] * 1000
    fig, ax = plt.subplots(figsize=(10, 4.8))
    im = ax.imshow(np.log10(data), aspect="auto", cmap="YlOrRd")
    ax.set_xticks(range(len(problems)))
    ax.set_xticklabels(problems, rotation=15, ha="right")
    ax.set_yticks(range(len(kernels)))
    ax.set_yticklabels(kernels)
    for i in range(len(kernels)):
        for j in range(len(problems)):
            if np.isfinite(data[i, j]):
                ax.text(j, i, f"{data[i, j]:.1f}", ha="center", va="center", fontsize=8)
    ax.set_title(f"Median latency (ms), log-scaled color ({mode})")
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04, label="log10(ms)")
    fig.tight_layout()
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=140)
    plt.close(fig)


def plot_complexity_scatter(out: Path) -> None:
    """Qualitative complexity vs MT performance for the summary page."""
    points = [
        ("numpy/jax einsum", 0.15, 0.20),
        ("numba fused rivals", 0.35, 0.15),
        ("numba BLAS tuned", 0.40, 0.95),
        ("tabmat", 0.55, 0.85),
        ("xsimd tuned", 0.70, 0.80),
        ("torch.compile triton", 0.75, 0.75),
        ("triton native tuned", 0.85, 0.55),
        ("torch.compile triton tiled", 0.90, 0.70),
    ]
    fig, ax = plt.subplots(figsize=(8.5, 5.2))
    for name, x, y in points:
        ax.scatter([x], [y], s=80)
        ax.annotate(name, (x, y), textcoords="offset points", xytext=(6, 4), fontsize=9)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1.05)
    ax.set_xlabel("Implementation / ops complexity (qualitative)")
    ax.set_ylabel("Multi-thread performance vs tabmat (qualitative)")
    ax.set_title("Complexity vs performance of explored sandwich backends")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=140)
    plt.close(fig)


def write_summary_json(rows: list[dict], out: Path) -> None:
    summary: dict[str, dict[str, dict[str, float]]] = {}
    for mode in ("single", "multi"):
        summary[mode] = {}
        for r in by_threading(rows, mode):
            summary[mode].setdefault(r["problem"], {})[r["kernel"]] = {
                "median_ms": r["median_seconds"] * 1000,
                "vs_tabmat": r["speedup_vs_tabmat"],
            }
    out.write_text(json.dumps(summary, indent=2), encoding="utf-8")


def main() -> None:
    rows = load_rows()
    out_dir = JOURNAL / "05-latest-benchmarks"
    plot_vs_tabmat(rows, "multi", out_dir / "mt_vs_tabmat.svg")
    plot_vs_tabmat(rows, "single", out_dir / "st_vs_tabmat.svg")
    plot_latency_heatmap(rows, "multi", out_dir / "mt_latency_heatmap.svg")
    plot_latency_heatmap(rows, "single", out_dir / "st_latency_heatmap.svg")
    plot_complexity_scatter(JOURNAL / "00-overview" / "complexity_vs_performance.svg")
    write_summary_json(rows, out_dir / "benchmark_summary.json")
    # Copy key artifact JSON next to reports for download.
    for name in ("autotune_results.json", "tabmat_advantage_analysis.json", "simd_inspection.json"):
        src = ARTIFACTS / name
        if src.is_file():
            dest_dir = {
                "autotune_results.json": JOURNAL / "03-autotuning",
                "tabmat_advantage_analysis.json": JOURNAL / "01-tabmat-baseline",
                "simd_inspection.json": JOURNAL / "02-simd-and-rivals",
            }[name]
            dest_dir.mkdir(parents=True, exist_ok=True)
            (dest_dir / name).write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
    print(f"Wrote journal assets under {JOURNAL}")
    print(f"Source link base: {GH}")


if __name__ == "__main__":
    main()
