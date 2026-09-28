---
name: planning-implementation
description: Implementation plan built from an approved spec or clear requirements, as ordered vertical-slice tasks with exact files, interfaces, tests, and verification commands. Use when a spec or ticket is approved and work is about to start, when a task feels too big to begin, when work must be split into tickets or across sessions or agents, or when the user asks for a plan or task breakdown.
license: Apache-2.0
metadata:
  version: "0.1.0"
  category: "plan"
  sources: "obra/superpowers writing-plans (MIT); mattpocock/skills to-tickets (MIT); mattpocock/skills wayfinder (MIT); addyosmani/agent-skills planning-and-task-breakdown (MIT)"
---

# Planning Implementation

A plan is the set of decisions an implementer can't make alone: which files, which names and signatures, which values, and which tests prove each step. Leave out everything else.

## When to use

- A spec, ticket, or design has been approved and implementation is about to start
- A task feels too large to start, or its order isn't obvious
- Work needs splitting into tickets, parallel agents, or several sessions
- The user asks for a plan, task list, or breakdown

**Not for:** working out what to build (use `clarifying-intent` or `writing-specs`); critiquing someone else's plan (use `reviewing-plans`); carrying out a plan that already exists (use `implementing-incrementally`).

## Process

1. **Read the spec and the code.** Collect the spec's project-wide constraints (version floors, naming rules, dependency limits) with their exact values. Read the modules you'll change, looking for existing patterns to follow and helpers to reuse.
   Exit: you can list the files to create or modify and the job of each.

2. **Map the files first.** Decide on boundaries before tasks. Each file gets one responsibility. Files that change together live together. Follow the repo's existing structure rather than restructuring it on your own initiative.
   Exit: a file map with one line of responsibility per file.

3. **Slice vertically.** Each task is a *tracer bullet*: a narrow path that runs through every layer it needs (schema → API → UI → test) and can be demonstrated or verified by itself. Order the tasks:
   - **Prefactor first.** Make the change easy, then make the easy change. A refactor that only moves code goes in its own task, before any behavior changes.
   - **Risk first** when one piece might not work at all (a new integration, an unproven library). Prove it early.
   - **Contract first** when two sides must be built in parallel. Define the types or schema, then build each side against that contract.
   - **Wide mechanical changes** (renaming a column, retyping a shared symbol) can't land as a single green slice, so use expand → migrate in batches → contract. Each batch is its own task, blocked by the expand step.
   Exit: an ordered list of tasks where each has a demoable result and names the tasks it is blocked by.

4. **Size each task.** A task is the smallest unit with its own test cycle that a reviewer could reject while approving its neighbors. It must fit in one fresh context window. Fold setup and config into the task whose result needs them. If a task touches more than ~5 files or can't be explained in two sentences, split it.
   Exit: every task passes the size test.

5. **Write each task so there is exactly one reasonable way to do it.** Include:
   - **Files**: create, modify (with line ranges if known), test.
   - **Interfaces**: what it *consumes* from earlier tasks and *produces* for later ones, as exact signatures. This is how an implementer who only sees this task learns the names its neighbors use.
   - **Steps**, each one action with a checkable result:
     1. write the failing test, with the spec's exact values in the assertions;
     2. run it, noting the command and the expected failure;
     3. implement the named signature;
     4. run it, noting the expected pass;
     5. checkpoint.
   - **Acceptance**: the observable behavior that proves it is done.

   Describe code by signature and constraints. Include a function body only for an algorithm the signature and tests don't already determine. A plan longer than the code it describes has written the code instead.
   Exit: no step says "TBD", "handle edge cases", "add appropriate validation", or "write tests for the above".

6. **Write a Review Focus section.** List up to five inputs or failure modes that the spec implies but no task's tests cover (empty input, concurrent edits, unicode, a timeout from the payment API), most likely first. Add a test for each one to the task that owns the code.
   Exit: the list exists, or states "checked, none found".

7. **Self-review against the spec:**
   - **coverage**: every requirement maps to a task;
   - **consistency**: a name defined in Task 2 is spelled the same in Task 6;
   - **step scan**: no placeholders, and no transcribed code bodies;
   - **order**: no task depends on a later one.
   Exit: a clean pass.

8. **Get the breakdown approved.** Show the task list: each task's title, what it's blocked by, and what it delivers. Ask whether the granularity and the dependencies look right. Save the plan where the repo keeps plans (default `docs/plans/YYYY-MM-DD-<feature>.md`), or as tickets if the user uses a tracker. For work that spans several sessions, the plan file is the index, and each task links to the details rather than containing everything.
   Exit: the user approves. Then hand off to `implementing-incrementally`, or to `dispatching-subagents` if the tasks are independent.

## Output

Start from [assets/plan-template.md](assets/plan-template.md). Its header (Goal, Architecture, Spec link, Global Constraints, Review Focus) is required.

## Red flags

- Horizontal tasks: "Task 1: all the models, Task 2: all the endpoints"
- A task whose only acceptance criterion is "tests pass"
- A function used in Task 4 that no task defines
- Refactoring and behavior change in the same task
- Pasting a full implementation into the plan
- Presenting the plan and starting on Task 1 in the same turn
