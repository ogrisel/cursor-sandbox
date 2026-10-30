"""Profile Lloyd assignment and update alternatives on the large-k tasks.

This is an experiment driver, not a benchmark contender. It times one phase at
a time after warmup and validates labels or centers against the current tiled
array-API implementation.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import torch

from kmeans_lloyd.iteration import assign_gemm_tiled, update_centroids_tiled


TASKS = {
    "k100-d32": (100, 65_536, 256, 4_096),
    "k550-d6": (550, 65_536, 256, 4_096),
    "k3000-d2": (3000, 65_536, 256, 4_096),
}


def timed(name, fn, repeats, rows, task, phase, validate):
    fn()
    torch.cuda.synchronize()
    samples = []
    peaks = []
    result = None
    for _ in range(repeats):
        torch.cuda.reset_peak_memory_stats()
        before = torch.cuda.memory_allocated()
        start = torch.cuda.Event(enable_timing=True)
        stop = torch.cuda.Event(enable_timing=True)
        start.record()
        result = fn()
        stop.record()
        stop.synchronize()
        samples.append(start.elapsed_time(stop) / 1000)
        peaks.append(torch.cuda.max_memory_allocated() - before)
    row = {
        "task": task,
        "phase": phase,
        "variant": name,
        "seconds": float(np.median(samples)),
        "seconds_all": samples,
        "peak_extra_bytes": int(max(peaks)),
        **validate(result),
    }
    rows.append(row)
    print(json.dumps(row), flush=True)
    return result


def gather_scores(x_tile, c_tile, c_norm):
    """Portable argmin plus gather instead of a second minimum reduction."""
    scores = c_norm[None, :] - 2 * torch.matmul(x_tile, c_tile.T)
    labels = torch.argmin(scores, dim=1)
    values = torch.take_along_dim(scores, labels[:, None], dim=1)[:, 0]
    return labels, values


def current_scores(x_tile, c_tile, c_norm):
    """The current two-reduction tile, spelled directly for torch.compile."""
    scores = c_norm[None, :] - 2 * torch.matmul(x_tile, c_tile.T)
    return torch.argmin(scores, dim=1), torch.min(scores, dim=1).values


def combined_scores(x_tile, c_tile, c_norm):
    """Torch control: one reduction returns both values and indices."""
    scores = c_norm[None, :] - 2 * torch.matmul(x_tile, c_tile.T)
    values, labels = torch.min(scores, dim=1)
    return labels, values


def direct_scores(x_tile, c_tile, c_norm):
    """Torch control: fuse low-dimensional scores and reduction without GEMM."""
    scores = c_norm[None, :] - 2 * torch.sum(
        x_tile[:, None, :] * c_tile[None, :, :], dim=2
    )
    values, labels = torch.min(scores, dim=1)
    return labels, values


def update_index_add(X, labels, old):
    """Torch control for a native scatter-based centroid update."""
    sums = torch.zeros_like(old)
    sums.index_add_(0, labels, X)
    counts = torch.bincount(labels, minlength=old.shape[0]).to(X.dtype)
    return torch.where(
        counts[:, None] == 0,
        old,
        sums / torch.clamp(counts[:, None], min=1),
    )


def update_sorted(X, labels, old):
    """Segmented mean using operations available through the array API."""
    order = torch.argsort(labels)
    sorted_labels = labels[order]
    sorted_X = X[order]
    observed, counts = torch.unique_consecutive(sorted_labels, return_counts=True)
    cumulative = torch.cumsum(sorted_X, dim=0)
    ends = torch.cumsum(counts, dim=0) - 1
    observed_sums = cumulative[ends]
    observed_sums[1:] = observed_sums[1:] - cumulative[ends[:-1]]
    ids = torch.arange(old.shape[0], device=X.device, dtype=labels.dtype)
    positions = torch.searchsorted(observed, ids)
    safe = torch.clamp(positions, max=observed.shape[0] - 1)
    present = observed[safe] == ids
    sums = observed_sums[safe]
    full_counts = counts[safe].to(X.dtype)
    means = sums / full_counts[:, None]
    return torch.where(present[:, None], means, old)


def fit_steps(X, initial, assign, update, max_iter=12):
    """Run a fixed number of Lloyd steps with interchangeable phases."""
    centers = initial.clone()
    labels = None
    for _ in range(max_iter):
        labels = assign(X, centers)
        centers = update(X, labels, centers)
        # Match the production loop's convergence synchronization without
        # stopping early: these experiments use the same fixed 12 iterations.
        float(torch.sum((centers - initial) ** 2))
        initial = centers
    assigned = centers[labels]
    inertia = torch.sum((X - assigned) ** 2)
    return centers, labels, inertia


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--task", choices=TASKS, required=True)
    parser.add_argument("--data-dir", default=str(Path.home() / "task-mix-data-v4"))
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False
    torch.manual_seed(0)
    k, base_n, base_k, update_n = TASKS[args.task]
    samples = np.load(Path(args.data_dir) / f"{args.task}.npy", mmap_mode="r")
    X = torch.as_tensor(np.asarray(samples), device="cuda")
    indices = np.random.default_rng(0).choice(len(samples), k, replace=False)
    centers = X[torch.as_tensor(indices, device="cuda")].contiguous()
    torch.cuda.synchronize()

    rows = []
    baseline_labels = timed(
        f"current-n{base_n}-k{base_k}",
        lambda: assign_gemm_tiled(X, centers, base_n, base_k),
        args.repeats,
        rows,
        args.task,
        "assign",
        lambda result: {"label_mismatches": 0},
    )

    def labels_valid(result):
        return {
            "label_mismatches": int(torch.count_nonzero(result != baseline_labels)),
        }

    for tile_n, tile_k in (
        (65_536, 128),
        (65_536, 512),
        (32_768, 1024),
        (16_384, k),
        (8_192, k),
    ):
        if tile_k > k:
            continue
        timed(
            f"current-n{tile_n}-k{tile_k}",
            lambda n=tile_n, q=tile_k: assign_gemm_tiled(X, centers, n, q),
            args.repeats,
            rows,
            args.task,
            "assign",
            labels_valid,
        )
    timed(
        "portable-gather-n65536-k256",
        lambda: assign_gemm_tiled(X, centers, 65_536, 256, step=gather_scores),
        args.repeats,
        rows,
        args.task,
        "assign",
        labels_valid,
    )
    timed(
        "torch-combined-n65536-k256",
        lambda: assign_gemm_tiled(X, centers, 65_536, 256, step=combined_scores),
        args.repeats,
        rows,
        args.task,
        "assign",
        labels_valid,
    )

    compiled_combined = torch.compile(combined_scores)
    compiled_gather = torch.compile(gather_scores)
    compiled_current = torch.compile(current_scores)
    compiled_direct = torch.compile(direct_scores)
    timed(
        "compile-current-n65536-k256",
        lambda: assign_gemm_tiled(X, centers, 65_536, 256, step=compiled_current),
        args.repeats,
        rows,
        args.task,
        "assign",
        labels_valid,
    )
    timed(
        "compile-gather-n65536-k256",
        lambda: assign_gemm_tiled(X, centers, 65_536, 256, step=compiled_gather),
        args.repeats,
        rows,
        args.task,
        "assign",
        labels_valid,
    )
    timed(
        "compile-combined-n65536-k256",
        lambda: assign_gemm_tiled(X, centers, 65_536, 256, step=compiled_combined),
        args.repeats,
        rows,
        args.task,
        "assign",
        labels_valid,
    )
    timed(
        "compile-direct-n8192-k256",
        lambda: assign_gemm_tiled(X, centers, 8_192, 256, step=compiled_direct),
        args.repeats,
        rows,
        args.task,
        "assign",
        labels_valid,
    )

    baseline_centers = timed(
        f"current-k{base_k}-n{update_n}",
        lambda: update_centroids_tiled(
            X, baseline_labels, centers, base_k, tile_n=update_n
        ),
        args.repeats,
        rows,
        args.task,
        "update",
        lambda result: {"max_center_error": 0.0},
    )

    def centers_valid(result):
        return {
            "max_center_error": float(torch.max(torch.abs(result - baseline_centers))),
        }

    for tile_n, tile_k in (
        (4_096, 128),
        (4_096, 512),
        (8_192, 256),
        (16_384, 256),
        (16_384, 512),
        (65_536, 256),
    ):
        tile_k = min(tile_k, k)
        timed(
            f"onehot-k{tile_k}-n{tile_n}",
            lambda n=tile_n, q=tile_k: update_centroids_tiled(
                X, baseline_labels, centers, q, tile_n=n
            ),
            args.repeats,
            rows,
            args.task,
            "update",
            centers_valid,
        )
    timed(
        "portable-sorted-segments",
        lambda: update_sorted(X, baseline_labels, centers),
        args.repeats,
        rows,
        args.task,
        "update",
        centers_valid,
    )
    timed(
        "torch-index-add",
        lambda: update_index_add(X, baseline_labels, centers),
        args.repeats,
        rows,
        args.task,
        "update",
        centers_valid,
    )

    assign_current = lambda data, old: assign_gemm_tiled(
        data, old, 65_536, min(256, k)
    )
    update_current = lambda data, labels, old: update_centroids_tiled(
        data, labels, old, min(256, k), tile_n=4_096
    )
    assign_portable = lambda data, old: assign_gemm_tiled(
        data, old, 65_536, min(128, k), step=gather_scores
    )
    update_tuned = lambda data, labels, old: update_centroids_tiled(
        data, labels, old, min(512, k), tile_n=16_384
    )
    assign_compiled = lambda data, old: assign_gemm_tiled(
        data, old, 65_536, min(256, k), step=compiled_gather
    )

    baseline_fit = timed(
        "current",
        lambda: fit_steps(X, centers, assign_current, update_current),
        args.repeats,
        rows,
        args.task,
        "fit-12",
        lambda result: {"inertia": float(result[2])},
    )
    baseline_inertia = float(baseline_fit[2])

    def fit_valid(result):
        return {
            "inertia": float(result[2]),
            "relative_inertia": float(result[2]) / baseline_inertia,
        }

    for name, assign, update in (
        ("portable-gather+tuned-onehot", assign_portable, update_tuned),
        ("compile-gather+tuned-onehot", assign_compiled, update_tuned),
        ("compile-gather+sorted-segments", assign_compiled, update_sorted),
        ("compile-gather+torch-index-add", assign_compiled, update_index_add),
    ):
        timed(
            name,
            lambda a=assign, u=update: fit_steps(X, centers, a, u),
            args.repeats,
            rows,
            args.task,
            "fit-12",
            fit_valid,
        )
    Path(args.out).write_text(json.dumps(rows, indent=2) + "\n")


if __name__ == "__main__":
    main()
