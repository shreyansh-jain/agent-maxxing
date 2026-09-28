---
name: dispatching-subagents
description: Delegation discipline for handing work to subagents, parallel agents, or background workers. Use when two or more independent tasks could run at once, a plan has tasks to farm out, a broad search would flood the main context, or a fresh-context reviewer is wanted for finished work.
license: Apache-2.0
metadata:
  version: "0.1.0"
  category: "agents"
  sources: "obra/superpowers dispatching-parallel-agents (MIT); obra/superpowers subagent-driven-development (MIT); addyosmani/agent-skills doubt-driven-development (MIT); addyosmani/agent-skills context-engineering (MIT)"
---

# Dispatching Subagents

A subagent knows only what its brief says, so the brief is the whole job. Whatever it reports back is a claim you still have to check.

## When to use

- Several failures, bugs, or tasks in separate files or subsystems, where each can be understood alone
- A plan whose tasks are well specified enough to hand to a fresh worker
- A wide search or read-through whose raw output would bury the main conversation
- Finished work that needs a reviewer who hasn't seen your reasoning

**Not for:** failures that may share one cause (use `debugging-systematically` first, then split); breaking a spec into tasks (use `planning-implementation`); passing a whole session on to a later one (use `handing-off-sessions`).

## The rule

```
NO DISPATCH WITHOUT A SELF-CONTAINED BRIEF; NO RESULT ACCEPTED WITHOUT VERIFICATION
```

Violating the letter of the rule is violating the spirit of the rule. A worker's "done" is not evidence that the work is done.

## Process

1. **Decide whether to split at all.** Split only if each unit can be finished without the others' results and none of them write the same files, branch, database, or port. If fixing one might fix another, investigate them together first. If the units share state, run them one after another, or give each its own worktree.
   Exit: each unit is written down, and nothing is shared between them.

2. **Size the fan-out.** Start with the fewest agents that cover the independent domains. Three to five is usually plenty. Each extra agent costs tokens and review time, and parallel writers multiply merge conflicts. Match the model to the task: a cheap, fast model for mechanical work with a clear spec, a standard model for multi-file judgment, and the strongest model for review and architecture.
   Exit: a fan-out number and a model tier for each unit.

3. **Write the brief.** Each brief is self-contained. Never paste session history or earlier tasks' summaries. It holds five parts:
   - **Goal:** one sentence saying what "finished" means.
   - **Context:** file paths, the interfaces it touches, error text, and the decisions already made. Keep it to what this unit needs.
   - **Constraints:** what it may not touch, whether it may commit or push, which commands are too expensive to run, and that it may not start subagents of its own.
   - **Output contract:** the exact shape of the report, plus a status (see Output).
   - **Stop conditions:** when to give up and report BLOCKED or NEEDS_CONTEXT rather than guess.
   Exit: a stranger with no chat history could do the task from the brief alone.

4. **Dispatch together.** Put all the independent dispatches in one message so they run at the same time. Record the base commit before any writer starts, so you can diff exactly what each one changed.
   Exit: every unit has been dispatched, and the base is recorded.

5. **Handle each status.**
   - DONE: go to review.
   - DONE_WITH_CONCERNS: read the concerns first. If they are about correctness or scope, deal with them before review.
   - NEEDS_CONTEXT: send what was missing and dispatch again.
   - BLOCKED: split the task, supply the missing piece, or move it up a model tier. Don't send the same brief again unchanged.
   Exit: every unit is at DONE, or you have made an explicit decision to drop it.

6. **Verify and integrate.** Treat each report as a set of claims. Read the actual diff from the recorded base, run the tests the unit touched, and check that its changes don't conflict with the other units. For important work, send a fresh-context reviewer the diff and the requirements, with no chat history. Tell it to try to disprove the work. Findings go back to the implementer, and the reviewer checks again, up to a fixed number of rounds.
   Exit: the verification commands have been run and their output read. The combined change passes after integration.

## Output

Every brief asks the worker to end with this block:

```
Status: DONE | DONE_WITH_CONCERNS | NEEDS_CONTEXT | BLOCKED
Changed: <files, or "none">
Evidence: <command run> → <result, one line>
Concerns / needs: <specific, or "none">
```

Anything longer goes in a report file, and the reply points to it.

## Rationalizations

| Excuse | Reality |
|---|---|
| "The agent can read the chat, no need to spell it out" | A subagent starts empty. Anything you didn't write in the brief, it doesn't know. |
| "Paste the whole history so it has everything" | History buries the task. Give it the goal, interfaces, constraints, and nothing else. |
| "It said DONE and tests pass" | That is its claim. Read the diff and run the tests yourself. |
| "More agents means faster" | Past the number of independent domains, extra agents add conflicts and review load, not speed. |
| "These failures look separate enough" | If one fix might fix another, split them after the investigation, not before. |
| "Resend the same brief, it'll get it this time" | A blocked worker needs a changed input: more context, a smaller task, or a stronger model. |

## Red flags

- Two agents told to edit the same file or run on the same branch
- A brief that says "as discussed" or "continue from above"
- Accepting a report without opening the diff
- A worker starting its own reviewers or sub-workers
- Sending out a second wave before the first one's results have been checked

## References

- [brief-template.md](references/brief-template.md): open when writing a brief for an implementer, investigator, or reviewer
