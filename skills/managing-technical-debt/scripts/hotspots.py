#!/usr/bin/env python3
"""Rank files by change frequency x size to find technical-debt hotspots.

Files that change often AND are large are where debt costs the most: every
change pays interest on their complexity. Run from inside a git repository.

Usage:
  python3 hotspots.py                      # last 12 months, top 20
  python3 hotspots.py --since "6 months ago" --top 30
  python3 hotspots.py --path src/ --exclude test --exclude .lock
  python3 hotspots.py --csv > hotspots.csv

Score = commits touching the file in the window x current line count.
Line count is a crude size proxy; confirm top hits with a real complexity
tool before acting. Exit code: 0 ok, 2 not a git repo or bad arguments.
"""
import argparse
import csv
import subprocess
import sys
from collections import Counter
from pathlib import Path


def git(args, cwd):
    result = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f"git {' '.join(args)} failed")
    return result.stdout


def count_lines(path):
    try:
        with open(path, "rb") as handle:
            data = handle.read()
    except OSError:
        return None
    if b"\0" in data[:8192]:
        return None
    return data.count(b"\n") + (1 if data and not data.endswith(b"\n") else 0)


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--since", default="12 months ago", help="git --since window (default: 12 months ago)")
    parser.add_argument("--top", type=int, default=20, help="number of files to show (default: 20)")
    parser.add_argument("--path", default=".", help="limit to this path within the repo")
    parser.add_argument("--exclude", action="append", default=[], help="skip files whose path contains this substring (repeatable)")
    parser.add_argument("--min-commits", type=int, default=2, help="ignore files changed fewer times (default: 2)")
    parser.add_argument("--csv", action="store_true", help="write CSV to stdout instead of a table")
    args = parser.parse_args()

    if args.top < 1 or args.min_commits < 1:
        parser.error("--top and --min-commits must be >= 1")

    try:
        root = Path(git(["rev-parse", "--show-toplevel"], cwd=".").strip())
        log = git(
            ["log", f"--since={args.since}", "--no-merges", "--name-only", "--format=", "--", args.path],
            cwd=".",
        )
    except (RuntimeError, FileNotFoundError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    churn = Counter(line.strip() for line in log.splitlines() if line.strip())
    rows = []
    for rel, commits in churn.items():
        if commits < args.min_commits or any(token in rel for token in args.exclude):
            continue
        lines = count_lines(root / rel)
        if lines is None:
            continue
        rows.append((commits * lines, commits, lines, rel))

    rows.sort(reverse=True)
    rows = rows[: args.top]
    if not rows:
        print(f"no files changed >= {args.min_commits} times since {args.since}", file=sys.stderr)
        return 0

    if args.csv:
        writer = csv.writer(sys.stdout)
        writer.writerow(["score", "commits", "lines", "path"])
        writer.writerows(rows)
        return 0

    print(f"Hotspots since {args.since} (score = commits x lines)\n")
    print(f"{'score':>10} {'commits':>8} {'lines':>7}  path")
    for score, commits, lines, rel in rows:
        print(f"{score:>10} {commits:>8} {lines:>7}  {rel}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
