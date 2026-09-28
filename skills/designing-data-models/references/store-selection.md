# Choosing a store

Start with relational. Switch only when an access pattern needs something relational cannot do well, and budget for the cost of running a second system.

| Store type | Strong at | Weak at | Pick it when |
|---|---|---|---|
| Relational (Postgres, MySQL) | joins, transactions, constraints, ad-hoc queries, mature tooling | horizontal write scaling past one primary; very wide sparse data | the default for business data |
| Document (MongoDB, Firestore, DynamoDB used as documents) | reading and writing a whole aggregate in one call; flexible fields | cross-document integrity; joins; ad-hoc analytics | aggregates are self-contained and read whole, and their shape varies |
| Key-value (Redis, DynamoDB used for single keys) | sub-millisecond lookups by key; counters; caches; locks | any query not keyed on the primary key; durability, depending on configuration | lookups are always by one known key, or the data is a derivable cache |
| Wide-column (Cassandra, Bigtable, ScyllaDB) | huge append-heavy writes; time-ordered reads within a partition | ad-hoc queries; transactions across partitions | known partition-key queries at very high write volume (events, telemetry) |
| Search (OpenSearch, Elasticsearch, Typesense) | full-text search, relevance ranking, faceting | being a source of truth; transactional updates | users search text; always feed it from the primary store |
| Time-series (TimescaleDB, InfluxDB, Prometheus) | range scans over time; downsampling; retention | relational business data | metrics or sensor data queried by time window |
| Analytical / columnar (ClickHouse, BigQuery, Snowflake) | aggregations over billions of rows | high-rate single-row updates; low-latency OLTP | reporting and analytics, fed from the primary store |

## Single-table design (DynamoDB-style) checklist

- Every access pattern is written down before any key is chosen.
- The partition key spreads load evenly, with no hot tenant or hot date.
- The sort key supports the range queries each pattern needs.
- Each secondary index is justified by a named pattern.
- Someone has written down what happens when a new, unforeseen query arrives, because the answer is often "add an index or copy the data".

## Keeping two stores in sync

- Prefer the outbox pattern. Write the change and an outbox row in the same transaction; a relay publishes the outbox row afterwards.
- Change data capture (CDC) from the primary database's log is the alternative.
- Never write to two stores from application code and hope both succeed.
- Assume the secondary store is stale, and design the UI and APIs for that.
