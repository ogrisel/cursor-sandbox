#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
    echo "Usage: $0 <blis|openblas|newaccelerate> [pytest|pairwise]" >&2
    exit 2
fi

blas_impl="$1"
mode="${2:-pytest}"
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

set +e
"${script_dir}/run_sklearn_blas_reproducer.sh" "$blas_impl" "$mode"
rc=$?
set -e

if [[ "$blas_impl" == "blis" ]]; then
    if [[ "$rc" -eq 0 ]]; then
        echo "Expected sklearn reproducer to FAIL with BLIS (got exit 0)" >&2
        exit 1
    fi
    echo "OK: sklearn reproducer failed as expected (exit ${rc})"
    exit 0
fi

if [[ "$rc" -ne 0 ]]; then
    echo "Expected sklearn reproducer to PASS with ${blas_impl} (got exit ${rc})" >&2
    exit 1
fi
echo "OK: sklearn reproducer passed with ${blas_impl}"
exit 0
