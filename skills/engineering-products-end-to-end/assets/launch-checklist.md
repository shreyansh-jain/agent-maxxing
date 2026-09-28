# <Product / increment>: launch readiness

Each line is ✅ done (with a link to the evidence), ❌ not done, or ⚠️ accepted risk (named approver). Go-live needs no ❌.

## Product
- [ ] Success metric and guardrails instrumented; events verified firing in a non-prod environment
- [ ] Date to review the metric is on the calendar
- [ ] Support, docs and changelog ready for users

## Reliability
- [ ] SLOs defined; dashboards show the user journey end to end
- [ ] Alerts route to an owner, and every alert has a runbook
- [ ] Load test at the estimated peak × headroom; results linked
- [ ] Timeouts, retries and degradation behavior verified for each dependency

## Safety
- [ ] Feature flag in place with a kill switch; default is off
- [ ] Rollback procedure written and rehearsed; time-to-rollback measured
- [ ] Data migrations rehearsed on a production-like copy; backfill resumable
- [ ] Backups and restore tested for any new datastore

## Security and privacy
- [ ] Threat model mitigations implemented or accepted
- [ ] Security review of the changed surface complete
- [ ] Personal data inventoried; retention and deletion paths work; no PII in logs

## Cost
- [ ] Cost estimate at launch load and at 10× load
- [ ] Budget alert configured

## Rollout plan
| Stage | Audience | Bake time | Health signal | Abort threshold |
|---|---|---|---|---|
| 1 | internal | | | |
| 2 | beta cohort | | | |
| 3 | 10% | | | |
| 4 | 100% | | | |

**Decision:** go / no-go, <date>, <approver>
