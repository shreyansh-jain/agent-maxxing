---
name: modeling-domains
description: Domain modeling with a shared glossary, bounded contexts, aggregates and invariants. Use when business terms are ambiguous, entities and rules are being defined for a new domain, a model is anemic or tangled, or domain boundaries are unclear.
license: Apache-2.0
metadata:
  version: "0.1.0"
  category: "architect"
  sources: "mattpocock/skills domain-modeling, codebase-design (MIT); wshobson/agents architecture-patterns (MIT)"
---

# Modeling Domains

Code that uses the business's words and enforces the business's rules in one place stays correct as it grows. Settle the language, draw the boundaries, and put each invariant inside the one object responsible for it.

## When to use

- The same word means different things to different people or modules ("account", "order", "customer")
- Starting a domain with real business rules: billing, scheduling, inventory, claims, logistics
- Rules are scattered across controllers, jobs and UI checks, and they disagree
- Deciding where a service or module boundary should go
- Entities are bags of getters and setters while "services" hold all the logic

**Not for:** table and index design (use `designing-data-models`); overall system topology (use `designing-system-architecture`); a single module's API shape (use `designing-interfaces`); recording a decision (use `documenting-decisions`).

## Process

1. **Decide how much modeling this needs.** CRUD over forms with few rules needs a glossary and nothing more. Full tactical DDD (aggregates, domain events, context maps) earns its cost only when the rules are complex, change often, and are expensive to get wrong. Say which case this is.
   Exit: one stated level of modeling, either glossary only or full tactical model, with the reason.

2. **Collect the language from the source.** Read the code, schema, tickets and docs, and note every noun and verb the business uses. Wherever two terms mean the same thing, or one term means two things, ask the user or a domain expert. Never guess. Use concrete scenarios to force precision. For example: "A customer cancels one item of a shipped order. Is that a cancellation, a return, or a refund?"
   Exit: every ambiguous term is resolved or listed as an open question.

3. **Write the glossary.** Put it in `CONTEXT.md`, or in the repo's existing equivalent. Each entry is the term, a one-line definition, what it is *not*, and any synonyms that are banned. Include no implementation detail. Create the file only once there is a first resolved term. After that, update it as each term settles; do not batch the updates.
   Exit: the glossary exists and the code's names match it, or the mismatches are listed.

4. **Event-storm lite.** List the business events in time order, in past tense: `OrderPlaced`, `PaymentCaptured`, `ShipmentDispatched`. Beside each event, write the command that triggers it, who issues that command, and the rule that can reject it. Clusters of events that share language and rules suggest bounded contexts.
   Exit: a timeline of events → commands → rules.

5. **Draw the bounded contexts.** A context is a boundary inside which each term has exactly one meaning. The same real-world thing can appear in several contexts under different models; for example, `Product` in Catalog and `Product` in Inventory. Draw a context map in mermaid showing how the contexts relate: upstream/downstream, shared kernel, anti-corruption layer, or published language.
   Exit: a context map in which every integration arrow names its relationship.

6. **Find the aggregates and their invariants.** An aggregate is the smallest cluster of objects that must be consistent in a single transaction. State each invariant as a rule, such as "an order's total equals the sum of its lines" or "a seat is booked at most once per show". Keep aggregates small. Reference other aggregates by ID, not by object. Rules that span aggregates are enforced eventually, through domain events or a process manager.
   Exit: each aggregate has a root, its invariants, and the commands that change it.

7. **Put behavior where the invariant lives.** Methods on the aggregate root enforce its rules (`order.addLine(...)` rejects a closed order). Setters that let callers bypass the rules must not exist. Use value objects (Money, EmailAddress, DateRange) for concepts that carry validation or units, and avoid bare primitives for them.
   Exit: no caller outside the aggregate can put it into an invalid state.

## Output

```
Modeling level: glossary only | full tactical, because <reason>
Glossary: <CONTEXT.md entries added/changed>
Event timeline: <event ← command ← actor, rule>
Context map: <mermaid, relationships labelled>
Aggregates: <root → invariants → commands>
Open questions for domain experts: <list>
```

## Red flags

- Choosing names before the business vocabulary is settled
- One `User` or `Account` model shared by every module, with a growing pile of nullable fields
- Business rules enforced in controllers, UI or SQL triggers instead of the aggregate
- Aggregates holding object references to other aggregates, so one transaction locks half the database
- Full DDD ceremony on a CRUD admin screen
- Resolving a term by picking the one you like instead of asking the domain expert

## References

- [patterns.md](references/patterns.md): open at step 5 or 6 for context-map relationships, aggregate sizing rules, and a CONTEXT.md entry format
