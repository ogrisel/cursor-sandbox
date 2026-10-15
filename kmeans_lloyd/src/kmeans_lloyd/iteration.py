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


def gemm_scores_argmin(xp, X, centroids, c_norm):
    """Argmin of ``||c||^2 - 2 x·c`` for one centroid tile.

    ``||x||^2`` does not depend on the centroid, so it cannot change the
    nearest-centroid index. Dropping it matches the dense Lloyd kernel in
    scikit-learn and avoids a reduction over the sample tile. ``c_norm``
    has shape ``(n_clusters,)`` and is the squared norm of each row of
    ``centroids``. Ties keep the smallest index.
    """
    scores = c_norm[None, :] - 2 * xp.matmul(X, xp.matrix_transpose(centroids))
    return xp.argmin(scores, axis=1), xp.min(scores, axis=1)


def assign_gemm_tiled(X, centroids, tile_n, tile_k, step=None):
    """Gram assignment over sample tiles and centroid tiles.

    Each tile is one matrix product of shape ``(tile_n, n_features)`` by
    ``(n_features, tile_k)`` plus an argmin. A running minimum combines
    tiles. Strict ``<`` keeps the smallest index on ties. ``step``, when
    given, replaces ``gemm_scores_argmin`` and is the function a caller
    may wrap with ``torch.compile``. It is called as
    ``step(X_tile, centroid_tile, centroid_squared_norm)``.
    """
    xp = array_namespace(X, centroids)
    if step is None:
        step = lambda x_tile, c_tile, c_norm: gemm_scores_argmin(xp, x_tile, c_tile, c_norm)
    n_samples = int(X.shape[0])
    n_clusters = int(centroids.shape[0])
    labels = xp.zeros(n_samples, dtype=xp.int64, device=_device(X))
    tiles = []
    for k0 in range(0, n_clusters, tile_k):
        k1 = min(k0 + tile_k, n_clusters)
        c_tile = centroids[k0:k1]
        tiles.append((k0, c_tile, xp.sum(c_tile * c_tile, axis=1)))
    for n0 in range(0, n_samples, tile_n):
        n1 = min(n0 + tile_n, n_samples)
        x_tile = X[n0:n1]
        best = xp.full((n1 - n0,), xp.inf, dtype=X.dtype, device=_device(X))
        local = xp.zeros(n1 - n0, dtype=xp.int64, device=_device(X))
        for k0, c_tile, c_norm in tiles:
            tile_labels, tile_scores = step(x_tile, c_tile, c_norm)
            better = tile_scores < best
            best = xp.where(better, tile_scores, best)
            local = xp.where(better, tile_labels + k0, local)
        labels[n0:n1] = local
    return labels


def update_centroids_tiled(X, labels, centroids, tile_k, tile_n=None):
    """Mean update one centroid tile at a time.

    The one-hot membership for a tile has shape ``(n_samples, tile_k)``
    instead of ``(n_samples, n_clusters)``. ``tile_n`` also splits the
    samples, so that membership has shape ``(tile_n, tile_k)`` and the
    sums are accumulated. An empty cluster keeps its previous centroid.
    """
    xp = array_namespace(X, labels, centroids)
    n_samples = int(X.shape[0])
    n_clusters = int(centroids.shape[0])
    n_features = int(X.shape[1])
    if tile_n is None:
        tile_n = n_samples
    updated = xp.empty_like(centroids)
    for k0 in range(0, n_clusters, tile_k):
        k1 = min(k0 + tile_k, n_clusters)
        ids = xp.arange(k1 - k0, dtype=labels.dtype, device=_device(X)) + k0
        width = k1 - k0
        if tile_n >= n_samples:
            membership = xp.astype(labels[:, None] == ids[None, :], X.dtype)
            counts = xp.sum(membership, axis=0)
            sums = xp.matmul(xp.matrix_transpose(membership), X)
        else:
            counts = xp.zeros(width, dtype=X.dtype, device=_device(X))
            sums = xp.zeros((width, n_features), dtype=X.dtype, device=_device(X))
            for n0 in range(0, n_samples, tile_n):
                n1 = min(n0 + tile_n, n_samples)
                membership = xp.astype(labels[n0:n1, None] == ids[None, :], X.dtype)
                counts = counts + xp.sum(membership, axis=0)
                sums = sums + xp.matmul(xp.matrix_transpose(membership), X[n0:n1])
        counts_safe = xp.where(counts == 0, xp.ones_like(counts), counts)
        means = sums / counts_safe[:, None]
        empty = counts[:, None] == 0
        updated[k0:k1] = xp.where(empty, centroids[k0:k1], means)
    return updated


