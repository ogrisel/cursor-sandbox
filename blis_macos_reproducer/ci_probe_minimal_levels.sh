#!/usr/bin/env bash
# Run every minimal level on BLIS and print which ones fail (CI diagnostics).
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
levels=(knn-imputer-only scalar-vs-imputer scalar-full-matrix sklearn-dist-vs-imputer pytest numpy-gemm)

echo "=== Minimal reproducer level probe (BLIS) ==="
for level in "${levels[@]}"; do
    echo "--- ${level} ---"
    set +e
    "${script_dir}/run_minimal_blas_reproducer.sh" blis "$level"
    rc=$?
    set -e
    if [[ "$rc" -eq 0 ]]; then
        echo "result: PASS"
    else
        echo "result: FAIL (exit ${rc})"
    fi
done
