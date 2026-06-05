"""Numba-compiled fused sandwich kernels for CPU."""

from __future__ import annotations

import numpy as np
import numba
from numba import njit, prange


@njit(cache=True)
def sandwich_numba_serial(X: np.ndarray, d: np.ndarray) -> np.ndarray:
    """Serial fused kernel: out[i,j] = sum_k X[k,i]*d[k]*X[k,j]."""
    n_rows, n_cols = X.shape
    out = np.zeros((n_cols, n_cols), dtype=X.dtype)
    for j in range(n_cols):
        for i in range(j, n_cols):
            acc = X.dtype.type(0.0)
            for k in range(n_rows):
                acc += X[k, i] * d[k] * X[k, j]
            out[i, j] = acc
            out[j, i] = acc
    return out


@njit(parallel=True, fastmath=True, cache=True)
def sandwich_numba_k_inner(X: np.ndarray, d: np.ndarray) -> np.ndarray:
    """Parallel over columns with k as innermost loop (can emit harmful scatter SIMD)."""
    n_rows, n_cols = X.shape
    out = np.zeros((n_cols, n_cols), dtype=X.dtype)
    for j in prange(n_cols):
        for i in range(n_cols):
            acc = X.dtype.type(0.0)
            for k in range(n_rows):
                acc += X[k, i] * d[k] * X[k, j]
            out[i, j] = acc
    return out


@njit(cache=True, fastmath=True)
def _flush_block_acc(
    acc: np.ndarray,
    out: np.ndarray,
    i0: int,
    j0: int,
    ni: int,
    nj: int,
    diagonal_block: bool,
) -> None:
    """Write a block accumulator symmetrically into out."""
    for li in range(ni):
        for lj in range(nj):
            gi = i0 + li
            gj = j0 + lj
            v = acc[li, lj]
            if diagonal_block:
                if gi > gj:
                    continue
                out[gi, gj] += v
                if gi != gj:
                    out[gj, gi] += v
            else:
                out[gi, gj] += v
                out[gj, gi] += v


@njit(cache=True, fastmath=True)
def _rank1_update_block(
    acc: np.ndarray,
    x_row: np.ndarray,
    i0: int,
    j0: int,
    ni: int,
    nj: int,
    w: float,
) -> None:
    """Fused rank-1 update for one lower-triangle block from weighted row x_row."""
    for li in range(ni):
        xi = x_row[i0 + li] * w
        lj = 0
        while lj + 4 <= nj:
            acc[li, lj] += xi * x_row[j0 + lj]
            acc[li, lj + 1] += xi * x_row[j0 + lj + 1]
            acc[li, lj + 2] += xi * x_row[j0 + lj + 2]
            acc[li, lj + 3] += xi * x_row[j0 + lj + 3]
            lj += 4
        while lj < nj:
            acc[li, lj] += xi * x_row[j0 + lj]
            lj += 1


@njit(cache=True, fastmath=True)
def _accumulate_kouter_blocks(X: np.ndarray, d: np.ndarray, out: np.ndarray, block: int) -> None:
    """K-outer blocked accumulation: block buffers stay hot while streaming rows."""
    n_rows, n_cols = X.shape
    n_blocks = (n_cols + block - 1) // block
    acc = np.zeros((n_blocks, n_blocks, block, block), dtype=X.dtype)

    for k in range(n_rows):
        w = d[k]
        for ib in range(n_blocks):
            i0 = ib * block
            i1 = i0 + block
            if i1 > n_cols:
                i1 = n_cols
            ni = i1 - i0
            for jb in range(ib + 1):
                j0 = jb * block
                j1 = j0 + block
                if j1 > n_cols:
                    j1 = n_cols
                nj = j1 - j0
                _rank1_update_block(acc[ib, jb], X[k], i0, j0, ni, nj, w)

    for ib in range(n_blocks):
        i0 = ib * block
        i1 = i0 + block
        if i1 > n_cols:
            i1 = n_cols
        ni = i1 - i0
        for jb in range(ib + 1):
            j0 = jb * block
            j1 = j0 + block
            if j1 > n_cols:
                j1 = n_cols
            nj = j1 - j0
            _flush_block_acc(acc[ib, jb], out, i0, j0, ni, nj, ib == jb)


