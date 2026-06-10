#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
XSIMD_INCLUDE="${ROOT}/third_party/xsimd/include"
OUT="${ROOT}/xsimd_ext/libsandwich_xsimd.so"
SRC="${ROOT}/xsimd_ext/sandwich_xsimd.cpp"

if [[ ! -f "${XSIMD_INCLUDE}/xsimd/xsimd.hpp" ]]; then
  echo "Fetching xsimd headers..."
  git clone --depth 1 --branch 13.2.0 https://github.com/xtensor-stack/xsimd.git "${ROOT}/third_party/xsimd"
fi

g++ -O3 -march=native -shared -fPIC -fopenmp -std=c++17 \
  -I"${XSIMD_INCLUDE}" \
  -o "${OUT}" \
  "${SRC}"

echo "Built ${OUT}"
