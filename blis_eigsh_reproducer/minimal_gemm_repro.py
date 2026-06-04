#!/usr/bin/env python
"""Fixed-data Python reproducer for the BLIS ``V @ diag(S) @ V.T`` bug.

The inputs are stored as plain ASCII files in ``fixtures/``:

    rows cols
    value_00 value_01 ...
    ...

This script loads ``V_100_10.txt`` and ``S_100_10.txt`` and performs only the
faulty step:

    C = (V @ diag(S)) @ V.T

The BLAS result is compared against a non-BLAS ``einsum`` reference. On macOS
arm64 with conda-forge BLIS, this single fixed-data GEMM returns ~1e+272 garbage.
"""

from __future__ import annotations

import argparse
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
FIX = os.path.join(HERE, "fixtures")


def _read_txt(name):
    path = os.path.join(FIX, name)
    with open(path, encoding="ascii") as f:
        rows, cols = map(int, f.readline().split())
        data = np.fromfile(f, sep=" ", dtype=np.float64)
    return data.reshape(rows, cols)


def _einsum_matmul(A, B):
    """Non-BLAS reference matmul (NumPy nditer C loop, no GEMM dispatch)."""
    return np.einsum("ik,kj->ij", A, B, optimize=False)


def _target_gemm():
    V = _read_txt("V_100_10.txt")
    S = _read_txt("S_100_10.txt").ravel()
    M1 = V @ np.diag(S)
    C = M1 @ V.T
    C_ref = _einsum_matmul(_einsum_matmul(V, np.diag(S)), V.T)
    err = float(np.max(np.abs(C - C_ref)))
    scale = float(np.max(np.abs(C_ref))) or 1.0
    rel = err / scale
    bad = rel > 1e-9 or not np.isfinite(C).all()
    print(
        f"Python fixed-data V@diag(S)@V.T: max_abs_err={err:.17e} "
        f"rel_err={rel:.17e} max|out|={float(np.max(np.abs(C))):.17e}"
        + ("   <<< MISMATCH (bug reproduced)" if bad else "   (ok)"),
        flush=True,
    )
    return 1 if bad else 0


def _print_backend():
    thread_env = {
        k: os.environ.get(k)
        for k in ("BLIS_NUM_THREADS", "OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "VECLIB_MAXIMUM_THREADS")
        if os.environ.get(k) is not None
    }
    print(f"thread env: {thread_env}  numpy {np.__version__}", flush=True)


def main() -> int:
    argparse.ArgumentParser(description=__doc__).parse_args()
    _print_backend()
    rc = _target_gemm()
    print(("FAIL" if rc else "PASS") + " [python-fixed-data]", flush=True)
    return rc


if __name__ == "__main__":
    sys.exit(main())
