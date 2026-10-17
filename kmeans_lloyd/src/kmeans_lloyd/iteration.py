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
        x_tile = X[n0:n1, :]
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
    labels = xp.argmin(scores, axis=1)
    # Gathering the winning score avoids a second reduction over the same
    # tile. This is portable and was consistently faster on PyTorch and CuPy.
    values = xp.take_along_axis(scores, labels[:, None], axis=1)[:, 0]
    return labels, values


def gemm_labels(xp, X, centroids, c_norm):
    """Nearest-center indices when one GEMM contains every centroid."""
    scores = c_norm[None, :] - 2 * xp.matmul(X, xp.matrix_transpose(centroids))
    return xp.argmin(scores, axis=1)


def broadcast_scores_argmin(xp, X, centroids, c_norm=None):
    """Broadcast squared distances and return the winning index and value.

    ``c_norm`` is accepted for compatibility with :func:`assign_gemm_tiled`'s
    step protocol. The caller must choose sample and centroid tiles that keep
    the ``(tile_n, tile_k, n_features)`` difference tensor bounded.
    """
    del c_norm
    distances = squared_distances_broadcast(xp, X, centroids)
    labels = xp.argmin(distances, axis=1)
    values = xp.take_along_axis(distances, labels[:, None], axis=1)[:, 0]
    return labels, values


