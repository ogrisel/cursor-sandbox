"""Tables and figures for the CPU and GPU optimization rerun (journal 019)."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

import numpy as np

TASKS = ("k3-d1000", "k17-d180", "k100-d32", "k550-d6", "k3000-d2")
PHASES = ("init", "lloyd", "fit")
BACKENDS = ("torch-cpu", "torch-cuda", "cupy")
BACKEND_LABELS = {
    "torch-cpu": "Torch CPU",
    "torch-cuda": "Torch CUDA",
    "cupy": "CuPy CUDA",
}
METHODS = {
    "init": ("baseline", "homogeneous"),
    "lloyd": ("legacy", "baseline", "interleaved-tuned", "homogeneous-lloyd"),
    "fit": ("legacy", "baseline", "homogeneous", "homogeneous-lloyd"),
}
# Initialization never used the winning-score gather, so the labels-only
# baseline is also the previous implementation for that phase.
REFERENCE = {"init": "baseline", "lloyd": "legacy", "fit": "legacy"}
LABELS = {
    "legacy": "previous",
    "baseline": "labels-only",
    "interleaved-tuned": "interleaved",
    "homogeneous": "augmented init + Lloyd",
    "homogeneous-lloyd": "augmented Lloyd",
}
INIT_LABELS = {"baseline": "previous", "homogeneous": "augmented init"}
COLORS = {
    "legacy": "#9D9D9D",
    "baseline": "#4C78A8",
    "interleaved-tuned": "#F2CF5B",
    "homogeneous": "#E45756",
    "homogeneous-lloyd": "#72B7B2",
}


def label(phase, method):
    return INIT_LABELS[method] if phase == "init" else LABELS[method]


def load(path):
    return [
        json.loads(line)
        for line in Path(path).read_text().splitlines()
        if line.strip()
    ]


def group(rows):
    groups = defaultdict(list)
    for row in rows:
        if "error" in row:
            continue
        key = (row["backend"], row["phase"], row["method"], row["task"]["name"])
        groups[key].append(row)
    return groups


def stat(groups, key, field):
    values = [row[field] for row in groups.get(key, [])]
    if not values:
        return float("nan"), float("nan"), 0
    return float(np.mean(values)), float(np.std(values)), len(values)


def cakedev0(rows):
    groups = defaultdict(list)
    for row in rows:
        if "error" in row or row.get("impl") != "sklearn-optimized":
            continue
        if row["phase"] == "init":
            phase = "init"
        else:
            phase = "lloyd" if row["init"] == "random" else "fit"
        groups[(phase, row["task"]["name"])].append(row)
    return groups


def _figure(path, groups, field, ylabel):
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(
        len(PHASES), len(BACKENDS), figsize=(16, 9), sharey="row"
    )
    xs = np.arange(len(TASKS))
    for row_index, phase in enumerate(PHASES):
        methods = METHODS[phase]
        width = 0.8 / len(methods)
        for col_index, backend in enumerate(BACKENDS):
            ax = axes[row_index, col_index]
            for index, method in enumerate(methods):
                values = []
                for task in TASKS:
                    ref = stat(
                        groups, (backend, phase, REFERENCE[phase], task), field
                    )[0]
                    value = stat(groups, (backend, phase, method, task), field)[0]
                    values.append(value / ref if ref else np.nan)
                ax.bar(
                    xs + (index - (len(methods) - 1) / 2) * width,
                    values,
                    width * 0.92,
                    color=COLORS[method],
                    label=label(phase, method),
                )
            ax.axhline(1, color="#333333", linewidth=0.8)
            ax.set_xticks(xs, TASKS, rotation=20, fontsize=8)
            ax.set_title(f"{phase}, {BACKEND_LABELS[backend]}", fontsize=10)
            ax.spines[["top", "right"]].set_visible(False)
            if col_index == 0:
                ax.set_ylabel(ylabel)
        handles, labels = axes[row_index, 0].get_legend_handles_labels()
        axes[row_index, -1].legend(
            handles,
            labels,
            fontsize=8,
            frameon=False,
            loc="center left",
            bbox_to_anchor=(1.02, 0.5),
        )
    fig.tight_layout()
    fig.savefig(path, metadata={"Date": None})
    plt.close(fig)


def quality_figure(path, groups):
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, len(PHASES), figsize=(14, 4))
    markers = {"torch-cpu": "o", "torch-cuda": "s", "cupy": "^"}
    for ax, phase in zip(axes, PHASES):
        for backend in BACKENDS:
            for method in METHODS[phase]:
                if method == REFERENCE[phase]:
                    continue
                values = []
                for task in TASKS:
                    ref = stat(
                        groups,
                        (backend, phase, REFERENCE[phase], task),
                        "inertia_per_point",
                    )[0]
                    value = stat(
                        groups, (backend, phase, method, task), "inertia_per_point"
                    )[0]
                    values.append(100 * (value / ref - 1))
                ax.plot(
                    range(len(TASKS)),
                    values,
                    marker=markers[backend],
                    linestyle="-",
                    color=COLORS[method],
                    alpha=0.85,
                    label=f"{label(phase, method)}, {BACKEND_LABELS[backend]}",
                )
        ax.axhline(0, color="#333333", linewidth=0.8)
        ax.set_xticks(range(len(TASKS)), TASKS, rotation=20, fontsize=8)
        ax.set_title(phase)
        ax.spines[["top", "right"]].set_visible(False)
        ax.legend(fontsize=6, frameon=False)
    axes[0].set_ylabel("mean inertia change from previous (%)")
    fig.tight_layout()
    fig.savefig(path, metadata={"Date": None})
    plt.close(fig)


def _table(lines, title, header, rows):
    lines += [f"### {title}", "", "| " + " | ".join(header) + " |"]
    lines.append("| --- |" + " ---: |" * (len(header) - 1))
    lines += ["| " + " | ".join(row) + " |" for row in rows]
    lines.append("")


def tables(groups, cake):
    lines = []
    for backend in BACKENDS:
        for phase in PHASES:
            rows = []
            for method in METHODS[phase]:
                cells = []
                for task in TASKS:
                    mean, std, count = stat(
                        groups, (backend, phase, method, task), "seconds"
                    )
                    cells.append(f"{mean:.3f} ± {std:.3f}" if count else "—")
                rows.append([label(phase, method)] + cells)
            _table(
                lines,
                f"{BACKEND_LABELS[backend]}, {phase}: seconds",
                ["method", *TASKS],
                rows,
            )

    rows = []
    for backend in BACKENDS:
        for phase in PHASES:
            for method in METHODS[phase]:
                if method == REFERENCE[phase]:
                    continue
                cells = []
                for task in TASKS:
                    ref = stat(groups, (backend, phase, REFERENCE[phase], task), "seconds")[0]
                    value = stat(groups, (backend, phase, method, task), "seconds")[0]
                    cells.append(f"{ref / value:.2f}x")
                rows.append(
                    [f"{BACKEND_LABELS[backend]}, {phase}, {label(phase, method)}"]
                    + cells
                )
    _table(lines, "Speedup over the previous implementation", ["row", *TASKS], rows)

    rows = []
    for backend in BACKENDS:
        for phase in PHASES:
            for method in METHODS[phase]:
                cells = []
                for task in TASKS:
                    value = stat(
                        groups, (backend, phase, method, task), "mem_increment_bytes"
                    )[0]
                    cells.append(f"{value / 2**20:.0f}")
                rows.append(
                    [f"{BACKEND_LABELS[backend]}, {phase}, {label(phase, method)}"]
                    + cells
                )
    _table(lines, "Peak memory increment (MiB)", ["row", *TASKS], rows)

    rows = []
    for backend in BACKENDS:
        for phase in PHASES:
            for method in METHODS[phase]:
                if method == REFERENCE[phase]:
                    continue
                cells = []
                for task in TASKS:
                    ref = stat(
                        groups,
                        (backend, phase, REFERENCE[phase], task),
                        "inertia_per_point",
                    )[0]
                    value = stat(
                        groups, (backend, phase, method, task), "inertia_per_point"
                    )[0]
                    cells.append(f"{100 * (value / ref - 1):+.3f}%")
                rows.append(
                    [f"{BACKEND_LABELS[backend]}, {phase}, {label(phase, method)}"]
                    + cells
                )
    _table(lines, "Mean inertia change from previous", ["row", *TASKS], rows)

    rows = []
    for phase in PHASES:
        cake_cells = []
        for task in TASKS:
            values = [row["seconds"] for row in cake.get((phase, task), [])]
            cake_cells.append(f"{np.mean(values):.3f}" if values else "—")
        rows.append([f"cakedev0 seconds, {phase}"] + cake_cells)
        for backend in BACKENDS:
            for method in (REFERENCE[phase], *[
                m for m in METHODS[phase] if m.startswith("homogeneous")
            ]):
                cells = []
                for task in TASKS:
                    values = [row["seconds"] for row in cake.get((phase, task), [])]
                    value = stat(groups, (backend, phase, method, task), "seconds")[0]
                    cells.append(f"{value / np.mean(values):.2f}x" if values else "—")
                rows.append(
                    [f"{BACKEND_LABELS[backend]} {label(phase, method)} / cakedev0, {phase}"]
                    + cells
                )
    _table(
        lines,
        "Same-host comparison with cakedev0 (time / cakedev0 time)",
        ["row", *TASKS],
        rows,
    )
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", required=True)
    parser.add_argument("--cakedev0", action="append", required=True)
    parser.add_argument("--reruns", help="rows that replace whole noisy cells")
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    rows = load(args.results)
    replaced = []
    if args.reruns:
        reruns = load(args.reruns)
        cells = set(group(reruns))

        def cell(row):
            return (row["backend"], row["phase"], row["method"], row["task"]["name"])

        replaced = [row for row in rows if cell(row) in cells]
        rows = [row for row in rows if cell(row) not in cells] + reruns
    cake_rows = [row for path in args.cakedev0 for row in load(path)]
    (out / "results.json").write_text(
        json.dumps(
            {
                "optimizations": rows,
                "replaced_first_run": replaced,
                "cakedev0": cake_rows,
            },
            indent=1,
        )
        + "\n"
    )
    groups = group(rows)
    _figure(out / "time-ratios.svg", groups, "seconds", "time / previous")
    _figure(
        out / "memory-ratios.svg",
        groups,
        "mem_increment_bytes",
        "peak memory / previous",
    )
    quality_figure(out / "quality-impact.svg", groups)
    (out / "tables.md").write_text(tables(groups, cakedev0(cake_rows)))


if __name__ == "__main__":
    main()
