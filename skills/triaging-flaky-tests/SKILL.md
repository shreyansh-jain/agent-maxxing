---
name: triaging-flaky-tests
description: Diagnosis discipline for non-deterministic tests. Use when a test passes and fails without code changes, fails only on CI or only in the full suite, fails depending on run order, time of day, timezone or machine load, or someone proposes adding a retry or a sleep to make it pass.
license: Apache-2.0
metadata:
  version: "0.1.0"
  category: "debug"
  sources: "obra/superpowers systematic-debugging condition-based-waiting and find-polluter (MIT); mattpocock/skills diagnosing-bugs (MIT); garrytan/gstack review testing specialist (MIT)"
---

# Triaging Flaky Tests

A flaky test is a deterministic bug whose trigger you have not controlled yet. Find the trigger, raise the failure rate until it can be debugged, then fix the cause instead of hiding it.

## When to use

- A test fails intermittently with no code change between runs
- It passes alone but fails in the full suite, or the reverse
- It fails on CI but never locally
- It fails near midnight, month end, DST changes, or in another timezone
- Someone suggests `retry(3)`, a longer timeout, `sleep`, or `.skip` to get the build green

**Not for:** a test that fails every time (use `debugging-systematically`); a red CI job where you have not yet confirmed the failure is intermittent (use `fixing-ci-failures`).

## The rule

```
NO RETRY, SLEEP, OR SKIP UNTIL THE NON-DETERMINISM HAS A NAMED SOURCE
```

Violating the letter of the rule is violating the spirit of the rule. A retry does not fix a flaky test. It hides a race that users will hit in production too.

## Process

1. **Confirm and measure the flake rate.** Run the one test (a single spec file, never the whole suite, serially, one worker) many times:
   `bash scripts/rerun_until_fail.sh 50 <single-test-command>`
   Exit: a measured rate ("7/50 failed") and the saved output of at least one failure. At 0/50, add stress (step 3) before you decide it is not flaky.

2. **Classify the failure.** Read the failure output and compare it against a passing run. Use [causes.md](references/causes.md) to put it in one class: timing/async, order dependence or shared state, time and date, randomness, concurrency, external dependency, resource limits, or environment difference.
   Exit: one class named, with the evidence that points to it.

3. **Raise the reproduction rate.** Make the suspected trigger more likely instead of waiting for luck. Examples: run under CPU stress or with `taskset` pinned to one core; inject a delay at the suspected race point; freeze the clock to 23:59:59 or the DST boundary; set `TZ=Pacific/Kiritimati`; fix the random seed and then sweep it; throttle the network stub.
   Exit: the failure reproduces at a high enough rate (above ~30%) that one change can be judged in a few runs.

4. **For order dependence, find the polluter.** Run each earlier spec file together with the victim, one pair at a time, serially:
   `bash scripts/find_polluter.sh "<runner command>" <victim-spec> <candidate-spec>...`
   Exit: the one spec file whose state leaks, and the shared thing it leaks (global, singleton, DB row, env var, temp file, module cache, mocked clock).

5. **Fix the cause, not the symptom.**
   - Timing: wait for the condition, not a duration. Poll for the state, event or element you need, with a timeout that fails loudly and names what it waited for.
   - Shared state: give each test its own fixture, reset the state in teardown, or isolate the resource (unique DB schema, temp dir, fresh module).
   - Time and randomness: inject a clock and a seed. Never read the wall clock or an unseeded RNG inside logic under test.
   - Real race in production code: fix the code, and keep the test as the regression guard.
   Exit: the fix names the source you found in step 2 or 4.

6. **Prove it.** Re-run the stressed loop from step 3 and the plain loop from step 1 with the fix in place.
   Exit: 0 failures at the same run count and stress that previously failed. Report the before and after rates.

A timeout or retry is legitimate only when the thing under test is *itself* timing behavior (debounce, backoff, rate limit) or an external system you do not control. Then write down why, next to it.

**Quarantine is not a fix.** If you must unblock others before the fix lands, and the user agrees, quarantine the test with a tracked reason and the measured flake rate. Say plainly that it is quarantined, not fixed.

## Output

```
Test: <path::name>
Flake rate: <before> → <after> (<N> runs, <conditions>)
Class: <timing | order | time | randomness | concurrency | external | resources | environment>
Source: <the specific shared state / race / clock read, file:line>
Fix: <what changed>; retries or sleeps added: none | <which, and why they are legitimate>
```

## Rationalizations

| Excuse | Reality |
|---|---|
| "It's just CI being slow, bump the timeout" | A slower machine exposed a race. The race is still there on fast machines, just rarer. |
| "Add a retry, it passes the second time" | Passing on retry shows the bug is intermittent. It says nothing about whether it is fixed. |
| "I ran it 5 times and it passed, it's fixed" | At a 10% flake rate, 5 clean runs happen 59% of the time. Measure at the same run count and stress that reproduced it. |
| "Run the whole suite in parallel to reproduce faster" | That changes several variables at once and can bring down the machine. Loop the one file serially and add targeted stress. |
| "It's a test problem, not a product problem" | Check first. Order-dependent and timing failures are often real concurrency bugs. |

## Red flags

- A diff for a flaky test that adds `sleep`, `retry`, `waitForTimeout`, or `.skip` and nothing else
- "Can't reproduce" after fewer than 30 runs, or with no stress added
- Running the full suite or parallel workers to hunt a single flake
- A fix that does not name which shared state, clock, seed, or race it removed

## References

- [causes.md](references/causes.md): open at step 2 to classify the failure and pick a stressor
- [scripts/rerun_until_fail.sh](scripts/rerun_until_fail.sh): `bash scripts/rerun_until_fail.sh <runs> <command...>` runs a command serially and reports the fail rate
- [scripts/find_polluter.sh](scripts/find_polluter.sh): `bash scripts/find_polluter.sh "<runner>" <victim> <candidates...>` finds which spec leaks state into the victim
