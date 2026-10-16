"""Plot classic, scalable, and random initialization strategies."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

TASKS = ["k3-d1000", "k17-d180", "k100-d32", "k550-d6", "k3000-d2"]
CLASSIC = [
    "torch-cpu",
    "sklearn-vanilla",
    "sklearn-optimized",
    "torch-cuda",
    "cupy",
    "cuml",
]
ALTERNATIVES = [
    "torch-cpu-scalable",
    "torch-cuda-scalable",
    "cupy-scalable",
    "cuml-scalable",
    "cuml-random",
    "random-baseline",
]
LABEL = {
    "torch-cpu": "API CPU, greedy",
    "sklearn-vanilla": "sklearn 1.7, greedy",
    "sklearn-optimized": "sklearn PRs, greedy",
    "torch-cuda": "API CUDA, greedy",
    "cupy": "API CuPy, greedy",
    "cuml": "cuML, greedy",
    "torch-cpu-scalable": "API CPU, scalable",
    "torch-cuda-scalable": "API CUDA, scalable",
    "cupy-scalable": "API CuPy, scalable",
    "cuml-scalable": "cuML, scalable",
    "cuml-random": "cuML, random",
    "random-baseline": "shared random rows",
}
COLOR = {
    name: color
    for name, color in zip(
        CLASSIC + ALTERNATIVES,
        (
            "#4C78A8",
            "#F58518",
            "#54A24B",
            "#E45756",
            "#B279A2",
            "#72B7B2",
            "#7EA6D8",
            "#FF9D9A",
            "#D6A5CF",
            "#4CB5AE",
            "#C49A00",
            "#8C8C8C",
        ),
    )
}


def _value(row, field):
    # cuML exposes no standalone random initializer. max_iter=0 followed by
    # subtraction is below timer noise, so its full zero-iteration fit is the
    # honest timing upper bound.
    if field == "seconds" and row["impl"] == "cuml-random":
        return row["fit_seconds"]
    return row.get(field)


def aggregate(rows, task, impl, field):
    values = [
        _value(row, field)
        for row in rows
        if "error" not in row
        and row.get("phase") == "init"
        and row["task"]["name"] == task
        and row["impl"] == impl
        and _value(row, field) is not None
    ]
    if not values:
        return np.nan, 0
    return float(np.mean(values)), float(np.std(values, ddof=1)) if len(values) > 1 else 0


def grouped(ax, rows, implementations, field, title, ylabel, best=None, log=False):
    present = [
        impl
        for impl in implementations
        if any(
            row.get("phase") == "init" and row["impl"] == impl and "error" not in row
            for row in rows
        )
    ]
    width = 0.88 / len(present)
    xs = np.arange(len(TASKS))
    for index, impl in enumerate(present):
        means, errors = [], []
        for task in TASKS:
            mean, error = aggregate(rows, task, impl, field)
            if best is not None:
                mean, error = mean / best[task], error / best[task]
            means.append(mean)
            errors.append(error)
        offset = (index - (len(present) - 1) / 2) * width
        ax.bar(
            xs + offset,
            means,
            yerr=errors,
            width=width * 0.94,
            color=COLOR[impl],
            label=LABEL[impl],
            error_kw={"elinewidth": 0.7, "capsize": 1},
        )
    ax.set_xticks(xs, TASKS, rotation=25, ha="right")
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    if log:
        ax.set_yscale("log")
    ax.spines[["top", "right"]].set_visible(False)


def _relocation_value(rows, impl, field):
    values = [
        row[field]
        for row in rows
        if "error" not in row
        and row["task"]["name"] == "k3000-d2"
        and row["init"] == "random"
        and row["impl"] == impl
    ]
    return float(np.mean(values)), float(np.std(values, ddof=1))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", required=True)
    parser.add_argument("--previous-fit", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    rows = json.loads(Path(args.results).read_text())
    previous = json.loads(Path(args.previous_fit).read_text())
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    fig, axes = plt.subplots(1, 2, figsize=(15, 5))
    grouped(axes[0], rows, CLASSIC, "seconds", "Greedy k-means++", "seconds", log=True)
    grouped(
        axes[1],
        rows,
        ALTERNATIVES[:-1],
        "seconds",
        "Scalable and random",
        "seconds",
        log=True,
    )
    for ax in axes:
        ax.legend(frameon=False, fontsize=7, ncol=2)
    fig.suptitle(
        "Initialization duration, mean +/- sample standard deviation "
        "(cuML random is a zero-iteration-fit upper bound)"
    )
    fig.tight_layout()
    fig.savefig(out / "duration.svg")
    plt.close(fig)

    fig, axes = plt.subplots(1, 2, figsize=(15, 5))
    grouped(axes[0], rows, CLASSIC, "mem_increment_bytes", "Greedy k-means++", "bytes", log=True)
    grouped(
        axes[1],
        rows,
        ALTERNATIVES[:-1],
        "mem_increment_bytes",
        "Scalable and random",
        "bytes",
        log=True,
    )
    for ax in axes:
        ax.legend(frameon=False, fontsize=7, ncol=2)
    fig.suptitle("Initialization peak memory increment")
    fig.tight_layout()
    fig.savefig(out / "memory.svg")
    plt.close(fig)

    quality_impls = CLASSIC + ALTERNATIVES[:-1]
    best = {
        task: min(aggregate(rows, task, impl, "inertia_per_point")[0] for impl in quality_impls)
        for task in TASKS
    }
    fig, axes = plt.subplots(1, 2, figsize=(15, 5))
    grouped(
        axes[0],
        rows,
        CLASSIC,
        "inertia_per_point",
        "Greedy k-means++",
        "inertia / best mean",
        best=best,
    )
    grouped(
        axes[1],
        rows,
        ALTERNATIVES,
        "inertia_per_point",
        "Scalable and random",
        "inertia / best mean",
        best=best,
    )
    for ax in axes:
        ax.legend(frameon=False, fontsize=7, ncol=2)
    fig.suptitle("No-Lloyd quality relative to the best initializer per task")
    fig.tight_layout()
    fig.savefig(out / "quality.svg")
    plt.close(fig)

    relocation = [
        ("API CUDA, keep", previous, "torch-cuda-keep", "#E45756"),
        ("API CUDA, stochastic (008)", previous, "torch-cuda-reassign", "#FF9D9A"),
        ("API CUDA, farthest", rows, "torch-cuda-farthest", "#B279A2"),
        ("sklearn 1.7, farthest", previous, "sklearn-vanilla", "#F58518"),
    ]
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    xs = np.arange(len(relocation))
    for ax, field, ylabel in (
        (axes[0], "seconds", "seconds"),
        (axes[1], "inertia_per_point", "mean inertia"),
    ):
        means, errors, colors, labels = [], [], [], []
        for label, source, impl, color in relocation:
            mean, error = _relocation_value(source, impl, field)
            means.append(mean)
            errors.append(error)
            colors.append(color)
            labels.append(label)
        ax.bar(xs, means, yerr=errors, color=colors, error_kw={"elinewidth": 0.8, "capsize": 2})
        ax.set_xticks(xs, labels, rotation=22, ha="right")
        ax.set_ylabel(ylabel)
        ax.spines[["top", "right"]].set_visible(False)
    axes[0].set_title("Runtime")
    axes[1].set_title("Quality after 12 Lloyd iterations")
    fig.suptitle("3000 clusters: empty-center relocation from shared random rows")
    fig.tight_layout()
    fig.savefig(out / "relocation.svg")
    plt.close(fig)

    print(f"wrote consolidated plots for {len(rows)} rows")


if __name__ == "__main__":
    main()
