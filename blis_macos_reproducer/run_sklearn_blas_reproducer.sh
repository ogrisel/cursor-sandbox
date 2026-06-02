#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
    echo "Usage: $0 <blis|openblas|newaccelerate> [pytest|pairwise]" >&2
    exit 2
fi

blas_impl="$1"
mode="${2:-pytest}"
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
env_name="blis-repro-sklearn"

if command -v mamba >/dev/null 2>&1; then
    mamba_bin="mamba"
elif command -v micromamba >/dev/null 2>&1; then
    mamba_bin="micromamba"
else
    echo "Neither mamba nor micromamba is available." >&2
    exit 1
fi

echo "Creating env '${env_name}' (python=3.14, sklearn, libblas=${blas_impl}) ..."
"$mamba_bin" create -y -n "$env_name" \
    python=3.14 \
    numpy scipy scikit-learn pytest joblib threadpoolctl \
    "libblas=*=*_${blas_impl}"

# Do not cap OMP_NUM_THREADS=1 for BLIS: sklearn macOS CI keeps BLAS threaded.
unset OMP_NUM_THREADS
export VECLIB_MAXIMUM_THREADS="${VECLIB_MAXIMUM_THREADS:-1}"

if [[ "$blas_impl" == "blis" ]]; then
    export BLIS_NUM_THREADS="${BLIS_NUM_THREADS:-8}"
    unset OPENBLAS_NUM_THREADS
elif [[ "$blas_impl" == "openblas" ]]; then
    export OPENBLAS_NUM_THREADS="${OPENBLAS_NUM_THREADS:-8}"
    unset BLIS_NUM_THREADS
else
    unset OPENBLAS_NUM_THREADS
    unset BLIS_NUM_THREADS
fi

if [[ "$mode" == "pairwise" ]]; then
    script="${script_dir}/sklearn_pairwise_blis_reproducer.py"
else
    script="${script_dir}/sklearn_knn_blis_reproducer.py"
fi

"$mamba_bin" run -n "$env_name" python "$script"
