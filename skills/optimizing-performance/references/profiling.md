# Measuring and profiling by layer

## Contents
- Benchmark hygiene
- Backend CPU and latency
- Database
- Memory
- Frontend
- Load testing

Tool flags change between versions. Check `--help` or the official docs for the installed version rather than trusting the examples below verbatim.

## Benchmark hygiene

- Warm up first (JIT compilation, caches, connection pools), then take at least 10 samples. Report median and p95.
- Fix the inputs: the same dataset, the same seed, and the same concurrency every run.
- Change one variable per comparison. Alternate A and B runs to cancel out drift (thermal throttling, noisy neighbors).
- A difference smaller than the run-to-run spread is not a result.
- HTTP: `hyperfine 'curl -s localhost:3000/orders > /dev/null'`, or a load tool at a fixed rate (below). Functions: the language's benchmark harness (`pytest-benchmark`, `go test -bench`, `cargo bench`, `tinybench`/`vitest bench`, JMH).

## Backend CPU and latency

| Stack | Profile with |
|---|---|
| Node | `node --cpu-prof app.js` (open the `.cpuprofile` in Chrome DevTools), `0x`, `clinic flame` |
| Python | `py-spy record -o out.svg --pid <pid>` or `py-spy top`; `cProfile` + `snakeviz` for scripts |
| Go | `net/http/pprof`, then `go tool pprof -http=: http://host/debug/pprof/profile?seconds=30` |
| JVM | async-profiler, or JFR (`jcmd <pid> JFR.start`) |
| Ruby | `stackprof`, `rbspy` |
| Any service with tracing | the span breakdown for one slow request, which shows DB, external calls and app time |

Read the flame graph for wide frames (where time is spent), not tall ones (deep stacks). Time the code spends waiting (I/O, locks, the pool) does not show in a CPU profile, so look at a trace or wall-clock profile for that.

## Database

- **Count queries per request.** Use the ORM's query log (Django `connection.queries` / django-debug-toolbar, Rails `ActiveRecord` logs / bullet, SQLAlchemy `echo=True`, Prisma `log: ['query']`). Many near-identical queries means an N+1: batch them with an eager load, a join, `IN (...)`, or a DataLoader.
- **Read the plan:** `EXPLAIN (ANALYZE, BUFFERS) <query>` (Postgres), `EXPLAIN ANALYZE` (MySQL 8+).

  | You see | Meaning | Move |
  |---|---|---|
  | Seq Scan on a large table, selective filter | no usable index | index shaped like the query: equality columns first, then range or sort |
  | estimated rows far from actual | stale statistics | `ANALYZE <table>`, then re-check the plan |
  | Sort above an index scan | index covers the filter, not the order | add the sort column to the index, in order |
  | Nested Loop with a huge inner loop count | join strategy chosen on bad estimates | fix statistics or rewrite the join |
  | high shared read buffers | data not in cache, IO-bound | narrow the columns, cover the index, or partition |

- **An index will not help** when it isn't selective (filtering on a value that 95% of rows have), on leading-wildcard `LIKE '%x'` (use trigram or full-text search), or on a function of a column (index the expression instead). Every index also slows every write, so measure write cost on write-heavy tables.
- **Unbounded reads:** list endpoints without `LIMIT`, loading a whole table into memory. Paginate with a cursor, or stream in chunks.
- **Row-by-row writes:** use bulk insert or update, and batch commits.
- **Pool exhaustion:** every endpoint slows at once, time is spent waiting for a connection, and the DB shows idle sessions. Use one pool per process, and size it so that instances × pool size stays under the DB's connection limit.
- **Slow query sources:** `pg_stat_statements` (sort by total time, not mean), the MySQL slow query log.

## Memory

- Take heap snapshots at t0, after N operations, and after 2N. Objects that grow proportionally are the leak. Node: `--inspect` + DevTools Memory; Python: `tracemalloc` snapshots compared; Go: `pprof` heap; JVM: heap dump + Eclipse MAT.
- Usual suspects: module-level caches without eviction, event listeners and timers never removed, closures retaining big objects, loading a full result set.

## Frontend

- **Lab:** Lighthouse or the DevTools Performance panel on a production build with CPU and network throttling. **Field:** the `web-vitals` library or CrUX, for what real users see.
- Current Core Web Vitals thresholds live at https://web.dev/articles/vitals. Fetch them rather than recalling them. Last checked 2026-09: good LCP ≤ 2.5 s, INP ≤ 200 ms, CLS ≤ 0.1, at the 75th percentile.
- Bundle size: the bundler's analyzer (`vite-bundle-visualizer`, `webpack-bundle-analyzer`, `next build` output). Look for duplicate libraries, full-library imports, and route code that belongs in a separate chunk.
- Network waterfall: requests chained one after another that could run in parallel, render-blocking CSS or JS, images without dimensions (layout shift), and missing compression or caching headers.
- Main thread: long tasks over 50 ms in the Performance panel, React Profiler for re-render storms, and layout thrashing (reading then writing layout inside a loop).

## Load testing

- Run at a fixed arrival rate, not a fixed number of users. That avoids coordinated omission, where a slow server lowers the load it receives. Tools: `k6`, `vegeta`, `wrk2`, `locust`.
- Step the rate up and plot latency against throughput. The knee is your capacity.
- Never load-test shared or production environments without explicit permission from the people who run them.
