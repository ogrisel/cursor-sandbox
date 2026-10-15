"""Correctness checks for one Lloyd iteration. GPU backends are optional."""

from __future__ import annotations

import numpy as np
import pytest
from array_api_compat import array_namespace

from kmeans_lloyd.iteration import (
    assign_gemm,
    assign_naive,
    assign_running,
    assign_running_tiled,
    assign_tiled,
    lloyd_iteration,
    update_centroids,
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
    np.testing.assert_array_equal(labels, reference)
    np.testing.assert_array_equal(tiled, reference)
    np.testing.assert_array_equal(running, reference)
    updated, _ = lloyd_iteration(x, c, assign="gemm")
    assert _to_numpy(updated).shape == c_np.shape
