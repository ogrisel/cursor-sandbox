#!/usr/bin/env python3
import argparse
import json
import math
import os
import subprocess
import sys
import threading
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np
import psutil
from lightgbm import LGBMRegressor
from sklearn.datasets import make_regression
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor


MODEL_NAMES = ("sklearn_hgb", "xgboost_hist", "lightgbm_hist")


@dataclass
class RunMetrics:
    model: str
    threads: int
    n_samples: int
    n_features: int
    fit_seconds: float
    predict_seconds: float
    total_seconds: float
    peak_rss_mb: float
    rmse: float
    r2: float
    timeout_s: float
    reduced_from_n_samples: int
    reduction_round: int
    hyperparameters: dict[str, Any]


def _common_hyperparameters() -> dict[str, Any]:
    return {
        "loss": "squared_error",
        "n_estimators": 220,
        "learning_rate": 0.05,
        "max_depth": 6,
        "num_leaves": 31,
        "max_bin": 255,
        "subsample": 0.8,
        "l2_regularization": 1.0,
        "min_samples_leaf": 20,
        "random_state": 42,
    }


def _build_model(model_name: str, threads: int):
    common = _common_hyperparameters()
    if model_name == "sklearn_hgb":
        return HistGradientBoostingRegressor(
            loss=common["loss"],
            max_iter=common["n_estimators"],
            learning_rate=common["learning_rate"],
            max_depth=common["max_depth"],
            max_leaf_nodes=common["num_leaves"],
            max_bins=common["max_bin"],
            min_samples_leaf=common["min_samples_leaf"],
            l2_regularization=common["l2_regularization"],
            random_state=common["random_state"],
            early_stopping=False,
        )
    if model_name == "xgboost_hist":
        return XGBRegressor(
            objective="reg:squarederror",
            n_estimators=common["n_estimators"],
            learning_rate=common["learning_rate"],
            max_depth=common["max_depth"],
            max_bin=common["max_bin"],
            subsample=common["subsample"],
            colsample_bytree=1.0,
            reg_lambda=common["l2_regularization"],
            tree_method="hist",
            grow_policy="depthwise",
            random_state=common["random_state"],
            n_jobs=threads,
            verbosity=0,
        )
    if model_name == "lightgbm_hist":
        return LGBMRegressor(
            objective="regression",
            n_estimators=common["n_estimators"],
            learning_rate=common["learning_rate"],
            max_depth=common["max_depth"],
            num_leaves=common["num_leaves"],
            max_bin=common["max_bin"],
            subsample=common["subsample"],
            subsample_freq=1,
            reg_lambda=common["l2_regularization"],
            min_child_samples=common["min_samples_leaf"],
            random_state=common["random_state"],
            n_jobs=threads,
            verbose=-1,
        )
    raise ValueError(f"Unknown model: {model_name}")


def _set_thread_env(threads: int) -> None:
    os.environ["OMP_NUM_THREADS"] = str(threads)
    os.environ["OPENBLAS_NUM_THREADS"] = str(threads)
    os.environ["MKL_NUM_THREADS"] = str(threads)
    os.environ["NUMEXPR_NUM_THREADS"] = str(threads)


def _monitor_peak_rss(stop_event: threading.Event, interval_s: float = 0.01) -> float:
    proc = psutil.Process()
    peak_rss = proc.memory_info().rss
    while not stop_event.is_set():
        rss = proc.memory_info().rss
        if rss > peak_rss:
            peak_rss = rss
        time.sleep(interval_s)
    return peak_rss / (1024 ** 2)


def _single_run(model_name: str, n_samples: int, n_features: int, threads: int, seed: int) -> dict[str, Any]:
    _set_thread_env(threads)
    X, y = make_regression(
        n_samples=n_samples,
        n_features=n_features,
        n_informative=max(4, int(n_features * 0.75)),
        noise=1.5,
        random_state=seed,
    )
    X = X.astype(np.float32)
    y = y.astype(np.float32)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=seed)

    model = _build_model(model_name=model_name, threads=threads)
    stop_event = threading.Event()
    peak_holder = {"peak_mb": 0.0}

    def _run_monitor():
        peak_holder["peak_mb"] = _monitor_peak_rss(stop_event=stop_event)

    monitor_thread = threading.Thread(target=_run_monitor, daemon=True)
    monitor_thread.start()
    start = time.perf_counter()
    fit_start = time.perf_counter()
    model.fit(X_train, y_train)
    fit_end = time.perf_counter()
    y_pred = model.predict(X_test)
    pred_end = time.perf_counter()
    stop_event.set()
    monitor_thread.join(timeout=1.0)
    total_end = time.perf_counter()

    rmse = math.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)
    return {
        "model": model_name,
        "threads": threads,
        "n_samples": n_samples,
        "n_features": n_features,
        "fit_seconds": fit_end - fit_start,
        "predict_seconds": pred_end - fit_end,
        "total_seconds": total_end - start,
        "peak_rss_mb": peak_holder["peak_mb"],
        "rmse": rmse,
        "r2": r2,
        "hyperparameters": _common_hyperparameters(),
    }


