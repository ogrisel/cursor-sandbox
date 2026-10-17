"""Benchmark backend-agnostic CPU optimization controls for KMeans."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

import numpy as np
from array_api_compat import array_namespace, device
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
SCORE_BUDGET = 128 * 2**20
METHODS = (
    "legacy",
    "baseline",
    "full-k",
    "wide-k",
    "interleaved",
    "hierarchical",
    "combined",
    "compiled",
    "n256-kall",
    "n1024-kall",
    "n4096-kall",
    "n8192-k256",
    "n16384-k256",
    "n4096-k512",
    "homogeneous",
    "homogeneous-lloyd",
    "tuned",
    "interleaved-tuned",
    "compiled-tuned",
    "fused-stats",
)
PHASES = ("init", "lloyd", "fit")


def _tiles(X, k, method):
    n = int(X.shape[0])
    if method in {
        "homogeneous",
        "homogeneous-lloyd",
        "tuned",
        "interleaved-tuned",
        "compiled-tuned",
        "fused-stats",
    }:
        if k <= 256:
            return min(n, 4096), k
        if k <= 1024:
            return min(n, 1024), k
        return min(n, 8192), min(k, 256)
    explicit = {
        "n256-kall": (256, k),
        "n1024-kall": (1024, k),
        "n4096-kall": (4096, k),
        "n8192-k256": (8192, min(k, 256)),
        "n16384-k256": (16_384, min(k, 256)),
        "n4096-k512": (4096, min(k, 512)),
    }
    if method in explicit:
        tile_n, tile_k = explicit[method]
        return min(n, tile_n), tile_k
    if method in {"legacy", "baseline", "hierarchical"}:
        return min(n, 4096), min(k, 256)
    tile_k = k if method in {"full-k", "interleaved", "combined", "compiled"} else min(k, 1024)
    itemsize = X.element_size() if hasattr(X, "element_size") else X.itemsize
    tile_n = max(1, min(n, SCORE_BUDGET // (itemsize * tile_k)))
    return tile_n, tile_k


def _hooks(X, method, tile_n, tile_k, fixed):
    from kmeans_lloyd.iteration import (
        _distances_to_candidates,
        assign_homogeneous_tiled,
        augment_for_gemm_scores,
        gemm_labels,
        gemm_scores_argmin,
        hierarchical_weighted_draw,
    )

    xp = array_namespace(X)
    step = None
    label_step = None
    assigner = None
    distance = None
    draw = (
        hierarchical_weighted_draw
        if method in {"hierarchical", "combined", "compiled"}
        else None
    )
    compile_seconds = 0.0
    if method == "legacy":
        def step(x_tile, c_tile, c_norm):
            return gemm_scores_argmin(xp, x_tile, c_tile, c_norm)
    if method in {"homogeneous", "homogeneous-lloyd"}:
        augmented = None

        def assigner(centers, selected_tile_n, selected_tile_k):
            nonlocal augmented
            if augmented is None:
                augmented = augment_for_gemm_scores(xp, X)
            assignment_data = augmented[:, : int(X.shape[1]) + 1]
            return assign_homogeneous_tiled(
                assignment_data,
                centers,
                selected_tile_n,
                selected_tile_k,
            )

        def homogeneous_distance(xp, data, x_norm, candidates):
            nonlocal augmented
            if augmented is None:
                ones = xp.ones(
                    (int(data.shape[0]), 1),
                    dtype=data.dtype,
                    device=device(data),
                )
                augmented = xp.concat(
                    (data, ones, x_norm[:, None]),
                    axis=1,
                )
            c_norm = xp.sum(candidates * candidates, axis=1)
            ones = xp.ones(
                (int(candidates.shape[0]), 1),
                dtype=candidates.dtype,
                device=device(candidates),
            )
            transformed = xp.concat(
                (-2 * candidates, c_norm[:, None], ones),
                axis=1,
            )
            return xp.matmul(
                augmented,
                xp.matrix_transpose(transformed),
            )

        if method == "homogeneous":
            distance = homogeneous_distance
    if method in {"compiled", "compiled-tuned"}:
        import torch

        step = torch.compile(
            lambda x_tile, c_tile, c_norm: gemm_scores_argmin(
                xp, x_tile, c_tile, c_norm
            ),
            dynamic=True,
        )
        label_step = torch.compile(
            lambda x_tile, c_tile, c_norm: gemm_labels(
                xp, x_tile, c_tile, c_norm
            ),
            dynamic=True,
        )
        distance_block = torch.compile(
            lambda data, x_norm, candidates: _distances_to_candidates(
                xp, data, x_norm, candidates
            ),
            dynamic=True,
        )

        def distance(unused_xp, data, x_norm, candidates):
            del unused_xp
            return distance_block(data, x_norm, candidates)

        started = time.perf_counter()
        c = fixed[: min(tile_k, int(fixed.shape[0])), :]
        step(X[: min(tile_n, 256), :], c, xp.sum(c * c, axis=1))
        label_step(
            X[: min(tile_n, 256), :],
            c,
            xp.sum(c * c, axis=1),
        )
        distance(
            xp,
            X[:256, :],
            xp.sum(X[:256, :] * X[:256, :], axis=1),
            c[: min(8, int(c.shape[0])), :],
        )
        compile_seconds = time.perf_counter() - started
    return (
        step,
        label_step,
        assigner,
        distance,
        draw,
        compile_seconds,
    )


def _fit(
    X,
    centers,
    rng,
    k,
    tile_n,
    tile_k,
    step,
    label_step,
    assigner,
    iteration,
    variance=None,
):
    from kmeans_lloyd.backends import native_accumulate
    from kmeans_lloyd.iteration import assign_gemm_tiled, fit_lloyd, inertia

    accumulate = native_accumulate(X, k)
    result = fit_lloyd(
        X,
        centers,
        max_iter=MAX_ITER,
        tol=TOL,
        tile_n=tile_n,
        tile_k=tile_k,
        update_tile_n=tile_n,
        update_tile_k=tile_k,
        reassign_empty=True,
        rng=rng,
        step=step,
        label_step=label_step,
        assigner=assigner,
        accumulate=accumulate,
        iteration=iteration,
        variance=variance,
    )
    if assigner is None:
        labels = assign_gemm_tiled(
            X,
            result["centers"],
            tile_n,
            tile_k,
            step=step,
            label_step=label_step,
        )
    else:
        labels = assigner(result["centers"], tile_n, tile_k)
    objective = float(inertia(X, labels, result["centers"], min(tile_n, 4096)))
    return result["centers"], result["n_iter"], objective


def _call(args, X, fixed):
    from kmeans_lloyd.iteration import (
        _row_norm_and_variance,
        kmeans_plusplus,
        lloyd_step_interleaved,
    )

    tile_n, tile_k = _tiles(X, args.k, args.method)
    (
        step,
        label_step,
        assigner,
        distance,
        draw,
        compile_seconds,
    ) = _hooks(
        X, args.method, tile_n, tile_k, fixed
    )
    iteration = (
        lloyd_step_interleaved
        if args.method in {"interleaved", "combined", "interleaved-tuned"}
        else None
    )
    rng = np.random.default_rng(args.seed)
    x_norm = None
    variance = None
    if args.method == "fused-stats" and args.phase == "fit":
        xp = array_namespace(X)
        x_norm, variance = _row_norm_and_variance(xp, X)
    if args.phase == "init":
        centers, _ = kmeans_plusplus(
            X,
            args.k,
            rng,
            distance=distance,
            draw=draw,
            x_norm=x_norm,
        )
        return centers, 0, None, tile_n, tile_k, compile_seconds
    if args.phase == "lloyd":
        centers, n_iter, objective = _fit(
            X,
            fixed,
            rng,
            args.k,
            tile_n,
            tile_k,
            step,
            label_step,
            assigner,
            iteration,
            variance,
        )
        return centers, n_iter, objective, tile_n, tile_k, compile_seconds
    centers, _ = kmeans_plusplus(
        X,
        args.k,
        rng,
        distance=distance,
        draw=draw,
        x_norm=x_norm,
    )
    centers, n_iter, objective = _fit(
        X,
        centers,
        rng,
        args.k,
        tile_n,
        tile_k,
        step,
        label_step,
        assigner,
        iteration,
        variance,
    )
    return centers, n_iter, objective, tile_n, tile_k, compile_seconds


def worker(argv):
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument("--worker", action="store_true")
    parser.add_argument("--method", choices=METHODS, required=True)
    parser.add_argument("--phase", choices=PHASES, required=True)
    parser.add_argument("--data", required=True)
    parser.add_argument("--centers", required=True)
    parser.add_argument("--k", type=int, required=True)
    parser.add_argument("--seed", type=int, required=True)
    args = parser.parse_args(argv)

    import torch

    torch.set_num_threads(4)
    samples = np.load(args.data)
    centers0 = np.load(args.centers)
    X = torch.as_tensor(samples)
    fixed = torch.as_tensor(centers0)
    before = _hwm_bytes()
    started = time.perf_counter()
    centers, n_iter, objective, tile_n, tile_k, compile_seconds = _call(
        args, X, fixed
    )
    seconds = time.perf_counter() - started
    memory = max(0, _hwm_bytes() - before)
    if objective is None:
        objective = _mean_inertia(samples, _to_numpy(centers)) * len(samples)
    print(
        json.dumps(
            {
                "backend": "torch-cpu",
                "method": args.method,
                "phase": args.phase,
                "seed": args.seed,
                "k": args.k,
                "seconds": seconds,
                "compile_seconds": compile_seconds,
                "mem_increment_bytes": memory,
                "mem_meter": "vmhwm",
                "inertia_per_point": objective / len(samples),
                "n_iter": n_iter,
                "tile_n": tile_n,
                "tile_k": tile_k,
            }
        ),
        flush=True,
    )


def _append(path, row):
    with path.open("a") as stream:
        stream.write(json.dumps(row) + "\n")


def drive(tasks, methods, phases, seeds, out, timeout):
    data_dir = HOME / "task-mix-data-v4"
    env = os.environ.copy()
    env.update(
        PYTHONPATH=str(ROOT / "src"),
        OMP_NUM_THREADS="4",
        MKL_NUM_THREADS="4",
        OPENBLAS_NUM_THREADS="4",
    )
    remote_python = HOME / "kmeans_lloyd/.pixi/envs/default/bin/python"
    python = remote_python if remote_python.exists() else Path(sys.executable)
    for task in TASKS:
        if tasks and task["name"] not in tasks:
            continue
        data_path = data_dir / f"{task['name']}.npy"
        generate(task, data_path)
        for seed in seeds:
            _, centers_path = save_random_start(data_path, task, seed)
            for phase in phases:
                ordered_methods = list(methods)
                if seed % 2:
                    ordered_methods.reverse()
                for method in ordered_methods:
                    command = [
                        str(python),
                        str(Path(__file__).resolve()),
                        "--worker",
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
                        f"start {task['name']} seed={seed} {phase} {method}",
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
                            timeout=timeout,
                            check=False,
                        )
                    except subprocess.TimeoutExpired as error:
                        row = {
                            "task": task,
                            "seed": seed,
                            "method": method,
                            "phase": phase,
                            "error": "timeout",
                            "timeout_seconds": timeout,
                            "stderr": (error.stderr or "")[-1000:],
                        }
                        _append(out, row)
                        print("  timeout", flush=True)
                        continue
                    lines = completed.stdout.strip().splitlines()
                    if completed.returncode or not lines:
                        row = {
                            "task": task,
                            "seed": seed,
                            "method": method,
                            "phase": phase,
                            "error": f"exit {completed.returncode}",
                            "stderr": completed.stderr[-2000:],
                        }
                        print(row["error"], row["stderr"][-300:], flush=True)
                    else:
                        row = json.loads(lines[-1])
                        row["task"] = task
                        row["wall_seconds"] = time.perf_counter() - started
                        print(
                            f"  {row['seconds']:.3f}s "
                            f"inertia={row['inertia_per_point']:.6g}",
                            flush=True,
                        )
                    _append(out, row)


def main():
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument("--worker", action="store_true")
    parser.add_argument("--tasks", default="")
    parser.add_argument("--methods", default=",".join(METHODS))
    parser.add_argument("--phases", default=",".join(PHASES))
    parser.add_argument("--seeds", default="0,1,2")
    parser.add_argument("--timeout", type=int, default=180)
    parser.add_argument("--out", default=str(HOME / "cpu-optimization-results.jsonl"))
    args, _ = parser.parse_known_args()
    if args.worker:
        worker(sys.argv[1:])
        return
    drive(
        {value for value in args.tasks.split(",") if value},
        [value for value in args.methods.split(",") if value],
        [value for value in args.phases.split(",") if value],
        [int(value) for value in args.seeds.split(",") if value],
        Path(args.out),
        args.timeout,
    )


if __name__ == "__main__":
    main()
