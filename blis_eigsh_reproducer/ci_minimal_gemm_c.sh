#!/usr/bin/env bash
# Build and run the fixed-data C reproducer against a selected conda BLAS.
set -euo pipefail

if [[ $# -lt 1 ]]; then
    echo "Usage: $0 <blis|openblas|newaccelerate>" >&2
    exit 2
fi

blas_impl="$1"
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
env_name="blis-eigsh-c-${blas_impl}"

if command -v mamba >/dev/null 2>&1; then
    mamba_bin="mamba"
elif command -v micromamba >/dev/null 2>&1; then
    mamba_bin="micromamba"
else
    echo "Neither mamba nor micromamba is available." >&2
    exit 1
fi

"$mamba_bin" create -y -n "$env_name" "libblas=*=*_${blas_impl}" libcblas
build_string="$("$mamba_bin" list -n "$env_name" libblas 2>/dev/null | awk '$1=="libblas"{print $3}')"
echo "Resolved libblas build: ${build_string:-<unknown>}"

prefix="$("$mamba_bin" run -n "$env_name" sh -c 'printf "%s" "$CONDA_PREFIX"')"
cc_bin="${CC:-cc}"
bin="${script_dir}/minimal_gemm_repro_c"

echo "Compiling with ${cc_bin} against ${prefix} ..."
set +e
"$cc_bin" -O2 -std=c99 \
    -I"${prefix}/include" \
    -L"${prefix}/lib" \
    -Wl,-rpath,"${prefix}/lib" \
    "${script_dir}/minimal_gemm_repro.c" \
    -lcblas -lblas -lm \
    -o "$bin"
compile_rc=$?
if [[ "$compile_rc" -ne 0 ]]; then
    echo "Retrying without -lcblas (some BLAS builds expose CBLAS from libblas) ..."
    "$cc_bin" -O2 -std=c99 \
        -I"${prefix}/include" \
        -L"${prefix}/lib" \
        -Wl,-rpath,"${prefix}/lib" \
        "${script_dir}/minimal_gemm_repro.c" \
        -lblas -lm \
        -o "$bin"
    compile_rc=$?
fi
set -e
if [[ "$compile_rc" -ne 0 ]]; then
    echo "ERROR: failed to compile/link the fixed-data C reproducer" >&2
    exit 2
fi

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

set +e
"$bin" "${script_dir}/fixtures"
rc=$?
set -e

if [[ "$blas_impl" == "blis" ]]; then
    if [[ "$rc" -eq 0 ]]; then
        echo "Expected fixed-data C reproducer to FAIL on BLIS (got exit 0)" >&2
        exit 1
    fi
    echo "OK: fixed-data C reproducer failed as expected on BLIS (exit ${rc})"
    exit 0
fi

if [[ "$rc" -ne 0 ]]; then
    echo "Expected fixed-data C reproducer to PASS on ${blas_impl} (got exit ${rc})" >&2
    exit 1
fi
echo "OK: fixed-data C reproducer passed on ${blas_impl}"