def stable_gemm_distances(
    xp,
    X,
    x_norm,
    centroids,
    c_norm=None,
    *,
    threshold=None,
    max_pair_bytes=128 * 2**20,
    stats=None,
):
    """GEMM distances with direct recomputation of cancellation-prone pairs.

    The relative test and defaults follow cakedev0/scikit-learn#23: recompute
    when the Gram residual is below ``1e-2 * (||x||² + ||c||²)`` in float32,
    or ``1e-8`` in float64. Selected pairs are gathered and evaluated as
    ``sum((x - c) ** 2)`` in bounded chunks. This helper intentionally uses
    advanced indexed assignment, outside the strict array API, and is an
    experimental PyTorch/CuPy/NumPy path rather than the portable default.
    """
    if c_norm is None:
        c_norm = xp.sum(centroids * centroids, axis=1)
    if threshold is None:
        threshold = 1e-2 if "32" in str(X.dtype) else 1e-8
    norms = x_norm[:, None] + c_norm[None, :]
    distances = norms - 2 * xp.matmul(X, xp.matrix_transpose(centroids))
    suspicious = distances < threshold * norms
    flat = xp.nonzero(xp.reshape(suspicious, (-1,)))[0]
    n_pairs = int(flat.shape[0])
    n_centroids = int(centroids.shape[0])
    n_features = int(X.shape[1])
    itemsize = X.element_size() if hasattr(X, "element_size") else X.itemsize
    pair_tile = max(1, max_pair_bytes // max(1, 2 * itemsize * n_features))
    for p0 in range(0, n_pairs, pair_tile):
        selected = flat[p0 : min(p0 + pair_tile, n_pairs)]
        sample_indices = selected // n_centroids
        center_indices = selected % n_centroids
        rows = xp.take(X, sample_indices, axis=0)
        centers = xp.take(centroids, center_indices, axis=0)
        difference = rows - centers
        exact = xp.sum(difference * difference, axis=1)
        distances[sample_indices, center_indices] = exact
    if stats is not None:
        stats["distance_pairs"] = stats.get("distance_pairs", 0) + int(
            X.shape[0]
        ) * n_centroids
        stats["recomputed_pairs"] = stats.get("recomputed_pairs", 0) + n_pairs
        stats["distance_calls"] = stats.get("distance_calls", 0) + 1
    return distances


def stable_gemm_scores_argmin(
    xp, X, centroids, c_norm, *, threshold=None, stats=None
):
    """Argmin and winning value after stable GEMM distance recomputation."""
    x_norm = xp.sum(X * X, axis=1)
    distances = stable_gemm_distances(
        xp,
        X,
        x_norm,
        centroids,
        c_norm,
        threshold=threshold,
        stats=stats,
    )
    labels = xp.argmin(distances, axis=1)
    values = xp.take_along_axis(distances, labels[:, None], axis=1)[:, 0]
    return labels, values


def assign_gemm_tiled(
    X, centroids, tile_n, tile_k, step=None, label_step=None
):
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
        def step(x_tile, c_tile, c_norm):
            return gemm_scores_argmin(xp, x_tile, c_tile, c_norm)

        if label_step is None:
            def label_step(x_tile, c_tile, c_norm):
                return gemm_labels(xp, x_tile, c_tile, c_norm)
    n_samples = int(X.shape[0])
    n_clusters = int(centroids.shape[0])
    labels = xp.zeros(n_samples, dtype=xp.int64, device=_device(X))
    tiles = []
    for k0 in range(0, n_clusters, tile_k):
        k1 = min(k0 + tile_k, n_clusters)
        c_tile = centroids[k0:k1, :]
        tiles.append((k0, c_tile, xp.sum(c_tile * c_tile, axis=1)))
    if label_step is not None and len(tiles) == 1:
        _, c_tile, c_norm = tiles[0]
        for n0 in range(0, n_samples, tile_n):
            n1 = min(n0 + tile_n, n_samples)
            labels[n0:n1] = label_step(X[n0:n1, :], c_tile, c_norm)
        return labels
    for n0 in range(0, n_samples, tile_n):
        n1 = min(n0 + tile_n, n_samples)
        x_tile = X[n0:n1, :]
        best = xp.full((n1 - n0,), xp.inf, dtype=X.dtype, device=_device(X))
        local = xp.zeros(n1 - n0, dtype=xp.int64, device=_device(X))
        for k0, c_tile, c_norm in tiles:
            tile_labels, tile_scores = step(x_tile, c_tile, c_norm)
            better = tile_scores < best
            best = xp.where(better, tile_scores, best)
            local = xp.where(better, tile_labels + k0, local)
        labels[n0:n1] = local
    return labels


def augment_for_gemm_scores(xp, X):
    """Append a ones column so center norms can be folded into GEMM."""
    ones = xp.ones(
        (int(X.shape[0]), 1),
        dtype=X.dtype,
        device=_device(X),
    )
    return xp.concat((X, ones), axis=1)


def assign_homogeneous_tiled(X_augmented, centroids, tile_n, tile_k):
    """Assign with ``[-2 C, ||C||²]`` folded into one augmented GEMM.

    ``X_augmented`` is :func:`augment_for_gemm_scores` applied once to the
    samples and can be reused across Lloyd iterations. This removes the
    elementwise multiply and center-norm addition after every matrix product
    while remaining expressible with portable array API operations.

    Columns after the ones column, such as row norms kept for k-means++, get
    zero coefficients. Column-slicing them away instead makes the matrix
    operand non-contiguous, which CuPy copies before every product.
    """
    xp = array_namespace(X_augmented, centroids)
    n_samples = int(X_augmented.shape[0])
    n_clusters = int(centroids.shape[0])
    n_extra = int(X_augmented.shape[1]) - int(centroids.shape[1]) - 1
    labels = xp.zeros(n_samples, dtype=xp.int64, device=_device(X_augmented))
    tiles = []
    for k0 in range(0, n_clusters, tile_k):
        k1 = min(k0 + tile_k, n_clusters)
        c_tile = centroids[k0:k1, :]
        c_norm = xp.sum(c_tile * c_tile, axis=1)
        parts = [-2 * c_tile, c_norm[:, None]]
        if n_extra:
            parts.append(
                xp.zeros(
                    (k1 - k0, n_extra),
                    dtype=c_tile.dtype,
                    device=_device(c_tile),
                )
            )
        tiles.append((k0, xp.concat(parts, axis=1)))
    for n0 in range(0, n_samples, tile_n):
        n1 = min(n0 + tile_n, n_samples)
        scores = xp.matmul(
            X_augmented[n0:n1, :],
            xp.matrix_transpose(tiles[0][1]),
        )
        local = xp.argmin(scores, axis=1)
        if len(tiles) == 1:
            labels[n0:n1] = local
            continue
        best = xp.take_along_axis(scores, local[:, None], axis=1)[:, 0]
        for k0, transformed in tiles[1:]:
            scores = xp.matmul(
                X_augmented[n0:n1, :],
                xp.matrix_transpose(transformed),
            )
            tile_labels = xp.argmin(scores, axis=1)
            tile_scores = xp.take_along_axis(
                scores, tile_labels[:, None], axis=1
            )[:, 0]
            better = tile_scores < best
            best = xp.where(better, tile_scores, best)
            local = xp.where(better, tile_labels + k0, local)
        labels[n0:n1] = local
    return labels


def update_centroids_tiled(
    X,
    labels,
    centroids,
    tile_k,
    tile_n=None,
    reassign_empty=False,
    rng=None,
    stats=None,
    accumulate=None,
):
    """Mean update one centroid tile at a time.

    The one-hot membership for a tile has shape ``(n_samples, tile_k)``
    instead of ``(n_samples, n_clusters)``. ``tile_n`` also splits the
    samples, so that membership has shape ``(tile_n, tile_k)`` and the sums
    are accumulated.

    ``accumulate(X, labels, n_clusters)``, when given, replaces the one-hot
    tiles. It returns per-cluster feature sums of shape
    ``(n_clusters, n_features)`` and counts of shape ``(n_clusters,)``, both
    in ``X.dtype``. The array API has no keyed reduction, so this is where a
    backend scatter-add can be injected; see :mod:`kmeans_lloyd.backends`.

    By default, an empty cluster keeps its previous centroid. With
    ``reassign_empty=True``, the samples farthest from their assigned centers
    are moved to the empty centers. The selected samples are removed from
    their donor sums and counts. This is the unweighted dense relocation
    policy used by scikit-learn's Lloyd implementation.
    """
    xp = array_namespace(X, labels, centroids)
    n_samples = int(X.shape[0])
    n_clusters = int(centroids.shape[0])
    n_features = int(X.shape[1])
    if tile_n is None:
        tile_n = n_samples
    if accumulate is not None:
        sums, all_counts = accumulate(X, labels, n_clusters)
        counts_safe = xp.where(all_counts == 0, xp.ones_like(all_counts), all_counts)
        updated = xp.where(
            all_counts[:, None] == 0, centroids, sums / counts_safe[:, None]
        )
        return _relocate_empty(
            xp, X, labels, centroids, updated, all_counts, reassign_empty, tile_n, stats
        )
    updated = xp.empty_like(centroids)
    all_counts = xp.empty(n_clusters, dtype=X.dtype, device=_device(X))
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
                sums = sums + xp.matmul(
                    xp.matrix_transpose(membership), X[n0:n1, :]
                )
        counts_safe = xp.where(counts == 0, xp.ones_like(counts), counts)
        means = sums / counts_safe[:, None]
        empty = counts[:, None] == 0
        updated[k0:k1, :] = xp.where(empty, centroids[k0:k1, :], means)
        all_counts[k0:k1] = counts
    return _relocate_empty(
        xp, X, labels, centroids, updated, all_counts, reassign_empty, tile_n, stats
    )


def _relocate_empty(xp, X, labels, centroids, updated, all_counts, reassign_empty, tile_n, stats):
    """Count empty clusters and optionally apply farthest-point relocation."""
    n_empty = int(_item(xp.sum(xp.astype(all_counts == 0, xp.int64))))
    if stats is not None:
        stats["empty_events"] = stats.get("empty_events", 0) + n_empty
    if reassign_empty and n_empty:
        updated, n_reassigned = _reassign_empty_farthest(
            xp,
            X,
            labels,
            centroids,
            updated,
            all_counts,
            tile_n=min(int(tile_n), 8192),
        )
        if stats is not None:
            stats["reassignments"] = stats.get("reassignments", 0) + n_reassigned
    return updated


def _reassign_empty_farthest(xp, X, labels, old_centers, updated, counts, tile_n):
    """Relocate empty centers with scikit-learn's farthest-point policy."""
    empty_indices = xp.nonzero(counts == 0)[0]
    n_empty = int(empty_indices.shape[0])
    if n_empty == 0:
        return updated, 0
    distances = _assigned_squared_distances(xp, X, labels, old_centers, tile_n)
    if _item(xp.max(distances)) == 0:
        return updated, 0
    farthest = xp.argsort(distances, descending=True)[:n_empty]
    for index in range(n_empty):
        picked = int(farthest[index])
        donor = int(labels[picked])
        donor_count = counts[donor]
        donor_sum = updated[donor, :] * donor_count
        updated[donor, :] = (donor_sum - X[picked, :]) / (donor_count - 1)
        counts[donor] = donor_count - 1
        empty = int(empty_indices[index])
        updated[empty, :] = X[picked, :]
        counts[empty] = xp.asarray(1, dtype=counts.dtype, device=_device(counts))
    return updated, n_empty


def _assigned_squared_distances(xp, X, labels, centers, tile_n):
    """Squared distance to the assigned old center, in sample tiles."""
    distances = xp.empty((int(X.shape[0]),), dtype=X.dtype, device=_device(X))
    for n0 in range(0, int(X.shape[0]), tile_n):
        n1 = min(n0 + tile_n, int(X.shape[0]))
        assigned = xp.take(centers, labels[n0:n1], axis=0)
        difference = X[n0:n1, :] - assigned
        distances[n0:n1] = xp.sum(difference * difference, axis=1)
    return distances


def lloyd_step(
    X,
    centroids,
    tile_n,
    tile_k,
    update_tile_k=None,
    update_tile_n=None,
    reassign_empty=False,
    rng=None,
    stats=None,
    step=None,
    label_step=None,
    assigner=None,
    recorder=None,
    accumulate=None,
):
    """One Lloyd iteration with a tiled Gram assignment and a tiled update.

    ``tile_n`` and ``tile_k`` select the assignment tiles. The update uses
    ``update_tile_k`` centroid columns of the one-hot at a time, defaulting
    to ``tile_k``. ``update_tile_n`` splits the sample axis of that one-hot.
    The default keeps every sample in one membership matrix. ``accumulate``
    replaces the one-hot update, as described in
    :func:`update_centroids_tiled`.
    """
    if update_tile_k is None:
        update_tile_k = tile_k

    def update(labels):
        return update_centroids_tiled(
            X,
            labels,
            centroids,
            update_tile_k,
            tile_n=update_tile_n,
            reassign_empty=reassign_empty,
            rng=rng,
            stats=stats,
            accumulate=accumulate,
        )

    def assign():
        if assigner is not None:
            return assigner(centroids, tile_n, tile_k)
        return assign_gemm_tiled(
            X, centroids, tile_n, tile_k, step=step, label_step=label_step
        )

    if recorder is None:
        labels = assign()
        updated = update(labels)
    else:
        with recorder.phase("assign"):
            labels = assign()
        with recorder.phase("update"):
            updated = update(labels)
    return updated, labels


def lloyd_step_interleaved(
    X,
    centroids,
    tile_n,
    tile_k,
    update_tile_k=None,
    update_tile_n=None,
    reassign_empty=False,
    rng=None,
    stats=None,
    step=None,
    label_step=None,
    assigner=None,
    recorder=None,
    accumulate=None,
):
    """Assign and accumulate one sample tile at a time.

    Interleaving keeps each sample tile hot between its GEMM assignment and
    centroid accumulation. It also provides a backend-agnostic fusion point:
    ``step`` can compile the distance/top-1 operation and ``accumulate`` can
    provide a keyed reduction. Without those callables, all operations remain
    portable array API operations.
    """
    del rng, update_tile_n
    if assigner is not None:
        raise ValueError(
            "lloyd_step_interleaved cannot use a whole-array assigner"
        )
    xp = array_namespace(X, centroids)
    n_samples = int(X.shape[0])
    n_clusters = int(centroids.shape[0])
    if update_tile_k is None:
        update_tile_k = tile_k
    if step is None:
        def step(x_tile, c_tile, c_norm):
            return gemm_scores_argmin(xp, x_tile, c_tile, c_norm)

        if label_step is None:
            def label_step(x_tile, c_tile, c_norm):
                return gemm_labels(xp, x_tile, c_tile, c_norm)
    center_tiles = []
    for k0 in range(0, n_clusters, tile_k):
        k1 = min(k0 + tile_k, n_clusters)
        c_tile = centroids[k0:k1, :]
        center_tiles.append((k0, c_tile, xp.sum(c_tile * c_tile, axis=1)))

    labels = xp.empty(n_samples, dtype=xp.int64, device=_device(X))
    sums = xp.zeros_like(centroids)
    counts = xp.zeros(n_clusters, dtype=X.dtype, device=_device(X))

    def assign_and_accumulate():
        for n0 in range(0, n_samples, tile_n):
            n1 = min(n0 + tile_n, n_samples)
            x_tile = X[n0:n1, :]
            if label_step is not None and len(center_tiles) == 1:
                _, c_tile, c_norm = center_tiles[0]
                local = label_step(x_tile, c_tile, c_norm)
            else:
                best = xp.full(
                    (n1 - n0,), xp.inf, dtype=X.dtype, device=_device(X)
                )
                local = xp.zeros(
                    n1 - n0, dtype=xp.int64, device=_device(X)
                )
                for k0, c_tile, c_norm in center_tiles:
                    tile_labels, tile_scores = step(
                        x_tile, c_tile, c_norm
                    )
                    better = tile_scores < best
                    best = xp.where(better, tile_scores, best)
                    local = xp.where(better, tile_labels + k0, local)
            labels[n0:n1] = local
            if accumulate is not None:
                part_sums, part_counts = accumulate(x_tile, local, n_clusters)
                sums[:] = sums + part_sums
                counts[:] = counts + part_counts
                continue
            for k0 in range(0, n_clusters, update_tile_k):
                k1 = min(k0 + update_tile_k, n_clusters)
                ids = (
                    xp.arange(
                        k1 - k0,
                        dtype=labels.dtype,
                        device=_device(labels),
                    )
                    + k0
                )
                membership = xp.astype(local[:, None] == ids[None, :], X.dtype)
                counts[k0:k1] = counts[k0:k1] + xp.sum(membership, axis=0)
                sums[k0:k1, :] = sums[k0:k1, :] + xp.matmul(
                    xp.matrix_transpose(membership), x_tile
                )

    if recorder is None:
        assign_and_accumulate()
    else:
        with recorder.phase("assign-update"):
            assign_and_accumulate()

    counts_safe = xp.where(counts == 0, xp.ones_like(counts), counts)
    updated = xp.where(
        counts[:, None] == 0,
        centroids,
        sums / counts_safe[:, None],
    )
    return (
        _relocate_empty(
            xp,
            X,
            labels,
            centroids,
            updated,
            counts,
            reassign_empty,
            tile_n,
            stats,
        ),
        labels,
    )


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


def kmeans_plusplus(
    X,
    n_clusters,
    rng,
    n_local_trials=None,
    distance=None,
    draw=None,
    x_norm=None,
):
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
    custom_distance = distance is not None
    if distance is None:
        distance = _distances_to_candidates
    if draw is None:
        draw = _weighted_draw
    chosen = [int(rng.integers(n_samples))]
    # One reduction of X * X. Repeating it inside every trial materializes a
    # full copy of the samples for each new center.
    if x_norm is None:
        x_norm = _row_squared_norm(xp, X)
    first_index = xp.asarray([chosen[0]], dtype=xp.int64, device=_device(X))
    first = xp.take(X, first_index, axis=0)
    if custom_distance:
        closest = distance(xp, X, x_norm, first)[:, 0]
    else:
        first_row = first[0, :]
        closest = x_norm + xp.sum(first_row * first_row) - 2 * xp.matmul(
            X, first_row
        )
        closest = xp.maximum(closest, xp.zeros_like(closest))
    for _ in range(1, n_clusters):
        picks = draw(xp, closest, rng, n_local_trials)
        candidates = xp.take(X, picks, axis=0)
        distances = distance(xp, X, x_norm, candidates)
        updated = xp.minimum(closest[:, None], distances)
        potentials = xp.sum(updated, axis=0)
        best = int(xp.argmin(potentials))
        closest = updated[:, best]
        chosen.append(int(picks[best]))
    indices = xp.asarray(chosen, dtype=xp.int64, device=_device(X))
    return xp.take(X, indices, axis=0), indices


def scalable_kmeans_plusplus(
    X,
    n_clusters,
    rng,
    oversampling_factor=2.0,
    n_rounds=8,
    n_local_trials=None,
    tile_n=8192,
    tile_k=256,
):
    """Initialize centers with an array-API k-means|| strategy.

    One uniform center is followed by ``n_rounds`` parallel D² sampling
    rounds. Each round draws ``ceil(oversampling_factor * n_clusters)``
    candidate rows. The candidate pool is weighted by the number of input
    rows nearest to each candidate, then reduced to ``n_clusters`` centers
    with weighted greedy k-means++.

    The defaults follow cuML's documented scalable initializer budget of
    ``oversampling_factor * n_clusters * 8`` sampled candidates. Sampling a
    fixed-size D² batch per round is close to k-means||'s independent
    Bernoulli sampling while bounding memory deterministically.

    Returns ``(centers, indices)`` where every center is a row of ``X``.
    """
    xp = array_namespace(X)
    n_samples = int(X.shape[0])
    n_clusters = int(n_clusters)
    n_rounds = int(n_rounds)
    oversampling_factor = float(oversampling_factor)
    if n_clusters < 1 or n_clusters > n_samples:
        raise ValueError(f"n_clusters must be in 1..n_samples, got {n_clusters} and {n_samples}")
    if oversampling_factor <= 0:
        raise ValueError("oversampling_factor must be positive")
    if n_rounds < 1:
        raise ValueError("n_rounds must be at least 1")

    candidate_indices, candidates, weights = _scalable_candidates(
        xp, X, n_clusters, rng, oversampling_factor, n_rounds, tile_n, tile_k
    )
    selected = _weighted_kmeans_plusplus(
        xp,
        candidates,
        weights,
        rng,
        n_clusters,
        n_local_trials=n_local_trials,
    )
    indices = xp.take(candidate_indices, selected, axis=0)
    return xp.take(X, indices, axis=0), indices


def _scalable_candidates(xp, X, n_clusters, rng, oversampling_factor, n_rounds, tile_n, tile_k):
    """Return k-means|| candidate indices, rows, and nearest-sample counts."""
    import math

    n_samples = int(X.shape[0])
    first = int(rng.integers(n_samples))
    candidate_indices = [xp.asarray([first], dtype=xp.int64, device=_device(X))]
    x_norm = _row_squared_norm(xp, X)
    closest = _minimum_squared_distances(
        xp,
        X,
        x_norm,
        X[first : first + 1],
        tile_n=tile_n,
        tile_k=tile_k,
    )
    draws_per_round = max(1, math.ceil(oversampling_factor * n_clusters))
    for _ in range(n_rounds):
        if not _item(xp.sum(closest)) > 0:
            break
        picks = xp.unique_values(_weighted_draw(xp, closest, rng, draws_per_round))
        candidate_indices.append(picks)
        new_centers = xp.take(X, picks, axis=0)
        new_distances = _minimum_squared_distances(
            xp,
            X,
            x_norm,
            new_centers,
            tile_n=tile_n,
            tile_k=tile_k,
        )
        closest = xp.minimum(closest, new_distances)

    # Guarantee that the weighted reduction has at least k candidate rows.
    uniform = xp.asarray(
        rng.choice(n_samples, size=n_clusters, replace=False),
        dtype=xp.int64,
        device=_device(X),
    )
    candidate_indices.append(uniform)
    candidate_indices = xp.unique_values(xp.concat(candidate_indices))
    candidates = xp.take(X, candidate_indices, axis=0)

    labels = assign_gemm_tiled(
        X,
        candidates,
        tile_n=min(int(tile_n), n_samples),
        tile_k=min(int(tile_k), int(candidates.shape[0])),
    )
    weights = _label_counts(xp, labels, int(candidates.shape[0]), X.dtype)
    return candidate_indices, candidates, weights


def _minimum_squared_distances(xp, X, x_norm, candidates, tile_n, tile_k):
    """Distance to the nearest candidate with bounded sample/candidate tiles."""
    n_samples = int(X.shape[0])
    n_candidates = int(candidates.shape[0])
    closest = xp.empty((n_samples,), dtype=X.dtype, device=_device(X))
    for n0 in range(0, n_samples, tile_n):
        n1 = min(n0 + tile_n, n_samples)
        best = xp.full((n1 - n0,), xp.inf, dtype=X.dtype, device=_device(X))
        for k0 in range(0, n_candidates, tile_k):
            k1 = min(k0 + tile_k, n_candidates)
            distances = _distances_to_candidates(
                xp,
                X[n0:n1],
                x_norm[n0:n1],
                candidates[k0:k1],
            )
            best = xp.minimum(best, xp.min(distances, axis=1))
        closest[n0:n1] = best
    return closest


def _label_counts(xp, labels, n_labels, dtype):
    """Count sorted integer labels without a backend-specific bincount."""
    observed = xp.unique_counts(labels)
    ids = xp.arange(n_labels, dtype=labels.dtype, device=_device(labels))
    positions = xp.searchsorted(observed.values, ids)
    last = xp.asarray(int(observed.values.shape[0]) - 1, dtype=positions.dtype, device=_device(labels))
    safe = xp.minimum(positions, last)
    found = xp.take(observed.values, safe, axis=0) == ids
    counts = xp.take(observed.counts, safe, axis=0)
    return xp.astype(xp.where(found, counts, xp.zeros_like(counts)), dtype)


def _weighted_kmeans_plusplus(
    xp,
    candidates,
    weights,
    rng,
    n_clusters,
    n_local_trials=None,
):
    """Reduce weighted k-means|| candidates with greedy k-means++."""
    import math

    if n_local_trials is None:
        n_local_trials = 2 + int(math.log(n_clusters))
    n_local_trials = max(1, min(int(n_local_trials), int(candidates.shape[0])))
    chosen = [int(_weighted_draw(xp, weights, rng, 1)[0])]
    norms = _row_squared_norm(xp, candidates)
    first = candidates[chosen[0]]
    closest = norms + xp.sum(first * first) - 2 * xp.matmul(candidates, first)
    closest = xp.maximum(closest, xp.zeros_like(closest))
    for _ in range(1, n_clusters):
        picks = _weighted_draw(xp, weights * closest, rng, n_local_trials)
        trial_centers = xp.take(candidates, picks, axis=0)
        distances = _distances_to_candidates(xp, candidates, norms, trial_centers)
        updated = xp.minimum(closest[:, None], distances)
        potentials = xp.sum(updated * weights[:, None], axis=0)
        best = int(xp.argmin(potentials))
        closest = updated[:, best]
        chosen.append(int(picks[best]))
    return xp.asarray(chosen, dtype=xp.int64, device=_device(candidates))


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
        diff = X[n0:n1, :] - assigned
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
    reassign_empty=False,
    step=None,
    label_step=None,
    assigner=None,
    distance=None,
    draw=None,
    iteration=None,
    x_norm=None,
    variance=None,
):
    """k-means++ initialization followed by Lloyd iterations until convergence.

    ``tol`` is scaled by the mean feature variance, matching scikit-learn.
    ``update_tile_n`` splits the sample axis of the one-hot update. The
    default is ``min(tile_n, 4096)``, which keeps that matrix off the full
    sample count. An empty cluster keeps its center unless
    ``reassign_empty=True``. The returned inertia is the sum of squared
    distances to the centers of the last iteration. ``step`` and ``distance``
    are optional callables a benchmark may wrap with ``torch.compile``; both
    default to the array-API implementations.
    """
    centers, indices = kmeans_plusplus(
        X,
        n_clusters,
        rng,
        distance=distance,
        draw=draw,
        x_norm=x_norm,
    )
    result = fit_lloyd(
        X,
        centers,
        max_iter=max_iter,
        tol=tol,
        tile_n=tile_n,
        tile_k=tile_k,
        update_tile_k=update_tile_k,
        update_tile_n=update_tile_n,
        reassign_empty=reassign_empty,
        rng=rng,
        step=step,
        label_step=label_step,
        assigner=assigner,
        iteration=iteration,
        variance=variance,
    )
    result["indices"] = indices
    return result


