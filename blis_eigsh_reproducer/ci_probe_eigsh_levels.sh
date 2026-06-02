#!/usr/bin/env bash
# Informational probe: run every level on BLIS in a single job so one CI run
# reveals whether the bug reproduces at each level (pytest -> sklearn -> numpy)
# and how large the reconstruction error gets per (n, rank) case.
# Never fails the job; it only gathers evidence to drive simplification.
set -uo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

for level in pytest sklearn-eigsh numpy-eigsh; do
    echo "==================================================================="
    echo "PROBE level=${level} backend=blis"
    echo "==================================================================="
    "${script_dir}/run_eigsh_blas_reproducer.sh" blis "$level"
    echo "probe[${level}] exit=$?"
done
exit 0
