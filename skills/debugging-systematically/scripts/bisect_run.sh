#!/usr/bin/env bash
# Find the first bad commit between a known-good and known-bad ref.
# Usage: bash bisect_run.sh <good-ref> <bad-ref> <command...>
# <command> must exit 0 on good, 1-124 on bad, 125 to skip an unbuildable commit.
set -euo pipefail

if [ "$#" -lt 3 ]; then
  echo "usage: bash bisect_run.sh <good-ref> <bad-ref> <command...>" >&2
  exit 2
fi

good="$1"; bad="$2"; shift 2

if [ -n "$(git status --porcelain --untracked-files=no)" ]; then
  echo "working tree has uncommitted changes; stash or commit them before bisecting" >&2
  exit 2
fi

git rev-parse --verify --quiet "$good^{commit}" >/dev/null || { echo "unknown good ref: $good" >&2; exit 2; }
git rev-parse --verify --quiet "$bad^{commit}" >/dev/null || { echo "unknown bad ref: $bad" >&2; exit 2; }

start_ref="$(git symbolic-ref --quiet --short HEAD || git rev-parse HEAD)"
trap 'git bisect reset "$start_ref" >/dev/null 2>&1 || true' EXIT

git bisect start "$bad" "$good" >/dev/null
git bisect run "$@"
git bisect log | tail -n 5
