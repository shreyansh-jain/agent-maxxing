---
name: estimating-capacity
description: Back-of-envelope estimation of traffic, storage, bandwidth, concurrency, latency and cost. Use when sizing a new system or feature, checking a design against peak or 10x load, setting latency budgets, or asking how many servers or how much storage.
license: Apache-2.0
metadata:
  version: "0.1.0"
  category: "architect"
  sources: "original; ideas: garrytan/gstack plan-eng-review (MIT), addyosmani/agent-skills performance-optimization (MIT)"
---

# Estimating Capacity

An estimate that is 2× off is useful; a design with no estimate is a guess. Derive every number from stated assumptions, show the arithmetic, and size for peak with headroom, not for the average.

## When to use

- Sizing a new system, feature or migration before choosing an architecture
- "Will this scale?", "how many instances or shards?", "how much storage per year?"
- Setting a latency budget across a request path
- Checking a proposed design against 10× growth, or estimating infrastructure cost

**Not for:** measuring and fixing an existing slow path (use `optimizing-performance`); choosing the architecture itself (use `designing-system-architecture`); reducing an actual cloud bill (use `controlling-cloud-costs`).

## Process

1. **List the assumptions.** Record each one with its source: user count (DAU/MAU), actions per user per day, payload sizes, read:write ratio, retention period, growth rate. Mark every guess as a guess. Ask the user for the two or three assumptions that dominate the result, and assume the rest.
   Exit: an assumptions table in which every row is sourced or labelled a guess.

2. **Traffic.** Average QPS = daily events ÷ 86,400. Peak QPS = average × a peak factor (2–3× for a consumer diurnal pattern, 5–10× for launches, flash sales or cron storms, or whatever the actual traffic graph shows). Do reads and writes separately. Multiply by fan-out: one user request that makes N backend or DB calls produces N× internal QPS.
   Exit: peak read QPS, peak write QPS, and internal QPS for each dependency.

3. **Storage.** Per-day growth = writes/day × bytes per record (including indexes, roughly 1.5–3× the raw row for an OLTP table). Multiply by retention and by the replication factor, then add the backup copies. Separate hot storage (DB/SSD) from cold storage (object store).
   Exit: storage at year 1 and year 3, hot vs cold.

4. **Bandwidth and concurrency.** Egress = peak read QPS × response size. Use Little's law for concurrency: in-flight requests = throughput × latency. That number sizes thread pools, connection pools and DB connections. Check it against the database's connection limit.
   Exit: peak egress, and peak concurrency per tier compared against its limits.

5. **Latency budget.** Start from the user-facing target (for example p99 300 ms) and allocate it hop by hop: client network, edge, service, each DB or downstream call. Sequential calls add up. Parallel fan-out is only as fast as its slowest branch, and with N branches the chance of hitting at least one slow branch is 1 − (1 − p)^N.
   Exit: a budget table whose total is within the target, or the hop that breaks it.

6. **Size with headroom.** Instances = peak load ÷ (per-instance capacity × target utilization). Target 50–70% at peak, and add N+1 (or one zone's worth) so that losing a node or zone does not overload the rest. Per-instance capacity comes from a benchmark or vendor numbers. Say which, and say it is an assumption until load-tested.
   Exit: an instance or shard count for each tier, and the first bottleneck at 10×.

7. **Cost it.** Multiply by current list prices (look them up; do not recall them) for compute, storage, egress and managed services. Do this at 1× and 10×.

8. **Sanity-check.** Compare with a known system, or with the orders of magnitude in the reference. If a number surprises you, re-derive it. The error is usually a units slip (bits vs bytes, per second vs per day).

## Worked example

A photo feature. Assumptions: 2M DAU (guess), 20 feed views and 2 uploads per user per day, 200 KB per photo, 1 KB of metadata, peak factor 3.

- **Reads.** 40M/day ÷ 86,400 ≈ 460 QPS average, so about 1,400 QPS at peak. Each feed view makes 1 metadata query plus 10 image fetches from the CDN.
- **Writes.** 4M/day ≈ 46 QPS average, so about 140 QPS at peak. A single primary database handles this comfortably.
- **Storage.** Images: 4M × 200 KB = 800 GB/day ≈ 290 TB/year, in object storage. Metadata: 4M × 1 KB × 2 (indexes) = 8 GB/day ≈ 3 TB/year hot. Plan partitioning or archival before year 2.
- **Egress.** 1,400 × 10 images × 200 KB ≈ 2.8 GB/s at peak. This is CDN territory, not something the origin should serve.
- **Concurrency.** 1,400 QPS × 0.15 s ≈ 210 in-flight feed requests. A pool of about 50 DB connections, at a few ms per query, is enough.
- **First bottleneck at 10×.** Metadata storage growth (about 30 TB/year hot), not QPS.

## Output

```
Assumptions: <table: value, source | guess>
Traffic: avg/peak read QPS, avg/peak write QPS, internal QPS per dependency
Storage: per day, year 1, year 3 (hot / cold, incl. indexes, replication)
Bandwidth: peak egress | Concurrency: in-flight per tier vs limit
Latency budget: <hop table> total vs target
Sizing: <tier → count at target utilisation, N+1>
Cost: 1× / 10× (prices looked up <date>)
First bottleneck at 10×: <component, why>
```

## Red flags

- Sizing from average QPS with no peak factor
- A per-instance capacity figure with no source
- Forgetting fan-out, indexes, replication or backups
- Mixing bits and bytes, or per-day and per-second, without labels
- Planning for 90%+ utilization at peak
- Remembered cloud prices presented as current

## References

- [numbers.md](references/numbers.md): open when you need latency, throughput or size orders of magnitude for a sanity check
