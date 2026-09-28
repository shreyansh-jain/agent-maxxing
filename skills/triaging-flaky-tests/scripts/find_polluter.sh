#!/usr/bin/env bash
# Find which spec file leaks state into a victim spec: run each candidate
# followed by the victim, one pair at a time, serially.
# Usage: bash find_polluter.sh "<runner command>" <victim-spec> <candidate-spec>...
#   The runner must accept several files and run them in order in one process, e.g.
#   "npx jest --runInBand --testSequencer=./ordered-sequencer.js"  or  "python -m pytest -p no:randomly"
#   REPEAT=<n>  run each pair n times (default 3), for polluters that only leak sometimes
set -uo pipefail

if [ "$#" -lt 3 ]; then
  echo 'usage: bash find_polluter.sh "<runner command>" <victim-spec> <candidate-spec>...' >&2
  exit 2
fi

runner="$1"; victim="$2"; shift 2
repeat="${REPEAT:-3}"
read -r -a runner_argv <<<"$runner"

if ! "${runner_argv[@]}" "$victim" >/dev/null 2>&1; then
  echo "victim fails on its own; this is not order dependence: $victim" >&2
  exit 2
fi

found=0
for candidate in "$@"; do
  [ "$candidate" = "$victim" ] && continue
  for _ in $(seq 1 "$repeat"); do
    if ! "${runner_argv[@]}" "$candidate" "$victim" >/dev/null 2>&1; then
      if "${runner_argv[@]}" "$candidate" >/dev/null 2>&1; then
        echo "POLLUTER: $candidate  (victim fails when run after it)"
        found=1
      else
        echo "SKIP: $candidate fails on its own, pair result is inconclusive"
      fi
      break
    fi
  done
done

[ "$found" = 1 ] || echo "no single polluter found among $# candidates; suspect a combination, or a shared resource outside the process"
