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


def test_explicit_initial_centers_run_once_and_warn():
    X = _blobs()
    centers = X[[0, 20, 40]]
    with pytest.warns(RuntimeWarning, match="only one init"):
        model = KMeans(3, init=centers, n_init=3, max_iter=1).fit(X)
    expected = np.stack([X[labels].mean(axis=0) for labels in np.split(np.arange(60), 3)])
    np.testing.assert_allclose(model.cluster_centers_, expected)
    assert model.n_iter_ == 1


def test_callable_init_receives_random_state():
    X = _blobs()
    seen = {}

    def init(X, n_clusters, random_state):
        seen["random_state"] = random_state
        return X[:n_clusters]

    KMeans(3, init=init, n_init=1, random_state=0).fit(X)
    assert isinstance(seen["random_state"], np.random.RandomState)


def test_explicit_centers_with_wrong_shape_are_rejected():
    with pytest.raises(ValueError, match="shape of the initial centers"):
        KMeans(3, init=np.zeros((2, 2))).fit(_blobs())


def test_portable_namespaces_have_no_native_path():
    import array_api_compat.numpy as xp

    from kmeans_lloyd.backends import native_accumulate

    assert native_accumulate(np.zeros((2, 2))) is None
    assert native_accumulate(xp.zeros((2, 2))) is None


def _native_backends():
    backends = []
    try:
        import torch

        backends.append(("torch-cpu", lambda a: torch.as_tensor(a)))
        if torch.cuda.is_available():
            backends.append(("torch-cuda", lambda a: torch.as_tensor(a, device="cuda")))
    except ImportError:
        pass
    try:
        import cupy

        if cupy.cuda.runtime.getDeviceCount() > 0:
            backends.append(("cupy", cupy.asarray))
    except (ImportError, RuntimeError):
        pass
    return backends


def _to_host(array):
    if hasattr(array, "get"):
        return array.get()
    if hasattr(array, "detach"):
        return array.detach().cpu().numpy()
    return np.asarray(array)


@pytest.mark.parametrize(
    "backend",
    [name for name, _ in _native_backends()]
    or [pytest.param("none", marks=pytest.mark.skip)],
)
@pytest.mark.parametrize("dtype", [np.float32, np.float64])
def test_native_update_matches_portable_one_hot(backend, dtype):
    from kmeans_lloyd.backends import native_accumulate
    from kmeans_lloyd.iteration import update_centroids_tiled

    convert = dict(_native_backends())[backend]
    rng = np.random.default_rng(0)
    X = convert(rng.standard_normal((257, 3)).astype(dtype))
    # Cluster 4 is empty, so both paths must run the farthest relocation.
    labels = convert(rng.choice([0, 1, 2, 3, 5], size=257).astype(np.int64))
    centers = convert(rng.standard_normal((6, 3)).astype(dtype))
    accumulate = native_accumulate(X)
    assert accumulate is not None
    portable_stats, native_stats = {}, {}
    portable = update_centroids_tiled(
        X, labels, centers, tile_k=4, tile_n=50, reassign_empty=True, stats=portable_stats
    )
    native = update_centroids_tiled(
        X,
        labels,
        centers,
        tile_k=4,
        tile_n=50,
        reassign_empty=True,
        stats=native_stats,
        accumulate=accumulate,
    )
    rtol = 1e-5 if dtype == np.float32 else 1e-12
    np.testing.assert_allclose(_to_host(native), _to_host(portable), rtol=rtol, atol=rtol)
    assert native_stats == portable_stats == {"empty_events": 1, "reassignments": 1}


@pytest.mark.parametrize(
    "backend",
    [name for name, _ in _native_backends()]
    or [pytest.param("none", marks=pytest.mark.skip)],
)
def test_estimator_native_and_portable_paths_agree(backend):
    from kmeans_lloyd.backends import use_native_backends

    convert = dict(_native_backends())[backend]
    X = convert(_blobs().astype(np.float32))
    native = KMeans(3, random_state=0).fit(X)
    previous = use_native_backends(False)
    try:
        portable = KMeans(3, random_state=0).fit(X)
    finally:
        use_native_backends(previous)
    np.testing.assert_allclose(
        _to_host(native.cluster_centers_), _to_host(portable.cluster_centers_), rtol=1e-5
    )
    np.testing.assert_array_equal(_to_host(native.labels_), _to_host(portable.labels_))


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
