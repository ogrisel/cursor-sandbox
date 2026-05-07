#!/usr/bin/env python3
import argparse
import json
import statistics
import subprocess
import sys
from pathlib import Path

import matplotlib.pyplot as plt


MODEL_CHOICES = ("sklearn_hgb", "sklearn_hgb_fixed", "xgboost_hist", "lightgbm_hist")


def _load_payload(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _collect_rows(
    benchmark_script: str,
    common_params_json_path: str,
    n_samples: int,
    n_features: int,
    models: list[str],
    threads: list[int],
    repeats: int,
    timeout_s: float,
    seed: int,
) -> dict:
    params_json = Path(common_params_json_path).read_text(encoding="utf-8")
    rows = []
    for model in models:
        for thread_count in threads:
            fit_values = []
            pred_values = []
            total_values = []
            r2_values = []
            effective_values = []
            fitted_trees_values = []
            fitted_trees_match_values = []
            for rep in range(repeats):
                cmd = [
                    sys.executable,
                    benchmark_script,
                    "single-run",
                    "--model",
                    model,
                    "--n-samples",
                    str(n_samples),
                    "--n-features",
                    str(n_features),
                    "--threads",
                    str(thread_count),
                    "--seed",
                    str(seed + rep),
                    "--common-params-json",
                    params_json,
                ]
                completed = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout_s, check=False)
                if completed.returncode != 0:
                    raise RuntimeError(
                        f"single-run failed for model={model}, threads={thread_count}\n"
                        f"stdout:\n{completed.stdout}\n"
                        f"stderr:\n{completed.stderr}"
                    )
                run = json.loads(completed.stdout)
                fit_values.append(run["fit_seconds"])
                pred_values.append(run["predict_seconds"])
                total_values.append(run["total_seconds"])
                r2_values.append(run["r2"])
                effective_values.append(run.get("effective_threads", thread_count))
                fitted_trees_values.append(run.get("fitted_trees"))
                fitted_trees_match_values.append(run.get("fitted_trees_match_expected", False))
            rows.append(
                {
                    "model": model,
                    "threads": thread_count,
                    "effective_threads_mean": statistics.mean(effective_values),
                    "fit_mean": statistics.mean(fit_values),
                    "predict_mean": statistics.mean(pred_values),
                    "total_mean": statistics.mean(total_values),
                    "r2_mean": statistics.mean(r2_values),
                    "fitted_trees_mean": statistics.mean(fitted_trees_values),
                    "fitted_trees_match_all": all(fitted_trees_match_values),
                    "fit_std": statistics.pstdev(fit_values),
                    "repeats": repeats,
                }
            )
    return {
        "final_rows": rows,
        "models": models,
        "params": json.loads(params_json),
        "dataset": {"n_samples": n_samples, "n_features": n_features},
        "repeats": repeats,
        "threads": threads,
    }


def _collect_by_model(rows: list[dict]) -> dict[str, dict[int, dict]]:
    by_model: dict[str, dict[int, dict]] = {}
    for row in rows:
        by_model.setdefault(row["model"], {})[int(row["threads"])] = row
    return by_model


def _plot(
    by_model: dict[str, dict[int, dict]],
    thread_grid: list[int],
    out_png: str,
    speedup_ymax: float | None,
) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
    ax_time, ax_speedup = axes

    for model, rows in sorted(by_model.items()):
        threads = [t for t in thread_grid if t in rows]
        if 1 not in rows or not threads:
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
    ax_time.set_xticks(thread_grid)
    ax_time.grid(alpha=0.3)

    ax_speedup.set_title("Speedup vs threads")
    ax_speedup.set_xlabel("Threads")
    ax_speedup.set_ylabel("Speedup (1-thread baseline)")
    ax_speedup.set_xticks(thread_grid)
    if speedup_ymax is not None:
        ax_speedup.set_ylim(0.0, speedup_ymax)
    ax_speedup.grid(alpha=0.3)

    handles, labels = ax_time.get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=min(4, max(1, len(labels))), frameon=False)
    fig.suptitle("Scalability curves on constrained comparable benchmark")
    fig.tight_layout(rect=(0, 0.08, 1, 0.95))
    fig.savefig(out_png, dpi=180)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-json", default="artifacts/comparable_large_results.json")
    parser.add_argument("--output-png", default="artifacts/scalability_curves.png")
    parser.add_argument("--collect", action="store_true")
    parser.add_argument("--output-data-json", default="artifacts/scalability_curve_data.json")
    parser.add_argument("--benchmark-script", default="benchmark_gbdt_regressors.py")
    parser.add_argument("--common-params-json", default="artifacts/comparable_large_params.json")
    parser.add_argument("--n-samples", type=int, default=176_000)
    parser.add_argument("--n-features", type=int, default=120)
    parser.add_argument(
        "--models",
        type=str,
        nargs="+",
        default=["sklearn_hgb", "sklearn_hgb_fixed", "xgboost_hist", "lightgbm_hist"],
    )
    parser.add_argument("--threads", type=int, nargs="+", default=[1, 2, 4, 8, 16])
    parser.add_argument("--repeats", type=int, default=2)
    parser.add_argument("--timeout-s", type=float, default=15.0)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--speedup-ymax", type=float, default=4.0)
    args = parser.parse_args()

    if args.collect:
        models = []
        for model_name in args.models:
            if model_name not in MODEL_CHOICES:
                raise ValueError(f"Unknown model '{model_name}'. Valid options: {MODEL_CHOICES}")
            models.append(model_name)
        payload = _collect_rows(
            benchmark_script=args.benchmark_script,
            common_params_json_path=args.common_params_json,
            n_samples=args.n_samples,
            n_features=args.n_features,
            models=models,
            threads=sorted(set(args.threads)),
            repeats=args.repeats,
            timeout_s=args.timeout_s,
            seed=args.seed,
        )
        Path(args.output_data_json).write_text(json.dumps(payload, indent=2), encoding="utf-8")
    else:
        payload = _load_payload(args.input_json)

    rows = payload["final_rows"]
    thread_grid = sorted({int(r["threads"]) for r in rows})
    by_model = _collect_by_model(rows)
    _plot(
        by_model,
        thread_grid=thread_grid,
        out_png=args.output_png,
        speedup_ymax=args.speedup_ymax,
    )
    print(json.dumps({"output_png": args.output_png, "thread_grid": thread_grid}))


if __name__ == "__main__":
    main()
