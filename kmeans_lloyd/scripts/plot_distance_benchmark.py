"""Plot and tabulate GEMM versus broadcast KMeans distance benchmarks."""

from __future__ import annotations

import argparse
import json
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
    text = Path(path).read_text()
    if Path(path).suffix == ".json":
        return json.loads(text)
    return [json.loads(line) for line in text.splitlines() if line.strip()]


def values(rows, phase, backend, method, task, field):
    return [
        row[field]
        for row in rows
        if "error" not in row
        and row["phase"] == phase
        and row["backend"] == backend
        and row["method"] == method
        and row["task"]["name"] == task
    ]


def errors(rows, phase, backend, method, task):
    return [
        row
        for row in rows
        if "error" in row
        and row["phase"] == phase
        and row["backend"] == backend
        and row["method"] == method
        and row["task"]["name"] == task
    ]


def mean_std(samples):
    if not samples:
        return np.nan, np.nan
    std = np.std(samples, ddof=1) if len(samples) > 1 else 0.0
    return float(np.mean(samples)), float(std)


def ratio(rows, phase, backend, task, field):
    gemm = values(rows, phase, backend, "gemm", task, field)
    broadcast = values(rows, phase, backend, "broadcast", task, field)
    gemm_mean, _ = mean_std(gemm)
    broadcast_mean, _ = mean_std(broadcast)
    if np.isfinite(gemm_mean) and np.isfinite(broadcast_mean):
        return broadcast_mean / gemm_mean, False
    failed = errors(rows, phase, backend, "broadcast", task)
    if field == "seconds" and np.isfinite(gemm_mean) and failed:
        return min(row.get("timeout_seconds", 60) for row in failed) / gemm_mean, True
    return np.nan, False


def impact_figure(path, rows, field, ylabel, percent_delta=False):
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(3, 1, figsize=(11, 9.2), squeeze=False)
    width = 0.26
    xs = np.arange(len(TASKS))
    for ax, phase in zip(axes[:, 0], PHASES):
        all_values = []
        for index, backend in enumerate(BACKENDS):
            positions = xs + (index - 1) * width
            pairs = [ratio(rows, phase, backend, task, field) for task in TASKS]
            means = [
                (pair[0] - 1) * 100
                if percent_delta and np.isfinite(pair[0])
                else pair[0]
                for pair in pairs
            ]
            all_values += [value for value in means if np.isfinite(value)]
            bars = ax.bar(
                positions,
                means,
                width=width * 0.92,
                color=COLORS[backend],
                label=LABELS[backend],
                edgecolor="white",
                linewidth=0,
            )
            for bar, (value, lower_bound) in zip(bars, pairs):
                if lower_bound:
                    bar.set_hatch("///")
                    ax.text(
                        bar.get_x() + bar.get_width() / 2,
                        value,
                        ">",
                        ha="center",
                        va="bottom",
                        fontsize=9,
                    )
        ax.axhline(0 if percent_delta else 1, color="#333333", linewidth=0.8)
        ax.set_xticks(xs, TASKS)
        ax.set_ylabel(ylabel)
        ax.set_title(
            {
                "init": "greedy k-means++ initialization",
                "lloyd": "12 Lloyd iterations from shared random rows",
                "fit": "k-means++ + 12 Lloyd iterations",
            }[phase],
            fontsize=10,
        )
        ax.spines[["top", "right"]].set_visible(False)
        positive = [value for value in all_values if value > 0]
        if (
            not percent_delta
            and positive
            and max(positive) / min(positive) >= 10
        ):
            ax.set_yscale("log")
    handles, labels = axes[0, 0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=3, frameon=False)
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    fig.savefig(path, metadata={"Date": None})
    plt.close(fig)


def raw_table(rows, phase, field, unit):
    lines = [
        "| backend and method | " + " | ".join(TASKS) + " |",
        "| --- |" + " ---: |" * len(TASKS),
    ]
    for backend in BACKENDS:
        for method in ("gemm", "broadcast"):
            cells = []
            for task in TASKS:
                samples = values(rows, phase, backend, method, task, field)
                mean, std = mean_std(samples)
                failed = errors(rows, phase, backend, method, task)
                if np.isfinite(mean):
                    if field == "mem_increment_bytes":
                        cells.append(f"{mean / 2**20:.0f} MiB")
                    elif field == "inertia_per_point":
                        cells.append(f"{mean:.6g}")
                    else:
                        cells.append(f"{mean:.2f} ± {std:.2f} s")
                elif failed:
                    if field == "seconds":
                        cells.append(
                            f">{failed[0].get('timeout_seconds', 60)} s"
                        )
                    else:
                        cells.append("timeout")
                else:
                    cells.append("–")
            lines.append(
                f"| {LABELS[backend]}, {method} | " + " | ".join(cells) + " |"
            )
    return "\n".join(lines)


def ratio_table(rows, phase, field):
    lines = [
        "| backend | " + " | ".join(TASKS) + " |",
        "| --- |" + " ---: |" * len(TASKS),
    ]
    for backend in BACKENDS:
        cells = []
        for task in TASKS:
            value, lower_bound = ratio(rows, phase, backend, task, field)
            marker = ">" if lower_bound else ""
            digits = 6 if field == "inertia_per_point" else 2
            cells.append(
                f"{marker}{value:.{digits}f}x" if np.isfinite(value) else "–"
            )
        lines.append(f"| {LABELS[backend]} | " + " | ".join(cells) + " |")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    rows = load(args.input)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    impact_figure(out / "duration-impact.svg", rows, "seconds", "broadcast / GEMM time")
    impact_figure(
        out / "memory-impact.svg",
        rows,
        "mem_increment_bytes",
        "broadcast / GEMM peak memory",
    )
    impact_figure(
        out / "quality-impact.svg",
        rows,
        "inertia_per_point",
        "broadcast inertia change (%)",
        percent_delta=True,
    )
    sections = []
    for phase in PHASES:
        for field, title, unit in (
            ("seconds", "duration", "s"),
            ("mem_increment_bytes", "peak memory", "MiB"),
            ("inertia_per_point", "quality", ""),
        ):
            sections.append(
                f"### {phase}: {title}\n\n{raw_table(rows, phase, field, unit)}"
            )
            sections.append(
                f"### {phase}: broadcast / GEMM {title}\n\n"
                f"{ratio_table(rows, phase, field)}"
            )
    text = "\n\n".join(sections) + "\n"
    (out / "tables.md").write_text(text)
    print(text)


if __name__ == "__main__":
    main()