@njit(cache=True, fastmath=True)
def _accumulate_tabmat_blocks(X: np.ndarray, d: np.ndarray, out: np.ndarray, block: int) -> None:
    """Blocked fused accumulation with symmetric mirror into out (block-outer)."""
    n_rows, n_cols = X.shape
    n_blocks = (n_cols + block - 1) // block

    for jb in range(n_blocks):
        j0 = jb * block
        j1 = j0 + block
        if j1 > n_cols:
            j1 = n_cols
        nj = j1 - j0
        for ib in range(jb + 1):
            i0 = ib * block
            i1 = i0 + block
            if i1 > n_cols:
                i1 = n_cols
            ni = i1 - i0
            acc = np.zeros((ni, nj), dtype=X.dtype)
            for k in range(n_rows):
                w = d[k]
                _rank1_update_block(acc, X[k], i0, j0, ni, nj, w)
            _flush_block_acc(acc, out, i0, j0, ni, nj, ib == jb)


@njit(cache=True, fastmath=True)
def sandwich_numba_kouter_st(X: np.ndarray, d: np.ndarray) -> np.ndarray:
    """Single-thread k-outer tabmat-style kernel (block buffers resident across rows)."""
    out = np.zeros((X.shape[1], X.shape[1]), dtype=X.dtype)
    _accumulate_kouter_blocks(X, d, out, 4)
    return out


@njit(cache=True, fastmath=True)
def sandwich_numba_tabmat_style_st(X: np.ndarray, d: np.ndarray) -> np.ndarray:
    """Single-thread tabmat-style: 4x4 blocks, symmetric mirror, fused weights."""
    out = np.zeros((X.shape[1], X.shape[1]), dtype=X.dtype)
    _accumulate_tabmat_blocks(X, d, out, 4)
    return out


@njit(cache=True, fastmath=True)
def sandwich_numba_rival_st(X: np.ndarray, d: np.ndarray) -> np.ndarray:
    """Best-effort single-thread fused rival: block-outer 4x4 + manual rank-1 unroll."""
    return sandwich_numba_tabmat_style_st(X, d)


@njit(parallel=True, fastmath=True, cache=True)
def sandwich_numba_tabmat_style_mt(X: np.ndarray, d: np.ndarray) -> np.ndarray:
    """Multi-thread tabmat-style: parallel over j-blocks, private accumulators."""
    n_rows, n_cols = X.shape
    block = 8
    n_blocks = (n_cols + block - 1) // block
    out = np.zeros((n_cols, n_cols), dtype=X.dtype)

    for jb in prange(n_blocks):
        j0 = jb * block
        j1 = j0 + block
        if j1 > n_cols:
            j1 = n_cols
        nj = j1 - j0
        for ib in range(jb + 1):
            i0 = ib * block
            i1 = i0 + block
            if i1 > n_cols:
                i1 = n_cols
            ni = i1 - i0
            acc = np.zeros((ni, nj), dtype=X.dtype)
            for k in range(n_rows):
                w = d[k]
                _rank1_update_block(acc, X[k], i0, j0, ni, nj, w)
            _flush_block_acc(acc, out, i0, j0, ni, nj, ib == jb)
    return out


@njit(parallel=True, fastmath=True, cache=True)
def _sandwich_kchunk_fused_impl(
    X: np.ndarray,
    d: np.ndarray,
    n_chunks: int,
    block: int,
) -> np.ndarray:
    n_rows, n_cols = X.shape
    k_chunk = (n_rows + n_chunks - 1) // n_chunks
    partial = np.zeros((n_chunks, n_cols, n_cols), dtype=X.dtype)

    for cb in prange(n_chunks):
        k0 = cb * k_chunk
        k1 = k0 + k_chunk
        if k1 > n_rows:
            k1 = n_rows
        _accumulate_tabmat_blocks(X[k0:k1], d[k0:k1], partial[cb], block)
    return np.sum(partial, axis=0)


