# Deep read of installed reference skills (2026-09-28)

Read from the local installs of superpowers 6.4.1, gstack 1.56, and Anthropic skill-creator. Word counts are SKILL.md bodies.

## superpowers (MIT, obra)

Frontmatter: `name` + `description` only; descriptions are pure "Use when…" triggers, never workflow summaries. Ships a SessionStart hook that injects `using-superpowers`.

| Skill | Words | Key technique worth keeping |
|---|---|---|
| brainstorming | 2613 | HARD-GATE: no implementation before approval. Classifies request as Spike / Bounded / Architectural out loud. |
| writing-plans | 1422 | Mandatory header + Global Constraints; tasks = smallest independently-rejectable unit; 2–5 min steps (failing test → run → implement → run); no placeholders. |
| executing-plans | 3267 | Completion contract: every named test run, `Expected:` compared against real output, deviations logged as `Ruling:`. |
| subagent-driven-development | 4871 | Fresh implementer per task → reviewer (spec + quality) → ≤5 fix rounds, escalating model from round 4. |
| test-driven-development | 1475 | Iron Law "no production code without a failing test first"; verify RED; rationalization table; red flags. |
| systematic-debugging | 1440 | Iron Law "no fixes without root cause"; 4 gated phases; supporting root-cause-tracing, defense-in-depth, condition-based-waiting, find-polluter.sh. |
| verification-before-completion | 580 | Gate: run the command, read the output, then claim. Regression proof: pass → revert fix → must fail → restore. |
| requesting-code-review | 424 | Reviewer gets BASE/HEAD SHAs + requirements, never session history. |
| receiving-code-review | 913 | Verify each item technically; forbids performative agreement. |
| using-git-worktrees | 1069 | Detect existing isolation first (`git-dir` vs `git-common-dir`); prefer native harness tools. |
| finishing-a-development-branch | 1269 | Verify tests → present exactly 3 options (merge / PR / keep) → clean up only what you created. |
| dispatching-parallel-agents | 865 | One agent per independent domain, crafted context, no shared state. |
| writing-skills | 3814 | TDD for docs (baseline pressure test → minimal skill → close loopholes). Description = triggers only. "Match the form to the failure." |

## gstack (MIT, garrytan)

SKILL.md generated from `SKILL.md.tmpl`; ~4,900-word shared preamble per skill (a token-cost criticism). Uses non-standard frontmatter (`triggers`, `preamble-tier`, `hooks`, `benefits-from`).

| Skill | Words | Key technique worth keeping |
|---|---|---|
| review | 12769 | Scope-drift check vs plan; specialist "army" (api-contract, data-migration, performance, security, testing, red-team) chosen adaptively; Fix-First (AUTO-FIX vs ASK); confidence calibration. |
| ship | 9207 | Skeleton + on-demand `sections/` with a manifest: merge base → tests → coverage audit → review → version → changelog → bisectable commits → PR. |
| investigate | 6556 | Iron Law + **scope lock**: after hypothesis, freeze edits to the narrowest dir via a PreToolUse hook. |
| cso | 10497 | 14-phase audit incl. secrets archaeology in git history, supply chain, CI/CD, LLM security, OWASP, STRIDE, false-positive filtering with confidence gates. |
| plan-eng-review | 7350 | Scope challenge at step 0; one issue at a time with opinionated recommendation. |
| qa | 10178 | Diff-aware / full / quick / regression modes; weighted health score; fix loop with atomic commits. |
| health | 6417 | Detect stack tools, run, weighted 0–10 score with history. |
| careful | 382 | PreToolUse regex guard on `rm -r`, `push --force`, `reset --hard`, `DROP TABLE`, `kubectl delete` → ask. |
| document-release | 7959 | Diff → Diátaxis coverage map → auto-fix safe docs, ask on risky. |

## Anthropic skill-creator (Apache-2.0)

- Descriptions should be slightly "pushy" — Claude under-triggers.
- Explain the *why* rather than shouting ALWAYS/NEVER.
- Evals: with-skill vs baseline runs; `grading.json` {text, passed, evidence}; blind comparator between versions.
- Description optimization: 60/40 train/test split, 3 runs per query, ≤5 iterations.
- `quick_validate.py` allows only the six spec keys.

## Distribution patterns observed

- superpowers `plugin.json`: name, description, version, author, homepage, repository, license, keywords. Skills discovered by `skills/<name>/SKILL.md` convention.
- Official marketplace entries: name, description, source (path or `{source:"url", url, sha}`), category, homepage, author.
- gstack uses section manifests `{sections:[{id,file,title,trigger}]}` for on-demand loading — a good scalability pattern.

## Lessons for this repo

1. Keep superpowers' trigger-only descriptions and Iron-Law bodies; keep bodies far shorter than gstack's.
2. Borrow gstack's on-demand sections, specialist checklists and scope-lock idea, without the shared mega-preamble.
3. Borrow skill-creator's eval format so each skill can ship `evals/evals.json`.
