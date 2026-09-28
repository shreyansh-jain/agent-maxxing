---
name: implementing-incrementally
description: Discipline for building features in thin, verified slices, executing a plan task by task, and keeping the codebase working between steps. Use when executing an implementation plan or tickets, when implementing a feature or change that touches more than one file, when about to write a large amount of code at once, or when picking up the next task in a multi-step change.
license: Apache-2.0
metadata:
  version: "0.1.0"
  category: "build"
  sources: "obra/superpowers executing-plans (MIT); addyosmani/agent-skills incremental-implementation (MIT); mattpocock/skills implement (MIT)"
---

# Implementing Incrementally

Change one logical thing, prove it works, and record where you are before you touch the next thing. The codebase is never broken for longer than one slice.

## When to use

- Executing an approved plan, spec, or set of tickets
- Implementing any change that touches more than one file
- You are about to write hundreds of lines before running anything
- Resuming a multi-step change, possibly after context compaction

**Not for:** deciding what to build or in what order (use `planning-implementation`); the test-first loop inside a slice (use `test-driven-development`); farming independent tasks out to subagents (use `dispatching-subagents`).

## The rule

```
NO NEXT SLICE UNTIL THE CURRENT ONE IS VERIFIED AND RECORDED
```

Violating the letter of the rule is violating the spirit of the rule.

## Process

1. **Set up the ledger.** Read the plan and the spec in full. Create or open a progress ledger next to the plan (for example `docs/plans/<plan>.progress.md`), unless the repo already has another place for it. Its first line names the plan. If the ledger already records completed tasks, trust it and `git log` over your own memory, and resume at the first task that isn't done. Before starting, check that the build and tests are green. If they aren't, report that first: otherwise you can't tell your breakage from what was already broken.
   Exit: the ledger exists and the baseline state is known.

2. **Take the smallest complete slice.** One task from the plan, or, with no plan, the thinnest end-to-end path that shows value. Ask what the simplest thing is that could work. Three similar lines beat a premature abstraction.
   Exit: you can say in one sentence what this slice makes true.

3. **Implement it test-first** at the plan's seam (**REQUIRED:** the `test-driven-development` skill). Touch only what the slice needs. If you notice something unrelated worth fixing, write it under "Noticed, not touched" in the ledger and leave the code alone.
   Exit: the slice's test went red, then green.

4. **Verify the slice.** Run the slice's test, then the typecheck or build, then the tests nearest the change. Save the full suite for the end, or run it earlier only if the project's norms and the user's instructions allow it. Compare actual output with the plan's `Expected:` lines. A mismatch means either the plan is wrong (make a ruling, step 5) or the code is wrong (use `debugging-systematically`).
   Exit: fresh passing output for every check you claim.

5. **Rule instead of stalling.** When the plan is ambiguous, contradicts itself, or turns out wrong in a small way, decide and keep going. The spec outranks the plan, and your judgment settles what neither covers. Record each decision as: `Ruling: <decision> — <why> — <cost if wrong>`. A deviation from the plan with no ruling recorded is a decision made in secret.
   Stop and ask only for:
   - an irreversible or destructive operation;
   - a security-sensitive change;
   - a side effect outside the working tree (a push, publish, deploy, or shared-branch merge);
   - a plan so broken that every way forward is a guess.

6. **Record and checkpoint.** Append `Task N: complete — <what is now true> — tests: <command> → <result>` to the ledger. If the user has asked you to commit, make one atomic commit for this slice. Otherwise, leave the working tree in a state that builds and say what is pending. Unfinished user-facing behavior goes behind a flag that defaults to off.
   Exit: the ledger line has been written. Then go to the next slice.

7. **Finish.** Once every task is done, run the full verification the project uses, re-read the spec requirement by requirement against the result, and get a review of the whole change (use `reviewing-code`, from a fresh context if possible). Report what is done, any rulings, anything noticed but not touched, and what is left for the user, such as commits or a PR.

Keep narration to one short line between tool calls. The ledger and the tool output carry the record.

## Rationalizations

| Excuse | Reality |
|---|---|
| "I'll write it all, then test it all" | The bugs pile up and hide each other. Slice-sized verification finds each one where it was introduced. |
| "It's faster to fix this nearby mess while I'm here" | That mixes concerns into the diff and breaks review. Note it; don't touch it. |
| "The plan is slightly off, I'll ask before continuing" | Small defects call for a recorded ruling, not a stall. Save questions for the four stop conditions. |
| "I remember where I was" | After compaction you don't. The ledger and git history do. |
| "Tests are green so the task is done" | Done means the acceptance criterion is met and recorded, not only that tests pass. |

## Red flags

- More than one slice's worth of uncommitted, unverified change
- The diff touches files the task doesn't name
- A plan deviation that no ruling explains
- Re-implementing a task whose ledger line already exists
- "Should work" in a ledger line instead of a command and its result
- The project doesn't build between two slices