def fit_lloyd(
    X,
    initial_centers,
    max_iter=300,
    tol=1e-4,
    tile_n=4096,
    tile_k=1024,
    update_tile_k=256,
    update_tile_n=None,
    reassign_empty=False,
    rng=None,
    step=None,
    label_step=None,
    assigner=None,
    accumulate=None,
    iteration=None,
    variance=None,
):
    """Run Lloyd iterations from caller-provided centers.

    This is the initializer-independent half of :func:`fit_kmeans`. The
    centers can be rows selected once from ``X`` and shared across backends,
    which isolates assignment, update, and convergence behavior from
    k-means++ sampling differences. ``reassign_empty=True`` enables the
    deterministic farthest-point relocation described by
    :func:`update_centroids_tiled`. ``accumulate`` optionally replaces the
    one-hot centroid sums with a backend keyed reduction.
    """
    xp = array_namespace(X, initial_centers)
    if int(max_iter) < 1:
        raise ValueError(f"max_iter must be at least 1, got {max_iter}")
    if update_tile_n is None:
        update_tile_n = min(int(tile_n), 4096)
    centers = initial_centers
    if iteration is None:
        iteration = lloyd_step
    # ``mean(var(X, axis=0))`` with the library reduction allocates a large
    # workspace (512 MiB on the timing shape). Feature tiles compute the same
    # scalar, which is the scikit-learn scale for ``tol``.
    if variance is None:
        variance = _mean_feature_variance(xp, X)
    threshold = float(tol) * _item(variance)
    labels = None
    n_iter = 0
    stats = {"empty_events": 0, "reassignments": 0}
    for n_iter in range(1, int(max_iter) + 1):
        updated, labels = iteration(
            X,
            centers,
            tile_n,
            tile_k,
            update_tile_k=update_tile_k,
            update_tile_n=update_tile_n,
            reassign_empty=reassign_empty,
            rng=rng,
            stats=stats,
            step=step,
            label_step=label_step,
            assigner=assigner,
            accumulate=accumulate,
        )
        shift = _item(xp.sum((updated - centers) ** 2))
        centers = updated
        if shift <= threshold:
            break
    value = inertia(X, labels, centers, tile_n=min(tile_n, 4096))
    return {
        "centers": centers,
        "labels": labels,
        "inertia": _item(value),
        "n_iter": n_iter,
        "shift": shift,
        "threshold": threshold,
        "empty_events": stats["empty_events"],
        "reassignments": stats["reassignments"],
    }


