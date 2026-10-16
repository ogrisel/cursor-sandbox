"""Tests for the scikit-learn compatible array-API KMeans estimator."""

from __future__ import annotations

import numpy as np
import pytest
from sklearn.utils.estimator_checks import parametrize_with_checks

from kmeans_lloyd import KMeans


def _blobs(seed=0):
    rng = np.random.default_rng(seed)
    centers = np.array([[-4.0, 0.0], [0.0, 4.0], [4.0, 0.0]])
    return np.concatenate(
        [center + 0.1 * rng.standard_normal((20, 2)) for center in centers]
    )


@parametrize_with_checks([KMeans(n_clusters=2, n_init=1, max_iter=20)])
def test_sklearn_estimator_checks(estimator, check):
    check(estimator)


@pytest.mark.parametrize("init", ["k-means++", "random"])
def test_initializers_are_deterministic(init):
    X = _blobs()
    first = KMeans(3, init=init, n_init=2, random_state=0).fit(X)
    second = KMeans(3, init=init, n_init=2, random_state=0).fit(X)
    np.testing.assert_allclose(first.cluster_centers_, second.cluster_centers_)
    np.testing.assert_array_equal(first.labels_, second.labels_)
    assert first.inertia_ == second.inertia_


def test_fit_predict_transform_and_score_match_objective():
    X = _blobs()
    model = KMeans(3, random_state=0).fit(X)
    distances = model.transform(X)
    labels = model.predict(X)
    np.testing.assert_array_equal(labels, model.labels_)
    np.testing.assert_allclose(np.sum(distances[np.arange(X.shape[0]), labels] ** 2), model.inertia_)
    assert model.score(X) == pytest.approx(-model.inertia_)


def test_rejects_unsupported_kmeans_options():
    X = _blobs()
    with pytest.raises(ValueError, match="init"):
        KMeans(3, init="scalable").fit(X)
    with pytest.raises(ValueError, match="algorithm"):
        KMeans(3, algorithm="elkan").fit(X)


def test_numpy_float32_is_preserved():
    model = KMeans(3, random_state=0).fit(_blobs().astype(np.float32))
    assert model.cluster_centers_.dtype == np.float32


def test_array_api_numpy_input():
    import array_api_compat.numpy as xp

    X = xp.asarray(_blobs().astype(np.float32))
    model = KMeans(3, random_state=0).fit(X)
    assert model.cluster_centers_.dtype == X.dtype
    assert model.predict(X).shape == (X.shape[0],)


def _gpu_backends():
    backends = []
    try:
        import torch

        if torch.cuda.is_available():
            backends.append(("torch", torch))
    except ImportError:
        pass
    try:
        import cupy

        if cupy.cuda.runtime.getDeviceCount() > 0:
            backends.append(("cupy", cupy))
    except (ImportError, RuntimeError):
        pass
    return backends


@pytest.mark.parametrize(
    "backend",
    [name for name, _ in _gpu_backends()]
    or [pytest.param("none", marks=pytest.mark.skip)],
)
def test_cuda_backends_preserve_namespace_and_dtype(backend):
    module = dict(_gpu_backends())[backend]
    host = _blobs().astype(np.float32)
    if backend == "torch":
        X = module.as_tensor(host, device="cuda")
    else:
        X = module.asarray(host)
    model = KMeans(3, n_init=1, random_state=0).fit(X)
    assert type(model.cluster_centers_).__module__.startswith(backend)
    assert model.cluster_centers_.dtype == X.dtype
    assert model.predict(X).shape == (X.shape[0],)
    assert model.transform(X).shape == (X.shape[0], 3)
