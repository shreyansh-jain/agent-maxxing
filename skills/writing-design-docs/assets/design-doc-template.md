# <Title>

| | |
|---|---|
| Status | Draft / In review / Approved / Rejected / Superseded by <link> |
| Author(s) | |
| Reviewers | <owners of affected systems> |
| Created / Updated | YYYY-MM-DD / YYYY-MM-DD |
| Related | <spec, issues, ADRs, threat model> |

## Summary

In one paragraph: the problem, the recommended design, the main trade-off, and the decision you need from reviewers.

## Context

Describe the current system and why a change is needed now. Include the relevant numbers (traffic, data size, error rates, cost), each with its source. Link to code and to earlier docs.

## Goals

- Measurable goal (e.g. "p99 read latency < 150ms at 3x current peak")

## Non-goals

- A tempting adjacent problem you are explicitly not solving

## Proposed design

### Overview
A diagram (Mermaid or a list of edges) and a short narrative.

### Components and responsibilities
### Data model and ownership
### APIs / contracts
Include a request/response example and the error cases.

### Key flows
Numbered steps, including what happens when each dependency is slow or down.

### Consistency, concurrency and idempotency
### Capacity and performance assumptions

## Alternatives considered

| Option | Summary | Pros | Cons | Why not |
|---|---|---|---|---|
| Do nothing / extend existing | | | | |
| Option B | | | | |

## Trade-offs and risks

The riskiest assumptions go first. Give each one a mitigation or a validation plan.

## Security and privacy

Trust boundaries, main threats, and mitigations (link the threat model). Personal data touched, with retention and deletion (link the data inventory). Otherwise write "N/A, because …".

## Observability

The signals that show this works, the dashboards, and the alerts with their runbooks.

## Rollout and migration

The phases, the flags, and the backfill or dual-write plan. Exit criteria for each phase.

## Rollback

What reverts, and how. What cannot be reverted, and the point of no return.

## Cost

Infrastructure and vendor cost at current and projected load. The operational burden.

## Ownership

Who runs it, who is on call, and where the runbook lives.

## Open questions

| Question | Owner | How it gets resolved | Blocking? |
|---|---|---|---|

## Decision log

| Date | Decision | Decided by | Notes |
|---|---|---|---|

---

**One-pager:** keep Summary, Context, Proposed design (overview only), Alternatives considered, Trade-offs and risks, Rollout and rollback, and Open questions.
