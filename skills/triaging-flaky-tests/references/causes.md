# Flake causes, signatures, and stressors

| Class | Signature in the failure | Stressor to raise the rate | Real fix |
|---|---|---|---|
| Timing / async | "element not found", "expected called once, called 0 times", unresolved promise, missing `await` | CPU stress, pin to one core, inject delay at the async boundary | await the condition (poll with a named timeout); add the missing `await`; flush the queue explicitly |
| Order dependence | passes alone, fails after a specific other file | run each candidate before the victim (`find_polluter.sh`); randomize order with a fixed seed | reset in teardown; per-test fixtures; no module-level mutable state |
| Shared resource | unique-constraint errors, "file exists", port in use, stale cache hit | run two copies at once, *only* when checking this class | unique names per test (schema, temp dir, port 0); clean up in `finally` |
| Time / date | fails near midnight, month end, DST, leap day, or in one timezone | freeze the clock at the boundary; `TZ=` far-off zones | inject a clock; compare in UTC; avoid "today" computed twice |
| Randomness | fails for some generated data | log the seed; sweep seeds 1..1000 | fix the seed in tests; fix the code path the bad seed exposes |
| Concurrency | lost update, deadlock, nondeterministic ordering of results | loop 100× with added parallelism *inside the code under test* | real synchronization in product code; sort before asserting on unordered results |
| External dependency | network timeouts, 429s, DNS errors | block the network; add latency to the stub | stub at the boundary; contract test separately |
| Resource limits | OOM, "too many open files", slow GC pauses | lower memory or ulimit | close handles; stream instead of loading; fix the leak |
| Environment | CI only: different OS, locale, file ordering, case sensitivity, env vars | reproduce in the CI image locally; diff `env` output | stop depending on the implicit environment; set it explicitly |

## Waiting for a condition, not a duration

```typescript
async function waitFor<T>(check: () => T | undefined | null | false, what: string, timeoutMs = 5000): Promise<T> {
  const start = Date.now();
  for (;;) {
    const value = check();
    if (value) return value;
    if (Date.now() - start > timeoutMs) throw new Error(`timed out after ${timeoutMs}ms waiting for ${what}`);
    await new Promise((r) => setTimeout(r, 10));
  }
}

// before: await sleep(200); expect(queue.done).toBe(true);
await waitFor(() => queue.done, "queue to drain");
```

Test frameworks usually ship this (`waitFor`, `expect.poll`, `eventually`, `await_until`). Use the framework's version when there is one.

## Reading the math on "it passed N times"

If a test fails with probability *p*, then *n* clean runs happen by chance with probability (1 − p)ⁿ. At p = 0.1, 10 clean runs happen 35% of the time and 30 clean runs 4% of the time. So verify a fix at the same run count and stress that reproduced the failure, and report both numbers.
