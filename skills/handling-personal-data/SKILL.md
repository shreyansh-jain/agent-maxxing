---
name: handling-personal-data
description: Engineering practice for collecting, storing, using and deleting personal data. Use when a feature touches PII, health, payment or location data, analytics or tracking, identifiers in logs, retention, deletion or export requests, or GDPR, CCPA or HIPAA concerns.
license: Apache-2.0
metadata:
  version: "0.1.0"
  category: "architect"
  sources: "wshobson/agents gdpr-data-handling (MIT); addyosmani/agent-skills security-and-hardening, observability-and-instrumentation (MIT); openai/skills security-threat-model (Apache-2.0)"
---

# Handling Personal Data

Every field of personal data needs a purpose, an owner, a retention period and a deletion path. Data you never collect cannot leak. Data you cannot find cannot be deleted.

This is engineering guidance, not legal advice. Legal basis, consent wording, cross-border transfer mechanisms and breach-notification duties under GDPR, CCPA/CPRA, HIPAA, PCI DSS and similar regimes depend on your jurisdiction and contracts. Flag them for the user's legal or privacy counsel rather than deciding them.

## When to use

- A new feature collects, stores, shares or derives data about a person: name, email, phone, IP address, device ID, location, payment, health, biometrics, behavioral events
- Adding analytics, tracking, session replay, error tracking or LLM features that see user content
- Designing retention, account deletion, data export or a data-subject request flow
- Logs, traces or analytics that may contain identifiers
- Sending personal data to a third party or another region

**Not for:** modeling attackers against the system as a whole (use `modeling-threats`); auditing code for vulnerabilities (use `auditing-security`); schema design without a privacy question (use `designing-data-models`).

## Process

1. **Inventory the data.** For the feature, list every personal-data field: where it enters, where it is stored (primary database, replicas, caches, search index, object storage, backups, data warehouse, logs, traces, analytics, third-party processors, LLM providers), who can read it, and where it flows. Grep for the field names across the codebase and configs, because copies hide in exports and event payloads.
   Exit: a table with one row per field, covering every storage location, including logs and third parties.

2. **Classify each field.** Use four levels:
   - **public**;
   - **internal**: pseudonymous IDs;
   - **personal**: name, email, IP, device ID, precise location;
   - **sensitive**: health, biometrics, government ID, financial account, children's data, sexual orientation, religion, political views, exact geolocation history, credentials.
   Sensitive fields need the strongest controls and usually a legal review.
   Exit: every field has a class.

3. **Minimize.** For each field, ask: what breaks if we don't collect it? What breaks if we store a coarser version, such as year of birth instead of a birthdate, city instead of GPS, or a hash instead of the raw value? What breaks if we keep it for less time? Remove fields with no answer. Record the purpose of each remaining field in one line; don't reuse data for a new purpose without checking.
   Exit: each remaining field has a stated purpose, and at least the fields without one are gone.

4. **Set retention and a deletion path.** Give each field a retention period and the mechanism that enforces it: a TTL, a scheduled purge job, or partitions that age out. Design account deletion to reach every location from step 1. Backups need a documented expiry window. Analytics and logs need identifier removal or aggregation. Third parties need a deletion API call or a contract term. Prefer tombstoning plus asynchronous purging, with a completion record.
   Exit: for every storage location, you can say how a specific user's data leaves it, and by when.

5. **Protect it in place.**
   - TLS in transit everywhere, including internal hops.
   - Encryption at rest. Use field-level or envelope encryption for sensitive fields, with keys in a KMS and not in the codebase.
   - Least-privilege access by role, with just-in-time elevation for production data.
   - An append-only audit log of who read or changed sensitive records.
   - Development and staging use synthetic or masked data, never production copies.
   Exit: each sensitive field has its encryption, access roles and audit coverage named.

6. **Keep it out of telemetry.** Scrub or hash identifiers in logs, traces, metrics labels, error reports and analytics events at the point of emission. An allowlist of loggable fields is safer than a denylist. Check that request bodies, headers (`Authorization`, cookies) and LLM prompts are not logged verbatim. Verify it by searching real emitted output, not by reading config alone.
   Exit: a sample of real logs and traces for the feature contains no raw personal data.

7. **Support data-subject requests.** Build the ability to *find* all data for a user ID (access and export in a machine-readable format), *correct* it, *delete* it (per step 4), and record consent or opt-out state where the processing depends on it. Authenticate every request before acting on it: a deletion or export request is itself an attack surface.
   Exit: export and delete can be run for one test user, and together they cover every location in the inventory.

8. **Flag the legal questions.** List for counsel: the legal basis per purpose, consent requirements, cross-border transfers (which regions, which processors), whether a DPIA or other assessment is needed, processor agreements, breach-notification duties, and any sector rules (HIPAA, PCI, COPPA). Do not answer them yourself.

## Output

```
| Field | Class | Purpose | Stored in | Retention | Deletion path | Protection |
|---|---|---|---|---|---|---|

Removed or coarsened: <field>: <why not needed>
Telemetry check: <what was searched, result>
DSR support: export <yes/how> · delete <yes/how> · correct <yes/how>
For counsel: <open legal questions>
```

## Red flags

- "We might need it later" as the purpose for a field
- Account deletion that only removes the `users` row
- Production database dumps in staging or on laptops
- Logging whole request or response bodies, or LLM prompts, in a service that handles user content
- Personal data used as metric labels or in URLs
- New third-party SDKs or LLM providers receiving user data without an entry in the inventory
- Deciding consent or legal-basis questions in code comments instead of flagging them

## References

- [retention-and-deletion.md](references/retention-and-deletion.md): open at step 4 for deletion patterns across databases, backups, warehouses, logs and processors
