# Reviewer subagent brief

Fill one brief per axis and dispatch the briefs in parallel. The reviewer sees only what you put here, never your session history. That is what keeps it from reading your intentions into the code.

```
You are reviewing one axis of a code change. Report findings only; do not edit files.

Change: <one-sentence intent> (spec: <path/URL or "none available">)
Diff: run `git diff <base>...<head>`; commits: `git log --oneline <base>..<head>`
If the diff output is truncated, read each changed file until you have seen every changed line.

Axis: <Spec | Correctness | Standards>
<For Spec:> Quote the spec line for each finding. Report (a) requirements missing or partial,
  (b) behavior nobody asked for, (c) requirements implemented incorrectly.
<For Correctness:> Use these checklists as prompts, not as findings: <paste the chosen sections>.
  Read outside the diff: grep sibling values of any new enum/status, and read callers of changed functions.
<For Standards:> Rules: <list the AGENTS.md / CLAUDE.md / CONTRIBUTING paths>. Cite file + rule for each finding.
  Then apply this smell baseline where the repo is silent, as judgment calls: <paste the table>.
  Skip anything a linter, formatter or type checker enforces.

For every finding give: file:line, severity (Blocker/Major/Minor/Nit), the evidence it is real
(not handled elsewhere, reachable, introduced by this diff), a concrete fix, and confidence 0-100.
Do not report pre-existing issues on untouched lines as regressions.
"No findings" is an acceptable answer. Do not pad. List anything you could not check and why.
Under 400 words.
```

When all axes return, you (the coordinator) verify each finding scored ≥ 50 yourself before reporting it, as in SKILL.md step 6. A subagent's confidence score is only a claim until you have checked it.
