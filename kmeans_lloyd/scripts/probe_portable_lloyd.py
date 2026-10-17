"""Compare the current and tuned portable Lloyd schedules on CUDA backends."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import array_api_compat
import numpy as np

from kmeans_lloyd.instrument import measure_call
from kmeans_lloyd.iteration import fit_lloyd


TASKS = {"k100-d32": 100, "k550-d6": 550, "k3000-d2": 3000}


def gather_scores(x_tile, c_tile, c_norm):
    """Argmin plus gather, using only Python array API operations."""
    xp = array_api_compat.array_namespace(x_tile, c_tile)
    scores = c_norm[None, :] - 2 * xp.matmul(x_tile, xp.matrix_transpose(c_tile))
    labels = xp.argmin(scores, axis=1)
    values = xp.take_along_axis(scores, labels[:, None], axis=1)[:, 0]
    return labels, values


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--task", choices=TASKS, required=True)
    parser.add_argument("--backend", choices=("torch", "cupy"), required=True)
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--data-dir", default=str(Path.home() / "task-mix-data-v4"))
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    k = TASKS[args.task]
    host = np.load(Path(args.data_dir) / f"{args.task}.npy")
    initial = np.load(Path(args.data_dir) / f"{args.task}-seed-0-centers.npy")
    if args.backend == "torch":
        import torch

        torch.backends.cuda.matmul.allow_tf32 = False
        X = torch.as_tensor(host, device="cuda")
        centers = torch.as_tensor(initial, device="cuda")
        synchronize = torch.cuda.synchronize
    else:
        import cupy

        X = cupy.asarray(host)
        centers = cupy.asarray(initial)
        synchronize = cupy.cuda.Stream.null.synchronize
    synchronize()

    configs = (
        (
            "current",
            dict(
                tile_n=65_536,
                tile_k=min(256, k),
                update_tile_k=min(256, k),
                update_tile_n=4_096,
            ),
        ),
        (
            "portable-tuned",
            dict(
                tile_n=65_536,
                tile_k=min(128, k),
                update_tile_k=min(512, k),
                update_tile_n=16_384,
                step=gather_scores,
            ),
        ),
    )
    rows = []
    for name, kwargs in configs:
        fn = lambda: fit_lloyd(
            X,
            centers,
            max_iter=12,
            tol=1e-8,
            reassign_empty=False,
            **kwargs,
        )
        fn()  # warm allocator and kernels
        for repeat in range(args.repeats):
            result, profile = measure_call(fn, (), X)
            row = {
                "task": args.task,
                "backend": args.backend,
                "variant": name,
                "repeat": repeat,
                "seconds": profile["seconds"],
                "peak_extra_bytes": profile["peak_extra_bytes"],
                "inertia": result["inertia"],
                "n_iter": result["n_iter"],
            }
            rows.append(row)
            print(json.dumps(row), flush=True)
    Path(args.out).write_text(json.dumps(rows, indent=2) + "\n")


if __name__ == "__main__":
    main()
