# Tracing to the root cause

Symptoms show up where bad data is *used*. Causes live where bad data is *made*. Trace backwards until you reach the place where a correct input became an incorrect output.

## Backward trace

1. Start at the failing line and write down the bad value (`order.total = NaN`).
2. Ask where that value came from: which caller passed it, and which function returned it.
3. Go one frame up and check the value there. If it is already bad, repeat.
4. Stop at the first frame where every input is good and the output is bad. That frame holds the root cause.

When the call stack is not available (async code, queues, jobs), add one tagged log per boundary that prints the value and a correlation id. Then read the logs in order.

## Where to look when the trace goes cold

| Evidence | Command |
|---|---|
| What changed recently | `git log --since="3 days" -p -- <path>` |
| Who changed this line and why | `git log -L <start>,<end>:<file>` |
| Dependency drift | diff the lockfile against the last known-good commit |
| Config and env drift | compare env vars and feature flags between a working env and the broken one |
| A working sibling | find similar code that works, then diff the two line by line |

## Fix at the source, guard at the boundaries

Fix the frame where the value first went bad. If bad data can reach that frame from outside (user input, network, disk), also add validation at that entry point so the next bad value fails loudly and early.

Do not add a null check or a default where the symptom appeared. That hides the bug and moves it somewhere else.
