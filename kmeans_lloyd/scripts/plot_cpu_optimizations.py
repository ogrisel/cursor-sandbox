"""Consolidate and plot the CPU optimization iterations."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

import numpy as np

TASKS = ("k100-d32", "k550-d6", "k3000-d2")
PHASES = ("init", "lloyd", "fit")
METHODS = {
    "init": ("baseline", "homogeneous"),
    "lloyd": (
        "legacy",
        "baseline",
        "interleaved-tuned",
        "homogeneous-lloyd",
    ),
    "fit": ("legacy", "baseline", "homogeneous", "homogeneous-lloyd"),
}
LABELS = {
    "legacy": "previous",
    "baseline": "labels-only",
    "interleaved-tuned": "interleaved",
    "homogeneous": "augmented GEMM",
    "homogeneous-lloyd": "augmented Lloyd",
}
COLORS = {
    "legacy": "#9D9D9D",
    "baseline": "#4C78A8",
    "interleaved-tuned": "#F2CF5B",
    "homogeneous": "#E45756",
    "homogeneous-lloyd": "#72B7B2",
}


def load(path):
    path = Path(path)
    text = path.read_text()
    if path.suffix == ".json":
        return json.loads(text)
    return [json.loads(line) for line in text.splitlines() if line.strip()]


def selected(rows, phase, method, task):
    return [
        row
        for row in rows
        if "error" not in row
        and row["phase"] == phase
        and row["method"] == method
        and row["task"]["name"] == task
    ]


def mean(rows, field):
    return float(np.mean([row[field] for row in rows]))


def ratio_figure(path, rows, field, ylabel):
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(3, 1, figsize=(10, 9))
    xs = np.arange(len(TASKS))
    for ax, phase in zip(axes, PHASES):
        methods = METHODS[phase]
        width = 0.8 / len(methods)
        baseline = {
            task: mean(selected(rows, phase, "baseline", task), field)
            for task in TASKS
        }
        for index, method in enumerate(methods):
            values = [
                mean(selected(rows, phase, method, task), field)
                / baseline[task]
                for task in TASKS
            ]
            positions = xs + (index - (len(methods) - 1) / 2) * width
            ax.bar(
                positions,
                values,
                width * 0.92,
                color=COLORS[method],
                label=LABELS[method],
            )
        ax.axhline(1, color="#333333", linewidth=0.8)
        ax.set_xticks(xs, TASKS)
        ax.set_ylabel(ylabel)
        ax.set_title(phase)
        ax.spines[["top", "right"]].set_visible(False)
    handles = {}
    for ax in axes:
        found_handles, found_labels = ax.get_legend_handles_labels()
        handles.update(zip(found_labels, found_handles))
    fig.legend(
        handles.values(),
        handles.keys(),
        loc="lower center",
        ncol=len(handles),
        frameon=False,
    )
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    fig.savefig(path, metadata={"Date": None})
    plt.close(fig)


def quality_figure(path, rows):
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, 3, figsize=(11, 3.7))
    for ax, phase in zip(axes, PHASES):
        for method in METHODS[phase]:
            values = []
            for task in TASKS:
                base = mean(
                    selected(rows, phase, "baseline", task),
                    "inertia_per_point",
                )
                value = mean(
                    selected(rows, phase, method, task),
                    "inertia_per_point",
                )
                values.append(100 * (value / base - 1))
            ax.plot(
                range(len(TASKS)),
                values,
                "o-",
                color=COLORS[method],
                label=LABELS[method],
            )
        ax.axhline(0, color="#333333", linewidth=0.8)
        ax.set_xticks(range(len(TASKS)), TASKS, rotation=20)
        ax.set_title(phase)
        ax.spines[["top", "right"]].set_visible(False)
    axes[0].set_ylabel("inertia change from labels-only (%)")
    handles, labels = axes[-1].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=3, frameon=False)
    fig.tight_layout(rect=(0, 0.14, 1, 1))
    fig.savefig(path, metadata={"Date": None})
    plt.close(fig)


def final_tables(rows, historical):
    lines = []
    for phase in PHASES:
        lines += [
            f"### {phase}: mean seconds",
            "",
            "| method | " + " | ".join(TASKS) + " |",
            "| --- |" + " ---: |" * len(TASKS),
        ]
        for method in METHODS[phase]:
            cells = [
                f"{mean(selected(rows, phase, method, task), 'seconds'):.3f}"
                for task in TASKS
            ]
            lines.append(f"| {LABELS[method]} | " + " | ".join(cells) + " |")
        lines.append("")

    old = defaultdict(list)
    cake = defaultdict(list)
    for row in historical:
        if row.get("phase") != "fit":
            continue
        task = row["task"]["name"]
        if task not in TASKS:
            continue
        phase = "lloyd" if row.get("init") == "random" else "fit"
        if row.get("impl") == "torch-cpu":
            old[(phase, task)].append(row)
        if row.get("impl") == "sklearn-optimized":
            cake[(phase, task)].append(row)
    for row in historical:
        if row.get("phase") != "init" or row["task"]["name"] not in TASKS:
            continue
        key = ("init", row["task"]["name"])
        if row.get("impl") == "torch-cpu":
            old[key].append(row)
        if row.get("impl") == "sklearn-optimized":
            cake[key].append(row)

    best = {
        "init": {"k100-d32": "homogeneous", "k550-d6": "homogeneous", "k3000-d2": "homogeneous"},
        "lloyd": {task: "homogeneous-lloyd" for task in TASKS},
        "fit": {
            "k100-d32": "homogeneous",
            "k550-d6": "homogeneous-lloyd",
            "k3000-d2": "homogeneous-lloyd",
        },
    }
    lines += [
        "### Historical cakedev0 gap and speedup projection",
        "",
        "| phase | task | old array API / cakedev0 | local speedup | "
        "projected optimized / cakedev0 |",
        "| --- | --- | ---: | ---: | ---: |",
    ]
    for phase in PHASES:
        for task in TASKS:
            historical_gap = mean(old[(phase, task)], "seconds") / mean(
                cake[(phase, task)], "seconds"
            )
            method = best[phase][task]
            local_reference = "baseline" if phase == "init" else "legacy"
            local_speedup = mean(
                selected(rows, phase, local_reference, task), "seconds"
            ) / mean(selected(rows, phase, method, task), "seconds")
            lines.append(
                f"| {phase} | {task} | {historical_gap:.2f}x | "
                f"{local_speedup:.2f}x | "
                f"{historical_gap / local_speedup:.2f}x |"
            )
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--iteration", action="append", required=True)
    parser.add_argument("--final", required=True)
    parser.add_argument("--historical", action="append", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    iterations = {
        f"iteration-{index + 1}": load(path)
        for index, path in enumerate(args.iteration)
    }
    final = load(args.final)
    historical = [
        row for path in args.historical for row in load(path)
    ]
    result = {
        "iterations": iterations,
        "final": final,
        "historical_reference": historical,
    }
    (out / "results.json").write_text(json.dumps(result, indent=2) + "\n")
    ratio_figure(
        out / "time-ratios.svg",
        final,
        "seconds",
        "time / labels-only",
    )
    ratio_figure(
        out / "memory-ratios.svg",
        final,
        "mem_increment_bytes",
        "peak memory / labels-only",
    )
    quality_figure(out / "quality-impact.svg", final)
    (out / "tables.md").write_text(final_tables(final, historical))


if __name__ == "__main__":
    main()
