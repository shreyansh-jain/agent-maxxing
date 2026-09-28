---
name: reviewing-plans
description: Engineering review of a plan, spec, or design before implementation starts, covering scope, architecture, failure modes, tests, and performance. Use when the user asks to review, critique, sanity-check or poke holes in a plan or design doc, before committing a team to an approach, or when a plan touches many files, adds new services, or changes interfaces others depend on.
license: Apache-2.0
metadata:
  version: "0.1.0"
  category: "plan"
  sources: "garrytan/gstack plan-eng-review (MIT); garrytan/gstack autoplan (MIT); obra/superpowers writing-plans (MIT); addyosmani/agent-skills doubt-driven-development (MIT)"
---

# Reviewing Plans

Problems cost the least to fix in the plan. Challenge the scope first, then the structure, and back every finding with evidence from the code.

## When to use

- The user asks you to review, critique, sanity-check, or poke holes in a plan, spec, or design doc
- A team is about to commit to an approach that is expensive to reverse
- A plan touches 8 or more files, adds new services or classes, or changes interfaces other code depends on
- You have just written a plan yourself and want an independent check before execution

**Not for:** reviewing code that has already been written (use `reviewing-code`); security threat modelling of existing code (use `auditing-security`); writing the plan (use `planning-implementation`).

## Process

1. **Fix the target and read it whole.** Name the plan you are reviewing by path or title. Read it end to end, along with the spec it implements. Then read the code it proposes to change. Check every interface, table, and function the plan mentions against the repo. A plan that calls a function that doesn't exist is the most common and cheapest bug to catch.
   Exit: every referenced existing symbol is confirmed to exist, or listed as a finding.

2. **Challenge the scope before the design.**
   - **What already exists?** For each sub-problem, look for a helper, library, or earlier feature that already solves it.
   - **What is the minimum?** Name the work that could be deferred without blocking the goal.
   - **Complexity tripwire.** If the plan touches 8 or more files, or adds 2 or more new services or classes, stop and put a smaller arrangement to the user, one that keeps the same features and contracts. Ask about each proposed cut separately, and wait for answers.
   Exit: the scope is agreed, or the tripwire questions have been answered.

3. **Review four areas, in order, with at most 8 top issues each:**
   - **Architecture:** boundaries and coupling, data flow, single points of failure, auth and data-access boundaries. For each new path or integration, name one realistic production failure and check whether the plan handles it.
   - **Code quality:** fit with existing patterns, error-handling gaps, missing edge cases, premature abstraction. Only propose sharing code once you have shown at least two real call sites.
   - **Tests:** does every behavior in the spec have a test at an honest seam? What about error paths, empty inputs, concurrency, and the Review Focus items?
   - **Performance:** N+1 access, unbounded queries or loops, memory, caching, hot paths.

   "No issues found" is a valid result for an area. Don't invent findings to fill a section.
   Exit: each area is reported.

4. **Grade each finding.** Give each one a severity (blocker / important / minor), a confidence level (high / medium / low), and evidence (a `file:line` or a quote from the spec). Findings based only on vague unease are low confidence; label them that way or drop them.
   Exit: every finding is graded and has evidence.

5. **Get an outside view for high-stakes plans.** If the plan is irreversible, touches security or money, or the user asks for it, send a fresh-context reviewer. Give it only the plan, the spec, and the repo, and tell it to *disprove* the plan (see `dispatching-subagents`). Merge its findings into yours, marked with their source.
   Exit: either done, or skipped because the stakes don't call for it.

6. **Resolve decisions one at a time.** For each blocker or important finding, give 2–3 options with your recommendation and what it costs. Let the user decide. Record accepted, rejected, and deferred outcomes. Edit the plan only if the user asks you to.

Apply engineering judgment throughout: prefer boring technology, reversible changes, incremental migration, and designs that work for a tired human at 3 a.m. See [references/engineering-judgment.md](references/engineering-judgment.md).

## Output

```
Plan review: <plan title/path>
Scope: <accepted | reduced: what changed | tripwire questions pending>
What already exists: <reusable pieces the plan should use>
Not in scope: <deferred items>

Findings
1. [blocker | high] <title>. Evidence: <file:line or spec quote>. Recommendation: <option> (alternatives: …)
…
Architecture: <n findings | No issues found>
Code quality: …   Tests: …   Performance: …

Verdict: ready | ready after blockers are resolved | rethink (why)
```

## Red flags

- Reviewing the plan's wording without opening the code it changes
- A finding with no evidence and no confidence label
- Listing a dozen minor nits while missing that the plan duplicates an existing module
- Rewriting the plan yourself before the user has decided anything
- Treating the approval of one scope cut as approval of all of them

## References

- [engineering-judgment.md](references/engineering-judgment.md): open when weighing trade-offs such as build vs reuse, big-bang vs incremental, or new technology vs boring technology
