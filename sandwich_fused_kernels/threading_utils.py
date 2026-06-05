"""Thread-pool controls for fair single- vs multi-threaded benchmarks."""

from __future__ import annotations

import os
from contextlib import contextmanager
from typing import Iterator

import numba


@contextmanager
def sandwich_threading(num_threads: int, *, blas_threads: int | None = None) -> Iterator[None]:
    """Pin Numba, OpenMP, and BLAS thread pools (BLAS may use a separate count)."""
    if num_threads < 1:
        raise ValueError("num_threads must be >= 1")
    if blas_threads is None:
        blas_threads = num_threads
    if blas_threads < 1:
        raise ValueError("blas_threads must be >= 1")

    prev_omp = os.environ.get("OMP_NUM_THREADS")
    prev_mkl = os.environ.get("MKL_NUM_THREADS")
    prev_openblas = os.environ.get("OPENBLAS_NUM_THREADS")
    prev_numba = numba.get_num_threads()

    os.environ["OMP_NUM_THREADS"] = str(num_threads)
    os.environ["MKL_NUM_THREADS"] = str(blas_threads)
    os.environ["OPENBLAS_NUM_THREADS"] = str(blas_threads)
    numba.set_num_threads(num_threads)

    try:
        from threadpoolctl import threadpool_limits

        with threadpool_limits(limits=blas_threads, user_api="blas"):
            with threadpool_limits(limits=num_threads, user_api="openmp"):
                yield
    except ImportError:
        yield
    finally:
        numba.set_num_threads(prev_numba)
        if prev_omp is None:
            os.environ.pop("OMP_NUM_THREADS", None)
        else:
            os.environ["OMP_NUM_THREADS"] = prev_omp
        if prev_mkl is None:
            os.environ.pop("MKL_NUM_THREADS", None)
        else:
            os.environ["MKL_NUM_THREADS"] = prev_mkl
        if prev_openblas is None:
            os.environ.pop("OPENBLAS_NUM_THREADS", None)
        else:
            os.environ["OPENBLAS_NUM_THREADS"] = prev_openblas


def default_multi_thread_count() -> int:
    return os.cpu_count() or 4
