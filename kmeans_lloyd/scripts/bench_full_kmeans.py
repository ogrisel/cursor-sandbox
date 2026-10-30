"""Time a full k-means fit: k-means++ plus Lloyd until convergence.

The fit itself is ``fit_kmeans``. ``torch.compile`` is optional and stays
outside that function.
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

# Bandwidth-bound init: each new center rereads X. This shape is about a
# second of that traffic on an L4, and a Lloyd iteration is in the same range
# once several iterations are added.
TIMING = {"name": "timing", "n_samples": 131_072, "n_features": 2_048, "n_clusters": 256, "seed": 0}
# Separated blobs. Both implementations should reach nearly the same inertia.
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


def main():
    torch = _configure()
    from array_api_compat import array_namespace

    from kmeans_lloyd.iteration import (
        _distances_to_candidates,
        fit_kmeans,
        gemm_scores_argmin,
        kmeans_plusplus,
        lloyd_step,
    )

    out = ROOT / "journal" / "005-full-kmeans"
    out.mkdir(parents=True, exist_ok=True)
    payload = {"gpu": torch.cuda.get_device_name(0), "torch": torch.__version__, "runs": []}

    def save():
        (out / "results.json").write_text(json.dumps(payload, indent=2) + "\n")

    samples_np = _normal(TIMING)
    samples = torch.as_tensor(samples_np, device="cuda")
    centers0 = samples[: TIMING["n_clusters"]].clone()

    # One Lloyd step. tile_k covers every centroid except the rows that split k.
    tiles = [
        (1024, 256),
        (4096, 256),
        (16384, 256),
        (65536, 256),
        (131072, 256),
        (4096, 128),
        (4096, 64),
        (4096, 32),
    ]
    for tile_n, tile_k in tiles:
        name = f"lloyd-{tile_n}x{tile_k}"
        print("start", name, flush=True)

        def one_step(tile_n=tile_n, tile_k=tile_k):
            return lloyd_step(samples, centers0, tile_n, tile_k, update_tile_k=min(tile_k, 256))

        _, timing = _bench(one_step, samples, warmup=1, repeats=2)
        timing.update({"name": name, "tile_n": tile_n, "tile_k": tile_k, "case": TIMING})
        payload["runs"].append(timing)
        print(timing["median_seconds"], timing["median_peak_extra_bytes"], flush=True)
        save()

    def plusplus():
        return kmeans_plusplus(samples, TIMING["n_clusters"], np.random.default_rng(2))

    print("start eager plusplus", flush=True)
    _, timing = _bench(plusplus, samples, warmup=1, repeats=2)
    timing.update({"name": "plusplus-eager", "case": TIMING})
    payload["runs"].append(timing)
    print(timing["median_seconds"], timing["median_peak_extra_bytes"], flush=True)
    save()

    def distance_tensors(data, x_norm, candidates):
        return _distances_to_candidates(array_namespace(data), data, x_norm, candidates)

    compiled_distance = torch.compile(distance_tensors, fullgraph=False)
    compiled_distance(samples, torch.sum(samples * samples, dim=1), samples[:8])
    torch.cuda.synchronize()

    def distance_hook(xp, data, x_norm, candidates):
        del xp
        return compiled_distance(data, x_norm, candidates)

    def plusplus_compiled():
        return kmeans_plusplus(
            samples,
            TIMING["n_clusters"],
            np.random.default_rng(2),
            distance=distance_hook,
        )

    print("start compiled plusplus", flush=True)
    _, timing = _bench(plusplus_compiled, samples, warmup=1, repeats=2)
    timing.update({"name": "plusplus-compiled", "case": TIMING})
    payload["runs"].append(timing)
    print(timing["median_seconds"], timing["median_peak_extra_bytes"], flush=True)
    save()

    def gemm_tile(x_tile, c_tile, c_norm):
        return gemm_scores_argmin(array_namespace(x_tile, c_tile, c_norm), x_tile, c_tile, c_norm)

    compiled_step = torch.compile(gemm_tile, fullgraph=False)
    compiled_step(samples[:4096], samples[: TIMING["n_clusters"]], torch.sum(samples[: TIMING["n_clusters"]] ** 2, dim=1))
    torch.cuda.synchronize()

    def fit(step=None, distance_fn=None):
        return fit_kmeans(
            samples,
            TIMING["n_clusters"],
            np.random.default_rng(2),
            max_iter=30,
            tile_n=4096,
            tile_k=TIMING["n_clusters"],
            update_tile_k=256,
            step=step,
            distance=distance_fn,
        )

    print("start eager fit", flush=True)
    fitted, timing = _bench(lambda: fit(), samples, warmup=0, repeats=1)
    timing.update(
        {
            "name": "fit-eager",
            "case": TIMING,
            "inertia": fitted["inertia"],
            "n_iter": fitted["n_iter"],
            "shift": fitted["shift"],
            "threshold": fitted["threshold"],
        }
    )
    payload["runs"].append(timing)
    print(timing, flush=True)
    save()

    print("start compiled fit", flush=True)
    fitted_c, timing = _bench(lambda: fit(step=compiled_step, distance_fn=distance_hook), samples, warmup=0, repeats=1)
    timing.update(
        {
            "name": "fit-compiled",
            "case": TIMING,
            "inertia": fitted_c["inertia"],
            "n_iter": fitted_c["n_iter"],
            "shift": fitted_c["shift"],
            "threshold": fitted_c["threshold"],
        }
    )
    payload["runs"].append(timing)
    print(timing, flush=True)
    save()

    blobs_np = _blobs(BLOBS)
    blobs = torch.as_tensor(blobs_np, device="cuda")
    print("start blob fit", flush=True)
    blob_fit, timing = _bench(
        lambda: fit_kmeans(
            blobs,
            BLOBS["n_clusters"],
            np.random.default_rng(3),
            max_iter=40,
            tile_n=4096,
            tile_k=BLOBS["n_clusters"],
            update_tile_k=BLOBS["n_clusters"],
        ),
        blobs,
        warmup=0,
        repeats=1,
    )
    timing.update(
        {
            "name": "fit-blobs",
            "case": BLOBS,
            "inertia": blob_fit["inertia"],
            "n_iter": blob_fit["n_iter"],
            "shift": blob_fit["shift"],
            "threshold": blob_fit["threshold"],
        }
    )
    payload["runs"].append(timing)
    np.save(out / "blobs-labels-torch.npy", blob_fit["labels"].detach().cpu().numpy())
    np.save(out / "blobs-centers-torch.npy", blob_fit["centers"].detach().cpu().numpy())
    np.save(out / "timing-centers-torch.npy", fitted["centers"].detach().cpu().numpy())
    print(timing, flush=True)
    save()


if __name__ == "__main__":
    main()
