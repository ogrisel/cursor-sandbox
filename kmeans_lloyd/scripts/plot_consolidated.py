"""Plot and tabulate initializer, Lloyd-only, and full-fit k-means results."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

TASKS = ["k3-d1000", "k17-d180", "k100-d32", "k550-d6", "k3000-d2"]
BACKENDS = {
    "torch-cpu": "Array API - Torch CPU",
    "torch-cuda": "Array API - Torch CUDA",
    "cupy": "Array API - CuPy",
    "sklearn-vanilla": "scikit-learn 1.7.2",
    "sklearn-optimized": "scikit-learn PRs 23+26",
    "cuml": "cuML 26.10",
    "shared": "shared random rows",
}
COLOR = {
    "torch-cpu": "#4C78A8",
    "torch-cuda": "#E45756",
    "cupy": "#B279A2",
    "sklearn-vanilla": "#F58518",
    "sklearn-optimized": "#54A24B",
    "cuml": "#72B7B2",
    "shared": "#8C8C8C",
}
INIT = {"plusplus": "greedy", "scalable": "scalable", "random": "random rows"}
HATCH = {"plusplus": "", "scalable": "///", "random": "..."}
API = ("torch-cpu", "torch-cuda", "cupy")
OTHERS = ("sklearn-vanilla", "sklearn-optimized", "cuml")


def series_key(row):
    """Return ``(phase, backend, relocation, init)`` or None for retired rows."""
    impl = row["impl"]
    if "error" in row or impl.endswith("-reassign"):
        return None
    phase = row.get("phase", "fit")
    if impl == "random-baseline":
        return phase, "shared", None, "random"
    backend = next(
        name for name in ("torch-cpu", "torch-cuda", "cupy", "sklearn-vanilla", "sklearn-optimized", "cuml")
        if impl.startswith(name)
    )
    relocation = None
    if impl.endswith("-keep"):
        relocation = "keep"
    elif impl.endswith("-farthest"):
        relocation = "farthest"
    return phase, backend, relocation, row["init"]


def label(key):
    _phase, backend, relocation, init = key
    text = BACKENDS[backend]
    if backend != "shared":
        text += f", {INIT[init]}"
    if relocation == "keep":
        text += ", keep empty"
    return text


def value(row, field):
    # cuML exposes no standalone random initializer, so its duration is the
    # zero-iteration fit; it is never plotted as an initializer cost.
    if field == "seconds" and row["impl"] == "cuml-random":
        return row["fit_seconds"]
    return row.get(field)


def stats(rows, key, task, field):
    values = [
        value(row, field)
        for row in rows
        if series_key(row) == key and row["task"]["name"] == task and value(row, field) is not None
    ]
    if not values:
        return np.nan, np.nan, 0
    std = float(np.std(values, ddof=1)) if len(values) > 1 else 0.0
    return float(np.mean(values)), std, len(values)


def best_means(rows, keys, field="inertia_per_point"):
    return {task: np.nanmin([stats(rows, key, task, field)[0] for key in keys]) for task in TASKS}


def bars(ax, rows, keys, field, scale=None):
    width = 0.9 / len(keys)
    xs = np.arange(len(TASKS))
    for index, key in enumerate(keys):
        means, errors = [], []
        positions = xs + (index - (len(keys) - 1) / 2) * width
        for position, task in zip(positions, TASKS):
            mean, std, count = stats(rows, key, task, field)
            divisor = scale[task] if scale else 1.0
            means.append(mean / divisor)
            errors.append(std / divisor)
            if not count and timed_out(rows, key, task):
                ax.text(
                    position, 0.02, "timeout", rotation=90, fontsize=7, ha="center",
                    va="bottom", color="#333333", transform=ax.get_xaxis_transform(),
                )
        ax.bar(
            positions,
            means,
            yerr=errors,
            width=width * 0.94,
            color=COLOR[key[1]],
            hatch=HATCH[key[3]],
            edgecolor="white",
            linewidth=0,
            label=label(key),
            error_kw={"elinewidth": 0.7, "capsize": 1},
        )
    ax.set_xticks(xs, TASKS)
    ax.spines[["top", "right"]].set_visible(False)


def uses_log_scale(rows, keys, field, scale=None):
    """Use a log axis when positive values span at least a factor of ten."""
    values = []
    for key in keys:
        for task in TASKS:
            mean, _std, count = stats(rows, key, task, field)
            if count and mean > 0:
                values.append(mean / (scale[task] if scale else 1.0))
    return bool(values) and max(values) / min(values) >= 10


def figure(path, rows, keys, field, title, ylabel, scale=None, log=False, reference=False):
    import matplotlib.pyplot as plt

    plt.rcParams["hatch.color"] = "white"
    fig, ax = plt.subplots(figsize=(14, 5.6))
    bars(ax, rows, keys, field, scale=scale)
    if log:
        ax.set_yscale("log")
    if reference:
        ax.axhline(1.0, color="black", linewidth=0.7, linestyle=":")
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.legend(frameon=False, fontsize=8, ncol=4, loc="upper center", bbox_to_anchor=(0.5, -0.07))
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def table(rows, keys, field, fmt, scale=None, header="configuration"):
    lines = [
        f"| {header} | " + " | ".join(TASKS) + " |",
        "| --- |" + " --- |" * len(TASKS),
    ]
    for key in keys:
        cells = []
        for task in TASKS:
            mean, _std, count = stats(rows, key, task, field)
            if not count:
                cells.append("timeout" if timed_out(rows, key, task) else "n/a")
            else:
                cells.append(fmt(mean / (scale[task] if scale else 1.0)))
        lines.append(f"| {label(key)} | " + " | ".join(cells) + " |")
    return "\n".join(lines)


def timed_out(rows, key, task):
    for row in rows:
        if "error" not in row or row["task"]["name"] != task:
            continue
        candidate = dict(row, error=None)
        candidate.pop("error")
        if series_key(candidate) == key:
            return True
    return False


def init_keys(rows, include_random):
    keys = []
    for backend in API + OTHERS:
        for init in ("plusplus", "scalable"):
            key = ("init", backend, None, init)
            if any(series_key(row) == key for row in rows):
                keys.append(key)
    if include_random:
        keys += [("init", "cuml", None, "random"), ("init", "shared", None, "random")]
    return keys


def fit_keys(inits, relocations=("farthest",)):
    keys = []
    for backend in API:
        for relocation in relocations:
            keys += [("fit", backend, relocation, init) for init in inits]
    for backend in OTHERS:
        for init in inits:
            if init == "scalable" and backend.startswith("sklearn"):
                continue
            keys.append(("fit", backend, None, init))
    return keys


def seconds(x):
    return f"{x:.2f} s"


def mebibytes(x):
    return f"{x / 2**20:.0f} MiB"


def ratio(x):
    return f"{x:.4f}"


def plot_init(rows, out, prefix=""):
    timed = init_keys(rows, include_random=False)
    quality = init_keys(rows, include_random=True)
    best = best_means(rows, quality)
    figure(
        out / f"{prefix}duration.svg", rows, timed, "seconds",
        "Initialization only: duration, mean and sample std over three seeds", "seconds",
        log=uses_log_scale(rows, timed, "seconds"),
    )
    figure(
        out / f"{prefix}memory.svg", rows, timed, "mem_increment_bytes",
        "Initialization only: peak memory increment", "bytes",
        log=uses_log_scale(rows, timed, "mem_increment_bytes"),
    )
    figure(
        out / f"{prefix}quality.svg", rows, quality, "inertia_per_point",
        "Initialization only: inertia / best mean for the same task",
        "inertia / best initializer mean", scale=best, reference=True,
        log=uses_log_scale(rows, quality, "inertia_per_point", best),
    )
    return timed, quality, best


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--tables", help="write markdown tables to this file")
    args = parser.parse_args()
    import matplotlib

    matplotlib.use("Agg")

    rows = json.loads(Path(args.results).read_text())
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    timed, quality, init_best = plot_init(rows, out, prefix="init-")

    lloyd = fit_keys(("random",))
    full = fit_keys(("plusplus", "scalable"))
    lloyd_tables = fit_keys(("random",), relocations=("keep", "farthest"))
    full_tables = fit_keys(("plusplus", "scalable"), relocations=("keep", "farthest"))
    lloyd_best = best_means(rows, lloyd_tables)
    fit_best = best_means(rows, full_tables)
    for name, keys, title, best, quality_label in (
        (
            "lloyd",
            lloyd,
            "Lloyd only from shared random rows (12 iterations)",
            lloyd_best,
            "best Lloyd-only mean",
        ),
        (
            "fit",
            full,
            "Full fit: initialization plus 12 Lloyd iterations",
            fit_best,
            "best full-fit mean",
        ),
    ):
        figure(
            out / f"{name}-duration.svg", rows, keys, "seconds", f"{title}: duration", "seconds",
            log=uses_log_scale(rows, keys, "seconds"),
        )
        figure(
            out / f"{name}-memory.svg", rows, keys, "mem_increment_bytes",
            f"{title}: peak memory increment", "bytes",
            log=uses_log_scale(rows, keys, "mem_increment_bytes"),
        )
        figure(
            out / f"{name}-quality.svg", rows, keys, "inertia_per_point",
            f"{title}: inertia / best mean for the same task",
            f"inertia / {quality_label}",
            scale=best,
            log=uses_log_scale(rows, keys, "inertia_per_point", best),
            reference=True,
        )

    if args.tables:
        sections = [
            ("init-seconds", table(rows, timed, "seconds", seconds)),
            ("init-memory", table(rows, timed, "mem_increment_bytes", mebibytes)),
            ("init-quality", table(rows, quality, "inertia_per_point", ratio, scale=init_best)),
            ("lloyd-seconds", table(rows, lloyd_tables, "seconds", seconds)),
            ("lloyd-memory", table(rows, lloyd_tables, "mem_increment_bytes", mebibytes)),
            ("lloyd-quality", table(rows, lloyd_tables, "inertia_per_point", ratio, scale=lloyd_best)),
            ("fit-seconds", table(rows, full_tables, "seconds", seconds)),
            ("fit-memory", table(rows, full_tables, "mem_increment_bytes", mebibytes)),
            ("fit-quality", table(rows, full_tables, "inertia_per_point", ratio, scale=fit_best)),
            (
                "best",
                "\n".join(
                    f"{task}: init {init_best[task]:.6g}, "
                    f"Lloyd {lloyd_best[task]:.6g}, full fit {fit_best[task]:.6g}"
                    for task in TASKS
                ),
            ),
        ]
        Path(args.tables).write_text(
            "\n\n".join(f"<!-- {name} -->\n{text}" for name, text in sections) + "\n"
        )
    print(f"wrote consolidated plots for {len(rows)} rows")


if __name__ == "__main__":
    main()
