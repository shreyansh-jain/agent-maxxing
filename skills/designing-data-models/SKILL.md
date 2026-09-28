---
name: designing-data-models
description: Access-pattern-driven schema design covering keys, types, constraints, indexes, tenancy and store choice. Use when designing or reviewing tables or collections, choosing relational vs document vs key-value, or when integrity or tenancy keeps breaking.
license: Apache-2.0
metadata:
  version: "0.1.0"
  category: "architect"
  sources: "wshobson/agents postgresql-table-design (MIT); supabase/agent-skills supabase-postgres-best-practices (MIT); addyosmani/agent-skills api-and-interface-design (MIT)"
---

# Designing Data Models

Data outlives the code that writes it. Design the schema from the queries it must serve, and make the database itself refuse invalid data. Every later migration costs far more than getting the model right now.

## When to use

- New tables, collections or key layouts for a feature
- Reviewing a proposed schema or ORM model before its first migration
- Choosing between relational, document, key-value, wide-column or search stores
- Recurring problems: duplicate rows, orphaned records, slow queries, tenants seeing each other's data, broken time zones, rounding errors in money

**Not for:** changing a schema that already holds production data (use `migrating-databases-safely`); tuning a slow query on an existing schema (use `optimizing-performance`); defining business concepts and their rules (use `modeling-domains`); where each data store sits in the system (use `designing-system-architecture`).

## Process

1. **List the access patterns first.** For each read and write, record: the query in words, its filters and sort order, how often it runs, its latency target, and its result size. Include admin, reporting, export and delete-my-data paths. These are the ones people forget.
   Exit: an access-pattern table that each proposed table or index can be traced back to.

2. **Choose the store from the patterns.** Default to relational (Postgres or the team's existing database). Choose something else only when a pattern demands it:
   - document store: self-contained aggregates read whole, with a flexible shape;
   - key-value store: single-key lookups at very high throughput, or caching;
   - wide-column store: huge append-heavy data queried by partition key;
   - search engine: full-text search and relevance ranking.

   A second store is a second system to run and keep in sync.
   Exit: one primary store per entity, with the reason for each non-default choice.

3. **Normalize, then denormalize on evidence.** Start at third normal form: each fact is stored once. Denormalize (a duplicated column, a counter, a read model) only for a measured hot read, and name the mechanism that keeps the copy correct: a trigger, a same-transaction write, or an event.
   Exit: every duplicated fact names its source of truth and its sync mechanism.

4. **Pick keys deliberately.** Use a surrogate primary key: a sequential BIGINT identity, or UUIDv7 or a ULID when IDs must be generated outside the database or must not be guessable. Random UUIDv4 primary keys fragment B-tree indexes. Enforce natural keys (email per tenant, SKU) with UNIQUE constraints. Never expose sequential IDs where enumerating them is a risk.
   Exit: each table has a primary key strategy and its natural-key unique constraints.

5. **Make the database enforce the invariants.** Use NOT NULL wherever a value is required, foreign keys with a chosen `ON DELETE`, CHECK constraints for ranges and enums, and UNIQUE constraints (including partial ones) for business uniqueness. Application-only validation will be bypassed, eventually, by a script, a job or a race.
   Exit: every rule the business states is either a constraint or an explicit note on why it can't be.

6. **Use the right types.**
   - Money: an integer in minor units plus a currency column, or `NUMERIC`. Never floats.
   - Instants: `timestamptz`, stored in UTC.
   - Local times for scheduling: store the local time together with the IANA zone.
   - Strings: `text` with CHECK constraints for length.
   - JSON columns: only for data that is truly schemaless, and never for fields you filter on.
   Exit: no float money, no zone-less timestamps for instants.

7. **Derive indexes from the access patterns.** Build one composite index per hot query, with equality columns first, then range and sort columns. Index the foreign key columns that joins and deletes use. Add partial indexes for hot subsets. Every index slows writes and costs storage, so an index that serves no listed pattern is deleted.
   Exit: each index maps to a named access pattern.

8. **Decide the cross-cutting policies.**
   - **Tenancy:** a tenant ID on every tenant-owned row, included in unique constraints and leading its indexes, and enforced by row-level security or a mandatory query scope. Alternatively a schema or database per tenant, where isolation outweighs the operational cost.
   - **Deletion:** hard delete, soft delete (`deleted_at` plus partial unique indexes), or an archive table. Choose per entity, and include the legal erasure path (see `handling-personal-data`).
   - **Audit:** `created_at`/`updated_at` everywhere, plus an append-only history table where "who changed what" matters.
   - **Growth:** the partitioning or retention plan for any table expected to exceed about 100M rows.
   Exit: each policy decided per entity.

## Output

```
Access patterns: <table>
Store choice: <entity → store, reason if non-default>
Schema: <DDL or ORM model>
Constraints: <rule → constraint>
Indexes: <index → access pattern>
Policies: tenancy | deletion | audit | growth, per entity
Denormalisations: <copy → source of truth → sync mechanism>
```

## Red flags

- Tables designed before any query is written down
- `float` or `double` for money, and `timestamp without time zone` for events
- Uniqueness or foreign-key rules enforced only in application code
- A tenant-owned table with no tenant ID in its unique constraints
- EAV tables or one giant JSON column, used to avoid designing the schema
- An index for every column, or none beyond the primary key
- A second datastore added for one query that an index would serve

## References

- [store-selection.md](references/store-selection.md): open at step 2 when a pattern might justify a non-relational store
