"""Plot the large-k Lloyd and scalable-init optimization probes."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np


TASKS = ["k100-d32", "k550-d6", "k3000-d2"]
SCALABLE_TASKS = ["k17-d180", "k100-d32", "k3000-d2"]
TASK_LABEL = {"k100-d32": "k=100, d=32", "k550-d6": "k=550, d=6", "k3000-d2": "k=3000, d=2"}
TASK_LABEL["k17-d180"] = "k=17, d=180"


def median(rows, field="seconds"):
    return float(np.median([row[field] for row in rows]))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--journal", required=True)
    parser.add_argument("--baseline", required=True)
    args = parser.parse_args()
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    journal = Path(args.journal)
    probes = json.loads((journal / "lloyd-probes.json").read_text())
    portable = json.loads((journal / "portable-results.json").read_text())
    cuml = json.loads((journal / "cuml-device-scaling.json").read_text())
    sensitivity = json.loads((journal / "scalable-sensitivity.json").read_text())
    baseline = json.loads(Path(args.baseline).read_text())

    runtime_variants = [
        ("Torch current", "#E45756", lambda task: median([
            r for r in portable if r["task"] == task and r["backend"] == "torch" and r["variant"] == "current"
        ])),
        ("Torch portable tuned", "#F28E8B", lambda task: median([
            r for r in portable if r["task"] == task and r["backend"] == "torch" and r["variant"] == "portable-tuned"
        ])),
        ("CuPy current", "#B279A2", lambda task: median([
            r for r in portable if r["task"] == task and r["backend"] == "cupy" and r["variant"] == "current"
        ])),
        ("CuPy portable tuned", "#D6A5CF", lambda task: median([
            r for r in portable if r["task"] == task and r["backend"] == "cupy" and r["variant"] == "portable-tuned"
        ])),
        ("Torch compile + tuned one-hot", "#4C78A8", lambda task: median([
            r for r in probes if r["task"] == task and r["phase"] == "fit-12"
            and r["variant"] == "compile-gather+tuned-onehot"
        ])),
        ("Torch compile + index-add", "#54A24B", lambda task: median([
            r for r in probes if r["task"] == task and r["phase"] == "fit-12"
            and r["variant"] == "compile-gather+torch-index-add"
        ])),
        ("cuML device-resident", "#72B7B2", lambda task: median([
            r for r in cuml if r["task"] == task and r["max_iter"] == 12
        ])),
    ]
    xs = np.arange(len(TASKS))
    width = 0.88 / len(runtime_variants)
    fig, ax = plt.subplots(figsize=(11.5, 5.2))
    for index, (name, color, getter) in enumerate(runtime_variants):
        values = [getter(task) for task in TASKS]
        ax.bar(xs + (index - 3) * width, values, width=width * 0.94, color=color, label=name)
    ax.set_xticks(xs, [TASK_LABEL[t] for t in TASKS])
    ax.set_yscale("log")
    ax.set_ylabel("seconds for 12 Lloyd iterations")
    ax.set_title("Large-k Lloyd optimization probes on NVIDIA L4")
    ax.legend(frameon=False, fontsize=8, ncol=3, loc="upper center", bbox_to_anchor=(0.5, -0.1))
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(journal / "lloyd-optimization.svg")
    plt.close(fig)

    assign_variants = [
        ("current", "current-n65536-k256", "#E45756"),
        ("argmin + gather", "portable-gather-n65536-k256", "#F58518"),
        ("compiled current tile", "compile-current-n65536-k256", "#4C78A8"),
    ]
    update_variants = [
        ("current one-hot", "current-k256-n4096", "#E45756"),
        ("tuned one-hot", None, "#F58518"),
        ("sorted segments", "portable-sorted-segments", "#B279A2"),
        ("Torch index-add", "torch-index-add", "#54A24B"),
    ]
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    for ax, variants, phase in (
        (axes[0], assign_variants, "assign"),
        (axes[1], update_variants, "update"),
    ):
        width = 0.85 / len(variants)
        for index, (label, variant, color) in enumerate(variants):
            values = []
            for task in TASKS:
                selected = variant
                if label == "tuned one-hot":
                    selected = "onehot-k100-n16384" if task == "k100-d32" else "onehot-k512-n16384"
                row = next(
                    r for r in probes
                    if r["task"] == task and r["phase"] == phase and r["variant"] == selected
                )
                values.append(1000 * row["seconds"])
            ax.bar(
                xs + (index - (len(variants) - 1) / 2) * width,
                values,
                width=width * 0.94,
                color=color,
                label=label,
            )
        ax.set_xticks(xs, [TASK_LABEL[t] for t in TASKS])
        ax.set_yscale("log")
        ax.set_ylabel("milliseconds per phase")
        ax.set_title("Assignment" if phase == "assign" else "Centroid update")
        ax.legend(frameon=False, fontsize=8)
        ax.spines[["top", "right"]].set_visible(False)
    fig.suptitle("One-phase timings after warmup")
    fig.tight_layout()
    fig.savefig(journal / "lloyd-phases.svg")
    plt.close(fig)

    def base_rows(task, phase, init):
        if phase == "init":
            impl = "torch-cuda" if init == "plusplus" else "torch-cuda-scalable"
        else:
            impl = "torch-cuda-farthest"
        return [
            row for row in baseline
            if "error" not in row and row.get("phase") == phase and row["task"]["name"] == task
            and row["init"] == init and row["impl"] == impl
        ]

    configs = [
        ("r2-o2", "2-2", "#4C78A8"),
        ("r4-o1", "4-1", "#F58518"),
        ("r4-o2", "4-2", "#54A24B"),
        ("r8-o1", "8-1", "#B279A2"),
        ("r8-o2", None, "#E45756"),
    ]
    fig, axes = plt.subplots(1, 3, figsize=(14, 4.5), sharey=True)
    for ax, task in zip(axes, SCALABLE_TASKS):
        for label, config, color in configs:
            for phase, marker, suffix in (("init", "o", " init"), ("fit", "s", " full fit")):
                greedy = base_rows(task, phase, "plusplus")
                if config is None:
                    scalable = base_rows(task, phase, "scalable")
                else:
                    scalable = [
                        row for row in sensitivity
                        if row["config"] == f"{config}-{phase}" and row["task"]["name"] == task
                    ]
                x = median(scalable) / median(greedy)
                y = (
                    np.mean([r["inertia_per_point"] for r in scalable])
                    / np.mean([r["inertia_per_point"] for r in greedy])
                )
                ax.scatter(x, y, marker=marker, color=color, s=45, label=label + suffix)
        ax.axvline(1, color="black", linestyle=":", linewidth=0.7)
        ax.axhline(1, color="black", linestyle=":", linewidth=0.7)
        ax.set_title(TASK_LABEL[task])
        ax.set_xlabel("time / greedy time")
        ax.spines[["top", "right"]].set_visible(False)
    axes[0].set_ylabel("inertia / greedy inertia")
    handles, labels = axes[-1].get_legend_handles_labels()
    fig.legend(handles, labels, frameon=False, fontsize=7, ncol=5, loc="lower center")
    fig.suptitle("Array-API scalable initialization sensitivity (circles: init, squares: full fit)")
    fig.tight_layout(rect=(0, 0.12, 1, 1))
    fig.savefig(journal / "scalable-sensitivity.svg")
    plt.close(fig)


if __name__ == "__main__":
    main()
