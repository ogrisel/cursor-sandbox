"""Time k-means++ from cakedev0/scikit-learn#23.

Run this with the virtualenv built from that pull request. The selected
centers are not the same sequence as the array-API implementation: that
pull request samples from per-chunk sums instead of one cumulative sum.
"""

from __future__ import annotations

import json
import resource
import time
from pathlib import Path

import numpy as np

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


def _time(fn, warmup, repeats):
    for _ in range(warmup):
        fn()
    samples = []
    for _ in range(repeats):
        started = time.perf_counter()
        fn()
        samples.append(time.perf_counter() - started)
    ordered = sorted(samples)
    mid = len(ordered) // 2
    median = ordered[mid] if len(ordered) % 2 else 0.5 * (ordered[mid - 1] + ordered[mid])
    return median, samples


def _inertia(samples, centers):
    # Squared distance to the nearest center, in chunks so the (n, k) matrix
    # is not formed when k is large.
    total = 0.0
    chunk = 4096
    norms = np.sum(centers * centers, axis=1)
    for start in range(0, samples.shape[0], chunk):
        block = samples[start : start + chunk]
        scores = np.sum(block * block, axis=1)[:, None] + norms[None, :] - 2 * block @ centers.T
        total += float(np.min(scores, axis=1).sum())
    return total


def main():
    from sklearn.cluster import kmeans_plusplus
    import sklearn

    out = Path(__file__).resolve().parents[1] / "journal" / "005-full-kmeans"
    out.mkdir(parents=True, exist_ok=True)
    samples = _normal(TIMING)

    def run():
        kmeans_plusplus(samples, n_clusters=TIMING["n_clusters"], random_state=0)

    median, draws = _time(run, warmup=1, repeats=2)
    centers, _ = kmeans_plusplus(samples, n_clusters=TIMING["n_clusters"], random_state=0)
    blobs = _blobs(BLOBS)
    blob_centers, _ = kmeans_plusplus(blobs, n_clusters=BLOBS["n_clusters"], random_state=3)
    payload = {
        "sklearn": sklearn.__version__,
        "commit": "7e26a5c37e1fa8031bef7da0ee43b633b07c8b9b",
        "pull_request": "https://github.com/cakedev0/scikit-learn/pull/23",
        "case": TIMING,
        "median_seconds": median,
        "samples": draws,
        "ru_maxrss_kb": int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss),
        "init_inertia": _inertia(samples, np.asarray(centers, dtype=np.float32)),
        "blob_init_inertia": _inertia(blobs, np.asarray(blob_centers, dtype=np.float32)),
    }
    (out / "plusplus-cpu.json").write_text(json.dumps(payload, indent=2) + "\n")
    np.save(out / "blobs-centers-cpu.npy", np.asarray(blob_centers, dtype=np.float32))
    print(json.dumps(payload, indent=2), flush=True)


if __name__ == "__main__":
    main()
