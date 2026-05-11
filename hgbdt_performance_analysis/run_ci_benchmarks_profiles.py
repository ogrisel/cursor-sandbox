#!/usr/bin/env python3
import argparse
import json
import os
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


def _resolve_thread_grid(requested_grid: list[int] | None) -> list[int]:
    if requested_grid:
        return sorted({max(1, int(t)) for t in requested_grid})
    cpu_count = max(1, os.cpu_count() or 1)
    return sorted({1, 2, cpu_count, 2 * cpu_count, 4 * cpu_count})


def _run_capture(cmd: list[str], timeout_s: float = 5.0) -> str | None:
    try:
        completed = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout_s, check=False)
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return None
    if completed.returncode != 0:
        return None
    return completed.stdout.strip()


def _linux_core_type_counts(logical_cpu_count: int) -> dict[str, int | None]:
    capacity_files = sorted(Path("/sys/devices/system/cpu").glob("cpu[0-9]*/cpu_capacity"))
    capacities: dict[int, int] = {}
    for path in capacity_files:
        try:
            value = int(path.read_text(encoding="utf-8").strip())
        except (ValueError, OSError):
            continue
        capacities[value] = capacities.get(value, 0) + 1
    if not capacities:
        return {"performance": logical_cpu_count, "efficiency": None, "low_power": None}
    sorted_caps = sorted(capacities.items(), key=lambda item: item[0], reverse=True)
    performance = sorted_caps[0][1] if len(sorted_caps) >= 1 else None
    efficiency = sorted_caps[1][1] if len(sorted_caps) >= 2 else None
    low_power = sum(count for _, count in sorted_caps[2:]) if len(sorted_caps) >= 3 else None
    return {"performance": performance, "efficiency": efficiency, "low_power": low_power}


def _linux_cgroup_quota() -> dict[str, Any] | None:
    cpu_max = Path("/sys/fs/cgroup/cpu.max")
    if cpu_max.exists():
        payload = cpu_max.read_text(encoding="utf-8").strip().split()
        if len(payload) == 2:
            quota_raw, period_raw = payload
            quota_us = None if quota_raw == "max" else int(quota_raw)
            period_us = int(period_raw)
            return {
                "controller": "cgroup_v2",
                "quota_us": quota_us,
                "period_us": period_us,
                "quota_cores": None if quota_us is None else (quota_us / period_us),
            }
    quota_path = Path("/sys/fs/cgroup/cpu/cpu.cfs_quota_us")
    period_path = Path("/sys/fs/cgroup/cpu/cpu.cfs_period_us")
    if quota_path.exists() and period_path.exists():
        quota = int(quota_path.read_text(encoding="utf-8").strip())
        period = int(period_path.read_text(encoding="utf-8").strip())
        quota_us = None if quota < 0 else quota
        return {
            "controller": "cgroup_v1",
            "quota_us": quota_us,
            "period_us": period,
            "quota_cores": None if quota_us is None else (quota_us / period),
        }
    return None


