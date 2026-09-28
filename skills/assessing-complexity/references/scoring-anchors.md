# Scoring anchors and worked examples

## Contents

1. Tie-breakers per dimension
2. Worked examples
3. Common mis-scores

## 1. Tie-breakers per dimension

**Scope.** Count deployable units and ownership boundaries, not files. A 40-file rename inside one module scores 1. A 3-line change in two services that deploy separately scores 2.

**Uncertainty.** Ask two questions: "has *this team* shipped this pattern in *this codebase*?" and "do we know the user wants it?" Score the higher answer. When the requirements themselves are unknown, the score is 3, however familiar the technology.

**Reversibility.** Ask what undoing it would take at 3am.
- Revert and redeploy: 1.
- A reverse migration or backfill: 2.
- Impossible, because the data is gone, customers already built against the API, or messages or money already left: 3.

Schema changes that only add columns, tables or indexes score 1–2. Drops, renames and type changes on live data score 3 until an expand-contract plan brings them down.

**Blast radius.** Score the worst credible outcome, not the likely one. Anything touching authentication, authorization, billing or data deletion is 3.

**Coupling.**
- An external consumer you can't redeploy (mobile apps in the wild, partner integrations, public SDKs) scores 3.
- Another internal team's service scores 2.

**Data sensitivity.** Personal data includes emails, IPs, device IDs, and free text that users type. Regulated data covers payment cards, health records, government IDs, credentials and minors' data.

**Scale / performance.**
- Score 2 when the change sits on a request path with meaningful traffic, or multiplies volume (fan-out, N+1).
- Score 3 when an SLO depends on it, or load grows by 10× or more.

**Operability.** Anything that needs someone to watch it, page on it, rotate it or back it up scores 2 or more.

## 2. Worked examples

| Request | Scores (S U R B C D Sc O) | Tier | Set by |
|---|---|---|---|
| Fix a typo in the settings page | 0 0 0 0 0 0 0 0 | C0 | — |
| Add a "sort by date" option to an existing list endpoint | 1 0 1 1 1 0 1 0 | C1 | max 1 |
| Add CSV export of a user's own invoices | 1 1 1 1 0 2 1 1 | C2 | Data (PII in export) |
| Rename `users.name` to `full_name` in production | 1 0 3 2 2 2 0 0 | C3 | Reversibility (live rename) |
| Add Stripe subscriptions to the app | 2 2 3 3 3 3 1 2 | C4 | 4 dimensions at 3 |
| Move session storage from Postgres to Redis | 2 1 2 3 1 3 2 3 | C3 | Blast (auth), Data, Ops |
| "Can we render PDFs server-side under 500 ms?" | — | Spike | the deliverable is an answer |
| Build a new internal analytics product for 3 teams | 3 3 1 2 2 2 2 3 | C4 | new product |

Notice the Stripe case: it could be read as "just a feature", but it touches money, an external contract and regulated data. That combination is what makes it C4.

## 3. Common mis-scores

- **Scoring the ticket, not the code.** "Add a field" turns out to need a migration, a new API version, and three consumers.
- **Ignoring the rollback path.** If nobody can describe how to undo it, Reversibility is at least 2.
- **Treating internal tools as harmless.** An admin tool that can delete customer data has a blast radius of 3.
- **Forgetting the non-happy path.** Retries, partial failures and concurrent edits turn a C1 into a C2.
- **Counting familiarity as safety.** The team knows the pattern, so Uncertainty is 0, but Reversibility can still be 3.
