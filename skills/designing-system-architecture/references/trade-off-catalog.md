# Trade-off catalog

Each pair is a pair of options that differ in structure. Pick the axes that match your drivers.

| Axis | Option A favors | Option B favors | Choose B only when |
|---|---|---|---|
| Modular monolith ↔ services | simple deploys, local transactions, easy refactors | independent deploy and scale per team | several teams must ship independently, or parts have very different scaling or runtime needs |
| Sync request/response ↔ async events | simple reasoning, immediate errors, easy debugging | decoupling, absorbing load spikes, fan-out to many consumers | the producer must not wait for consumers, or consumers change often |
| One database ↔ database per context | joins, transactions, a single backup | isolated schemas, independent scaling | contexts are owned by different teams and share little data |
| Managed service ↔ self-hosted | low ops load, fast start | control, cost at very large scale, data residency | a named compliance, cost-at-scale or capability driver exists |
| Relational ↔ document / KV | integrity constraints, ad-hoc queries | flexible shape, very high write throughput on a single key | access patterns are known, narrow and key-based (see `designing-data-models`) |
| Server-rendered ↔ SPA + API | fast first load, SEO, less client code | rich interactivity, offline support, several clients sharing one API | the product is an app, not documents, or mobile clients share the API |
| Serverless ↔ long-running | scale to zero, no servers to patch | steady cost at constant load, long connections, warm caches | load is steady and high, or cold starts break a latency target |
| Strong ↔ eventual consistency | correctness without extra reasoning | availability and latency across regions | the business tolerates stale reads, stated per entity |
| Single region ↔ multi-region | simplicity, cheap consistency | regional failure tolerance, latency for global users | an availability target or user latency requires it, and the team can run failovers |
| Build ↔ buy | differentiation, control | time to market, maintenance offloaded | build only if it is the differentiator or no vendor meets a hard driver |

## Cost signals to include in the trade-off table

- **Ops load:** number of deployables, number of stateful components, and the on-call surface.
- **Cognitive load:** the number of concepts a new engineer must learn before shipping a change.
- **Coupling:** how many components must change, or deploy, for a typical feature.
- **Exit cost:** the effort to reverse the choice after one year of data and callers.

## Smells in an option

- A distributed monolith: services that must deploy in lockstep, or that share tables.
- Chatty boundaries: one user action causes more than about 10 cross-service calls.
- Entity services (`UserService`, `OrderService`) with no behavior: they split data along boundaries that don't reflect the business.
- Queues added only for "decoupling", with no named driver and no one owning the dead-letter queue.
