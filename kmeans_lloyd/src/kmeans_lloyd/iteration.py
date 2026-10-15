"""One Lloyd iteration of k-means, written against the Python array API.

``lloyd_iteration`` is the naive algorithm: broadcast squared Euclidean
distances, ``argmin`` for the assignment, then a mean update. The other
assignment functions are the same math with a different schedule (tiles,
one centroid at a time) or the Gram identity. Those rewrites exist so a
compiler can see a smaller region of distance-plus-argmin work.
"""

from __future__ import annotations

from array_api_compat import array_namespace
from array_api_compat import device as api_device


def _device(array):
    """Array-API device, including NumPy arrays which have no ``.device``."""
    return api_device(array)


def lloyd_iteration(X, centroids, assign="naive", recorder=None, **assign_kwargs):
    """Run one Lloyd iteration.

    Parameters
    ----------
    X : Array
        Samples, shape ``(n_samples, n_features)``.
    centroids : Array
        Current centroids, shape ``(n_clusters, n_features)``.
    assign : {"naive", "gemm", "tiled", "running"}
        Assignment schedule. ``naive`` is the broadcast formulation.
    recorder : optional
        Context-manager factory with a ``phase(name)`` method. Used to
        time the assignment and the centroid update separately.
    assign_kwargs :
        Forwarded to the tiled assignment (``tile_n``, ``tile_k``, ``step``).

    Returns
    -------
    new_centroids : Array
        Shape ``(n_clusters, n_features)``. A cluster that received no
        samples keeps its previous centroid.
    labels : Array
        Shape ``(n_samples,)``. Integer index of the nearest centroid.
        Ties keep the smallest index.
    """
    labels = _assign(X, centroids, assign, recorder=recorder, **assign_kwargs)
    if recorder is None:
        updated = update_centroids(X, labels, centroids)
    else:
        with recorder.phase("update"):
            updated = update_centroids(X, labels, centroids)
    return updated, labels


def assign_naive(X, centroids):
    """Label each sample with the nearest centroid.

    Distances are ``sum((x - c) ** 2)`` materialized by broadcasting
    ``X`` against every centroid, then reduced with ``argmin``.
    """
    xp = array_namespace(X, centroids)
    return broadcast_distance_argmin(xp, X, centroids)


def assign_gemm(X, centroids):
    """Label each sample using the expanded squared-distance identity.

    ``||x - c||^2 = ||x||^2 + ||c||^2 - 2 x·c``. This still ends in
    ``argmin`` over the ``(n_samples, n_clusters)`` distance matrix.
    """
    xp = array_namespace(X, centroids)
    return gemm_distance_argmin(xp, X, centroids)


def assign_tiled(X, centroids, tile_n, tile_k, distance="broadcast", step=None):
    """Naive or Gram distances, evaluated on sample and centroid tiles.

    Each tile returns a local argmin. A running minimum combines tiles.
    Strict ``<`` keeps the smallest index when distances tie, matching
    a single ``argmin`` over the full distance matrix.
    """
    xp = array_namespace(X, centroids)
    if step is None:
        step = tile_broadcast_argmin if distance == "broadcast" else tile_gemm_argmin
    n_samples = int(X.shape[0])
    n_clusters = int(centroids.shape[0])
    labels = xp.zeros(n_samples, dtype=xp.int64, device=_device(X))
    best = xp.full((n_samples,), xp.inf, dtype=X.dtype, device=_device(X))
    for n0 in range(0, n_samples, tile_n):
        n1 = min(n0 + tile_n, n_samples)
        best_tile = best[n0:n1]
        labels_tile = labels[n0:n1]
        x_tile = X[n0:n1]
        for k0 in range(0, n_clusters, tile_k):
            k1 = min(k0 + tile_k, n_clusters)
            local_labels, local_dist = step(xp, x_tile, centroids[k0:k1])
            better = local_dist < best_tile
            best_tile = xp.where(better, local_dist, best_tile)
            labels_tile = xp.where(better, local_labels + k0, labels_tile)
        best[n0:n1] = best_tile
        labels[n0:n1] = labels_tile
    return labels


def assign_running(X, centroids, step=None, return_distance=False):
    """One centroid at a time: squared distance, then a running argmin.

    The per-centroid body is a single reduction over features followed by
    an elementwise update of the best distance and index. That is the
    shape ``cupy.fuse`` can actually compile; ``argmin`` itself is not a
    fusion-aware CuPy routine. ``torch.compile`` can fuse the whole Python
    loop when the cluster count is modest, so callers tile ``centroids``.
    """
    xp = array_namespace(X, centroids)
    if step is None:
        step = running_argmin_step
    n_samples = X.shape[0]
    best_dist = xp.full((n_samples,), xp.inf, dtype=X.dtype, device=_device(X))
    best_idx = xp.zeros(n_samples, dtype=xp.int64, device=_device(X))
    n_clusters = int(centroids.shape[0])
    for j in range(n_clusters):
        index = xp.asarray(j, dtype=best_idx.dtype, device=_device(X))
        best_dist, best_idx = step(xp, X, centroids[j], best_dist, best_idx, index)
    if return_distance:
        return best_idx, best_dist
    return best_idx


