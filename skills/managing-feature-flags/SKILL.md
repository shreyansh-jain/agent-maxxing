---
name: managing-feature-flags
description: Feature flag lifecycle from creation through rollout to removal, including safe defaults, targeting and flag-debt cleanup. Use when adding a feature flag or kill switch, gating a release, doing a percentage rollout, or removing stale flags and dead code paths.
license: Apache-2.0
metadata:
  version: "0.1.0"
  category: "ship"
  sources: "addyosmani/agent-skills shipping-and-launch, incremental-implementation (MIT); garrytan/gstack canary (MIT)"
---

# Managing Feature Flags

Every flag is temporary debt with an owner, a safe default and a removal date, all fixed at the moment the flag is created.

## When to use

- Adding a flag to ship incomplete work, gate a release, run an experiment, or add a kill switch
- Rolling a change out by percentage, cohort or tenant
- Removing a flag after full rollout, or cleaning up many stale flags
- A flag misbehaved: wrong users saw a feature, or the flag service went down

**Not for:** the overall shipping flow and deploy stages (use `shipping-changes`); designing the experiment and its metrics (use `measuring-product-outcomes`); an active outage caused by a change (use `responding-to-incidents`, where turning the flag off is usually the first mitigation).

## Process

1. **Pick the flag type.** Each type has a different lifetime:
   | Type | Purpose | Lifetime |
   |---|---|---|
   | Release | hide unfinished or unrolled-out work | days to weeks; removed after 100% |
   | Experiment | A/B assignment | the length of the test; removed after the decision |
   | Ops / kill switch | turn off a costly or risky path under load or failure | long-lived, reviewed quarterly |
   | Permission / entitlement | plan- or customer-specific access | long-lived; really configuration, so consider modeling it as data |
   Exit: the type is chosen, and a permission flag has been checked against being product configuration instead.

2. **Create it with its exit.** Name it `<area>_<behavior>` in the repo's convention (e.g. `billing_new_invoice_pdf`). Record the owner, the type, a one-line purpose, and, for release and experiment flags, an **expiry date** and a **removal ticket** filed now. Use the flag provider's metadata fields if it has them; otherwise use a registry file in the repo.
   Check the provider's SDK and API specifics in its current docs (`grounding-in-official-docs`) rather than from memory.
   Exit: the flag exists with an owner, a type, an expiry and a linked removal ticket.

3. **Make the default safe.** Evaluate the flag in one place per request and pass the result down, rather than calling the flag service deep in many functions. Define what happens when the flag service is slow or unreachable: fall back to a hard-coded default, which for release flags is **off** (the old behavior). Set a short timeout, and cache the last-known values. Do not nest flags inside other flags; if two flags interact, test all four combinations or merge them.
   Exit: with the flag service unavailable, the product behaves exactly as before the change.

4. **Test both paths.** Write tests for flag-on and flag-off behavior, at the same seam. Make the flag easy to override in tests, through an injected client or a test helper, never by mutating global state. If the flag gates a data or schema change, the old path must still work with data written by the new path (see `migrating-databases-safely`).
   Exit: CI runs both states for the gated behavior.

5. **Roll out in steps with a watch signal.** Before starting, name the signal (error rate, latency, a business metric), the abort threshold, and who watches it. A typical sequence:
   - internal users;
   - 1%;
   - 10%;
   - 50%;
   - 100%.
   Hold each step for a fixed bake time. Target on a stable key, such as a user or account id hashed consistently, so users don't flicker between variants. Changing a production flag is a production change: do it only with the user's approval and record who changed what, when, and why. Use the provider's audit log, or a note in the ticket.
   Exit: each step held within threshold, or the flag went back to off and the reason was logged.

6. **Remove it.** Once a release flag has sat at 100% for its bake period and is past its decision point:
   1. Delete the losing branch of code and the flag checks.
   2. Remove the tests for the dead path.
   3. Delete configuration and targeting rules.
   4. Archive the flag in the provider, after the code is deployed everywhere, so old deployments never evaluate a missing flag.
   5. Close the removal ticket.
   For a bulk cleanup, list flags past expiry or at 100% or 0% for longer than N days, confirm each with its owner, and remove one flag per change so any revert stays small.
   Exit: `grep` for the flag key returns nothing in code, and the flag is archived.

## Output

```
Flag: <key> · type: release | experiment | ops | permission · owner: <name>
Purpose: <one line> · expires: <date> · removal ticket: <link>
Default / fallback: <off → old behavior> · timeout: <ms> · evaluated at: <one place>
Tests: on ✓ off ✓ (<test paths>)
Rollout: internal → 1% → 10% → 50% → 100% · bake: <time> · signal: <metric> abort at <threshold>
Change log: <who, when, what, why>
Removal: code paths deleted ✓ tests ✓ config ✓ archived ✓
```

## Rationalizations

| Excuse | Reality |
|---|---|
| "We'll clean it up later" | Later never has a date. File the removal ticket when you create the flag. |
| "Default doesn't matter, the service is always up" | Flag services go down. The default is your production behavior during that outage. |
| "Only the on path matters now" | Until you need to turn it off in an incident and the off path is broken. |
| "It's a quick toggle, no need to ask" | A flag flip changes production for real users. It needs the same approval as a deploy. |
| "Let's reuse the old flag for this new thing" | Reused flags mean mismatched targeting and old code paths quietly switching back on. Make a new one. |

## Red flags

- A flag with no owner or expiry
- The flag service called inside loops or deep helpers
- Nested flags with untested combinations
- A flag at 100% for months while both code paths remain
- The flag archived in the provider before the code referencing it has been deployed
- Flag values changed in production without a record
