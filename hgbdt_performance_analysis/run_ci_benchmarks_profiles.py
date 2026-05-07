#!/usr/bin/env python3
import argparse
import json
import platform
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

import matplotlib

from artifact_layout import machine_artifacts_dir, resolve_machine_tag

matplotlib.use("Agg")
import matplotlib.pyplot as plt


BASE_DIR = Path(__file__).resolve().parent
BENCHMARK_SCRIPT = BASE_DIR / "benchmark_gbdt_regressors.py"
ANALYZE_SCRIPT = BASE_DIR / "analyze_benchmark_results.py"
EXTRACT_SCRIPT = BASE_DIR / "extract_profile_insights.py"

DEEP_FEW_TREES_PARAMS = {
    "loss": "squared_error",
    "n_estimators": 48,
    "learning_rate": 0.08,
    "max_depth": 10,
    "num_leaves": 127,
    "max_bin": 255,
    "subsample": 1.0,
    "l2_regularization": 2.0,
    "min_samples_leaf": 20,
    "min_child_weight": 20.0,
    "min_split_gain": 0.0,
    "random_state": 42,
}


def _run(cmd: list[str]) -> str:
    completed = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if completed.returncode != 0:
        raise RuntimeError(
            "Command failed:\n"
            + " ".join(cmd)
            + f"\nstdout:\n{completed.stdout}\nstderr:\n{completed.stderr}"
        )
    return completed.stdout


def _profile_once(
    model: str,
    out_dir: Path,
    n_samples: int,
    n_features: int,
    threads: int,
    native_enabled: bool,
) -> dict[str, str]:
    profile_dir = out_dir / "profiles"
    profile_dir.mkdir(parents=True, exist_ok=True)
    cprofile_path = profile_dir / f"{model}.pstats"
    base_cmd = [
        str(BENCHMARK_SCRIPT),
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
        "42",
    ]
    _run([sys.executable, "-m", "cProfile", "-o", str(cprofile_path), *base_cmd])
    payload: dict[str, str] = {"cprofile": str(cprofile_path)}

    if native_enabled:
        py_spy = shutil.which("py-spy")
        speedscope_path = profile_dir / f"{model}.speedscope.json"
        if py_spy:
            try:
                _run(
                    [
                        py_spy,
                        "record",
                        "--format",
                        "speedscope",
                        "--output",
                        str(speedscope_path),
                        "--",
                        sys.executable,
                        *base_cmd,
                    ]
                )
                payload["speedscope"] = str(speedscope_path)
            except RuntimeError:
                pass
    return payload


def _write_ranked_models_plot(benchmark_summary_json: Path, output_png: Path, title: str) -> None:
    summary = json.loads(benchmark_summary_json.read_text(encoding="utf-8"))
    ranked = summary.get("ranked_models", [])
    if not ranked:
        return
    model_labels = [str(row["model"]) for row in ranked]
    median_totals = [float(row["median_total_s"]) for row in ranked]
    fig, ax = plt.subplots(figsize=(8, 4.5))
    bars = ax.bar(
        model_labels,
        median_totals,
        color=["#4e79a7", "#f28e2b", "#59a14f", "#e15759"][: len(model_labels)],
    )
    ax.set_ylabel("Median total time (s)")
    ax.set_title(title)
    ax.grid(axis="y", alpha=0.25)
    for bar, value in zip(bars, median_totals):
        ax.text(bar.get_x() + bar.get_width() / 2, value, f"{value:.3f}", ha="center", va="bottom", fontsize=9)
    fig.tight_layout()
    output_png.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_png, dpi=160)
    plt.close(fig)


def _write_scalability_plot(benchmark_results_json: Path, output_png: Path, title: str) -> None:
    payload = json.loads(benchmark_results_json.read_text(encoding="utf-8"))
    runs = payload.get("runs", [])
    by_dataset: dict[str, list[dict[str, Any]]] = {}
    for run in runs:
        by_dataset.setdefault(str(run["dataset_name"]), []).append(run)
    if not by_dataset:
        return

    datasets = sorted(by_dataset)
    fig, axes = plt.subplots(1, len(datasets), figsize=(6 * len(datasets), 4.5), squeeze=False)
    for idx, dataset in enumerate(datasets):
        ax = axes[0][idx]
        rows = by_dataset[dataset]
        model_thread: dict[str, dict[int, dict[str, Any]]] = {}
        for row in rows:
            model = str(row["model"])
            thread = int(row["threads"])
            model_thread.setdefault(model, {})[thread] = row
        for model, per_thread in sorted(model_thread.items()):
            if 1 not in per_thread:
                continue
            threads = sorted(per_thread)
            baseline = float(per_thread[1]["fit_seconds"])
            speedup = [baseline / float(per_thread[t]["fit_seconds"]) for t in threads]
            ax.plot(threads, speedup, marker="o", label=model)
        ax.set_title(dataset)
        ax.set_xlabel("Threads")
        ax.set_ylabel("Fit speedup vs 1-thread")
        ax.grid(alpha=0.3)
    handles, labels = axes[0][0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=min(4, max(1, len(labels))), frameon=False)
    fig.suptitle(title)
    fig.tight_layout(rect=(0, 0.07, 1, 0.94))
    output_png.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_png, dpi=160)
    plt.close(fig)


