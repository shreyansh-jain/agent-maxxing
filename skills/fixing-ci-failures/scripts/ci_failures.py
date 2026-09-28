#!/usr/bin/env python3
"""List failing GitHub Actions checks and show the first error lines of each failed job log.

Usage:
  python3 ci_failures.py              # PR for the current branch
  python3 ci_failures.py --pr 123     # a specific PR number or URL
  python3 ci_failures.py --context 20 # lines of log shown around the first error

Requires an authenticated GitHub CLI (`gh auth status`). Non-Actions checks are
listed with their URL only. Exit code: 0 no failures, 1 failures found, 2 usage/setup error.
"""
import argparse
import json
import re
import subprocess
import sys

ERROR_RE = re.compile(r"(error|failed|failure|exception|traceback|assert|fatal|panic|✗|✕)", re.I)
FAILING_STATES = {"FAILURE", "ERROR", "CANCELLED", "TIMED_OUT", "ACTION_REQUIRED", "STARTUP_FAILURE"}
RUN_ID_RE = re.compile(r"/actions/runs/(\d+)")


def gh(*args):
    result = subprocess.run(["gh", *args], capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f"gh {' '.join(args)} failed")
    return result.stdout


def failing_checks(pr):
    args = ["gh", "pr", "checks", "--json", "name,state,link,workflow"]
    if pr:
        args.insert(3, pr)
    # `gh pr checks` exits non-zero when any check fails or is pending, so judge success by the JSON.
    result = subprocess.run(args, capture_output=True, text=True)
    try:
        checks = json.loads(result.stdout)
    except json.JSONDecodeError:
        print(f"could not list checks: {result.stderr.strip()}", file=sys.stderr)
        sys.exit(2)
    return [c for c in checks if c.get("state", "").upper() in FAILING_STATES]


def first_error(log, context):
    lines = log.splitlines()
    for i, line in enumerate(lines):
        if ERROR_RE.search(line):
            start = max(0, i - 2)
            return "\n".join(lines[start:start + context])
    return "\n".join(lines[-context:])


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--pr", help="PR number or URL (default: current branch)")
    parser.add_argument("--context", type=int, default=15, help="log lines to show per failure")
    opts = parser.parse_args()

    try:
        gh("auth", "status")
    except (RuntimeError, FileNotFoundError) as exc:
        print(f"gh is not installed or not authenticated: {exc}", file=sys.stderr)
        sys.exit(2)

    failures = failing_checks(opts.pr)
    if not failures:
        print("No failing checks.")
        sys.exit(0)

    seen_runs = set()
    for check in failures:
        link = check.get("link") or ""
        print(f"== {check.get('workflow') or '?'} / {check['name']}: {check['state']}\n   {link}")
        match = RUN_ID_RE.search(link)
        if not match:
            print("   (not a GitHub Actions run; open the link for logs)\n")
            continue
        run_id = match.group(1)
        if run_id in seen_runs:
            print("   (log shown above for this run)\n")
            continue
        seen_runs.add(run_id)
        try:
            log = gh("run", "view", run_id, "--log-failed")
        except RuntimeError as exc:
            print(f"   could not fetch log: {exc}\n")
            continue
        snippet = first_error(log, opts.context)
        print("   " + snippet.replace("\n", "\n   ") + "\n")
    sys.exit(1)


if __name__ == "__main__":
    main()
