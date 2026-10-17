"""Time cuML KMeans on the same arrays as fit_kmeans.

Device memory is the nvidia-smi high-water mark during fit, because cuML
does not report a peak through the PyTorch allocator.
"""

from __future__ import annotations

import json
import subprocess
import threading
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


def _used_mib():
    text = subprocess.check_output(
        ["nvidia-smi", "--query-gpu=memory.used", "--format=csv,noheader,nounits"],
        text=True,
    )
    return int(text.strip().splitlines()[0])


def _fit_sampled(fn):
    peak = {"value": _used_mib()}
    stop = {"flag": False}

    def watch():
        while not stop["flag"]:
            peak["value"] = max(peak["value"], _used_mib())
            time.sleep(0.05)

    thread = threading.Thread(target=watch)
    thread.start()
    started = time.perf_counter()
    try:
        result = fn()
    finally:
        stop["flag"] = True
        thread.join()
    return result, time.perf_counter() - started, peak["value"]


def _inertia(samples, labels, centers):
    assigned = centers[labels]
    diff = samples - assigned
    return float(np.sum(diff * diff))


def main():
    from cuml.cluster import KMeans
    import cuml

    out = Path(__file__).resolve().parents[1] / "journal" / "005-full-kmeans"
    out.mkdir(parents=True, exist_ok=True)
    before = _used_mib()

    def one(samples, n_clusters, max_iter, seed):
        model = KMeans(
            n_clusters=n_clusters,
            max_iter=max_iter,
            tol=1e-4,
            init="k-means++",
            random_state=seed,
            output_type="numpy",
            n_init=1,
        )
        model.fit(samples)
        labels = np.asarray(model.labels_)
        centers = np.asarray(model.cluster_centers_, dtype=np.float32)
        n_iter = int(getattr(model, "n_iter_", -1))
        reported = getattr(model, "inertia_", None)
        return labels, centers, n_iter, None if reported is None else float(np.asarray(reported))

    samples = _normal(TIMING)
    # One warmup fit so the first timed call is not the library load.
    one(samples[:4096], 4, 2, 0)
    labels, centers, n_iter, reported = None, None, None, None

    def run():
        nonlocal labels, centers, n_iter, reported
        labels, centers, n_iter, reported = one(samples, TIMING["n_clusters"], 30, 2)

    _, seconds, peak = _fit_sampled(run)
    inertia = _inertia(samples, labels, centers)
    blobs = _blobs(BLOBS)

    def run_blobs():
        return one(blobs, BLOBS["n_clusters"], 40, 3)

    blob_result, blob_seconds, blob_peak = _fit_sampled(run_blobs)
    blob_labels, blob_centers, blob_iters, blob_reported = blob_result
    payload = {
        "cuml": cuml.__version__,
        "before_mib": before,
        "timing": {
            "case": TIMING,
            "seconds": seconds,
            "peak_used_mib": peak,
            "n_iter": n_iter,
            "inertia": inertia,
            "reported_inertia": reported,
        },
        "blobs": {
            "case": BLOBS,
            "seconds": blob_seconds,
            "peak_used_mib": blob_peak,
            "n_iter": blob_iters,
            "inertia": _inertia(blobs, blob_labels, blob_centers),
            "reported_inertia": blob_reported,
        },
    }
    (out / "cuml.json").write_text(json.dumps(payload, indent=2) + "\n")
    np.save(out / "blobs-labels-cuml.npy", blob_labels)
    np.save(out / "blobs-centers-cuml.npy", blob_centers)
    print(json.dumps(payload, indent=2), flush=True)


if __name__ == "__main__":
    main()
