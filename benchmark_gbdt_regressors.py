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
from threadpoolctl import threadpool_limits
from xgboost import XGBRegressor


MODEL_NAMES = ("sklearn_hgb", "sklearn_hgb_fixed", "xgboost_hist", "lightgbm_hist")


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


def _common_hyperparameters(overrides: dict[str, Any] | None = None) -> dict[str, Any]:
    params = {
        "loss": "squared_error",
        "n_estimators": 220,
        "learning_rate": 0.05,
        "max_depth": 6,
        "num_leaves": 31,
        "max_bin": 255,
        "subsample": 0.8,
        "l2_regularization": 1.0,
        "min_samples_leaf": 20,
        "min_child_weight": 20.0,
        "min_split_gain": 0.0,
        "random_state": 42,
    }
    if overrides:
        params.update(overrides)
    return params


def _build_model(model_name: str, threads: int, common: dict[str, Any]):
    if model_name in {"sklearn_hgb", "sklearn_hgb_fixed"}:
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
            max_leaves=common["num_leaves"],
            max_bin=common["max_bin"],
            subsample=common["subsample"],
            colsample_bytree=1.0,
            reg_lambda=common["l2_regularization"],
            min_child_weight=common["min_child_weight"],
            gamma=common["min_split_gain"],
            tree_method="hist",
            grow_policy="lossguide",
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
            min_split_gain=common["min_split_gain"],
            min_child_weight=common["min_child_weight"],
            random_state=common["random_state"],
            n_jobs=threads,
            verbosity=-1,
        )
    raise ValueError(f"Unknown model: {model_name}")


def _set_thread_env(threads: int) -> None:
    os.environ["OMP_NUM_THREADS"] = str(threads)
    os.environ["OPENBLAS_NUM_THREADS"] = str(threads)
    os.environ["MKL_NUM_THREADS"] = str(threads)
    os.environ["NUMEXPR_NUM_THREADS"] = str(threads)


def _effective_thread_count(model_name: str, requested_threads: int) -> int:
    """Thread count used by the model internals.

    `sklearn_hgb_fixed` emulates a simple scikit-learn-side mitigation for
    oversubscription by capping OpenMP workers to host CPU count.
    """
    if model_name != "sklearn_hgb_fixed":
        return requested_threads
    cpu_count = os.cpu_count() or requested_threads
    return max(1, min(requested_threads, cpu_count))


def _monitor_peak_rss(stop_event: threading.Event, interval_s: float = 0.01) -> float:
    proc = psutil.Process()
    peak_rss = proc.memory_info().rss
    while not stop_event.is_set():
        rss = proc.memory_info().rss
        if rss > peak_rss:
            peak_rss = rss
        time.sleep(interval_s)
    return peak_rss / (1024 ** 2)


def _single_run(
    model_name: str,
    n_samples: int,
    n_features: int,
    threads: int,
    seed: int,
    common_overrides: dict[str, Any] | None,
) -> dict[str, Any]:
    effective_threads = _effective_thread_count(model_name=model_name, requested_threads=threads)
    _set_thread_env(effective_threads)
    common = _common_hyperparameters(overrides=common_overrides)
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

    model = _build_model(model_name=model_name, threads=effective_threads, common=common)
    stop_event = threading.Event()
    peak_holder = {"peak_mb": 0.0}

    def _run_monitor():
        peak_holder["peak_mb"] = _monitor_peak_rss(stop_event=stop_event)

    monitor_thread = threading.Thread(target=_run_monitor, daemon=True)
    monitor_thread.start()
    start = time.perf_counter()
    fit_start = time.perf_counter()
    with threadpool_limits(limits=effective_threads):
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
        "effective_threads": effective_threads,
        "n_samples": n_samples,
        "n_features": n_features,
        "fit_seconds": fit_end - fit_start,
        "predict_seconds": pred_end - fit_end,
        "total_seconds": total_end - start,
        "peak_rss_mb": peak_holder["peak_mb"],
        "rmse": rmse,
        "r2": r2,
        "hyperparameters": common,
    }


def _run_in_subprocess(
    model: str,
    n_samples: int,
    n_features: int,
    threads: int,
    seed: int,
    timeout_s: float,
    common_params_json: str | None,
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
    if common_params_json is not None:
        cmd.extend(["--common-params-json", common_params_json])
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
        current_n_samples = dataset["start_n_samples"]
        reduction_round = 0
        while True:
            timeout_happened = False
            dataset_runs: list[dict[str, Any]] = []
            for threads in thread_grid:
                per_thread_runs: list[dict[str, Any]] = []
                for model in MODEL_NAMES:
                    run = _run_in_subprocess(
                        model=model,
                        n_samples=current_n_samples,
                        n_features=dataset["n_features"],
                        threads=threads,
                        seed=args.seed,
                        timeout_s=args.timeout_s,
                        common_params_json=args.common_params_json,
                    )
                    if run.get("timeout", False):
                        timeout_happened = True
                        break
                    run["dataset_name"] = dataset["name"]
                    run["timeout_s"] = args.timeout_s
                    run["reduced_from_n_samples"] = dataset["start_n_samples"]
                    run["reduction_round"] = reduction_round
                    per_thread_runs.append(run)
                if timeout_happened:
                    break

                r2_values = [r["r2"] for r in per_thread_runs]
                r2_spread = max(r2_values) - min(r2_values)
                for r in per_thread_runs:
                    r["r2_spread_for_scenario"] = r2_spread
                    r["r2_spread_tolerance"] = args.max_r2_spread
                    r["r2_spread_within_tolerance"] = r2_spread <= args.max_r2_spread
                dataset_runs.extend(per_thread_runs)
            if timeout_happened:
                reduced = int(current_n_samples * args.reduction_factor)
                if reduced < args.min_n_samples:
                    raise RuntimeError(
                        f"Could not keep runtimes <= {args.timeout_s}s for dataset={dataset['name']} "
                        f"for all thread settings even after reducing to n_samples={current_n_samples}."
                    )
                current_n_samples = reduced
                reduction_round += 1
                continue
            all_runs.extend(dataset_runs)
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
    common_overrides = None if args.common_params_json is None else json.loads(args.common_params_json)
    result = _single_run(
        model_name=args.model,
        n_samples=args.n_samples,
        n_features=args.n_features,
        threads=args.threads,
        seed=args.seed,
        common_overrides=common_overrides,
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
    single.add_argument("--common-params-json", type=str, default=None)

    bench = subparsers.add_parser("benchmark", help="Run all benchmarks with adaptive sizing.")
    bench.add_argument("--output-json", type=str, default="artifacts/benchmark_results.json")
    bench.add_argument("--timeout-s", type=float, default=10.0)
    bench.add_argument("--reduction-factor", type=float, default=0.72)
    bench.add_argument("--min-n-samples", type=int, default=10_000)
    bench.add_argument("--seed", type=int, default=42)
    bench.add_argument("--max-r2-spread", type=float, default=0.03)
    bench.add_argument("--thread-grid", type=int, nargs="*", default=None)
    bench.add_argument("--common-params-json", type=str, default=None)

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
