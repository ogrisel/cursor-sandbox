"""Plot k-means++ initialization without Lloyd iterations."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

ORDER = (
    "torch-cpu",
    "sklearn-vanilla",
    "sklearn-optimized",
    "torch-cuda",
    "cupy",
    "cuml",
    "random-baseline",
)
LABEL = {
    "torch-cpu": "API CPU",
    "sklearn-vanilla": "sklearn 1.7",
    "sklearn-optimized": "sklearn PRs",
    "torch-cuda": "API CUDA",
    "cupy": "API CuPy",
    "cuml": "cuML",
    "random-baseline": "random baseline",
}
COLOR = {
    name: color
    for name, color in zip(
        ORDER,
        ("#4C78A8", "#F58518", "#54A24B", "#E45756", "#B279A2", "#72B7B2", "#8C8C8C"),
    )
}


def _selected(row, impl, include_baseline):
    if "error" in row or row["impl"] != impl:
        return False
    if impl == "random-baseline":
        return include_baseline
    return row.get("phase", "init") == "init" and row["init"] == "plusplus"


def aggregate(rows, task, impl, field, include_baseline=False):
    values = [
        row[field]
        for row in rows
        if _selected(row, impl, include_baseline)
        and row["task"]["name"] == task
        and row.get(field) is not None
    ]
    if not values:
        return np.nan, 0
    return float(np.mean(values)), float(np.std(values, ddof=1)) if len(values) > 1 else 0


def grouped(ax, rows, tasks, field, title, ylabel, log=False, normalize=False, include_baseline=False):
    present = [
        impl
        for impl in ORDER
        if (include_baseline or impl != "random-baseline")
        and any(_selected(row, impl, include_baseline) for row in rows)
    ]
    width = 0.88 / len(present)
    xs = np.arange(len(tasks))
    best = {}
    if normalize:
        for task in tasks:
            candidates = [
                aggregate(rows, task, impl, field)[0]
                for impl in present
                if impl != "random-baseline"
            ]
            best[task] = np.nanmin(candidates)
    for index, impl in enumerate(present):
        means, errors = [], []
        for task in tasks:
            mean, error = aggregate(rows, task, impl, field, include_baseline=include_baseline)
            if normalize and best[task] > 0:
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

    fig, ax = plt.subplots(figsize=(11, 4.8))
    grouped(ax, rows, tasks, "seconds", "k-means++ only", "seconds", log=True)
    ax.legend(frameon=False, fontsize=8, ncol=3)
    fig.suptitle("Initialization duration, mean +/- sample standard deviation")
    fig.tight_layout()
    fig.savefig(out / "duration.svg")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(11, 4.8))
    grouped(
        ax, rows, tasks, "mem_increment_bytes",
        "k-means++ only", "bytes", log=True,
    )
    ax.legend(frameon=False, fontsize=8, ncol=3)
    fig.suptitle("Initialization peak memory increment")
    fig.tight_layout()
    fig.savefig(out / "memory.svg")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(11, 4.8))
    grouped(
        ax, rows, tasks, "inertia_per_point",
        "k-means++ only", "inertia / best mean",
        normalize=True, include_baseline=True,
    )
    ax.legend(frameon=False, fontsize=8, ncol=3)
    fig.suptitle("Initialization quality relative to the best k-means++ contender")
    fig.tight_layout()
    fig.savefig(out / "quality.svg")
    plt.close(fig)
    print(f"wrote k-means++ plots for {len(rows)} rows")


if __name__ == "__main__":
    main()
