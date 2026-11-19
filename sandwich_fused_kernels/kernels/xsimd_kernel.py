"""Python wrapper for the xsimd C++ sandwich kernel."""

from __future__ import annotations

import ctypes
import os
from pathlib import Path

import numpy as np

_LIB: ctypes.CDLL | None = None
_LIB_PATH = Path(__file__).resolve().parents[1] / "xsimd_ext" / "libsandwich_xsimd.so"


def _load_library() -> ctypes.CDLL:
    global _LIB
    if _LIB is not None:
        return _LIB
    if not _LIB_PATH.is_file():
        raise FileNotFoundError(
            f"xsimd shared library not found at {_LIB_PATH}. "
            "Run sandwich_fused_kernels/xsimd_ext/build.sh first."
        )
    lib = ctypes.CDLL(str(_LIB_PATH))
    lib.sandwich_xsimd_f64.argtypes = [
        ctypes.c_void_p,
        ctypes.c_void_p,
        ctypes.c_void_p,
        ctypes.c_int64,
        ctypes.c_int64,
        ctypes.c_int,
        ctypes.c_int,
        ctypes.c_int,
    ]
    lib.sandwich_xsimd_f64.restype = None
    lib.sandwich_xsimd_batch_width.argtypes = []
    lib.sandwich_xsimd_batch_width.restype = ctypes.c_int64
    _LIB = lib
    return lib


def xsimd_batch_width() -> int:
    """SIMD lane width (doubles per batch) used by the native kernel."""
    return int(_load_library().sandwich_xsimd_batch_width())


def sandwich_xsimd(
    X: np.ndarray,
    d: np.ndarray,
    *,
    num_threads: int = 1,
    block: int = 4,
    chunk_factor: int = 4,
) -> np.ndarray:
    """Compute X.T @ diag(d) @ X via the xsimd/OpenMP extension."""
    if X.dtype != np.float64:
        raise TypeError("sandwich_xsimd currently supports float64 only")
    Xc = np.ascontiguousarray(X, dtype=np.float64)
    dc = np.ascontiguousarray(d, dtype=np.float64)
    if dc.shape[0] != Xc.shape[0]:
        raise ValueError("d must have length n_rows")

    out = np.zeros((Xc.shape[1], Xc.shape[1]), dtype=np.float64)
    lib = _load_library()
    lib.sandwich_xsimd_f64(
        Xc.ctypes.data_as(ctypes.c_void_p),
        dc.ctypes.data_as(ctypes.c_void_p),
        out.ctypes.data_as(ctypes.c_void_p),
        Xc.shape[0],
        Xc.shape[1],
        int(num_threads),
        int(block),
        int(chunk_factor),
    )
    return out


def warmup_xsimd(num_threads: int = 1) -> None:
    """Trigger library load and one small compilation-free run."""
    rng = np.random.default_rng(0)
    X = rng.standard_normal((64, 8))
    d = rng.random(64) + 0.1
    prev = os.environ.get("OMP_NUM_THREADS")
    os.environ["OMP_NUM_THREADS"] = str(num_threads)
    try:
        sandwich_xsimd(X, d, num_threads=num_threads)
    finally:
        if prev is None:
            os.environ.pop("OMP_NUM_THREADS", None)
        else:
            os.environ["OMP_NUM_THREADS"] = prev
