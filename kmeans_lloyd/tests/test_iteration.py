"""Correctness checks for one Lloyd iteration. GPU backends are optional."""

from __future__ import annotations

import numpy as np
import pytest
from array_api_compat import array_namespace

from kmeans_lloyd.iteration import (
    assign_gemm,
    assign_gemm_tiled,
    assign_naive,
    assign_running,
    assign_running_stateful,
    assign_running_tiled,
    assign_tiled,
    fit_kmeans,
    inertia,
    kmeans_plusplus,
    lloyd_iteration,
    lloyd_step,
    update_centroids,
    update_centroids_tiled,
)


def _blobs(n_per=12, d=6, k=3, dtype=np.float64, seed=0):
    rng = np.random.default_rng(seed)
    centers = np.array(
        [[-4.0, 0.0, 1.0, 0.5, -1.0, 2.0], [3.0, 3.0, -2.0, 0.0, 1.0, -1.0], [0.5, -3.0, 2.5, 4.0, 0.0, 0.5]],
        dtype=dtype,
    )[:k, :d]
    pieces = []
    for center in centers:
        pieces.append(center + 0.05 * rng.standard_normal((n_per, d)))
    x = np.concatenate(pieces, axis=0).astype(dtype)
    initial = x[:k].copy()
    return x, initial


def _to_numpy(array):
    module = type(array).__module__
    if module.startswith("torch"):
        return array.detach().cpu().numpy()
    if module.startswith("cupy"):
        return array.get()
    return np.asarray(array)


def _as_numpy_namespace(array):
    import array_api_compat.numpy as xp

    return xp.asarray(array)


def test_naive_matches_explicit_loop():
    x_np, c_np = _blobs()
    x = _as_numpy_namespace(x_np)
    c = _as_numpy_namespace(c_np)
    labels = _to_numpy(assign_naive(x, c))
    expected = np.empty(x_np.shape[0], dtype=np.int64)
    for i, row in enumerate(x_np):
        dist = np.sum((c_np - row) ** 2, axis=1)
        expected[i] = np.argmin(dist)
    np.testing.assert_array_equal(labels, expected)


def test_tiled_and_running_match_naive():
    x_np, c_np = _blobs(n_per=10, d=5, k=3)
    x = _as_numpy_namespace(x_np)
    c = _as_numpy_namespace(c_np)
    reference = _to_numpy(assign_naive(x, c))
    tiled = _to_numpy(assign_tiled(x, c, tile_n=7, tile_k=2, distance="broadcast"))
    running = _to_numpy(assign_running(x, c))
    retiled = _to_numpy(assign_running_tiled(x, c, tile_k=2))
    np.testing.assert_array_equal(tiled, reference)
    np.testing.assert_array_equal(running, reference)
    np.testing.assert_array_equal(retiled, reference)


def test_gemm_matches_naive_in_float64():
    x_np, c_np = _blobs()
    x = _as_numpy_namespace(x_np)
    c = _as_numpy_namespace(c_np)
    np.testing.assert_array_equal(_to_numpy(assign_gemm(x, c)), _to_numpy(assign_naive(x, c)))


def test_empty_cluster_keeps_previous_centroid():
    x_np = np.array([[0.0, 0.0], [0.1, -0.1], [5.0, 5.0]], dtype=np.float64)
    c_np = np.array([[0.0, 0.0], [1.0, 1.0], [100.0, -100.0]], dtype=np.float64)
    x = _as_numpy_namespace(x_np)
    c = _as_numpy_namespace(c_np)
    updated, labels = lloyd_iteration(x, c)
    updated = _to_numpy(updated)
    labels = _to_numpy(labels)
    assert set(labels.tolist()) == {0, 1}
    np.testing.assert_allclose(updated[2], c_np[2])
    members = x_np[labels == 0]
    np.testing.assert_allclose(updated[0], members.mean(axis=0))


