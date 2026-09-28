# Splitting a messy working tree

The goal is a sequence of commits that each build, pass, and do one thing. That keeps the history bisectable and each commit revertable on its own.

## 1. Inventory

```bash
git status --short
git diff --stat
git diff <file>          # read each hunk and label it
```

Label every hunk with the commit it belongs to, e.g. `refactor`, `fix-tax`, `format`, `deps`. A file can carry hunks for several labels.

## 2. Order

Put the commits in this order so each one stands alone:
1. Mechanical changes (formatting, renames, moved files). Reviewers skim these.
2. Dependency or config changes the later commits rely on.
3. Refactors that change no behavior (prefactoring).
4. The behavior change, together with its tests.

## 3. Stage by hunk

| Situation | Command |
|---|---|
| Interactive terminal available | `git add -p <file>`, answering `y`/`n`/`s` (split) per hunk |
| No interactive terminal (agent harness) | `git diff <file> > /tmp/all.patch`, edit a copy down to the wanted hunks, then `git apply --cached /tmp/part.patch` |
| Whole new file belongs to one commit | `git add <file>` |
| Staged a hunk by mistake | `git restore --staged -p <file>`, or `git restore --staged <file>` and start again |

Before each commit, check what is staged:

```bash
git diff --staged --stat
git diff --staged        # read it; this is what the commit will contain
```

## 4. Verify each commit stands alone

If the user allows it, check that every commit in the stack builds and passes the fast checks, not just the tip:

```bash
git stash --keep-index --include-untracked   # test exactly what is staged
<fast typecheck / single relevant test file>
git stash pop
```

## 5. When not to split

- The change is small, and splitting would leave a commit that does not build.
- The repo squash-merges PRs and the user does not care about intermediate commits. Ask once rather than spending effort on a split nobody will see.