@njit(parallel=True, fastmath=True, cache=True)
def _sandwich_kchunk_blas_impl(X: np.ndarray, d: np.ndarray, n_chunks: int) -> np.ndarray:
    n_rows, n_cols = X.shape
    k_chunk = (n_rows + n_chunks - 1) // n_chunks
    partial = np.zeros((n_chunks, n_cols, n_cols), dtype=X.dtype)

    for cb in prange(n_chunks):
        k0 = cb * k_chunk
        k1 = k0 + k_chunk
        if k1 > n_rows:
            k1 = n_rows
        Xc = X[k0:k1]
        dc = d[k0:k1]
        weighted = Xc * dc.reshape(-1, 1)
        partial[cb] = weighted.T @ Xc
    return np.sum(partial, axis=0)


def _fused_chunk_count() -> int:
    threads = numba.get_num_threads()
    if threads <= 1:
        return 1
    return threads * 4


def _blas_chunk_count() -> int:
    threads = numba.get_num_threads()
    if threads <= 1:
        return 1
    return threads * 2


def sandwich_numba_k_chunk_tabmat(X: np.ndarray, d: np.ndarray) -> np.ndarray:
    """Row-chunk partials + block-outer tabmat-style fused micro-kernel."""
    return _sandwich_kchunk_fused_impl(X, d, _fused_chunk_count(), 4)


def sandwich_numba_rival_mt(X: np.ndarray, d: np.ndarray) -> np.ndarray:
    """Multi-thread fused rival: k-chunk partials + block-outer 4x4 micro-kernel."""
    return sandwich_numba_k_chunk_tabmat(X, d)


def sandwich_numba_blas_kchunk_mt(X: np.ndarray, d: np.ndarray) -> np.ndarray:
    """Multi-thread BLAS rival: prange row chunks with single-thread GEMM per worker."""
    return _sandwich_kchunk_blas_impl(X, d, _blas_chunk_count())


def sandwich_numba_k_chunk_tabmat_mt(X: np.ndarray, d: np.ndarray) -> np.ndarray:
    """Alias for rival_mt with explicit name."""
    return sandwich_numba_rival_mt(X, d)


sandwich_numba_kchunk_kouter_mt = sandwich_numba_rival_mt


@njit(parallel=True, fastmath=True, cache=True)
def sandwich_numba_fused_blocked(X: np.ndarray, d: np.ndarray) -> np.ndarray:
    """Blocked fused kernel: no weighted-X buffer; k fused in inner accumulation."""
    n_rows, n_cols = X.shape
    block = 32
    out = np.zeros((n_cols, n_cols), dtype=X.dtype)
    n_blocks = (n_cols + block - 1) // block

    for jb in prange(n_blocks):
        j0 = jb * block
        j1 = j0 + block
        if j1 > n_cols:
            j1 = n_cols
        nj = j1 - j0
        for ib in range(n_blocks):
            i0 = ib * block
            i1 = i0 + block
            if i1 > n_cols:
                i1 = n_cols
            ni = i1 - i0
            acc = np.zeros((ni, nj), dtype=X.dtype)
            for k in range(n_rows):
                w = d[k]
                for li in range(ni):
                    xi = X[k, i0 + li] * w
                    for lj in range(nj):
                        acc[li, lj] += xi * X[k, j0 + lj]
            for li in range(ni):
                for lj in range(nj):
                    out[i0 + li, j0 + lj] += acc[li, lj]
    return out


@njit(cache=True)
def sandwich_numba_blas_fused(X: np.ndarray, d: np.ndarray) -> np.ndarray:
    """Single BLAS call: (X * d).T @ X (materializes weighted X)."""
    weighted = X * d.reshape(-1, 1)
    return weighted.T @ X


@njit(parallel=True, fastmath=True, cache=True)
def sandwich_numba_blas_chunked(X: np.ndarray, d: np.ndarray) -> np.ndarray:
    """Chunk rows and delegate each chunk to BLAS (weighted Gram), then reduce."""
    n_rows, n_cols = X.shape
    chunk = 8192
    n_chunks = (n_rows + chunk - 1) // chunk
    partial = np.zeros((n_chunks, n_cols, n_cols), dtype=X.dtype)

    for cb in prange(n_chunks):
        k0 = cb * chunk
        k1 = k0 + chunk
        if k1 > n_rows:
            k1 = n_rows
        Xc = X[k0:k1]
        dc = d[k0:k1]
        weighted = Xc * dc.reshape(-1, 1)
        partial[cb] = weighted.T @ Xc
    return np.sum(partial, axis=0)