def running_tile_distances(X, centroids):
    """Running assignment for one centroid tile, including distances.

    Returning both lets a tiled driver keep the global argmin. This is the
    function ``torch.compile`` is asked to turn into a single kernel.
    """
    return assign_running(X, centroids, return_distance=True)


def assign_running_tiled(X, centroids, tile_k, block=None):
    """Running argmin over centroid tiles of ``tile_k`` columns.

    ``block(X, centroid_tile)`` returns ``(local_labels, local_distances)``.
    """
    xp = array_namespace(X, centroids)
    if block is None:
        block = running_tile_distances
    n_samples = int(X.shape[0])
    n_clusters = int(centroids.shape[0])
    labels = xp.zeros(n_samples, dtype=xp.int64, device=_device(X))
    best = xp.full((n_samples,), xp.inf, dtype=X.dtype, device=_device(X))
    for k0 in range(0, n_clusters, tile_k):
        k1 = min(k0 + tile_k, n_clusters)
        local_labels, local_dist = block(X, centroids[k0:k1])
        better = local_dist < best
        best = xp.where(better, local_dist, best)
        labels = xp.where(better, local_labels + k0, labels)
    return labels


def update_centroids(X, labels, centroids):
    """Replace each centroid by the mean of the samples assigned to it."""
    xp = array_namespace(X, labels, centroids)
    n_clusters = centroids.shape[0]
    cluster_ids = xp.arange(n_clusters, dtype=labels.dtype, device=_device(X))
    membership = xp.astype(labels[:, None] == cluster_ids[None, :], X.dtype)
    counts = xp.sum(membership, axis=0)
    sums = xp.matmul(xp.matrix_transpose(membership), X)
    counts_safe = xp.where(counts == 0, xp.ones_like(counts), counts)
    updated = sums / counts_safe[:, None]
    empty = counts[:, None] == 0
    return xp.where(empty, centroids, updated)


def squared_distances_broadcast(xp, X, centroids):
    """Pairwise squared Euclidean distances, shape ``(n_samples, n_clusters)``."""
    diff = X[:, None, :] - centroids[None, :, :]
    return xp.sum(diff * diff, axis=-1)


def squared_distances_gemm(xp, X, centroids):
    """Pairwise squared distances from the Gram identity."""
    x_norm = xp.sum(X * X, axis=1, keepdims=True)
    c_norm = xp.sum(centroids * centroids, axis=1, keepdims=True)
    dots = xp.matmul(X, xp.matrix_transpose(centroids))
    return x_norm + xp.matrix_transpose(c_norm) - 2 * dots


def broadcast_distance_argmin(xp, X, centroids):
    """Fuse candidate: broadcast squared distance and argmin, one function."""
    distances = squared_distances_broadcast(xp, X, centroids)
    return xp.argmin(distances, axis=1)


def gemm_distance_argmin(xp, X, centroids):
    """Fuse candidate: Gram distances and argmin, one function."""
    distances = squared_distances_gemm(xp, X, centroids)
    return xp.argmin(distances, axis=1)


def tile_broadcast_argmin(xp, X, centroids):
    """Broadcast distance, argmin, and the winning distance for one tile."""
    distances = squared_distances_broadcast(xp, X, centroids)
    return xp.argmin(distances, axis=1), xp.min(distances, axis=1)


def tile_gemm_argmin(xp, X, centroids):
    """Gram distance, argmin, and the winning distance for one tile."""
    distances = squared_distances_gemm(xp, X, centroids)
    return xp.argmin(distances, axis=1), xp.min(distances, axis=1)


def centroid_squared_distance(xp, X, centroid):
    """Squared distance from every sample to one centroid.

    ``centroid`` has shape ``(n_features,)`` and broadcasts against ``X``.
    No indexing, so this body is a legal ``cupy.fuse`` reduction candidate.
    """
    diff = X - centroid
    return xp.sum(diff * diff, axis=-1)


def running_argmin_step(xp, X, centroid, best_dist, best_idx, index):
    """Distance to one centroid and an update of the running argmin.

    ``centroid`` has shape ``(n_features,)`` and broadcasts against ``X``.
    ``index`` is a 0-d integer array so the update does not build a new
    vector inside the fused region.
    """
    diff = X - centroid
    dist = xp.sum(diff * diff, axis=-1)
    better = dist < best_dist
    return xp.where(better, dist, best_dist), xp.where(better, index, best_idx)


def broadcast_distance_only(xp, X, centroids):
    """Squared distances with no argmin. Positive control for distance fusion."""
    return squared_distances_broadcast(xp, X, centroids)


def _assign(X, centroids, assign, recorder=None, **assign_kwargs):
    functions = {
        "naive": assign_naive,
        "gemm": assign_gemm,
        "tiled": assign_tiled,
        "running": assign_running,
    }
    try:
        function = functions[assign]
    except KeyError as exc:
        known = ", ".join(sorted(functions))
        raise ValueError(f"unknown assign={assign!r}; expected one of {known}") from exc
    if recorder is None:
        return function(X, centroids, **assign_kwargs)
    with recorder.phase("assign"):
        return function(X, centroids, **assign_kwargs)
