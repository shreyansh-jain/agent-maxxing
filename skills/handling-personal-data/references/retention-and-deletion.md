# Retention and deletion patterns

Deleting personal data means removing it from every copy. For each storage location in the inventory, pick one of these patterns and write down who runs it and how completion is recorded.

| Location | Pattern | Notes |
|---|---|---|
| Primary database | Tombstone the user (`deleted_at`, identifiers nulled), then a purge job hard-deletes or anonymizes the dependent rows | Keep a minimal record that the deletion happened (user id, timestamp, request id), with no personal data in it |
| Read replicas, caches | These follow the primary, but check the cache TTLs and any caches that never expire | Explicitly evict cache keys that contain user data |
| Search indexes | Delete the document by id when the record is purged | Indexes are often rebuilt from snapshots. Make sure the snapshot source is already purged |
| Object storage (uploads, exports) | Store files under per-user key prefixes so they can be deleted by prefix; set lifecycle rules for generated exports | Delete versioned buckets version by version, including delete markers |
| Backups | Don't edit backups. Document the expiry window (e.g. 35 days). On restore, replay the deletion log before bringing the data online | The deletion log itself must not contain personal data beyond the user id |
| Data warehouse / lake | Key on pseudonymous ids. Keep the id → identity map in the primary store, so deleting the map entry anonymizes the history | Partition by date and drop old partitions to enforce retention |
| Event streams (Kafka, etc.) | Set topic retention to at most the allowed period. Use compaction with tombstones for keyed topics | Consumers that materialize data inherit the same obligation |
| Logs and traces | Don't log raw personal data (scrub at emission). Set index retention (e.g. 14–30 days). Hash identifiers where correlation is needed | Error trackers and APM tools hold copies too, so set their retention |
| Analytics / product tools | Send pseudonymous ids. Use the vendor's user-deletion API, and call it from your deletion job | Session replay: mask inputs by default |
| Third-party processors (email, payments, CRM, LLM APIs) | Call each vendor's deletion API from the job, or record the contractual retention | Record each processor in the inventory. Check whether the LLM provider retains prompts or trains on them |
| Local devices / mobile | Clear on logout and account deletion. Avoid storing personal data unencrypted on the device | |

## Enforcing retention

- Make retention executable: a TTL column plus a scheduled job, database-native TTLs, or partition drops. A retention policy that exists only in a document isn't enforced.
- Monitor the purge jobs. A purge job that fails silently means the policy isn't being applied.
- Test deletion end to end with a synthetic user: create them, touch every feature, delete them, then query every location.
