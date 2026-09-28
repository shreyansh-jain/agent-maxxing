---
name: measuring-product-outcomes
description: Defining success metrics, product analytics events and A/B experiments so a feature's impact can be proven. Use when adding analytics or tracking events, choosing a success metric or KPI, designing or reading an A/B test, or asked whether a shipped feature worked.
license: Apache-2.0
metadata:
  version: "0.1.0"
  category: "product"
  sources: "openai/skills define-goal (Apache-2.0); addyosmani/agent-skills observability-and-instrumentation, shipping-and-launch (MIT); muratcankoylan/Agent-Skills-for-Context-Engineering evaluation (MIT)"
---

# Measuring Product Outcomes

Decide what "it worked" means before you build, and put in the smallest set of events that can prove or disprove it.

## When to use

- A feature is being planned or shipped and nobody has said how success will be judged
- "Add tracking / analytics / events for X"
- Designing, sizing, or reading an A/B test or experiment
- "Did the new onboarding work?" or "Why did conversion drop?"

**Not for:** technical telemetry such as latency, errors and traces (use `instrumenting-observability`); rolling a change out gradually (use `managing-feature-flags`); deciding what to build (use `scoping-product-increments`); handling PII in event data (use `handling-personal-data`, and read step 3 here).

## Process

1. **Define the metric tree first.** Name one **primary metric**: the user behavior that moves if the feature works, such as "% of new workspaces that invite a teammate within 7 days". Add **guardrails**, the metrics that must not get worse (retention, support tickets, latency, revenue per user). Add **input metrics** that explain movement, such as funnel steps. For each metric, write the exact definition: numerator, denominator, time window, and which users count. Prefer rates and cohorts to raw counts, because counts grow with traffic whether or not the feature works.
   Exit: a written definition that two people would compute identically, plus its current baseline.

2. **Design the events, not a firehose.** Track only the events those metrics need. Name them `object_action` in the past tense (`invite_sent`, `report_exported`), using one convention across the product. Give each event a small, typed property set (ids, plan, surface, variant) and a `schema_version`. Write the taxonomy down in the repo, in a tracking plan or next to the code. Never rename an event in place: add the new one, run both, then retire the old.
   Exit: a tracking plan listing each event with its trigger, properties and types, and the metric it feeds.

3. **Keep personal data out.** Events carry stable pseudonymous ids, never emails, names, free text, tokens or full URLs with query strings. Check consent requirements for the product's regions. If a property might identify a person, ask whether the metric needs it at all.
   Exit: every property on the plan is justified, and none is raw PII.

4. **Instrument at the source of truth.** Fire business events where the fact becomes true, which is usually the server after the write commits, not on a button click that might fail. Use client events only for UI-only behavior (a viewed element, a hover, a client-side error). Make events idempotent, or de-duplicate them on an event id.
   Exit: each event is emitted exactly once for each real occurrence.

5. **Verify events before trusting dashboards.** Trigger each event in a dev or staging environment, then confirm in the analytics tool or its debug view that it arrived with the right properties. Write a test that asserts the event is emitted with the right payload. After launch, compare event counts against the source-of-truth table (e.g. `invite_sent` count vs rows in `invites`).
   Exit: observed payloads match the plan, and counts reconcile within a stated tolerance.

6. **Experiment only when the decision needs it.** Run an A/B test when the effect is uncertain and the traffic can detect it. Before starting, write down:
   - hypothesis ("showing X increases Y because Z");
   - primary metric and guardrails;
   - randomization unit (user, account, session; use the unit the metric is measured on);
   - minimum detectable effect, and the sample size and duration it implies (compute them; do not guess);
   - the decision rule.
   Then:
   - Do not peek-and-stop. Fix the duration, or use a sequential method designed for early looks.
   - Check sample ratio mismatch (e.g. a 50/50 split that arrives as 52/48 on a large sample) before reading results. A mismatch means the assignment or logging is broken.
   - Run for at least one full weekly cycle, and watch for novelty effects that fade.
   Exit: a pre-registered plan, and a readout against it.

7. **Read the result honestly.** Report the effect size with its confidence interval, not just "significant". Include the guardrails. Segment only for hypotheses stated in advance; unplanned slicing finds noise. "No detectable effect" is a valid and useful result.

## Output

```
Primary metric: <definition> · baseline <x> · target <y>
Guardrails: <metric: must not worsen beyond z>
Events: <object_action (props…) → metric>   Owner: <team>
Verification: <how each event was observed> · reconciles with <table> within <n%>
Experiment (if any): H: … · unit: … · MDE: … · n per arm: … · duration: … · decision rule: …
Readout: effect <Δ> (95% CI <a, b>) · guardrails <ok | breached> · SRM <ok | failed> · decision: ship | iterate | revert
```

## Rationalizations

| Excuse | Reality |
|---|---|
| "Track everything, we'll figure it out later" | Firehose data is unowned, unnamed and unverified. Nobody trusts it later. |
| "The button click is close enough" | Clicks count attempts, not successes. Instrument where the fact becomes true. |
| "It's significant after 2 days, ship it" | Early peeking inflates false positives, and weekly cycles are not yet covered. |
| "Let's slice by country to find where it worked" | Unplanned segmentation finds noise. Pre-register it, or label it exploratory. |
| "Email in the event makes debugging easier" | It makes the analytics store a PII store. Use pseudonymous ids. |

## Red flags

- A feature ships with no success metric written down
- Event names mixing conventions (`ClickedInvite`, `invite-sent`, `inviteSent`)
- Metrics defined as raw counts with no denominator
- Stopping a test the moment the p-value dips below 0.05
- A 50/50 test showing an uneven split, read anyway
- Free-text or email properties in analytics events

## References

- [experiment-math.md](references/experiment-math.md): open when sizing a test, checking sample ratio mismatch, or reading intervals
