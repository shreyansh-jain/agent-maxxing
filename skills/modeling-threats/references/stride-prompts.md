# STRIDE prompts per trust boundary

Ask all six questions at each boundary. Keep a threat only if it can be written as a complete abuse path: attacker → entry point → weakness → asset → impact.

| Letter | Question to ask at the boundary | Typical control |
|---|---|---|
| **S**poofing | Can the caller claim to be someone else, such as another user, tenant, service or webhook sender? | Strong authentication, signed requests (HMAC with timestamp), mTLS, verifying the audience and issuer of tokens |
| **T**ampering | Can data be modified in transit, at rest, or by a party who shouldn't write it, including via mass-assignment or client-controlled IDs and prices? | Server-side authority for prices and roles, field allowlists, integrity checks, TLS, write-scoped credentials |
| **R**epudiation | Could someone deny doing a sensitive action, and would you be able to prove it? | Append-only audit log with actor, action, target and timestamp, stored outside the actor's control |
| **I**nformation disclosure | Can data leak across tenants or users, or through errors, logs, caches, URLs, timing or search indexes? | Per-object authorization, tenant scoping at the query layer, error redaction, not putting secrets in URLs or logs |
| **D**enial of service | Can one caller exhaust CPU, memory, connections, queue depth, a paid API quota, or storage? | Rate limits and quotas per principal, size limits, timeouts, bounded queues, cost caps |
| **E**levation of privilege | Can a lower-privileged caller reach a higher-privileged action, through IDOR, a missing check on a secondary route, role confusion, deserialization, SSRF into internal services, or path traversal? | Deny by default, checks on every route (not just the UI), SSRF allowlists, sandboxing |

## Boundaries people forget

- Background jobs and queues. Messages are often trusted as if they had passed the API's checks, but they didn't.
- Admin tooling and internal dashboards.
- Webhooks you receive (spoofing, replay) and webhooks you send (SSRF through user-supplied URLs).
- CI/CD. PRs from forks, secrets exposed to workflows, and dependency install scripts.
- Exports, reports and search indexes, which copy data outside its original access controls.
- Caches keyed without the tenant or user.

## LLM and agent features

Treat everything the model reads as attacker-controlled: user input, retrieved documents, web pages, tool output, file contents and email.

| Threat | Question | Control |
|---|---|---|
| Prompt injection (direct or indirect) | Can content the model reads change what it does? | Separate instructions from data; never let retrieved content grant permissions; confirm high-impact actions with a human |
| Tool abuse | What is the worst thing each tool can do if the model is fully steered? | Least-privilege tools, scoped credentials per user, allowlisted arguments, dry-run modes |
| Exfiltration | Can the model send data out through a tool call, a URL it renders, an image link or an email? | Egress allowlists, no auto-fetching of model-generated URLs, output filtering for secrets |
| Excessive autonomy | Can a loop of actions run without a checkpoint? | Step and cost budgets, human approval for irreversible steps |
| Cross-user leakage | Can one user's data enter another user's context through memory, a cache or a shared vector index? | Per-tenant indexes or filters enforced outside the model |
| Output trust | Is model output inserted into SQL, shell commands, HTML or code without validation? | Treat it as untrusted input: parameterize, escape, sandbox |

## Likelihood and impact scale

| Score | Likelihood | Impact |
|---|---|---|
| 3 | Reachable by an anonymous or any authenticated user, with a known technique | Cross-tenant data exposure, account takeover, money movement, code execution, or loss of integrity-critical data |
| 2 | Needs a valid account plus a specific precondition, or an insider | Exposure of one user's data, a partial outage, an abuse cost that needs a human to clean up |
| 1 | Needs an unlikely chain, physical access, or an already-compromised dependency | Minor information leak, or noisy denial of service with an easy mitigation |
