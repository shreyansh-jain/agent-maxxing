---
name: designing-system-architecture
description: System-level architecture design for new products, services and major re-platforms, driven by quality attributes and explicit trade-offs. Use when choosing how components, services, data stores and integrations fit together, or when splitting, merging or re-platforming a system.
license: Apache-2.0
metadata:
  version: "0.1.0"
  category: "architect"
  sources: "garrytan/gstack plan-eng-review (MIT); wshobson/agents architecture-patterns, microservices-patterns (MIT); mattpocock/skills codebase-design (MIT); addyosmani/agent-skills api-and-interface-design (MIT)"
---

# Designing System Architecture

Architecture is choosing which qualities you will pay for. Name those qualities with numbers first, generate real alternatives, and pick the simplest one that meets them, preferring choices you can undo.

## When to use

- A new product, service or major feature that needs components, data stores and integrations decided
- "Should this be a separate service?", "monolith or microservices?", "which queue or database?"
- Re-platforming, splitting a monolith, merging services, or moving to event-driven
- Build vs buy for a component such as auth, search, payments or a workflow engine

**Not for:** sizing the load on an architecture you already chose (use `estimating-capacity`); defining entities and domain boundaries (use `modeling-domains`); table and index design (use `designing-data-models`); timeouts, retries and failure handling (use `designing-resilient-systems`); a single module or API signature (use `designing-interfaces`); writing up the result for review (use `writing-design-docs`).

## The rule

```
NO ARCHITECTURE CHOICE WITHOUT NAMED QUALITY TARGETS AND AT LEAST TWO REAL ALTERNATIVES
```

Violating the letter of the rule is violating the spirit of the rule. With only one option you haven't made a design decision, only a default choice.

## Process

1. **Pin the drivers.** Write down the quality attributes as numbers, not adjectives. For example: p99 latency under 300 ms; 99.9% availability; read-your-writes consistency for orders; 50k DAU in year one; under $2k/month infrastructure; one on-call team of four. Add the hard constraints (regulation, existing stack, deadline, team skills) and what is explicitly *not* required.
   Exit: a driver table where each row has a target or the word "unknown", and every "unknown" has an owner. If the load numbers are unknown, run `estimating-capacity` first.

2. **Map the context.** Draw a C4 context diagram in mermaid: the system as one box, its users, and each external system it talks to. Then draw a container diagram (apps, services, data stores, queues). Label every arrow with its protocol and whether it is sync or async.
   Exit: every external dependency and data store appears on the diagram.

3. **Generate 2–3 options that differ in structure.** Two variants of the same design are not alternatives. Good pairs: a modular monolith vs services; sync request/response vs an event log; managed service vs self-hosted; one database vs one per bounded context. When a subagent tool is available, have separate agents draft options under different stances (minimal, clean, scale-ready) so they do not converge.
   Exit: each option has a container diagram and a one-paragraph description.

4. **Score against the drivers.** Build a table with options as columns and drivers as rows. Add these rows:
   - operational load (things to run, page on and upgrade)
   - team fit, per Conway's law: every service boundary needs an owning team
   - cost at the expected load and at 10× that load
   - time to first release
   - **reversibility**. A one-way door (data store choice, public API, tenancy model) deserves a slow decision. A two-way door (library, internal protocol) deserves a fast one.

   Exit: every cell is filled, and the losing options lose for a stated reason.

5. **Spend innovation tokens deliberately.** Default to the boring technology the team already runs. Each new language, datastore or paradigm costs one of about three tokens available to a team, and must buy a driver that nothing boring can meet.
   Exit: every non-boring choice names the driver it buys.

6. **Decide build vs buy for each non-core component.** Buy (or use managed) unless the component is your product's differentiator, or vendor lock-in, cost at scale, or a compliance issue is a named driver. Record the exit plan for each vendor.

7. **Find the failure and scaling edges.** For the chosen option, walk each arrow and ask what happens when this dependency is slow, down or wrong. Then ask what breaks first at 10× load. Hand the detailed answers to `designing-resilient-systems`.
   Exit: the top three risks, each with a mitigation or an explicit acceptance.

8. **Record the decision.** Write one ADR for each one-way door (use `documenting-decisions`). For a design that others must review, write it up with `writing-design-docs`.

## Output

```
Drivers: <table of quality attributes with targets>
Context + container diagrams: <mermaid>
Options: A <name>, B <name>, (C <name>)
Trade-off table: drivers × options, plus ops load, team fit, cost@1x/10x, time-to-first-release, reversibility
Decision: <option>, because <drivers it wins on>; accepted costs: <what we give up>
Innovation tokens spent: <choice → driver>
Top risks: <risk → mitigation | accepted>
One-way doors recorded as ADRs: <list>
```

## Rationalizations

| Excuse | Reality |
|---|---|
| "Everyone uses microservices" | Services are an org-scaling tool. Without separate teams and independent deploy needs, you pay distributed-system costs for nothing. |
| "We might need to scale to millions" | Design for 10× the expected load and keep a path to 100×. Designing for a million users on day one delays the day you get any. |
| "The requirements are obvious" | Then writing the driver table takes five minutes, and it will show where the requirements conflict. |
| "This is the modern stack" | Modern costs innovation tokens. Name the driver it buys, or use what the team already operates. |
| "We'll figure out ops later" | Ops load is a first-class driver. A design the team cannot run at 3am is a broken design. |

## Red flags

- A diagram with no numbers anywhere near it
- One option presented as "the architecture"
- A new datastore or language for a problem the existing one handles
- Service boundaries that don't match team boundaries, or services that must deploy together
- A shared database written by several services
- A synchronous call chain of more than three hops on a user-facing path
- No answer to "how do we undo this?" for a one-way door

## References

- [trade-off-catalog.md](references/trade-off-catalog.md): open at step 3 to find structurally different options and the drivers each one favors
