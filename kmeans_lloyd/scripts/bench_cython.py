"""Time one dense Lloyd iteration from cakedev0/scikit-learn#26.

The routine is ``sklearn.cluster._k_means_lloyd.lloyd_iter_chunked_dense``
on that branch: sample chunks of 256, a GEMM for ``||c||^2 - 2 x·c``,
then a scatter into per-thread center buffers. This script does not import
PyTorch. Run it with the virtualenv that installed that branch.
"""

from __future__ import annotations

import json
import os
import platform
import resource
import time
from pathlib import Path

import numpy as np

COMPARE = {"name": "cython-compare", "n_samples": 65_536, "n_clusters": 1_024, "n_features": 2_048}


def _labels_reference(samples, centroids):
    norms = np.sum(centroids * centroids, axis=1)
    scores = norms[None, :] - 2 * samples @ centroids.T
    return np.argmin(scores, axis=1).astype(np.int32)


def _call(lloyd, samples, centroids, update_centers, n_threads):
    n_samples, n_clusters = samples.shape[0], centroids.shape[0]
    centers_new = np.zeros_like(centroids)
    weights = np.zeros(n_clusters, dtype=np.float32)
    labels = np.empty(n_samples, dtype=np.int32)
    shift = np.zeros(n_clusters, dtype=np.float32)
    sample_weight = np.ones(n_samples, dtype=np.float32)
    lloyd(
        samples,
        sample_weight,
        centroids,
        centers_new,
        weights,
        labels,
        shift,
        n_threads,
        update_centers,
    )
    return labels, centers_new


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
    if len(ordered) % 2:
        median = ordered[mid]
    else:
        median = 0.5 * (ordered[mid - 1] + ordered[mid])
    return median, samples


def main():
    from sklearn.cluster._k_means_common import CHUNK_SIZE
    from sklearn.cluster._k_means_lloyd import lloyd_iter_chunked_dense
    import sklearn

    check_rng = np.random.default_rng(1)
    small_x = check_rng.standard_normal((180, 7)).astype(np.float32)
    small_c = np.ascontiguousarray(small_x[:6])
    small_labels, _ = _call(lloyd_iter_chunked_dense, small_x, small_c, False, 2)
    reference = _labels_reference(small_x, small_c)
    if not np.array_equal(small_labels, reference):
        mismatch = int(np.sum(small_labels != reference))
        raise SystemExit(f"small assign disagreed in {mismatch} rows")

    rng = np.random.default_rng(0)
    samples = rng.standard_normal((COMPARE["n_samples"], COMPARE["n_features"])).astype(np.float32)
    centroids = np.ascontiguousarray(samples[: COMPARE["n_clusters"]])
    n_threads = os.cpu_count() or 1
    n_chunks = max(1, COMPARE["n_samples"] // CHUNK_SIZE)
    threads_used = min(n_threads, n_chunks)
    theoretical = (
        threads_used * CHUNK_SIZE * COMPARE["n_clusters"] * 4
        + threads_used * COMPARE["n_clusters"] * COMPARE["n_features"] * 4
    )

    def assign():
        _call(lloyd_iter_chunked_dense, samples, centroids, False, n_threads)

    def full():
        _call(lloyd_iter_chunked_dense, samples, centroids, True, n_threads)

    assign_median, assign_samples = _time(assign, warmup=1, repeats=3)
    labels, _ = _call(lloyd_iter_chunked_dense, samples, centroids, False, n_threads)
    reference = _labels_reference(samples, centroids)
    full_median, full_samples = _time(full, warmup=1, repeats=3)
    rss_kb = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    out = Path(__file__).resolve().parents[1] / "journal" / "004-tile-tradeoff"
    out.mkdir(parents=True, exist_ok=True)
    np.save(out / "compare-labels-cython.npy", labels)
    payload = {
        "sklearn": sklearn.__version__,
        "chunk_size": int(CHUNK_SIZE),
        "n_threads": threads_used,
        "cpu_count": n_threads,
        "host": platform.node(),
        "case": COMPARE,
        "assign_median_seconds": assign_median,
        "assign_samples": assign_samples,
        "lloyd_median_seconds": full_median,
        "lloyd_samples": full_samples,
        "label_mismatch_vs_numpy_scores": int(np.sum(labels != reference)),
        "n_labels": int(labels.shape[0]),
        "theoretical_thread_bytes": int(theoretical),
        "ru_maxrss_kb": int(rss_kb),
        "compiler_note": "Built with the host g++. The PR reports dense Lloyd is in the same range on GCC 13 as on newer GCC for the laptop table.",
    }
    (out / "cython.json").write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(payload, indent=2), flush=True)


if __name__ == "__main__":
    main()
