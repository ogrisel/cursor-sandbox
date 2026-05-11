#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
from typing import Any


BASE_DIR = Path(__file__).resolve().parent

SKLEARN_MODELS = {"sklearn_hgb", "sklearn_hgb_fixed", "sklearn_hgb_adaptive"}
ALT_MODELS = {"lightgbm_hist", "xgboost_hist"}


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _setting_name_from_file(path: Path) -> str:
    stem = path.stem
    if stem == "benchmark_results":
        return "baseline_default"
    suffix = stem.removeprefix("benchmark_results_")
    return suffix or "baseline_default"


def _collect_setting_payloads(machine_dir: Path) -> dict[str, dict[str, Any]]:
    payloads: dict[str, dict[str, Any]] = {}
    for results_path in sorted(machine_dir.glob("benchmark_results*.json")):
        setting = _setting_name_from_file(results_path)
        summary_suffix = "" if setting == "baseline_default" else f"_{setting}"
        summary_path = machine_dir / f"benchmark_summary{summary_suffix}.json"
        payloads[setting] = {
            "results_path": results_path,
            "summary_path": summary_path,
            "results": _load_json(results_path),
            "summary": _load_json(summary_path) if summary_path.exists() else {},
        }
    return payloads


def _mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def _parity_rows(runs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = [r for r in runs if int(r["threads"]) == 1]
    return sorted(rows, key=lambda r: (str(r["dataset_name"]), str(r["model"])))


def _scalability_rows(runs: list[dict[str, Any]], core_threads: int) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str], dict[int, dict[str, Any]]] = {}
    for row in runs:
        key = (str(row["dataset_name"]), str(row["model"]))
        grouped.setdefault(key, {})[int(row["threads"])] = row
    out = []
    for (dataset, model), per_thread in sorted(grouped.items()):
        regular_threads = sorted(t for t in per_thread if t <= core_threads)
        if 1 not in per_thread or not regular_threads:
            continue
        max_threads = regular_threads[-1]
        base_fit = float(per_thread[1]["fit_seconds"])
        max_fit = float(per_thread[max_threads]["fit_seconds"])
        speedup = 0.0 if max_fit == 0 else base_fit / max_fit
        out.append(
            {
                "dataset": dataset,
                "model": model,
                "max_regular_threads": max_threads,
                "fit_s_1_thread": base_fit,
                "fit_s_regular_max_threads": max_fit,
                "speedup_1_to_regular_max": speedup,
            }
        )
    return out


def _oversubscription_rows(runs: list[dict[str, Any]], core_threads: int) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str], dict[int, dict[str, Any]]] = {}
    for row in runs:
        key = (str(row["dataset_name"]), str(row["model"]))
        grouped.setdefault(key, {})[int(row["threads"])] = row

    rows: list[dict[str, Any]] = []
    t2 = 2 * core_threads
    t4 = 4 * core_threads
    for (dataset, model), per_thread in sorted(grouped.items()):
        if core_threads not in per_thread:
            continue
        fit_core = float(per_thread[core_threads]["fit_seconds"])
        fit_2x = float(per_thread[t2]["fit_seconds"]) if t2 in per_thread else None
        fit_4x = float(per_thread[t4]["fit_seconds"]) if t4 in per_thread else None
        rows.append(
            {
                "dataset": dataset,
                "model": model,
                "core_threads": core_threads,
                "fit_s_cores": fit_core,
                "fit_s_2x_cores": fit_2x,
                "fit_s_4x_cores": fit_4x,
                "fit_ratio_2x_vs_cores": None if fit_2x is None else (fit_2x / fit_core),
                "fit_ratio_4x_vs_cores": None if fit_4x is None else (fit_4x / fit_core),
            }
        )
    return rows


