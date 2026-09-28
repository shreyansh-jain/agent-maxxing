---
name: clarifying-intent
description: Intent-discovery interview before building anything new or changing behavior. Use when a request names a thing to build but not who it is for, why, or what done means, when the user asks to be grilled or to stress-test an idea, or before any feature, component, or behavior change whose purpose and success criteria are not yet agreed.
license: Apache-2.0
metadata:
  version: "0.1.0"
  category: "define"
  sources: "obra/superpowers brainstorming (MIT); mattpocock/skills grilling (MIT); addyosmani/agent-skills interview-me (MIT); addyosmani/agent-skills idea-refine (MIT); garrytan/gstack office-hours (MIT)"
---

# Clarifying Intent

Before you design or build anything, agree with the user on the outcome, who it is for, and how you will know it worked. Building the wrong thing well is still a failure.

## When to use

- The ask names a thing ("add a dashboard") but not the purpose, the user, or what success looks like
- The user says "grill me", "poke holes in this", "are we sure?", or "stress-test my plan"
- A new feature, component, or behavior change is about to start and nobody has written down what done means
- You catch yourself guessing at a requirement in order to keep moving

**Not for:** turning an already-agreed intent into a written spec (use `writing-specs`); breaking a spec into tasks (use `planning-implementation`); critiquing a finished plan (use `reviewing-plans`); explaining existing code.

## The rule

```
NO IMPLEMENTATION BEFORE THE USER CONFIRMS THE RESTATED INTENT
```

Violating the letter of the rule is violating the spirit of the rule. Read-only exploration (reading code, docs, git history) is allowed while the gate is closed. Scaffolding, installing dependencies, and writing product code are not.

## Process

1. **Classify out loud.** Before your first question, say which path this is, so the user can override you:
   - **Spike**: "can we…?" or "is it possible…?". The output is an answer, not code you keep. Agree the question and the probe in 2–3 sentences, then investigate.
   - **Bounded**: a scoped change to a flow that already exists in this repo. Ask the questions that matter, give a short design in chat, and stop for a yes.
   - **Architectural**: a new project, a new subsystem, or a change to interfaces other code depends on. Run the full interview, then hand off to `writing-specs`.

   When unsure, take the heavier path. The ratchet only turns one way: if hidden complexity shows up mid-task, stop, say so, and step up. Nothing steps down.
   Exit: the path is stated and the user has had a chance to override it.

2. **Look up facts; ask only for decisions.** Read the code, docs, and history before you ask anything. Never ask the user something the repo can answer. If a fact needs digging, send a subagent (see `dispatching-subagents`) and hold back only the questions that depend on its answer.
   Exit: every open question is a decision only the user can make.

3. **Lead with a hypothesis.** State your best guess of the intent in one sentence, with a confidence number: "I think you want X so that Y — about 60% sure; unclear: who uses it." If you can't write that sentence, you aren't ready to design.
   Exit: a hypothesis with a confidence number and the reason it isn't higher.

4. **Interview in rounds over the decision tree.** Every decision branches into the decisions that hang off it. The *frontier* is the set of open decisions whose prerequisites are already settled. Each round, ask at most three frontier questions. Number them and attach your recommended answer to each, because people react faster than they generate. Any question that depends on another open question waits for a later round. After each round, recompute the frontier.
   Probe these whenever they are unsettled:
   - **Outcome**: what changes for whom when this works?
   - **Evidence of demand**: who has this problem today, and what are they doing about it now?
   - **Narrowest wedge**: what is the smallest version that would still be worth shipping?
   - **Success**: a measurable condition, not an adjective. Translate "fast" into "p95 < 300 ms".
   - **Out of scope**: what should this deliberately *not* do?

   If an answer only signals sophistication ("scalable", "clean", "modern"), probe what they actually need. If the answer is "whatever you think", that hands the decision back to you. Re-ask it as a choice between two concrete options.
   Exit: the frontier is empty, and you could predict the user's answers to your next three questions.

5. **Restate and get an explicit yes.** Write the restatement using the Output template below, then stop the turn. "Sounds good", silence, or "whatever you think" does not count as yes. Restate more concretely and ask again.
   Exit: the user has explicitly confirmed the restatement, or corrected it and then confirmed the corrected version.

6. **Hand off by path.** For a spike, investigate and report a recommendation, labelling any code as throwaway. For a bounded change, present the short design and wait for a yes before implementing. For an architectural change, go to `writing-specs`, carrying the confirmed restatement over word for word.

## Output

```
Path: Spike | Bounded | Architectural (why)
Outcome: <what changes, for whom>
User: <who, in their situation>
Why now: <the trigger>
Success: <measurable conditions>
Constraints: <hard limits: stack, deadline, compliance, budget>
Out of scope: <deliberate non-goals>
Assumptions: <what you inferred rather than heard, each one correctable>
→ Is this right? A yes lets me proceed to <next step>.
```

## Rationalizations

| Excuse | Reality |
|---|---|
| "The ask is clear enough" | If you can't write the outcome and the success condition in one line each, it isn't. |
| "It's too simple to need this" | A bounded change needs two sentences and a yes. That is cheap. Skipping the yes is not. |
| "Questions waste their time" | Four good questions take minutes. Building the wrong thing takes days, and the user pays for it. |
| "I'll figure it out while building" | Changing direction after code exists costs far more, and sunk cost bends the design. |
| "They said 'whatever you think'" | That hands the decision back to you. Offer two concrete options and let them pick. |
| "I understand this kind of app, so it's bounded" | "Bounded" is about what already exists in this repo, not about what you know. |

## Red flags

- Asking the user something `grep` or the docs could answer
- A question with no recommended answer attached
- Starting to scaffold while the user is still reading your design
- Treating approval of an idea as approval of an artifact that doesn't exist yet
- Three rounds in and your confidence number hasn't moved: you're asking the wrong questions
- The restatement has no "Out of scope" line
