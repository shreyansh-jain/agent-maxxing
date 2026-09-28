# <Feature> Implementation Plan

**Goal:** <one sentence: what this builds>
**Architecture:** <2–3 sentences on the approach>
**Spec:** <path or link. Implementers read the spec alongside this plan.>
**Execution:** implementing-incrementally (inline) or dispatching-subagents (one agent per independent task)

## Global Constraints

- <project-wide requirement with its exact value, copied from the spec, e.g. "Node >= 20", "no new runtime dependencies">

## File Map

| File | Responsibility |
|---|---|
| `src/…` | <one line> |

## Review Focus

1. <input or failure mode the spec implies but no test covers yet>. The test for it is added in Task <N>.

---

### Task 1: <demoable result, in words the user would recognise>

**Blocked by:** none
**Files:** create `…` · modify `…:120-145` · test `tests/…`
**Interfaces:**
- Consumes: <exact signatures from earlier tasks>
- Produces: `functionName(arg: Type): ReturnType`. Later tasks rely on this.

- [ ] **Write the failing test** `test_<behavior>`: asserts <exact value from the spec>
- [ ] **Run it:** `<single-test command>`. Expected: FAIL, <reason>
- [ ] **Implement** `functionName` in `…`. <Add a line on the approach only if the signature and test leave a real choice.>
- [ ] **Run it:** `<same command>`. Expected: PASS
- [ ] **Checkpoint:** run `<typecheck command>`, then commit if the user has asked for commits

**Acceptance:** <observable behavior>

### Task 2: …
