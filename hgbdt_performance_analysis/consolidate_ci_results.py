#!/usr/bin/env python3
import argparse
import json
import shutil
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean
from typing import Any


BASE_DIR = Path(__file__).resolve().parent


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _discover_artifact_dirs(downloaded_root: Path, artifact_prefix: str) -> list[tuple[str, Path]]:
    found: list[tuple[str, Path]] = []
    for entry in sorted(downloaded_root.iterdir()):
        if not entry.is_dir():
            continue
        if entry.name.startswith(artifact_prefix):
            machine_tag = entry.name[len(artifact_prefix) :]
            if machine_tag:
                found.append((machine_tag, entry))
                continue
        manifest_path = entry / "run_manifest.json"
        if manifest_path.exists():
            manifest = _load_json(manifest_path)
            machine_tag = str(manifest.get("machine_tag", "")).strip()
            if machine_tag:
                found.append((machine_tag, entry))
    deduped: dict[str, Path] = {}
    for machine_tag, path in found:
        deduped[machine_tag] = path
    return sorted(deduped.items())


def _copy_into_repo(machine_dirs: list[tuple[str, Path]], artifacts_root: Path) -> list[Path]:
    target_root = artifacts_root / "machines"
    target_root.mkdir(parents=True, exist_ok=True)
    written_dirs: list[Path] = []
    for machine_tag, source_dir in machine_dirs:
        target_dir = target_root / machine_tag
        if target_dir.exists():
            shutil.rmtree(target_dir)
        shutil.copytree(source_dir, target_dir)
        written_dirs.append(target_dir)
    return written_dirs


def _safe_ratio(num: float, den: float) -> float | None:
    if den == 0.0:
        return None
    return num / den


def _build_platform_summary(machine_dirs: list[Path]) -> dict[str, Any]:
    machines: list[dict[str, Any]] = []
    model_totals: dict[str, list[float]] = defaultdict(list)
    top_model_counter: Counter[str] = Counter()
    bottom_model_counter: Counter[str] = Counter()
    missing_files: list[str] = []

    for machine_dir in machine_dirs:
        manifest_path = machine_dir / "run_manifest.json"
        summary_path = machine_dir / "benchmark_summary.json"
        if not manifest_path.exists() or not summary_path.exists():
            missing_files.append(str(machine_dir))
            continue

        manifest = _load_json(manifest_path)
        summary = _load_json(summary_path)
        ranked_models = summary.get("ranked_models", [])
        if not ranked_models:
            missing_files.append(str(summary_path))
            continue

        top_model = str(ranked_models[0]["model"])
        bottom_model = str(ranked_models[-1]["model"])
        top_model_counter[top_model] += 1
        bottom_model_counter[bottom_model] += 1

        per_model_rows: list[dict[str, Any]] = []
        for row in ranked_models:
            model_name = str(row["model"])
            median_total_s = float(row["median_total_s"])
            model_totals[model_name].append(median_total_s)
            per_model_rows.append(
                {
                    "model": model_name,
                    "median_total_s": median_total_s,
                    "mean_total_s": float(row["mean_total_s"]),
                    "mean_r2": float(row["mean_r2"]),
                }
            )

        machines.append(
            {
                "machine_tag": str(manifest.get("machine_tag", machine_dir.name)),
                "system": str(manifest.get("system", "unknown")),
                "architecture": str(manifest.get("architecture", "unknown")),
                "native_profile_enabled": bool(manifest.get("native_profile_enabled", False)),
                "top_model": top_model,
                "bottom_model": bottom_model,
                "ranked_models": per_model_rows,
            }
        )

    model_variation_rows: list[dict[str, Any]] = []
    for model_name, totals in sorted(model_totals.items()):
        ratio = _safe_ratio(max(totals), min(totals))
        model_variation_rows.append(
            {
                "model": model_name,
                "machines_seen": len(totals),
                "mean_median_total_s": mean(totals),
                "best_median_total_s": min(totals),
                "worst_median_total_s": max(totals),
                "worst_to_best_ratio": ratio,
            }
        )

    return {
        "n_machines": len(machines),
        "machines": sorted(machines, key=lambda m: m["machine_tag"]),
        "top_model_counts": dict(top_model_counter),
        "bottom_model_counts": dict(bottom_model_counter),
        "model_variation": model_variation_rows,
        "missing_or_invalid_inputs": missing_files,
    }


