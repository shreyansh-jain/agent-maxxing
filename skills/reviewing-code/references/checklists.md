# Review checklists

## Contents
- Picking specialists
- Correctness baseline (always)
- Security
- Data and migrations
- API and contracts
- Concurrency
- Error handling and silent failures
- Performance
- Tests
- Standards smell baseline

Checklists are prompts for where to look. They are not findings. Every item you flag still has to pass verification (SKILL.md step 6).

## Picking specialists

| The diff touches | Add |
|---|---|
| request handlers, auth, sessions, uploads, webhooks, templates, shell or SQL construction | Security |
| migrations, schema, ORM models, backfills | Data and migrations |
| public endpoints, SDKs, events, webhooks, serialized types | API and contracts |
| jobs, queues, caches, locks, shared mutable state, `async` code | Concurrency |
| `try`/`catch`, fallbacks, retries, optional chaining over I/O | Error handling |
| loops over data, queries, hot paths, bundles, list endpoints | Performance |
| any behavior change | Tests (always) |

Once the diff is over about 200 lines, or any specialist has returned a Blocker, run one final **adversarial pass**. Assume the other passes missed something. Try double submission, a partial failure halfway through a loop, the first run with empty data, maximum-size input, a slow dependency, and a garbage response from an external service.

## Correctness baseline (always)

- Off-by-one errors, inverted conditions, wrong operator precedence, `=` vs `==`
- Null, empty, zero, negative and very large values at every new branch
- The new code path is actually reached (wired into routing, registered, exported)
- A new enum, status or type value is handled by **every** consumer. Grep the sibling values and read each switch, allowlist, filter, serializer and UI mapping
- Changed function behavior: every caller still gets what it expects
- Time: timezones, "today" computed twice, DST, inclusive vs exclusive ranges
- Type coercion at boundaries (JSON number vs string, float money, integer overflow)
- Partial completion: what state is left behind if step 3 of 5 throws

## Security

- Untrusted input reaching SQL, a shell, templates, file paths, URLs (SSRF), headers, redirects, or deserializers
- Authorization, not just authentication: can user A act on user B's object by changing an id?
- Checks that default to allow; new routes missing the auth middleware used by their siblings
- Escape hatches: `dangerouslySetInnerHTML`, `v-html`, `|safe`, `mark_safe`, `.html_safe`, raw SQL APIs
- Secrets in code, logs, error responses or URLs; tokens compared with `==` instead of in constant time
- Predictable randomness for tokens; weak hashes for passwords
- Model or LLM output written to storage, executed, or fetched as a URL without validation
- For anything deeper, hand off to the `auditing-security` skill

## Data and migrations

- Rollback path exists and actually reverses the change
- `NOT NULL` added to a column that has nulls; a type narrowing that truncates data
- Column or table dropped or renamed while running code still reads it (needs expand then contract)
- Index creation or `ALTER` that locks a large table (Postgres: `CONCURRENTLY`)
- Backfill runs in one statement instead of in batches
- Deploy order: does old code with the new schema, or new code with the old schema, crash?
- For the full procedure, hand off to the `migrating-databases-safely` skill

## API and contracts

- A field is removed, renamed or retyped; a new required parameter; a changed status code or error shape
- Old clients (mobile apps, SDKs, webhook subscribers) that cannot upgrade in lockstep
- New endpoints are inconsistent with existing error format, pagination, or rate limits
- Docs, OpenAPI or examples not updated

## Concurrency

- Check-then-act without a unique constraint or atomic update (`find_or_create`, "if not exists then insert")
- Status transitions not guarded with `WHERE status = old`
- Shared mutable state across requests, threads or tests
- Missing `await`; fire-and-forget promises whose errors vanish
- Blocking I/O or `sleep` inside an async handler
- Cache invalidation racing the write it protects

## Error handling and silent failures

- Empty `catch`, or catch-log-continue where the caller needed to know about the error
- Broad catches that also swallow unrelated errors
- Fallback to a default, mock or stale value that hides an outage from the user and from monitoring
- Retries that exhaust without surfacing an error; errors with no context (which operation, which id)
- Optional chaining that silently skips a required side effect

## Performance

- A query or network call inside a loop (N+1); a missing eager load or batch
- A new `WHERE` or `ORDER BY` on an unindexed column of a large table
- Unbounded result sets: no `LIMIT`, no pagination, `list()` over a whole table
- O(n²) scans (`find` inside `map`) on collections that grow with data
- Sequential awaits that could run in parallel
- Heavy new frontend dependencies or barrel imports
- Flag only what the data volume makes real. Tuning belongs to the `optimizing-performance` skill

## Tests

- Each new branch and error path has a test; so does the "denied" case of each permission check
- The tests assert behavior through the public interface, not implementation details or mocks of internals
- Expected values come from an independent source, not recomputed the way the code computes them
- The tests would fail if the change were reverted
- No new sleeps, real network calls, wall-clock reads, or order dependence

## Standards smell baseline

These apply only where the repo's documented standards are silent. A documented rule always wins. Each smell is a judgment call ("possible Feature Envy"), never a hard violation.

| Smell | Looks like | Suggested move |
|---|---|---|
| Mysterious name | a name that does not say what it holds or does | rename it; if no honest name exists, the design is unclear |
| Duplicated logic | the same shape in two hunks | extract it once and call it from both places |
| Feature envy | a function mostly reads another object's data | move it next to that data |
| Data clump | the same 3+ parameters always travel together | introduce a type |
| Primitive obsession | a string or number standing in for a domain concept | give the concept a small type |
| Repeated switch | the same `switch` on the same type in several places | use one map or polymorphism |
| Shotgun surgery | one logical change needs edits in many files | gather what changes together |
| Speculative generality | parameters, hooks or layers with no current caller | delete them until they are needed |
| Middle man | a wrapper that only forwards calls | call the target directly |
| Bolted-on conditional | a special case wedged into an unrelated flow | give it its own function or policy |
