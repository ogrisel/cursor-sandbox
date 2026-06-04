#!/usr/bin/env bash
# Run every minimal fixed-data variant of the V@diag(S)@V.T reproducer, each in
# its own fresh process, on the requested backend. Informational: prints which
# variant(s) reproduce the BLIS corruption from fixed data (no power iterations).
set -uo pipefail

if [[ $# -lt 1 ]]; then
    echo "Usage: $0 <blis|openblas|newaccelerate>" >&2
    exit 2
fi

blas_impl="$1"
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
env_name="blis-eigsh-mingemm"

if command -v mamba >/dev/null 2>&1; then
    mamba_bin="mamba"
elif command -v micromamba >/dev/null 2>&1; then
    mamba_bin="micromamba"
else
    echo "Neither mamba nor micromamba is available." >&2
    exit 1
fi

"$mamba_bin" create -y -n "$env_name" python=3.14 numpy scipy "libblas=*=*_${blas_impl}"
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

declare -a summary
for variant in single gemm-prequel svd-prequel eigsh-prequel contig-vt fortran-v strided-view; do
    echo "==================================================================="
    "$mamba_bin" run -n "$env_name" \
        python "${script_dir}/minimal_gemm_repro.py" --variant "$variant"
    rc=$?
    if [[ "$rc" -eq 0 ]]; then
        summary+=("${variant}: PASS (no repro)")
    else
        summary+=("${variant}: FAIL (bug reproduced)")
    fi
done

echo "==================================================================="
echo "MINIMAL GEMM VARIANT SUMMARY (backend=${blas_impl}, libblas=${build_string})"
printf '  %s\n' "${summary[@]}"
echo "==================================================================="
exit 0
