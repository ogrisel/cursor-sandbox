"""Benchmark stable GEMM fallback on translated float32 assignment data."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

import numpy as np
from array_api_compat import array_namespace
from bench_distance_formulations import (
    BACKENDS,
    _arrays,
    _broadcast_tile_n,
    _synchronize,
)
from bench_task_mix import HOME, _hwm_bytes

ROOT = Path(__file__).resolve().parents[1]
METHODS = ("gemm", "stable-1e-6", "stable-1e-2", "broadcast")
OFFSETS = (0.0, 10.0, 1000.0)
N_SAMPLES = 100_000
N_FEATURES = 32
N_CLUSTERS = 100


def _labels(args, X, centers, stats):
    from kmeans_lloyd.iteration import (
        assign_gemm_tiled,
        broadcast_scores_argmin,
        stable_gemm_scores_argmin,
    )
    from kmeans_lloyd.kmeans import _tile_schedule

    xp = array_namespace(X, centers)
    tiles = _tile_schedule(X, N_CLUSTERS)
    step = None
    if args.method == "broadcast":
        tiles["tile_n"] = min(
            tiles["tile_n"], _broadcast_tile_n(X, tiles["tile_k"])
        )

        def step(x_tile, c_tile, c_norm):
            return broadcast_scores_argmin(xp, x_tile, c_tile, c_norm)

    elif args.method.startswith("stable"):
        threshold = float(args.method.removeprefix("stable-"))

        def step(x_tile, c_tile, c_norm):
            return stable_gemm_scores_argmin(
                xp,
                x_tile,
                c_tile,
                c_norm,
                threshold=threshold,
                stats=stats,
            )

    labels = assign_gemm_tiled(
        X, centers, tiles["tile_n"], tiles["tile_k"], step=step
    )
    return labels, tiles


def worker(argv):
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument("--worker", action="store_true")
    parser.add_argument("--backend", choices=BACKENDS, required=True)
    parser.add_argument("--method", choices=METHODS, required=True)
    parser.add_argument("--offset", type=float, required=True)
    parser.add_argument("--seed", type=int, required=True)
    args = parser.parse_args(argv)

    rng = np.random.default_rng(args.seed)
    host = (rng.uniform(size=(N_SAMPLES, N_FEATURES)) + args.offset).astype(
        np.float32
    )
    centers_host = host[:N_CLUSTERS].copy()
    X, centers = _arrays(args.backend, host, centers_host)
    _synchronize(args.backend)
    # Compile/cache the selected GPU kernels outside the measurement.
    warm_stats = {}
    _labels(args, X[:256, :], centers, warm_stats)
    _synchronize(args.backend)

    stats = {}
    if args.backend == "torch-cpu":
        before = _hwm_bytes()
        started = time.perf_counter()
        labels, tiles = _labels(args, X, centers, stats)
        seconds = time.perf_counter() - started
        memory = max(0, _hwm_bytes() - before)
        meter = "vmhwm"
    else:
        from kmeans_lloyd.instrument import measure_call

        output, profile = measure_call(
            lambda: _labels(args, X, centers, stats), (), X
        )
        labels, tiles = output
        seconds = profile["seconds"]
        memory = profile["peak_extra_bytes"]
        meter = args.backend.split("-")[0] + "-pool"

    # Direct broadcast is the correctness reference and is outside timing.
    reference_args = argparse.Namespace(method="broadcast")
    reference, _ = _labels(reference_args, X, centers, {})
    from kmeans_lloyd.iteration import inertia

    objective = float(inertia(X, labels, centers)) / N_SAMPLES
    label_errors = int(np.count_nonzero(_host(labels) != _host(reference)))
    print(
        json.dumps(
            {
                "backend": args.backend,
                "method": args.method,
                "offset": args.offset,
                "seed": args.seed,
                "seconds": seconds,
                "mem_increment_bytes": memory,
                "mem_meter": meter,
                "inertia_per_point": objective,
                "label_errors": label_errors,
                "distance_pairs": stats.get("distance_pairs", 0),
                "recomputed_pairs": stats.get("recomputed_pairs", 0),
                "tile_n": tiles["tile_n"],
                "tile_k": tiles["tile_k"],
                "n_samples": N_SAMPLES,
                "n_features": N_FEATURES,
                "n_clusters": N_CLUSTERS,
            }
        ),
        flush=True,
    )


def _host(array):
    if hasattr(array, "get"):
        return array.get()
    if hasattr(array, "detach"):
        return array.detach().cpu().numpy()
    return np.asarray(array)


def _append(path, row):
    with path.open("a") as stream:
        stream.write(json.dumps(row) + "\n")


def drive(backends, methods, offsets, seeds, out):
    env = os.environ.copy()
    env.update(
        PYTHONPATH=str(ROOT / "src"),
        NVIDIA_TF32_OVERRIDE="0",
        OMP_NUM_THREADS="4",
        MKL_NUM_THREADS="4",
        OPENBLAS_NUM_THREADS="4",
    )
    remote_python = HOME / "kmeans_lloyd/.pixi/envs/default/bin/python"
    python = remote_python if remote_python.exists() else Path(sys.executable)
    for offset in offsets:
        for seed in seeds:
            for backend in backends:
                for method in methods:
                    command = [
                        str(python),
                        str(Path(__file__).resolve()),
                        "--worker",
                        "--backend",
                        backend,
                        "--method",
                        method,
                        "--offset",
                        str(offset),
                        "--seed",
                        str(seed),
                    ]
                    print(
                        f"start offset={offset:g} seed={seed} {backend} {method}",
                        flush=True,
                    )
                    completed = subprocess.run(
                        command,
                        cwd=ROOT,
                        env=env,
                        text=True,
                        capture_output=True,
                        timeout=60,
                        check=False,
                    )
                    lines = completed.stdout.strip().splitlines()
                    if completed.returncode or not lines:
                        row = {
                            "backend": backend,
                            "method": method,
                            "offset": offset,
                            "seed": seed,
                            "error": f"exit {completed.returncode}",
                            "stderr": completed.stderr[-2000:],
                        }
                        print(row["error"], flush=True)
                    else:
                        row = json.loads(lines[-1])
                        print(
                            f"  {row['seconds']:.4f}s "
                            f"errors={row['label_errors']}",
                            flush=True,
                        )
                    _append(out, row)


def main():
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument("--worker", action="store_true")
    parser.add_argument("--backends", default=",".join(BACKENDS))
    parser.add_argument("--methods", default=",".join(METHODS))
    parser.add_argument("--offsets", default=",".join(map(str, OFFSETS)))
    parser.add_argument("--seeds", default="0,1,2")
    parser.add_argument(
        "--out", type=Path, default=Path.home() / "cancellation-results.jsonl"
    )
    args, _ = parser.parse_known_args()
    if args.worker:
        worker(sys.argv[1:])
        return
    drive(
        [value for value in args.backends.split(",") if value],
        [value for value in args.methods.split(",") if value],
        [float(value) for value in args.offsets.split(",") if value],
        [int(value) for value in args.seeds.split(",") if value],
        args.out,
    )


if __name__ == "__main__":
    main()
