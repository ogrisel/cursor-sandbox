"""Compare portable and CuPy-specific centroid reductions on CUDA."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import cupy as cp
import cupyx
import numpy as np

from kmeans_lloyd.iteration import update_centroids_tiled

TASKS = {
    "k100-d32": 100,
    "k550-d6": 550,
    "k3000-d2": 3000,
}

ACCUMULATE = cp.RawKernel(
    r"""
    extern "C" __global__
    void accumulate(
        const float* X, const long long* labels, float* sums, int* counts,
        const int n_samples, const int n_features
    ) {
        const int i = blockDim.x * blockIdx.x + threadIdx.x;
        const int size = n_samples * n_features;
        if (i >= size) return;
        const int sample = i / n_features;
        const int feature = i - sample * n_features;
        const long long label = labels[sample];
        atomicAdd(&sums[label * n_features + feature], X[i]);
        if (feature == 0) atomicAdd(&counts[label], 1);
    }
    """,
    "accumulate",
)


def scatter_update(X, labels, old):
    sums = cp.zeros_like(old)
    cupyx.scatter_add(sums, (labels, slice(None)), X)
    counts = cp.bincount(labels, minlength=old.shape[0]).astype(X.dtype)
    return cp.where(counts[:, None] == 0, old, sums / cp.maximum(counts[:, None], 1))


def add_at_update(X, labels, old):
    sums = cp.zeros_like(old)
    cp.add.at(sums, labels, X)
    counts = cp.bincount(labels, minlength=old.shape[0]).astype(X.dtype)
    return cp.where(counts[:, None] == 0, old, sums / cp.maximum(counts[:, None], 1))


def raw_update(X, labels, old):
    sums = cp.zeros_like(old)
    counts = cp.zeros(old.shape[0], dtype=cp.int32)
    size = X.size
    ACCUMULATE(
        ((size + 255) // 256,),
        (256,),
        (X, labels, sums, counts, X.shape[0], X.shape[1]),
    )
    counts_float = counts.astype(X.dtype)
    return cp.where(
        counts[:, None] == 0,
        old,
        sums / cp.maximum(counts_float[:, None], 1),
    )


def timed(fn, repeats):
    fn()
    cp.cuda.Stream.null.synchronize()
    samples = []
    result = None
    for _ in range(repeats):
        start = cp.cuda.Event()
        stop = cp.cuda.Event()
        start.record()
        result = fn()
        stop.record()
        stop.synchronize()
        samples.append(cp.cuda.get_elapsed_time(start, stop) / 1000)
    return result, samples


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--task", choices=TASKS, required=True)
    parser.add_argument("--data-dir", type=Path, default=Path.home() / "task-mix-data-v4")
    parser.add_argument("--repeats", type=int, default=5)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    k = TASKS[args.task]
    host = np.load(args.data_dir / f"{args.task}.npy", mmap_mode="r")
    X = cp.asarray(host)
    labels = cp.asarray(
        np.random.default_rng(0).integers(k, size=X.shape[0], dtype=np.int64)
    )
    old = cp.zeros((k, X.shape[1]), dtype=X.dtype)
    variants = {
        "portable-current": lambda: update_centroids_tiled(
            X, labels, old, tile_k=min(k, 256), tile_n=4096
        ),
        "portable-tuned": lambda: update_centroids_tiled(
            X, labels, old, tile_k=min(k, 512), tile_n=16_384
        ),
        "cupyx-scatter-add": lambda: scatter_update(X, labels, old),
        "cupy-add-at": lambda: add_at_update(X, labels, old),
        "raw-fused-atomic": lambda: raw_update(X, labels, old),
    }
    reference, _ = timed(variants["cupyx-scatter-add"], 1)
    rows = []
    for name, fn in variants.items():
        result, samples = timed(fn, args.repeats)
        row = {
            "task": args.task,
            "variant": name,
            "seconds": float(np.median(samples)),
            "seconds_all": samples,
            "max_abs_error": float(cp.max(cp.abs(result - reference))),
            "cupy": cp.__version__,
        }
        rows.append(row)
        print(json.dumps(row), flush=True)
    args.out.write_text(json.dumps(rows, indent=2) + "\n")


if __name__ == "__main__":
    main()
