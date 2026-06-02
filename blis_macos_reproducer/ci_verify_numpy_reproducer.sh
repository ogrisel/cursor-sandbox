#!/usr/bin/env bash
# CI helper: while the BLIS bug is present, only the blis env should fail the reproducer.
set -euo pipefail

if [[ $# -lt 1 ]]; then
    echo "Usage: $0 <blis|openblas|newaccelerate>" >&2
    exit 2
fi

blas_impl="$1"
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

set +e
"${script_dir}/run_numpy_blas_reproducer.sh" "$blas_impl"
rc=$?
set -e

if [[ "$blas_impl" == "blis" ]]; then
    if [[ "$rc" -eq 0 ]]; then
        echo "Expected reproducer to FAIL with BLIS (got exit 0)" >&2
        exit 1
    fi
    echo "OK: BLIS reproducer failed as expected (exit ${rc})"
    exit 0
fi

if [[ "$rc" -ne 0 ]]; then
    echo "Expected reproducer to PASS with ${blas_impl} (got exit ${rc})" >&2
    exit 1
fi
echo "OK: ${blas_impl} reproducer passed"
exit 0
