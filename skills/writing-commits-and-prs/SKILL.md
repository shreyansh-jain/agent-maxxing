---
name: writing-commits-and-prs
description: Commit messages, commit splitting, and pull request titles and descriptions that follow the repository's own conventions. Use when asked to commit, draft a commit message, split a messy working tree into commits, open or update a PR, or rewrite a PR description after new commits.
license: Apache-2.0
metadata:
  version: "0.1.0"
  category: "ship"
  sources: "getsentry/skills commit, pr-writer (Apache-2.0); addyosmani/agent-skills git-workflow-and-versioning (MIT); openai/skills yeet (Apache-2.0); anthropics/claude-plugins-official commit-commands (Apache-2.0)"
---

# Writing Commits and PRs

A commit message tells a future reader why the change was made, and a PR description is a cover note that helps the reviewer. Neither is a changelog, and both follow the conventions the repository already uses.

## When to use

- The user asks you to commit, or to draft a commit message they will run themselves
- The working tree mixes several unrelated changes that need separate commits
- Opening a pull request, or refreshing its title and body after scope changed

**Not for:** the full pre-merge pipeline of syncing the base, running checks, and landing the change (use `shipping-changes`); answering reviewer comments (use `receiving-code-review`); conflicts during merge or rebase (use `resolving-merge-conflicts`).

## Process

1. **Check permission.** Only run `git commit`, `git push`, or `gh pr create` when the user asked for that action in this turn or their standing instructions allow it. Otherwise write the message and hand it over.
   Exit: you know whether you are *writing* the message or also *running* the command.

2. **Learn the house style.** Run `git log --oneline -20`, then `git log -5 --format='%B---'` for full bodies. Look for CONTRIBUTING.md, commitlint or commitizen config, and `.github/pull_request_template.md`. Note the prefix scheme (Conventional Commits, `[area]`, ticket keys), subject case and length, and trailers.
   Exit: you can state the convention in one line, e.g. "conventional, lowercase, scope optional, `Refs JIRA-123` footer".

3. **Read what is actually changing.** Run `git status`, `git diff`, and `git diff --staged`. For a PR, read the whole branch with `git log <base>..HEAD` and `git diff <base>...HEAD`, not just the last commit.
   Exit: you can name every logical change in the diff.

4. **Split into atomic commits.** Each commit should be one reviewable change that builds and passes on its own. Keep refactors, formatting, dependency bumps and behavior changes in separate commits. Stage partial files with `git add -p <file>`, or with `git apply --cached` on a hand-written patch when interactive staging is unavailable. Never sweep unrelated files in with `git add -A`.
   Exit: each planned commit has one purpose you can state in its subject.

5. **Write the message.**
   - The subject is imperative, specific, and within the repo's length norm (≤72 characters if there is none). "Fix rounding of tax on discounted lines", not "fix bug" or "updates".
   - The body explains *why*: previous behavior, motivation, and any trade-off. The diff already shows *what*.
   - Footers: issue references only when verified, breaking-change notes, and trailers the repo uses.
   - Add attribution trailers only if the user's instructions call for them. When instructions conflict, the user's own instructions win over tool defaults.
   - Pass paragraphs as separate `-m` arguments or with `-F <file>`. Never embed a literal `\n` or open an interactive editor.

6. **Write the PR.** Fill in the repo's template if one exists. Otherwise:
   - **Title:** the dominant change of the whole branch, in the commit subject style.
   - **Body:** first, what changed and what effect it has. Then add only what the reviewer needs: why this approach, risk, migration, and where to start reading.
   - Size the body to the change. A small fix gets one paragraph. A contract change gets a before/after snippet.
   - Leave out file-by-file lists, pasted CI logs, and routine "ran the tests" lines unless they change the reviewer's risk assessment.
   - Write the body to a temp file and pass it with `--body-file`. Open new PRs as drafts unless the user says otherwise. When updating a PR, rewrite the body to describe the current diff; don't narrate its review history.
   Exit: a reviewer who reads only the title and first paragraph knows what to expect.

7. **Scrub.** Remove secrets, customer names, emails, internal URLs the repo keeps private, and any unverified issue numbers.

## Output

```
<type>(<scope>): <imperative subject in house style>

<why this change: previous behavior, motivation, trade-off>

<footers the repo uses, e.g. Refs #123 / BREAKING CHANGE: ...>
```

## Red flags

- Writing a message before reading `git log`, or inventing a convention the repo does not use
- A subject that says "and": it is two commits
- `git add -A` or `git commit -a` on a tree with unrelated edits
- The PR body lists files or restates the diff instead of explaining it
- Adding a `Co-Authored-By` or similar trailer the user's instructions forbid
- Committing or pushing because a plan step says so, when the user has not asked

## References

- [splitting-commits.md](references/splitting-commits.md): open when a working tree mixes unrelated changes, or `git add -p` is unavailable
