# Numbers for sanity checks

**These are orders of magnitude, so check them against your hardware.** They are rough 2020s-era figures for commodity cloud hardware. Before sizing anything real, replace them with your own benchmark or the vendor's current documentation. Last reviewed: 2026-09.

## Latency

| Operation | Order of magnitude |
|---|---|
| L1 cache / main memory reference | ~1 ns / ~100 ns |
| Read 1 MB sequentially from memory | ~10–50 µs |
| Random read from NVMe SSD | ~10–100 µs |
| Read 1 MB sequentially from SSD | ~0.1–1 ms |
| Round trip within one datacenter or AZ | ~0.1–0.5 ms |
| Round trip between AZs in a region | ~0.5–2 ms |
| Round trip across a continent | ~30–80 ms |
| Round trip transatlantic / transpacific | ~70–150 ms |
| Simple indexed OLTP query (warm cache) | ~0.5–5 ms |
| TLS handshake on a new connection | 1–2 extra round trips |

## Throughput (per instance, highly workload-dependent)

| Component | Order of magnitude |
|---|---|
| Stateless HTTP service, simple handler | 1k–10k req/s per core-heavy instance |
| Relational DB primary, simple indexed writes | 1k–10k writes/s |
| Relational DB, simple indexed reads (with replicas and cache) | 10k–100k reads/s |
| In-memory KV store (single node) | 100k+ ops/s |
| Log/queue broker partition | 10–100 MB/s |
| 1 Gbps network link | ~125 MB/s |

## Sizes

| Thing | Order of magnitude |
|---|---|
| UUID / BIGINT | 16 B / 8 B |
| A typical JSON API response | 1–50 KB |
| A compressed phone photo | 100 KB – 3 MB |
| One minute of 1080p video | ~50–150 MB |
| Index overhead on an OLTP table | 0.5–2× the raw data |

## Time conversions

- 1 day ≈ 86,400 s ≈ 10^5 s
- 1 month ≈ 2.6M s
- 1 year ≈ 31.5M s ≈ 3 × 10^7 s
- 1M requests/day ≈ 12 req/s average

## Availability budgets

| Target | Downtime per 30 days |
|---|---|
| 99% | ~7.2 h |
| 99.9% | ~43 min |
| 99.95% | ~22 min |
| 99.99% | ~4.3 min |

If the system has serial dependencies, their availabilities multiply. For example, three dependencies at 99.9% each give at most ~99.7%.