def lloyd_step(
    X,
    centroids,
    tile_n,
    tile_k,
    update_tile_k=None,
    update_tile_n=None,
    step=None,
    recorder=None,
):
    """One Lloyd iteration with a tiled Gram assignment and a tiled update.

    ``tile_n`` and ``tile_k`` select the assignment tiles. The update uses
    ``update_tile_k`` centroid columns of the one-hot at a time, defaulting
    to ``tile_k``. ``update_tile_n`` splits the sample axis of that one-hot.
    The default keeps every sample in one membership matrix.
    """
    if update_tile_k is None:
        update_tile_k = tile_k
    if recorder is None:
        labels = assign_gemm_tiled(X, centroids, tile_n, tile_k, step=step)
        updated = update_centroids_tiled(X, labels, centroids, update_tile_k, tile_n=update_tile_n)
    else:
        with recorder.phase("assign"):
            labels = assign_gemm_tiled(X, centroids, tile_n, tile_k, step=step)
        with recorder.phase("update"):
            updated = update_centroids_tiled(X, labels, centroids, update_tile_k, tile_n=update_tile_n)
    return updated, labels


def running_tile_update(X, centroids, best_dist, best_idx, offset):
    """Running argmin for one centroid tile, merged into the caller state.

    ``offset`` is a 0-d integer array holding the first centroid index of
    this tile. Passing it as an array keeps a compiled caller from
    specializing on each tile's Python index.
    """
    xp = array_namespace(X, centroids, best_dist, best_idx, offset)
    local_idx, local_dist = assign_running(X, centroids, return_distance=True)
    better = local_dist < best_dist
    return xp.where(better, local_dist, best_dist), xp.where(better, local_idx + offset, best_idx)


def assign_running_stateful(X, centroids, tile_k, block=None):
    """Running assignment whose compiled block also merges the running state.

    ``block(X, centroid_tile, best_dist, best_idx, offset)`` returns the
    updated distance and index. Without ``block`` this is the same labels
    as ``assign_running_tiled``.
    """
    xp = array_namespace(X, centroids)
    if block is None:
        block = running_tile_update
    n_samples = int(X.shape[0])
    n_clusters = int(centroids.shape[0])
    labels = xp.zeros(n_samples, dtype=xp.int64, device=_device(X))
    best = xp.full((n_samples,), xp.inf, dtype=X.dtype, device=_device(X))
    for k0 in range(0, n_clusters, tile_k):
        k1 = min(k0 + tile_k, n_clusters)
        offset = xp.asarray(k0, dtype=labels.dtype, device=_device(X))
        best, labels = block(X, centroids[k0:k1], best, labels, offset)
    return labels


def kmeans_plusplus(X, n_clusters, rng, n_local_trials=None, distance=None):
    """k-means++ initialization in the array API.

    The first center is a uniform draw from ``rng`` (a
    ``numpy.random.Generator``). Each later center draws
    ``n_local_trials`` candidates with probability proportional to the
    squared distance to the nearest center chosen so far, and keeps the
    candidate that most reduces the sum of those distances. The default
    trial count is ``2 + log(n_clusters)``, the same rule as scikit-learn.

    Returns ``(centers, indices)``. ``centers[j]`` is the row ``X[indices[j]]``.
    """
    import math

    xp = array_namespace(X)
    n_samples = int(X.shape[0])
    n_clusters = int(n_clusters)
    if n_clusters < 1 or n_clusters > n_samples:
        raise ValueError(f"n_clusters must be in 1..n_samples, got {n_clusters} and {n_samples}")
    if n_local_trials is None:
        n_local_trials = 2 + int(math.log(n_clusters))
    n_local_trials = max(1, min(int(n_local_trials), n_samples))
    if distance is None:
        distance = _distances_to_candidates
    chosen = [int(rng.integers(n_samples))]
    # One reduction of X * X. Repeating it inside every trial materializes a
    # full copy of the samples for each new center.
    x_norm = _row_squared_norm(xp, X)
    first = X[chosen[0]]
    closest = x_norm + xp.sum(first * first) - 2 * xp.matmul(X, first)
    closest = xp.maximum(closest, xp.zeros_like(closest))
    for _ in range(1, n_clusters):
        picks = _weighted_draw(xp, closest, rng, n_local_trials)
        candidates = xp.take(X, picks, axis=0)
        distances = distance(xp, X, x_norm, candidates)
        updated = xp.minimum(closest[:, None], distances)
        potentials = xp.sum(updated, axis=0)
        best = int(xp.argmin(potentials))
        closest = updated[:, best]
        chosen.append(int(picks[best]))
    centers = xp.stack([X[index] for index in chosen])
    indices = xp.asarray(chosen, dtype=xp.int64, device=_device(X))
    return centers, indices


def inertia(X, labels, centers, tile_n=8192):
    """Sum of squared distances from each sample to its assigned center.

    Samples are visited in blocks of ``tile_n`` so the difference tensor
    stays at ``(tile_n, n_features)`` rather than a second copy of ``X``.
    """
    xp = array_namespace(X, labels, centers)
    n_samples = int(X.shape[0])
    total = None
    for n0 in range(0, n_samples, tile_n):
        n1 = min(n0 + tile_n, n_samples)
        assigned = xp.take(centers, labels[n0:n1], axis=0)
        diff = X[n0:n1] - assigned
        part = xp.sum(diff * diff)
        total = part if total is None else total + part
    return total


