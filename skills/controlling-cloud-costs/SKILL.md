---
name: controlling-cloud-costs
description: Measure-first cloud cost reduction and cost-aware design. Use when a cloud bill jumps or is too high, when asked to cut spend, find waste or idle resources, set budgets and anomaly alerts, compute unit cost per request or tenant, or weigh the cost of a design.
license: Apache-2.0
metadata:
  version: "0.1.0"
  category: "operate"
  sources: "wshobson/agents cost-optimization (MIT); addyosmani/agent-skills performance-optimization (MIT)"
---

# Controlling Cloud Costs

Cut spend where the money actually goes, prove the saving afterwards, and never trade reliability or data for it without the owner saying yes.

## When to use

- "Our bill doubled", "why is AWS/GCP/Azure so expensive", "cut our cloud spend by X%"
- Finding idle, orphaned or oversized resources
- Setting up cost allocation tags, budgets or anomaly alerts
- Calculating cost per request, tenant, job or customer
- Comparing the running cost of design options before building

**Not for:** making code faster when latency is the goal (use `optimizing-performance`); sizing for future load (use `estimating-capacity`); writing the IaC change itself (use `writing-infrastructure-as-code`); log and metric design (use `instrumenting-observability`, then come back here for retention and cardinality costs).

## The rule

```
NO CUT WITHOUT A MEASURED BASELINE, AND NO DELETION WITHOUT THE OWNER'S EXPLICIT APPROVAL
```

Violating the letter of the rule is violating the spirit of the rule. An "idle" resource is only idle until someone's disaster-recovery plan needs it.

## Process

1. **Get the bill broken down.** Pull spend by service, account or project, region and tag for the last 30–90 days (AWS Cost Explorer / CUR, GCP billing export to BigQuery, Azure Cost Management). Use read-only credentials. If most spend is untagged, fixing allocation is the first deliverable.
   Exit: a table of the top 10 cost lines with their trend, and the share of spend you cannot attribute.

2. **Explain changes before cutting.** For a jump, find the day it started and match it against deploys, traffic, new resources and config changes. A spike is often a bug (a retry loop, a runaway log level, a cross-region data path), not a pricing problem.
   Exit: each large delta has a cause, or is marked unexplained.

3. **Compute unit cost.** Divide cost by the business driver (requests, active tenants, GB processed, jobs run). Unit cost separates growth, which is fine, from inefficiency, which is fixable.
   Exit: cost per unit for the top services, before any changes.

4. **Pick levers by size × safety.** Start at the top of the list. Typical levers, roughly safest first:
   - **Waste:** unattached volumes, old snapshots, idle load balancers, unused IPs, forgotten dev environments, stopped-but-billed instances.
   - **Retention and cardinality:** log levels, log and metric retention, high-cardinality labels, trace sampling.
   - **Storage tiering:** lifecycle rules to infrequent-access or archive tiers, deleting incomplete multipart uploads.
   - **Rightsizing:** size to measured p95 utilization over at least two weeks, not averages; keep headroom.
   - **Scaling:** autoscaling, scheduling non-prod environments to zero off-hours, spot or preemptible capacity for interruptible work.
   - **Data transfer:** cross-AZ and cross-region chatter, NAT gateway traffic, missing CDN or VPC endpoints.
   - **Commitments:** savings plans, reserved or committed-use discounts, only for a stable baseline and only after the steps above.
   Exit: a ranked list with estimated monthly savings, risk, and owner for each lever.

5. **Change with approval, one lever at a time.** Present the list. For each deletion, downsize or commitment purchase, wait for explicit approval from the owner. Snapshot or back up before deleting anything stateful. Make changes through IaC where it exists, so they don't drift back.
   Exit: approved changes applied, each with a rollback note.

6. **Verify the saving and guard it.** After a full billing cycle (or daily granularity after a few days), compare against the baseline and the unit cost. Keep what saved money without hurting SLOs, and revert what hurt them. Add budgets with alerts at thresholds such as 80% and 100%, turn on anomaly detection, and require cost tags in policy so new resources stay attributable.
   Exit: measured savings per lever, budgets and anomaly alerts in place.

**Cost as a design constraint.** When comparing designs, estimate the monthly cost at the expected load and at 10× that load, from the pricing pages (fetch current prices rather than recalling them). Name the dominant cost driver of each option (requests, storage, egress, always-on compute).

## Output

```
Spend: $<total>/mo (<period>), <x>% untagged
Top lines: <service/tag>: $<n> (<trend>)
Unit cost: $<n> per <driver>
Levers (ranked): <lever>: est. $<saving>/mo, risk <low/med/high>, owner <team>, status <proposed/approved/applied>
Verified: <lever>: $<before> → $<after>; SLO impact <none/…>
Guards: budgets <thresholds>, anomaly alerts <on/off>, tag policy <on/off>
```

## Rationalizations

| Excuse | Reality |
|---|---|
| "That volume is obviously unused, delete it" | Obvious to you. Ask the owner and snapshot first. Deletions don't come back. |
| "Buy a 3-year savings plan, instant 40%" | Commitments lock in today's waste. Remove waste and rightsize first. |
| "Downsize everything to the average CPU" | Averages hide peaks. Size to p95 with headroom, or you've traded cost for an outage. |
| "Savings are obvious, no need to check the next bill" | Changes drift back and costs move elsewhere. Measure it. |

## Red flags

- Cutting before you know the top 10 cost lines
- Deleting resources, snapshots or buckets without the owner's written approval
- Rightsizing from a few days of data, or from averages
- Commitment purchases before waste removal
- Savings claimed from estimates, never checked on the bill
- A spike "fixed" by throttling, without finding the bug that caused it
