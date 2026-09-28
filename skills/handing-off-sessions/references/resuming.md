# Resuming from a handoff

Treat the handoff as a claim about the state of things at the moment it was written. Check it before you build on it.

1. **Check the state.** Run `git status` and `git log -1`. Compare the branch, SHA, and uncommitted files with the `State` section. If they differ, someone has worked since the handoff was written. Read what changed before you go further.
2. **Read the "Read first" items**, and only those. Leave the rest of the repo alone until a next step needs it.
3. **Re-run the last check.** If the handoff recorded `npm test -- tests/x.test.ts → 2 failing`, run it and confirm you get the same result. A different result means the handoff is stale.
4. **Respect decisions and failed attempts.** Don't reopen a recorded decision unless new evidence contradicts it. Don't retry a failed approach unless you know what's different this time.
5. **Start at next step 1.** If it's blocked by an open question, ask that question first. Don't guess the answer.
6. **When you finish or stop,** update the handoff in place or write a new one. Leave the previous one in place.
