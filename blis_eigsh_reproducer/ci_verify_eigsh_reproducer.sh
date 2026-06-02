#!/usr/bin/env bash
# CI gate wrapper: run the reproducer and assert the expected outcome per backend.
#   blis                 -> expected to FAIL  (bug reproduced)
#   openblas / accelerate -> expected to PASS (no bug)
set -euo pipefail

if [[ $# -lt 1 ]]; then
    echo "Usage: $0 <blis|openblas|newaccelerate> [level]" >&2
    exit 2
fi

blas_impl="$1"
level="${2:-numpy-eigsh}"
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

set +e
"${script_dir}/run_eigsh_blas_reproducer.sh" "$blas_impl" "$level"
rc=$?
set -e

if [[ "$blas_impl" == "blis" ]]; then
    if [[ "$rc" -eq 0 ]]; then
        echo "Expected level '${level}' to FAIL on BLIS (got exit 0)" >&2
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