def _infer_root_cause(machine_dir: Path) -> tuple[str, list[str]]:
    profile_summary_path = machine_dir / "profile_summary.json"
    if not profile_summary_path.exists():
        return (
            "Profile summary missing for sklearn; use benchmark symptom patterns only.",
            [
                "Add dedicated single-thread and multi-thread profile capture for sklearn and top alternative.",
                "Capture per-node work-size histograms to correlate overhead with node granularity.",
            ],
        )
    summary = _load_json(profile_summary_path)
    sklearn = summary.get("sklearn_hgb", {})
    leaf_entries = sklearn.get("speedscope_top_leaf", [])
    leaf_text = " ".join(str(row.get("leaf_frame", "")).lower() for row in leaf_entries)
    if any(k in leaf_text for k in ("omp", "pthread", "cond", "lock", "wait", "sleep")):
        return (
            "Native hotspots indicate synchronization/runtime overhead (OpenMP/pthread wait-heavy stacks).",
            [
                "Introduce adaptive thread gating based on node sample count and feature count.",
                "Batch multiple frontier nodes per parallel region to increase task granularity.",
                "Reduce barrier frequency by fusing short OpenMP regions in split/histogram paths.",
            ],
        )
    cprofile_entries = sklearn.get("cprofile_top", [])
    cprofile_text = " ".join(str(row.get("function", "")).lower() for row in cprofile_entries)
    if any(k in cprofile_text for k in ("python", "wrapper", "dispatch", "predict")):
        return (
            "Python-level dispatch/orchestration contributes meaningfully to sklearn runtime.",
            [
                "Move short-lived orchestration loops to Cython/C-level helpers.",
                "Preallocate and reuse temporary buffers in split and histogram kernels.",
                "Add lightweight fast paths for small-node splits to bypass heavy orchestration.",
            ],
        )
    return (
        "Underperformance likely combines tree-growth orchestration overhead and suboptimal threading granularity.",
        [
            "Instrument per-stage timings (binning, split search, partitioning) inside sklearn HGBT fit loop.",
            "Tune scheduling policy and chunk sizes to improve effective parallel work per task.",
            "Prototype fused split+partition kernels to reduce memory traffic.",
        ],
    )


def _identify_issues(runs: list[dict[str, Any]], core_threads: int) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    by_dataset = sorted({str(r["dataset_name"]) for r in runs})
    for dataset in by_dataset:
        rows = [r for r in runs if str(r["dataset_name"]) == dataset and int(r["threads"]) == 1]
        sk = [float(r["total_seconds"]) for r in rows if str(r["model"]) in SKLEARN_MODELS]
        alt = [float(r["total_seconds"]) for r in rows if str(r["model"]) in ALT_MODELS]
        if sk and alt:
            best_sk = min(sk)
            best_alt = min(alt)
            ratio = best_sk / best_alt if best_alt else 0.0
            if ratio > 1.05:
                issues.append(
                    {
                        "type": "single_thread",
                        "dataset": dataset,
                        "ratio": ratio,
                        "detail": f"Best sklearn total is {ratio:.3f}x slower than best alternative at thread=1.",
                    }
                )

    scalability = _scalability_rows(runs=runs, core_threads=core_threads)
    for dataset in by_dataset:
        rows = [r for r in scalability if r["dataset"] == dataset]
        sk_speed = [float(r["speedup_1_to_regular_max"]) for r in rows if r["model"] in SKLEARN_MODELS]
        alt_speed = [float(r["speedup_1_to_regular_max"]) for r in rows if r["model"] in ALT_MODELS]
        if sk_speed and alt_speed:
            best_sk = max(sk_speed)
            best_alt = max(alt_speed)
            gap = best_alt - best_sk
            if gap > 0.20:
                issues.append(
                    {
                        "type": "scalability",
                        "dataset": dataset,
                        "gap": gap,
                        "detail": f"Best sklearn speedup trails best alternative by {gap:.3f} (1->regular max threads).",
                    }
                )
    for dataset in by_dataset:
        rows_core = [r for r in runs if str(r["dataset_name"]) == dataset and int(r["threads"]) == core_threads]
        rows_4x = [r for r in runs if str(r["dataset_name"]) == dataset and int(r["threads"]) == 4 * core_threads]
        if not rows_core or not rows_4x:
            continue
        sk_core = [float(r["fit_seconds"]) for r in rows_core if str(r["model"]) in SKLEARN_MODELS]
        sk_4x = [float(r["fit_seconds"]) for r in rows_4x if str(r["model"]) in SKLEARN_MODELS]
        alt_core = [float(r["fit_seconds"]) for r in rows_core if str(r["model"]) in ALT_MODELS]
        alt_4x = [float(r["fit_seconds"]) for r in rows_4x if str(r["model"]) in ALT_MODELS]
        if sk_core and sk_4x and alt_core and alt_4x:
            sk_ratio = min(sk_4x) / min(sk_core)
            alt_ratio = min(alt_4x) / min(alt_core)
            if sk_ratio > alt_ratio + 0.15:
                issues.append(
                    {
                        "type": "oversubscription",
                        "dataset": dataset,
                        "detail": (
                            f"At 4x cores, sklearn fit-time ratio vs cores is {sk_ratio:.3f} "
                            f"vs {alt_ratio:.3f} for best alternative."
                        ),
                    }
                )
    return issues


