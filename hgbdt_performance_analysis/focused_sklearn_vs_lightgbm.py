#!/usr/bin/env python3
import argparse
import json
import statistics
import subprocess
import sys
from pathlib import Path

from artifact_layout import machine_artifacts_dir


MODELS = ("sklearn_hgb", "lightgbm_hist")
BASE_DIR = Path(__file__).resolve().parent


def _single_run(
    model: str,
    n_samples: int,
    n_features: int,
    threads: int,
    timeout_s: float,
    common_params_json: str,
    seed: int,
) -> dict:
    cmd = [
        sys.executable,
        str(BASE_DIR / "benchmark_gbdt_regressors.py"),
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
        common_params_json,
    ]
    completed = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout_s, check=False)
    if completed.returncode != 0:
        raise RuntimeError(
            f"single-run failed for {model}\nstdout:\n{completed.stdout}\nstderr:\n{completed.stderr}"
        )
    return json.loads(completed.stdout)


def _find_shared_n_samples(
    start_n_samples: int,
    n_features: int,
    timeout_s: float,
    reduction_factor: float,
    min_n_samples: int,
    common_params_json: str,
    thread_grid: list[int],
) -> tuple[int, int]:
    current = start_n_samples
    round_id = 0
    while True:
        timed_out = False
        for threads in thread_grid:
            for model in MODELS:
                try:
                    run = _single_run(
                        model=model,
                        n_samples=current,
                        n_features=n_features,
                        threads=threads,
                        timeout_s=timeout_s,
                        common_params_json=common_params_json,
                        seed=42,
                    )
                except subprocess.TimeoutExpired:
                    timed_out = True
                    break
                if run["total_seconds"] >= timeout_s:
                    timed_out = True
                    break
            if timed_out:
                break
        if not timed_out:
            return current, round_id
        reduced = int(current * reduction_factor)
        if reduced < min_n_samples:
            raise RuntimeError(
                f"Cannot satisfy timeout for n_features={n_features}. Last n_samples={current}."
            )
        current = reduced
        round_id += 1


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--common-params-path", required=True)
    parser.add_argument(
        "--output-json",
        default=None,
    )
    parser.add_argument(
        "--output-txt",
        default=None,
    )
    parser.add_argument("--artifacts-root", type=str, default=str(BASE_DIR / "artifacts"))
    parser.add_argument("--machine-tag", type=str, default=None)
    parser.add_argument("--timeout-s", type=float, default=10.0)
    parser.add_argument("--reduction-factor", type=float, default=0.8)
    parser.add_argument("--min-n-samples", type=int, default=50_000)
    parser.add_argument("--repeats", type=int, default=3)
    args = parser.parse_args()
    artifacts_dir = machine_artifacts_dir(
        base_dir=BASE_DIR,
        artifacts_root=args.artifacts_root,
        machine_tag=args.machine_tag,
    )
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    if args.output_json is None:
        args.output_json = str(artifacts_dir / "focused_scaling_aligned.json")
    if args.output_txt is None:
        args.output_txt = str(artifacts_dir / "focused_scaling_aligned.txt")

    common_params = json.loads(Path(args.common_params_path).read_text(encoding="utf-8"))
    common_json = json.dumps(common_params)
    datasets = [
        {"name": "medium_plus", "start_n_samples": 140_000, "n_features": 80},
        {"name": "larger", "start_n_samples": 220_000, "n_features": 100},
    ]
    thread_grid = [1, 2, 4]

    rows = []
    for dataset in datasets:
        n_samples, reduction_round = _find_shared_n_samples(
            start_n_samples=dataset["start_n_samples"],
            n_features=dataset["n_features"],
            timeout_s=args.timeout_s,
            reduction_factor=args.reduction_factor,
            min_n_samples=args.min_n_samples,
            common_params_json=common_json,
            thread_grid=thread_grid,
        )
        for model in MODELS:
            for threads in thread_grid:
                fit_times = []
                total_times = []
                r2_values = []
                rss_values = []
                for rep in range(args.repeats):
                    run = _single_run(
                        model=model,
                        n_samples=n_samples,
                        n_features=dataset["n_features"],
                        threads=threads,
                        timeout_s=args.timeout_s,
                        common_params_json=common_json,
                        seed=42 + rep,
                    )
                    fit_times.append(run["fit_seconds"])
                    total_times.append(run["total_seconds"])
                    r2_values.append(run["r2"])
                    rss_values.append(run["peak_rss_mb"])
                rows.append(
                    {
                        "dataset": dataset["name"],
                        "n_samples": n_samples,
                        "n_features": dataset["n_features"],
                        "reduction_round": reduction_round,
                        "model": model,
                        "threads": threads,
                        "fit_mean": statistics.mean(fit_times),
                        "fit_std": statistics.pstdev(fit_times),
                        "total_mean": statistics.mean(total_times),
                        "r2_mean": statistics.mean(r2_values),
                        "r2_std": statistics.pstdev(r2_values),
                        "peak_rss_mean_mb": statistics.mean(rss_values),
                        "repeats": args.repeats,
                    }
                )

    Path(args.output_json).write_text(json.dumps(rows, indent=2), encoding="utf-8")

    lines = []
    index = {}
    for row in rows:
        index[(row["dataset"], row["model"], row["threads"])] = row
    for dataset in sorted({r["dataset"] for r in rows}):
        sk1 = index[(dataset, "sklearn_hgb", 1)]
        sk4 = index[(dataset, "sklearn_hgb", 4)]
        l1 = index[(dataset, "lightgbm_hist", 1)]
        l4 = index[(dataset, "lightgbm_hist", 4)]
        lines.append(
            f"{dataset}\tsklearn_hgb\tn={sk1['n_samples']}\tf1={sk1['fit_mean']:.4f}\tf2={index[(dataset, 'sklearn_hgb', 2)]['fit_mean']:.4f}"
            f"\tf4={sk4['fit_mean']:.4f}\tspeedup1to4={sk1['fit_mean'] / sk4['fit_mean']:.3f}\teff={sk1['fit_mean'] / sk4['fit_mean'] / 4:.3f}"
            f"\tr2_t1={sk1['r2_mean']:.4f}\tr2_t4={sk4['r2_mean']:.4f}"
        )
        lines.append(
            f"{dataset}\tlightgbm_hist\tn={l1['n_samples']}\tf1={l1['fit_mean']:.4f}\tf2={index[(dataset, 'lightgbm_hist', 2)]['fit_mean']:.4f}"
            f"\tf4={l4['fit_mean']:.4f}\tspeedup1to4={l1['fit_mean'] / l4['fit_mean']:.3f}\teff={l1['fit_mean'] / l4['fit_mean'] / 4:.3f}"
            f"\tr2_t1={l1['r2_mean']:.4f}\tr2_t4={l4['r2_mean']:.4f}"
        )
        r2_gap = abs(sk1["r2_mean"] - l1["r2_mean"])
        lines.append(f"{dataset}\tr2_gap_t1\t{r2_gap:.6f}")

    Path(args.output_txt).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"output_json": args.output_json, "output_txt": args.output_txt, "n_rows": len(rows)}))


if __name__ == "__main__":
    main()
