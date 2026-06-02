#!/usr/bin/env bash
set -euo pipefail

# Back-compat alias for ci_verify_minimal_reproducer.sh
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
level="${2:-scalar-vs-imputer}"
exec "${script_dir}/ci_verify_minimal_reproducer.sh" "$1" "$level"