def fit_kmeans(
    X,
    n_clusters,
    rng,
    max_iter=300,
    tol=1e-4,
    tile_n=4096,
    tile_k=1024,
    update_tile_k=256,
    update_tile_n=None,
    step=None,
    distance=None,
):
    """k-means++ initialization followed by Lloyd iterations until convergence.

    ``tol`` is scaled by the mean feature variance, matching scikit-learn.
    ``update_tile_n`` splits the sample axis of the one-hot update. The
    default is ``min(tile_n, 4096)``, which keeps that matrix off the full
    sample count. An empty cluster keeps its center. The returned inertia is the sum of
    squared distances to the centers of the last iteration. ``step`` and
    ``distance`` are optional callables a benchmark may wrap with
    ``torch.compile``; both default to the array-API implementations.
    """
    xp = array_namespace(X)
    if update_tile_n is None:
        update_tile_n = min(int(tile_n), 4096)
    centers, indices = kmeans_plusplus(X, n_clusters, rng, distance=distance)
    # ``mean(var(X, axis=0))`` with the library reduction allocates a large
    # workspace (512 MiB on the timing shape). Feature tiles compute the same
    # scalar, which is the scikit-learn scale for ``tol``.
    variance = _mean_feature_variance(xp, X)
    threshold = float(tol) * _item(variance)
    labels = None
    n_iter = 0
    for n_iter in range(1, int(max_iter) + 1):
        updated, labels = lloyd_step(
            X,
            centers,
            tile_n,
            tile_k,
            update_tile_k=update_tile_k,
            update_tile_n=update_tile_n,
            step=step,
        )
        shift = _item(xp.sum((updated - centers) ** 2))
        centers = updated
        if shift <= threshold:
            break
    value = inertia(X, labels, centers, tile_n=min(tile_n, 4096))
    return {
        "centers": centers,
        "labels": labels,
        "indices": indices,
        "inertia": _item(value),
        "n_iter": n_iter,
        "shift": shift,
        "threshold": threshold,
    }


def _mean_feature_variance(xp, X, tile_d=128):
    """Mean over features of the population variance, one feature tile at a time."""
    n_samples = int(X.shape[0])
    n_features = int(X.shape[1])
    n = xp.asarray(n_samples, dtype=X.dtype, device=_device(X))
    total = xp.asarray(0, dtype=X.dtype, device=_device(X))
    for d0 in range(0, n_features, tile_d):
        block = X[:, d0 : d0 + tile_d]
        mean = xp.mean(block, axis=0)
        centered = block - mean[None, :]
        total = total + xp.sum(centered * centered) / n
    return total / xp.asarray(n_features, dtype=X.dtype, device=_device(X))


def _row_squared_norm(xp, X, tile_d=256):
    """Squared row norm, one feature tile at a time.

    ``sum(X * X, axis=1)`` materializes a tensor the size of ``X``. A
    feature tile keeps that product at ``(n_samples, tile_d)``.
    """
    n_features = int(X.shape[1])
    total = None
    for d0 in range(0, n_features, tile_d):
        block = X[:, d0 : d0 + tile_d]
        part = xp.sum(block * block, axis=1)
        total = part if total is None else total + part
    return total


def _distances_to_candidates(xp, X, x_norm, candidates):
    """Squared distances from every sample to a handful of candidate rows."""
    centroid_norm = xp.sum(candidates * candidates, axis=1)
    dots = xp.matmul(X, xp.matrix_transpose(candidates))
    distances = x_norm[:, None] + centroid_norm[None, :] - 2 * dots
    return xp.maximum(distances, xp.zeros_like(distances))


def _item(array):
    if hasattr(array, "item"):
        return float(array.item())
    return float(array)


def _weighted_draw(xp, weights, rng, n_draws):
    """Draw ``n_draws`` indices with probability proportional to ``weights``."""
    cumulative = xp.cumulative_sum(weights)
    total = _item(cumulative[-1])
    n_samples = int(weights.shape[0])
    if not total > 0:
        return xp.asarray(rng.integers(n_samples, size=n_draws), dtype=xp.int64, device=_device(weights))
    draws = xp.asarray(rng.random(n_draws), dtype=weights.dtype, device=_device(weights)) * cumulative[-1]
    found = xp.searchsorted(cumulative, draws, side="left")
    last = xp.asarray(n_samples - 1, dtype=found.dtype, device=_device(found))
    return xp.minimum(found, last)


def _assign(X, centroids, assign, recorder=None, **assign_kwargs):
    functions = {
        "naive": assign_naive,
        "gemm": assign_gemm,
        "tiled": assign_tiled,
        "running": assign_running,
        "gemm_tiled": assign_gemm_tiled,
        "running_tiled": assign_running_tiled,
        "running_stateful": assign_running_stateful,
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
