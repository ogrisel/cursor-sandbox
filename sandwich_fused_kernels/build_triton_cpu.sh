#!/usr/bin/env bash
# Build triton-cpu into the Helion venv (experimental CPU backend for Triton).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV="${ROOT}/.venv-helion"
TRITON_CPU="${ROOT}/third_party/triton-cpu"
PY="${VENV}/bin/python"

if [[ ! -x "${PY}" ]]; then
  echo "Helion venv not found at ${VENV}. Create it first (torch + helion)."
  exit 1
fi

if [[ ! -d "${TRITON_CPU}/.git" ]]; then
  echo "Cloning triton-cpu..."
  git clone --depth 1 https://github.com/triton-lang/triton-cpu.git "${TRITON_CPU}"
fi

echo "Updating triton-cpu submodules (sleef, etc.)..."
git -C "${TRITON_CPU}" submodule update --init --recursive

export LIBRARY_PATH="/usr/lib/gcc/x86_64-linux-gnu/13:/usr/lib/x86_64-linux-gnu:${LIBRARY_PATH:-}"
export LDFLAGS="-L/usr/lib/gcc/x86_64-linux-gnu/13"
export CPLUS_INCLUDE_PATH="/usr/include/c++/13:/usr/include/x86_64-linux-gnu/c++/13"
export CXXFLAGS="-I/usr/include/c++/13 -I/usr/include/x86_64-linux-gnu/c++/13"
export TRITON_CPU_BACKEND=1
export MAX_JOBS="${MAX_JOBS:-4}"

uv pip install --python "${PY}" pip setuptools wheel ninja pybind11
"${PY}" -m pip install -r "${TRITON_CPU}/python/requirements.txt"
cd "${TRITON_CPU}"
rm -rf build
"${PY}" -m pip install -e . --no-build-isolation

echo "triton-cpu installed. Verify with:"
echo "  TRITON_CPU_BACKEND=1 ${PY} -c \"import triton.backends; print('cpu' in triton.backends.backends)\""
