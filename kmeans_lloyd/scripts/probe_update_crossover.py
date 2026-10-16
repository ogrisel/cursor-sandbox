"""Time native scatter-add and portable one-hot centroid updates across k.

Atomic scatter-adds serialize when many samples share few clusters, while the
one-hot GEMM costs grow with ``k``. This probe locates the crossover on each
task's data with uniformly random labels.
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import numpy as np

from kmeans_lloyd.backends import _cupy_accumulate, _torch_accumulate
from kmeans_lloyd.iteration import update_centroids_tiled
from kmeans_lloyd.kmeans import _tile_schedule

DATASETS = ("k3-d1000", "k17-d180", "k100-d32", "k550-d6")
CLUSTERS = (2, 3, 5, 8, 12, 17, 24, 32, 48, 64, 100)


def _backend(name):
    if name == "cupy":
        import cupy

        return cupy.asarray, cupy.cuda.Stream.null.synchronize, _cupy_accumulate
    import torch

    torch.backends.cuda.matmul.allow_tf32 = False

    def to_device(array):
        return torch.as_tensor(np.ascontiguousarray(array), device="cuda")

    return to_device, torch.cuda.synchronize, _torch_accumulate


def _timed(fn, sync, repeats, *args, **kwargs):
    fn(*args, **kwargs)
    sync()
    samples = []
    for _ in range(repeats):
        started = time.perf_counter()
        fn(*args, **kwargs)
        sync()
        samples.append(time.perf_counter() - started)
    return float(np.median(samples))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--backend", choices=("torch-cuda", "cupy"), required=True)
    parser.add_argument("--data-dir", type=Path, default=Path.home() / "task-mix-data-v4")
    parser.add_argument("--repeats", type=int, default=5)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    to_device, sync, accumulate = _backend(args.backend)
    rows = []
    for dataset in DATASETS:
        X = to_device(np.load(args.data_dir / f"{dataset}.npy", mmap_mode="r"))
        for k in CLUSTERS:
            labels = to_device(
                np.random.default_rng(0).integers(k, size=X.shape[0], dtype=np.int64)
            )
            old = X[:k, :] * 0
            tiles = _tile_schedule(X, k)
            native = _timed(accumulate, sync, args.repeats, X, labels, k)
            portable = _timed(
                update_centroids_tiled,
                sync,
                args.repeats,
                X,
                labels,
                old,
                tile_k=tiles["update_tile_k"],
                tile_n=tiles["update_tile_n"],
            )
            row = {
                "backend": args.backend,
                "dataset": dataset,
                "n_samples": int(X.shape[0]),
                "n_features": int(X.shape[1]),
                "k": k,
                "native_seconds": native,
                "portable_seconds": portable,
                "native_speedup": portable / native,
            }
            rows.append(row)
            print(json.dumps(row), flush=True)
    args.out.write_text(json.dumps(rows, indent=2) + "\n")


if __name__ == "__main__":
    main()
