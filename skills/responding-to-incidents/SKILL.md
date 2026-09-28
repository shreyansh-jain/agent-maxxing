---
name: responding-to-incidents
description: Production incident response, mitigation-first, through to a blameless postmortem. Use when production is down, degraded, erroring or losing data right now, an alert or page has fired, a deploy just broke users, or when writing the postmortem or on-call handoff afterwards.
license: Apache-2.0
metadata:
  version: "0.1.0"
  category: "operate"
  sources: "wshobson/agents incident-runbook-templates, postmortem-writing, on-call-handoff-patterns (MIT); garrytan/gstack canary, careful (MIT); addyosmani/agent-skills shipping-and-launch (MIT)"
---

# Responding to Incidents

During an incident the goal is to stop user harm, not to understand it. Mitigate with the smallest reversible action, then diagnose calmly once the bleeding stops.

## When to use

- Users are hitting errors, timeouts, wrong data or an outage right now
- An alert or page fired, or a deploy correlates with a spike
- Data loss or corruption is suspected
- After the incident: timeline, postmortem, follow-ups, on-call handoff

**Not for:** a bug with no active user harm (use `debugging-systematically`); a red CI build (use `fixing-ci-failures`); adding alerts and dashboards for the future (use `instrumenting-observability`).

## The rule

```
MITIGATE BEFORE YOU DIAGNOSE, AND NEVER TOUCH PRODUCTION WITHOUT EXPLICIT APPROVAL
```

Violating the letter of the rule is violating the spirit of the rule. You propose commands; the human with authority runs them or approves each one.

## Process

1. **Establish facts in five minutes.** Find out what users are experiencing, when it started, and what changed just before that: deploys, config or flag flips, migrations, traffic spikes, dependency status pages. Open a timeline and timestamp every observation and action in UTC from this point on.
   Exit: one sentence describing the impact and a start time, even if both are rough.

2. **Set severity and roles.** Use SEV1 for a full outage or data loss, SEV2 for a major feature down or a large share of users affected, SEV3 for a degradation with a workaround. Name an incident commander who decides, a communicator who posts updates, and an operator who runs commands. Even when one person holds all three, keep them separate in the notes.
   Exit: the severity has been announced and the first status update has been posted, or drafted for the human to post.

3. **Mitigate with the smallest reversible action.** Try these in order: roll back the last deploy; turn off the feature flag; revert the config; shed or rate-limit the offending traffic; fail over; scale up. Prefer an action that can be undone in one step. For each proposed action, state the exact command, the target (cluster, region, database), the expected effect, and how to undo it. Then **wait for explicit approval** before it runs.
   Exit: the user-facing symptom metric is back within SLO, or the next mitigation has been chosen.

4. **Protect the evidence.** Before restarting or rolling back, and only if it costs seconds, capture what will disappear: a log excerpt, a thread or heap dump, the slow-query list, the pod `describe` output. Never delete data, truncate tables, or `kubectl delete` resources to "clean up" during an incident.

5. **Communicate on a clock.** Post updates every 30 minutes for SEV1 and every 60 minutes for SEV2, even when there is no news. Each update covers current impact, what is being tried, and when the next update will come. Say "we don't know yet" rather than speculate.

6. **Confirm recovery.** Watch the symptom metric for a full bake period, e.g. 30 minutes at normal traffic. Check for secondary damage: queues that need draining, jobs that need re-running, data that needs repairing. Only declare the incident resolved once the metric has stayed healthy.
   Exit: the metric is healthy for the whole bake period and the backlog has been handled or ticketed.

7. **Diagnose and write the postmortem.** Once the incident is mitigated, switch to `debugging-systematically` for root cause. Write the postmortem from [postmortem.md](assets/postmortem.md) within 48 hours. Keep it blameless: describe systems and decisions, not people. Every action item gets an owner and a due date, and at least one must reduce *detection* or *mitigation* time, not only fix the trigger.

8. **Hand off.** If the incident outlasts a shift, write a handoff covering current state, what has been tried, what is still running, the next decision point, and open risks. The next responder must be able to act without reading the whole chat.

## Rationalizations

| Excuse | Reality |
|---|---|
| "I almost have the root cause, let me finish first" | Users are still failing while you think. Roll back first; the cause will still be there. |
| "Rollback is risky, a forward fix is faster" | A forward fix is untested code shipped under pressure. Roll back unless rollback is impossible, and write down why. |
| "It's an emergency, I'll just run it" | Emergencies are when a wrong command does the most damage. State the command and target, then get approval. |
| "No update until we know more" | Silence reads as chaos. Post on the clock. |
| "The fix is in, we're done" | You are done when the metric has held through the bake period and the backlog is clean. |

## Red flags

- Reading code while the error rate is still climbing and no mitigation has been tried
- Running commands against production that nobody approved
- More than one person changing production at the same time without the commander knowing
- `DROP`, `DELETE`, `TRUNCATE`, `kubectl delete`, `rm -rf` or `--force` proposed as a mitigation
- "Resolved" declared minutes after a change, with no bake period
- A postmortem whose root cause is "human error"

## References

- [postmortem.md](assets/postmortem.md): copy and fill in when writing the postmortem
