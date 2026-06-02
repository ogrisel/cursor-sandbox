#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
    echo "Usage: $0 <blis|openblas|newaccelerate> [level]" >&2
    echo "  Delegates to run_minimal_blas_reproducer.sh (default: scalar-vs-imputer)." >&2
    echo "  Use level=pytest for the full upstream pytest subset." >&2
    exit 2
fi

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
level="${2:-scalar-vs-imputer}"
exec "${script_dir}/run_minimal_blas_reproducer.sh" "$1" "$level"