def _mean_feature_variance(xp, X, tile_d=128):
    """Mean over features of the population variance, one feature tile at a time."""
    n_samples = int(X.shape[0])
    n_features = int(X.shape[1])
    n = xp.asarray(n_samples, dtype=X.dtype, device=_device(X))
    total = xp.asarray(0, dtype=X.dtype, device=_device(X))
    for d0 in range(0, n_features, tile_d):
        block = X[:, d0 : min(d0 + tile_d, n_features)]
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
        block = X[:, d0 : min(d0 + tile_d, n_features)]
        part = xp.sum(block * block, axis=1)
        total = part if total is None else total + part
    return total


def _row_norm_and_variance(xp, X, tile_d=128):
    """Compute initialization row norms and Lloyd tolerance scale together."""
    n_samples = int(X.shape[0])
    n_features = int(X.shape[1])
    n = xp.asarray(n_samples, dtype=X.dtype, device=_device(X))
    row_norm = xp.zeros(n_samples, dtype=X.dtype, device=_device(X))
    variance_sum = xp.asarray(0, dtype=X.dtype, device=_device(X))
    for d0 in range(0, n_features, tile_d):
        block = X[:, d0 : min(d0 + tile_d, n_features)]
        row_norm = row_norm + xp.sum(block * block, axis=1)
        mean = xp.mean(block, axis=0)
        centered = block - mean[None, :]
        variance_sum = variance_sum + xp.sum(centered * centered) / n
    variance = variance_sum / xp.asarray(
        n_features, dtype=X.dtype, device=_device(X)
    )
    return row_norm, variance


