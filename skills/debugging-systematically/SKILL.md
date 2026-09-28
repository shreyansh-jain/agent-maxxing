---
name: debugging-systematically
description: Root-cause debugging discipline for bugs, failures and regressions. Use when a test fails, something throws or crashes, output is wrong, behavior changed after a deploy or upgrade, a performance regression appears, or a previous fix did not hold.
license: Apache-2.0
metadata:
  version: "0.1.0"
  category: "debug"
  sources: "obra/superpowers systematic-debugging (MIT); mattpocock/skills diagnosing-bugs (MIT); garrytan/gstack investigate (MIT); addyosmani/agent-skills debugging-and-error-recovery (MIT)"
---

# Debugging Systematically

A bug is fixed when you can name its cause and show a check that goes red without the fix and green with it; everything else is guessing.

## When to use

- A test, build, or CI job fails and the reason is not already obvious from the first error line
- Wrong output, crash, hang, or "it worked yesterday"
- A performance regression
- A fix was applied and the problem came back, or a second symptom appeared

**Not for:** tests that pass and fail without code changes (use `triaging-flaky-tests`); CI-only failures where the job log is the main evidence (use `fixing-ci-failures`); production outages where mitigation comes before diagnosis (use `responding-to-incidents`).

## The rule

```
NO FIX WITHOUT A RED-CAPABLE REPRO AND A NAMED ROOT CAUSE
```

Violating the letter of the rule is violating the spirit of the rule. A fix you cannot explain is a coincidence you have not yet caught.

## Process

1. **Build the feedback loop.** This is most of the work. Find one command that drives the real code path and asserts the *user's exact symptom*. Try these in order: a failing test at the nearest seam; a curl or HTTP script; a CLI run diffed against a known-good output; a headless browser script; replaying a captured payload; a throwaway harness around one function; a fuzz or property loop for "sometimes wrong"; `git bisect run` when a good and a bad state are known.
   Tighten it: faster (narrow the scope), sharper (assert the symptom, not "didn't crash"), deterministic (pin time, seed randomness, isolate the filesystem and network).
   Exit: you have *run* one command, shown its output, and it fails on this bug. If you cannot build one, stop, list what you tried, and ask for access, a captured artifact, or permission to add instrumentation.

2. **Reproduce and minimise.** Confirm the loop shows the failure the user described, not a nearby one. Then cut inputs, config, callers and steps one at a time, re-running after each cut.
   Exit: every remaining element is load-bearing. Removing any one of them turns the loop green.

3. **Read the evidence before theorising.** Read the full error and stack trace, not the first line. Run `git log -p` on the failing area and check recent dependency or config changes. Find a working sibling (similar code that works) and list every difference between it and the broken code.
   Exit: you can point to the line or boundary where good data becomes bad.

4. **Hypothesise, ranked.** Write 3–5 hypotheses, each falsifiable: "If X is the cause, changing Y makes the bug disappear." Show the list to the user if they are present, because they often re-rank it instantly. Do not wait on them.
   Exit: a ranked list, each with the prediction that would kill it.

5. **Test one variable at a time.** Each probe maps to one prediction. Prefer a debugger or REPL; otherwise add targeted logs at the boundaries that distinguish hypotheses, tagged with a unique prefix such as `[DBG-7f3a]` so cleanup is one grep. For performance problems, measure a baseline and bisect instead of logging.
   Exit: one hypothesis survives and the others are falsified by observed output.

6. **Fix at the root, test first.** Turn the minimised repro into a failing test at a seam that exercises the real bug pattern. Watch it fail, apply the smallest fix at the source (not where the symptom surfaced), and watch it pass. Then re-run the original, un-minimised loop. If no honest seam exists, say so: that is an architectural finding.
   Exit: the test fails when the fix is reverted and passes when it is restored.

7. **Clean up and report.** Remove the tagged logs (`grep -rn "DBG-7f3a"`), delete throwaway harnesses, and state the root cause in one sentence.

**Three strikes.** If three fixes have failed, stop fixing. Three failures mean the model of the system is wrong, not the fix. Return to step 3, question the architecture, and tell the user what you have ruled out.

**Scope lock.** Once a hypothesis survives, edit only the module it implicates. Changes spreading into unrelated files mean you are patching symptoms.

## Output

```
Root cause: <one sentence: what, where (file:line), why it produced the symptom>
Repro: <the command>, red before / green after
Fix: <what changed and why it is at the source>
Regression test: <path>, or "no honest seam: <reason>"
Ruled out: <hypotheses falsified, with the evidence>
```

## Rationalizations

| Excuse | Reality |
|---|---|
| "I can see the bug, just fix it" | Then writing the repro takes two minutes and proves it. Seeing a bug and seeing *the* bug differ. |
| "No time for process, it's urgent" | Guess-fixing is the slow path: each wrong fix costs a full cycle and adds noise. |
| "It's probably X, let me try it" | "Probably" is a hypothesis. Rank it with the others and test it. |
| "I'll fix several things at once" | Then you cannot tell which change mattered, and you have hidden new bugs. |
| "The test is hard to write, I'll verify manually" | A hard-to-test bug is the one most likely to come back. Write the harness. |
| "One more fix attempt" (after 2 failures) | Three strikes. Question the model, not the patch. |

## Red flags

- Editing code before the repro command exists
- Proposing a fix in the same breath as reading the error
- "Should work now" without running the loop
- Adding a retry, sleep, `try/catch`, or null check to make the symptom disappear
- The fix touches files the surviving hypothesis does not implicate
- Each fix reveals a new failure somewhere else

## References

- [feedback-loops.md](references/feedback-loops.md): open when you cannot find a repro command, or the bug is non-deterministic
- [root-cause-tracing.md](references/root-cause-tracing.md): open when the error surfaces far from where bad data enters
- [scripts/bisect_run.sh](scripts/bisect_run.sh): run with `bash scripts/bisect_run.sh <good-ref> <bad-ref> <command>` when a known-good commit exists
