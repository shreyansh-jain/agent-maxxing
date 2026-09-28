#!/usr/bin/env bash
# Run one test command serially N times and report the failure rate.
# Usage: bash rerun_until_fail.sh <runs> <command...>
#   STOP_ON_FAIL=1  stop at the first failure
#   OUT_DIR=<dir>   where failing outputs are saved (default: a new temp dir)
# Pass a single spec file with the runner's serial flag, e.g.
#   bash rerun_until_fail.sh 50 npx jest --runInBand path/to/one.test.ts
set -uo pipefail

if [ "$#" -lt 2 ] || ! [[ "$1" =~ ^[0-9]+$ ]]; then
  echo "usage: bash rerun_until_fail.sh <runs> <command...>" >&2
  exit 2
fi

runs="$1"; shift
out_dir="${OUT_DIR:-$(mktemp -d -t flaky-XXXXXX)}"
mkdir -p "$out_dir"
fails=0

for i in $(seq 1 "$runs"); do
  log="$out_dir/run-$i.log"
  if "$@" >"$log" 2>&1; then
    rm -f "$log"
    printf '.'
  else
    fails=$((fails + 1))
    printf 'F'
    if [ "${STOP_ON_FAIL:-0}" = "1" ]; then
      echo
      echo "first failure on run $i; output: $log"
      exit 1
    fi
  fi
done

echo
echo "failed $fails/$runs runs"
if [ "$fails" -gt 0 ]; then
  echo "failing outputs kept in $out_dir"
  exit 1
fi
rmdir "$out_dir" 2>/dev/null || true
