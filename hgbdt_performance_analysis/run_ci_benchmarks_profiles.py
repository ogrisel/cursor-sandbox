#!/usr/bin/env python3
import argparse
import json
import platform
import shutil
import subprocess
import sys
from pathlib import Path

from artifact_layout import machine_artifacts_dir, resolve_machine_tag


BASE_DIR = Path(__file__).resolve().parent
BENCHMARK_SCRIPT = BASE_DIR / "benchmark_gbdt_regressors.py"
ANALYZE_SCRIPT = BASE_DIR / "analyze_benchmark_results.py"
EXTRACT_SCRIPT = BASE_DIR / "extract_profile_insights.py"


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
                # Keep CI green on environments where native tracing is restricted.
                pass
    return payload


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
    args = parser.parse_args()

    out_dir = machine_artifacts_dir(
        base_dir=BASE_DIR,
        artifacts_root=args.artifacts_root,
        machine_tag=args.machine_tag,
    )
    out_dir.mkdir(parents=True, exist_ok=True)

    machine_tag = resolve_machine_tag(args.machine_tag)
    benchmark_json = out_dir / "benchmark_results.json"
    benchmark_summary_json = out_dir / "benchmark_summary.json"
    benchmark_summary_md = out_dir / "benchmark_report.md"
    profile_spec_json = out_dir / "profile_spec.json"
    profile_summary_json = out_dir / "profile_summary.json"
    profile_summary_md = out_dir / "profile_summary.md"

    _run(
        [
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
    )
    _run(
        [
            sys.executable,
            str(ANALYZE_SCRIPT),
            "--artifacts-root",
            args.artifacts_root,
            "--machine-tag",
            machine_tag,
            "--input-json",
            str(benchmark_json),
            "--output-json",
            str(benchmark_summary_json),
            "--output-md",
            str(benchmark_summary_md),
        ]
    )

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
            "--artifacts-root",
            args.artifacts_root,
            "--machine-tag",
            machine_tag,
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
        "outputs": {
            "benchmark_json": str(benchmark_json),
            "benchmark_summary_json": str(benchmark_summary_json),
            "benchmark_summary_md": str(benchmark_summary_md),
            "profile_spec_json": str(profile_spec_json),
            "profile_summary_json": str(profile_summary_json),
            "profile_summary_md": str(profile_summary_md),
        },
    }
    (out_dir / "run_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