def _collect_cpu_info() -> dict[str, Any]:
    system = platform.system().strip().lower()
    logical = max(1, os.cpu_count() or 1)
    info: dict[str, Any] = {
        "system": platform.system(),
        "architecture": platform.machine(),
        "logical_cpu_count": logical,
        "physical_cpu_count": None,
        "hyperthreading_enabled": None,
        "core_type_counts": {"performance": None, "efficiency": None, "low_power": None},
        "cfs_quota": None,
        "cpuset": None,
        "model_name": None,
        "data_sources": [],
    }

    if system == "linux":
        lscpu_out = _run_capture(["lscpu"])
        cores_per_socket = None
        sockets = None
        if lscpu_out:
            info["data_sources"].append("lscpu")
            for line in lscpu_out.splitlines():
                lower = line.lower()
                if lower.startswith("model name:"):
                    info["model_name"] = line.split(":", 1)[1].strip()
                elif lower.startswith("core(s) per socket:"):
                    value = line.split(":", 1)[1].strip()
                    if value.isdigit():
                        cores_per_socket = int(value)
                elif lower.startswith("socket(s):"):
                    value = line.split(":", 1)[1].strip()
                    if value.isdigit():
                        sockets = int(value)
        phys_pairs = _run_capture(["lscpu", "-p=core,socket"])
        if phys_pairs:
            unique_pairs = {
                line.strip()
                for line in phys_pairs.splitlines()
                if line.strip() and not line.strip().startswith("#")
            }
            if unique_pairs:
                info["physical_cpu_count"] = len(unique_pairs)
        if info["physical_cpu_count"] is None and cores_per_socket and sockets:
            info["physical_cpu_count"] = cores_per_socket * sockets
        if info["physical_cpu_count"]:
            info["hyperthreading_enabled"] = logical > int(info["physical_cpu_count"])
        info["core_type_counts"] = _linux_core_type_counts(logical_cpu_count=logical)
        info["cfs_quota"] = _linux_cgroup_quota()
        cpuset_candidates = [Path("/sys/fs/cgroup/cpuset.cpus.effective"), Path("/sys/fs/cgroup/cpuset/cpuset.cpus")]
        for path in cpuset_candidates:
            if path.exists():
                info["cpuset"] = path.read_text(encoding="utf-8").strip() or None
                break
        return info

    if system == "darwin":
        info["data_sources"].append("sysctl")
        logical_out = _run_capture(["sysctl", "-n", "hw.logicalcpu"])
        physical_out = _run_capture(["sysctl", "-n", "hw.physicalcpu"])
        model_out = _run_capture(["sysctl", "-n", "machdep.cpu.brand_string"])
        if logical_out and logical_out.isdigit():
            info["logical_cpu_count"] = int(logical_out)
        if physical_out and physical_out.isdigit():
            info["physical_cpu_count"] = int(physical_out)
        if model_out:
            info["model_name"] = model_out
        p_cores = _run_capture(["sysctl", "-n", "hw.perflevel0.physicalcpu"])
        e_cores = _run_capture(["sysctl", "-n", "hw.perflevel1.physicalcpu"])
        l_cores = _run_capture(["sysctl", "-n", "hw.perflevel2.physicalcpu"])
        info["core_type_counts"] = {
            "performance": int(p_cores) if p_cores and p_cores.isdigit() else None,
            "efficiency": int(e_cores) if e_cores and e_cores.isdigit() else None,
            "low_power": int(l_cores) if l_cores and l_cores.isdigit() else None,
        }
        if info["physical_cpu_count"]:
            info["hyperthreading_enabled"] = int(info["logical_cpu_count"]) > int(info["physical_cpu_count"])
        return info

    if system == "windows":
        ps = _run_capture(
            [
                "powershell",
                "-NoProfile",
                "-Command",
                "Get-CimInstance Win32_Processor | Select-Object Name,NumberOfCores,NumberOfLogicalProcessors,ThreadCount | ConvertTo-Json -Compress",
            ],
            timeout_s=15.0,
        )
        if ps:
            info["data_sources"].append("powershell-cim")
            payload = json.loads(ps)
            if isinstance(payload, dict):
                payload = [payload]
            if isinstance(payload, list) and payload:
                cores = [int(row.get("NumberOfCores", 0)) for row in payload if row.get("NumberOfCores")]
                logicals = [int(row.get("NumberOfLogicalProcessors", 0)) for row in payload if row.get("NumberOfLogicalProcessors")]
                threads = [int(row.get("ThreadCount", 0)) for row in payload if row.get("ThreadCount")]
                if cores:
                    info["physical_cpu_count"] = sum(cores)
                if logicals:
                    info["logical_cpu_count"] = sum(logicals)
                if payload[0].get("Name"):
                    info["model_name"] = str(payload[0]["Name"]).strip()
                thread_count = sum(threads) if threads else int(info["logical_cpu_count"])
                phys = int(info["physical_cpu_count"]) if info["physical_cpu_count"] else 0
                info["hyperthreading_enabled"] = bool(phys and thread_count > phys)
        return info

    return info


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
    bars = ax.bar(model_labels, median_totals, color=["#4e79a7", "#f28e2b", "#59a14f", "#e15759"][: len(model_labels)])
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


