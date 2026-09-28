# Postmortem: <short title>

**Severity:** SEV<n>  **Status:** draft | reviewed  **Date:** <YYYY-MM-DD>
**Authors:** <names>  **Incident commander:** <name>

This review is blameless. It describes how systems, signals and decisions behaved, not who made a mistake.

## Summary

Two or three sentences for someone who reads nothing else: what users experienced, for how long, and what stopped it.

## Impact

| Measure | Value |
|---|---|
| Duration (start → mitigated → resolved) | <UTC> → <UTC> → <UTC> |
| Users / requests affected | <number or %> |
| Error budget consumed | <% of window> |
| Data lost or corrupted | <none / description and repair status> |
| Revenue or contractual impact | <if known> |

## Timeline (UTC)

| Time | Event |
|---|---|
| hh:mm | Triggering change or event |
| hh:mm | First alert, or first user report (record which one came first) |
| hh:mm | Responder engaged |
| hh:mm | Mitigation applied |
| hh:mm | Metric back within SLO |
| hh:mm | Resolved |

**Time to detect:** <min>  **Time to mitigate:** <min>  **Time to resolve:** <min>

## Root cause and contributing factors

The technical cause, traced to where the failure first started (see the debugging-systematically skill). Then the contributing factors: the conditions that let the cause reach users, or that slowed detection or mitigation.

## What went well

- 

## What went poorly

- 

## Where we got lucky

- 

## Action items

Each item has an owner and a due date. At least one must shorten detection or mitigation, not only prevent this exact trigger.

| Action | Type (prevent / detect / mitigate) | Owner | Due | Ticket |
|---|---|---|---|---|
|  |  |  |  |  |
