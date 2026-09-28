---
name: resolving-merge-conflicts
description: Resolving git merge, rebase, and cherry-pick conflicts by reconstructing what each side intended. Use when git reports CONFLICT, a rebase or merge stops partway, conflict markers appear in files, or a lockfile or generated file conflicts after pulling the base branch.
license: Apache-2.0
metadata:
  version: "0.1.0"
  category: "ship"
  sources: "mattpocock/skills resolving-merge-conflicts (MIT); addyosmani/agent-skills git-workflow-and-versioning (MIT)"
---

# Resolving Merge Conflicts

A conflict is two intents colliding, so resolve it by finding out what each side meant. The resolved code keeps both intents where it can, and it never includes behavior that neither side wrote.

## When to use

- `git merge`, `git rebase`, `git cherry-pick`, `git stash pop` or `git pull` stopped with `CONFLICT`
- A file contains `<<<<<<<`, `=======`, `>>>>>>>` markers
- A lockfile, snapshot or generated file conflicts after updating from the base branch

**Not for:** composing the commit or PR message afterwards (use `writing-commits-and-prs`); the full "sync with base, test, and land" pipeline (use `shipping-changes`); tests that fail after a clean merge (use `debugging-systematically`).

## The rule

```
NO HUNK RESOLVED BEFORE YOU CAN STATE WHAT BOTH SIDES INTENDED
```

Violating the letter of the rule is violating the spirit of the rule. Picking "ours" or "theirs" for the whole file without reading both sides throws away someone's work without anyone noticing.

## Process

1. **See the state.** Run `git status` to learn which operation is in progress and which files are unmerged. During a rebase, *ours* is the branch being rebased onto and *theirs* is your commit being replayed, which is the reverse of a merge. Say which is which before touching anything.
   Exit: you can name the operation, both sides, and every conflicted file.

2. **Get a three-way view.** Run `git checkout --conflict=zdiff3 <file>` (or `diff3` on older git) so each hunk also shows the common ancestor. The ancestor tells you what each side *changed*, which is what matters.
   Exit: every conflicted hunk shows base, ours, and theirs.

3. **Reconstruct both intents.** For each side, run `git log --merge -p -- <file>` and read the commit messages, the linked PRs and the issues. Also look for code *outside* the hunk that the other side changed and this hunk depends on, such as a renamed function or a new required argument.
   Exit: for each hunk, one sentence per side: "ours adds retry on 429; theirs extracts the client into http.ts".

4. **Resolve each hunk.**
   - **Compatible intents:** combine them, for example by applying our retry inside their extracted client.
   - **Incompatible intents:** pick the one matching the goal of the merge, note the trade-off, and tell the user.
   - **Genuinely unclear:** ask the user. Do not guess.
   - **Generated files and lockfiles:** do not hand-merge. Take either side, then regenerate with the project's tool (`npm install`, `uv lock`, `cargo generate-lockfile`, codegen, snapshot update).
   - Never write new behavior that neither side had.
   Exit: `git diff --check` reports no leftover markers, and `grep -rnE '^(<<<<<<<|>>>>>>>)' .` finds none.

5. **Verify.** Find the project's checks (typecheck, lint, the tests that cover the touched files) and run the narrowest set that covers the conflicted files. A merge that compiles but breaks behavior is still a failed merge.
   Exit: the checks pass, or you report exactly what is still failing and why.

6. **Continue the operation.** Stage the resolved files and run `git merge --continue`, `git rebase --continue` or `git cherry-pick --continue`. During a rebase, repeat from step 1 for each stopped commit. Only abort (`--abort`) if the user agrees: aborting discards their in-progress resolution.
   Exit: `git status` shows no operation in progress, and you summarise how each hunk was resolved.

For a long rebase that hits the same conflict repeatedly, suggest `git config rerere.enabled true` so git records and reuses each resolution.

## Output

```
Operation: rebase of feature/x onto main (ours = main, theirs = feature/x)
src/api/client.ts
  hunk 1: ours added 429 retry; theirs moved client to http.ts → retry applied inside http.ts
  hunk 2: both changed timeout (5s vs 10s) → kept 10s per theirs' commit msg "match upstream SLA"; flagged
package-lock.json: regenerated with npm install
Checks: tsc --noEmit ✓, tests/api/client.test.ts ✓
```

## Rationalizations

| Excuse | Reality |
|---|---|
| "Just take theirs, it's newer" | Newer is not correct. Taking one side for the whole file drops the other side's fix without anyone seeing it. |
| "I'll hand-merge the lockfile" | Hand-merged lockfiles install something neither side tested. Regenerate them. |
| "It compiles, so it's resolved" | Semantic conflicts compile fine. Run the tests that cover the files. |
| "Abort and start over is cleaner" | Aborting throws away the user's partial resolution. Ask first. |

## Red flags

- Resolving with `git checkout --ours .` or `--theirs .` across many files
- Writing code in a hunk that appears in neither side
- Not knowing which side is "ours" during a rebase
- Continuing the rebase without running any check
