#!/usr/bin/env bash
# Diagnostic sweep (BLIS only): create the env once, then run the numpy-eigsh
# reproducer under several BLIS thread counts, each guarded by a wall-clock
# timeout. One CI job tells us, per thread count, whether BLIS:
#   PASS  (exit 0)   -> reconstruction within decimal=6
#   FAIL  (exit 1)   -> numerical reproduction of the upstream bug
#   HANG  (exit 124) -> deadlock (killed by the timeout guard)
# Never fails the job; it only gathers evidence.
set -uo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
env_name="blis-eigsh-sweep"
timeout_secs="${TIMEOUT_SECS:-150}"
level="${LEVEL:-numpy-eigsh}"

if command -v mamba >/dev/null 2>&1; then
    mamba_bin="mamba"
elif command -v micromamba >/dev/null 2>&1; then
    mamba_bin="micromamba"
else
    echo "Neither mamba nor micromamba is available." >&2
    exit 1
fi

pkgs=(python=3.14 numpy scipy "libblas=*=*_blis")
if [[ "$level" != "numpy-eigsh" ]]; then
    pkgs+=(scikit-learn)
fi
if [[ "$level" == "pytest" ]]; then
    pkgs+=(pytest)
fi

echo "Creating env '${env_name}' (level=${level}) ..."
"$mamba_bin" create -y -n "$env_name" "${pkgs[@]}"
build_string="$("$mamba_bin" list -n "$env_name" libblas 2>/dev/null \
    | awk '$1=="libblas"{print $3}')"
echo "Resolved libblas build: ${build_string:-<unknown>}"

# Portable timeout: fork the child, KILL it (and exec'd descendants share the
# pid) on alarm, propagate the real exit code otherwise. Returns 124 on timeout.
run_with_timeout() {
    local secs="$1"
    shift
    perl -e '
        my $s = shift;
        my $pid = fork;
        if ($pid == 0) { exec @ARGV or exit 127; }
        my $rc = 0;
        eval {
            local $SIG{ALRM} = sub { die "timeout\n"; };
            alarm $s;
            waitpid($pid, 0);
            $rc = $? >> 8;
            alarm 0;
        };
        if ($@) { kill "KILL", $pid; waitpid($pid, 0); exit 124; }
        exit $rc;
    ' "$secs" "$@"
}

unset OMP_NUM_THREADS || true
unset OPENBLAS_NUM_THREADS || true
export VECLIB_MAXIMUM_THREADS=1

declare -a results
for t in 1 2 4 8; do
    echo "==================================================================="
    echo "SWEEP BLIS_NUM_THREADS=${t} level=${level} timeout=${timeout_secs}s"
    echo "==================================================================="
    BLIS_NUM_THREADS="$t" run_with_timeout "$timeout_secs" \
        "$mamba_bin" run -n "$env_name" \
        python "${script_dir}/eigsh_blis_reproducer.py" --level "$level"
    rc=$?
    case "$rc" in
        0) verdict="PASS" ;;
        1) verdict="FAIL(numerical-repro)" ;;
        124) verdict="HANG(timeout)" ;;
        *) verdict="ERR(exit=${rc})" ;;
    esac
    echo "sweep[threads=${t}] -> ${verdict}"
    results+=("threads=${t}: ${verdict}")
done

echo "==================================================================="
echo "SWEEP SUMMARY (level=${level}, libblas=${build_string})"
printf '  %s\n' "${results[@]}"
echo "==================================================================="
exit 0
