#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
    echo "Usage: $0 <blis|openblas|newaccelerate> [level]" >&2
    echo "  level: $(cd "$(dirname "$0")" && python minimal_blis_reproducer.py --list-levels 2>/dev/null || echo 'scalar-vs-imputer')" >&2
    exit 2
fi

blas_impl="$1"
level="${2:-scalar-vs-imputer}"
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
env_name="blis-repro-minimal"

if command -v mamba >/dev/null 2>&1; then
    mamba_bin="mamba"
elif command -v micromamba >/dev/null 2>&1; then
    mamba_bin="micromamba"
else
    echo "Neither mamba nor micromamba is available." >&2
    exit 1
fi

pkgs=(python=3.14 numpy "libblas=*=*_${blas_impl}")
if [[ "$level" != "numpy-gemm" ]]; then
    pkgs+=(scipy scikit-learn)
fi
if [[ "$level" == "pytest" ]]; then
    pkgs+=(pytest)
fi

echo "Creating env '${env_name}' for level=${level} libblas=${blas_impl} ..."
"$mamba_bin" create -y -n "$env_name" "${pkgs[@]}"

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

"$mamba_bin" run -n "$env_name" \
    python "${script_dir}/minimal_blis_reproducer.py" --level "$level"
