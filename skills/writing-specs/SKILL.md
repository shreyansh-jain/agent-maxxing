---
name: writing-specs
description: Written specification for a feature, subsystem, or significant change, produced from an agreed intent and the current code. Use when the user asks for a spec, PRD, requirements or design doc, when an architectural change has confirmed intent but nothing written down, or when vague requirements need turning into testable success criteria before planning.
license: Apache-2.0
metadata:
  version: "0.1.0"
  category: "define"
  sources: "addyosmani/agent-skills spec-driven-development (MIT); mattpocock/skills to-spec (MIT); obra/superpowers brainstorming (MIT); garrytan/gstack spec (MIT)"
---

# Writing Specs

A spec records every decision someone would otherwise have to guess at, and it states success as conditions a test can check.

## When to use

- The user asks for a spec, PRD, requirements doc, or design doc
- Intent is confirmed for an architectural change, but nothing is written down yet
- Requirements exist only as adjectives ("faster", "more robust") and need measurable criteria
- One request spans several capabilities that can be tested independently and need separating

**Not for:** discovering what the user wants in the first place (use `clarifying-intent` first); breaking an approved spec into tasks (use `planning-implementation`); recording one architecture decision after the fact (use `documenting-decisions`).

## Process

1. **Start from the confirmed intent.** Carry the restated outcome, user, success conditions, and out-of-scope items over exactly as they were confirmed. If none exist, or the ask is still ambiguous, switch to `clarifying-intent` and come back afterwards.
   Exit: the intent section can be written without guessing.

2. **Read the code before writing any technical content.** Find the modules this touches, the interfaces it must respect, similar features to copy from, and the project's existing test seams. Use the project's own domain vocabulary. Respect ADRs in the area. If the repo already uses a spec system (OpenSpec, RFC folder, issue templates), write in that format and save where it expects.
   Exit: you can name the existing modules and interfaces involved, with evidence.

3. **Surface assumptions first.** Before you draft, list everything you are assuming and have not been told: platform, auth model, data volume, browser support, backward compatibility. Ask the user to correct the list. Silent assumptions are how specs go wrong.
   Exit: the user has seen the assumption list.

4. **Scope check.** If the work covers several independent subsystems, propose one spec per subsystem. Each spec should produce software that works and can be tested on its own.
   Exit: one spec, one coherent deliverable.

5. **Draft, using the template in Output.** Rules for the draft:
   - Success criteria are measurable. Reframe "make search faster" as "p95 search latency < 300 ms on the 1M-row fixture".
   - Behaviors are numbered, one observable behavior each ("As a <user>, I can <action>, so that <benefit>"), and cover the error and empty cases too, not only the happy path.
   - Decisions describe modules, interfaces, contracts, and schema changes, *not* file paths or code, because those go stale. The one exception: a type or state machine settled by a prototype may be included as a snippet.
   - Testing names the seams where behavior will be verified. Prefer existing seams, and as few as possible.
   Exit: every section is filled or explicitly marked "none".

6. **Self-review with fresh eyes.** Check for:
   - placeholders (`TBD`, "handle errors appropriately");
   - contradictions between sections;
   - requirements that could be read two ways;
   - success criteria no test could check;
   - behaviors with no testing seam.
   Fix what you find inline.
   Exit: a clean pass.

7. **Get approval on the written file.** Save it where the repo keeps specs (default `docs/specs/YYYY-MM-DD-<topic>.md`), then ask the user to review the file itself. Approving the conversation does not approve the document. If the user has asked you to commit or file an issue, do it once they approve.
   Exit: explicit approval of the written spec. Then hand off to `planning-implementation`.

## Output

```markdown
# Spec: <name>

## Problem
<The user's problem, from the user's point of view.>

## Outcome and success criteria
- <measurable condition>   ← each one checkable by a test or a metric

## Behaviors
1. As a <user>, I can <action>, so that <benefit>.
2. When <error or empty case>, the system <observable response>.

## Decisions
- Modules: <built or changed, and each one's responsibility>
- Interfaces and contracts: <APIs, events, types, error semantics>
- Data: <schema changes and migration needs>

## Testing
- Seams: <where behavior is verified>; prior art: <similar existing tests>

## Boundaries
- Always: <e.g. validate input at the API edge>
- Ask first: <e.g. new dependencies, schema changes>
- Never: <e.g. log PII>

## Out of scope
- <deliberate non-goal>

## Assumptions and open questions
- <assumption, marked confirmed or unconfirmed>
```

## Red flags

- Writing the technical sections before reading the modules they describe
- A success criterion containing "fast", "easy", "robust", or "intuitive" with no number or test
- File paths and function bodies in the Decisions section
- Only happy-path behaviors
- Treating "looks good" in chat as approval of a file the user hasn't opened
- The spec covers three unrelated deliverables