def _write_fit_time_plot(benchmark_results_json: Path, output_png: Path, title: str, core_threads: int) -> None:
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
            threads = sorted(per_thread)
            fit_values = [float(per_thread[t]["fit_seconds"]) for t in threads]
            ax.plot(threads, fit_values, marker="o", label=model)
        for thread_value, label in [(core_threads, "cores"), (2 * core_threads, "2x"), (4 * core_threads, "4x")]:
            ax.axvline(thread_value, color="#777777", linestyle="--", linewidth=0.8, alpha=0.5)
            ax.text(thread_value, ax.get_ylim()[1], label, rotation=90, va="top", ha="center", fontsize=8, color="#666666")
        ax.set_title(dataset)
        ax.set_xlabel("Threads")
        ax.set_ylabel("Fit time (s)")
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
    core_threads: int,
    common_params: dict[str, Any] | None,
) -> dict[str, str]:
    suffix = "" if setting_name == "baseline_default" else f"_{setting_name}"
    benchmark_json = out_dir / f"benchmark_results{suffix}.json"
    benchmark_summary_json = out_dir / f"benchmark_summary{suffix}.json"
    benchmark_summary_md = out_dir / f"benchmark_report{suffix}.md"
    benchmark_rank_png = out_dir / f"benchmark_ranked_models{suffix}.png"
    scalability_png = out_dir / f"scalability{suffix}.png"
    fit_time_png = out_dir / f"fit_time_threads{suffix}.png"

    cmd = [
        sys.executable,
        str(BENCHMARK_SCRIPT),
        "benchmark",
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
    _write_ranked_models_plot(benchmark_summary_json=benchmark_summary_json, output_png=benchmark_rank_png, title=f"Per-machine model ranking ({setting_name})")
    _write_scalability_plot(benchmark_results_json=benchmark_json, output_png=scalability_png, title=f"Scalability by dataset ({setting_name})")
    _write_fit_time_plot(
        benchmark_results_json=benchmark_json,
        output_png=fit_time_png,
        title=f"Absolute fit time vs threads ({setting_name})",
        core_threads=core_threads,
    )
    return {
        "benchmark_json": str(benchmark_json),
        "benchmark_summary_json": str(benchmark_summary_json),
        "benchmark_summary_md": str(benchmark_summary_md),
        "benchmark_ranked_models_png": str(benchmark_rank_png),
        "scalability_png": str(scalability_png),
        "fit_time_threads_png": str(fit_time_png),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifacts-root", default=str(BASE_DIR / "artifacts"))
    parser.add_argument("--machine-tag", default=None)
    parser.add_argument("--timeout-s", type=float, default=4.0)
    parser.add_argument("--thread-grid", nargs="+", type=int, default=None)
    parser.add_argument("--benchmark-min-n-samples", type=int, default=5_000)
    parser.add_argument("--benchmark-reduction-factor", type=float, default=0.6)
    parser.add_argument("--profile-n-samples", type=int, default=40_000)
    parser.add_argument("--profile-n-features", type=int, default=80)
    parser.add_argument("--profile-threads", type=int, default=4)
    parser.add_argument("--profile-models", nargs="+", default=["sklearn_hgb", "lightgbm_hist"])
    parser.add_argument("--skip-alt-hparams", action="store_true")
    args = parser.parse_args()
    cpu_info = _collect_cpu_info()
    core_threads = int(cpu_info.get("logical_cpu_count") or max(1, os.cpu_count() or 1))
    thread_grid = _resolve_thread_grid(args.thread_grid)
    args.thread_grid = thread_grid

    out_dir = machine_artifacts_dir(base_dir=BASE_DIR, artifacts_root=args.artifacts_root, machine_tag=args.machine_tag)
    out_dir.mkdir(parents=True, exist_ok=True)

    settings: list[tuple[str, dict[str, Any] | None]] = [("baseline_default", None)]
    if not args.skip_alt_hparams:
        settings.append(("deep_few_trees", DEEP_FEW_TREES_PARAMS))

    setting_outputs: dict[str, dict[str, str]] = {}
    for setting_name, common_params in settings:
        setting_outputs[setting_name] = _run_benchmark_setting(
            setting_name=setting_name,
            out_dir=out_dir,
            args=args,
            core_threads=core_threads,
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
        "machine_tag": resolve_machine_tag(args.machine_tag),
        "system": platform.system(),
        "architecture": platform.machine(),
        "cpu_count": core_threads,
        "cpu_info": cpu_info,
        "thread_grid": thread_grid,
        "oversubscription_targets": {
            "cores": core_threads,
            "x2_cores": 2 * core_threads,
            "x4_cores": 4 * core_threads,
        },
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
