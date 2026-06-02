#!/usr/bin/env python
"""Progressive reproducer for the macOS arm64 BLIS ``test_randomized_eigsh_reconst_low_rank`` failure.

Upstream context: scikit-learn#34162 (lock-file update flips conda ``libblas`` to
BLIS on macOS arm64), discussion_r3332644920.  The test
``sklearn/utils/tests/test_extmath.py::test_randomized_eigsh_reconst_low_rank``
starts failing because the randomized eigendecomposition no longer reconstructs
the original low-rank PSD matrix to ``decimal=6``.

This script reproduces the failure at several levels, stripping sklearn piece by
piece (run with ``--level <name>``; see ``--list-levels``):

* ``pytest``        -- run the upstream test verbatim (largest sklearn surface).
* ``sklearn-eigsh`` -- call ``sklearn.utils.extmath._randomized_eigsh`` directly.
* ``numpy-eigsh``   -- self-contained NumPy + SciPy port of ``_randomized_eigsh``
                       (no sklearn at all): the minimal reproducer target.

Every level loops over the same ``(n, rank)`` grid as the upstream
``@pytest.mark.parametrize`` and reports the reconstruction / orthonormality
error per case.  The process exits non-zero as soon as one case exceeds the
upstream ``decimal=6`` tolerance, which is exactly what happens on BLIS but not
on OpenBLAS / Accelerate.

Threading note: like the KNNImputer reproducer, the bug needs BLIS to actually
use several threads (``BLIS_NUM_THREADS=8``); do not pin everything to a single
thread.
"""

from __future__ import annotations

import argparse
import subprocess
import sys

import numpy as np
from scipy import linalg

# Same parametrization as the upstream test.
PARAM_GRID = (
    (10, 7),
    (100, 10),
    (100, 80),
    (500, 10),
    (500, 250),
    (500, 400),
)

LEVELS = ("numpy-eigsh", "numpy-kernels", "sklearn-eigsh", "pytest")

# ``assert_array_almost_equal(..., decimal=6)`` passes iff
# ``abs(desired - actual) < 1.5 * 10**(-6)``.
DECIMAL = 6
TOL = 1.5 * 10 ** (-DECIMAL)


# --------------------------------------------------------------------------- #
# Self-contained NumPy + SciPy port of sklearn's randomized eigsh machinery.
# Mirrors sklearn/utils/extmath.py (_randomized_range_finder, _randomized_svd,
# _randomized_eigsh) for the dense float64 symmetric-PSD path exercised by the
# failing test, with the array-api / sparse / validation branches removed.
# --------------------------------------------------------------------------- #
def _np_randomized_range_finder(A, *, size, n_iter, power_iteration_normalizer, random_state):
    Q = random_state.normal(size=(A.shape[1], size))
    Q = np.asarray(Q)

    if power_iteration_normalizer == "auto":
        power_iteration_normalizer = "none" if n_iter <= 2 else "LU"

    qr_normalizer = lambda x: linalg.qr(x, mode="economic", check_finite=False)
    if power_iteration_normalizer == "QR":
        normalizer = qr_normalizer
    elif power_iteration_normalizer == "LU":
        normalizer = lambda x: linalg.lu(x, permute_l=True, check_finite=False)
    else:
        normalizer = lambda x: (x, None)

    for _ in range(n_iter):
        Q, _ = normalizer(A @ Q)
        Q, _ = normalizer(A.T @ Q)

    Q, _ = qr_normalizer(A @ Q)
    return Q


def _np_randomized_svd(
    M,
    n_components,
    *,
    n_oversamples=10,
    n_iter="auto",
    power_iteration_normalizer="auto",
    transpose="auto",
    flip_sign=True,
    random_state,
    svd_lapack_driver="gesdd",
):
    n_random = n_components + n_oversamples
    n_samples, n_features = M.shape

    if n_iter == "auto":
        n_iter = 7 if n_components < 0.1 * min(M.shape) else 4

    if transpose == "auto":
        transpose = n_samples < n_features
    if transpose:
        M = M.T

    Q = _np_randomized_range_finder(
        M,
        size=n_random,
        n_iter=n_iter,
        power_iteration_normalizer=power_iteration_normalizer,
        random_state=random_state,
    )

    B = Q.T @ M
    Uhat, s, Vt = linalg.svd(B, full_matrices=False, lapack_driver=svd_lapack_driver)
    del B
    U = Q @ Uhat

    if flip_sign:
        U, Vt = _svd_flip(U, Vt, u_based_decision=not transpose)

    if transpose:
        return Vt[:n_components, :].T, s[:n_components], U[:, :n_components].T
    return U[:, :n_components], s[:n_components], Vt[:n_components, :]


def _svd_flip(u, v, u_based_decision=True):
    if u_based_decision:
        max_abs_cols = np.argmax(np.abs(u), axis=0)
        signs = np.sign(u[max_abs_cols, range(u.shape[1])])
    else:
        max_abs_rows = np.argmax(np.abs(v), axis=1)
        signs = np.sign(v[range(v.shape[0]), max_abs_rows])
    u = u * signs
    v = v * signs[:, np.newaxis]
    return u, v


