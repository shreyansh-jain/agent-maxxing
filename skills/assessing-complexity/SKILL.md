---
name: assessing-complexity
description: Principal-engineer triage that scores a piece of work on risk dimensions and picks the process track and skills it needs. Use when starting any non-trivial task, feature, project or product, when asked how big or risky something is, or when unsure how much design, review and rollout rigor a change deserves.
license: Apache-2.0
metadata:
  version: "0.1.0"
  category: "lead"
  sources: "original; ideas: garrytan/gstack plan-eng-review (MIT); ideas: obra/superpowers brainstorming (MIT); ideas: addyosmani/agent-skills spec-driven-development (MIT)"
---

# Assessing Complexity

Rigor should match risk. Score the work on what makes it dangerous, not on how much typing it takes, then run exactly the process that level of risk needs: no more, no less.

## When to use

- At the start of any task larger than a one-line fix, before choosing how to work
- "How big is this?", "how risky is this?", "what's the plan of attack?", "do we need a design doc?"
- A task that looked small keeps growing, touches data, or reaches other teams
- Before committing to an estimate or a timeline

**Not for:** interviewing the user about what they want (use `clarifying-intent`, which this skill usually precedes or follows); running the full product lifecycle once the track is C4 (use `engineering-products-end-to-end`); sizing infrastructure load (use `estimating-capacity`).

## The rule

```
SCORE BEFORE YOU START, AND LET THE HIGHEST-RISK DIMENSION SET THE TRACK
```

Risk does not average out. A two-line change that rewrites production data is a C3 no matter how small the diff.

## Process

1. **Gather facts first.** Read the request, the code it touches, the callers, the data it reads or writes, and recent history in that area. Never score from the prompt alone: complexity hides in callers, data, and integrations.
   Exit: you can name the files, services, data stores and external parties involved, or you have listed what is unknown.

2. **Score eight dimensions, 0–3 each.** Use the anchors below, and cite evidence for every score above 0.

   | Dimension | 0 | 1 | 2 | 3 |
   |---|---|---|---|---|
   | **Scope** | 1 file | one module | several modules or one service | several services or repos |
   | **Uncertainty** | done here before | known pattern, new to this repo | new to the team | unknown whether it is possible or wanted |
   | **Reversibility** | `git revert` undoes it | needs a redeploy or config rollback | a data migration or backfill to undo | one-way door: deleted data, published contract, sent emails, money moved |
   | **Blast radius** | developers only | some users, degraded | all users, or a core flow | money, security, legal, or safety |
   | **Coupling** | self-contained | one internal consumer | several teams or an external API | contract with external customers or partners |
   | **Data sensitivity** | none | internal data | personal data (PII) | regulated: payments, health, credentials, children |
   | **Scale / performance** | irrelevant | known load, existing path | new hot path or bigger volume | SLO-critical or order-of-magnitude growth |
   | **Operability** | no runtime change | new config or flag | new job, queue or cron | new service, datastore or on-call surface |

   Exit: eight scores, each with a one-line reason.

3. **Derive the tier: highest floor wins.**
   - **C0 Trivial:** every dimension is 0 (a typo, a copy change, a constant with an obvious effect).
   - **C1 Small:** the maximum score is 1.
   - **C2 Feature:** the maximum score is 2.
   - **C3 System:** any dimension scores 3, *or* Reversibility plus Blast radius is 4 or more.
   - **C4 Product:** it is a new product, platform or multi-quarter initiative, *or* four or more dimensions score 3.
   - **Spike:** the deliverable is an answer ("can we…?"), not kept code. Time-box it, then re-assess.

   If the scores sit on a boundary, take the higher tier. Exit: one tier, plus the dimension that set it.

4. **Pick the track.** Run every skill listed for the tier, in order. Skills in *italics* are conditional: run them when their dimension scored 2 or more.

   | Tier | Track |
   |---|---|
   | C0 | edit → `verifying-before-completion` |
   | C1 | brief confirm of intent → `test-driven-development` → `verifying-before-completion` → self-review with `reviewing-code` |
   | C2 | `clarifying-intent` → `writing-specs` (short) → `planning-implementation` → `implementing-incrementally` + `test-driven-development` → `reviewing-code` → `shipping-changes` |
   | C3 | the C2 track, plus `writing-design-docs` and `reviewing-plans` before any code, `planning-test-strategy`, a staged rollout via `managing-feature-flags`, and `instrumenting-observability`. Conditional: *`designing-system-architecture`* (Scope, Operability), *`modeling-threats`* and *`auditing-security`* (Blast radius, Data), *`handling-personal-data`* (Data), *`migrating-databases-safely`* (Reversibility), *`estimating-capacity`* and *`optimizing-performance`* (Scale), *`designing-resilient-systems`* (Coupling, Operability), *`designing-interfaces`* (Coupling) |
   | C4 | `engineering-products-end-to-end`, which runs C3 tracks per increment |
   | Spike | a question and a time-box agreed in two sentences → throwaway code on a scratch branch → a written answer → re-assess the real work |

   Exit: an ordered list of skills and the gates that need the user's sign-off.

5. **Publish the card and get agreement.** Show the Output card before starting work. The user may choose a lighter track. Record that choice as an **accepted risk** in their words; never downgrade silently.

6. **Re-assess on new evidence.** Re-score whenever you discover a new data store, a new consumer, a migration, a security boundary, or a scope increase over 50%. The ratchet only turns one way: step up and say so. If a lighter track now looks right, propose it; don't just take it.

## Output

```
Complexity: C<n> <name>   (set by: <dimension>=<score>, <reason>)
Scores: Scope 2 · Uncertainty 1 · Reversibility 3 · Blast 2 · Coupling 1 · Data 2 · Scale 0 · Ops 1
Evidence: <one line per score ≥2, with file/service names>
Track: <ordered skills>
Gates needing your sign-off: <e.g. design doc, migration plan, prod rollout>
Unknowns that could raise the tier: <list>
Accepted risk: <none | the user's words>
```

## Rationalizations

| Excuse | Reality |
|---|---|
| "It's only a few lines" | Lines measure effort, not risk. Score Reversibility and Blast radius first. |
| "The average score is low" | Averages hide the one dimension that pages someone at 3am. Highest floor wins. |
| "Process will slow us down" | Under-scoped C3 work is the slowest path: rework, incidents, rollbacks. Over-process on C1 is also waste, so match the tier. |
| "I'll scope it once I start coding" | Scoring takes minutes, and its evidence gathering is work you need anyway. |
| "The user wants it fast, so C1" | Speed is the user's call to make explicitly, as an accepted risk, not yours to assume. |

## Red flags

- Scoring without having opened the code or the data model
- A score of 3 anywhere, yet the plan has no design doc or rollout
- The words "migration", "backfill", "auth", "payment", "delete" or "public API" appear and Reversibility or Blast radius is 0–1
- Tier dropped mid-task without the user agreeing
- A C0/C1 task whose diff now spans several modules

## References

- [scoring-anchors.md](references/scoring-anchors.md): open when a dimension is ambiguous, or to calibrate against worked examples
