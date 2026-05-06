#!/usr/bin/env python3
import argparse
import json
import statistics
import subprocess
import sys
from pathlib import Path


MODELS = ("sklearn_hgb", "xgboost_hist", "lightgbm_hist")


def _run_single(model: str, n_samples: int, n_features: int, timeout_s: float, params_json: str) -> dict:
    cmd = [
        sys.executable,
        "benchmark_gbdt_regressors.py",
        "single-run",
        "--model",
        model,
        "--n-samples",
        str(n_samples),
        "--n-features",
        str(n_features),
        "--threads",
        "1",
        "--seed",
        "42",
        "--common-params-json",
        params_json,
    ]
    completed = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout_s, check=False)
    if completed.returncode != 0:
        raise RuntimeError(
            f"single-run failed model={model} rc={completed.returncode}\n"
            f"stdout:\n{completed.stdout}\n"
            f"stderr:\n{completed.stderr}"
        )
    return json.loads(completed.stdout)


def _candidate_grid() -> list[dict]:
    return [
        {
            "name": "cfg_a_depth4_leaf15",
            "n_estimators": 200,
            "learning_rate": 0.05,
            "max_depth": 4,
            "num_leaves": 15,
            "max_bin": 255,
            "subsample": 1.0,
            "l2_regularization": 1.0,
            "min_samples_leaf": 20,
            "min_child_weight": 20.0,
            "min_split_gain": 0.0,
            "random_state": 42,
            "loss": "squared_error",
        },
        {
            "name": "cfg_b_depth5_leaf31",
            "n_estimators": 180,
            "learning_rate": 0.06,
            "max_depth": 5,
            "num_leaves": 31,
            "max_bin": 255,
            "subsample": 1.0,
            "l2_regularization": 1.0,
            "min_samples_leaf": 30,
            "min_child_weight": 30.0,
            "min_split_gain": 0.0,
            "random_state": 42,
            "loss": "squared_error",
        },
        {
            "name": "cfg_c_depth3_leaf8",
            "n_estimators": 240,
            "learning_rate": 0.07,
            "max_depth": 3,
            "num_leaves": 8,
            "max_bin": 255,
            "subsample": 1.0,
            "l2_regularization": 1.0,
            "min_samples_leaf": 20,
            "min_child_weight": 20.0,
            "min_split_gain": 0.0,
            "random_state": 42,
            "loss": "squared_error",
        },
        {
            "name": "cfg_d_depth4_leaf31_more_reg",
            "n_estimators": 180,
            "learning_rate": 0.05,
            "max_depth": 4,
            "num_leaves": 31,
            "max_bin": 255,
            "subsample": 1.0,
            "l2_regularization": 3.0,
            "min_samples_leaf": 30,
            "min_child_weight": 30.0,
            "min_split_gain": 0.0,
            "random_state": 42,
            "loss": "squared_error",
        },
    ]


def _score_candidate(scenario_rows: list[dict]) -> tuple[float, float, float]:
    spreads = [row["r2_spread"] for row in scenario_rows]
    means = [row["r2_mean"] for row in scenario_rows]
    return max(spreads), statistics.mean(spreads), -statistics.mean(means)


def _to_md(table_rows: list[dict], best_name: str, out_path: Path) -> None:
    lines = [
        "# Shared hyperparameter calibration",
        "",
        "| candidate | dataset | n_samples | n_features | r2_spread | r2_mean | max_total_s |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in table_rows:
        lines.append(
            f"| {row['candidate']} | {row['dataset']} | {row['n_samples']} | {row['n_features']} | "
            f"{row['r2_spread']:.6f} | {row['r2_mean']:.6f} | {row['max_total_s']:.4f} |"
        )
    lines.extend(["", f"Best candidate: `{best_name}`"])
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-best-json", default="artifacts/aligned_common_params.json")
    parser.add_argument("--output-report-json", default="artifacts/calibration_report.json")
    parser.add_argument("--output-report-md", default="artifacts/calibration_report.md")
    parser.add_argument("--timeout-s", type=float, default=10.0)
    args = parser.parse_args()

    datasets = [
        {"name": "medium", "n_samples": 90_000, "n_features": 80},
        {"name": "large_like", "n_samples": 120_000, "n_features": 100},
    ]
    candidates = _candidate_grid()
    table_rows: list[dict] = []
    per_candidate_rows: dict[str, list[dict]] = {}

    for candidate in candidates:
        params_json = json.dumps({k: v for k, v in candidate.items() if k != "name"}, sort_keys=True)
        scenario_rows = []
        for ds in datasets:
            model_runs = []
            for model in MODELS:
                run = _run_single(
                    model=model,
                    n_samples=ds["n_samples"],
                    n_features=ds["n_features"],
                    timeout_s=args.timeout_s,
                    params_json=params_json,
                )
                model_runs.append(run)
            r2_values = [r["r2"] for r in model_runs]
            totals = [r["total_seconds"] for r in model_runs]
            row = {
                "candidate": candidate["name"],
                "dataset": ds["name"],
                "n_samples": ds["n_samples"],
                "n_features": ds["n_features"],
                "r2_spread": max(r2_values) - min(r2_values),
                "r2_mean": statistics.mean(r2_values),
                "max_total_s": max(totals),
                "runs": model_runs,
            }
            scenario_rows.append(row)
            table_rows.append({k: row[k] for k in ("candidate", "dataset", "n_samples", "n_features", "r2_spread", "r2_mean", "max_total_s")})
        per_candidate_rows[candidate["name"]] = scenario_rows

    best_name = min(per_candidate_rows.keys(), key=lambda name: _score_candidate(per_candidate_rows[name]))
    best_params = {k: v for k, v in next(c for c in candidates if c["name"] == best_name).items() if k != "name"}

    Path(args.output_best_json).write_text(json.dumps(best_params, indent=2), encoding="utf-8")
    Path(args.output_report_json).write_text(
        json.dumps(
            {
                "best_candidate": best_name,
                "best_params": best_params,
                "results": table_rows,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    _to_md(table_rows=table_rows, best_name=best_name, out_path=Path(args.output_report_md))
    print(json.dumps({"best_candidate": best_name, "best_params_json": args.output_best_json}))


if __name__ == "__main__":
    main()
