"""Remeasure k-means++ and a full fit after the tiled reductions.

The sample norm and the inertia no longer allocate a tensor the size of
``X``. The centroid update accumulates sample tiles of ``tile_n``.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
os.environ.setdefault("NVIDIA_TF32_OVERRIDE", "0")

TIMING = {"name": "timing", "n_samples": 131_072, "n_features": 2_048, "n_clusters": 256, "seed": 0}
BLOBS = {
    "name": "blobs",
    "n_samples": 32_768,
    "n_features": 32,
    "n_clusters": 8,
    "seed": 1,
    "separation": 12.0,
    "noise": 0.4,
}


def _configure():
    import torch

    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False
    try:
        torch.set_float32_matmul_precision("highest")
    except Exception:
        pass
    return torch


def _normal(case):
    rng = np.random.default_rng(case["seed"])
    return rng.standard_normal((case["n_samples"], case["n_features"])).astype(np.float32)


def _blobs(case):
    rng = np.random.default_rng(case["seed"])
    centers = rng.standard_normal((case["n_clusters"], case["n_features"])).astype(np.float32)
    centers *= np.float32(case["separation"])
    labels = rng.integers(0, case["n_clusters"], size=case["n_samples"])
    noise = rng.standard_normal((case["n_samples"], case["n_features"])).astype(np.float32)
    return centers[labels] + np.float32(case["noise"]) * noise


def _bench(fn, example, warmup, repeats):
    from kmeans_lloyd.instrument import measure_call

    rows = []
    result = None
    for index in range(warmup + repeats):
        result, profile = measure_call(fn, (), example)
        profile["warmup"] = index < warmup
        rows.append(profile)
    steady = [row for row in rows if not row["warmup"]]
    ordered = sorted(row["seconds"] for row in steady)
    mid = len(ordered) // 2
    median = ordered[mid] if len(ordered) % 2 else 0.5 * (ordered[mid - 1] + ordered[mid])
    peaks = sorted(row["peak_extra_bytes"] for row in steady)
    peak = peaks[mid] if len(peaks) % 2 else int(0.5 * (peaks[mid - 1] + peaks[mid]))
    return result, {"median_seconds": median, "median_peak_extra_bytes": peak, "profiles": rows}


def _nearest_inertia(samples, centers):
    from kmeans_lloyd.iteration import assign_gemm_tiled, inertia

    labels = assign_gemm_tiled(samples, centers, tile_n=8192, tile_k=int(centers.shape[0]))
    value = inertia(samples, labels, centers)
    return float(value.detach().cpu()) if hasattr(value, "detach") else float(value)


def _fit(data, n_clusters, seed, max_iter, step=None, distance=None):
    from kmeans_lloyd.iteration import fit_kmeans

    tile_n = 65536 if int(data.shape[0]) > 65536 else 4096
    return fit_kmeans(
        data,
        n_clusters,
        np.random.default_rng(seed),
        max_iter=max_iter,
        tile_n=tile_n,
        tile_k=n_clusters,
        update_tile_k=min(n_clusters, 256),
        step=step,
        distance=distance,
    )


def _summarize(name, fitted, timing):
    timing = dict(timing)
    timing.update(
        {
            "name": name,
            "inertia": fitted["inertia"],
            "n_iter": fitted["n_iter"],
            "shift": fitted["shift"],
            "threshold": fitted["threshold"],
        }
    )
    return timing


def main():
    torch = _configure()
    from array_api_compat import array_namespace

    from kmeans_lloyd.iteration import (
        _distances_to_candidates,
        gemm_scores_argmin,
        kmeans_plusplus,
        lloyd_step,
    )

    out = ROOT / "journal" / "005-full-kmeans"
    out.mkdir(parents=True, exist_ok=True)
    samples = torch.as_tensor(_normal(TIMING), device="cuda")
    centers0 = samples[: TIMING["n_clusters"]].clone()

    def one_step():
        return lloyd_step(
            samples,
            centers0,
            65536,
            256,
            update_tile_k=256,
            update_tile_n=4096,
        )

    print("start tiled lloyd", flush=True)
    _, lloyd = _bench(one_step, samples, warmup=1, repeats=2)
    print(lloyd["median_seconds"], lloyd["median_peak_extra_bytes"], flush=True)

    def plusplus():
        return kmeans_plusplus(samples, TIMING["n_clusters"], np.random.default_rng(2))

    print("start plusplus", flush=True)
    (init_centers, _), plus = _bench(plusplus, samples, warmup=1, repeats=2)
    print(plus["median_seconds"], plus["median_peak_extra_bytes"], flush=True)
    init_inertia = _nearest_inertia(samples, init_centers)
    print("init inertia", init_inertia, flush=True)

    print("start fit 30", flush=True)
    fitted, fit_timing = _bench(lambda: _fit(samples, 256, 2, 30), samples, warmup=0, repeats=1)
    fit_timing = _summarize("fit-eager-tiled", fitted, fit_timing)
    print(fit_timing["median_seconds"], fit_timing["median_peak_extra_bytes"], fit_timing["n_iter"], flush=True)

    print("start fit 6", flush=True)
    fitted6, fit6 = _bench(lambda: _fit(samples, 256, 2, 6), samples, warmup=0, repeats=1)
    fit6 = _summarize("fit-eager-tiled-6", fitted6, fit6)
    print(fit6["median_seconds"], fit6["inertia"], fit6["shift"], flush=True)

    def distance_tensors(data, x_norm, candidates):
        return _distances_to_candidates(array_namespace(data), data, x_norm, candidates)

    compiled_distance = torch.compile(distance_tensors, fullgraph=False)
    x_norm = torch.sum(samples[:, :256] * samples[:, :256], dim=1)
    compiled_distance(samples, x_norm, samples[:7])

    def gemm_tile(x_tile, c_tile, c_norm):
        return gemm_scores_argmin(array_namespace(x_tile, c_tile, c_norm), x_tile, c_tile, c_norm)

    compiled_step = torch.compile(gemm_tile, fullgraph=False)
    compiled_step(samples[:65536], samples[:256], torch.sum(samples[:256] ** 2, dim=1))
    torch.cuda.synchronize()

    def distance_hook(xp, data, x_norm, candidates):
        del xp
        return compiled_distance(data, x_norm, candidates)

    print("start compiled fit", flush=True)
    fitted_c, fit_c = _bench(
        lambda: _fit(samples, 256, 2, 30, step=compiled_step, distance=distance_hook),
        samples,
        warmup=0,
        repeats=1,
    )
    fit_c = _summarize("fit-compiled-tiled", fitted_c, fit_c)
    print(fit_c["median_seconds"], fit_c["median_peak_extra_bytes"], fit_c["inertia"], flush=True)

    blobs = torch.as_tensor(_blobs(BLOBS), device="cuda")
    print("start blobs", flush=True)
    blob_fit, blob_timing = _bench(lambda: _fit(blobs, 8, 3, 40), blobs, warmup=0, repeats=1)
    blob_timing = _summarize("fit-blobs-tiled", blob_fit, blob_timing)
    blob_init, _ = kmeans_plusplus(blobs, 8, np.random.default_rng(3))
    blob_init_inertia = _nearest_inertia(blobs, blob_init)
    np.save(out / "blobs-labels-torch-tiled.npy", blob_fit["labels"].detach().cpu().numpy())

    payload = {
        "note": "row norm uses feature tiles of 256; inertia and the centroid update use sample tiles",
        "lloyd": {k: lloyd[k] for k in lloyd if k != "profiles"},
        "plusplus": {k: plus[k] for k in plus if k != "profiles"},
        "init_inertia_timing": init_inertia,
        "init_inertia_blobs": blob_init_inertia,
        "fit": {k: fit_timing[k] for k in fit_timing if k != "profiles"},
        "fit_6": {k: fit6[k] for k in fit6 if k != "profiles"},
        "fit_compiled": {k: fit_c[k] for k in fit_c if k != "profiles"},
        "blobs": {k: blob_timing[k] for k in blob_timing if k != "profiles"},
    }
    (out / "optimized.json").write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(payload, indent=2), flush=True)


if __name__ == "__main__":
    main()
