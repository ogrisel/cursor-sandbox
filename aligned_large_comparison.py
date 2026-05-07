#!/usr/bin/env python3
import argparse
import json
import statistics
import subprocess
import sys
from pathlib import Path


MODELS = ("sklearn_hgb", "xgboost_hist", "lightgbm_hist")


def _run_single(
    model: str,
    n_samples: int,
    n_features: int,
    threads: int,
    seed: int,
    params_json: str,
    timeout_s: float,
) -> dict:
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
        str(threads),
        "--seed",
        str(seed),
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
    # Every candidate respects requested constraints:
    # - n_estimators >= 10
    # - num_leaves >= 31
    return [
        {
            "name": "cfg_a_balanced_120",
            "n_estimators": 120,
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
        {
            "name": "cfg_b_regularized_90",
            "n_estimators": 90,
            "learning_rate": 0.07,
            "max_depth": 4,
            "num_leaves": 31,
            "max_bin": 255,
            "subsample": 1.0,
            "l2_regularization": 8.0,
            "min_samples_leaf": 45,
            "min_child_weight": 45.0,
            "min_split_gain": 0.05,
            "random_state": 42,
            "loss": "squared_error",
        },
        {
            "name": "cfg_c_shallow_160",
            "n_estimators": 160,
            "learning_rate": 0.04,
            "max_depth": 3,
            "num_leaves": 31,
            "max_bin": 255,
            "subsample": 1.0,
            "l2_regularization": 4.0,
            "min_samples_leaf": 35,
            "min_child_weight": 35.0,
            "min_split_gain": 0.0,
            "random_state": 42,
            "loss": "squared_error",
        },
        {
            "name": "cfg_d_deeper_80",
            "n_estimators": 80,
            "learning_rate": 0.08,
            "max_depth": 6,
            "num_leaves": 31,
            "max_bin": 255,
            "subsample": 1.0,
            "l2_regularization": 6.0,
            "min_samples_leaf": 50,
            "min_child_weight": 50.0,
            "min_split_gain": 0.1,
            "random_state": 42,
            "loss": "squared_error",
        },
        {
            "name": "cfg_e_more_leaves_100",
            "n_estimators": 100,
            "learning_rate": 0.06,
            "max_depth": 5,
            "num_leaves": 63,
            "max_bin": 255,
            "subsample": 1.0,
            "l2_regularization": 10.0,
            "min_samples_leaf": 40,
            "min_child_weight": 40.0,
            "min_split_gain": 0.1,
            "random_state": 42,
            "loss": "squared_error",
        },
        {
            "name": "cfg_f_small_forest_40",
            "n_estimators": 40,
            "learning_rate": 0.12,
            "max_depth": 4,
            "num_leaves": 31,
            "max_bin": 255,
            "subsample": 1.0,
            "l2_regularization": 5.0,
            "min_samples_leaf": 55,
            "min_child_weight": 55.0,
            "min_split_gain": 0.2,
            "random_state": 42,
            "loss": "squared_error",
        },
    ]


def _validate_constraints(candidate: dict) -> None:
    if candidate["n_estimators"] < 10:
        raise ValueError(f"Invalid candidate {candidate['name']}: n_estimators must be >= 10")
    if candidate["num_leaves"] < 31:
        raise ValueError(f"Invalid candidate {candidate['name']}: num_leaves must be >= 31")


def _find_runtime_compliant_n_samples(
    params_json: str,
    start_n_samples: int,
    n_features: int,
    timeout_s: float,
    reduction_factor: float,
    min_n_samples: int,
) -> int:
    n_samples = start_n_samples
    while True:
        try:
            all_runs = [
                _run_single(
                    model=model,
                    n_samples=n_samples,
                    n_features=n_features,
                    threads=1,
                    seed=42,
                    params_json=params_json,
                    timeout_s=timeout_s,
                )
                for model in MODELS
            ]
        except Exception:
            reduced = int(n_samples * reduction_factor)
            if reduced < min_n_samples:
                raise RuntimeError("Could not find runtime-compliant n_samples for candidate")
            n_samples = reduced
            continue

        if max(r["total_seconds"] for r in all_runs) < timeout_s:
            return n_samples
        reduced = int(n_samples * reduction_factor)
        if reduced < min_n_samples:
            raise RuntimeError("Could not find runtime-compliant n_samples for candidate")
        n_samples = reduced


def _calibrate(
    candidates: list[dict],
    start_n_samples: int,
    n_features: int,
    timeout_s: float,
    reduction_factor: float,
    min_n_samples: int,
) -> tuple[dict, list[dict]]:
    calibration_rows = []
    best = None
    for candidate in candidates:
        _validate_constraints(candidate)
        params = {k: v for k, v in candidate.items() if k != "name"}
        params_json = json.dumps(params, sort_keys=True)
        n_samples = _find_runtime_compliant_n_samples(
            params_json=params_json,
            start_n_samples=start_n_samples,
            n_features=n_features,
            timeout_s=timeout_s,
            reduction_factor=reduction_factor,
            min_n_samples=min_n_samples,
        )
        runs = [
            _run_single(
                model=model,
                n_samples=n_samples,
                n_features=n_features,
                threads=1,
                seed=42,
                params_json=params_json,
                timeout_s=timeout_s,
            )
            for model in MODELS
        ]
        if not all(run.get("fitted_trees_match_expected", False) for run in runs):
            raise RuntimeError(
                "Calibration run found fitted tree count mismatch: "
                + "; ".join(
                    f"{r['model']} fitted={r.get('fitted_trees')} expected={r.get('expected_trees')}"
                    for r in runs
                )
            )
        r2_values = [r["r2"] for r in runs]
        tree_values = [r["fitted_trees"] for r in runs]
        row = {
            "candidate": candidate["name"],
            "n_estimators": params["n_estimators"],
            "num_leaves": params["num_leaves"],
            "n_samples": n_samples,
            "n_features": n_features,
            "r2_spread": max(r2_values) - min(r2_values),
            "r2_mean": statistics.mean(r2_values),
            "fitted_trees_min": min(tree_values),
            "fitted_trees_max": max(tree_values),
            "fitted_trees_spread": max(tree_values) - min(tree_values),
            "max_total_s": max(r["total_seconds"] for r in runs),
            "runs": runs,
            "params": params,
        }
        calibration_rows.append(row)
        if best is None:
            best = row
            continue
        best_key = (best["r2_spread"], best["max_total_s"])
        key = (row["r2_spread"], row["max_total_s"])
        if key < best_key:
            best = row

    if best is None:
        raise RuntimeError("No valid calibration result found")
    return best, calibration_rows


def _final_benchmark(
    params: dict,
    n_samples: int,
    n_features: int,
    timeout_s: float,
    repeats: int,
) -> list[dict]:
    params_json = json.dumps(params, sort_keys=True)
    rows = []
    for model in MODELS:
        for threads in (1, 2, 4):
            fit_values = []
            pred_values = []
            total_values = []
            r2_values = []
            rss_values = []
            fitted_trees_values = []
            for rep in range(repeats):
                run = _run_single(
                    model=model,
                    n_samples=n_samples,
                    n_features=n_features,
                    threads=threads,
                    seed=42 + rep,
                    params_json=params_json,
                    timeout_s=timeout_s,
                )
                if not run.get("fitted_trees_match_expected", False):
                    raise RuntimeError(
                        f"Final benchmark tree mismatch for {model} threads={threads}: "
                        f"fitted={run.get('fitted_trees')} expected={run.get('expected_trees')}"
                    )
                fit_values.append(run["fit_seconds"])
                pred_values.append(run["predict_seconds"])
                total_values.append(run["total_seconds"])
                r2_values.append(run["r2"])
                rss_values.append(run["peak_rss_mb"])
                fitted_trees_values.append(run["fitted_trees"])

            rows.append(
                {
                    "model": model,
                    "threads": threads,
                    "n_samples": n_samples,
                    "n_features": n_features,
                    "fit_mean": statistics.mean(fit_values),
                    "predict_mean": statistics.mean(pred_values),
                    "total_mean": statistics.mean(total_values),
                    "fit_std": statistics.pstdev(fit_values),
                    "r2_mean": statistics.mean(r2_values),
                    "r2_std": statistics.pstdev(r2_values),
                    "peak_rss_mean_mb": statistics.mean(rss_values),
                    "fitted_trees_mean": statistics.mean(fitted_trees_values),
                    "fitted_trees_std": statistics.pstdev(fitted_trees_values),
                }
            )
    return rows


def _write_report_md(
    path: Path,
    best: dict,
    calibration_rows: list[dict],
    final_rows: list[dict],
    repeats: int,
    timeout_s: float,
) -> None:
    by_model = {r["model"]: r for r in final_rows if r["threads"] == 1}
    r2_spread_final = max(r["r2_mean"] for r in by_model.values()) - min(r["r2_mean"] for r in by_model.values())

    lines = [
        "# Comparable large-run benchmark",
        "",
        "## Constraints enforced",
        "- n_estimators >= 10",
        "- num_leaves/max_leaf_nodes >= 31",
        f"- timeout per single run: {timeout_s:.1f}s",
        "",
        "## Calibration candidates (thread=1)",
        "| candidate | n_estimators | num_leaves | n_samples | r2_spread | r2_mean | max_total_s |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in calibration_rows:
        lines.append(
            f"| {row['candidate']} | {row['n_estimators']} | {row['num_leaves']} | {row['n_samples']} | "
            f"{row['r2_spread']:.6f} | {row['r2_mean']:.6f} | {row['max_total_s']:.4f} |"
        )
    lines.extend(
        [
            "",
            f"Best calibrated candidate: `{best['candidate']}`",
            "",
            "## Final comparable timing table",
            f"(all runs on same dataset `n_samples={best['n_samples']}`, `n_features={best['n_features']}`, repeats={repeats})",
            "",
            "| model | threads | fit_mean_s | predict_mean_s | total_mean_s | r2_mean | peak_rss_mean_mb | fitted_trees_mean |",
            "| --- | --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for row in sorted(final_rows, key=lambda r: (r["threads"], r["total_mean"])):
        lines.append(
            f"| {row['model']} | {row['threads']} | {row['fit_mean']:.4f} | {row['predict_mean']:.4f} | "
            f"{row['total_mean']:.4f} | {row['r2_mean']:.6f} | {row['peak_rss_mean_mb']:.2f} | {row['fitted_trees_mean']:.1f} |"
        )

    lines.extend(
        [
            "",
            "## Final comparability check",
            f"- R² spread across libraries at thread=1: `{r2_spread_final:.6f}`",
            f"- Fitted trees at thread=1: `{[int(by_model[m]['fitted_trees_mean']) for m in sorted(by_model)]}`",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-params-json", default="artifacts/comparable_large_params.json")
    parser.add_argument("--output-json", default="artifacts/comparable_large_results.json")
    parser.add_argument("--output-md", default="artifacts/comparable_large_report.md")
    parser.add_argument("--start-n-samples", type=int, default=220_000)
    parser.add_argument("--n-features", type=int, default=120)
    parser.add_argument("--timeout-s", type=float, default=10.0)
    parser.add_argument("--reduction-factor", type=float, default=0.8)
    parser.add_argument("--min-n-samples", type=int, default=40_000)
    parser.add_argument("--repeats", type=int, default=3)
    args = parser.parse_args()

    candidates = _candidate_grid()
    best, calibration_rows = _calibrate(
        candidates=candidates,
        start_n_samples=args.start_n_samples,
        n_features=args.n_features,
        timeout_s=args.timeout_s,
        reduction_factor=args.reduction_factor,
        min_n_samples=args.min_n_samples,
    )
    final_rows = _final_benchmark(
        params=best["params"],
        n_samples=best["n_samples"],
        n_features=best["n_features"],
        timeout_s=args.timeout_s,
        repeats=args.repeats,
    )

    Path(args.output_params_json).write_text(json.dumps(best["params"], indent=2), encoding="utf-8")
    Path(args.output_json).write_text(
        json.dumps(
            {
                "constraints": {
                    "min_n_estimators": 10,
                    "min_num_leaves": 31,
                    "timeout_s": args.timeout_s,
                },
                "best_candidate": best["candidate"],
                "best_candidate_n_samples": best["n_samples"],
                "best_candidate_n_features": best["n_features"],
                "calibration_rows": calibration_rows,
                "final_rows": final_rows,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    _write_report_md(
        path=Path(args.output_md),
        best=best,
        calibration_rows=calibration_rows,
        final_rows=final_rows,
        repeats=args.repeats,
        timeout_s=args.timeout_s,
    )
    print(
        json.dumps(
            {
                "output_json": args.output_json,
                "output_md": args.output_md,
                "output_params_json": args.output_params_json,
                "best_candidate": best["candidate"],
                "n_samples": best["n_samples"],
            }
        )
    )


if __name__ == "__main__":
    main()
