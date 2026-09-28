# Brief templates

Fill in each slot and delete any line that doesn't apply. The brief should make sense to someone who has never seen the conversation.

## Implementer

```
Goal: <one sentence; what "done" means>

Context:
- Repo/dir: <path>; base commit: <sha>
- Files in scope: <paths>
- Interfaces you must use or keep stable: <signatures>
- Decisions already made: <bullets; do not revisit>

Constraints:
- Touch only the files in scope. Do not start subagents.
- Commit: <allowed / not allowed>. Push: never.
- Run only: <the one focused test command>; do not run the full suite.

Stop and report NEEDS_CONTEXT or BLOCKED if: the task needs a design choice
not listed above, you need code outside scope, or you have read several files
without making progress.

Report: end your reply with
Status / Changed / Evidence (command → result) / Concerns
```

## Investigator (read-only)

```
Question: <the one question to answer>
Where to look: <paths, logs, URLs>
Out of scope: <what not to chase>
Do not edit files.
Report: answer first, then evidence as file:line or command output, then
open questions. Under <N> words. Mark anything you inferred rather than saw.
```

## Reviewer (fresh context, adversarial)

```
You are reviewing a change you did not write. Your job is to find reasons it
is wrong; approving is the fallback when you find none.

Requirements: <spec text or path>
Diff: git diff <base>...<head>
Check: (1) every requirement is met, (2) nothing unrequested was added,
(3) correctness bugs, (4) tests prove the behavior rather than the mock.

Report each finding as: severity (critical/important/minor), file:line,
what is wrong, the evidence. "No findings" is a valid result.
```

## Judge (comparing candidates)

Write the rubric **before** reading the candidates. List 3–6 criteria and their weights. Score each candidate against the rubric, cite evidence for every score, and only then pick one. A judge that writes its rubric after seeing the candidates ends up rationalizing its first impression.
