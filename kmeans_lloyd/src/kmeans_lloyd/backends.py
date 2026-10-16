"""Optional backend-native kernels behind the portable array-API Lloyd code.

The Python array API standard has no keyed (segmented) reduction, so the
portable centroid update multiplies one-hot membership tiles by ``X``.
PyTorch and CuPy both expose a scatter-add that sums rows by label directly,
which removes the membership matrix entirely. :func:`native_accumulate`
returns such a callable for those namespaces and ``None`` otherwise, in which
case callers keep the portable fallback.

Labels passed to these callables are produced by the nearest-centroid
assignment and are always in ``[0, n_clusters)``. That invariant matters:
CuPy's indexed add wraps out-of-range indices instead of raising.

Both scatter-adds use atomic floating-point additions on CUDA, so per-cluster
sums are not bitwise reproducible across runs. Measured center differences
against the one-hot path are below ``1e-6`` in float32.
"""

from __future__ import annotations

from array_api_compat import is_cupy_array, is_torch_array

_ENABLED = True


def use_native_backends(enabled):
    """Enable or disable the native paths globally; returns the old setting.

    Benchmarks use this to measure the portable fallback on the same arrays.
    """
    global _ENABLED
    previous = _ENABLED
    _ENABLED = bool(enabled)
    return previous


def native_accumulate(X):
    """Return a keyed sums-and-counts callable for ``X``'s namespace, or None."""
    if not _ENABLED:
        return None
    if is_torch_array(X):
        return _torch_accumulate
    if is_cupy_array(X):
        return _cupy_accumulate
    return None


def _torch_accumulate(X, labels, n_clusters):
    import torch

    sums = torch.zeros((n_clusters, X.shape[1]), dtype=X.dtype, device=X.device)
    sums.index_add_(0, labels, X)
    counts = torch.bincount(labels, minlength=n_clusters).to(X.dtype)
    return sums, counts


def _cupy_accumulate(X, labels, n_clusters):
    import cupy

    sums = cupy.zeros((n_clusters, X.shape[1]), dtype=X.dtype)
    # CuPy 14 deprecates ``cupyx.scatter_add`` in favor of this spelling;
    # both lower to the same atomic kernel and timed alike in journal 014.
    cupy.add.at(sums, labels, X)
    # TODO: a single RawKernel that accumulates sums and counts in one launch
    # was 2.2x to 2.4x faster than add.at plus bincount at 550 and 3000
    # clusters (journal 014). It would need per-dtype kernels, cached
    # compilation, and the same empty-cluster tests before replacing this.
    counts = cupy.bincount(labels, minlength=n_clusters).astype(X.dtype)
    return sums, counts
