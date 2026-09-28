# Lock safety of common DDL

Last reviewed 2026-09-28 for PostgreSQL 12–17 and MySQL 8.0/8.4 (InnoDB). Lock behaviour changes between versions, so check each row against the manual for your exact version before relying on it:
- PostgreSQL: https://www.postgresql.org/docs/current/sql-altertable.html and https://www.postgresql.org/docs/current/explicit-locking.html
- MySQL: https://dev.mysql.com/doc/refman/8.4/en/innodb-online-ddl-operations.html

## Contents
- The lock queue trap
- PostgreSQL
- MySQL
- Session guards

## The lock queue trap

Both engines have this problem. An `ALTER` that is waiting for a lock also blocks every query that arrives after it, including plain reads. So one long-running transaction plus one waiting `ALTER` stops the table completely. Set a short lock timeout on every DDL statement and retry it, rather than letting it wait.

## PostgreSQL

| Change | Lock / cost | Safe technique |
|---|---|---|
| `ADD COLUMN` nullable, no default | ACCESS EXCLUSIVE, brief; metadata only | safe with `lock_timeout` |
| `ADD COLUMN ... DEFAULT <constant>` (incl. NOT NULL) | PG 11+: metadata only | safe with `lock_timeout`. A **volatile** default (`clock_timestamp()`, `gen_random_uuid()`) rewrites the table: add the column nullable, then backfill |
| `ALTER COLUMN ... SET NOT NULL` | ACCESS EXCLUSIVE + full scan | `ADD CONSTRAINT c CHECK (col IS NOT NULL) NOT VALID` → `VALIDATE CONSTRAINT c` → `SET NOT NULL` (PG 12+ skips the scan) → drop `c` |
| `ALTER COLUMN ... TYPE` | usually a full rewrite under ACCESS EXCLUSIVE | new column + dual-write + backfill + swap. Exceptions that are metadata only: `varchar(n)` → larger `n`, `varchar` → `text` |
| `RENAME COLUMN` / `RENAME TO` | brief, metadata only | the database is fine; running code is not. Use expand/contract, or a view shim |
| `DROP COLUMN` | brief, metadata only | only after no deployed code reads or writes it. ORMs that `SELECT *` into strict models count as readers |
| `CREATE INDEX` | SHARE: blocks writes for the whole build | `CREATE INDEX CONCURRENTLY`. It cannot run inside a transaction; if it fails it leaves an INVALID index, so `DROP INDEX CONCURRENTLY` and retry |
| `DROP INDEX` | ACCESS EXCLUSIVE | `DROP INDEX CONCURRENTLY` |
| `REINDEX` | blocks writes | `REINDEX ... CONCURRENTLY` (PG 12+) |
| `ADD FOREIGN KEY` | SHARE ROW EXCLUSIVE on both tables + validation scan | `ADD CONSTRAINT ... NOT VALID`, then `VALIDATE CONSTRAINT` (SHARE UPDATE EXCLUSIVE, which allows reads and writes) |
| `ADD CHECK` | ACCESS EXCLUSIVE + scan | `NOT VALID`, then `VALIDATE CONSTRAINT` |
| `ADD UNIQUE` / `PRIMARY KEY` | builds an index under a blocking lock | `CREATE UNIQUE INDEX CONCURRENTLY idx ...` → `ADD CONSTRAINT c UNIQUE USING INDEX idx` |
| `ALTER TYPE ... ADD VALUE` (enum) | brief | the new value can't be used in the same transaction; ship it before the code that uses it |
| `VACUUM FULL` / `CLUSTER` | ACCESS EXCLUSIVE + full rewrite | `pg_repack`, if it is available and approved |

Watch while running:
```sql
SELECT pid, wait_event_type, wait_event, state, now() - xact_start AS xact_age, left(query, 80)
FROM pg_stat_activity WHERE datname = current_database() ORDER BY xact_age DESC NULLS LAST;
SELECT client_addr, replay_lag FROM pg_stat_replication;
```

## MySQL (InnoDB)

Always state `ALGORITHM=` and `LOCK=` explicitly. MySQL then raises an error when it can't honour them, instead of quietly falling back to a blocking table copy.

| Change | Behaviour | Safe technique |
|---|---|---|
| `ADD COLUMN` | `ALGORITHM=INSTANT` in 8.0.12+ (last position); any position in 8.0.29+ | `ALGORITHM=INSTANT`; if it is refused, use gh-ost or pt-online-schema-change |
| `DROP COLUMN` | INSTANT in 8.0.29+; otherwise INPLACE with a table rebuild | INSTANT where supported, otherwise an online schema-change tool |
| `RENAME COLUMN` (same type) | metadata only | the database is fine, but running code breaks: expand/contract |
| change a column's data type | `ALGORITHM=COPY`, blocks writes | gh-ost or pt-online-schema-change |
| grow a `VARCHAR` | INPLACE only if the length prefix stays 1 byte (≤255 bytes) or stays 2 bytes | check the byte width; otherwise use an online tool |
| `ADD INDEX` | `ALGORITHM=INPLACE, LOCK=NONE`; concurrent DML allowed | safe; still watch replication lag, because replicas apply the DDL single-threaded |
| `ADD FOREIGN KEY` | INPLACE only with `foreign_key_checks=0`, otherwise COPY | validate orphans first, and decide with the user |
| `NULL` → `NOT NULL` | table rebuild | online tool; backfill first |

Watch while running: `SHOW PROCESSLIST`, `performance_schema.metadata_locks`, and `SHOW REPLICA STATUS` (`Seconds_Behind_Source`).

## Session guards

```sql
-- PostgreSQL, per migration session
SET lock_timeout = '3s';
SET statement_timeout = '15min';   -- long enough for CONCURRENTLY builds, short enough to stop runaways

-- MySQL
SET SESSION lock_wait_timeout = 5;  -- metadata-lock wait, in seconds
```

If a guarded statement times out, it failed safely. Retry it with backoff, or find and deal with the long transaction that blocked it, with the user's approval before killing any session.