def _distances_to_candidates(xp, X, x_norm, candidates):
    """Squared distances from every sample to a handful of candidate rows."""
    centroid_norm = xp.sum(candidates * candidates, axis=1)
    dots = xp.matmul(X, xp.matrix_transpose(candidates))
    distances = x_norm[:, None] + centroid_norm[None, :] - 2 * dots
    return xp.maximum(distances, xp.zeros_like(distances))


def stable_distances_to_candidates(
    xp, X, x_norm, candidates, *, threshold=None, stats=None
):
    """Stable GEMM distances with the k-means++ distance-hook signature."""
    return stable_gemm_distances(
        xp,
        X,
        x_norm,
        candidates,
        threshold=threshold,
        stats=stats,
    )


def broadcast_distances_to_candidates_tiled(
    xp, X, x_norm, candidates, tile_n
):
    """Broadcast candidate distances while bounding the 3D temporary.

    The ``x_norm`` argument makes this callable compatible with
    :func:`kmeans_plusplus`'s distance hook; direct differences do not use it.
    The returned ``(n_samples, n_candidates)`` matrix is small because greedy
    k-means++ evaluates only ``2 + floor(log(k))`` candidates per round.
    """
    del x_norm
    n_samples = int(X.shape[0])
    n_candidates = int(candidates.shape[0])
    distances = xp.empty(
        (n_samples, n_candidates), dtype=X.dtype, device=_device(X)
    )
    for n0 in range(0, n_samples, tile_n):
        n1 = min(n0 + tile_n, n_samples)
        distances[n0:n1, :] = squared_distances_broadcast(
            xp, X[n0:n1, :], candidates
        )
    return distances


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


