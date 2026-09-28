---
name: simplifying-code
description: Behavior-preserving cleanup of working code for readability, duplication and needless complexity. Use when code works but is hard to read, after a feature lands and the diff feels heavy, when the user asks to clean up, tidy, simplify or de-duplicate, or when a review flags nesting, long functions, dead code or over-engineering.
license: Apache-2.0
metadata:
  version: "0.1.0"
  category: "build"
  sources: "addyosmani/agent-skills code-simplification (MIT); anthropics/claude-plugins-official code-simplifier (Apache-2.0); garrytan/gstack deslop-shared-libs (MIT); mattpocock/skills code-review (MIT)"
---

# Simplifying Code

Simplification changes how code says something, never what it does, and every change must make the code faster to understand, not just shorter.

## When to use

- A feature works and its tests pass, but the code is heavier than it needs to be
- Deep nesting, long functions, nested ternaries, unclear names, duplicated blocks, dead code
- Abstractions with one implementation, wrappers that only delegate, options nobody passes
- The user asks to clean up, tidy, simplify, or "deslop" recent work

**Not for:** code with no tests where behavior is unknown (use `refactoring-legacy-code` first); changing behavior or interfaces (use `designing-interfaces` and `test-driven-development`); a review of someone else's change (use `reviewing-code`); performance work (use `optimizing-performance`, since simpler is sometimes slower).

## Process

1. **Scope it.** Default to the code changed in this session or branch (`git diff <base>...HEAD --stat`). Widen only when the user asks. Unscoped cleanups make noisy diffs and hide regressions.
   Exit: a list of files and functions in scope.

2. **Pin the behavior.** Find the tests that cover the scope and run them as single files. If coverage is missing for something you plan to touch, add a characterization test first, or leave that code alone.
   Exit: a green test run that exercises every function you will change.

3. **Understand before removing (Chesterton's fence).** For anything that looks pointless, check `git log -L` or blame, its callers, and its error paths. Code that looks odd often exists for a platform quirk, a performance reason or an old incident.
   Exit: for each removal, you can say why the code existed and why that reason no longer applies.

4. **Pick changes from the catalog below**, and apply them **one at a time**. Re-run the scoped tests after each change. If a test fails, revert that change. Do not debug a refactor.
   Exit: each change has been applied and tested on its own.

5. **Extract shared code only when it is proven.** Before creating a helper to de-duplicate, find at least two real call sites (with file:line) that would use it, and check whether an existing utility already does the job. If you can't find two, don't extract. "No worthwhile extraction" is a valid result.

6. **Judge the result as a whole.** Compare before and after: is it easier to follow for someone new to the code? If the diff only moved complexity around, revert it.

**Keep refactors separate.** Don't mix simplification with feature or bug-fix changes in one diff. If the user has asked you to commit, commit each on its own.

## Catalog

| Signal | Change |
|---|---|
| Nesting 3+ levels deep | guard clauses and early returns |
| Nested ternaries | `if` chain, `switch`, or a lookup table |
| Boolean flag parameter | two named functions, or an options object |
| Same condition in several places | a named predicate |
| Function doing several jobs | split along its responsibilities |
| Generic names (`data`, `tmp`, `res2`) | names that say what the value holds |
| Comment explaining *what* | delete it, or rename so the code says it |
| Unreachable branch, unused export, commented-out block | delete it, after a repo-wide search confirms nothing uses it |
| Wrapper that only forwards | inline it and call the target directly |
| Interface or factory with one implementation and no second in sight | inline it (speculative generality) |
| Same fields always passed together | bundle them into one type |

**Don't over-simplify:** don't inline a helper that names a concept, merge two simple functions into one complex one, or trade clarity for fewer lines. Comments explaining *why* stay.

## Output

```
Scope: <files/functions>
Changes: <one line each: what changed, and the signal that justified it>
Skipped: <candidates left alone and why, e.g. no test coverage, reason for the code still applies>
Evidence: <test files run, result>
```

## Red flags

- A test had to change to pass after a "pure refactor"
- The diff touches files outside the agreed scope
- A new shared helper has only one caller
- Deleting code you haven't searched for callers of
- Several simplifications applied before re-running tests
- Line count went down but you had to re-read the new version twice
