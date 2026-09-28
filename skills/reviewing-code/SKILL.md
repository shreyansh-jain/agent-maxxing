---
name: reviewing-code
description: Multi-axis review of a diff, branch or pull request for spec fit, correctness and repo standards, with confidence-filtered findings. Use when asked to review a PR, branch, commit range or pasted diff, before merging or landing a change, after an agent or teammate finishes a task, or when asked to find bugs in recent changes.
license: Apache-2.0
metadata:
  version: "0.1.0"
  category: "review"
  sources: "mattpocock/skills code-review (MIT); garrytan/gstack review + specialists (MIT); anthropics/claude-plugins-official code-review and pr-review-toolkit (Apache-2.0); addyosmani/agent-skills code-review-and-quality (MIT); obra/superpowers requesting-code-review (MIT); getsentry/skills find-bugs (Apache-2.0); ideas: trailofbits/skills"
---

# Reviewing Code

A review is worth the findings that are real, important and actionable, and nothing else. Check spec fit, correctness and standards separately, verify every candidate finding, and report only what survives.

## When to use

- "Review this PR / branch / diff", "anything wrong with these changes?", "find bugs before I merge"
- An implementation task (yours, a subagent's, a teammate's) just finished and needs a gate before it lands
- A pasted diff or a commit range to evaluate

**Not for:** a dedicated security audit of a system or a risky surface (use `auditing-security`); responding to review comments you received (use `receiving-code-review`); reviewing a plan before code exists (use `reviewing-plans`); cleaning up working code (use `simplifying-code`).

## Process

1. **Pin the range.** Resolve the base (`git merge-base <base> HEAD`) and use a three-dot diff: `git diff <base>...HEAD` plus `git log --oneline <base>..HEAD`. For a PR, use `gh pr diff <n>` / `gh pr view <n>`. If the diff output is truncated, read every changed file until you have seen every changed line.
   Exit: the base resolves, the diff is non-empty, and you have seen all of it. A bad ref or an empty diff stops the review here.

2. **Gather intent and standards.** Intent: the linked issue, spec or plan (from commit messages, PR body, branch name, or `docs/`/`specs/`); ask for it if nothing is found. Standards: `AGENTS.md`/`CLAUDE.md` (root and in touched directories), `CONTRIBUTING.md`, style or architecture docs, and lint config.
   Exit: you can state in one sentence what the change is supposed to do, or you have recorded "no spec available".

3. **Check scope drift first.** Compare what was asked with what changed. Look for missing requirements, and for unrequested behavior, files or refactors mixed in. A change doing two things is two changes.
   Exit: a scope verdict of on target, missing items, or scope creep (list each).

4. **Review three axes independently.** Each axis gets its own pass. When a subagent tool is available, give each axis a fresh-context reviewer using [reviewer-brief.md](references/reviewer-brief.md) (diff command, intent, standards files, and that axis's checklist, never your session history), and run them in parallel.
   - **Spec:** does the code do what the intent says, including edge cases and error paths the spec implies?
   - **Correctness:** bugs, data safety, concurrency, security, performance traps, silent failures, test gaps. Pick the specialist checklists in [checklists.md](references/checklists.md) that match what the diff touches.
   - **Standards:** the repo's documented rules, then the smell baseline. Documented repo rules override the baseline. Skip anything a linter or type checker already enforces.
   Exit: each axis has returned a candidate list, or explicitly "no findings".

5. **Look outside the diff.** Bugs often live in code the diff did not touch. For each new enum value, status, role, flag or config key, grep for its *sibling values* and read every switch, allowlist, serializer and UI that handles them. For each changed function signature or behavior, read its callers. For each bug you confirm, search for the same pattern elsewhere in the change.
   Exit: every new value and changed contract has been traced to its consumers.

6. **Verify and score every candidate.** For each one, read the surrounding code and confirm three things: it is not handled elsewhere, it is reachable, and it is new in this diff. Then score your confidence from 0 to 100 that it is a real problem someone will hit. Keep **≥ 80**. Put 50–79 under "Needs verification" with the check that would settle it. Drop anything below 50. Zero findings is a valid result: do not invent issues to look thorough.
   Exit: every surviving finding cites `file:line`, has evidence, and has a concrete fix.

7. **Report.** Use the format below. Order by severity within each axis. Do not merge or re-rank across axes, so that a clean standards pass cannot hide a spec miss.

Do not post PR comments, push fixes, or edit code unless the user asked for that. If they asked you to fix findings, apply the mechanical, unambiguous ones. Batch the judgment calls into one question.

**Reviewing your own work:** use a fresh-context subagent when one is available. You wrote the code, so you will read what you meant rather than what you wrote.

## Output

```
Review of <base>..<head> (<N> files, +A/−D). Intent: <one sentence> | no spec available
Scope: on target | missing: … | creep: …

## Spec
- [Blocker|Major|Minor] file:line: problem. Evidence: … Fix: … (confidence NN)
## Correctness
- …
## Standards
- … (cites rule: AGENTS.md "…" | smell: Feature Envy)
## Needs verification
- file:line: suspicion. Settle by: <command or check>

Verdict: approve | approve with nits | request changes. Worst issue: <one line per axis, or "none">
Not checked: <areas skipped and why>
```

Severity:
- **Blocker**: data loss, a security hole, broken core behavior, or a crash in a common path.
- **Major**: a real bug in an edge path, a missed requirement, or a breaking contract change.
- **Minor**: a maintainability or clarity problem with a concrete cost.
- **Nit**: optional.

Approve when the change clearly improves the codebase, even if it is not how you would have written it.

## Red flags

- Findings about lines the diff did not touch, presented as regressions (pre-existing issues go under "FYI", if anywhere)
- A finding without `file:line` and evidence
- Reporting what the linter, type checker or CI will catch anyway
- "Looks good overall" padding, or 20 nits burying one blocker
- A new enum value or status reviewed without grepping for its siblings
- Declaring "no issues" without listing what was not checked

## References

- [checklists.md](references/checklists.md): open at step 4 to choose the correctness specialists and the standards smell baseline
- [reviewer-brief.md](references/reviewer-brief.md): open when dispatching an axis to a subagent
