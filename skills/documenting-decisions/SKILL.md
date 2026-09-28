---
name: documenting-decisions
description: Architecture decision records and keeping project docs in step with shipped code. Use when a hard-to-reverse technical choice is made or revisited, when asked to write or supersede an ADR, when a change adds or alters public surface (API, CLI flag, config, env var), or when asked to update or audit docs after a feature lands.
license: Apache-2.0
metadata:
  version: "0.1.0"
  category: "docs"
  sources: "addyosmani/agent-skills documentation-and-adrs (MIT); mattpocock/skills domain-modeling (MIT); garrytan/gstack document-release, document-generate (MIT)"
---

# Documenting Decisions

Code shows what was built. Docs record why it was built that way and how to use it. Write the why when a decision is made, and bring the how-to up to date when the public surface changes.

## When to use

- A choice was made that is expensive to reverse: a datastore, an auth strategy, an API style, a module boundary, a major dependency
- An existing decision is being revisited or replaced
- A change adds, renames, or removes public surface: an endpoint, an exported function, a CLI flag, a config key, an env var
- The user asks to "update the docs" or "sync documentation" after shipping

**Not for:** agent instruction files like AGENTS.md or CLAUDE.md (use `writing-agent-context-files`); the requirements for work not yet built (use `writing-specs`); PR descriptions (use `writing-commits-and-prs`); code comments, which belong to the change itself.

## Process

### A. Recording a decision

1. **Decide whether it deserves an ADR.** Write one only when all three hold: it is **hard to reverse**, a future reader would find it **surprising without context**, and it came from a **real trade-off** between genuine alternatives. If any is missing, a line in the PR or a code comment is enough.
   Exit: you can name the alternatives that were rejected.

2. **Match the existing convention.** Look for `docs/adr/`, `docs/decisions/`, `adr/`, an `.adr-dir` file, or ADRs with a different extension or markup. Continue their numbering, filename pattern and headings. If the evidence conflicts, raise the conflict with the user instead of adding a third scheme. Use [assets/adr-template.md](assets/adr-template.md) only when there is no convention.
   Exit: the path and number of the new ADR are chosen.

3. **Write it from evidence.** Context holds the forces and constraints that were true at the time. Decision holds what was chosen, in one or two sentences. Alternatives lists each option and why it lost. Consequences covers both the good and the bad. Get facts from the conversation, the spec, and the code. Mark anything you inferred as an assumption, and never invent benchmark numbers or quotes.
   Exit: a reader who missed the discussion could argue with the decision on its merits.

4. **Keep the history.** Never edit an accepted ADR's decision. Write a new ADR that supersedes it, and change only the old one's status line to `Superseded by ADR-NNNN`.

### B. Syncing docs after a change

1. **Extract the changed public surface** from `git diff <base>...HEAD`. Look for new or renamed exports, endpoints, commands, flags, config keys, env vars, and removed features.

2. **Build a coverage map** for each item using the four documentation kinds (Diátaxis):
   ```
   item              reference   how-to   tutorial   explanation
   --dry-run flag    README ✓    ✗        n/a        ✗
   POST /exports     ✗           ✗        ✗          ✗   ← critical gap
   ```
   Reference says what it is and its options. How-to shows how to do a task with it. Tutorial is a guided first use. Explanation says why it works this way. Not every item needs all four; every item needs at least reference.
   Exit: every changed item has a row.

3. **Fix what is safe, ask about the rest.** Directly update facts that are now wrong: commands, flags, paths, defaults, examples. Ask before rewriting narrative sections, restructuring docs, or deleting pages. Flag architecture diagrams that no longer match the code, but don't redraw them unasked.

4. **Check that examples work.** Run or type-check every command and code snippet you added or changed, if the user's instructions allow. A doc example that doesn't run is worse than no example.

## Output

For an ADR: the file at its conventional path, plus one line saying what it supersedes, if anything.

For a doc sync:
```
Updated: README.md (--dry-run in flags table), docs/api.md (POST /exports reference)
Needs a decision: docs/guides/exporting.md narrative predates async exports: rewrite?
Gaps left: no how-to for resuming a failed export
Diagram drift: docs/architecture.md still shows the sync export path
```

## Red flags

- Writing an ADR for a choice that could be reversed in an afternoon
- Starting a new numbering or folder scheme next to an existing one
- Editing the decision of an accepted ADR instead of superseding it
- Inventing rationale, numbers, or alternatives that nobody discussed
- Adding a doc example you never ran

## References

- [assets/adr-template.md](assets/adr-template.md): copy when the repo has no ADR convention
