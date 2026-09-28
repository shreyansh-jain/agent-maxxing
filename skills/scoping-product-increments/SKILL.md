---
name: scoping-product-increments
description: Scoping a product problem down to the smallest valuable increment worth building next. Use when an idea, roadmap item or feature request is too big or vague to start, when deciding an MVP, cutting scope to a deadline, or choosing what to build first.
license: Apache-2.0
metadata:
  version: "0.1.0"
  category: "product"
  sources: "garrytan/gstack office-hours, plan-ceo-review (MIT); addyosmani/agent-skills idea-refine, incremental-implementation (MIT); openai/skills define-goal (Apache-2.0)"
---

# Scoping Product Increments

Build the smallest thing that tests the riskiest assumption for a real user within a fixed appetite. Everything else is a later increment or a non-goal.

## When to use

- "We want to build X". X is a platform, a vision, or a roadmap line, not a shippable slice.
- A deadline is fixed and the scope is not.
- Choosing an MVP, a pilot, a beta, or "what do we build first?"
- A feature request arrives with a solution attached but no stated problem.

**Not for:** surfacing what the user actually wants in a conversation (use `clarifying-intent`); writing the full spec for an increment already chosen (use `writing-specs`); estimating how hard it is (use `assessing-complexity`); defining the success metric and instrumentation (use `measuring-product-outcomes`).

## Process

1. **Name the user, the problem, and the evidence.** Write down one specific kind of user (a role in a situation, not "everyone"), the job they are trying to get done, and what they do today instead. The status quo is the real competitor: a spreadsheet, a Slack thread, a manual step. Then list the evidence of demand. Behavior counts: they pay, they complain when it breaks, they built a workaround. Interest does not count: signups, "sounds useful".
   Exit: one sentence of the form "*<user>* struggles to *<job>* because *<cause>*; today they *<workaround>*; evidence: *<behavior>*". If the evidence line is empty, the first increment is a validation experiment, not a feature.

2. **Set the appetite before the scope.** Decide how much time the problem is worth, for example "two weeks, one engineer". This is a budget, not an estimate. Scope then flexes to fit the appetite, instead of the timeline flexing to fit the scope.
   Exit: an appetite in engineer-weeks, agreed with the user.

3. **List the risks and order them.** For this bet, mark each of the four risks high or low:
   - **Value**: will they use it or pay for it?
   - **Usability**: can they figure it out?
   - **Feasibility**: can we build it within the appetite, with our stack and data?
   - **Viability**: does it work for the business (legal, cost, support, sales)?
   The first increment must retire the highest risk. A feasibility risk calls for a spike or a walking skeleton. A value risk calls for something a real user touches, even if it is manual behind the scenes.
   Exit: the single riskiest assumption, stated so that it can be falsified.

4. **Find the narrowest wedge.** Pick the smallest version one real user would miss if it were taken away this week. Cut along user-visible behavior, not technical layers. A thin end-to-end path (a walking skeleton) beats a complete backend with no UI. Use this ladder, cheapest first: a manual process or concierge → a script or an existing tool → a configuration or flag of what exists → new code.
   Exit: an increment description that a user could try, which fits the appetite with slack.

5. **Draw the cut line.** Write three lists:
   - **In**: the must-haves for the wedge to work.
   - **Nice-to-have**: included only if time remains, and cut first.
   - **Non-goals**: explicitly out, each with a reason.
   Non-goals prevent scope creep better than any plan. Mark rabbit holes (areas likely to eat the appetite) and decide on them now.
   Exit: every requested item sits on exactly one list, and the user has agreed the non-goals.

6. **Sequence the follow-ups lightly.** When there are several candidate next increments, rank them with one simple lens and show your numbers. Use RICE (reach × impact × confidence ÷ effort) or cost of delay ÷ duration. The ranking is only as good as its guesses, so state the confidence and let the user override it.
   Exit: an ordered list of the next 2–4 increments, each with the risk it retires.

## Output

```
Problem: <user> struggles to <job> because <cause>. Today: <workaround>. Evidence: <behavior | none: validate first>
Appetite: <n engineer-weeks>
Riskiest assumption: <falsifiable statement> (risk type: value | usability | feasibility | viability)
Increment 1: <what a user can do that they could not before>
  In: …   Nice-to-have: …   Non-goals: … (why)   Rabbit holes: … (decision)
Done means: <observable user behavior or metric>, measured by <how>
Next: 2. <increment>: retires <risk>  3. …
```

Hand the chosen increment to `writing-specs`, and its success signal to `measuring-product-outcomes`.

## Rationalizations

| Excuse | Reality |
|---|---|
| "Users need the full platform before it's useful" | Then the value is not yet understood. Find the one job someone would use a slice for. |
| "We'll figure out the metric after launch" | Then nobody can say whether it worked. Define "done means" now. |
| "It's only a bit more to add X too" | Every addition taxes the appetite and delays learning. Put X on the next increment. |
| "Everyone we asked loved it" | Liking is free. Look for behavior: payment, workarounds, complaints. |
| "Doing it manually first is a waste" | A manual version tests value in days. Code tests it in weeks. |

## Red flags

- The user is "everyone" or "developers"
- No non-goals list
- The increment is a technical layer ("build the API first") with no user-visible outcome
- The timeline grows to fit the scope
- The first increment retires a low risk while the biggest risk waits until the end

## References

- [increment-brief.md](assets/increment-brief.md): copy when writing the increment down for the team