def _run_benchmark_setting(
    setting_name: str,
    out_dir: Path,
    args: argparse.Namespace,
    machine_tag: str,
    common_params: dict[str, Any] | None,
) -> dict[str, str]:
    suffix = "" if setting_name == "baseline_default" else f"_{setting_name}"
    benchmark_json = out_dir / f"benchmark_results{suffix}.json"
    benchmark_summary_json = out_dir / f"benchmark_summary{suffix}.json"
    benchmark_summary_md = out_dir / f"benchmark_report{suffix}.md"
    benchmark_rank_png = out_dir / f"benchmark_ranked_models{suffix}.png"
    scalability_png = out_dir / f"scalability{suffix}.png"

    cmd = [
        sys.executable,
        str(BENCHMARK_SCRIPT),
        "benchmark",
        "--artifacts-root",
        args.artifacts_root,
        "--machine-tag",
        machine_tag,
        "--output-json",
        str(benchmark_json),
        "--timeout-s",
        str(args.timeout_s),
        "--thread-grid",
        *[str(t) for t in sorted(set(args.thread_grid))],
        "--min-n-samples",
        str(args.benchmark_min_n_samples),
        "--reduction-factor",
        str(args.benchmark_reduction_factor),
    ]
    if common_params is not None:
        cmd.extend(["--common-params-json", json.dumps(common_params, sort_keys=True)])
    _run(cmd)
    _run(
        [
            sys.executable,
            str(ANALYZE_SCRIPT),
            "--input-json",
            str(benchmark_json),
            "--output-json",
            str(benchmark_summary_json),
            "--output-md",
            str(benchmark_summary_md),
        ]
    )
    _write_ranked_models_plot(
        benchmark_summary_json=benchmark_summary_json,
        output_png=benchmark_rank_png,
        title=f"Per-machine model ranking ({setting_name})",
    )
    _write_scalability_plot(
        benchmark_results_json=benchmark_json,
        output_png=scalability_png,
        title=f"Scalability by dataset ({setting_name})",
    )
    return {
        "benchmark_json": str(benchmark_json),
        "benchmark_summary_json": str(benchmark_summary_json),
        "benchmark_summary_md": str(benchmark_summary_md),
        "benchmark_ranked_models_png": str(benchmark_rank_png),
        "scalability_png": str(scalability_png),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifacts-root", default=str(BASE_DIR / "artifacts"))
    parser.add_argument("--machine-tag", default=None)
    parser.add_argument("--timeout-s", type=float, default=4.0)
    parser.add_argument("--thread-grid", nargs="+", type=int, default=[1, 2, 4])
    parser.add_argument("--benchmark-min-n-samples", type=int, default=5_000)
    parser.add_argument("--benchmark-reduction-factor", type=float, default=0.6)
    parser.add_argument("--profile-n-samples", type=int, default=40_000)
    parser.add_argument("--profile-n-features", type=int, default=80)
    parser.add_argument("--profile-threads", type=int, default=4)
    parser.add_argument("--profile-models", nargs="+", default=["sklearn_hgb", "lightgbm_hist"])
    parser.add_argument("--skip-alt-hparams", action="store_true")
    args = parser.parse_args()

    out_dir = machine_artifacts_dir(
        base_dir=BASE_DIR,
        artifacts_root=args.artifacts_root,
        machine_tag=args.machine_tag,
    )
    out_dir.mkdir(parents=True, exist_ok=True)

    machine_tag = resolve_machine_tag(args.machine_tag)

    settings: list[tuple[str, dict[str, Any] | None]] = [("baseline_default", None)]
    if not args.skip_alt_hparams:
        settings.append(("deep_few_trees", DEEP_FEW_TREES_PARAMS))

    setting_outputs: dict[str, dict[str, str]] = {}
    for setting_name, common_params in settings:
        setting_outputs[setting_name] = _run_benchmark_setting(
            setting_name=setting_name,
            out_dir=out_dir,
            args=args,
            machine_tag=machine_tag,
            common_params=common_params,
        )

    baseline_outputs = setting_outputs["baseline_default"]
    profile_spec_json = out_dir / "profile_spec.json"
    profile_summary_json = out_dir / "profile_summary.json"
    profile_summary_md = out_dir / "profile_summary.md"

    native_enabled = platform.system().strip().lower() != "windows"
    profile_spec: dict[str, dict[str, str]] = {}
    for model in args.profile_models:
        profile_spec[model] = _profile_once(
            model=model,
            out_dir=out_dir,
            n_samples=args.profile_n_samples,
            n_features=args.profile_n_features,
            threads=args.profile_threads,
            native_enabled=native_enabled,
        )
    profile_spec_json.write_text(json.dumps(profile_spec, indent=2), encoding="utf-8")
    _run(
        [
            sys.executable,
            str(EXTRACT_SCRIPT),
            "--spec-json",
            str(profile_spec_json),
            "--output-json",
            str(profile_summary_json),
            "--output-md",
            str(profile_summary_md),
        ]
    )

    manifest = {
        "machine_tag": machine_tag,
        "system": platform.system(),
        "architecture": platform.machine(),
        "native_profile_enabled": native_enabled,
        "settings": setting_outputs,
        "outputs": {
            **baseline_outputs,
            "profile_spec_json": str(profile_spec_json),
            "profile_summary_json": str(profile_summary_json),
            "profile_summary_md": str(profile_summary_md),
        },
    }
    (out_dir / "run_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
