"""Plot and tabulate the ``kmeans_lloyd.KMeans`` task-mix benchmark."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

TASKS = ["k3-d1000", "k17-d180", "k100-d32", "k550-d6", "k3000-d2"]
LABEL = {
    "torch-cpu": "Array API - Torch CPU",
    "torch-cpu-generic": "Array API - Torch CPU, generic update",
    "torch-cuda": "Array API - Torch CUDA",
    "torch-cuda-generic": "Array API - Torch CUDA, generic update",
    "cupy": "Array API - CuPy",
    "cupy-generic": "Array API - CuPy, generic update",
    "sklearn-vanilla": "scikit-learn 1.7.2",
    "sklearn-optimized": "scikit-learn PRs 23+26",
    "cuml": "cuML 26.10",
    "cuml-plusplus": "cuML 26.10",
    "cuml-scalable": "cuML 26.10, scalable",
    "random-baseline": "shared random rows",
}
COLOR = {
    "torch-cpu": "#4C78A8",
    "torch-cuda": "#E45756",
    "cupy": "#B279A2",
    "sklearn-vanilla": "#F58518",
    "sklearn-optimized": "#54A24B",
    "cuml": "#72B7B2",
    "random-baseline": "#8C8C8C",
}
FIT_IMPLS = (
    "torch-cpu",
    "torch-cpu-generic",
    "torch-cuda",
    "torch-cuda-generic",
    "cupy",
    "cupy-generic",
    "sklearn-vanilla",
    "sklearn-optimized",
    "cuml",
)
INIT_IMPLS = (
    "torch-cpu",
    "torch-cuda",
    "cupy",
    "sklearn-vanilla",
    "sklearn-optimized",
    "cuml-plusplus",
    "cuml-scalable",
)


def _color(impl):
    return COLOR[next(name for name in COLOR if impl.startswith(name))]


def load(path):
    text = Path(path).read_text()
    if Path(path).suffix == ".json":
        return json.loads(text)
    return [json.loads(line) for line in text.splitlines() if line.strip()]


def stats(rows, impl, init, task, field):
    values = [
        row[field]
        for row in rows
        if "error" not in row
        and row["impl"] == impl
        and row["init"] == init
        and row["task"]["name"] == task
        and row.get(field) is not None
    ]
    if not values:
        return np.nan, np.nan, 0
    std = float(np.std(values, ddof=1)) if len(values) > 1 else 0.0
    return float(np.mean(values)), std, len(values)


def failures(rows, impl, init, task):
    return [
        row["error"]
        for row in rows
        if "error" in row and row["impl"] == impl and row["init"] == init and row["task"]["name"] == task
    ]


def uses_log_scale(values):
    positive = [v for v in values if np.isfinite(v) and v > 0]
    return bool(positive) and max(positive) / min(positive) >= 10


def panel(ax, rows, series, field, title, ylabel, scale=None):
    width = 0.9 / len(series)
    xs = np.arange(len(TASKS))
    plotted = []
    for index, (impl, init) in enumerate(series):
        positions = xs + (index - (len(series) - 1) / 2) * width
        means, errors = [], []
        for position, task in zip(positions, TASKS):
            mean, std, count = stats(rows, impl, init, task, field)
            divisor = scale[task] if scale else 1.0
            means.append(mean / divisor)
            errors.append(std / divisor)
            if not count and failures(rows, impl, init, task):
                ax.text(
                    position, 0.02, failures(rows, impl, init, task)[0], rotation=90,
                    fontsize=6, ha="center", va="bottom", color="#333333",
                    transform=ax.get_xaxis_transform(),
                )
        plotted += means
        generic = impl.endswith("-generic")
        scalable = init == "scalable"
        ax.bar(
            positions,
            means,
            yerr=errors,
            width=width * 0.94,
            color=_color(impl),
            alpha=0.45 if generic else 0.7 if scalable else 1.0,
            hatch="///" if generic else "..." if scalable else "",
            edgecolor="white",
            linewidth=0,
            label=LABEL[impl] if not impl.startswith("cuml") or init != "scalable" else LABEL["cuml-scalable"],
            error_kw={"elinewidth": 0.7, "capsize": 1},
        )
    if scale:
        ax.axhline(1.0, color="#333333", linewidth=0.7)
    if uses_log_scale(plotted):
        ax.set_yscale("log")
    ax.set_xticks(xs, TASKS)
    ax.set_title(title, fontsize=10)
    ax.set_ylabel(ylabel)
    ax.spines[["top", "right"]].set_visible(False)


def best(rows, series, field="inertia_per_point"):
    result = {}
    for task in TASKS:
        values = [stats(rows, impl, init, task, field)[0] for impl, init in series]
        finite = [v for v in values if np.isfinite(v)]
        result[task] = min(finite) if finite else np.nan
    return result


def figure(path, rows, panels, field, ylabel, quality=False):
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(len(panels), 1, figsize=(11, 3.6 * len(panels)), squeeze=False)
    for ax, (title, series) in zip(axes[:, 0], panels):
        scale = best(rows, series) if quality else None
        panel(ax, rows, series, field, title, ylabel, scale=scale)
    seen = {}
    for panel_ax in axes[:, 0]:
        for handle, text in zip(*panel_ax.get_legend_handles_labels()):
            seen.setdefault(text, handle)
    fig.legend(list(seen.values()), list(seen.keys()), loc="lower center", ncol=3, fontsize=8, frameon=False)
    fig.tight_layout(rect=(0, 0.1, 1, 1))
    fig.savefig(path, metadata={"Date": None})
    plt.close(fig)


def fmt_seconds(mean, std, count, errors):
    if not count:
        return errors[0] if errors else "–"
    return f"{mean:.2f} ± {std:.2f} s"


def table(rows, series, field="seconds"):
    lines = ["| implementation | " + " | ".join(TASKS) + " |", "| --- |" + " ---: |" * len(TASKS)]
    for impl, init in series:
        name = LABEL["cuml-scalable"] if impl == "cuml" and init == "scalable" else LABEL[impl]
        cells = []
        for task in TASKS:
            mean, std, count = stats(rows, impl, init, task, field)
            if field == "seconds":
                cells.append(fmt_seconds(mean, std, count, failures(rows, impl, init, task)))
            elif field == "mem_increment_bytes":
                cells.append(f"{mean / 2**20:.0f} MiB" if count else "–")
            else:
                cells.append(f"{mean:.4g}" if count else "–")
        lines.append(f"| {name} | " + " | ".join(cells) + " |")
    return "\n".join(lines)


def quality_table(rows, series):
    scale = best(rows, series)
    lines = ["| implementation | " + " | ".join(TASKS) + " |", "| --- |" + " ---: |" * len(TASKS)]
    for impl, init in series:
        name = LABEL["cuml-scalable"] if impl == "cuml" and init == "scalable" else LABEL[impl]
        cells = []
        for task in TASKS:
            mean, _std, count = stats(rows, impl, init, task, "inertia_per_point")
            cells.append(f"{mean / scale[task]:.4f}" if count else "–")
        lines.append(f"| {name} | " + " | ".join(cells) + " |")
    return "\n".join(lines)


def speedups(rows, init):
    lines = [
        "| backend | " + " | ".join(TASKS) + " |",
        "| --- |" + " ---: |" * len(TASKS),
    ]
    for backend in ("torch-cpu", "torch-cuda", "cupy"):
        cells = []
        for task in TASKS:
            native = stats(rows, backend, init, task, "seconds")[0]
            generic = stats(rows, backend + "-generic", init, task, "seconds")[0]
            cells.append(f"{generic / native:.2f}x" if np.isfinite(native) and np.isfinite(generic) else "–")
        lines.append(f"| {LABEL[backend]} | " + " | ".join(cells) + " |")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--fit", required=True)
    parser.add_argument("--init", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    fit = load(args.fit)
    init = load(args.init)
    greedy = [(impl, "plusplus") for impl in FIT_IMPLS] + [("cuml", "scalable")]
    shared = [(impl, "random") for impl in FIT_IMPLS]
    fit_panels = [
        ("k-means++ initialization + 12 Lloyd iterations", greedy),
        ("shared random-row start + 12 Lloyd iterations", shared),
    ]
    init_series = [(impl, "scalable" if impl == "cuml-scalable" else "plusplus") for impl in INIT_IMPLS]
    init_panels = [("initialization only", init_series)]
    figure(out / "fit-duration.svg", fit, fit_panels, "seconds", "seconds")
    figure(out / "fit-memory.svg", fit, fit_panels, "mem_increment_bytes", "peak extra bytes")
    figure(out / "fit-quality.svg", fit, fit_panels, "inertia_per_point", "inertia / best", quality=True)
    quality_init = init_series + [("random-baseline", "random")]
    figure(out / "init-duration.svg", init, init_panels, "seconds", "seconds")
    figure(out / "init-memory.svg", init, init_panels, "mem_increment_bytes", "peak extra bytes")
    figure(
        out / "init-quality.svg", init, [("initialization only", quality_init)],
        "inertia_per_point", "inertia / best", quality=True,
    )
    sections = {
        "fit duration, k-means++": table(fit, greedy),
        "fit duration, shared random start": table(fit, shared),
        "fit quality, k-means++": quality_table(fit, greedy),
        "fit quality, shared random start": quality_table(fit, shared),
        "fit memory, k-means++": table(fit, greedy, "mem_increment_bytes"),
        "native speedup over generic, k-means++": speedups(fit, "plusplus"),
        "native speedup over generic, shared random start": speedups(fit, "random"),
        "init duration": table(init, init_series),
        "init quality": quality_table(init, quality_init),
    }
    text = "\n\n".join(f"### {name}\n\n{body}" for name, body in sections.items())
    (out / "tables.md").write_text(text + "\n")
    print(text)


if __name__ == "__main__":
    main()