def _np_randomized_eigsh(
    M,
    n_components,
    *,
    n_oversamples=10,
    n_iter="auto",
    power_iteration_normalizer="auto",
    selection="module",
    random_state,
):
    if selection != "module":
        raise NotImplementedError(selection)
    U, S, Vt = _np_randomized_svd(
        M,
        n_components=n_components,
        n_oversamples=n_oversamples,
        n_iter=n_iter,
        power_iteration_normalizer=power_iteration_normalizer,
        flip_sign=False,
        random_state=random_state,
    )
    eigvecs = U[:, :n_components]
    eigvals = S[:n_components]
    diag_VtU = np.einsum("ji,ij->j", Vt[:n_components, :], U[:, :n_components])
    eigvals = eigvals * np.sign(diag_VtU)
    return eigvals, eigvecs


# --------------------------------------------------------------------------- #
# Shared checks (mirror the body of test_randomized_eigsh_reconst_low_rank).
# --------------------------------------------------------------------------- #
def _make_low_rank_psd(n, rank, seed=69):
    """Identical construction to the upstream test (and its rng consumption)."""
    rng = np.random.RandomState(seed)
    X = rng.randn(n, rank)
    A = X @ X.T
    # The very same ``rng`` is then passed to _randomized_eigsh, so the
    # range-finder Gaussian is drawn from this advanced state.
    return A, rng


def _reconstruction_errors(A, S, V, rank):
    """Return (norm_err, orth_err, reconstruct_err) as the test would assert."""
    norm_err = float(np.max(np.abs(np.linalg.norm(V, axis=0) - np.ones(S.shape))))
    orth_err = float(np.max(np.abs(V.T @ V - np.diag(np.ones(S.shape)))))
    A_reconstruct = V @ np.diag(S) @ V.T
    reconstruct_err = float(np.max(np.abs(A_reconstruct - A)))
    return norm_err, orth_err, reconstruct_err


def _run_eigsh_grid(level, eigsh_fn):
    """Run ``eigsh_fn`` over the parametrize grid, print errors, return rc."""
    print(f"=== level={level} | tol(decimal={DECIMAL})={TOL:.3g} ===", flush=True)
    print(
        f"{'n':>5} {'rank':>5} {'norm_err':>12} {'orth_err':>12} "
        f"{'reconst_err':>14} {'status':>7}",
        flush=True,
    )
    failures = []
    for n, rank in PARAM_GRID:
        print(f"... running n={n} rank={rank}", flush=True)
        A, rng = _make_low_rank_psd(n, rank)
        S, V = eigsh_fn(A, rank, rng)
        norm_err, orth_err, reconstruct_err = _reconstruction_errors(A, S, V, rank)
        worst = max(norm_err, orth_err, reconstruct_err)
        ok = worst < TOL
        if not ok:
            failures.append((n, rank, reconstruct_err))
        print(
            f"{n:>5} {rank:>5} {norm_err:>12.3e} {orth_err:>12.3e} "
            f"{reconstruct_err:>14.3e} {'OK' if ok else 'FAIL':>7}",
            flush=True,
        )
    if failures:
        worst = max(f[2] for f in failures)
        cases = ", ".join(f"(n={n},rank={r})" for n, r, _ in failures)
        print(
            f"FAIL [{level}]: {len(failures)}/{len(PARAM_GRID)} cases exceed "
            f"decimal={DECIMAL}; worst reconst_err={worst:.3e}; cases: {cases}",
            flush=True,
        )
        return 1
    print(f"PASS [{level}]: all {len(PARAM_GRID)} cases within decimal={DECIMAL}", flush=True)
    return 0


# --------------------------------------------------------------------------- #
# Level runners.
# --------------------------------------------------------------------------- #
def run_numpy_eigsh() -> int:
    def fn(A, rank, rng):
        return _np_randomized_eigsh(A, n_components=rank, random_state=rng)

    return _run_eigsh_grid("numpy-eigsh", fn)


def _einsum_matmul(A, B):
    """Non-BLAS reference matmul (NumPy nditer C loop, no GEMM dispatch)."""
    return np.einsum("ik,kj->ij", A, B, optimize=False)


