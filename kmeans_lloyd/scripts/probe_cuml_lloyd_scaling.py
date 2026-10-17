"""Measure cuML Lloyd scaling with input already resident on the GPU."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import cupy
import numpy as np
from cuml.cluster import KMeans


TASKS = {"k100-d32": 100, "k550-d6": 550, "k3000-d2": 3000}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--tasks", default=",".join(TASKS))
    parser.add_argument("--iterations", default="1,4,12")
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--data-dir", default=str(Path.home() / "task-mix-data-v4"))
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    data_dir = Path(args.data_dir)
    rows = []
    for task in args.tasks.split(","):
        k = TASKS[task]
        host = np.load(data_dir / f"{task}.npy")
        data = cupy.asarray(host)
        centers = np.load(data_dir / f"{task}-seed-0-centers.npy")
        KMeans(
            n_clusters=2, init="random", n_init=1, max_iter=1, output_type="numpy"
        ).fit(data[:128])
        for max_iter in map(int, args.iterations.split(",")):
            samples = []
            n_iter = None
            inertia = None
            for _ in range(args.repeats):
                cupy.cuda.Stream.null.synchronize()
                started = time.perf_counter()
                model = KMeans(
                    n_clusters=k,
                    init=centers,
                    n_init=1,
                    max_iter=max_iter,
                    tol=1e-8,
                    random_state=0,
                    output_type="numpy",
                ).fit(data)
                cupy.cuda.Stream.null.synchronize()
                samples.append(time.perf_counter() - started)
                n_iter = int(model.n_iter_)
                inertia = float(model.inertia_) / len(data)
            row = {
                "task": task,
                "k": k,
                "max_iter": max_iter,
                "n_iter": n_iter,
                "seconds": float(np.median(samples)),
                "seconds_all": samples,
                "inertia_per_point": inertia,
            }
            rows.append(row)
            print(json.dumps(row), flush=True)
    Path(args.out).write_text(json.dumps(rows, indent=2) + "\n")


if __name__ == "__main__":
    main()