def _table(rows: list[dict[str, Any]], columns: list[tuple[str, str]]) -> list[str]:
    lines = ["| " + " | ".join(c[1] for c in columns) + " |", "| " + " | ".join(["---"] * len(columns)) + " |"]
    for row in rows:
        vals: list[str] = []
        for key, _ in columns:
            value = row.get(key, "n/a")
            if value is None:
                vals.append("n/a")
            elif isinstance(value, float):
                vals.append(f"{value:.6g}")
            else:
                vals.append(str(value))
        lines.append("| " + " | ".join(vals) + " |")
    return lines


def _fmt_meta(value: Any) -> str:
    if value is None:
        return "n/a"
    if isinstance(value, str) and not value.strip():
        return "n/a"
    return str(value)


def _write_machine_analysis(machine_dir: Path, payloads: dict[str, dict[str, Any]]) -> Path:
    root_cause_text, root_cause_plan = _infer_root_cause(machine_dir)
    lines = [f"# Detailed platform analysis: {machine_dir.name}", ""]
    manifest_path = machine_dir / "run_manifest.json"
    core_threads = 1
    if manifest_path.exists():
        manifest = _load_json(manifest_path)
        core_threads = int(manifest.get("cpu_count", 1))
        cpu_info = manifest.get("cpu_info", {})
        lines.extend(
            [
                f"- System: `{_fmt_meta(manifest.get('system'))}`",
                f"- Architecture: `{_fmt_meta(manifest.get('architecture'))}`",
                f"- CPU count (logical): `{_fmt_meta(cpu_info.get('logical_cpu_count', core_threads))}`",
                f"- CPU count (physical): `{_fmt_meta(cpu_info.get('physical_cpu_count'))}`",
                f"- Hyper-threading enabled: `{_fmt_meta(cpu_info.get('hyperthreading_enabled'))}`",
                f"- CPU model: `{_fmt_meta(cpu_info.get('model_name'))}`",
                f"- Core type counts: `{_fmt_meta(cpu_info.get('core_type_counts'))}`",
                f"- CFS/CPU quota: `{_fmt_meta(cpu_info.get('cfs_quota'))}`",
                f"- CPU set: `{_fmt_meta(cpu_info.get('cpuset'))}`",
                f"- Thread grid: `{_fmt_meta(manifest.get('thread_grid'))}`",
                f"- Native profile enabled: `{_fmt_meta(manifest.get('native_profile_enabled'))}`",
                "",
            ]
        )

    for setting_name, payload in sorted(payloads.items()):
        runs = payload["results"]["runs"]
        parity = _parity_rows(runs)
        scalability = _scalability_rows(runs=runs, core_threads=core_threads)
        issues = _identify_issues(runs=runs, core_threads=core_threads)
        oversub = _oversubscription_rows(runs=runs, core_threads=core_threads)
        plot_suffix = "" if setting_name == "baseline_default" else f"_{setting_name}"
        scalability_plot = machine_dir / f"scalability{plot_suffix}.png"
        fit_time_plot = machine_dir / f"fit_time_threads{plot_suffix}.png"

        lines.extend([f"## Setting: `{setting_name}`", ""])
        if scalability_plot.exists():
            lines.extend([f"![scalability-{setting_name}]({scalability_plot.name})", ""])
        if fit_time_plot.exists():
            lines.extend([f"![absolute-fit-time-{setting_name}]({fit_time_plot.name})", ""])
            lines.extend(
                [
                    f"_Vertical markers denote `cores={core_threads}`, `2x={2 * core_threads}`, and `4x={4 * core_threads}` thread regimes._",
                    "",
                ]
            )

        lines.extend(["### Parity checks (thread=1)", ""])
        lines.extend(
            _table(
                parity,
                [
                    ("dataset_name", "dataset"),
                    ("model", "model"),
                    ("r2", "r2"),
                    ("fitted_trees", "fitted_trees"),
                    ("expected_trees", "expected_trees"),
                    ("fitted_trees_match_expected", "trees_match"),
                    ("total_nodes", "total_nodes"),
                    ("avg_nodes_per_tree", "avg_nodes_per_tree"),
                ],
            )
        )
        lines.append("")
        lines.extend([f"### Scalability summary (`1 -> cores={core_threads}`)", ""])
        lines.extend(
            _table(
                scalability,
                [
                    ("dataset", "dataset"),
                    ("model", "model"),
                    ("max_regular_threads", "max_regular_threads"),
                    ("fit_s_1_thread", "fit_s_1_thread"),
                    ("fit_s_regular_max_threads", "fit_s_regular_max_threads"),
                    ("speedup_1_to_regular_max", "speedup_1_to_regular_max"),
                ],
            )
        )
        lines.append("")
        lines.extend([f"### Oversubscription regime summary (`cores={core_threads}`, `2x`, `4x`)", ""])
        lines.extend(
            _table(
                oversub,
                [
                    ("dataset", "dataset"),
                    ("model", "model"),
                    ("fit_s_cores", "fit_s_cores"),
                    ("fit_s_2x_cores", "fit_s_2x_cores"),
                    ("fit_s_4x_cores", "fit_s_4x_cores"),
                    ("fit_ratio_2x_vs_cores", "fit_ratio_2x_vs_cores"),
                    ("fit_ratio_4x_vs_cores", "fit_ratio_4x_vs_cores"),
                ],
            )
        )
        lines.append("")
        if not issues:
            lines.extend(
                [
                    "### Underperformance findings",
                    "",
                    "- No material sklearn underperformance flags detected for this setting under current thresholds.",
                    "",
                ]
            )
            continue

        lines.extend(["### Underperformance findings and root cause analysis", ""])
        lines.append(f"- Root cause signal: {root_cause_text}")
        for issue in issues:
            lines.append(f"- Issue ({issue['type']}, dataset `{issue['dataset']}`): {issue['detail']}")
            lines.append("  - Implementation plan:")
            for step in root_cause_plan:
                lines.append(f"    - {step}")
        lines.append("")

    out_path = machine_dir / "detailed_analysis.md"
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out_path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifacts-root", default=str(BASE_DIR / "artifacts"))
    args = parser.parse_args()

    artifacts_root = Path(args.artifacts_root)
    machines_root = artifacts_root / "machines"
    machine_dirs = sorted([p for p in machines_root.iterdir() if p.is_dir()]) if machines_root.exists() else []
    if not machine_dirs:
        raise RuntimeError(f"No machine directories found in {machines_root}")

    report_paths: list[Path] = []
    for machine_dir in machine_dirs:
        setting_payloads = _collect_setting_payloads(machine_dir)
        if not setting_payloads:
            continue
        report_paths.append(_write_machine_analysis(machine_dir, setting_payloads))

    index_lines = ["# Platform detailed analyses", ""]
    for path in report_paths:
        rel = path.relative_to(artifacts_root)
        index_lines.append(f"- [{path.parent.name}](./{rel.as_posix()})")
    (artifacts_root / "platform_detailed_analysis_index.md").write_text("\n".join(index_lines) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "reports": [str(p) for p in report_paths],
                "index_md": str(artifacts_root / "platform_detailed_analysis_index.md"),
            }
        )
    )


if __name__ == "__main__":
    main()
