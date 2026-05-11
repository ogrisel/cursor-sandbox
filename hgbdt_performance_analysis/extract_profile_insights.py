#!/usr/bin/env python3
import argparse
import json
import pstats
from collections import Counter
from pathlib import Path

from artifact_layout import machine_artifacts_dir


BASE_DIR = Path(__file__).resolve().parent


def _cprofile_top(pstats_path: str, n: int) -> list[dict]:
    stats = pstats.Stats(pstats_path)
    rows = []
    for (filename, line, func), values in sorted(
        stats.stats.items(), key=lambda kv: kv[1][3], reverse=True
    )[:n]:
        cc, nc, tt, ct, _ = values
        rows.append(
            {
                "function": f"{filename}:{line}:{func}",
                "primitive_calls": cc,
                "total_calls": nc,
                "total_time_s": tt,
                "cumulative_time_s": ct,
            }
        )
    return rows


def _speedscope_top(speedscope_path: str, n: int) -> list[dict]:
    payload = json.loads(Path(speedscope_path).read_text(encoding="utf-8"))
    frames = payload["shared"]["frames"]
    counter: Counter[str] = Counter()
    for profile in payload.get("profiles", []):
        samples = profile.get("samples", [])
        weights = profile.get("weights")
        if weights is None:
            weights = [1] * len(samples)
        for stack, weight in zip(samples, weights):
            if not stack:
                continue
            leaf_idx = stack[-1]
            frame_name = frames[leaf_idx]["name"]
            counter[frame_name] += weight

    top = counter.most_common(n)
    return [{"leaf_frame": frame, "sample_weight": weight} for frame, weight in top]


def _write_md(path: str, payload: dict) -> None:
    lines = ["# Profiling snapshots", ""]
    for model, entries in payload.items():
        lines.append(f"## {model}")
        if "cprofile_top" in entries:
            lines.append("### Python-level (cProfile) top cumulative entries")
            lines.append("| function | primitive_calls | total_calls | total_time_s | cumulative_time_s |")
            lines.append("| --- | --- | --- | --- | --- |")
            for row in entries["cprofile_top"]:
                lines.append(
                    f"| {row['function']} | {row['primitive_calls']} | {row['total_calls']} | "
                    f"{row['total_time_s']:.6g} | {row['cumulative_time_s']:.6g} |"
                )
        if "speedscope_top_leaf" in entries:
            lines.append("")
            lines.append("### Native/C/C++/Cython-flavored stack leaf hotspots (py-spy --native)")
            lines.append("| leaf_frame | sample_weight |")
            lines.append("| --- | --- |")
            for row in entries["speedscope_top_leaf"]:
                lines.append(f"| {row['leaf_frame']} | {row['sample_weight']:.6g} |")
        lines.append("")
    Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--spec-json", required=True, help="JSON mapping model->profile files")
    parser.add_argument("--output-json", default=None)
    parser.add_argument("--output-md", default=None)
    parser.add_argument("--artifacts-root", type=str, default=str(BASE_DIR / "artifacts"))
    parser.add_argument("--machine-tag", type=str, default=None)
    parser.add_argument("--top-n", type=int, default=12)
    args = parser.parse_args()
    artifacts_dir = machine_artifacts_dir(
        base_dir=BASE_DIR,
        artifacts_root=args.artifacts_root,
        machine_tag=args.machine_tag,
    )
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    if args.output_json is None:
        args.output_json = str(artifacts_dir / "profile_summary.json")
    if args.output_md is None:
        args.output_md = str(artifacts_dir / "profile_summary.md")

    spec = json.loads(Path(args.spec_json).read_text(encoding="utf-8"))
    out: dict = {}
    for model, profile_files in spec.items():
        model_out = {}
        cprofile_path = profile_files.get("cprofile")
        speedscope_path = profile_files.get("speedscope")
        if cprofile_path:
            model_out["cprofile_top"] = _cprofile_top(cprofile_path, args.top_n)
        if speedscope_path:
            model_out["speedscope_top_leaf"] = _speedscope_top(speedscope_path, args.top_n)
        out[model] = model_out

    Path(args.output_json).write_text(json.dumps(out, indent=2), encoding="utf-8")
    _write_md(args.output_md, out)
    print(json.dumps({"output_json": args.output_json, "output_md": args.output_md}))


if __name__ == "__main__":
    main()
