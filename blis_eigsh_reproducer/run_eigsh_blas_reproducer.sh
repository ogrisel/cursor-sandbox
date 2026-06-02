#!/usr/bin/env bash
# Create a dedicated (micro)mamba env pinned to a specific conda libblas build
# (blis / openblas / newaccelerate) and run the randomized-eigsh reproducer.
set -euo pipefail

if [[ $# -lt 1 ]]; then
    echo "Usage: $0 <blis|openblas|newaccelerate> [level]" >&2
    echo "  level: numpy-eigsh (default) | sklearn-eigsh | pytest" >&2
    exit 2
fi

blas_impl="$1"
level="${2:-numpy-eigsh}"
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
env_name="blis-eigsh-${blas_impl}"

if command -v mamba >/dev/null 2>&1; then
    mamba_bin="mamba"
elif command -v micromamba >/dev/null 2>&1; then
    mamba_bin="micromamba"
else
    echo "Neither mamba nor micromamba is available." >&2
    exit 1
fi

# numpy-eigsh / numpy-kernels are self-contained (numpy + scipy only); the
# sklearn levels need scikit-learn (and pytest for the upstream-test level).
pkgs=(python=3.14 numpy scipy "libblas=*=*_${blas_impl}")
if [[ "$level" == "sklearn-eigsh" || "$level" == "pytest" ]]; then
    pkgs+=(scikit-learn)
fi
if [[ "$level" == "pytest" ]]; then
    pkgs+=(pytest)
fi

echo "Creating env '${env_name}' for level=${level} libblas=${blas_impl} ..."
"$mamba_bin" create -y -n "$env_name" "${pkgs[@]}"

# Confirm the conda libblas build string actually matches the requested backend
# (NumPy 2.x reports a generic name in __config__, so check conda metadata).
build_string="$("$mamba_bin" list -n "$env_name" libblas 2>/dev/null \
    | awk '$1=="libblas"{print $3}')"
echo "Resolved libblas build: ${build_string:-<unknown>}"
if [[ -n "$build_string" && "$build_string" != *"_${blas_impl}" ]]; then
    echo "ERROR: requested ${blas_impl} but libblas build is ${build_string}" >&2
    exit 1
fi

# Threading: the randomized-eigsh numerical corruption reproduces
# *deterministically* with a single BLIS thread, so default to 1 thread for a
# clean, reproducible gate. (With BLIS_NUM_THREADS>=4 macOS arm64 BLIS also
# deadlocks on these matrices -- a separate bug -- see README / sweep script.)
unset OMP_NUM_THREADS || true
export VECLIB_MAXIMUM_THREADS="${VECLIB_MAXIMUM_THREADS:-1}"
if [[ "$blas_impl" == "blis" ]]; then
    export BLIS_NUM_THREADS="${BLIS_NUM_THREADS:-1}"
    unset OPENBLAS_NUM_THREADS || true
elif [[ "$blas_impl" == "openblas" ]]; then
    export OPENBLAS_NUM_THREADS="${OPENBLAS_NUM_THREADS:-1}"
    unset BLIS_NUM_THREADS || true
else
    unset OPENBLAS_NUM_THREADS || true
    unset BLIS_NUM_THREADS || true
fi

"$mamba_bin" run -n "$env_name" \
    python "${script_dir}/eigsh_blis_reproducer.py" --level "$level"
