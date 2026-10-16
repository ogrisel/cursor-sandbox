"""Plot the 010 initializer comparison and empty-center relocation figure."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from plot_consolidated import plot_init


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

    plot_init(rows, out)

    relocation = [
        ("Array API - Torch CUDA, keep empty", previous, "torch-cuda-keep", "#E45756"),
        ("Array API - Torch CUDA, stochastic (008)", previous, "torch-cuda-reassign", "#FF9D9A"),
        ("Array API - Torch CUDA, farthest", rows, "torch-cuda-farthest", "#B279A2"),
        ("scikit-learn 1.7.2, farthest", previous, "sklearn-vanilla", "#F58518"),
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
