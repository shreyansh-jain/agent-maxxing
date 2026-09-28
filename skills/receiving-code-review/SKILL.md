---
name: receiving-code-review
description: Discipline for acting on code review feedback from people, bots or other agents. Use when review comments arrive on a PR, a reviewer subagent returns findings, a user relays feedback to address, or a suggestion looks wrong, unclear or out of scope.
license: Apache-2.0
metadata:
  version: "0.1.0"
  category: "review"
  sources: "obra/superpowers receiving-code-review (MIT); addyosmani/agent-skills code-review-and-quality (MIT); garrytan/gstack review greptile-triage (MIT)"
---

# Receiving Code Review

A review comment is a claim about the code, and you check it before you change anything. Correct feedback gets fixed and shown. Wrong feedback gets a technical reply. Unclear feedback gets a question before you implement anything.

## When to use

- A PR has review comments to address (human, Copilot, CodeRabbit, Greptile, a reviewer subagent)
- The user pastes or forwards feedback ("the reviewer says…", "fix items 1–6")
- A suggestion seems wrong for this codebase, conflicts with an earlier decision, or asks for scope nobody requested

**Not for:** reviewing someone else's change (use `reviewing-code`); CI failures on the PR (use `fixing-ci-failures`).

## The rule

```
VERIFY EACH COMMENT AGAINST THE CODE BEFORE CHANGING ANYTHING
```

Violating the letter of the rule is violating the spirit of the rule. A reviewer sees a slice of the code, and agreeing without checking just moves their blind spot into your commit.

## Process

1. **Read all of it first.** Collect every comment (`gh pr view <n> --comments`, `gh api repos/{owner}/{repo}/pulls/<n>/comments` for inline threads) and number them. Don't start fixing item 1 before reading item 9, because items often interact.
   Exit: a numbered list of every comment, with file:line.

2. **Restate each item as a technical requirement.** "Use a map here" becomes "lookup in `resolveUser` is O(n) per call; they want O(1)". If you can't restate an item, it is unclear.
   Exit: each item is either restated or marked unclear.

3. **Stop on anything unclear.** Ask about every unclear item in one message, before implementing *any* item. A partial understanding produces a wrong fix that looks right.
   Exit: no unclear items remain, or the question has been sent and you are waiting.

4. **Verify each item against reality.** Read the code and its callers. Run the relevant single test file where one exists. Check whether the concern is already handled elsewhere, whether the suggested change breaks callers or other platforms, and whether there is a documented reason for the current code (comments, ADRs, `git log -L`). For "implement this properly" requests, grep for real usage first. An unused path is a candidate for deletion (YAGNI), not for gold-plating.
   Exit: each item has a verdict:

   | Verdict | Meaning |
   |---|---|
   | **Accept** | correct and in scope |
   | **Push back** | incorrect for this codebase, breaks something, or contradicts a decision the user made; you have evidence |
   | **Clarify** | cannot verify without information you don't have |
   | **Defer** | correct but out of scope; propose a follow-up instead of growing this change |

   Items that conflict with the user's earlier decisions go to the user, not straight to the reviewer.

5. **Implement accepted items one at a time.** Order: blockers and security issues first, then simple fixes, then larger refactors. After each item, run the check that proves it (the single relevant test file, the type checker), so a regression can be traced to one item.
   Exit: each accepted item has its own verified change.

6. **Respond in the reply shape below.** Draft the replies; post them only if the user asked you to reply on the PR. If you pushed back and later find the reviewer was right, say so in one line and fix it.

## Output

Per item, one line, factual, no preamble:

```
1. Accept: fixed in src/users/resolve.ts:42, now a Map lookup; test users/resolve.test.ts passes.
2. Push back: the null check is needed because `legacyImport()` passes null (src/import/legacy.ts:88); test added to show it.
3. Clarify: "handle the error case": the network error or the 404? They need different handling.
4. Defer: agree the retry policy should be shared; proposed follow-up instead of widening this PR.
```

Replies state what changed, where, and the evidence. Skip thanks, praise and "you're absolutely right". The fix shows you heard the comment.

## Rationalizations

| Excuse | Reality |
|---|---|
| "The reviewer is senior, just do it" | Seniority doesn't make a claim true for this code. Verify it. That takes minutes. |
| "It's a bot, ignore it" / "It's a bot, apply it" | Bots are right sometimes and wrong often. Same process: verify, then decide. |
| "I'll do the clear ones now and ask about the rest later" | Unclear items often change how the clear ones should be done. Ask first. |
| "Pushing back will look defensive" | Evidence isn't defensive. Silently applying a wrong change is the bigger failure. |
| "While I'm here I'll also refactor X" | That's new scope inside a review response. Defer it. |
| "I'll batch all fixes and test at the end" | Then you can't tell which fix broke what. |

## Red flags

- Editing files before every comment has been read
- Implementing a suggestion you can't explain
- Reply text that contains agreement or thanks but no location or evidence
- Adding a feature, abstraction or config option because a reviewer said "properly", without grepping for real usage
- Posting replies or resolving threads the user didn't ask you to touch
