---
name: verifying-before-completion
description: Evidence gate before any claim that work is done, fixed, passing, or ready. Use when about to report success, mark a task complete, say tests or builds pass, hand work back to the user, open a PR, or trust a subagent's report that something works.
license: Apache-2.0
metadata:
  version: "0.1.0"
  category: "debug"
  sources: "obra/superpowers verification-before-completion (MIT); addyosmani/agent-skills test-driven-development prove-it pattern (MIT); garrytan/gstack ship verification gate (MIT)"
---

# Verifying Before Completion

A claim about the state of the work is only true if output you have just produced shows it, in this turn.

## When to use

- You are about to write "done", "fixed", "passing", "works", "ready", or any word that means the same
- Marking a task or plan step complete
- Handing work back, opening a PR, or moving on to the next task
- A subagent or tool reports success on your behalf

**Not for:** finding out why something fails (use `debugging-systematically`); a full review of change quality (use `reviewing-code`); the release checklist (use `shipping-changes`).

## The rule

```
NO COMPLETION CLAIM WITHOUT FRESH EVIDENCE FROM THIS TURN
```

Violating the letter of the rule is violating the spirit of the rule. A paraphrase ("looks good", "should be fine now", "all set") is a claim.

## Process

1. **Name the proving command.** For each claim, identify the command whose output would show it true. The claim decides the evidence you need:

   | Claim | Evidence that proves it | Not enough |
   |---|---|---|
   | Tests pass | the test command's output: 0 failures, and the exit code | an earlier run; "should pass" |
   | Build or typecheck is clean | that command exits 0 | the linter passing |
   | Bug fixed | the original repro now passes | the code changed |
   | Regression test works | it fails with the fix reverted and passes with the fix restored | it passes once |
   | Requirements met | a line-by-line check against the spec | the tests are green |
   | Subagent finished the job | the actual diff, plus your own run of its tests | its report |
   | UI works | you drove it (browser script or screenshot) | the component compiles |

2. **Run it fresh and in full.** Run the whole command, not a subset you extrapolate from. Output from before your last edit is stale.

3. **Read the output.** Check the exit code, the failure and skip counts, and any warnings. A pass message sitting above an error is not a pass.

4. **Claim exactly what the output shows.** If it confirms the claim, state the claim along with the command and the key result. If it doesn't, state the real status with the evidence. If only part was verified, say which part.

5. **If you are not allowed to run the proving command** (the user or the project forbids that suite, it needs credentials you don't have, or it is too expensive under the user's rules), run the narrowest permitted check that bears on the claim, such as a single spec file or `tsc --noEmit`. Report the claim as **unverified** and name the command that would verify it.

For a regression fix, check both directions: run the test and see it pass, revert the fix and see it fail, restore the fix and see it pass again.

## Output

```
Status: done | partially done | not done
Verified: <claim> — `<command>` → <key result, e.g. "42 passed, 0 failed, exit 0">
Unverified: <claim> — would be verified by `<command>` (not run because <reason>)
Remaining: <anything the user must do>
```

## Rationalizations

| Excuse | Reality |
|---|---|
| "It's a one-line change" | One-line changes break builds. The check takes seconds. |
| "I ran it a few edits ago" | That output belongs to different code. Run it again. |
| "The agent said it succeeded" | Agents report what they meant to do. Read the diff and run the tests. |
| "The linter passed" | Linters don't compile, type-check, or run your logic. |
| "I'm confident" | Confidence is not evidence. |
| "The user is waiting, just report done" | A wrong "done" costs them more than ten seconds of verification. |

## Red flags

- "Should", "probably", "seems to", or "I believe" next to a status
- Saying "Great!", "Perfect!" or "Done!" before any command has run
- Reporting a count ("all 42 tests pass") that doesn't appear in the output of this turn
- Moving to the next task while the last command's output went unread
- Treating a partial run as the whole suite without saying so
