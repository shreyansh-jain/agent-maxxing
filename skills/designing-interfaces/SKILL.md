---
name: designing-interfaces
description: Interface and module design for APIs, public functions, module boundaries and service contracts. Use when designing a new API or endpoint, choosing what a module exposes, deciding where a seam belongs, changing a contract other code depends on, or when code is hard to test or call.
license: Apache-2.0
metadata:
  version: "0.1.0"
  category: "build"
  sources: "mattpocock/skills codebase-design (MIT); addyosmani/agent-skills api-and-interface-design (MIT)"
---

# Designing Interfaces

Good modules are deep: a small interface hides a lot of behavior, and every observable behavior of that interface is a promise someone will depend on.

## When to use

- Designing a new REST, GraphQL, RPC or library API, or a CLI surface
- Deciding what a module, class or package exposes, and what it hides
- A function is hard to test, has many parameters, or callers must know its internals to use it
- Changing a contract that other teams, services or clients depend on
- Choosing between several designs for the same capability

**Not for:** writing the requirements the interface serves (use `writing-specs`); restructuring existing code without changing its contract (use `simplifying-code` or `refactoring-legacy-code`); removing or migrating an old API (use `upgrading-dependencies` for consumers, `migrating-databases-safely` for schemas).

## Vocabulary

Use these terms precisely, and keep using them, so the design conversation stays unambiguous.

| Term | Meaning |
|---|---|
| **Interface** | everything a caller must know: signature, invariants, ordering, error modes, config, performance |
| **Depth** | the behavior a caller gets per unit of interface they must learn |
| **Seam** | the place where behavior can be swapped without editing callers; the interface lives there |
| **Adapter** | a concrete implementation that fits a seam (Postgres repo, in-memory fake) |

## Process

1. **List the callers and what they need.** Write 2–3 real call sites as code before designing anything, and name the most common caller.
   Exit: example calls exist, written as the caller wants to write them.

2. **Design it twice.** Sketch at least two very different interfaces. Good contrasts: a minimal one (1–3 entry points), one tuned for the most common caller, and a ports-and-adapters one if dependencies cross the seam. When subagents are available, give each design to a separate subagent with a different constraint and compare the results.
   Exit: two or more candidates, each with its signature, a usage example, what it hides, and its error modes.

3. **Compare on depth and cost of change.** For each candidate ask:
   - **Deletion test:** if this module were deleted, would complexity scatter across callers (it earns its keep) or vanish (it's a pass-through)?
   - **Hyrum's Law:** which incidental behaviors (ordering, timing, error text) could callers start to rely on? Hide them or document them.
   - **Seam count:** one adapter means a hypothetical seam, so don't add the abstraction yet. Two real adapters mean a real seam.
   - **Testability:** can a test exercise the behavior through this interface alone?
   Exit: one recommended design, with the reason it beats the others.

4. **Write the contract before the implementation.** Types, the error model, validation rules, and one example request and response for each operation. Get agreement from the user or consuming team when they exist.
   Exit: a contract file or type definitions that could be handed to someone else to implement.

5. **Plan for change.** Prefer additive evolution: new optional fields, new endpoints, new functions. Changing or removing anything is a breaking change: version it, or run a deprecation window with a migration path.
   Exit: the contract says how it will evolve without breaking current callers.

## Design rules

- **Accept dependencies instead of creating them.** Pass in the clock, the HTTP client and the repository, so tests and callers can swap them.
- **Return results instead of mutating arguments.** A function that returns a value is testable and composable.
- **Validate at the edges and trust inside.** Parse untrusted input (requests, env vars, third-party responses) into typed values once, at the boundary.
- **One error strategy per interface.** Pick exceptions, result types or error objects and use the same one everywhere. Callers must be able to tell "not found", "invalid" and "failed" apart without parsing strings.
- **Make the common case trivial.** Defaults cover the most common caller; options serve the rest.
- **Idempotent writes where retries happen.** Derive the idempotency key from the intent (an order id), not from the attempt, and claim it atomically with a unique constraint.

## Output

```
Callers: <who calls this, with the most common case named>
Options considered: <A: …, B: …, C: …, one line each with its main trade-off>
Recommendation: <choice + why, in terms of depth, testability, and cost of change>
Contract: <types / endpoints / error model, or a path to the contract file>
Evolution: <how it changes without breaking callers>
```

## Red flags

- The interface mirrors the implementation's internal steps (`init`, `load`, `process`, `finalize`)
- Boolean flag parameters (`send(msg, true, false)`)
- An abstraction with exactly one implementation "for flexibility"
- Callers must call methods in a specific order that the types don't enforce
- Errors come back as `null` in some places, thrown in others, and `{ error }` in a third
- You designed only one option

## References

- [http-api-conventions.md](references/http-api-conventions.md): open when the interface is an HTTP API (resources, status codes, pagination, versioning, idempotency)