def test_update_centroids_mean():
    x_np = np.array([[0.0, 0.0], [2.0, 4.0], [10.0, 0.0]], dtype=np.float64)
    labels_np = np.array([0, 0, 1], dtype=np.int64)
    c_np = np.zeros((2, 2), dtype=np.float64)
    xp = array_namespace(_as_numpy_namespace(x_np))
    updated = update_centroids(
        _as_numpy_namespace(x_np),
        xp.asarray(labels_np),
        _as_numpy_namespace(c_np),
    )
    np.testing.assert_allclose(_to_numpy(updated)[0], [1.0, 2.0])
    np.testing.assert_allclose(_to_numpy(updated)[1], [10.0, 0.0])


def test_gemm_tiled_matches_naive_when_tiles_do_not_divide():
    x_np, c_np = _blobs(n_per=9, d=4, k=3)
    x = _as_numpy_namespace(x_np)
    c = _as_numpy_namespace(c_np)
    reference = _to_numpy(assign_naive(x, c))
    tiled = _to_numpy(assign_gemm_tiled(x, c, tile_n=5, tile_k=2))
    stateful = _to_numpy(assign_running_stateful(x, c, tile_k=2))
    np.testing.assert_array_equal(tiled, reference)
    np.testing.assert_array_equal(stateful, reference)


def test_tiled_update_matches_one_hot_update():
    x_np = np.array([[0.0, 0.0], [2.0, 4.0], [10.0, 0.0], [11.0, 1.0]], dtype=np.float64)
    labels_np = np.array([0, 0, 1, 2], dtype=np.int64)
    c_np = np.array([[9.0, 9.0], [8.0, 8.0], [7.0, 7.0], [6.0, 6.0]], dtype=np.float64)
    x = _as_numpy_namespace(x_np)
    labels = array_namespace(x).asarray(labels_np)
    c = _as_numpy_namespace(c_np)
    full = _to_numpy(update_centroids(x, labels, c))
    tiled = _to_numpy(update_centroids_tiled(x, labels, c, tile_k=3))
    chunked = _to_numpy(update_centroids_tiled(x, labels, c, tile_k=3, tile_n=3))
    np.testing.assert_allclose(tiled, full)
    np.testing.assert_allclose(chunked, full)
    np.testing.assert_allclose(tiled[3], c_np[3])


def test_lloyd_step_matches_naive_iteration():
    x_np, c_np = _blobs(n_per=8, d=4, k=3)
    x = _as_numpy_namespace(x_np)
    c = _as_numpy_namespace(c_np)
    reference, reference_labels = lloyd_iteration(x, c, assign="naive")
    updated, labels = lloyd_step(x, c, tile_n=5, tile_k=2, update_tile_k=2)
    np.testing.assert_array_equal(_to_numpy(labels), _to_numpy(reference_labels))
    np.testing.assert_allclose(_to_numpy(updated), _to_numpy(reference))


def test_kmeans_plusplus_second_center_is_far_from_the_first():
    x_np = np.array([[0.0, 0.0], [0.1, 0.0], [10.0, 10.0], [10.2, 9.8]], dtype=np.float64)
    x = _as_numpy_namespace(x_np)

    class _Rng:
        def integers(self, n, size=None):
            if size is None:
                return 0
            return np.zeros(size, dtype=np.int64)

        def random(self, size):
            return np.full(size, 0.99)

    centers, indices = kmeans_plusplus(x, 2, _Rng(), n_local_trials=1)
    indices = _to_numpy(indices)
    assert indices[0] == 0
    assert indices[1] in (2, 3)
    np.testing.assert_allclose(_to_numpy(centers), x_np[indices])


def test_kmeans_plusplus_is_deterministic_for_a_generator():
    x_np, _ = _blobs(n_per=6, d=4, k=3)
    x = _as_numpy_namespace(x_np)
    first = _to_numpy(kmeans_plusplus(x, 3, np.random.default_rng(4))[1])
    second = _to_numpy(kmeans_plusplus(x, 3, np.random.default_rng(4))[1])
    np.testing.assert_array_equal(first, second)
    assert len(set(first.tolist())) == 3


