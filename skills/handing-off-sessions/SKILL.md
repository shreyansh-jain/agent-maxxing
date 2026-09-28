---
name: handing-off-sessions
description: Session handoff documents that let a fresh agent or a later session resume work without the original conversation. Use when context is running out, work must pause and resume later, a task moves to another agent or teammate, or the user asks to save progress, checkpoint, or write up where things stand.
license: Apache-2.0
metadata:
  version: "0.1.0"
  category: "agents"
  sources: "mattpocock/skills handoff (MIT); mattpocock/skills claude-handoff (MIT); garrytan/gstack context-save and context-restore (MIT); addyosmani/agent-skills context-engineering (MIT)"
---

# Handing Off Sessions

A handoff is an index into what already exists plus the few things that exist only in this conversation. The next agent should be able to start work within one read.

## When to use

- The context window is nearly full, or compaction is about to drop detail
- Work stops today and resumes in a new session
- A task passes to another agent, a background worker, or a teammate
- The user says "save progress", "checkpoint", "write up where we are", or "hand this off"

**Not for:** briefing a subagent on one task inside this session (use `dispatching-subagents`); recording a design decision permanently (use `documenting-decisions`); writing persistent project instructions (use `writing-agent-context-files`).

## Process

1. **Gather the state instead of recalling it.** Run `git status`, `git log --oneline <base>..HEAD`, and `git diff --stat`. Note the branch, any uncommitted files, and the last command that was run along with its result. Find what already records the work: the spec, the plan, issues, PRs, ADRs, and test output files.
   Exit: you have the actual git state and a list of existing artifacts, with paths or URLs.

2. **Separate what is recorded from what exists only here.** Anything already in an artifact gets a reference, not a copy. The handoff exists for what lives only in this conversation: decisions and why they were made, approaches that failed and how, open questions, gotchas, and what the user said they want.
   Exit: every line in the draft is either a pointer or something found nowhere else.

3. **Redact.** Replace keys, tokens, passwords, connection strings, customer data, and personal details with `<REDACTED>`, and say where the real value lives (an env var name, a vault path). A handoff often becomes another agent's prompt or gets pasted into a ticket.
   Exit: a search of the draft finds no secret-shaped strings.

4. **Write it to fit the next session.** If the user said what the next session is for, put that first and cut anything it doesn't need. Write next steps as concrete actions, each with the command or file to start from, in priority order. Name the skills the next agent should load.
   Exit: the first next step can be done without asking a question.

5. **Save it outside the repo unless told otherwise.** Use the OS temp directory or the user's notes location, so the handoff doesn't end up in a commit. Give the user the path. If they asked for a live continuation, start the new agent with the handoff as its prompt and give it a descriptive name.
   Exit: the user has the path, or the name of the new agent.

## Output

```markdown
# Handoff: <task> (<date>)

## Goal
<1–2 sentences: what "done" means for the whole effort>

## State
- Branch `<name>` at `<sha>`; uncommitted: <files or "none">
- Last check: `<command>` → <result>

## Read first
- <path/URL>: <why>

## Decisions (not recorded elsewhere)
- <decision>: <reason>

## Tried and failed
- <approach>: <what happened>

## Next steps
1. <action>: start at `<file or command>`

## Open questions
- <question>: <who can answer>

## Suggested skills
- <skill-name>: <when to use it>
```

## Red flags

- Pasting the plan, the diff, or the spec into the handoff instead of linking to it
- "Continue where we left off" with no command or file to start from
- Writing the state from memory without running `git status`
- A live token or connection string anywhere in the document
- Saving the handoff inside the working tree when nobody asked for that

## References

- [resuming.md](references/resuming.md): open when you are the agent *receiving* a handoff
