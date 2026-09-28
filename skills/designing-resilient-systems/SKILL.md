---
name: designing-resilient-systems
description: Failure-mode design for distributed calls: timeouts, retries, idempotency, breakers, bulkheads, backpressure. Use when a path calls networks, queues or third parties, or after cascading failures, retry storms, duplicate processing or lost messages.
license: Apache-2.0
metadata:
  version: "0.1.0"
  category: "architect"
  sources: "wshobson/agents microservices-patterns, python-resilience (MIT); addyosmani/agent-skills api-and-interface-design (MIT); garrytan/gstack plan-eng-review (MIT)"
---

# Designing Resilient Systems

Every remote call will be slow, fail, or succeed twice. Design for each of those explicitly, so that one sick dependency degrades one feature instead of taking the whole system down.

## When to use

- Designing or reviewing any code path that calls a network service, database, queue or third-party API
- Payment, ordering, messaging or webhook flows, where duplicates or losses cost money
- After an incident involving cascading failure, a retry storm, thread-pool exhaustion, duplicate charges or lost messages
- Adding a queue, a background worker, or a new external dependency

**Not for:** a live outage happening now (use `responding-to-incidents`); making a path faster (use `optimizing-performance`); picking the overall topology (use `designing-system-architecture`); adding alerts and traces (use `instrumenting-observability`).

## The rule

```
EVERY REMOTE CALL HAS A TIMEOUT, A BOUNDED RETRY POLICY, AND A DEFINED FAILURE BEHAVIOR
```

Violating the letter of the rule is violating the spirit of the rule. A call with no timeout is a thread you have lent to a stranger indefinitely.

## Process

1. **Build a failure-mode table.** Draw one row per dependency on the path. The columns are: what happens when it is **slow**, **down**, returns **errors**, returns **wrong or stale data**, or **succeeds twice**. For each cell, write the user-visible effect and the intended behavior.
   Exit: no empty cells; "crash" and "hang" are not acceptable intended behaviors.

2. **Set timeouts from budgets.** Derive each timeout from the caller's latency budget (see `estimating-capacity`). Set connect and read timeouts separately. Propagate a deadline so downstream calls stop when the caller has already given up.
   Exit: every call has an explicit timeout smaller than its caller's.

3. **Retry only what is safe, with backoff, jitter and a budget.** Retry transient failures only: timeouts, connection resets, 429, 503. Never retry validation errors or 4xx logic errors. Use capped exponential backoff with full jitter. Limit total attempts, and cap retries as a fraction of traffic (a retry budget of about 10%) so that a retry storm cannot multiply load. Retry at one layer only: retries at several layers multiply each other.
   Exit: a retry policy per call, stating what is retried, max attempts, backoff, and which layer owns it.

4. **Make writes idempotent.** Assume at-least-once delivery everywhere; exactly-once delivery is not available over a network. Every retried or queued write carries an idempotency key. The receiver stores the key together with the result, atomically with the effect, and replays that result for duplicates. Consumers deduplicate by message ID or make the operation naturally idempotent (for example, set a status instead of incrementing a counter).
   Exit: each write path states its idempotency key and where duplicates are detected.

5. **Contain the blast radius.** Isolate resources per dependency with bulkheads: separate connection pools, thread pools or concurrency limits, so a slow dependency cannot drain capacity from the others. Add a circuit breaker around each dependency that can go dark. It opens on an error or latency threshold, fails fast while open, and probes for recovery in a half-open state.
   Exit: each dependency has its own resource limit and a breaker, or a stated reason why it needs neither.

6. **Apply backpressure and shed load.** Bound every queue and buffer. When the system is saturated, reject early with 429 or 503 and a `Retry-After` header rather than queuing forever. Prioritize: shed analytics before checkout. Size worker concurrency to what the downstream can absorb.
   Exit: no unbounded queue, and a defined overload response.

7. **Degrade gracefully.** For each non-critical dependency, choose a fallback: cached or stale data, a default, a hidden feature, or a queued write for later. Critical dependencies fail with a clear error, never a hang.
   Exit: the failure-mode table shows a fallback or a clear error in every "down" cell.

8. **Handle poison and lost messages.** Queues need a maximum receive count, a dead-letter queue with an owner and an alert, and a replay procedure. Use the outbox pattern for "write to the database and publish an event", so neither happens without the other.
   Exit: every queue has a DLQ, an owner, and a replay path.

9. **Prove it.** Write tests that inject each failure mode: a slow stub, an error stub, a duplicate delivery. Where a safe environment exists, run a fault-injection or game-day exercise.

## Output

```
Failure-mode table: dependency × {slow, down, errors, wrong/stale, duplicate} → effect → behavior
Timeouts: <call → connect/read, deadline propagation>
Retries: <call → retryable errors, attempts, backoff+jitter, owning layer, budget>
Idempotency: <write → key → dedupe store>
Isolation: <dependency → bulkhead limit, breaker thresholds>
Overload: <queues bounded, shed order, 429/503 behavior>
Fallbacks: <dependency → degraded behavior>
Queues: <queue → DLQ, owner, replay>
Tests: <failure injected → expected behavior>
```

## Rationalizations

| Excuse | Reality |
|---|---|
| "The provider is reliable" | Everything fails eventually. The SLA refunds your fees, not your users' trust. |
| "Just retry until it works" | Unbounded retries turn a blip into an outage by multiplying load on a struggling dependency. |
| "Our queue guarantees exactly-once" | Delivery might be deduplicated inside the broker; your side effects are not. Make the handler idempotent. |
| "Timeouts will cause false failures" | No timeout causes real failures: exhausted pools and a frozen service. Tune the value; don't remove it. |
| "We'll add resilience after launch" | The first incident will add it for you, at 3am, under pressure. |

## Red flags

- An HTTP client or DB driver used with its default (often infinite) timeout
- Retries on POST without an idempotency key
- Retries configured at the client, the service mesh and the job runner all at once
- One shared connection pool for every downstream dependency
- An unbounded in-memory queue, or `maxReceiveCount` unset
- A DLQ nobody watches
- "Write to the database, then publish to Kafka" as two separate steps with no outbox

## References

- [patterns.md](references/patterns.md): open when choosing breaker thresholds, backoff formulas, idempotency storage, or the outbox shape
