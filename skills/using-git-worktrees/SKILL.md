---
name: using-git-worktrees
description: Isolated git worktree workspaces for parallel or risky work. Use when starting feature work that should not disturb the current checkout, running several agents or branches at once, before executing an implementation plan, or when asked to set up, list, or clean up worktrees.
license: Apache-2.0
metadata:
  version: "0.1.0"
  category: "ship"
  sources: "obra/superpowers using-git-worktrees, finishing-a-development-branch (MIT); addyosmani/agent-skills git-workflow-and-versioning (MIT)"
---

# Using Git Worktrees

Check whether you are already isolated, then use the harness's own worktree tool, and fall back to raw `git worktree` only when there is no such tool. Never create state the harness cannot see.

## When to use

- Starting a feature, spike, or hotfix that must not touch the user's current checkout
- Running several agents or branches in parallel against one repository
- Before executing a multi-task plan
- Listing, pruning, or removing worktrees after work lands

**Not for:** splitting work across subagents (use `dispatching-subagents`, which may call this skill); landing and cleaning up a finished branch (use `shipping-changes`); merge or rebase conflicts (use `resolving-merge-conflicts`).

## Process

1. **Detect existing isolation.**
   ```bash
   git_dir=$(cd "$(git rev-parse --git-dir)" && pwd -P)
   common_dir=$(cd "$(git rev-parse --git-common-dir)" && pwd -P)
   superproject=$(git rev-parse --show-superproject-working-tree 2>/dev/null)
   ```
   If `git_dir != common_dir` and `superproject` is empty, you are already in a linked worktree. Report the path and branch (or the detached HEAD) and skip to step 4. Inside a submodule, the two directories also differ, so treat a submodule as a normal checkout.
   Exit: you know whether a new worktree is needed.

2. **Get consent and choose the mechanism.** If neither the user's instructions nor the plan asks for isolation, ask once: "Set up an isolated worktree so your current branch stays untouched?" Then:
   - **Native tool first.** If the harness has one (an `EnterWorktree`-style tool, a `/worktree` command, a `--worktree` flag), use it. It owns placement, branch creation, and cleanup. Running `git worktree add` alongside it creates a phantom workspace the harness cannot manage.
   - **Git fallback.** Use the directory the user's instructions name. If none, use an existing `.worktrees/` or `worktrees/` directory. If neither exists, use `.worktrees/`.
   Exit: a mechanism and a path are chosen.

3. **Create the worktree safely (git fallback only).**
   ```bash
   git check-ignore -q .worktrees || echo ".worktrees/" >> .git/info/exclude
   git worktree add .worktrees/<branch> -b <branch> <base>
   ```
   `.git/info/exclude` ignores the directory locally without editing a tracked file. Edit `.gitignore` instead only when the user wants the rule shared, and commit it only if they ask. If the sandbox denies `worktree add`, say so and work in place.
   Exit: `git worktree list` shows the new path, and `git status` in the main checkout is unchanged.

4. **Set up and record a baseline.** Install dependencies using the project's lockfile tool (`npm ci`, `pnpm install --frozen-lockfile`, `uv sync`, `cargo fetch`, `go mod download`). Copy any untracked config the app needs, such as `.env`, only if the user agrees. Then run the narrowest check the user's instructions allow, typically a typecheck or one test file, and record the result.
   Exit: the baseline is known. If it is already failing, report that before starting work, so later failures aren't blamed on your changes.

5. **Clean up only what you created.** When work lands or is abandoned:
   ```bash
   git worktree remove .worktrees/<branch>      # refuses if there are uncommitted changes
   git worktree prune
   ```
   Never remove a worktree that the harness or the user created, never pass `--force` without asking, and never delete an unmerged branch without confirmation.

## Output

```
Worktree: /repo/.worktrees/feat-bulk-export on feat-bulk-export (from main@3f2c1a9)
Created with: native tool | git worktree add
Ignored via: .git/info/exclude
Baseline: tsc --noEmit ✓ ; tests/export.test.ts ✓ (12 passed)
```

## Rationalizations

| Excuse | Reality |
|---|---|
| "I'm obviously in the main checkout" | Harness-created worktrees and submodules both look like normal checkouts. Run the detection commands. |
| "`git worktree add` is faster than finding the native tool" | The harness cannot see or clean up a worktree it did not create. |
| "The directory is surely ignored" | Run `git check-ignore`. If it isn't, the next `git add -A` stages the whole nested checkout. |
| "The baseline can wait" | Without a baseline, you cannot tell whether a later failure is yours or was already there. |

## Red flags

- Creating a worktree while already inside one
- A worktree directory that shows up in `git status` as untracked
- Running `git worktree remove --force` or `branch -D` without asking
- Editing and committing `.gitignore` when the user did not ask for a shared rule
