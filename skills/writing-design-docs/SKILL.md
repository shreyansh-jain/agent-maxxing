---
name: writing-design-docs
description: Technical design documents and RFCs that decide how a system or change will be built. Use when asked for a design doc, RFC, tech spec or architecture proposal, or when a change spans services or teams, is hard to reverse, or needs alternatives weighed first.
license: Apache-2.0
metadata:
  version: "0.1.0"
  category: "architect"
  sources: "addyosmani/agent-skills documentation-and-adrs, spec-driven-development (MIT); garrytan/gstack plan-eng-review (MIT); mattpocock/skills to-spec (MIT); obra/superpowers brainstorming (MIT)"
---

# Writing Design Docs

A design doc exists to get a decision made cheaply before code makes it expensive. It earns its length only through the alternatives it rules out and the trade-offs it makes visible.

## When to use

- A change spans several services, teams or data stores, or introduces a new one
- It is hard to reverse: data model, public API, protocol, vendor, storage engine, tenancy model
- Several reasonable designs exist and people disagree
- "Write an RFC / design doc / tech spec for …", or a reviewer asks "what else did you consider?"

**Not for:** defining *what* to build and why, meaning users, requirements and success criteria (use `writing-specs`); breaking an agreed design into tasks (use `planning-implementation`); recording a single decision after the fact (use `documenting-decisions`); reviewing someone else's design (use `reviewing-plans`).

## Do you need one?

| Situation | Artifact |
|---|---|
| Local change, one obvious approach, easy to revert | No doc. A good PR description is enough |
| One decision with real alternatives | An ADR (`documenting-decisions`) |
| One team, a few days to two weeks, some risk | A **one-pager**: context, proposal, alternatives, risks, rollout |
| Cross-team, new service or data model, irreversible, or weeks of work | A **full design doc**, using [assets/design-doc-template.md](assets/design-doc-template.md) |

If the repo has an RFC or design-doc convention (a `docs/rfcs/` folder, a numbering scheme, a template), use it instead of this one.

## Process

1. **Ground it.** Read the spec or issue, the code the design touches, the existing ADRs, and any earlier docs in the area. List the constraints you found: SLAs, data volumes, existing contracts, team ownership, deadlines. Where you estimated numbers, say so.
   Exit: a context section a newcomer could follow, with every claim about the current system traceable to code or docs.

2. **State goals and non-goals.** Goals are measurable ("p99 < 200ms at 5k rps", "tenant data isolated at the storage layer"). Non-goals are the tempting adjacent problems you are explicitly *not* solving. They prevent scope creep in review.
   Exit: 3–6 goals, each checkable, and at least 2 non-goals.

3. **Generate real alternatives before choosing.** Sketch at least two genuinely different designs, plus "do nothing / extend what exists". Compare them on the same dimensions: complexity, cost, latency, reliability, security, migration effort, team fit, reversibility. For high-stakes choices, consider having separate subagents each argue for one option.
   Exit: a comparison table, with each rejected option given a specific rejection reason.

4. **Detail the chosen design at the level reviewers need.** Cover these parts:
   - components and their responsibilities;
   - data model and ownership;
   - APIs or contracts, with examples;
   - key flows as sequence steps, including failure paths;
   - consistency and concurrency behavior;
   - capacity assumptions.
   Diagrams go in as text: Mermaid, or a list of edges. Stop before implementation detail that belongs in the plan.
   Exit: a reviewer can say what happens when each dependency fails, and where each piece of data lives.

5. **Cover the cross-cutting sections.** Every section below gets real content, or "N/A, because …":
   - **Security and privacy.** Link a `modeling-threats` output for anything crossing trust boundaries, and a `handling-personal-data` inventory if it touches PII.
   - **Observability.** What proves this is working, and what pages someone.
   - **Rollout and migration.** Flags, phases, backfills, and dual running.
   - **Rollback.** What reverts, and what cannot.
   - **Cost.**
   - **Operational ownership.**
   Exit: no section is blank, and irreversible steps are called out explicitly.

6. **Surface risks and open questions.** List the unknowns that could change the decision, each with who resolves it and how (spike, load test, vendor call). Put the riskiest assumptions first. A doc with no open questions was usually written after the decision.
   Exit: each open question has an owner, or is marked blocking.

7. **Run the review.** Put a one-paragraph summary and the decision you are asking for at the top. Name the reviewers who own affected systems. Collect comments, then either update the doc or answer the comment in writing. Record the outcome in the decision log: approved, approved with changes, or rejected, plus who decided and when. When the approved design changes materially during implementation, update the doc or supersede it.
   Exit: the decision log has an entry, and status is `Approved`, `Rejected` or `Superseded`.

## Output

A Markdown file following the repo's convention, or `docs/design/<yyyy-mm-dd>-<slug>.md`, from the template. The first screen must answer: what is being decided, the recommendation, the main trade-off, and what is needed from the reader.

## Red flags

- Only one option presented, or straw-man alternatives nobody would pick
- Goals like "scalable", "robust" or "clean" with no number or test
- Security, rollout or rollback left as "TBD" in a doc marked ready for review
- Implementation detail (file-by-file changes) crowding out the decision
- Claims about the current system with no reference to code or docs
- The doc is written after the code merged, to justify it

## References

- [design-doc-template.md](assets/design-doc-template.md): the full template; copy it for full docs, or cut to the one-pager sections
