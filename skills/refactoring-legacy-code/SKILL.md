---
name: refactoring-legacy-code
description: Safe change of untested or poorly understood code using characterization tests, seams and small reversible steps. Use when code must change but has little or no test coverage, when behavior is known only by what it does today, when a large module or rewrite is being considered, or when the user calls the code legacy, fragile, or scary to touch.
license: Apache-2.0
metadata:
  version: "0.1.0"
  category: "build"
  sources: "mattpocock/skills codebase-design (MIT); mattpocock/skills improve-codebase-architecture (MIT); addyosmani/agent-skills deprecation-and-migration (MIT); addyosmani/agent-skills code-simplification (MIT)"
---

# Refactoring Legacy Code

Legacy code is code without tests. To change it safely, first pin down what it *does* today, then change it in steps small enough that each one can be checked and undone.

## When to use

- You must change code with little or no test coverage
- Nobody can say for sure what the code should do, only what it does now
- A function or class is too entangled to test: it creates its own dependencies, uses globals, or talks directly to the DB and network
- Someone proposes a rewrite of a large module
- The user calls the code fragile, legacy, scary, or "don't touch it"

**Not for:** tidying code that is already well tested (use `simplifying-code`); getting oriented in an unfamiliar repo before any change is planned (use `onboarding-to-codebases`); replacing a library or framework version (use `upgrading-dependencies`); new behavior on code with good tests (use `test-driven-development`).

## The rule

```
NO CHANGE TO UNTESTED BEHAVIOR UNTIL A CHARACTERIZATION TEST PINS IT
```

Violating the letter of the rule is violating the spirit of the rule. If you can't pin a behavior, you can't claim you preserved it.

## Process

1. **Find the change point and its blast radius.** Name the exact function where the new behavior must go. List its callers (search for the symbol, including dynamic uses: reflection, string dispatch, templates, config) and what it touches (DB, files, network, globals).
   Exit: the change point, its callers, and its side effects are written down.

2. **Find a seam.** A seam is a place where you can swap behavior without editing the code under test. Prefer them in this order:
   - a parameter or constructor argument you can pass a fake into;
   - an overridable method (subclass in the test);
   - a module or import boundary you can substitute (dependency injection, module mocking at the boundary);
   - a config or environment switch.
   If none exists, create the smallest one with a mechanical, low-risk edit (see [breaking-dependencies.md](references/breaking-dependencies.md)). Use the IDE's or language server's automated refactorings wherever you can.
   Exit: the change point can be called from a test with its external dependencies replaced.

3. **Write characterization tests.** Call the code with realistic inputs and assert on **whatever it does now**, including behavior that looks wrong. Start with an assertion you expect to fail, read the actual value from the failure, and paste that value in as the expected one. Cover the paths your change will touch, plus the edges: empty input, nulls, the error paths. For large outputs, use a golden file (approval test).
   Suspected bugs get pinned as they are, with a name like `test_currently_rounds_negative_totals_up`, and are reported to the user. Do not fix them silently.
   Exit: the tests are green on the unchanged code, and they go red when you deliberately break the code path (check this once).

4. **Make the change in small, reversible steps.** Each step either refactors (behavior stays the same, tests stay green) or changes behavior (a new test first, per `test-driven-development`). Never both in one step. Run the relevant test files after every step.
   When adding new logic to a tangled function, **sprout** it: write it as a new, tested function, and add one call to it from the old code. To add behavior around an existing call, **wrap** it: write a new function that calls the old one and adds the new logic.
   Exit: the change is made, and every step left the tests green.

5. **Replace rather than rewrite.** For a large module, don't do a big-bang rewrite. Use a **strangler**: route one caller or one use case at a time to the new implementation, behind a switch that can go back to the old one. Keep both until the old path has no traffic, then delete it.
   Exit: the plan migrates one caller at a time, and each migration is reversible.

6. **Leave it better tested than you found it.** Keep the characterization tests. Rename them to describe intended behavior once the user confirms that behavior is correct.

## Output

```
Change point: <file:function>, callers: <n> (<list or path to list>)
Seam used: <parameter / override / module boundary / new seam: how>
Characterization tests: <paths>, covering <paths/edges>; verified red on deliberate break
Suspected existing bugs (pinned, not fixed): <list>
Steps: <refactor vs behavior change, in order>
```

## Rationalizations

| Excuse | Reality |
|---|---|
| "It's faster to rewrite it cleanly" | Rewrites lose undocumented behavior that callers depend on. Strangle it one caller at a time. |
| "I'll just be careful" | Being careful doesn't show you behavior you didn't know about. A test does. |
| "The current behavior is obviously a bug, I'll fix it while I'm here" | Someone may depend on it. Pin it, report it, and fix it as a separate, deliberate change. |
| "It's too tangled to test" | Then the first change is making a seam, not changing the logic. |

## Red flags

- Editing the logic before any test calls it
- A characterization test whose expected value you wrote from what the code *should* do
- A "refactor" commit that also changes behavior
- A plan that switches every caller at once
- Deleting code because it "looks unused" without a search for dynamic references

## References

- [breaking-dependencies.md](references/breaking-dependencies.md): open when the code can't be called from a test because it constructs or reaches for its own dependencies
