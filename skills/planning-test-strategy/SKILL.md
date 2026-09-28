---
name: planning-test-strategy
description: Risk-based test strategy for a feature, service or system. Use when deciding what to test and at which level, planning tests for a new feature or rewrite, auditing a slow or untrustworthy suite, or setting coverage, flake and CI-gate policy.
license: Apache-2.0
metadata:
  version: "0.1.0"
  category: "build"
  sources: "levnikolaevich/claude-code-skills ln-32-test-strategy-planner (MIT); addyosmani/agent-skills test-driven-development (MIT); mattpocock/skills tdd (MIT); garrytan/gstack qa (MIT)"
---

# Planning Test Strategy

Every test should earn its place by catching a specific defect that matters and that nothing cheaper already catches. Start from risks, not from test types.

## When to use

- A new feature, service, rewrite or migration needs a test plan before implementation
- "What should we test here?" / "Is this enough coverage?"
- The suite is slow, flaky or distrusted, and needs pruning or rebalancing
- Setting policy: coverage targets, which tests gate merges, nightly runs, flake budget

**Not for:** writing the next failing test inside the red-green loop (use `test-driven-development`); building browser or API journey tests (use `testing-end-to-end`); fixing one intermittently failing test (use `triaging-flaky-tests`); CI job configuration (use `setting-up-ci-pipelines`).

## Process

1. **Read what exists.** Find the requirements and acceptance criteria. Detect runners, test directories, fixtures, factories, CI gates, coverage reports and contract tests. Map each existing test that touches the scope to the behavior it proves. Coverage shows which lines ran; it does not show that an assertion would fail on a bug.
   Exit: an inventory of existing tests per behavior, marked proven, partial or missing.

2. **Build the risk map.** Trace each critical flow from trigger to durable or user-visible outcome. Mark what is expensive to get wrong: money, auth and permissions, data integrity, destructive or irreversible actions, public contracts, migrations. For each flow, list plausible defect classes: rejected valid input, accepted invalid input, boundary error, partial failure, duplicate delivery, ordering, timeout and retry, concurrency, rollback.
   Exit: a ranked list of risks, each rated by impact and likelihood (high / medium / low), with the reasoning in one line.

3. **Pick the cheapest level that catches each risk.** Use the table below. Push each check to the smallest test that can see the defect. Only add a larger test when the defect lives in the wiring between parts.
   Exit: every high and medium risk has a level and a named oracle (the observation that would fail).

4. **Decide what not to test.** Framework and library behavior, trivial getters, generated code, and states no user can reach get no tests. Record each exclusion as an accepted risk, so "no test" is a decision rather than an omission. Mark redundant or implementation-coupled tests for merging or deletion.
   Exit: an explicit exclusions list.

5. **Plan data and environments.** Use synthetic data only; never production personal data. Each test creates what it needs through factories, isolated per test. List which real dependencies are needed (database, queue, browser) and which may be faked, and check that no fake skips the failure mode the test claims to prove.
   Exit: each test row names its setup and environment.

6. **Place tests in CI.** Pre-merge runs fast, deterministic tests that cover release-critical risks. Slow or broad checks (full E2E matrix, load, mutation, fuzzing) run nightly or before release. A test that is not trusted is deleted or fixed. Quarantine is a short-lived holding state with an owner and a date.
   Exit: every row has a gate: pre-merge, nightly, pre-release, or manual.

## Test levels

| Level | Size (resources) | Catches | Cost |
|---|---|---|---|
| Unit | small: one process, no I/O | logic, boundaries, pure transforms | ms, very stable |
| Property / fuzz | small | invariants over huge input spaces (roundtrip, idempotence, ordering) | seconds |
| Integration | medium: localhost, real DB or queue | queries, transactions, serialization, wiring | seconds |
| Contract | medium | provider/consumer API drift between services | seconds |
| End-to-end | large: full stack, browser | critical journeys working as users see them | minutes, flaky risk |
| Migration rehearsal | large | schema and data changes on production-shaped data | minutes |
| Load / soak | large | capacity, latency under concurrency, leaks | long, pre-release |
| Security | varies | authz bypass, injection, secrets, dependency CVEs | varies |

Choose the shape to fit the product, not a slogan. Logic-heavy libraries want a wide base of unit and property tests. CRUD-heavy web apps get most of their confidence from integration tests (the "trophy"). Keep E2E to a handful of revenue- and trust-critical journeys.

## Output

```
Scope: <feature/system>  Existing: <N tests mapped, key gaps>
| Risk | Impact | Level | Test (new/keep/update/delete) | Oracle | Data/env | Gate |
|---|---|---|---|---|---|---|
Excluded (accepted risk): <item: reason>
Policies: coverage <signal, e.g. "no drop on changed files">, flake budget <e.g. zero tolerated in pre-merge>, runtime budget <pre-merge ≤ N min>
Open questions: <only those that change level or priority>
```

## Rationalizations

| Excuse | Reality |
|---|---|
| "Let's aim for 90% coverage" | Coverage counts executed lines, not caught bugs. Use it to find untested areas, never as the goal. |
| "E2E tests catch everything, write those" | They catch wiring bugs slowly and flakily. Most defects are cheaper to catch lower down. |
| "Mock the database, it's faster" | Then the test cannot catch the query, transaction or constraint bugs where the risk usually is. |
| "Test every function" | Tests coupled to internals break on every refactor and prove nothing a user sees. |
| "We'll add tests after launch" | The risks you mapped do not wait. Plan at least the high-impact rows now. |

## Red flags

- A test row with no named defect or oracle
- Coverage percentage used as the success criterion
- More E2E tests than critical user journeys
- Tests reading production data or shared, mutable fixtures
- Retries or quarantine used as the flake policy, with no owner or expiry
- Pre-merge suite growing past its runtime budget with no pruning

## References

- [risk-catalog.md](references/risk-catalog.md): open at step 2 to list defect classes per kind of system (API, UI, data pipeline, payments, auth, async jobs)