def test_mean_feature_variance_matches_library_var():
    from kmeans_lloyd.iteration import _mean_feature_variance

    rng = np.random.default_rng(0)
    x_np = rng.standard_normal((40, 17)).astype(np.float64)
    x = _as_numpy_namespace(x_np)
    xp = array_namespace(x)
    got = float(_to_numpy(_mean_feature_variance(xp, x, tile_d=5)))
    expected = float(np.var(x_np, axis=0).mean())
    np.testing.assert_allclose(got, expected, rtol=1e-10, atol=1e-12)


def test_fit_kmeans_converges_on_separated_blobs():
    rng = np.random.default_rng(0)
    centers = np.array([[0.0, 0.0, 0.0, 0.0], [8.0, 0.0, 0.0, 0.0], [0.0, 8.0, 0.0, 0.0]])
    pieces = [center + 0.05 * rng.standard_normal((25, 4)) for center in centers]
    x_np = np.concatenate(pieces).astype(np.float64)
    x = _as_numpy_namespace(x_np)
    fitted = fit_kmeans(
        x,
        3,
        np.random.default_rng(1),
        max_iter=30,
        tile_n=9,
        tile_k=2,
        update_tile_k=2,
    )
    assert fitted["n_iter"] < 30
    assert fitted["shift"] <= fitted["threshold"]
    labels = _to_numpy(fitted["labels"])
    assert len(set(labels.tolist())) == 3
    manual = 0.0
    centers_np = _to_numpy(fitted["centers"])
    for row, label in zip(x_np, labels):
        manual += np.sum((row - centers_np[label]) ** 2)
    np.testing.assert_allclose(fitted["inertia"], manual)
    np.testing.assert_allclose(fitted["inertia"], float(_to_numpy(inertia(x, fitted["labels"], fitted["centers"]))))
    np.testing.assert_allclose(
        fitted["inertia"],
        float(_to_numpy(inertia(x, fitted["labels"], fitted["centers"], tile_n=7))),
    )


def _gpu_pairs():
    pairs = []
    try:
        import torch

        if torch.cuda.is_available():
            pairs.append(("torch", torch))
    except ImportError:
        pass
    try:
        import cupy

        if cupy.cuda.runtime.getDeviceCount() > 0:
            pairs.append(("cupy", cupy))
    except Exception:
        pass
    return pairs


@pytest.mark.parametrize("backend", [name for name, _ in _gpu_pairs()] or [pytest.param("none", marks=pytest.mark.skip)])
def test_gpu_assignment_matches_numpy(backend):
    modules = dict(_gpu_pairs())
    xp_mod = modules[backend]
    x_np, c_np = _blobs(dtype=np.float32, seed=1)
    if backend == "torch":
        x = xp_mod.as_tensor(x_np, device="cuda")
        c = xp_mod.as_tensor(c_np, device="cuda")
    else:
        x = xp_mod.asarray(x_np)
        c = xp_mod.asarray(c_np)
    reference = _to_numpy(assign_naive(_as_numpy_namespace(x_np.astype(np.float64)), _as_numpy_namespace(c_np.astype(np.float64))))
    labels = _to_numpy(assign_naive(x, c))
    tiled = _to_numpy(assign_tiled(x, c, tile_n=8, tile_k=2, distance="broadcast"))
    running = _to_numpy(assign_running(x, c))
    gemm_tiled = _to_numpy(assign_gemm_tiled(x, c, tile_n=8, tile_k=2))
    stateful = _to_numpy(assign_running_stateful(x, c, tile_k=2))
    np.testing.assert_array_equal(labels, reference)
    np.testing.assert_array_equal(tiled, reference)
    np.testing.assert_array_equal(running, reference)
    np.testing.assert_array_equal(gemm_tiled, reference)
    np.testing.assert_array_equal(stateful, reference)
    centers, plus_index = kmeans_plusplus(x, c_np.shape[0], np.random.default_rng(2))
    assert _to_numpy(centers).shape == c_np.shape
    assert _to_numpy(plus_index).shape == (c_np.shape[0],)
    updated, _ = lloyd_iteration(x, c, assign="gemm")
    assert _to_numpy(updated).shape == c_np.shape