def _run_in_subprocess(
    model: str,
    n_samples: int,
    n_features: int,
    threads: int,
    seed: int,
    timeout_s: float,
) -> dict[str, Any]:
    cmd = [
        sys.executable,
        __file__,
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
    ]
    try:
        completed = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout_s,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return {"timeout": True}

    if completed.returncode != 0:
        raise RuntimeError(
            f"Subprocess failed for {model} with rc={completed.returncode}\n"
            f"stdout:\n{completed.stdout}\n"
            f"stderr:\n{completed.stderr}"
        )
    return json.loads(completed.stdout)


def _default_thread_grid() -> list[int]:
    cpu_count = os.cpu_count() or 1
    candidate = [1, 2, 4, 8]
    grid = sorted({t for t in candidate if t <= cpu_count})
    if cpu_count not in grid:
        grid.append(cpu_count)
    return sorted(set(grid))


def _benchmark(args: argparse.Namespace) -> None:
    out_path = Path(args.output_json)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    thread_grid = _default_thread_grid() if args.thread_grid is None else sorted(set(args.thread_grid))
    dataset_grid = [
        {"name": "small", "start_n_samples": 50_000, "n_features": 40},
        {"name": "medium", "start_n_samples": 140_000, "n_features": 80},
        {"name": "large", "start_n_samples": 320_000, "n_features": 120},
    ]
    all_runs: list[dict[str, Any]] = []

    for dataset in dataset_grid:
        for threads in thread_grid:
            current_n_samples = dataset["start_n_samples"]
            reduction_round = 0
            while True:
                timeout_happened = False
                scenario_runs: list[dict[str, Any]] = []
                for model in MODEL_NAMES:
                    run = _run_in_subprocess(
                        model=model,
                        n_samples=current_n_samples,
                        n_features=dataset["n_features"],
                        threads=threads,
                        seed=args.seed,
                        timeout_s=args.timeout_s,
                    )
                    if run.get("timeout", False):
                        timeout_happened = True
                        break
                    run["dataset_name"] = dataset["name"]
                    run["timeout_s"] = args.timeout_s
                    run["reduced_from_n_samples"] = dataset["start_n_samples"]
                    run["reduction_round"] = reduction_round
                    scenario_runs.append(run)
                if timeout_happened:
                    reduced = int(current_n_samples * args.reduction_factor)
                    if reduced < args.min_n_samples:
                        raise RuntimeError(
                            f"Could not keep runtimes <= {args.timeout_s}s for dataset={dataset['name']} "
                            f"threads={threads} even after reducing to n_samples={current_n_samples}."
                        )
                    current_n_samples = reduced
                    reduction_round += 1
                    continue

                r2_values = [r["r2"] for r in scenario_runs]
                r2_spread = max(r2_values) - min(r2_values)
                for r in scenario_runs:
                    r["r2_spread_for_scenario"] = r2_spread
                    r["r2_spread_tolerance"] = args.max_r2_spread
                    r["r2_spread_within_tolerance"] = r2_spread <= args.max_r2_spread
                all_runs.extend(scenario_runs)
                break

    with out_path.open("w", encoding="utf-8") as f:
        json.dump(
            {
                "metadata": {
                    "timeout_s": args.timeout_s,
                    "thread_grid": thread_grid,
                    "dataset_grid": dataset_grid,
                    "reduction_factor": args.reduction_factor,
                    "min_n_samples": args.min_n_samples,
                    "max_r2_spread": args.max_r2_spread,
                },
                "runs": all_runs,
            },
            f,
            indent=2,
        )

    print(json.dumps({"output_json": str(out_path), "n_runs": len(all_runs)}))


def _emit_single(args: argparse.Namespace) -> None:
    result = _single_run(
        model_name=args.model,
        n_samples=args.n_samples,
        n_features=args.n_features,
        threads=args.threads,
        seed=args.seed,
    )
    print(json.dumps(result))


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Benchmark histogram GBDT regressors.")
    subparsers = parser.add_subparsers(dest="mode", required=True)

    single = subparsers.add_parser("single-run", help="Run a single benchmark and emit JSON.")
    single.add_argument("--model", choices=MODEL_NAMES, required=True)
    single.add_argument("--n-samples", type=int, required=True)
    single.add_argument("--n-features", type=int, required=True)
    single.add_argument("--threads", type=int, required=True)
    single.add_argument("--seed", type=int, default=42)

    bench = subparsers.add_parser("benchmark", help="Run all benchmarks with adaptive sizing.")
    bench.add_argument("--output-json", type=str, default="artifacts/benchmark_results.json")
    bench.add_argument("--timeout-s", type=float, default=10.0)
    bench.add_argument("--reduction-factor", type=float, default=0.72)
    bench.add_argument("--min-n-samples", type=int, default=10_000)
    bench.add_argument("--seed", type=int, default=42)
    bench.add_argument("--max-r2-spread", type=float, default=0.03)
    bench.add_argument("--thread-grid", type=int, nargs="*", default=None)

    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    if args.mode == "single-run":
        _emit_single(args)
        return
    if args.mode == "benchmark":
        _benchmark(args)
        return
    raise ValueError(f"Unexpected mode: {args.mode}")


if __name__ == "__main__":
    main()
