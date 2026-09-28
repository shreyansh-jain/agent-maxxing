---
name: shipping-changes
description: End-to-end discipline for taking finished work from a branch to merged and released, including pre-merge verification, integration choice, staged rollout and rollback. Use when implementation is done and the user wants to ship, land, merge, release or deploy a branch, open it for review, cut a release, or plan a launch with feature flags or a canary.
license: Apache-2.0
metadata:
  version: "0.1.0"
  category: "ship"
  sources: "garrytan/gstack ship, land-and-deploy, canary (MIT); obra/superpowers finishing-a-development-branch (MIT); addyosmani/agent-skills shipping-and-launch, git-workflow-and-versioning (MIT)"
---

# Shipping Changes

Ship only what you verified against the latest base branch, and let the user choose how to integrate. Every irreversible step — commit, push, merge, deploy — happens only on their say-so.

## When to use

- "I'm done, ship it" / "land this" / "get this merged" / "open a PR"
- Preparing a branch for review or release
- Cutting a release, bumping a version, updating a changelog
- Planning a production rollout: feature flag, canary, staged percentage, rollback plan

**Not for:** writing the commit message or PR body itself (use `writing-commits-and-prs`); red CI checks on the PR (use `fixing-ci-failures`); conflicts during the base-branch merge (use `resolving-merge-conflicts`); a deploy that is already hurting users (use `responding-to-incidents`).

## The rule

```
NO COMMIT, PUSH, MERGE OR DEPLOY WITHOUT THE USER ASKING FOR IT, AND NONE WITHOUT FRESH VERIFICATION ON THE LATEST BASE
```

Violating the letter of the rule is violating the spirit of the rule. A plan, a skill or an earlier "yes" does not authorise the next irreversible step. Only the user's instruction in this session does.

## Process

1. **Establish the state.** Check the current branch, the base branch (confirm it if you are unsure), uncommitted changes, whether you are in a worktree, and whether a PR already exists (`git status`, `git log --oneline <base>..HEAD`, `gh pr view`).
   Exit: you can state the branch, base, commit count, and dirty or clean status.

2. **Bring in the base first.** Fetch, then merge or rebase the latest base into the branch, following the repo's convention. Do this *before* running any checks: tests that pass on a stale base prove nothing about the merge. If conflicts appear, switch to `resolving-merge-conflicts`.
   Exit: the branch contains the latest base, with no conflicts.

3. **Verify.** Run the project's own checks: type check, lint, build, and the tests the change affects. If the user's instructions forbid running the full suite, run the narrowest set that covers the diff and say what you left out. Read the diff end to end: look for debug leftovers, secrets, stray files, TODOs without owners, and scope creep beyond what was asked. **REQUIRED:** follow `verifying-before-completion`, which means showing output rather than claiming it passed.
   Exit: fresh output shows the checks green on the merged state, or the failures are listed and shipping stops.

4. **Shape the history.** If the user has asked you to commit, make bisectable commits. Each commit is one logical change, compiles, and passes tests. Order them infrastructure → core logic → callers → docs, and keep tests with the code they cover. Use `writing-commits-and-prs` for the messages. If the user has not asked you to commit, leave the work in the tree and summarise what is ready.

5. **Present the integration options and wait.**
   ```
   Ready: <branch> (<n> commits on <base>, checks green).
   1. Merge into <base> locally
   2. Push and open a pull request
   3. Keep the branch as-is
   ```
   Carry out only the option the user picks. After a local merge, re-run the checks on the merged result before deleting anything. Clean up only a worktree or branch that *you* created. Never discard work unless the user explicitly asks.

6. **Release, if asked.** Bump the version according to the project's scheme (semver: breaking → major, feature → minor, fix → patch), update the CHANGELOG in user-facing language, and tag it only when instructed.

7. **Roll out safely, if deploying.** Before deploying, write down: the rollback command, the health signal (error rate, latency, a key business metric), and the abort threshold. Prefer dark launches behind a feature flag, then a canary or staged percentage (e.g. 1% → 10% → 50% → 100%), watching the health signal for a fixed bake time at each stage. Every deploy command runs only after the user approves that specific command.
   Exit: each stage held its bake time within threshold, or the rollback ran.

## Output

```
Branch: <name> → <base>   Base merged: <sha>   Commits: <n> (bisectable: yes/no)
Checks: <command> → pass | <what was not run and why>
Diff review: <clean | issues found>
Awaiting: choice of 1/2/3   (or: PR <url> | merged <sha> | deployed <version> at <stage>)
Rollback: <command>   Health signal: <metric, threshold>
```

## Rationalizations

| Excuse | Reality |
|---|---|
| "Tests passed an hour ago" | Code or base changed since. Fresh run on the merged state or it doesn't count. |
| "The plan says commit after each task" | Plans don't grant permission; the user does. Ask, or leave it in the tree. |
| "They said ship it earlier, so push too" | Each irreversible step needs its own go-ahead unless the user explicitly delegated the whole flow. |
| "One big commit is simpler" | One big commit can't be bisected or partially reverted. |
| "It's a small change, skip the canary" | Small changes cause most outages because nobody watches them. Keep the bake time. |

## Red flags

- Running tests before merging the base
- `git push --force` on a shared branch, or `--no-verify` to get past hooks
- Deleting a branch or worktree before verifying the merged result
- A deploy without a written rollback command and abort threshold
- Choosing merge vs PR for the user
- Claiming "shipped" without a PR URL, merge SHA or deployed version