def run_numpy_kernels() -> int:
    """Localize the broken primitive on the failing (n, rank) cases.

    Compares BLAS GEMM (``A @ Q``) against a non-BLAS einsum reference and checks
    the internal consistency of the LU / QR / SVD factorizations used by the
    randomized-eigsh pipeline. On a correct BLAS all residuals are ~1e-13; on
    macOS arm64 BLIS the broken primitive(s) show a huge residual.
    """
    print(f"=== level=numpy-kernels | flag threshold=1e-6 ===", flush=True)
    rc = 0
    for n, rank in ((100, 10), (100, 80)):
        print(f"--- localization n={n} rank={rank} ---", flush=True)
        A, rng = _make_low_rank_psd(n, rank)
        size = rank + 10
        Q = np.asarray(rng.normal(size=(n, size)))

        # (1) Bare GEMM correctness: BLAS A@Q vs non-BLAS einsum reference.
        C_blas = A @ Q
        C_ref = _einsum_matmul(A, Q)
        gemm_abs = float(np.max(np.abs(C_blas - C_ref)))
        scale = float(np.max(np.abs(C_ref))) or 1.0
        gemm_rel = gemm_abs / scale
        print(f"  [1] GEMM  A@Q : max_abs_err={gemm_abs:.3e}  rel_err={gemm_rel:.3e}", flush=True)

        # (2) LU residual: M = PL @ U (scipy.linalg.lu, permute_l, getrf->BLAS).
        M = A @ Q
        PL, U = linalg.lu(M, permute_l=True, check_finite=False)
        lu_err = float(np.max(np.abs(_einsum_matmul(PL, U) - M)))
        print(f"  [2] LU   A@Q : ||PL@U - M||_max={lu_err:.3e}", flush=True)

        # (3) QR residual + orthonormality (scipy.linalg.qr, geqrf->BLAS).
        Qf, R = linalg.qr(M, mode="economic", check_finite=False)
        qr_err = float(np.max(np.abs(_einsum_matmul(Qf, R) - M)))
        orth_err = float(np.max(np.abs(_einsum_matmul(Qf.T, Qf) - np.eye(Qf.shape[1]))))
        print(
            f"  [3] QR   A@Q : ||Q@R - M||_max={qr_err:.3e}  "
            f"||Q'Q - I||_max={orth_err:.3e}",
            flush=True,
        )

        # (4) SVD residual on the projected matrix B = Qf.T @ A (gesdd->BLAS).
        B = _einsum_matmul(Qf.T, A)
        Uhat, s, Vt = linalg.svd(B, full_matrices=False, lapack_driver="gesdd")
        svd_err = float(np.max(np.abs(_einsum_matmul(Uhat * s, Vt) - B)))
        print(f"  [4] SVD  B   : ||U*s@Vt - B||_max={svd_err:.3e}", flush=True)

        worst = max(gemm_rel, lu_err, qr_err, orth_err, svd_err)
        verdict = "OK" if worst < 1e-6 else "FAIL"
        print(f"  -> {verdict} (worst residual={worst:.3e})", flush=True)
        if worst >= 1e-6:
            rc = 1
    print(("PASS" if rc == 0 else "FAIL") + " [numpy-kernels]", flush=True)
    return rc


def run_sklearn_eigsh() -> int:
    from sklearn.utils.extmath import _randomized_eigsh

    def fn(A, rank, rng):
        return _randomized_eigsh(A, n_components=rank, random_state=rng)

    return _run_eigsh_grid("sklearn-eigsh", fn)


def run_pytest() -> int:
    cmd = [
        sys.executable,
        "-m",
        "pytest",
        "-vs",
        "--no-header",
        "--tb=short",
        "--pyargs",
        "sklearn.utils.tests.test_extmath",
        "-k",
        "test_randomized_eigsh_reconst_low_rank",
    ]
    print("Running:", " ".join(cmd), flush=True)
    return subprocess.call(cmd)


_RUNNERS = {
    "numpy-eigsh": run_numpy_eigsh,
    "numpy-kernels": run_numpy_kernels,
    "sklearn-eigsh": run_sklearn_eigsh,
    "pytest": run_pytest,
}

_DESCRIPTIONS = {
    "numpy-eigsh": "NumPy+SciPy port of _randomized_eigsh (no sklearn)",
    "numpy-kernels": "Localize broken primitive: GEMM vs LU/QR/SVD residuals",
    "sklearn-eigsh": "sklearn.utils.extmath._randomized_eigsh directly",
    "pytest": "upstream test_randomized_eigsh_reconst_low_rank",
}


def _print_backend() -> None:
    """Best-effort report of the NumPy/SciPy BLAS backend in use."""
    import os

    thread_env = {
        k: os.environ.get(k)
        for k in (
            "BLIS_NUM_THREADS",
            "OPENBLAS_NUM_THREADS",
            "OMP_NUM_THREADS",
            "VECLIB_MAXIMUM_THREADS",
        )
        if os.environ.get(k) is not None
    }
    print(f"thread env: {thread_env}", flush=True)
    try:
        cfg = np.show_config(mode="dicts")  # NumPy >= 1.25
        blas = cfg.get("Build Dependencies", {}).get("blas", {})
        print(f"numpy BLAS: name={blas.get('name')} version={blas.get('version')}", flush=True)
    except Exception:
        try:
            np.show_config()
        except Exception:
            pass
    print(f"numpy {np.__version__}", flush=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--level", choices=LEVELS, default="numpy-eigsh")
    parser.add_argument("--list-levels", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.list_levels:
        for name in LEVELS:
            print(f"  {name}: {_DESCRIPTIONS[name]}")
        return 0
    _print_backend()
    return _RUNNERS[args.level]()


if __name__ == "__main__":
    sys.exit(main())
