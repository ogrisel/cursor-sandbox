#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
    echo "Usage: $0 <blis|openblas|newaccelerate> [level]" >&2
    exit 2
fi

blas_impl="$1"
level="${2:-scalar-vs-imputer}"
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

set +e
"${script_dir}/run_minimal_blas_reproducer.sh" "$blas_impl" "$level"
rc=$?
set -e

# numpy-gemm is informational: BLIS may pass while scalar-vs-imputer fails.
if [[ "$level" == "numpy-gemm" ]]; then
    echo "OK: numpy-gemm finished (exit ${rc}); not used as BLIS gate"
    exit 0
fi

if [[ "$blas_impl" == "blis" ]]; then
    if [[ "$rc" -eq 0 ]]; then
        echo "Expected level '${level}' to FAIL with BLIS (got exit 0)" >&2
        exit 1
    fi
    echo "OK: level '${level}' failed as expected on BLIS (exit ${rc})"
    exit 0
fi

if [[ "$rc" -ne 0 ]]; then
    echo "Expected level '${level}' to PASS with ${blas_impl} (got exit ${rc})" >&2
    exit 1
fi
echo "OK: level '${level}' passed with ${blas_impl}"
exit 0
