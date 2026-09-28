# Domain modeling patterns

## CONTEXT.md entry format

```markdown
## Order
A customer's confirmed request to buy one or more items, with a fixed price.
Not: a Cart (unconfirmed, prices may change) or a Shipment (physical fulfilment).
Avoid: "purchase", "transaction".
```

Use one entry per term. Keep the definitions in business language. Put implementation details, table names and API fields somewhere else.

## Context-map relationships

| Relationship | Meaning | Use when |
|---|---|---|
| Upstream / downstream | the downstream context depends on the upstream context's model | the default for most integrations |
| Customer / supplier | the downstream team can negotiate what the upstream team provides | both teams sit in the same org and plan together |
| Conformist | the downstream context adopts the upstream model as-is | the upstream won't change and its model is good enough |
| Anti-corruption layer | the downstream context translates the upstream model into its own | integrating a legacy system or third party whose model would pollute yours |
| Shared kernel | a small shared model owned jointly | two contexts truly share a concept and the teams coordinate closely; keep it tiny |
| Open host / published language | the upstream context publishes a stable, documented contract | many consumers need the same integration |

## Aggregate sizing rules

1. Design small aggregates. Most aggregates are a root plus value objects.
2. Only a true invariant justifies putting two things in one aggregate. "They are often loaded together" does not.
3. Reference other aggregates by ID.
4. Change one aggregate per transaction. Coordinate changes across aggregates with domain events and eventual consistency.
5. If an aggregate is frequently contended or grows without bound (an order with 100k lines), it is too big. Split it.

## Invariant checklist

For each rule, ask:
- Which aggregate owns it?
- Does it need to be immediately consistent, or is eventual consistency acceptable? Ask the business how long a delay is acceptable.
- What happens when it is violated? Reject the command, compensate afterwards, or alert a human.

## Anemic model symptoms and the fix

| Symptom | Fix |
|---|---|
| `OrderService.addLine(order, line)` checks the order's status | Move the check to `order.addLine(line)` |
| Public setters on every field | Replace them with intention-revealing commands (`order.cancel(reason)`) |
| Validation duplicated across the API, jobs and UI | Put the validation in value-object constructors and aggregate methods |
| Strings and numbers used for money, email and dates | Introduce value objects that carry units and validation |

## When DDD is overkill

- CRUD over a small number of entities with few rules
- Prototypes, where speed of learning matters more than correctness
- Integration glue whose model belongs to another system

In these cases, keep the glossary and skip the rest.
