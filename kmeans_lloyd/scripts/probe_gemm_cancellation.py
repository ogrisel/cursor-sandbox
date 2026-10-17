"""Probe cancellation and stable-distance thresholds far from the origin."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from array_api_compat import array_namespace

from kmeans_lloyd.iteration import (
    kmeans_plusplus,
    stable_distances_to_candidates,
    stable_gemm_distances,
)

OFFSETS = (0.0, 1.0, 10.0, 100.0, 1e3, 1e4, 1e5)
FEATURES = (2, 32, 1000)
THRESHOLDS = (1e-8, 1e-6, 1e-4, 1e-3, 1e-2)


def _array(backend, host):
    if backend.startswith("torch"):
        import torch

        device = "cuda" if backend == "torch-cuda" else "cpu"
        return torch.as_tensor(host, device=device)
    import cupy

    return cupy.asarray(host)


def _host(array):
    if hasattr(array, "get"):
        return array.get()
    if hasattr(array, "detach"):
        return array.detach().cpu().numpy()
    return np.asarray(array)


def _synchronize(backend):
    if backend == "torch-cuda":
        import torch

        torch.cuda.synchronize()
    elif backend == "cupy":
        import cupy

        cupy.cuda.Stream.null.synchronize()


def _stable_distance(stats):
    def distance(xp, data, x_norm, candidates):
        return stable_distances_to_candidates(
            xp, data, x_norm, candidates, stats=stats
        )

    return distance


def distance_rows(backend, dtype):
    rows = []
    for n_features in FEATURES:
        base = np.random.default_rng(0).uniform(size=(32, n_features))
        for offset in OFFSETS:
            unique = (base + offset).astype(dtype)
            X = _array(backend, np.repeat(unique, 4, axis=0))
            centers = _array(backend, unique)
            xp = array_namespace(X, centers)
            x_norm = xp.sum(X * X, axis=1)
            c_norm = xp.sum(centers * centers, axis=1)
            norms = x_norm[:, None] + c_norm[None, :]
            raw = norms - 2 * xp.matmul(X, xp.matrix_transpose(centers))
            gemm = xp.maximum(raw, xp.zeros_like(raw))
            direct = xp.sum(
                (X[:, None, :] - centers[None, :, :]) ** 2, axis=2
            )
            direct_host = _host(direct)
            gemm_host = _host(gemm)
            direct_labels = np.argmin(direct_host, axis=1)
            positive = direct_host > 0
            common = {
                "kind": "distances",
                "backend": backend,
                "dtype": np.dtype(dtype).name,
                "n_features": n_features,
                "offset": offset,
                "n_unique_input_rows": int(np.unique(unique, axis=0).shape[0]),
                "gemm_label_errors": int(
                    np.count_nonzero(np.argmin(gemm_host, axis=1) != direct_labels)
                ),
                "gemm_false_zeros": int(
                    np.count_nonzero((gemm_host == 0) & positive)
                ),
                "gemm_negative_raw": int(np.count_nonzero(_host(raw) < 0)),
                "gemm_max_abs_error": float(
                    np.max(np.abs(gemm_host - direct_host))
                ),
            }
            for threshold in THRESHOLDS:
                stats = {}
                stable = stable_gemm_distances(
                    xp,
                    X,
                    x_norm,
                    centers,
                    c_norm,
                    threshold=threshold,
                    stats=stats,
                )
                stable_host = _host(stable)
                row = {
                    **common,
                    "threshold": threshold,
                    "recomputed_fraction": (
                        stats["recomputed_pairs"] / stats["distance_pairs"]
                    ),
                    "stable_label_errors": int(
                        np.count_nonzero(
                            np.argmin(stable_host, axis=1) != direct_labels
                        )
                    ),
                    "stable_false_zeros": int(
                        np.count_nonzero((stable_host == 0) & positive)
                    ),
                    "stable_max_abs_error": float(
                        np.max(np.abs(stable_host - direct_host))
                    ),
                }
                rows.append(row)
                print(json.dumps(row), flush=True)
            del X, centers
    return rows


def plusplus_rows(backend, dtype):
    rows = []
    for offset in OFFSETS:
        rng = np.random.default_rng(0)
        unique = (rng.uniform(size=(10, 2)) + offset).astype(dtype)
        X = _array(backend, np.repeat(unique, 50, axis=0))
        for method in ("gemm", "stable"):
            stats = {}
            distance = _stable_distance(stats) if method == "stable" else None

            centers, _ = kmeans_plusplus(
                X, 10, np.random.default_rng(0), distance=distance
            )
            _synchronize(backend)
            row = {
                "kind": "plusplus",
                "backend": backend,
                "dtype": np.dtype(dtype).name,
                "n_features": 2,
                "offset": offset,
                "method": method,
                "n_unique_input_rows": int(np.unique(unique, axis=0).shape[0]),
                "n_unique_centers": int(
                    np.unique(_host(centers), axis=0).shape[0]
                ),
                "recomputed_fraction": (
                    stats.get("recomputed_pairs", 0)
                    / max(1, stats.get("distance_pairs", 0))
                ),
            }
            rows.append(row)
            print(json.dumps(row), flush=True)
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--backend", choices=("torch-cpu", "torch-cuda", "cupy"), required=True
    )
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    rows = []
    for dtype in (np.float32, np.float64):
        rows += distance_rows(args.backend, dtype)
        rows += plusplus_rows(args.backend, dtype)
    args.out.write_text(json.dumps(rows, indent=2) + "\n")


if __name__ == "__main__":
    main()