@njit(parallel=True, fastmath=True, cache=True)
def sandwich_numba_blas_tiled(X: np.ndarray, d: np.ndarray) -> np.ndarray:
    """Smaller row chunks (2048) to improve cache locality vs blas_chunked."""
    n_rows, n_cols = X.shape
    chunk = 2048
    n_chunks = (n_rows + chunk - 1) // chunk
    partial = np.zeros((n_chunks, n_cols, n_cols), dtype=X.dtype)

    for cb in prange(n_chunks):
        k0 = cb * chunk
        k1 = k0 + chunk
        if k1 > n_rows:
            k1 = n_rows
        Xc = X[k0:k1]
        dc = d[k0:k1]
        weighted = Xc * dc.reshape(-1, 1)
        partial[cb] = weighted.T @ Xc
    return np.sum(partial, axis=0)


@njit(parallel=True, fastmath=True, cache=True)
def sandwich_numba_k_parallel(X: np.ndarray, d: np.ndarray) -> np.ndarray:
    """Parallel over row blocks; each block writes to a private partial matrix."""
    n_rows, n_cols = X.shape
    k_block = 256
    n_k_blocks = (n_rows + k_block - 1) // k_block
    partial = np.zeros((n_k_blocks, n_cols, n_cols), dtype=X.dtype)

    for kb in prange(n_k_blocks):
        k0 = kb * k_block
        k1 = k0 + k_block
        if k1 > n_rows:
            k1 = n_rows
        for j in range(n_cols):
            for i in range(j, n_cols):
                acc = X.dtype.type(0.0)
                for k in range(k0, k1):
                    acc += X[k, i] * d[k] * X[k, j]
                partial[kb, i, j] = acc
                partial[kb, j, i] = acc
    return np.sum(partial, axis=0)


_VARIANTS = {
    "serial": sandwich_numba_serial,
    "k_inner": sandwich_numba_k_inner,
    "kouter_st": sandwich_numba_kouter_st,
    "rival_st": sandwich_numba_rival_st,
    "tabmat_style_st": sandwich_numba_tabmat_style_st,
    "tabmat_style_mt": sandwich_numba_tabmat_style_mt,
    "tabmat_style": sandwich_numba_rival_mt,
    "rival_mt": sandwich_numba_rival_mt,
    "kchunk_kouter_mt": sandwich_numba_rival_mt,
    "k_chunk_tabmat": sandwich_numba_k_chunk_tabmat,
    "blas_kchunk_mt": sandwich_numba_blas_kchunk_mt,
    "fused_blocked": sandwich_numba_fused_blocked,
    "blas_fused": sandwich_numba_blas_fused,
    "blas_chunked": sandwich_numba_blas_chunked,
    "blas_tiled": sandwich_numba_blas_tiled,
    "k_parallel": sandwich_numba_k_parallel,
    "blocked": sandwich_numba_fused_blocked,
}


def sandwich_numba(
    X: np.ndarray,
    d: np.ndarray,
    rows: np.ndarray | None = None,
    cols: np.ndarray | None = None,
    variant: str = "rival_mt",
) -> np.ndarray:
    """Dispatch to a compiled numba kernel on contiguous row/column subsets."""
    if rows is None:
        rows = np.arange(X.shape[0], dtype=np.int64)
    if cols is None:
        cols = np.arange(X.shape[1], dtype=np.int64)

    X_sub = np.ascontiguousarray(X[np.ix_(rows, cols)])
    d_sub = np.ascontiguousarray(np.asarray(d, dtype=X.dtype)[rows])
    fn = _VARIANTS[variant]
    return fn(X_sub, d_sub)


def warmup_numba(variant: str = "rival_mt") -> None:
    """Trigger JIT compilation before timed runs."""
    rng = np.random.default_rng(0)
    X = rng.standard_normal((128, 16), dtype=np.float64)
    d = rng.random(128, dtype=np.float64)
    sandwich_numba(X, d, variant=variant)
