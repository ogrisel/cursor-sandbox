#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
blis_version="${BLIS_VERSION:-2.0}"
workdir="${RUNNER_TEMP:-/tmp}/blis-c-repro"

rm -rf "$workdir"
mkdir -p "$workdir"
cd "$workdir"

echo "Downloading BLIS ${blis_version} ..."
curl -fsSL -o blis.tar.gz "https://github.com/flame/blis/archive/refs/tags/${blis_version}.tar.gz"
tar -xzf blis.tar.gz
cd "blis-${blis_version}"

./configure --enable-cblas auto
if command -v nproc >/dev/null 2>&1; then
    n_jobs="$(nproc)"
else
    n_jobs="$(sysctl -n hw.ncpu)"
fi
make -j"${n_jobs}"

lib_dir="$(find "$workdir/blis-${blis_version}/lib" -mindepth 1 -maxdepth 1 -type d | head -n 1)"
if [[ -z "${lib_dir}" ]]; then
    echo "Unable to locate BLIS library directory" >&2
    exit 1
fi

arch_name="$(basename "$lib_dir")"
include_dir="$workdir/blis-${blis_version}/include/$arch_name"
if [[ ! -d "$include_dir" ]]; then
    include_dir="$workdir/blis-${blis_version}/include"
fi

cblas_include="$workdir/blis-${blis_version}/build"

cc \
    -O2 \
    -I"$cblas_include" \
    -I"$include_dir" \
    -I"$include_dir/blis" \
    -I"$workdir/blis-${blis_version}/include" \
    -I"$workdir/blis-${blis_version}" \
    "${script_dir}/blis_gemm_reproducer.c" \
    -L"$lib_dir" \
    -lblis -lm \
    -Wl,-rpath,"$lib_dir" \
    -o "$workdir/blis_gemm_reproducer"

export BLIS_NUM_THREADS=8
export OMP_NUM_THREADS=1
export DYLD_LIBRARY_PATH="${lib_dir}:${DYLD_LIBRARY_PATH:-}"
"$workdir/blis_gemm_reproducer"
