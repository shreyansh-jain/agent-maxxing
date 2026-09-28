# Building a feedback loop

The loop is the one command you re-run after every change. A tight loop is red-capable, deterministic, fast, and runs without a human.

## Loop types, cheapest first

| Loop | Build it when | Shape |
|---|---|---|
| Failing test | a test seam reaches the bug | `pytest tests/test_x.py::test_symptom -x` |
| HTTP script | the bug shows at an API | `curl -sf localhost:3000/api/x -d @payload.json \| jq '.total'` compared against the expected value |
| Golden diff | a CLI or batch job gives wrong output | `./tool < fixture.in \| diff - fixture.expected` |
| Headless browser | the bug is in the UI | a Playwright script that asserts on the DOM, console errors, or a network response |
| Replay | the bug needs real input | save the real request or event to disk, then feed it straight into the handler |
| Throwaway harness | the system is too big to boot | import one module, stub its collaborators, call the function |
| Property / fuzz | the output is "sometimes wrong" | run 1,000 random inputs and assert an invariant (roundtrip, ordering, conservation) |
| Bisection | a good and a bad state are known | `git bisect run <loop>` (see `scripts/bisect_run.sh`) |
| Differential | two versions or configs disagree | run the same input through both and diff the outputs |
| Human in the loop | a person must click, as a last resort | a script that prints each step, waits for Enter, and captures the output |

## Tightening

- **Faster:** skip unrelated setup, cache fixtures, run one test instead of the file.
- **Sharper:** assert the exact wrong value the user reported, not "no exception".
- **Deterministic:** freeze the clock, seed the RNG, use a temp directory, stub the network.

A deterministic 2-second loop is worth more than a flaky 30-second one.

## Non-deterministic bugs

Don't aim for a clean repro. Aim to raise the reproduction rate. Loop the trigger 100×, run the copies in parallel, add CPU or IO stress, and shrink timing windows with injected delays. A bug that fails 50% of the time can be debugged; one that fails 1% of the time cannot. Keep raising the rate first. If it's a test that only fails sometimes, switch to the `triaging-flaky-tests` skill.

## When no loop is possible

Say so. List what you tried. Ask for one of these:
1. access to an environment that reproduces the bug;
2. a captured artifact (HAR file, log excerpt, core dump, screen recording with timestamps), with secrets redacted;
3. permission to add temporary, tagged instrumentation where the bug occurs.

Do not move on to hypotheses without a loop.
