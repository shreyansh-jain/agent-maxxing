---
name: testing-end-to-end
description: Reliable browser and API end-to-end tests for critical user journeys. Use when writing or fixing Playwright, Cypress or similar E2E tests, adding a journey test for a feature, or when E2E tests are slow, brittle, or break on unrelated UI changes.
license: Apache-2.0
metadata:
  version: "0.1.0"
  category: "build"
  sources: "anthropics/skills webapp-testing (Apache-2.0); wshobson/agents e2e-testing-patterns (MIT); addyosmani/agent-skills test-driven-development, browser-testing-with-devtools (MIT); garrytan/gstack qa (MIT)"
---

# Testing End to End

An E2E test proves that one critical journey works the way a user experiences it. Keep them few, make them fully independent, and let them wait on conditions, never on time.

## When to use

- Adding a journey test: sign-up, checkout, onboarding, a core create/edit/delete flow
- Writing or fixing Playwright, Cypress, WebdriverIO or API-level journey tests
- E2E tests break whenever markup or copy changes, or are slow or order-dependent
- Verifying a UI change in a real browser before calling it done

**Not for:** deciding which journeys deserve E2E coverage at all (use `planning-test-strategy`); a test that passes and fails with no code change (use `triaging-flaky-tests`); unit or component tests in the red-green loop (use `test-driven-development`); accessibility audits (use `building-accessible-interfaces`).

## Process

1. **Check the tool, don't recall it.** Read the installed version from the lockfile and the project's E2E config (base URL, projects, retries, reporters, global setup). Check current APIs with `npx playwright --help` or the docs for that version. APIs for waits, fixtures and auth state change between majors.
   Exit: you know the runner, version, config file, and how the app server is started for tests.

2. **Name the journey and its outcome.** One test = one user goal, stated as the user would say it: "a returning customer can reorder from order history". Write down the observable end state (a confirmation message, a new row in a list, a received email in a test inbox).
   Exit: a one-line journey with a user-visible assertion at the end.

3. **Set up state through the back door.** Create users, data and permissions through API calls, seed scripts or factories, not by clicking through the UI. Each test creates its own uniquely named data (for example with a random suffix) and never depends on another test's leftovers. Log in once in global setup and reuse the saved auth state, except in the tests that exercise login itself.
   Exit: the test runs alone, in any order, on a fresh environment.

4. **Locate elements the way users do.** Prefer role plus accessible name (`getByRole('button', { name: 'Place order' })`), then label, placeholder or text. Use a `data-testid` only when there is no stable user-facing handle. Never use CSS classes, DOM position or XPath chains. A locator that cannot find an element by role often reveals an accessibility bug.
   Exit: no locator depends on styling or structure.

5. **Wait on conditions, never on time.** Use web-first assertions that retry (`await expect(locator).toBeVisible()`, `toHaveText`, `toHaveURL`) and wait for specific network responses when an action triggers one. `sleep`, `waitForTimeout` and fixed delays are banned. They make tests slow when they are long enough and flaky when they are not.
   Exit: `grep -rnE "waitForTimeout|sleep\(|cy\.wait\([0-9]" <e2e dir>` finds nothing new.

6. **Mock only at the edge you don't own.** Hit your own frontend and backend for real. Stub third-party services (payments, email, maps) at the network boundary or with the vendor's sandbox, and say which ones are stubbed. A journey that mocks your own API is a component test in disguise.
   Exit: the list of stubbed boundaries is written in the test file or suite README.

7. **Make failures diagnosable.** Enable trace, screenshot and video capture on failure (on first retry, if the runner supports it) and keep the artifacts in CI. Assertion messages name the journey step.
   Exit: a deliberately broken assertion produces a trace that shows the failing step.

8. **Run it narrowly, then prove it.** Locally, run the single spec file headless with one worker (for example `npx playwright test tests/e2e/reorder.spec.ts --workers=1`). Run it 3–5 times in a row to catch obvious nondeterminism. Leave parallelism and sharding to CI. Watch the test fail once, by breaking the expected outcome, so you know the assertion can catch a regression.
   Exit: repeated runs pass, and a broken expectation fails at the right step.

## Output

```
Journey: <user goal>  Spec: <path>
Setup: <API/seed/factory>, auth: <reused state | login under test>
Stubbed boundaries: <list or none>
Evidence: <command> → N/N passes; broken-expectation run failed at step "<step>"
```

## Rationalizations

| Excuse | Reality |
|---|---|
| "Just add a 2-second wait, it's timing" | It will be too short on a slow CI runner and wasted time on a fast one. Wait for the condition that actually signals readiness. |
| "Click through signup to create the user" | That tests signup in every test, and makes every test fail when signup breaks. Seed through the API. |
| "The class name is the only thing unique" | Add an accessible name or a test id. Styling changes should never break tests. |
| "Run the whole E2E suite locally to be safe" | It is slow, and parallel local runs fight over ports and data. Run the one spec; CI runs the rest. |
| "Retries will handle the flakiness" | Retries hide real races. Fix the wait or the data isolation. |

## Red flags

- `waitForTimeout`, `sleep`, or `cy.wait(<number>)` in a test
- Tests that must run in a specific order, or share a user account
- Locators with `nth-child`, generated class names, or deep CSS paths
- An E2E test for every edge case of a form (push those down to unit or component tests)
- Mocking your own backend in a "journey" test
- A new E2E test that was never seen failing

## References

- [patterns.md](references/patterns.md): open when setting up auth-state reuse, network waits, test-data factories, or CI sharding
