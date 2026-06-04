#!/usr/bin/env python
"""Minimal, fixed-data reproducer for the BLIS ``V @ diag(S) @ V.T`` corruption.

The full investigation (see ``eigsh_blis_reproducer.py --level numpy-trace``)
localized the failure of ``test_randomized_eigsh_reconst_low_rank`` to a *single*
GEMM -- the final reconstruction ``(V @ diag(S)) @ V.T`` for the ``n=100,
rank=10`` case -- with every preceding pipeline step bit-exact on BLIS.

This script tries to trigger that one GEMM from **fixed captured operands**
(``fixtures/V_100_10.txt`` / ``S_100_10.txt``), without running the randomized
power iterations / SVD that originally produced them. Because the corruption was
order/state dependent, several "prequel" variants probe how little state is
needed:

  single        : just the target GEMM, nothing before it.
  gemm-prequel  : one fixed-data GEMM (the 10x7 reconstruction) THEN the target.
  svd-prequel   : a single scipy.linalg.svd THEN the target.
  eigsh-prequel : the full (10,7) randomized-eigsh THEN the target.

Each variant is meant to run in its OWN fresh process. The target GEMM is always
the same fixed-data ``(V @ diag(S)) @ V.T``; we compare it against a non-BLAS
einsum reference and flag a mismatch (BLIS returns ~1e+300 garbage).
"""

from __future__ import annotations

import argparse
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
FIX = os.path.join(HERE, "fixtures")

VARIANTS = (
    "single",
    "gemm-prequel",
    "svd-prequel",
    "eigsh-prequel",
    "contig-vt",
    "fortran-v",
    "strided-view",
)


def _load(n, rank):
    def read_txt(name):
        path = os.path.join(FIX, name)
        with open(path, encoding="ascii") as f:
            rows, cols = map(int, f.readline().split())
            data = np.fromfile(f, sep=" ", dtype=np.float64)
        return data.reshape(rows, cols)

    if n == 100 and rank == 10:
        return read_txt("V_100_10.txt"), read_txt("S_100_10.txt").ravel()
    return (
        np.load(os.path.join(FIX, f"V_{n}_{rank}.npy")),
        np.load(os.path.join(FIX, f"S_{n}_{rank}.npy")),
    )


def _einsum_matmul(A, B):
    """Non-BLAS reference matmul (NumPy nditer C loop, no GEMM dispatch)."""
    return np.einsum("ik,kj->ij", A, B, optimize=False)


def _target_gemm(layout="as-loaded"):
    """The localized failing op: (V @ diag(S)) @ V.T for n=100, rank=10.

    ``layout`` controls the memory layout of the operands, to probe whether the
    BLIS dgemm corruption depends on contiguity / strides:
      as-loaded   : V as stored in the .npy (C-contiguous), second operand V.T (view)
      contig-vt   : materialize the second operand contiguous (ascontiguousarray)
      fortran-v   : V in Fortran (column-major) order
      strided-view: V as a column slice of a larger array (mimics U[:, :rank])
    """
    V, S = _load(100, 10)
    if layout == "fortran-v":
        V = np.asfortranarray(V)
    elif layout == "strided-view":
        n, rank = V.shape
        big = np.zeros((n, rank + 10), dtype=V.dtype)
        big[:, :rank] = V
        V = big[:, :rank]  # non-contiguous column-slice view, like U[:, :rank]

    Vt = np.ascontiguousarray(V.T) if layout == "contig-vt" else V.T
    M1 = V @ np.diag(S)          # (100, 10) -- GEMM with k=10
    C = M1 @ Vt                  # (100, 10) @ (10, 100) -> (100, 100), small k
    C_ref = _einsum_matmul(_einsum_matmul(V, np.diag(S)), np.asarray(V.T))
    err = float(np.max(np.abs(C - C_ref)))
    scale = float(np.max(np.abs(C_ref))) or 1.0
    rel = err / scale
    bad = rel > 1e-9 or not np.isfinite(C).all()
    flags = "C" if V.flags["C_CONTIGUOUS"] else ("F" if V.flags["F_CONTIGUOUS"] else "strided")
    print(
        f"  target (V@diag(S))@V.T [V={flags}, Vt={'C' if Vt.flags['C_CONTIGUOUS'] else 'view'}]"
        f" : max_abs_err={err:.3e} rel_err={rel:.3e} max|out|={float(np.max(np.abs(C))):.3e}"
        + ("   <<< MISMATCH (bug reproduced)" if bad else "   (ok)"),
        flush=True,
    )
    return 1 if bad else 0


def _prequel_gemm():
    """The 10x7 reconstruction GEMM from fixed data (no SVD, pure numpy)."""
    V, S = _load(10, 7)
    _ = (V @ np.diag(S)) @ V.T
    print("  prequel: did fixed-data (10,7) reconstruction GEMM", flush=True)


def _prequel_svd():
    """A single scipy LAPACK SVD before the target (does it set up the state?)."""
    from scipy import linalg

    A, _ = _load(100, 10)  # reuse a fixed array just to have something to SVD
    linalg.svd(A, full_matrices=False, lapack_driver="gesdd")
    print("  prequel: did one scipy.linalg.svd (gesdd)", flush=True)


def _prequel_eigsh():
    """Run the full (10,7) randomized-eigsh pipeline before the target."""
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "_eigsh_mod", os.path.join(HERE, "eigsh_blis_reproducer.py")
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    A, rng = mod._make_low_rank_psd(10, 7)
    mod._np_randomized_eigsh(A, n_components=7, random_state=rng)
    print("  prequel: ran full (10,7) randomized-eigsh pipeline", flush=True)


def _print_backend():
    thread_env = {
        k: os.environ.get(k)
        for k in ("BLIS_NUM_THREADS", "OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "VECLIB_MAXIMUM_THREADS")
        if os.environ.get(k) is not None
    }
    print(f"thread env: {thread_env}  numpy {np.__version__}", flush=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--variant", choices=VARIANTS, default="single")
    args = parser.parse_args()
    _print_backend()
    print(f"=== variant={args.variant} ===", flush=True)
    layout = "as-loaded"
    if args.variant == "gemm-prequel":
        _prequel_gemm()
    elif args.variant == "svd-prequel":
        _prequel_svd()
    elif args.variant == "eigsh-prequel":
        _prequel_eigsh()
    elif args.variant in ("contig-vt", "fortran-v", "strided-view"):
        layout = args.variant
    rc = _target_gemm(layout=layout)
    print(("FAIL" if rc else "PASS") + f" [{args.variant}]", flush=True)
    return rc


if __name__ == "__main__":
    sys.exit(main())
