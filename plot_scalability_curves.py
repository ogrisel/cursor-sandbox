#!/usr/bin/env python3
import argparse
import json
import os
from pathlib import Path

import matplotlib.pyplot as plt


def _load_rows(path: str) -> list[dict]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    return payload["final_rows"]


def _collect_by_model(rows: list[dict], max_threads: int) -> dict[str, dict[int, dict]]:
    by_model: dict[str, dict[int, dict]] = {}
    for row in rows:
        t = int(row["threads"])
        if t > max_threads:
            continue
        by_model.setdefault(row["model"], {})[t] = row
    return by_model


def _plot(by_model: dict[str, dict[int, dict]], max_threads: int, out_png: str) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
    ax_time, ax_speedup = axes

    for model, rows in sorted(by_model.items()):
        threads = sorted(rows)
        if 1 not in rows:
            continue
        fit_times = [rows[t]["fit_mean"] for t in threads]
        baseline = rows[1]["fit_mean"]
        speedups = [baseline / rows[t]["fit_mean"] for t in threads]
        ideal = threads

        ax_time.plot(threads, fit_times, marker="o", label=model)
        ax_speedup.plot(threads, speedups, marker="o", label=model)
        ax_speedup.plot(threads, ideal, linestyle="--", alpha=0.35, color=ax_speedup.lines[-1].get_color())

    ax_time.set_title("Fit time vs threads")
    ax_time.set_xlabel("Threads")
    ax_time.set_ylabel("Mean fit time (s)")
    ax_time.set_xticks(range(1, max_threads + 1))
    ax_time.grid(alpha=0.3)

    ax_speedup.set_title("Speedup vs threads")
    ax_speedup.set_xlabel("Threads")
    ax_speedup.set_ylabel("Speedup (1-thread baseline)")
    ax_speedup.set_xticks(range(1, max_threads + 1))
    ax_speedup.grid(alpha=0.3)

    handles, labels = ax_time.get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=3, frameon=False)
    fig.suptitle("Scalability curves on constrained comparable benchmark")
    fig.tight_layout(rect=(0, 0.08, 1, 0.95))
    fig.savefig(out_png, dpi=180)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-json", default="artifacts/comparable_large_results.json")
    parser.add_argument("--output-png", default="artifacts/scalability_curves.png")
    args = parser.parse_args()

    cpu_count = os.cpu_count() or 1
    rows = _load_rows(args.input_json)
    by_model = _collect_by_model(rows, max_threads=cpu_count)
    _plot(by_model, max_threads=cpu_count, out_png=args.output_png)
    print(json.dumps({"output_png": args.output_png, "max_threads": cpu_count}))


if __name__ == "__main__":
    main()
