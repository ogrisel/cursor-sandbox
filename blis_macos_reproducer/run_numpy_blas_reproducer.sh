#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
    echo "Usage: $0 <blis|openblas|newaccelerate>" >&2
    exit 2
fi

blas_impl="$1"
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
env_name="blis-repro"

if command -v mamba >/dev/null 2>&1; then
    mamba_bin="mamba"
elif command -v micromamba >/dev/null 2>&1; then
    mamba_bin="micromamba"
else
    echo "Neither mamba nor micromamba is available." >&2
    exit 1
fi

echo "Creating env '${env_name}' with libblas=*=*_${blas_impl} ..."
"$mamba_bin" create -y -n "$env_name" numpy "libblas=*=*_${blas_impl}"

export OMP_NUM_THREADS=1
export VECLIB_MAXIMUM_THREADS=1

if [[ "$blas_impl" == "blis" ]]; then
    export BLIS_NUM_THREADS=8
    unset OPENBLAS_NUM_THREADS
elif [[ "$blas_impl" == "openblas" ]]; then
    export OPENBLAS_NUM_THREADS=8
    unset BLIS_NUM_THREADS
else
    unset OPENBLAS_NUM_THREADS
    unset BLIS_NUM_THREADS
fi

"$mamba_bin" run -n "$env_name" \
    python "${script_dir}/numpy_blis_reproducer.py" --expected-blas "$blas_impl"
