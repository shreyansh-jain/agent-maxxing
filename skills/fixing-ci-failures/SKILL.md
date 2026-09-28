---
name: fixing-ci-failures
description: Triage and repair of failing CI checks and pipelines. Use when a pull request has red checks, a GitHub Actions / GitLab CI / CircleCI / Buildkite job fails, main went red after a merge, a build passes locally but fails in CI, or a pipeline config needs fixing.
license: Apache-2.0
metadata:
  version: "0.1.0"
  category: "ship"
  sources: "openai/skills gh-fix-ci (Apache-2.0); getsentry/skills iterate-pr (Apache-2.0); addyosmani/agent-skills ci-cd-and-automation (MIT)"
---

# Fixing CI Failures

The job log is the evidence. Read the first real error, reproduce the exact CI command locally, fix the cause, and never make a check green by weakening it.

## When to use

- A PR shows failing checks
- `main` or a release branch went red after a merge
- "Works on my machine" but not in CI
- A workflow file, cache, matrix or runner configuration is broken

**Not for:** a test that fails intermittently with no code change (use `triaging-flaky-tests`); a bug the CI surfaced that needs deep investigation (use `debugging-systematically` once you have the failing command); a CI failure caused by a dependency bump (use `upgrading-dependencies`).

## The rule

```
NEVER MAKE CI GREEN BY SKIPPING, DELETING, OR SOFTENING A CHECK
```

Violating the letter of the rule is violating the spirit of the rule. `continue-on-error`, `|| true`, `.skip`, raised thresholds, deleted assertions and `--no-verify` all count.

## Process

1. **Collect the failures.** Run `python3 scripts/ci_failures.py [--pr N]` (it needs an authenticated `gh`), or list them by hand: `gh pr checks <pr>`, then `gh run view <run-id> --log-failed`. For other CI providers, open the job's log URL, and ask the user for the log if you can't reach it.
   Exit: for each failing job you have its name, its run URL, and the first error line. That means the first error, not the last line of the log.

2. **Classify each failure.** Put each one into one of four buckets:
   - **Regression**: the diff broke something. The same job passes on the base branch.
   - **Environment drift**: the base branch now fails too. Causes include a new runner image, an unpinned tool or dependency, an expired secret, or a changed external service.
   - **Flaky**: a re-run of the same commit passes. Hand it to `triaging-flaky-tests`; don't paper over it.
   - **Config**: the workflow YAML, cache key, matrix, path filter or permissions are wrong.
   To tell them apart, compare against the last green run on the base branch (`gh run list --branch main --workflow <wf> --limit 5`).
   Exit: every failure has a bucket and the evidence for it.

3. **Reproduce the exact command locally.** Copy the job's `run:` step and use the same tool versions (read them from the workflow, `.tool-versions`, `.nvmrc`, or the lockfile). Run only the failing target, such as one test file or one lint rule, not the whole suite.
   Exit: the local command fails the same way. If the failure only happens in CI, list the differences between CI and local: OS, versions, env vars, secrets, services, parallelism.

4. **Propose the fix before applying it.** Tell the user the cause, the bucket, and the smallest fix. Examples: fix the code; pin the drifting tool; correct the cache key; add the missing service container. If the user has already asked you to go ahead and fix it, proceed. Otherwise wait.

5. **Fix and verify locally.** Apply the fix, then re-run the reproduced command and show that it passes. For config fixes, validate the YAML (for example `actionlint` if it is installed) and check that nothing else changed its behaviour, such as triggers, permissions or secrets exposure.
   Exit: the local repro passes, and the diff contains no skips or softened checks.

6. **Recheck in CI.** Pushing is the user's call. Unless they asked you to push, give them the commit and the command, then wait. After a push, poll the checks (`gh pr checks <pr> --watch`) until they finish, and report each job's final state.
   Exit: every previously failing job is green, or each remaining failure has been re-classified with new evidence.

## Output

```
<job name>: <bucket>, <first error line>
  cause: <one sentence>   fix: <what changed>   local repro: <command> → pass
Remaining: <jobs still red, why, next step>
```

## Rationalizations

| Excuse | Reality |
|---|---|
| "It's flaky, just re-run it" | Re-run once to *classify* it. A second re-run hides it. If it's flaky, triage it. |
| "Mark it continue-on-error for now" | "For now" means forever. The next real failure will slip through that job. |
| "This test is outdated, delete it" | Only when the behaviour it covers was removed on purpose, and you say so in the PR. |
| "CI is just different, can't reproduce" | List the differences and remove them one at a time. CI is a computer, not a mystery. |
| "Bump the coverage threshold down, it's close" | The threshold is the team's bar. Changing it is the team's decision, not a fix. |

## Red flags

- Reading only the last lines of the log
- The fix diff touches the test and not the code under test
- Changing the workflow's `on:` triggers, `permissions:` or `pull_request_target` to make something pass
- Running the full suite locally instead of the failing target
- Pushing or re-running jobs without the user's go-ahead

## References

- [scripts/ci_failures.py](scripts/ci_failures.py): run `python3 scripts/ci_failures.py --help`; it lists failing GitHub Actions checks for a PR or branch and prints the first error lines from each failed log
