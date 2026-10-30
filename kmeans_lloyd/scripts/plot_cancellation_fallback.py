"""Consolidate and plot the GEMM cancellation fallback experiment."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

import numpy as np

TASKS = ["k3-d1000", "k17-d180", "k100-d32", "k550-d6", "k3000-d2"]
PHASES = ("init", "lloyd", "fit")
BACKENDS = ("torch-cpu", "torch-cuda", "cupy")
LABELS = {
    "torch-cpu": "Torch CPU",
    "torch-cuda": "Torch CUDA",
    "cupy": "CuPy CUDA",
}
COLORS = {
    "torch-cpu": "#4C78A8",
    "torch-cuda": "#E45756",
    "cupy": "#B279A2",
}


def load(path):
    path = Path(path)
    text = path.read_text()
    if path.suffix == ".json":
        return json.loads(text)
    return [json.loads(line) for line in text.splitlines() if line.strip()]


def mean(rows, field):
    return float(np.mean([row[field] for row in rows]))


def ordinary_rows(stable_path, clean_path):
    rows = load(stable_path)
    clean = load(clean_path)
    replaced = {
        (row["backend"], row["phase"], row["seed"], row["task"]["name"])
        for row in clean
    }
    rows = [
        row
        for row in rows
        if (row["backend"], row["phase"], row["seed"], row["task"]["name"])
        not in replaced
    ]
    return rows + clean


def ordinary_figure(path, stable, baseline):
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    baseline_index = defaultdict(list)
    stable_index = defaultdict(list)
    for row in baseline:
        if row.get("method") == "gemm" and "error" not in row:
            key = (row["backend"], row["phase"], row["task"]["name"])
            baseline_index[key].append(row)
    for row in stable:
        if "error" not in row:
            key = (row["backend"], row["phase"], row["task"]["name"])
            stable_index[key].append(row)

    fig, axes = plt.subplots(3, 1, figsize=(11, 9.2))
    width = 0.26
    xs = np.arange(len(TASKS))
    for ax, phase in zip(axes, PHASES):
        for index, backend in enumerate(BACKENDS):
            ratios = []
            for task in TASKS:
                key = (backend, phase, task)
                ratios.append(
                    mean(stable_index[key], "seconds")
                    / mean(baseline_index[key], "seconds")
                )
            ax.bar(
                xs + (index - 1) * width,
                ratios,
                width * 0.92,
                color=COLORS[backend],
                label=LABELS[backend],
            )
        ax.axhline(1, color="#333333", linewidth=0.8)
        ax.set_xticks(xs, TASKS)
        ax.set_ylabel("stable / GEMM time")
        ax.set_title(phase)
        ax.spines[["top", "right"]].set_visible(False)
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=3, frameon=False)
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    fig.savefig(path, metadata={"Date": None})
    plt.close(fig)


def translated_figure(path, rows, field, ylabel, log=False):
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    methods = ("gemm", "stable-1e-6", "stable-1e-2", "broadcast")
    styles = ("o-", "s--", "D-", "^-")
    offsets = (0.0, 10.0, 1000.0)
    fig, axes = plt.subplots(1, 3, figsize=(12, 3.8), sharey=True)
    for ax, backend in zip(axes, BACKENDS):
        for method, style in zip(methods, styles):
            ys = []
            for offset in offsets:
                selected = [
                    row
                    for row in rows
                    if row["backend"] == backend
                    and row["method"] == method
                    and row["offset"] == offset
                ]
                ys.append(mean(selected, field))
            ax.plot(range(3), ys, style, label=method)
        ax.set_xticks(range(3), ("0", "10", "1000"))
        ax.set_xlabel("translation offset")
        ax.set_title(LABELS[backend])
        ax.spines[["top", "right"]].set_visible(False)
        if log:
            ax.set_yscale("log")
    axes[0].set_ylabel(ylabel)
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=4, frameon=False)
    fig.tight_layout(rect=(0, 0.12, 1, 1))
    fig.savefig(path, metadata={"Date": None})
    plt.close(fig)


def threshold_figure(path, probes):
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    rows = [
        row
        for row in probes
        if row["kind"] == "distances"
        and row["dtype"] == "float32"
        and row["n_features"] == 32
        and row["offset"] == 1000.0
    ]
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.8))
    for backend in BACKENDS:
        selected = sorted(
            [row for row in rows if row["backend"] == backend],
            key=lambda row: row["threshold"],
        )
        thresholds = [row["threshold"] for row in selected]
        axes[0].plot(
            thresholds,
            [row["stable_label_errors"] for row in selected],
            "o-",
            label=LABELS[backend],
            color=COLORS[backend],
        )
        axes[1].plot(
            thresholds,
            [100 * row["recomputed_fraction"] for row in selected],
            "o-",
            label=LABELS[backend],
            color=COLORS[backend],
        )
    for ax in axes:
        ax.set_xscale("log")
        ax.set_xlabel("relative threshold")
        ax.spines[["top", "right"]].set_visible(False)
    axes[0].set_ylabel("wrong labels / 128")
    axes[1].set_ylabel("pairs recomputed (%)")
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=3, frameon=False)
    fig.tight_layout(rect=(0, 0.12, 1, 1))
    fig.savefig(path, metadata={"Date": None})
    plt.close(fig)


def ordinary_table(stable, baseline):
    base = defaultdict(list)
    new = defaultdict(list)
    for row in baseline:
        if row.get("method") == "gemm" and "error" not in row:
            base[(row["backend"], row["phase"], row["task"]["name"])].append(row)
    for row in stable:
        if "error" not in row:
            new[(row["backend"], row["phase"], row["task"]["name"])].append(row)
    lines = []
    for phase in PHASES:
        lines += [
            f"### {phase}: stable / GEMM time",
            "",
            "| backend | " + " | ".join(TASKS) + " |",
            "| --- |" + " ---: |" * len(TASKS),
        ]
        for backend in BACKENDS:
            cells = []
            for task in TASKS:
                key = (backend, phase, task)
                cells.append(
                    f"{mean(new[key], 'seconds') / mean(base[key], 'seconds'):.2f}x"
                )
            lines.append(f"| {LABELS[backend]} | " + " | ".join(cells) + " |")
        lines.append("")
    lines += [
        "### Stable recomputation rate",
        "",
        "| phase and backend | " + " | ".join(TASKS) + " |",
        "| --- |" + " ---: |" * len(TASKS),
    ]
    for phase in PHASES:
        for backend in BACKENDS:
            cells = []
            for task in TASKS:
                selected = new[(backend, phase, task)]
                fraction = sum(row["recomputed_pairs"] for row in selected) / sum(
                    row["distance_pairs"] for row in selected
                )
                cells.append(f"{fraction * 100:.5f}%")
            lines.append(
                f"| {phase}, {LABELS[backend]} | " + " | ".join(cells) + " |"
            )
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--stable", required=True)
    parser.add_argument("--stable-clean", required=True)
    parser.add_argument("--baseline", required=True)
    parser.add_argument("--probe", action="append", required=True)
    parser.add_argument("--translated", action="append", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    stable = ordinary_rows(args.stable, args.stable_clean)
    baseline = load(args.baseline)
    probes = [row for path in args.probe for row in load(path)]
    translated = [row for path in args.translated for row in load(path)]
    result = {
        "ordinary_stable": stable,
        "cancellation_probes": probes,
        "translated_assignment": translated,
    }
    (out / "results.json").write_text(json.dumps(result, indent=2) + "\n")
    ordinary_figure(out / "ordinary-overhead.svg", stable, baseline)
    translated_figure(
        out / "translated-time.svg",
        translated,
        "seconds",
        "assignment time (s)",
        log=True,
    )
    translated_figure(
        out / "translated-errors.svg",
        translated,
        "label_errors",
        "wrong labels / 100,000",
    )
    threshold_figure(out / "threshold-sensitivity.svg", probes)
    (out / "tables.md").write_text(ordinary_table(stable, baseline))


if __name__ == "__main__":
    main()
