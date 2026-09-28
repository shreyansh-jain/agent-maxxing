---
name: engineering-products-end-to-end
description: Principal-engineer playbook that takes a product or platform from problem to operated system through gated phases. Use when building a new product, platform or multi-quarter initiative, when work is assessed as C4, or when asked to lead, architect or plan a product end to end.
license: Apache-2.0
metadata:
  version: "0.1.0"
  category: "lead"
  sources: "original; ideas: garrytan/gstack office-hours, plan-eng-review, autoplan, ship (MIT); ideas: addyosmani/agent-skills spec-driven-development, shipping-and-launch (MIT); ideas: mattpocock/skills wayfinder, to-tickets (MIT)"
---

# Engineering Products End to End

A product is done when it is solving the problem it was built for in production, observably and affordably, and the team can operate and change it. Run every phase, gate every one-way door, and ship the thinnest end-to-end slice first.

## When to use

- A new product, platform, major subsystem, or multi-quarter initiative
- `assessing-complexity` returned **C4**
- "Lead this", "architect this end to end", "how would a principal engineer run this?"

**Not for:** a single feature inside an existing product (use `assessing-complexity`, which will pick a C2 or C3 track); only the architecture step (use `designing-system-architecture`); only scoping (use `scoping-product-increments`).

## The rule

```
NO PHASE STARTS UNTIL THE PREVIOUS GATE'S ARTIFACT EXISTS AND THE USER HAS APPROVED IT
```

Gates are cheap on paper and expensive in production. Each phase may be short (a one-page artifact is fine), but none is skipped. The user may explicitly waive a gate; record that as an accepted risk in the decision log.

## Process

Keep artifacts where the repo already keeps docs. Otherwise use `docs/product/<name>/`: `brief.md`, `increments.md`, `design.md`, `adr/`, `launch.md`, `decisions.md`. Each phase ends at a gate, and the gate is the exit criterion.

1. **Frame.** Run `assessing-complexity` on the whole initiative. List the one-way doors (data models, public contracts, vendor lock-in, pricing, data retention). These get the most scrutiny later.
   Gate: complexity card accepted.

2. **Discover the problem.** Use `clarifying-intent` to establish who has the problem, how they cope today, evidence of demand, and what changes for them. Use `measuring-product-outcomes` to define **one success metric, guardrail metrics, and kill criteria** before anything is designed.
   Gate: `brief.md` (problem, users, evidence, metric, guardrails, kill criteria, non-goals) approved.

3. **Shape increments.** Use `scoping-product-increments` to cut the product into increments. Increment 1 is a **walking skeleton**: the thinnest slice that runs end to end through every layer and every deployment step, reaching one real user journey. Sequence by risk: retire the biggest value, usability, feasibility and viability risks first.
   Gate: `increments.md` with an appetite, cut lines and exit criteria per increment approved.

4. **Architect.** Write `design.md` with `writing-design-docs`:
   - quality attributes and targets (latency, availability, consistency, cost ceiling, compliance);
   - `estimating-capacity` for load, storage and cost;
   - `modeling-domains` for bounded contexts and language;
   - `designing-data-models` and `designing-interfaces` for the schemas and contracts behind the one-way doors;
   - `designing-system-architecture`, with 2–3 options and trade-offs, and boring technology by default;
   - `designing-resilient-systems` for failure modes;
   - `modeling-threats` and `handling-personal-data` for security and privacy.

   Record each hard-to-reverse choice with `documenting-decisions`. Then run `reviewing-plans` against the design, with a fresh-context reviewer for the one-way doors.
   Gate: `design.md` and ADRs approved, with the review findings resolved or accepted.

5. **Plan the first increment.** Use `writing-specs` for the increment's behavior, `planning-test-strategy` for which risks get which tests, and `planning-implementation` for ordered vertical-slice tasks. Decide on flags (`managing-feature-flags`), CI (`setting-up-ci-pipelines`) and infrastructure (`writing-infrastructure-as-code`) now, not at launch.
   Gate: spec, test strategy and plan approved.

6. **Build the increment.** Re-run `assessing-complexity` on the increment and follow its C2 or C3 track: `implementing-incrementally` with `test-driven-development`, plus `testing-end-to-end`, `building-accessible-interfaces` and `building-llm-features` where they apply. Every task passes `reviewing-code`; security-sensitive tasks also pass `auditing-security`. Keep the walking skeleton deployable at every step.
   Gate: increment exit criteria met, with evidence from `verifying-before-completion`.

7. **Launch readiness.** Complete `assets/launch-checklist.md`:
   - telemetry from `instrumenting-observability`: SLOs, dashboards, alerts, runbooks;
   - load checked against the capacity estimate (`optimizing-performance`);
   - a security review;
   - rollback rehearsed;
   - data migration rehearsed (`migrating-databases-safely`);
   - a cost ceiling with an alert (`controlling-cloud-costs`);
   - docs and support handoff.

   Gate: go/no-go, where every "no" is either fixed or accepted by the user by name.

8. **Release.** Use `shipping-changes` for a staged rollout behind a flag: internal → beta cohort → percentage steps. Each stage has a bake time, a health signal and an abort threshold. Deploy commands run only when the user approves each one.
   Gate: 100% rollout held for its bake time.

9. **Operate and learn.** Compare the success metric against its target on a fixed date. Handle incidents with `responding-to-incidents`. Log shortcuts in the debt ledger (`managing-technical-debt`). Then decide, with the user and in writing: **iterate** (next increment, back to step 5), **pivot** (back to step 2), or **stop** (the kill criteria were hit).
   Gate: decision recorded in `decisions.md`.

## Output

At the start of each phase, and whenever asked, show the status board:

```
Product: <name>   Tier: C4   Phase: <n. name>   Increment: <k>/<total>
Artifacts: brief ✅ · increments ✅ · design ⏳ · adr (3) · launch ☐
One-way doors: <list, each with its ADR, or "open">
Open risks: <top 3, with owner skill>
Accepted risks: <waived gates, in the user's words>
Next gate: <what must exist, and who approves it>
```

## Rationalizations

| Excuse | Reality |
|---|---|
| "We know what users want, skip discovery" | Then writing the brief takes 20 minutes. Evidence of demand is the most common missing input. |
| "Design everything up front" | Design the one-way doors deeply. Leave two-way doors to the increments. |
| "Build the backend fully, then the UI" | Horizontal layers hide integration risk. The walking skeleton goes through every layer first. |
| "Observability and runbooks after launch" | You can't run a staged rollout without a health signal. It is part of done. |
| "The metric can be decided later" | Without a success metric and kill criteria set in advance, every result looks like success. |

## Red flags

- Architecture work before `brief.md` exists
- Increment 1 cannot be deployed or used end to end
- A one-way door with no ADR
- Launch planned without a rollback, a health signal, or a cost ceiling
- No date set for checking the success metric

## References

- [launch-checklist.md](assets/launch-checklist.md): copy into the product docs at step 7
- [product-brief.md](assets/product-brief.md): copy at step 2
