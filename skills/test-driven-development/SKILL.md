---
name: test-driven-development
description: Test-first development discipline (red, green, refactor) for features, bug fixes and behavior changes. Use when implementing new behavior, fixing a reported bug, changing existing behavior, or when the user mentions TDD, test-first, or red-green-refactor.
license: Apache-2.0
metadata:
  version: "0.1.0"
  category: "build"
  sources: "obra/superpowers test-driven-development (MIT); mattpocock/skills tdd (MIT); addyosmani/agent-skills test-driven-development (MIT)"
---

# Test-Driven Development

A test you never watched fail proves nothing, so every behavior starts as a failing test at an agreed seam.

## When to use

- Adding a feature, endpoint, function, or branch of logic
- Fixing a reported bug: the failing test *is* the proof the bug exists
- Changing behavior that existing callers rely on
- The user asks for TDD, test-first, or red-green-refactor

**Not for:** finding the cause of a bug you cannot yet reproduce (use `debugging-systematically`, then come back here for the fix); adding tests around untested legacy code before changing it (use `refactoring-legacy-code`); tests that fail intermittently (use `triaging-flaky-tests`). Throwaway prototypes, generated code and pure config need no TDD. Ask the user if one of those is the case; do not decide it alone.

## The rule

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

Violating the letter of the rule is violating the spirit of the rule. If you wrote code before its test, delete it and start from the test. Do not keep it "as reference" and do not adapt it. Writing it again from the test is fast, and it is the only way the test gets to prove something.

## Process

1. **Discover how this repo tests.** Read the build file, test config, CI workflow and neighbouring tests. Find the command that runs **one test file** (`pytest tests/test_x.py`, `npx vitest run src/x.test.ts`, `go test ./pkg/x -run TestY`, `cargo test x::`). Use the checked-in wrappers (`./gradlew`, `make test`) over global tools. Never assume `npm test`.
   Exit: you have run the single-file command once and seen it execute.

2. **Agree the seams.** A seam is the public interface where behavior is observed: a function's return value, an HTTP response, a CLI's output, an emitted event. Write down which seams you will test and confirm them with the user when they are present. Test through seams, never through internals.
   Exit: a short list of seams, each with the behaviors to cover.

3. **RED: one failing test.** Write one test for one behavior, named as a sentence (`rejects an expired coupon`). Before writing the assertion, name the production change that should make this test fail. The expected value comes from an independent source: a literal, a worked example, or the spec. Never recompute it with the code under test.
   Run the single file. Exit: it **fails**, it fails **for the reason you predicted** (the feature is missing, not a typo or an import error), and the failure message is readable.

4. **GREEN: the least code that passes.** Hard-code, special-case, whatever is smallest. Do not add options, parameters or branches that no test demands.
   Run the single file. Exit: it passes, and the output is clean (no new warnings or errors).

5. **REFACTOR while green.** Remove duplication, improve names, extract helpers. Change no behavior. Re-run after each change.
   Exit: the file is still green and the code reads cleanly.

6. **Next slice.** Pick the next behavior and go back to step 3. Work in vertical slices: one test, then its implementation. Never write all the tests up front, because a batch of tests describes imagined behavior and fixes a structure before you understand it.

7. **Close out.** Run the tests for every file you touched. Then run the broader suite the way the user's instructions allow: some environments forbid whole-suite runs, and in those, say which files you ran and which you did not. Hand the evidence to `verifying-before-completion`.

**Bug fixes (prove-it pattern).** Write a test that reproduces the report at the seam where users hit it, watch it fail with the user's symptom, fix, and watch it pass. Then revert the fix, confirm the test goes red again, and restore the fix. A regression test that passes without the fix protects nothing.

## Good tests, briefly

- **Behavior, not implementation.** The test survives a rewrite of the internals. If refactoring breaks it while behavior is unchanged, it is coupled to the implementation.
- **Mock only at system boundaries**: third-party APIs, the clock, randomness, and sometimes the network or disk. Never mock your own modules. Prefer a real test database over a mocked repository.
- **One behavior per test.** An "and" in the name means you should split it.
- **No change detectors.** Asserting a constant's value or an exact log string fails on every deliberate change and misses real bugs. Test the behavior that depends on the value instead.

## Rationalizations

| Excuse | Reality |
|---|---|
| "Too simple to need a test" | Simple code breaks too, and the test takes 30 seconds. |
| "I'll add tests after" | Tests written after the code pass immediately, which proves nothing. They test what you built, not what was needed. |
| "I already tested it manually" | Manual testing leaves no record and can't be re-run. It won't catch the next regression. |
| "Deleting an hour of code is wasteful" | That's sunk cost. Keeping code you can't trust is the real waste, and rewriting from the test is quick. |
| "This test is hard to write" | Hard to test means hard to use. Fix the interface (`designing-interfaces`). |
| "I'll run the full suite each cycle to be safe" | It's slow and can hang the machine. Run the single file each cycle and the broader set once at the end. |
| "The test passed on the first run, great" | Then it tests existing behavior or nothing at all. Make it fail first. |

## Red flags

- Production code exists and no failing test was run for it
- The test passed the first time it ran
- You can't say why the test failed
- The expected value is computed by the same helper the code uses
- `jest.fn()`, `mock.patch` or a stub standing in for your own module
- Several tests written before any implementation

## References

- [writing-good-tests.md](references/writing-good-tests.md): open when choosing what to assert, whether to mock, or how to structure a test file
