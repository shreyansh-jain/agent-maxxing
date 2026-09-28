---
name: optimizing-performance
description: Measure-first performance work across backend services, databases and frontends. Use when an endpoint, query, job, page or build is slow, latency or memory regressed, Core Web Vitals or a performance budget is failing, costs rise with load, or someone wants to optimize code before measuring it.
license: Apache-2.0
metadata:
  version: "0.1.0"
  category: "operate"
  sources: "addyosmani/agent-skills performance-optimization (MIT); getsentry/skills django-perf-review (Apache-2.0); garrytan/gstack benchmark and review performance specialist (MIT); mattpocock/skills diagnosing-bugs (MIT)"
---

# Optimizing Performance

Measure, find the single biggest cost, remove it, and measure again. An optimization without a before-and-after number is a guess that added complexity.

## When to use

- "This endpoint / query / page / job / build is slow"
- A latency, memory, CPU or bundle-size regression after a change or upgrade
- Failing a budget: p95 SLO, Core Web Vitals, cold start, CI time, cloud cost
- Preparing for a known load increase
- Someone proposes caching, memoizing, rewriting or parallelizing "for performance"

**Not for:** a functional bug that happens to be slow to reproduce (use `debugging-systematically`); adding metrics, traces and dashboards (use `instrumenting-observability`); a production outage caused by load (use `responding-to-incidents` first).

## The rule

```
NO OPTIMIZATION WITHOUT A BASELINE, A TARGET, AND A PROFILE THAT POINTS AT IT
```

Violating the letter of the rule is violating the spirit of the rule. Intuition about where time goes is wrong often enough that acting on it without a profile is a coin toss.

## Process

1. **Define the metric and the target.** Name the user-visible number (p95 latency of `GET /orders`, LCP on `/checkout`, peak RSS of the import job, CI wall time) and the goal ("p95 < 300 ms at 50 rps"). If the user has no target, propose one and confirm it.
   Exit: one metric, one target, and the conditions it is measured under (data size, concurrency, device, network).

2. **Build a reproducible measurement.** Use the same input, realistic data volume, warm-up runs, and at least 10 iterations. Report the median and p95, not a single run. Measure an environment that resembles production (a production-sized dataset, production build flags). Where the system has real traffic, check production telemetry first. It often answers "where" for free.
   Exit: a command or script that prints the baseline number with its spread, and that you have run twice with consistent results.

3. **Profile to locate the cost.** Use the tool that matches the symptom, from [profiling.md](references/profiling.md): a CPU profiler or flame graph, a query log with counts and timings, `EXPLAIN (ANALYZE, BUFFERS)`, heap snapshots, or a network waterfall and performance trace. Break the total down into parts (DB x ms, serialization y ms, network z ms). Amdahl's law applies: optimizing a component that takes 5% of the time can remove at most 5%.
   Exit: the top one or two costs are named, with evidence and their share of the total.

4. **Change one thing.** Fix the dominant cost with the smallest change that addresses it. Typical fixes: batch an N+1, add an index shaped like the query, paginate an unbounded read, remove repeated work from a loop, parallelize independent I/O, stream instead of loading everything, cache a pure and expensive result with an explicit invalidation rule, split a bundle, or defer non-critical work. Behavior must not change. Keep the existing tests green.
   Exit: a single, reviewable change.

5. **Re-measure: keep or revert.** Run the same measurement under the same conditions. If the improvement is inside the noise, or the target metric moved but another one regressed (memory, write cost, freshness), revert or rethink.
   Exit: before/after numbers with spread, and a keep or revert decision.

6. **Guard the gain.** Add the cheapest check that would catch a regression: a query-count assertion in the endpoint test, an `EXPLAIN` plan check, a bundle-size budget, a benchmark with a threshold in CI, or an SLO alert. Record the numbers in the PR description.
   Exit: a guard exists, or you have noted why none is practical.

Repeat steps 3–6 until the target is met. Then stop. Optimizing past the target spends complexity budget on nothing.

## Where to look first

| Symptom | Measure first | Usual causes |
|---|---|---|
| One endpoint slow | query count and time per request; span breakdown | N+1, missing or wrong index, unbounded result, serialization of big graphs |
| Every endpoint slow at once | connection pool wait, CPU, GC, downstream latency | pool exhaustion, a noisy neighbor, a shared lock, a slow dependency |
| Slow under load only | throughput vs latency curve, lock waits | contention, synchronous I/O in async code, missing backpressure |
| Memory grows until restart | heap snapshots over time | unbounded caches, listeners never removed, whole-table loads |
| Batch job slow | per-stage timing | row-by-row writes, no bulk operations, one transaction per row |
| Page load slow | performance trace, network waterfall, bundle analysis | render-blocking assets, big bundles, request waterfalls, unoptimized images |
| Interactions laggy | long tasks on the main thread | heavy handlers, re-render storms, layout thrashing |

## Output

```
Metric: <name> under <conditions>. Target: <value>
Baseline: median <x>, p95 <y> (n=<runs>)
Profile: <cost 1> (<share>), <cost 2> (<share>). Evidence: <profile / plan / query log>
Change: <what, file:line>
After: median <x'>, p95 <y'> (n=<runs>); side effects checked: <memory, writes, freshness>
Guard: <test / budget / alert>
```

## Rationalizations

| Excuse | Reality |
|---|---|
| "Obviously the slow part is X" | Then the profile will confirm it in minutes. It often shows Y. |
| "Let's add a cache" | A cache adds staleness and invalidation bugs, and it hides the cost rather than removing it. Profile first, and cache only a measured, pure hotspot. |
| "One run showed it's 30% faster" | Single runs are noise. Compare medians over repeated runs under the same conditions. |
| "It's faster on my laptop with the dev database" | With 50 rows, every query is fast. Measure with production-like data volume. |
| "While I'm in here I'll optimize the other loops too" | Unmeasured changes add risk and no proven gain. One change, one measurement. |

## Red flags

- A performance PR with no before/after numbers
- Adding an index without reading the query plan before and after
- `useMemo`, caching or parallelism added by reflex
- The benchmark runs on a tiny or empty dataset
- The target metric improved, but nobody checked memory, write cost or correctness

## References

- [profiling.md](references/profiling.md): open at steps 2–3 for measurement and profiling commands per layer (backend, database, frontend, memory)
