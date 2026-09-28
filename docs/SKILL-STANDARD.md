# Skill standard

Every skill in `skills/` follows this contract. `scripts/validate_skills.py` enforces the mechanical parts; review enforces the rest.

The contract is the [Agent Skills spec](https://agentskills.io/specification) plus the rules below, which come from Anthropic's [authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices), superpowers' `writing-skills`, Anthropic's `skill-creator`, and the failure reports collected in [`research/03`](../research/03-directories-popularity-criticisms.md).

## 1. Layout

```
skills/<name>/
  SKILL.md            required — the entry point, loaded on activation
  references/*.md     optional — detail loaded only when SKILL.md points to it
  scripts/*           optional — executable helpers; invoke via interpreter (`python3 scripts/x.py`)
  assets/*            optional — templates the skill copies or fills
  evals/evals.json    required — behavior evals (skill-creator schema)
  evals/triggers.json required — trigger evals (should / should-not activate)
```

References are one level deep: SKILL.md links to `references/x.md`, and `references/x.md` links to nothing else in the skill.

## 2. Frontmatter

Only the six spec keys, so the same file loads in Claude Code, claude.ai, the Skills API, Codex, Gemini CLI, Copilot, Cursor and OpenCode. Anything else hard-fails on claude.ai uploads.

```yaml
---
name: debugging-systematically
description: Root-cause debugging discipline for bugs, failures and regressions. Use when a test fails, something throws, output is wrong, behavior changed unexpectedly, or a previous fix did not hold.
license: Apache-2.0
metadata:
  version: "1.0.0"
  category: "debug"
  sources: "obra/superpowers systematic-debugging (MIT); mattpocock/skills diagnosing-bugs (MIT)"
---
```

| Key | Rule |
|---|---|
| `name` | `^[a-z0-9]+(-[a-z0-9]+)*$`, ≤64 chars, equals the directory name, gerund or verb-first (`reviewing-code`, not `code-review-helper`), never contains `claude` or `anthropic` |
| `description` | ≤1024 chars (aim ≤500), third person, one line. Shape: *one noun phrase saying what it is* + *"Use when …" listing concrete triggers and symptoms*. Never summarize the process: agents follow a summarized workflow instead of reading the body |
| `license` | `Apache-2.0` for skills authored here |
| `metadata` | flat map, **quoted string values only**: `version` (semver), `category` (one of `lead`, `product`, `define`, `architect`, `plan`, `build`, `debug`, `review`, `operate`, `ship`, `docs`, `agents`), `sources` (`owner/repo skill (LICENSE)` entries separated by `;`, `ideas: owner/repo` for idea-only borrowing, `original` if none) |

Keep every value on one line. No YAML block scalars, no lists: the validator parses this subset deliberately so frontmatter stays portable.

## 3. Body contract

Sections in this order; omit a section only when it would be empty.

1. `# Title`, then **one sentence** stating the core principle.
2. `## When to use`: bullets of observable situations. Then `**Not for:**` naming the sibling skill to use instead. This line is what prevents overlapping skills from fighting.
3. `## The rule`: only for discipline skills. One fenced line in capitals (the Iron Law) + "Violating the letter of the rule is violating the spirit of the rule."
4. `## Process`: numbered phases. Each phase ends with an **exit criterion**, which is something checkable, not "when done".
5. `## Output`: the exact shape of what the skill produces (report template, file, message), if it produces something.
6. `## Rationalizations`: table `| Excuse | Reality |`, for discipline skills only.
7. `## Red flags`: short bullets meaning "stop, you are about to violate this".
8. `## References`: `- [file](references/file.md): open when <condition>`.

## 4. Budgets

| Thing | Budget | Why |
|---|---|---|
| description | ≤500 chars target, 1024 hard | all descriptions share a startup budget; overflow is dropped silently |
| SKILL.md body | ≤1,500 words target, 500 lines hard | spec recommends <5k tokens; bloated skills dilute attention |
| a reference file | TOC at top if >100 lines | agents often preview only the head |

## 5. Writing rules

- **Match the form to the failure.** If agents skip the step under pressure, write a rule, a rationalization table and red flags. If the output has the wrong shape, write a recipe for the right shape, not a list of prohibitions. If an element gets omitted, add a required slot to the template.
- **Explain the why** once, briefly, so the agent can handle cases the rule didn't foresee.
- **No nuance clauses.** "Don't X unless it matters" reopens negotiation. Express a real exception as its own condition on something observable.
- **Retrieval over pre-training.** Anything version-sensitive (API flags, thresholds, CLI options) is fetched or read from `--help` at run time, not hard-coded.
- **Scripts measure, the model judges.** Put deterministic checks in `scripts/`; keep judgment in prose.
- **Respect the harness and the user.** Never commit, push, deploy, or run expensive suites unless the user's instructions allow it. Skills say "if the user has asked you to commit", not "commit".
- **Cross-reference by name**: `**REQUIRED:** use the verifying-before-completion skill`. Never `@path`, which force-loads files.
- **One excellent example**, in the most relevant language. No multi-language dilution.
- **No time-sensitive facts** in the body. Put them in a reference with a "last checked" date.

## 6. Evals

`evals/evals.json` uses [skill-creator's schema](https://github.com/anthropics/skills/blob/main/skills/skill-creator/references/schemas.md):

```json
{
  "skill_name": "debugging-systematically",
  "evals": [
    {
      "id": 1,
      "prompt": "A realistic, tempting task with backstory",
      "expected_output": "What success looks like",
      "expectations": ["Verifiable statement 1", "Verifiable statement 2"]
    }
  ]
}
```

At least 3 evals. At least one must apply **pressure** (time, sunk cost, authority, "just this once") for discipline skills.

`evals/triggers.json`: at least 6 `should_trigger: true` and 6 `false`. The false ones are **near misses** that share keywords but belong to a sibling skill.

```json
[
  {"query": "realistic user message", "should_trigger": true},
  {"query": "near-miss message", "should_trigger": false}
]
```

Run them with Anthropic's `skill-creator` (baseline vs with-skill runs, blind comparison, description optimization). A skill is **v1.0.0** once its evals beat baseline; before that, keep `version: "0.x"`.

## 7. Adding a skill

1. Copy `templates/skill/` to `skills/<name>/`.
2. Write `evals/` **first**, and run them without the skill to see the baseline failure (RED).
3. Write the smallest SKILL.md that fixes that failure (GREEN).
4. Re-run the evals, then close any loopholes they expose (REFACTOR).
5. If the skill draws on a new upstream, license-check it, copy its license into `licenses/`, and register it in `scripts/build_notices.py`. Copyleft, custom-licensed and unlicensed repos may only be cited as `ideas:`.
6. Regenerate, then validate:
   ```bash
   python3 scripts/build_marketplace.py   # plugins come from metadata.category
   python3 scripts/build_notices.py       # credits come from metadata.sources
   python3 scripts/validate_skills.py --strict
   ```
7. If the skill belongs in the default install, add it to `CORE` in `scripts/build_marketplace.py`, keeping `swe-core` under the 8,000-character description budget.
