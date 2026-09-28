---
name: managing-technical-debt
description: Finding, recording, prioritizing and paying down technical debt so it is visible to product decisions. Use when code slows the team down, when asked what to refactor first or for a debt backlog, when justifying cleanup, or when deciding whether to take a shortcut.
license: Apache-2.0
metadata:
  version: "0.1.0"
  category: "lead"
  sources: "mattpocock/skills improve-codebase-architecture (MIT); garrytan/gstack retro, health (MIT); addyosmani/agent-skills deprecation-and-migration, code-simplification (MIT); wshobson/agents ai-debt-detector (MIT)"
---

# Managing Technical Debt

Debt matters only where you keep paying interest on it. Find the code that changes often and hurts every time, put a price on it, and pay it down alongside the feature work that touches it.

## When to use

- "What should we refactor first?", "build a tech-debt backlog", "why is everything slow to change here?"
- Estimates keep slipping in the same area, or the same kind of bug keeps recurring
- Justifying cleanup time to product or leadership
- Deciding whether to take a deliberate shortcut to hit a date, and how to record it
- Quarterly or pre-planning health review of a codebase

**Not for:** executing one specific refactor safely (use `refactoring-legacy-code`); tidying a recent diff (use `simplifying-code`); outdated packages (use `upgrading-dependencies`); a single architecture decision (use `documenting-decisions`).

## Process

1. **Find the hotspots from evidence.** Run `python3 scripts/hotspots.py --since "12 months ago" --exclude test` to rank files by change frequency × size. Cross-check the top results against:
   - bug-fix commits: `git log --since="12 months ago" --oneline -i -E --grep "fix|bug" -- <file>`;
   - incidents and slow reviews in that area;
   - a real complexity tool, if the stack has one.
   Ask the team where changes hurt: their answers usually match the churn list.
   Exit: 5–15 candidate areas, each backed by at least one number, such as churn, bug count, lead time or incidents.

2. **Describe each item as a ledger entry.** Record these fields:
   - **What:** the specific structural problem, in `file`/module terms.
   - **Interest:** what it costs now. Hours lost per change, recurring bug class, onboarding friction, incident risk, blocked features.
   - **Blast radius:** what else breaks or slows down because of it.
   - **Principal:** the cost to fix, as a rough size (S/M/L) and the approach.
   - **Trigger:** the upcoming work that will touch it.
   Record items in the repo's existing tracker or in `docs/tech-debt.md`, one entry per item.
   Exit: every candidate has all five fields. An item you cannot describe the interest for is not yet debt; it is taste.

3. **Classify it.** Place each item in the quadrant: deliberate or inadvertent, crossed with prudent or reckless.
   - *Deliberate-prudent* ("ship now, fix after launch") needs a repayment date.
   - *Reckless* items point to a process gap, such as missing review or no tests, that needs fixing as well as the code.
   - Also tag the kind: code, architecture, test, dependency, infrastructure, documentation, or knowledge (a single owner is a bus-factor risk).
   Exit: each entry has a quadrant and a kind.

4. **Prioritize by interest, not by ugliness.** Rank by interest × how soon the trigger arrives, divided by principal. High-interest, low-principal items come first. High-interest, high-principal items need a staged plan. Low-interest items stay in the ledger, however ugly they look. Stable, rarely changed code is not worth paying off.
   Exit: a ranked top 5, each with the reason it beats the next item.

5. **Pay it down alongside feature work.** Prefer these, in order:
   - fixing debt in the files a feature already touches;
   - "make the change easy, then make the easy change": a prefactoring task placed before the feature in the plan;
   - strangler-style replacement behind a seam for large items;
   - a time-boxed cleanup slot for items with no feature trigger.
   Every paydown gets tests first; see `refactoring-legacy-code` for the safe mechanics. Avoid big-bang rewrites.
   Exit: each top-5 item is attached to a specific upcoming task, or scheduled with an owner.

6. **Make the trade-off visible.** For each top item, write one line product can weigh: "Payments changes take ~2 extra days each and caused 3 incidents this year; a 1-week fix removes both." When a new shortcut is proposed, record it in the ledger *before* taking it, with its interest and a repayment trigger.
   Exit: stakeholders can see the cost of not fixing each top item in their own terms.

7. **Re-measure.** After a paydown, re-run the hotspot script and compare the numbers you recorded at step 1. Close ledger items with evidence, and prune items whose interest has dropped to zero.

## Output

```
| # | Item (where) | Kind | Quadrant | Interest (evidence) | Blast radius | Principal | Trigger | Plan |
|---|---|---|---|---|---|---|---|---|

Top 5 rationale: …
Stakeholder summary: <one line per item, in time, money or risk terms>
Recorded shortcuts: <new deliberate debt, with repayment trigger>
```

## Red flags

- A debt list built from code smells alone, with no churn, bug or lead-time evidence
- Prioritizing the ugliest code instead of the most-changed code
- Proposing a rewrite when a strangler or incremental path exists
- A "tech-debt sprint" with no measured before and after
- Shortcuts taken without a ledger entry and a repayment trigger
- Refactoring stable code that nobody needs to change

## References

- [scripts/hotspots.py](scripts/hotspots.py): run `python3 scripts/hotspots.py --help`; ranks files by commits × lines over a time window
