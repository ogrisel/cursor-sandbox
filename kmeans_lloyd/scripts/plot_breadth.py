"""Plots for the breadth comparison. Reads the JSONL written by bench_breadth."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

IMPLS = ("torch-cpu", "sklearn-vanilla", "sklearn-optimized", "torch-cuda", "cuml")
LABELS = {
    "torch-cpu": "array API, PyTorch CPU",
    "sklearn-vanilla": "scikit-learn 1.7.2",
    "sklearn-optimized": "scikit-learn PRs 23 and 26",
    "torch-cuda": "array API, PyTorch CUDA",
    "cuml": "cuML 26.10",
}
COLORS = {
    "torch-cpu": "#4C78A8",
    "sklearn-vanilla": "#F58518",
    "sklearn-optimized": "#54A24B",
    "torch-cuda": "#E45756",
    "cuml": "#72B7B2",
}


def load(path: Path):
    text = path.read_text()
    if text.lstrip().startswith("["):
        source = json.loads(text)
    else:
        source = [json.loads(line) for line in text.splitlines() if line.strip()]
    rows = []
    for row in source:
        if "error" in row or "seconds" not in row:
            continue
        rows.append(row)
    return rows


def _grouped(ax, cases, rows, phase, field, title, ylabel, log=False):
    import numpy as np

    present = [impl for impl in IMPLS if any(row["impl"] == impl and row["phase"] == phase for row in rows)]
    width = 0.8 / max(len(present), 1)
    xs = np.arange(len(cases))
    for index, impl in enumerate(present):
        values = []
        errors = []
        for name in cases:
            match = [
                row[field]
                for row in rows
                if row["case"]["name"] == name and row["impl"] == impl and row["phase"] == phase and row.get(field) is not None
            ]
            values.append(float(np.mean(match)) if match else np.nan)
            errors.append(float(np.std(match, ddof=1)) if len(match) > 1 else 0.0)
        offset = (index - (len(present) - 1) / 2) * width
        ax.bar(
            xs + offset,
            values,
            yerr=errors,
            width=width * 0.92,
            color=COLORS[impl],
            label=LABELS[impl],
            error_kw={"elinewidth": 0.8, "capsize": 1.5},
        )
    ax.set_xticks(xs, cases, rotation=30, ha="right")
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    if log:
        ax.set_yscale("log")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def _has(rows, name):
    return any(row["case"]["name"] == name and row["phase"] == "fit" for row in rows)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    rows = load(Path(args.results))
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    structure = [name for name in ("tight", "mild", "loose", "overlap", "noise") if _has(rows, name)]
    centroids = [name for name in ("k4", "k16", "k64", "k128") if _has(rows, name)]
    speed = [name for name in ("tall", "wide", "mixed", "speed-m", "speed-l", "speed-xl") if _has(rows, name)]

    fig, axes = plt.subplots(1, 2, figsize=(11.2, 4.4))
    _grouped(axes[0], structure, rows, "init", "inertia_per_point", "After k-means++", "mean squared distance")
    _grouped(axes[1], structure, rows, "fit", "inertia_per_point", "After the fit", "mean squared distance")
    axes[1].legend(frameon=False, fontsize=8, loc="upper left")
    fig.suptitle("Blob structure, 20000 x 32, 8 clusters", fontsize=12)
    fig.tight_layout()
    fig.savefig(out / "inertia-structure.svg")
    plt.close(fig)

    fig, axes = plt.subplots(1, 3, figsize=(13.5, 4.2))
    _grouped(axes[0], speed, rows, "init", "seconds", "k-means++", "seconds", log=True)
    _grouped(axes[1], speed, rows, "lloyd", "seconds", "One Lloyd iteration", "seconds", log=True)
    _grouped(axes[2], speed, rows, "fit", "seconds", "Full fit", "seconds", log=True)
    axes[2].legend(frameon=False, fontsize=8)
    fig.suptitle("Duration on the larger shapes", fontsize=12)
    fig.tight_layout()
    fig.savefig(out / "time-scale.svg")
    plt.close(fig)

    fig, axes = plt.subplots(1, 2, figsize=(11.2, 4.4))
    _grouped(
        axes[0],
        speed,
        rows,
        "fit",
        "mem_increment_bytes",
        "Full fit, peak increment",
        "bytes",
        log=True,
    )
    _grouped(axes[1], centroids, rows, "fit", "seconds", "Full fit versus centroid count", "seconds", log=True)
    axes[0].legend(frameon=False, fontsize=8)
    fig.tight_layout()
    fig.savefig(out / "memory-and-k.svg")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8.4, 4.2))
    _grouped(ax, structure, rows, "fit", "n_iter", "Iterations until the shared budget", "iterations")
    ax.legend(frameon=False, fontsize=8)
    fig.tight_layout()
    fig.savefig(out / "iterations-structure.svg")
    plt.close(fig)

    fig, axes = plt.subplots(1, 3, figsize=(13.5, 4.2))
    _grouped(axes[0], speed, rows, "lloyd", "seconds", "One shared-center step", "seconds", log=True)
    _grouped(axes[1], speed, rows, "fixed-fit", "seconds", "Shared-center fit", "seconds", log=True)
    _grouped(
        axes[2],
        speed,
        rows,
        "fixed-fit",
        "inertia_per_point",
        "Shared-center fit quality",
        "mean squared distance",
    )
    axes[2].legend(frameon=False, fontsize=8)
    fig.suptitle("Lloyd isolated from initialization (mean +/- one standard deviation)", fontsize=12)
    fig.tight_layout()
    fig.savefig(out / "fixed-centers.svg")
    plt.close(fig)
    print(f"wrote plots for {len(rows)} rows", flush=True)


if __name__ == "__main__":
    main()
