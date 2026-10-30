"""Plot peak memory and runtime from journal results.json files."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
JOURNAL = ROOT / "journal"


def _mib(value):
    if value is None:
        return None
    return value / (1024 * 1024)


def _load(folder):
    path = JOURNAL / folder / "results.json"
    return json.loads(path.read_text())


def _paired_bars(path, title, rows, ylabel, log=False):
    labels = [row[0] for row in rows]
    eager = [row[1] for row in rows]
    other = [row[2] for row in rows]
    positions = range(len(labels))
    width = 0.38
    fig, ax = plt.subplots(figsize=(10.5, 4.8))
    ax.bar([p - width / 2 for p in positions], eager, width, label="eager", color="#8c3a2f")
    ax.bar([p + width / 2 for p in positions], other, width, label="compiled or fused", color="#2f5d50")
    ax.set_xticks(list(positions), labels, rotation=25, ha="right")
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    if log:
        ax.set_yscale("log")
    ax.legend(frameon=False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=140)
    plt.close(fig)
    print(path)


def plot_probe():
    data = _load("001-fusion-probe")
    wanted = [
        ("naive-argmin", "probe-broadcast", "naive\nargmin"),
        ("distance-only", "probe-broadcast", "distance\nonly"),
        ("gemm-argmin", "probe-broadcast", "gemm\nargmin"),
        ("one-centroid-distance", "probe-one-centroid", "one centroid\ndistance"),
        ("running-step", "probe-one-centroid", "running\nstep"),
        ("running-loop-k32", "probe-running-loop-k32", "running\nloop k=32"),
    ]
    for backend, mode in (("torch", "torch.compile"), ("cupy", "cupy.fuse")):
        memory_rows = []
        time_rows = []
        for name, case, label in wanted:
            eager = _find(data, backend, "eager", name, case)
            other = _find(data, backend, mode, name, case)
            if eager is None or other is None or other.get("status") != "ok" or eager.get("status") != "ok":
                continue
            memory_rows.append((label, _mib(eager["median_peak_extra_bytes"]), _mib(other["median_peak_extra_bytes"])))
            time_rows.append((label, eager["median_seconds"] * 1e3, other["median_seconds"] * 1e3))
        folder = JOURNAL / "001-fusion-probe"
        _paired_bars(
            folder / f"memory-{backend}.svg",
            f"{backend}: peak extra memory on the probe",
            memory_rows,
            "MiB above the inputs",
        )
        _paired_bars(
            folder / f"time-{backend}.svg",
            f"{backend}: median runtime on the probe",
            time_rows,
            "milliseconds",
        )


def _find(data, backend, mode, name, case):
    for row in data["runs"]:
        if (
            row.get("backend") == backend
            and row.get("mode") == mode
            and row.get("name") == name
            and row.get("case") == case
        ):
            return row
    return None


def _short_case(name):
    for marker in ("-broadcast", "-running", "-gemm-tile"):
        if marker in name:
            return name.split(marker)[0]
    return name


def _eager_compiled_rows(data, name, backend, compiled_mode, time_scale):
    memory_rows = []
    time_rows = []
    for row in data["runs"]:
        if row.get("name") != name or row.get("backend") != backend or row.get("mode") != "eager":
            continue
        if row.get("status") != "ok":
            continue
        other = _find(data, backend, compiled_mode, name, row["case"])
        if other is None or other.get("status") != "ok":
            continue
        label = _short_case(row["case"])
        memory_rows.append(
            (label, _mib(row["median_peak_extra_bytes"]), _mib(other["median_peak_extra_bytes"]))
        )
        time_rows.append((label, row["median_seconds"] * time_scale, other["median_seconds"] * time_scale))
    return memory_rows, time_rows


def plot_bench(folder):
    data = _load(folder)
    out = JOURNAL / folder
    memory_rows, time_rows = _eager_compiled_rows(data, "gemm-argmin", "torch", "torch.compile", 1.0)
    if memory_rows:
        _paired_bars(
            out / "gemm-memory.svg",
            "GEMM argmin, peak extra memory",
            memory_rows,
            "MiB above the inputs",
        )
        _paired_bars(
            out / "gemm-time.svg",
            "GEMM argmin, median runtime",
            time_rows,
            "seconds",
        )
    memory_rows, time_rows = _eager_compiled_rows(data, "running-tile", "torch", "torch.compile", 1e3)
    if memory_rows:
        _paired_bars(
            out / "running-memory.svg",
            "Running tile of 32 centroids, peak extra memory",
            memory_rows,
            "MiB above the inputs",
            log=True,
        )
        _paired_bars(
            out / "running-time.svg",
            "Running tile of 32 centroids, median runtime",
            time_rows,
            "milliseconds",
        )
    memory_rows, time_rows = _eager_compiled_rows(data, "broadcast-tile", "torch", "torch.compile", 1e3)
    if memory_rows:
        _paired_bars(
            out / "broadcast-memory.svg",
            "Broadcast tile, peak extra memory",
            memory_rows,
            "MiB above the inputs",
            log=True,
        )
        _paired_bars(
            out / "broadcast-time.svg",
            "Broadcast tile, median runtime",
            time_rows,
            "milliseconds",
        )


if __name__ == "__main__":
    plot_probe()
    bench = JOURNAL / "003-resized-shapes" / "results.json"
    if bench.exists():
        plot_bench("003-resized-shapes")
