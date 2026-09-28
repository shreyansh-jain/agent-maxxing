---
name: setting-up-ci-pipelines
description: Design and hardening of CI pipelines for fast feedback, reproducibility and least privilege. Use when creating a new CI workflow, adding jobs or gates, speeding up slow CI, adding caching or matrices, or securing workflows (tokens, secrets, fork PRs, pinned actions).
license: Apache-2.0
metadata:
  version: "0.1.0"
  category: "ship"
  sources: "addyosmani/agent-skills ci-cd-and-automation (MIT); wshobson/agents github-actions-templates (MIT); getsentry/skills gha-security-review (Apache-2.0)"
---

# Setting Up CI Pipelines

A pipeline is a product with two users: developers who need a fast, trustworthy verdict, and attackers who want its tokens. Optimize for the first and deny the second.

## When to use

- A repo has no CI, or needs new jobs (lint, types, tests, build, e2e, release)
- CI is slow, or reruns are common, and someone wants it faster
- Adding caching, matrices, artifacts, required checks or branch protection
- Hardening workflows: `permissions:`, secrets, fork PRs, third-party actions, OIDC

**Not for:** a failing check on a specific PR (use `fixing-ci-failures`); a test that fails intermittently (use `triaging-flaky-tests`); the infrastructure the pipeline deploys (use `writing-infrastructure-as-code`); rollout strategy and release (use `shipping-changes`); a full security audit of the app (use `auditing-security`).

## Process

1. **Inventory what exists.** Read the current workflows, the project's real commands (package scripts, Makefile, task runner), the runtime versions in use, and today's timings (for example `gh run list --limit 20 --json databaseId,conclusion,createdAt,updatedAt,name`).
   Exit: a list of jobs with their duration, the slowest step, and the commands developers run locally.

2. **Define the gate.** List the checks a change must pass to merge, cheapest first: format/lint and type check → unit tests → build → integration tests → e2e. Set a time budget (e.g. under 10 minutes to a first verdict). Every check must have a **local equivalent**, one command that runs the same thing (`make ci`, `npm run ci`), so CI never becomes the only place a failure can be reproduced.
   Exit: an ordered gate list, a time budget, and the local command for each check.

3. **Structure the jobs for fast feedback.**
   - Run cheap checks first and in parallel. Make expensive jobs `needs:` the cheap ones, so a lint error never waits behind e2e.
   - Cache dependencies keyed on the lockfile hash (`hashFiles('**/package-lock.json')`), plus build caches where the tool supports them. Never cache anything the build writes secrets into.
   - Use a matrix only where the axis catches real bugs (supported runtime versions, OSes you ship to). Otherwise run one leg on PRs and the full matrix on the main branch or nightly.
   - Set `concurrency:` with `cancel-in-progress: true` for PR workflows, so superseded pushes stop burning minutes.
   - Set `timeout-minutes` on every job, and a short `retention-days` on artifacts.
   - Pin runtime versions from the repo (`.nvmrc`, `.python-version`, `go.mod`) so CI and local match.
   Exit: a workflow in which the first failing class of check reports within the budget.

4. **Lock down privilege.**
   - Default to `permissions: contents: read` at the top level, and grant write scopes per job only where needed.
   - Pin third-party actions to a full commit SHA, with the version in a comment (`uses: owner/action@<sha> # v4.2.1`). Let Dependabot or Renovate bump them.
   - Never run untrusted PR code with secrets. Avoid `pull_request_target` and `workflow_run` combined with a checkout of the PR head. If you must use them, never execute the checked-out code.
   - Never interpolate attacker-controlled values (PR title, branch name, issue or comment body) directly into `run:`. Pass them through `env:` and quote them.
   - Prefer OIDC federation to cloud providers over long-lived secrets. Scope secrets to environments that have required reviewers.
   Exit: no job holds more permission than its steps use, and no secret reaches fork-PR code.

5. **Make it required and observable.** Mark the gate jobs as required status checks in branch protection or rulesets. Use one aggregating "all checks passed" job if the matrix makes names unstable. Upload test reports (JUnit, coverage) as artifacts, and surface failures in the job summary.

6. **Verify.** Run the local equivalent. Validate the workflow syntax (`actionlint` if available). Open a draft PR, only if the user wants one, and compare the new timings with step 1.
   Exit: before/after durations, and every gate job green on a real run, or the run is pending and you say so.

## Output

```
Gate (in order): lint+types → unit → build → integration → e2e   budget: <N> min
Local equivalents: <check> → <command>
Timing: before <X> min → after <Y> min (slowest step: <name>)
Security: permissions default read; actions SHA-pinned; fork PRs get no secrets; OIDC for <cloud>
Required checks: <names>
```

## Red flags

- `permissions: write-all`, or no `permissions:` key at all, on a workflow that holds secrets
- `pull_request_target` combined with `actions/checkout` of `github.event.pull_request.head.sha`
- `${{ github.event.pull_request.title }}` or a similar value inside a `run:` script
- Third-party actions on `@main` or a mutable tag in jobs with secrets or deploy power
- CI-only scripts no developer can run locally
- `continue-on-error: true` on a gate job, or tests retried until green
- Cache keys that ignore the lockfile, so a stale cache hides dependency changes
