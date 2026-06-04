#!/usr/bin/env bash
# Run the fixed-data Python reproducer against a selected conda BLAS.
set -euo pipefail

if [[ $# -lt 1 ]]; then
    echo "Usage: $0 <blis|openblas|newaccelerate>" >&2
    exit 2
fi

blas_impl="$1"
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
env_name="blis-eigsh-python-${blas_impl}"

if command -v mamba >/dev/null 2>&1; then
    mamba_bin="mamba"
elif command -v micromamba >/dev/null 2>&1; then
    mamba_bin="micromamba"
else
    echo "Neither mamba nor micromamba is available." >&2
    exit 1
fi

"$mamba_bin" create -y -n "$env_name" python=3.14 numpy threadpoolctl "libblas=*=*_${blas_impl}"
build_string="$("$mamba_bin" list -n "$env_name" libblas 2>/dev/null | awk '$1=="libblas"{print $3}')"
echo "Resolved libblas build: ${build_string:-<unknown>}"

unset OMP_NUM_THREADS || true
export VECLIB_MAXIMUM_THREADS=1
if [[ "$blas_impl" == "blis" ]]; then
    export BLIS_NUM_THREADS="${BLIS_NUM_THREADS:-1}"
    unset OPENBLAS_NUM_THREADS || true
elif [[ "$blas_impl" == "openblas" ]]; then
    export OPENBLAS_NUM_THREADS="${OPENBLAS_NUM_THREADS:-1}"
    unset BLIS_NUM_THREADS || true
else
    unset OPENBLAS_NUM_THREADS BLIS_NUM_THREADS || true
fi

echo "threadpoolctl -i numpy:"
"$mamba_bin" run -n "$env_name" python -m threadpoolctl -i numpy

set +e
"$mamba_bin" run -n "$env_name" python "${script_dir}/minimal_gemm_repro.py"
rc=$?
set -e

if [[ "$blas_impl" == "blis" ]]; then
    if [[ "$rc" -eq 0 ]]; then
        echo "Expected fixed-data Python reproducer to FAIL on BLIS (got exit 0)" >&2
        exit 1
    fi
    echo "OK: fixed-data Python reproducer failed as expected on BLIS (exit ${rc})"
    exit 0
fi

if [[ "$rc" -ne 0 ]]; then
    echo "Expected fixed-data Python reproducer to PASS on ${blas_impl} (got exit ${rc})" >&2
    exit 1
fi
echo "OK: fixed-data Python reproducer passed on ${blas_impl}"
