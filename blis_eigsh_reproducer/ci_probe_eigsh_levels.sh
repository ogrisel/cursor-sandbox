#!/usr/bin/env bash
# Informational probe on BLIS (single-threaded, deterministic): localize the
# broken primitive, then show that every level reproduces the same failure.
# Never fails the job; it only gathers evidence.
set -uo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

for level in numpy-kernels numpy-eigsh sklearn-eigsh pytest; do
    echo "==================================================================="
    echo "PROBE level=${level} backend=blis"
    echo "==================================================================="
    "${script_dir}/run_eigsh_blas_reproducer.sh" blis "$level"
    echo "probe[${level}] exit=$?"
done
exit 0