def _format_ratio(value: float | None) -> str:
    if value is None:
        return "n/a"
    return f"{value:.3f}x"


def _write_platform_md(path: Path, payload: dict[str, Any]) -> None:
    machines = payload["machines"]
    lines = [
        "# Platform-specific benchmark conclusions",
        "",
        f"- Machines consolidated: **{payload['n_machines']}**",
        f"- Most frequent top model: `{max(payload['top_model_counts'], key=payload['top_model_counts'].get) if payload['top_model_counts'] else 'n/a'}`",
        "",
        "## Per-machine ranking winner/loser",
        "| machine_tag | system | architecture | top_model | slowest_model | native_profile_enabled |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for machine in machines:
        lines.append(
            f"| {machine['machine_tag']} | {machine['system']} | {machine['architecture']} | "
            f"{machine['top_model']} | {machine['bottom_model']} | {machine['native_profile_enabled']} |"
        )

    lines.extend(
        [
            "",
            "## Cross-platform model runtime variation",
            "| model | machines_seen | mean_median_total_s | best_median_total_s | worst_median_total_s | worst_to_best_ratio |",
            "| --- | --- | --- | --- | --- | --- |",
        ]
    )
    for row in payload["model_variation"]:
        lines.append(
            f"| {row['model']} | {row['machines_seen']} | {row['mean_median_total_s']:.6g} | "
            f"{row['best_median_total_s']:.6g} | {row['worst_median_total_s']:.6g} | {_format_ratio(row['worst_to_best_ratio'])} |"
        )

    top_model_counts = payload["top_model_counts"]
    if len(top_model_counts) > 1:
        lines.extend(
            [
                "",
                "## Conclusion",
                "- Fastest model varies by platform; keep platform-specific benchmark snapshots in `artifacts/machines/<machine-tag>/` before drawing global conclusions.",
                "- Use `model_variation.worst_to_best_ratio` from `platform_specific_summary.json` to track how sensitive each model is to OS/architecture changes.",
            ]
        )
    else:
        lines.extend(
            [
                "",
                "## Conclusion",
                "- Current consolidated runs show a stable top-ranked model across platforms, but per-model runtime ratios still vary and should be tracked per machine.",
            ]
        )

    missing = payload.get("missing_or_invalid_inputs", [])
    if missing:
        lines.extend(["", "## Skipped machine inputs", *[f"- `{entry}`" for entry in missing]])

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--downloaded-artifacts-root", required=True)
    parser.add_argument("--artifacts-root", default=str(BASE_DIR / "artifacts"))
    parser.add_argument("--artifact-prefix", default="benchmark-profiles-")
    parser.add_argument("--output-summary-json", default=None)
    parser.add_argument("--output-summary-md", default=None)
    args = parser.parse_args()

    downloaded_root = Path(args.downloaded_artifacts_root)
    artifacts_root = Path(args.artifacts_root)
    machine_sources = _discover_artifact_dirs(downloaded_root=downloaded_root, artifact_prefix=args.artifact_prefix)
    if not machine_sources:
        raise RuntimeError(
            f"No machine artifact directories found under {downloaded_root} "
            f"with prefix {args.artifact_prefix!r}."
        )
    machine_dirs = _copy_into_repo(machine_dirs=machine_sources, artifacts_root=artifacts_root)
    summary_json_path = (
        Path(args.output_summary_json)
        if args.output_summary_json is not None
        else artifacts_root / "platform_specific_summary.json"
    )
    summary_md_path = (
        Path(args.output_summary_md)
        if args.output_summary_md is not None
        else artifacts_root / "platform_specific_conclusions.md"
    )
    summary_json_path.parent.mkdir(parents=True, exist_ok=True)
    summary_md_path.parent.mkdir(parents=True, exist_ok=True)

    summary_payload = _build_platform_summary(machine_dirs=machine_dirs)
    summary_json_path.write_text(json.dumps(summary_payload, indent=2), encoding="utf-8")
    _write_platform_md(path=summary_md_path, payload=summary_payload)
    print(
        json.dumps(
            {
                "machines_written": [str(path) for path in machine_dirs],
                "summary_json": str(summary_json_path),
                "summary_md": str(summary_md_path),
                "n_machines": summary_payload["n_machines"],
            }
        )
    )


if __name__ == "__main__":
    main()
