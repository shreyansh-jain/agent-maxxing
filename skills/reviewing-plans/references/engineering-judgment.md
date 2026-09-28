# Engineering judgment lenses

Use these as lenses on every finding. None of them is a separate checklist pass.

| Lens | Question to ask | Origin |
|---|---|---|
| Blast radius | If this goes wrong, what breaks, and who notices? | SRE practice |
| Reversibility | Can a flag, a revert, or a rollback undo it in minutes? One-way doors deserve more scrutiny. | Bezos "one-way vs two-way doors" |
| Boring by default | Is each new technology worth one of the team's few "innovation tokens"? | McKinley, "Choose Boring Technology" |
| Incremental over big bang | Could this be a strangler migration, a canary, or a series of flagged steps? | Fowler, strangler fig |
| Make the change easy first | Should a refactor land first, separately from the behavior change? | Beck |
| Essential vs accidental complexity | Is this complexity in the problem, or did we create it? | Brooks, "No Silver Bullet" |
| Systems over heroes | Would a tired on-call engineer at 3 a.m. operate this correctly? | Operations practice |
| Conway's law | Do the module boundaries match the teams that will own them? | Conway; Skelton and Pais |
| Error budgets | What reliability target applies, and does the plan spend the budget sensibly? | Google SRE |
| Prove the callers | Is the shared abstraction backed by at least two real call sites? | gstack plan-eng-review |
| Failure is information | Will we know it failed: logs, metrics, alerts? | Allspaw; observability practice |

## Common plan defects, most frequent first

1. References to functions, tables, or endpoints that don't exist, or that have different signatures.
2. Rebuilding something the codebase or a dependency already provides.
3. Only the happy path: no behavior for errors, empty states, retries, or partial failure.
4. Horizontal tasks that aren't demoable until the last one lands.
5. A migration with no rollback, or one that can't run while the old code is still deployed.
6. Tests planned only at the unit level for behavior that is really about integration.
7. Unbounded work: a list with no pagination, a job with no batch size, a retry with no cap.
