"""Ablate the reduction step of scalable k-means++ on shared candidates.

All variants reuse one array-API k-means|| candidate pool per seed and differ
only in how it is reduced to ``k`` centers:

* ``weighted-greedy``: the array-API implementation (rows of ``X``);
* ``unweighted-greedy``: cuVS's step 8a, greedy k-means++ ignoring weights;
* ``unweighted-greedy+weighted-lloyd``: cuVS's complete reduction, followed by
  weighted Lloyd on the candidates with cuVS's default ``max_iter=300`` and
  ``tol=1e-4`` convergence rule;
* ``weighted-greedy+weighted-lloyd``: the array-API reduction followed by the
  same weighted Lloyd recluster.

Run on CUDA with PyTorch. Quality is full-data mean inertia without Lloyd.
"""

from __future__ import annotations

import argparse
import copy
import json
import math
import time
from pathlib import Path

import numpy as np
import torch

from kmeans_lloyd.iteration import (
    _scalable_candidates,
    _weighted_kmeans_plusplus,
    assign_gemm_tiled,
    kmeans_plusplus,
)

HOME = Path.home()
TASKS = {"k3-d1000": 3, "k17-d180": 17, "k100-d32": 100, "k550-d6": 550, "k3000-d2": 3000}


def mean_inertia(X, centers, tile_n=8192):
    total = 0.0
    c_norm = (centers * centers).sum(1)
    for start in range(0, X.shape[0], tile_n):
        tile = X[start : start + tile_n]
        d = (tile * tile).sum(1, keepdim=True) + c_norm - 2 * tile @ centers.T
        total += float(d.min(1).values.clamp_min(0).sum())
    return total / X.shape[0]


def weighted_lloyd(C, w, centers, max_iter=300, tol=1e-4):
    """Weighted Lloyd with cuVS's convergence rule on the cost and the shift."""
    k = centers.shape[0]
    prior = None
    for iteration in range(1, max_iter + 1):
        labels = assign_gemm_tiled(
            C, centers, tile_n=min(8192, C.shape[0]), tile_k=min(256, k)
        )
        sums = torch.zeros_like(centers).index_add_(0, labels, C * w[:, None])
        counts = torch.zeros(k, dtype=C.dtype, device=C.device).index_add_(0, labels, w)
        new = torch.where(
            counts[:, None] > 0, sums / counts.clamp_min(1e-30)[:, None], centers
        )
        cost = float((w * ((C - centers[labels]) ** 2).sum(1)).sum())
        shift = float(((new - centers) ** 2).sum())
        centers = new
        done = shift < tol
        if prior is not None and cost != 0 and iteration > 1 and cost / prior > 1 - tol:
            done = True
        prior = cost
        if done:
            break
    return centers, iteration


def run(task, seed, oversampling_factor, n_rounds):
    k = TASKS[task]
    X = torch.as_tensor(np.load(HOME / "task-mix-data-v4" / f"{task}.npy"), device="cuda")
    torch.backends.cuda.matmul.allow_tf32 = False
    rng = np.random.default_rng(seed)
    xp = __import__("array_api_compat").array_namespace(X)
    started = time.perf_counter()
    indices, C, w = _scalable_candidates(xp, X, k, rng, oversampling_factor, n_rounds, 8192, 256)
    torch.cuda.synchronize()
    candidate_seconds = time.perf_counter() - started
    rows = []
    n_trials = 2 + int(math.ceil(math.log(k))) if k > 1 else 1

    def record(name, centers, extra):
        rows.append(
            {
                "task": task,
                "seed": seed,
                "variant": name,
                "n_candidates": int(C.shape[0]),
                "candidate_seconds": candidate_seconds,
                "inertia_per_point": mean_inertia(X, centers),
                **extra,
            }
        )

    state = copy.deepcopy(rng)
    picked = _weighted_kmeans_plusplus(xp, C, w, copy.deepcopy(state), k)
    weighted = C[picked]
    record("weighted-greedy", weighted, {})
    unweighted, _ = kmeans_plusplus(C, k, copy.deepcopy(state), n_local_trials=n_trials)
    record("unweighted-greedy", unweighted, {})
    for name, start in (
        ("unweighted-greedy+weighted-lloyd", unweighted),
        ("weighted-greedy+weighted-lloyd", weighted),
    ):
        torch.cuda.synchronize()
        started = time.perf_counter()
        refined, n_iter = weighted_lloyd(C, w, start.clone())
        torch.cuda.synchronize()
        record(name, refined, {"recluster_iter": n_iter, "recluster_seconds": time.perf_counter() - started})
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--tasks", default=",".join(TASKS))
    parser.add_argument("--seeds", default="0,1,2")
    parser.add_argument("--oversampling-factor", type=float, default=2.0)
    parser.add_argument("--init-rounds", type=int, default=8)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    out = Path(args.out)
    for task in args.tasks.split(","):
        for seed in (int(value) for value in args.seeds.split(",")):
            for row in run(task, seed, args.oversampling_factor, args.init_rounds):
                with out.open("a") as stream:
                    stream.write(json.dumps(row) + "\n")
                print(
                    f"{task} seed={seed} {row['variant']}: {row['inertia_per_point']:.6g} "
                    f"m={row['n_candidates']} iter={row.get('recluster_iter', '-')}",
                    flush=True,
                )
            torch.cuda.empty_cache()


if __name__ == "__main__":
    main()
