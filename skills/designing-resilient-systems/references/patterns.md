# Resilience patterns reference

## Backoff with full jitter

```
sleep = random(0, min(cap, base * 2 ** attempt))
```

Typical starting values are base 100 ms, cap 10–20 s, and 3–5 attempts for user-facing calls. Background jobs can use more attempts over a longer window. If the server sends `Retry-After`, honor it. Full jitter prevents synchronized retry waves when many clients fail at the same moment.

## Retry budget

Allow retries only while `retries / requests` stays under about 10% over a sliding window. Past that point the dependency is struggling, and retrying adds load without adding successes.

## Idempotency keys

1. The client generates a unique key per logical operation, such as a UUID, and sends it with every attempt of that operation.
2. The server does the following in one transaction: insert `(key, request_hash, status='in_progress')` and fail on conflict; perform the effect; store the response.
3. When a duplicate key arrives with the same request hash, return the stored response. If the request hash differs, return 422, because the key was reused for a different request.
4. Expire keys after the longest plausible retry window, typically 24 h to 7 d.

## Circuit breaker states

| State | Behavior | Transition |
|---|---|---|
| Closed | calls pass through; failures are counted | opens when the error rate or the slow-call rate exceeds a threshold (e.g. 50% over a minimum of 20 calls in 10 s) |
| Open | fails fast with no call made, and uses the fallback | moves to half-open after a cool-down (e.g. 30 s) |
| Half-open | lets a few probe calls through | closes if the probes succeed; reopens if they fail |

## Bulkheads

- Give each dependency its own connection pool or semaphore, sized using Little's law: its QPS × p99 latency, plus headroom.
- Separate pools for user-facing work and batch work.
- Keep per-tenant concurrency limits in multi-tenant systems, so one noisy tenant cannot starve the others.

## Transactional outbox

```
BEGIN;
  UPDATE orders SET status = 'paid' WHERE id = $1;
  INSERT INTO outbox (id, topic, payload) VALUES (gen_random_uuid(), 'order.paid', $2);
COMMIT;
-- relay: poll or tail outbox → publish → mark sent (at-least-once; consumers dedupe by outbox id)
```

## Consumer checklist

- Process each message idempotently, deduplicating by message ID or through a natural key.
- Acknowledge only after the effect is durable.
- Set a maximum receive count, then route to a DLQ with an alert.
- Replay from the DLQ only after fixing the cause, and replay idempotently.
- Handle out-of-order delivery with version or sequence checks where ordering matters.

## Timeouts cheat sheet

| Layer | Rule of thumb |
|---|---|
| User-facing request | the overall deadline equals the product's latency target |
| Each downstream call | less than the remaining deadline, minus a margin for local work |
| Connect timeout | short (100 ms – 1 s); connecting should be fast |
| Database statement | set `statement_timeout` or the equivalent, per role or per query |
| Background job | a maximum runtime, with a heartbeat so stuck jobs are detected |
