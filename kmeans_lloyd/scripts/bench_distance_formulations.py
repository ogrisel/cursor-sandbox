"""Compare tiled GEMM and broadcast distances in KMeans end to end.

The three phases are greedy k-means++ alone, 12 Lloyd iterations from shared
random rows, and k-means++ followed by those Lloyd iterations. Workers are
fresh processes with a 60-second timeout. Broadcast tiles cap the 3D
``(tile_n, tile_k, n_features)`` difference tensor at 128 MiB.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

import numpy as np
from bench_task_mix import (
    HOME,
    MAX_ITER,
    TASKS,
    TOL,
    _hwm_bytes,
    _mean_inertia,
    _to_numpy,
    generate,
    save_random_start,
)

ROOT = Path(__file__).resolve().parents[1]
TIMEOUT = 60
BROADCAST_TILE_BYTES = 128 * 2**20
BACKENDS = ("torch-cpu", "torch-cuda", "cupy")
METHODS = ("gemm", "broadcast")
PHASES = ("init", "lloyd", "fit")


def _broadcast_tile_n(X, tile_k):
    itemsize = np.dtype(str(X.dtype).removeprefix("torch.")).itemsize
    elements_per_row = max(1, tile_k * int(X.shape[1]))
    return max(
        1,
        min(
            int(X.shape[0]),
            BROADCAST_TILE_BYTES // (itemsize * elements_per_row),
        ),
    )


def _arrays(backend, samples, centers):
    if backend.startswith("torch"):
        import torch

        torch.set_num_threads(4)
        device = "cuda" if backend == "torch-cuda" else "cpu"
        if device == "cuda":
            torch.backends.cuda.matmul.allow_tf32 = False
            torch.backends.cudnn.allow_tf32 = False
        return (
            torch.as_tensor(samples, device=device),
            torch.as_tensor(centers, device=device),
        )
    import cupy

    return cupy.asarray(samples), cupy.asarray(centers)


def _synchronize(backend):
    if backend == "torch-cuda":
        import torch

        torch.cuda.synchronize()
    elif backend == "cupy":
        import cupy

        cupy.cuda.Stream.null.synchronize()


def _distance_hooks(X, method, tile_n, tile_k, n_clusters):
    if method == "gemm":
        return None, None, tile_n

    from array_api_compat import array_namespace

    from kmeans_lloyd.iteration import (
        broadcast_distances_to_candidates_tiled,
        broadcast_scores_argmin,
    )

    xp = array_namespace(X)
    assign_tile_n = min(tile_n, _broadcast_tile_n(X, tile_k))
    def step(x_tile, c_tile, c_norm):
        return broadcast_scores_argmin(xp, x_tile, c_tile, c_norm)

    def distance(xp, data, x_norm, candidates):
        return broadcast_distances_to_candidates_tiled(
            xp,
            data,
            x_norm,
            candidates,
            _broadcast_tile_n(data, int(candidates.shape[0])),
        )

    return step, distance, assign_tile_n


def _fit(X, centers, rng, tiles, step, accumulate):
    from kmeans_lloyd.iteration import assign_gemm_tiled, fit_lloyd, inertia

    result = fit_lloyd(
        X,
        centers,
        max_iter=MAX_ITER,
        tol=TOL,
        tile_n=tiles["tile_n"],
        tile_k=tiles["tile_k"],
        update_tile_n=tiles["update_tile_n"],
        update_tile_k=tiles["update_tile_k"],
        reassign_empty=True,
        rng=rng,
        step=step,
        accumulate=accumulate,
    )
    labels = assign_gemm_tiled(
        X,
        result["centers"],
        tiles["tile_n"],
        tiles["tile_k"],
        step=step,
    )
    objective = float(inertia(X, labels, result["centers"], tiles["tile_n"]))
    return result["centers"], result["n_iter"], objective


def _call(args, X, fixed):
    from kmeans_lloyd.backends import native_accumulate
    from kmeans_lloyd.iteration import kmeans_plusplus
    from kmeans_lloyd.kmeans import _tile_schedule

    tiles = _tile_schedule(X, args.k)
    step, distance, tiles["tile_n"] = _distance_hooks(
        X, args.method, tiles["tile_n"], tiles["tile_k"], args.k
    )
    accumulate = native_accumulate(X, args.k)
    rng = np.random.default_rng(args.seed)

    if args.phase == "init":
        centers, _ = kmeans_plusplus(X, args.k, rng, distance=distance)
        return centers, 0, None, tiles
    if args.phase == "lloyd":
        centers, n_iter, objective = _fit(
            X, fixed, rng, tiles, step, accumulate
        )
        return centers, n_iter, objective, tiles
    centers, _ = kmeans_plusplus(X, args.k, rng, distance=distance)
    centers, n_iter, objective = _fit(
        X, centers, rng, tiles, step, accumulate
    )
    return centers, n_iter, objective, tiles


def _warm_gpu(args, X, fixed):
    if args.backend == "torch-cpu":
        return
    from array_api_compat import array_namespace

    from kmeans_lloyd.iteration import (
        _distances_to_candidates,
        broadcast_distances_to_candidates_tiled,
        broadcast_scores_argmin,
        gemm_scores_argmin,
    )

    xp = array_namespace(X)
    x = X[:128, :]
    c = fixed[: min(args.k, 8), :]
    c_norm = xp.sum(c * c, axis=1)
    if args.method == "gemm":
        gemm_scores_argmin(xp, x, c, c_norm)
        _distances_to_candidates(xp, x, xp.sum(x * x, axis=1), c)
    else:
        broadcast_scores_argmin(xp, x, c, c_norm)
        broadcast_distances_to_candidates_tiled(
            xp, x, xp.sum(x * x, axis=1), c, 128
        )
    _synchronize(args.backend)


def worker(argv):
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument("--worker", action="store_true")
    parser.add_argument("--backend", choices=BACKENDS, required=True)
    parser.add_argument("--method", choices=METHODS, required=True)
    parser.add_argument("--phase", choices=PHASES, required=True)
    parser.add_argument("--data", required=True)
    parser.add_argument("--centers", required=True)
    parser.add_argument("--k", type=int, required=True)
    parser.add_argument("--seed", type=int, required=True)
    args = parser.parse_args(argv)

    samples = np.load(args.data, mmap_mode="r")
    centers0 = np.load(args.centers)
    X, fixed = _arrays(args.backend, samples, centers0)
    _synchronize(args.backend)
    _warm_gpu(args, X, fixed)

    if args.backend == "torch-cpu":
        before = _hwm_bytes()
        started = time.perf_counter()
        centers, n_iter, objective, tiles = _call(args, X, fixed)
        seconds = time.perf_counter() - started
        memory = max(0, _hwm_bytes() - before)
        meter = "vmhwm"
    else:
        from kmeans_lloyd.instrument import measure_call

        output, profile = measure_call(
            lambda: _call(args, X, fixed), (), X
        )
        centers, n_iter, objective, tiles = output
        seconds = profile["seconds"]
        memory = profile["peak_extra_bytes"]
        meter = args.backend.split("-")[0] + "-pool"

    if objective is None:
        objective = _mean_inertia(samples, _to_numpy(centers)) * len(samples)
    print(
        json.dumps(
            {
                "backend": args.backend,
                "method": args.method,
                "phase": args.phase,
                "seed": args.seed,
                "k": args.k,
                "seconds": seconds,
                "mem_increment_bytes": memory,
                "mem_meter": meter,
                "inertia_per_point": objective / len(samples),
                "n_iter": n_iter,
                "tile_n": tiles["tile_n"],
                "tile_k": tiles["tile_k"],
                "broadcast_tile_bytes": BROADCAST_TILE_BYTES,
            }
        ),
        flush=True,
    )


def _append(path, row):
    with path.open("a") as stream:
        stream.write(json.dumps(row) + "\n")


def _tail_text(value, size):
    if isinstance(value, bytes):
        value = value.decode(errors="replace")
    return (value or "")[-size:]


def drive(tasks, backends, methods, phases, seeds, out):
    data_dir = HOME / "task-mix-data-v4"
    env = os.environ.copy()
    env.update(
        PYTHONPATH=str(ROOT / "src"),
        NVIDIA_TF32_OVERRIDE="0",
        OMP_NUM_THREADS="4",
        MKL_NUM_THREADS="4",
        OPENBLAS_NUM_THREADS="4",
    )
    python = HOME / "kmeans_lloyd/.pixi/envs/default/bin/python"
    for task in TASKS:
        if tasks and task["name"] not in tasks:
            continue
        data_path = data_dir / f"{task['name']}.npy"
        generate(task, data_path)
        for seed in seeds:
            _, centers_path = save_random_start(data_path, task, seed)
            ordered_methods = list(methods)
            if seed % 2:
                ordered_methods.reverse()
            for phase in phases:
                for backend in backends:
                    for method in ordered_methods:
                        command = [
                            str(python),
                            str(Path(__file__).resolve()),
                            "--worker",
                            "--backend",
                            backend,
                            "--method",
                            method,
                            "--phase",
                            phase,
                            "--data",
                            str(data_path),
                            "--centers",
                            str(centers_path),
                            "--k",
                            str(task["k"]),
                            "--seed",
                            str(seed),
                        ]
                        print(
                            f"start {task['name']} seed={seed} {phase} "
                            f"{backend} {method}",
                            flush=True,
                        )
                        started = time.perf_counter()
                        try:
                            completed = subprocess.run(
                                command,
                                cwd=ROOT,
                                env=env,
                                text=True,
                                capture_output=True,
                                timeout=TIMEOUT,
                                check=False,
                            )
                        except subprocess.TimeoutExpired as error:
                            row = {
                                "task": task,
                                "seed": seed,
                                "backend": backend,
                                "method": method,
                                "phase": phase,
                                "error": "timeout",
                                "timeout_seconds": TIMEOUT,
                                "stderr": _tail_text(error.stderr, 1000),
                            }
                            _append(out, row)
                            print("  timeout", flush=True)
                            continue
                        lines = completed.stdout.strip().splitlines()
                        if completed.returncode or not lines:
                            row = {
                                "task": task,
                                "seed": seed,
                                "backend": backend,
                                "method": method,
                                "phase": phase,
                                "error": f"exit {completed.returncode}",
                                "stderr": _tail_text(completed.stderr, 2000),
                            }
                            _append(out, row)
                            print(f"  exit {completed.returncode}", flush=True)
                            continue
                        row = json.loads(lines[-1])
                        row["task"] = task
                        row["wall_seconds"] = time.perf_counter() - started
                        _append(out, row)
                        print(
                            f"  {row['seconds']:.3f}s "
                            f"inertia={row['inertia_per_point']:.6g}",
                            flush=True,
                        )


def main():
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument("--worker", action="store_true")
    parser.add_argument("--tasks", default="")
    parser.add_argument("--backends", default=",".join(BACKENDS))
    parser.add_argument("--methods", default=",".join(METHODS))
    parser.add_argument("--phases", default=",".join(PHASES))
    parser.add_argument("--seeds", default="0,1,2")
    parser.add_argument("--out", default=str(HOME / "distance-results.jsonl"))
    args, _ = parser.parse_known_args()
    if args.worker:
        worker(sys.argv[1:])
        return
    drive(
        {value for value in args.tasks.split(",") if value},
        [value for value in args.backends.split(",") if value],
        [value for value in args.methods.split(",") if value],
        [value for value in args.phases.split(",") if value],
        [int(value) for value in args.seeds.split(",") if value],
        Path(args.out),
    )


if __name__ == "__main__":
    main()