def hierarchical_weighted_draw(
    xp, weights, rng, n_draws, chunk_size=256
):
    """Draw from chunk sums, then from weights inside the selected chunks.

    This is distributionally equivalent to a cumulative sum over every
    sample, but writes a cumulative array of length ``ceil(n / chunk_size)``
    instead of one of length ``n``. It follows the two-level sampling shape
    used by cakedev0's chunked k-means++ implementation. The selected chunk
    indices are read by Python so this is intended for CPU backends.
    """
    n_samples = int(weights.shape[0])
    chunk_size = max(1, int(chunk_size))
    n_full = n_samples // chunk_size
    pieces = []
    if n_full:
        full = xp.reshape(weights[: n_full * chunk_size], (n_full, chunk_size))
        pieces.append(xp.sum(full, axis=1))
    if n_full * chunk_size < n_samples:
        pieces.append(
            xp.reshape(xp.sum(weights[n_full * chunk_size :]), (1,))
        )
    chunk_weights = pieces[0] if len(pieces) == 1 else xp.concat(pieces)
    if not _item(xp.sum(chunk_weights)) > 0:
        return xp.asarray(
            rng.integers(n_samples, size=n_draws),
            dtype=xp.int64,
            device=_device(weights),
        )
    selected_chunks = _weighted_draw(xp, chunk_weights, rng, n_draws)
    selected = []
    for draw_index in range(int(n_draws)):
        chunk = int(selected_chunks[draw_index])
        start = chunk * chunk_size
        stop = min(start + chunk_size, n_samples)
        local = _weighted_draw(xp, weights[start:stop], rng, 1)
        selected.append(local + start)
    return xp.concat(selected)


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
