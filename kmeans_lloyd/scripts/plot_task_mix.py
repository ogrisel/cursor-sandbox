"""Plot the bounded task-mix benchmark from its JSON snapshot."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

ORDER = (
    "torch-cpu-keep",
    "torch-cpu-reassign",
    "sklearn-vanilla",
    "sklearn-optimized",
    "torch-cuda-keep",
    "torch-cuda-reassign",
    "cupy-keep",
    "cupy-reassign",
    "cuml",
    "random-baseline",
)
LABEL = {
    "torch-cpu-keep": "API CPU, keep",
    "torch-cpu-reassign": "API CPU, reassign",
    "sklearn-vanilla": "sklearn 1.7",
    "sklearn-optimized": "sklearn PRs",
    "torch-cuda-keep": "API CUDA, keep",
    "torch-cuda-reassign": "API CUDA, reassign",
    "cupy-keep": "API CuPy, keep",
    "cupy-reassign": "API CuPy, reassign",
    "cuml": "cuML",
    "random-baseline": "random baseline",
}
COLOR = {
    name: color
    for name, color in zip(
        ORDER,
        ("#4C78A8", "#7EA6D8", "#F58518", "#54A24B", "#E45756", "#FF9D9A",
         "#B279A2", "#D6A5CF", "#72B7B2", "#8C8C8C"),
    )
}


def aggregate(rows, task, impl, init, field):
    values = [
        row[field]
        for row in rows
        if "error" not in row
        and row["task"]["name"] == task
        and row["impl"] == impl
        and row["init"] == init
        and row.get(field) is not None
    ]
    if not values:
        return np.nan, 0
    return float(np.mean(values)), float(np.std(values, ddof=1)) if len(values) > 1 else 0


def grouped(ax, rows, tasks, init, field, title, ylabel, log=False, normalize=False, include_baseline=False):
    present = [
        impl
        for impl in ORDER
        if (include_baseline or impl != "random-baseline")
        and any(row["impl"] == impl and row["init"] == init and "error" not in row for row in rows)
    ]
    width = 0.88 / len(present)
    xs = np.arange(len(tasks))
    best = {}
    if normalize:
        for task in tasks:
            candidates = [
                aggregate(rows, task, impl, init, field)[0]
                for impl in present
                if impl != "random-baseline"
            ]
            best[task] = np.nanmin(candidates)
    for index, impl in enumerate(present):
        means, errors = [], []
        for task in tasks:
            mean, error = aggregate(rows, task, impl, init, field)
            if normalize:
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
    ax.set_xticks(xs, tasks, rotation=25, ha="right")
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    if log:
        ax.set_yscale("log")
    ax.spines[["top", "right"]].set_visible(False)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    rows = json.loads(Path(args.results).read_text())
    tasks = ["k3-d1000", "k17-d180", "k100-d32", "k550-d6", "k3000-d2"]
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    fig, axes = plt.subplots(1, 2, figsize=(14, 4.8))
    grouped(axes[0], rows, tasks, "plusplus", "seconds", "k-means++ + Lloyd", "seconds", log=True)
    grouped(axes[1], rows, tasks, "random", "seconds", "Shared random rows + Lloyd", "seconds", log=True)
    axes[1].legend(frameon=False, fontsize=7, ncol=2)
    fig.suptitle("Full fit duration, mean +/- sample standard deviation")
    fig.tight_layout()
    fig.savefig(out / "duration.svg")
    plt.close(fig)

    fig, axes = plt.subplots(1, 2, figsize=(14, 4.8))
    grouped(
        axes[0], rows, tasks, "plusplus", "inertia_per_point",
        "k-means++ + Lloyd", "inertia / best mean", normalize=True,
    )
    grouped(
        axes[1], rows, tasks, "random", "inertia_per_point",
        "Shared random rows + Lloyd", "inertia / best mean", normalize=True,
        include_baseline=True,
    )
    axes[1].legend(frameon=False, fontsize=7, ncol=2)
    fig.suptitle("Fit quality relative to the best contender per task")
    fig.tight_layout()
    fig.savefig(out / "quality.svg")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(10.5, 4.8))
    grouped(
        ax, rows, tasks, "plusplus", "mem_increment_bytes",
        "k-means++ full-fit peak increment", "bytes", log=True,
    )
    ax.legend(frameon=False, fontsize=7, ncol=3)
    fig.tight_layout()
    fig.savefig(out / "memory.svg")
    plt.close(fig)

    focus = "k3000-d2"
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
    grouped(
        axes[0], rows, [focus], "random", "seconds",
        "3000 clusters: shared random start", "seconds", log=True,
    )
    grouped(
        axes[1], rows, [focus], "random", "inertia_per_point",
        "Relocation improves the shared start", "mean inertia",
        include_baseline=True,
    )
    axes[1].legend(frameon=False, fontsize=7, ncol=2)
    fig.tight_layout()
    fig.savefig(out / "relocation.svg")
    plt.close(fig)
    print(f"wrote task-mix plots for {len(rows)} rows")


if __name__ == "__main__":
    main()
