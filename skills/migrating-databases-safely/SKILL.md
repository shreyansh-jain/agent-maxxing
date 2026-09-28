---
name: migrating-databases-safely
description: Zero-downtime schema and data migration discipline for production databases. Use when adding, renaming, dropping or retyping a column or table, adding an index or constraint, backfilling rows, or writing any migration that will run against a live database with traffic.
license: Apache-2.0
metadata:
  version: "0.1.0"
  category: "operate"
  sources: "addyosmani/agent-skills deprecation-and-migration (MIT); wshobson/agents database-migration (MIT); supabase/agent-skills supabase-postgres-best-practices (MIT)"
---

# Migrating Databases Safely

Old code and new code share the database during every rollout, so every step must be valid for both. A migration that assumes a single cutover is an outage waiting for a slow deploy.

## When to use

- Writing or reviewing a migration file (`migrations/`, Prisma, Alembic, Rails, Flyway, Liquibase, Django, Ecto)
- Renaming, dropping, retyping or making a column NOT NULL
- Adding an index, foreign key, unique or check constraint to a table that already has rows
- Backfilling or transforming existing data
- Splitting or merging tables, or moving data between stores

**Not for:** slow queries with no schema change (use `optimizing-performance`); removing a public API or feature (use `designing-interfaces`); an ORM or database *version* bump (use `upgrading-dependencies`); a migration that is already breaking production (use `responding-to-incidents` first).

## The rule

```
NO DESTRUCTIVE OR LOCKING CHANGE IN THE SAME DEPLOY AS THE CODE THAT NEEDS IT
```

Violating the letter of the rule is violating the spirit of the rule. Additive changes ship first; destructive changes ship last, alone, after nothing reads the old shape.

## Process

1. **Classify each statement.** For every statement, record which lock it takes, how long it holds that lock, and whether it rewrites the table. Look it up in [lock-safety.md](references/lock-safety.md) for your engine and version. Don't rely on memory, because behaviour changes between versions. Then check the table size (`SELECT pg_total_relation_size('t')`, or `information_schema.TABLES` on MySQL) and the write rate.
   Exit: every statement is labelled *safe*, *safe with technique*, or *unsafe*.

2. **Split into expand → migrate → contract.** No step may break the code running before it or after it.
   - **Expand**: add new nullable columns or tables, and build indexes concurrently or online. Deploy on its own.
   - **Dual-write**: the app writes both the old and new shapes. Deploy.
   - **Backfill**: copy existing rows, in batches (step 3).
   - **Switch reads**: the app reads the new shape and still writes both. Deploy, then let it run long enough to trust it.
   - **Contract**: stop writing the old shape. Then drop it in a *separate, later* deploy.
   Exit: a numbered list of deploys, each marked with the rollback that keeps it safe.

3. **Make backfills boring.** Batch by primary-key range, 1k–10k rows per batch, and commit each batch. Throttle between batches, and watch replication lag and lock waits while it runs. Make it idempotent (`WHERE new_col IS NULL`) and resumable from the last key. Run it as a job or script, never inside the schema migration transaction.
   Exit: the script can be killed and restarted without losing work or duplicating it.

4. **Guard every DDL statement.** Set a short `lock_timeout` (e.g. `SET lock_timeout = '3s'`) and a `statement_timeout`, so a blocked `ALTER` fails fast instead of queueing every query behind it. Retry with backoff. Add constraints as `NOT VALID` and then `VALIDATE` them. Build indexes `CONCURRENTLY` (Postgres) or with `ALGORITHM=INPLACE, LOCK=NONE`, or use gh-ost or pt-online-schema-change (MySQL).
   Exit: no statement can hold an exclusive lock on a hot table for more than a few seconds.

5. **Prove the down path.** Write the rollback for each step and run up → down → up against a copy of production-shaped data, such as a branch database, a restored snapshot, or a staging database with realistic row counts. If a step can't be reversed (a dropped column, a lossy retype), say so and require a backup or snapshot first.
   Exit: rollback has been exercised, or the irreversibility is written down and accepted.

6. **Get confirmation before touching production.** Show the user the exact statements, the target database, the expected lock, the expected duration, and the rollback. Then wait for an explicit yes. Never run a migration, backfill, `DROP`, `TRUNCATE` or `DELETE` against a shared or production database on your own initiative.
   Exit: the user has approved this specific command against this specific target.

7. **Watch while it runs.** Track lock waits (`pg_locks`, `pg_stat_activity`), replication lag, error rate, and p99 latency. Stop the run if lag or latency crosses the threshold you agreed beforehand.

## Output

```
Migration plan: <change>
Engine/version: <e.g. Postgres 16>   Table size: <rows / GB>   Write rate: <per s>
Deploy 1 (expand):  <statements>   lock: <type, duration>   rollback: <how>
Deploy 2 (dual-write + backfill): <code change; backfill job, batch size, throttle>
Deploy 3 (switch reads): <code change>   bake: <duration / signal>
Deploy 4 (contract): <statements>   irreversible: <yes/no, backup taken>
Monitoring: <lag / lock / latency thresholds and abort action>
```

## Rationalizations

| Excuse | Reality |
|---|---|
| "The table is small" | Measure it. Tables grow, and even a small hot table queues all traffic behind one exclusive lock. |
| "It's just a rename" | During the rollout, old code queries the old name. Expand/contract it. |
| "We have a maintenance window" | Then write down the window and the lock duration. A migration that overruns is still an outage. |
| "The ORM generated it, so it's fine" | ORMs emit whatever is easiest. Read the SQL (`prisma migrate diff`, `alembic upgrade --sql`, `rails db:migrate:status`). |
| "We'll write the rollback if we need it" | You will need it at the worst moment. Exercise it now. |
| "Backfill in the migration is simpler" | One huge transaction holds locks, bloats the WAL or binlog, lags replicas, and can't be resumed. |

## Red flags

- `ALTER TABLE ... ADD COLUMN ... NOT NULL` without a default, on an existing table
- `CREATE INDEX` without `CONCURRENTLY` or an online algorithm on a table with traffic
- A column rename or drop in the same PR as the code that stops using it
- `UPDATE big_table SET ...` with no `WHERE` batching
- No `lock_timeout` on DDL against a hot table
- A migration file you have not read as raw SQL
- About to run anything against a database URL you didn't create yourself

## References

- [lock-safety.md](references/lock-safety.md): open when classifying any DDL statement for Postgres or MySQL
