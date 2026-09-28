# Risk catalog by system type

Use this list as prompts at step 2. Keep only the risks that apply to the change, and rank them.

| System | Defect classes worth a test | Usual cheapest level |
|---|---|---|
| HTTP / RPC API | validation gaps (accepts bad, rejects good); wrong status or error shape; missing authz check per role and tenant; pagination edges (empty, last page, cursor reuse); breaking a field consumers read | integration + contract |
| Auth and permissions | privilege escalation across roles; tenant isolation (user A reads B's data); expired or revoked token accepted; password reset and session fixation flows | integration, one E2E login journey |
| Payments and money | rounding and currency precision; double charge on retry; partial refund math; idempotency key reuse; webhook replay and ordering | unit (math) + integration (idempotency) |
| Data pipeline / batch | schema drift in input; duplicates and late data; timezone and DST boundaries; partial run then restart; empty and huge inputs | property + integration on fixtures |
| Async jobs / queues | at-least-once delivery → duplicate side effects; poison messages; retry storms; ordering assumptions; job timeout mid-write | integration with a real broker |
| Database changes | migration on production-shaped data; lock time; backfill resumability; rollback path; constraint violations in existing rows | migration rehearsal |
| UI | critical journey broken end to end; form validation and error messages; loading, empty and error states; keyboard and screen reader access | component tests + a few E2E |
| Integrations (third-party APIs) | timeouts, 429s and 5xx; changed response shapes; sandbox vs production differences | contract tests against recorded responses, plus one live smoke test |
| Caching | stale reads after writes; stampede on expiry; per-user data served to another user | integration |
| Concurrency | lost updates; double submits; race between check and act | integration with parallel calls |
| Performance-sensitive paths | N+1 queries; unbounded result sets; regressions against a latency budget | query-count assertions + load test pre-release |

## Oracles, strongest first

1. A durable state change: a DB row, a file, or an emitted event checked through the public interface.
2. The returned contract: status, body shape and values from an independent source of truth.
3. A user-visible rendering: text, role and state of an element.
4. An invariant that holds for all inputs (property test).
5. A log line or metric. Use this only when nothing else is observable.

Do not use an oracle that recomputes the expected value the same way the code does.
