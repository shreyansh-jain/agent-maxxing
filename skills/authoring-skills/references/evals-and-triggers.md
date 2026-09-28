# Evals and trigger tests

## Behaviour evals: `evals/evals.json`

```json
{
  "skill_name": "my-skill",
  "evals": [
    {
      "id": 1,
      "prompt": "Realistic request with backstory, paths, and a temptation",
      "expected_output": "What a good run does",
      "expectations": ["Checkable statement about the transcript or output"]
    }
  ]
}
```

- **Prompts** read like real user messages: concrete file names, some context, casual wording. "Fix the bug" is too vague. "Checkout returns total: null since yesterday's release, fixture in fixtures/cart.json" is the right level of detail.
- **Expectations** describe behaviour you can check in a transcript: "runs the repro before editing", "does not weaken the assertion". Avoid ones a grader can't settle, like "is thoughtful".
- **Pressure** (discipline skills only): combine at least two pressures in one prompt. For example: "demo in 20 minutes" plus "I already tried three fixes" plus "just make it pass".

## Trigger evals: `evals/triggers.json`

```json
[
  {"query": "request that needs this skill", "should_trigger": true},
  {"query": "near miss for a sibling skill", "should_trigger": false}
]
```

- Write at least 6 of each kind. Vary the phrasing: formal, casual, typos, and requests that don't name the skill.
- The most useful false cases are **near misses**: requests that share keywords but belong to a neighbouring skill. A false case with no overlap at all teaches nothing.

## Running them

Anthropic's `skill-creator` can run with-skill and baseline agents side by side, grade the expectations, compare two versions blind, and optimize the description against the trigger set with a train/test split. Any subagent harness works if it follows this protocol:

1. **One fresh context per sample**, with the real surrounding context (the full skill, not an excerpt).
2. **Always run a no-skill control.** If the control already passes, the skill isn't needed.
3. **At least 5 repetitions per variant.** A single sample can mislead.
4. **Read every flagged transcript yourself.** Graders count quoted counter-examples and template echoes as hits.
5. **Treat variance as a result.** If five runs interpret the skill five different ways, the wording isn't binding yet. Tighten the form before adding more words.

## Versioning

Keep a skill below `1.0.0` until its evals beat the baseline. Record which model and harness the evals ran on, since behaviour shifts between models.
