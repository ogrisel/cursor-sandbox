#!/usr/bin/env python3
import argparse
import json
from collections import defaultdict
from pathlib import Path
from statistics import geometric_mean, mean, median

from artifact_layout import machine_artifacts_dir


BASE_DIR = Path(__file__).resolve().parent


def _load(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _scenario_key(run: dict) -> tuple[str, int]:
    return run["dataset_name"], run["threads"]


def _collect_runs_by_model(runs: list[dict]) -> dict[str, list[dict]]:
    by_model: dict[str, list[dict]] = defaultdict(list)
    for run in runs:
        by_model[run["model"]].append(run)
    return by_model


def _single_thread_table(runs: list[dict]) -> list[dict]:
    return sorted(
        [r for r in runs if r["threads"] == 1],
        key=lambda r: (r["dataset_name"], r["total_seconds"]),
    )


def _scalability_table(runs: list[dict]) -> list[dict]:
    by_model_dataset: dict[tuple[str, str], dict[int, dict]] = defaultdict(dict)
    for run in runs:
        by_model_dataset[(run["model"], run["dataset_name"])][run["threads"]] = run

    rows: list[dict] = []
    for (model, dataset_name), per_threads in sorted(by_model_dataset.items()):
        threads_available = sorted(per_threads.keys())
        if 1 not in per_threads or len(threads_available) < 2:
            continue
        base = per_threads[1]["fit_seconds"]
        max_threads = max(threads_available)
        scaled = per_threads[max_threads]["fit_seconds"]
        speedup = base / scaled
        efficiency = speedup / max_threads
        rows.append(
            {
                "model": model,
                "dataset_name": dataset_name,
                "max_threads": max_threads,
                "fit_s_1_thread": base,
                "fit_s_max_threads": scaled,
                "speedup_vs_1_thread": speedup,
                "parallel_efficiency": efficiency,
            }
        )
    return rows


def _memory_growth_table(runs: list[dict]) -> list[dict]:
    rows: list[dict] = []
    by_model = _collect_runs_by_model([r for r in runs if r["threads"] == 1])
    for model, model_runs in sorted(by_model.items()):
        ordered = sorted(model_runs, key=lambda r: r["n_samples"])
        if len(ordered) < 2:
            continue
        slope_mb_per_1k = (
            (ordered[-1]["peak_rss_mb"] - ordered[0]["peak_rss_mb"])
            / (ordered[-1]["n_samples"] - ordered[0]["n_samples"])
            * 1000
        )
        rows.append(
            {
                "model": model,
                "smallest_samples": ordered[0]["n_samples"],
                "largest_samples": ordered[-1]["n_samples"],
                "peak_mb_smallest": ordered[0]["peak_rss_mb"],
                "peak_mb_largest": ordered[-1]["peak_rss_mb"],
                "approx_mb_per_1k_samples": slope_mb_per_1k,
            }
        )
    return rows


def _rank_models(runs: list[dict]) -> list[dict]:
    by_model = _collect_runs_by_model(runs)
    rows = []
    for model, model_runs in sorted(by_model.items()):
        total_times = [r["total_seconds"] for r in model_runs]
        fit_times = [r["fit_seconds"] for r in model_runs]
        max_r2_spread = max(r["r2_spread_for_scenario"] for r in model_runs)
        rows.append(
            {
                "model": model,
                "median_total_s": median(total_times),
                "mean_total_s": mean(total_times),
                "median_fit_s": median(fit_times),
                "geo_mean_total_s": geometric_mean(total_times),
                "mean_peak_rss_mb": mean(r["peak_rss_mb"] for r in model_runs),
                "mean_r2": mean(r["r2"] for r in model_runs),
                "max_r2_spread_for_matched_scenario": max_r2_spread,
            }
        )
    rows.sort(key=lambda r: r["median_total_s"])
    return rows


def _table_md(rows: list[dict], columns: list[str]) -> str:
    if not rows:
        return "_No data_\n"
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = [
        "| " + " | ".join(f"{row[col]:.6g}" if isinstance(row[col], float) else str(row[col]) for col in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, sep, *body]) + "\n"


def _write_markdown(out_path: str, payload: dict, ranked: list[dict], single_thread: list[dict], scaling: list[dict], memory: list[dict]) -> None:
    least_model = ranked[-1]["model"] if ranked else "unknown"
    best_model = ranked[0]["model"] if ranked else "unknown"
    metadata = payload["metadata"]
    lines = [
        "# Histogram GBDT Regressor Benchmark Report",
        "",
        "## Experiment controls",
        f"- Timeout budget per individual run: `{metadata['timeout_s']} s`",
        f"- Adaptive reduction factor after timeout: `{metadata['reduction_factor']}`",
        f"- Threads tested: `{metadata['thread_grid']}`",
        f"- Dataset templates: `{metadata['dataset_grid']}`",
        "",
        "## Overall ranking (lower is faster)",
        _table_md(
            ranked,
            [
                "model",
                "median_total_s",
                "mean_total_s",
                "geo_mean_total_s",
                "mean_peak_rss_mb",
                "mean_r2",
                "max_r2_spread_for_matched_scenario",
            ],
        ),
        "",
        "## Single-thread behavior",
        _table_md(
            single_thread,
            [
                "dataset_name",
                "model",
                "n_samples",
                "n_features",
                "fit_seconds",
                "predict_seconds",
                "total_seconds",
                "peak_rss_mb",
                "r2",
            ],
        ),
        "",
        "## Multi-thread scalability",
        _table_md(
            scaling,
            [
                "dataset_name",
                "model",
                "max_threads",
                "fit_s_1_thread",
                "fit_s_max_threads",
                "speedup_vs_1_thread",
                "parallel_efficiency",
            ],
        ),
        "",
        "## Memory growth trend (thread=1)",
        _table_md(
            memory,
            [
                "model",
                "smallest_samples",
                "largest_samples",
                "peak_mb_smallest",
                "peak_mb_largest",
                "approx_mb_per_1k_samples",
            ],
        ),
        "",
        "## Initial conclusion",
        f"- Best median runtime model: `{best_model}`",
        f"- Least-performing median runtime model: `{least_model}`",
        "- All scenarios report explicit `r2_spread_for_scenario` to verify score parity while keeping matched hyperparameter values.",
    ]
    Path(out_path).write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-json", default=None)
    parser.add_argument("--output-md", default=None)
    parser.add_argument("--output-json", default=None)
    parser.add_argument("--artifacts-root", type=str, default=str(BASE_DIR / "artifacts"))
    parser.add_argument("--machine-tag", type=str, default=None)
    args = parser.parse_args()
    artifacts_dir = machine_artifacts_dir(
        base_dir=BASE_DIR,
        artifacts_root=args.artifacts_root,
        machine_tag=args.machine_tag,
    )
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    if args.input_json is None:
        args.input_json = str(artifacts_dir / "benchmark_results.json")
    if args.output_md is None:
        args.output_md = str(artifacts_dir / "benchmark_report.md")
    if args.output_json is None:
        args.output_json = str(artifacts_dir / "benchmark_summary.json")

    payload = _load(args.input_json)
    runs = payload["runs"]
    ranked = _rank_models(runs)
    single_thread = _single_thread_table(runs)
    scaling = _scalability_table(runs)
    memory = _memory_growth_table(runs)

    Path(args.output_json).write_text(
        json.dumps(
            {
                "ranked_models": ranked,
                "single_thread_runs": single_thread,
                "scalability": scaling,
                "memory_growth": memory,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    _write_markdown(args.output_md, payload, ranked, single_thread, scaling, memory)
    print(json.dumps({"summary_json": args.output_json, "summary_md": args.output_md}))


if __name__ == "__main__":
    main()
