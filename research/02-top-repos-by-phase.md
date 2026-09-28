# Engineering skills across 33 repos, by SDLC phase (2026-09-28)

Repos were shallow-cloned and their SKILL.md files read. **V** = body read, so the technique is taken from it. **D** = description only.

## Repo key

| Key | Repo | Stars | Skills |
|---|---|---|---|
| SP | https://github.com/obra/superpowers | 292k | 15 |
| SPL | https://github.com/obra/superpowers-lab | 429 | 4 |
| GS | https://github.com/garrytan/gstack | 134k | ~55 |
| MP | https://github.com/mattpocock/skills | 271k | 38 |
| AN | https://github.com/anthropics/skills | 179k | 20 |
| CPO | https://github.com/anthropics/claude-plugins-official | 37k | 31 + commands/agents |
| AO | https://github.com/addyosmani/agent-skills | 99.5k | 25 |
| TOB | https://github.com/trailofbits/skills | 7.3k | 85 |
| VL | https://github.com/vercel-labs/agent-skills | 31.6k | 9 |
| WS | https://github.com/wshobson/agents | 40k | 183 |
| OAI | https://github.com/openai/skills | 27.7k | 44 |
| SEN | https://github.com/getsentry/skills | 1.0k | 27 |
| CF | https://github.com/cloudflare/skills | 2.9k | 14 |
| SUP | https://github.com/supabase/agent-skills | 2.7k | 2 |
| EXPO | https://github.com/expo/skills | 2.6k | 26 |
| HC | https://github.com/hashicorp/agent-skills | 877 | 20 |
| MS | https://github.com/microsoft/skills | 3.1k | 205 (mostly Azure SDKs) |
| GG | https://github.com/google-gemini/gemini-skills | 4.2k | 3 |
| GOO | https://github.com/google/skills | 20.4k | 153 (GCP) |
| DN | https://github.com/dotnet/skills | 5.5k | 108 |
| IMP | https://github.com/pbakaus/impeccable | 71.9k | 2 core |
| UUX | https://github.com/nextlevelbuilder/ui-ux-pro-max-skill | 131k | 6 |
| CE | https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering | 18k | 23 |
| NEO | https://github.com/NeoLabHQ/context-engineering-kit | 1.7k | ~50 |
| CS | https://github.com/callstackincubator/agent-skills | 1.7k | 13 |
| STR | https://github.com/stripe/ai | 1.8k | 10 |
| NEON | https://github.com/neondatabase/agent-skills | 95 | 17 |
| GHC | https://github.com/github/awesome-copilot | 39k | 441 |

Also exist: firebase/agent-skills, datadog-labs/agent-skills, angular/skills, K-Dense-AI/claude-scientific-skills (science). gsd-build/get-shit-done ships commands/agents, no SKILL.md.

## 1. Ideation / Spec
- **brainstorming** (SP, V): HARD-GATE before implementation; classify Spike / Bounded / Architectural out loud; spec self-review.
- **office-hours** (GS, V): six forcing questions (demand reality, status quo, desperate specificity, narrowest wedge, observation, future-fit); premise challenge.
- **spec** (GS, V): five phases; reads code before asking technical questions; quality gate before filing.
- **grilling / grill-me / grill-with-docs** (MP, V): design tree; each round asks the full *frontier* of unblocked questions, numbered, each with a recommended answer; facts are looked up by subagents, decisions go to the user.
- **interview-me** (AO, V): one question at a time to ~95% confidence; "what they ask ≠ what they want".
- **idea-refine**, **spec-driven-development** (AO, D); **to-spec**, **domain-modeling** (MP, D); **define-goal** (OAI, V: outcomes and evidence over activity).

## 2. Planning
- **writing-plans** (SP, V): mandatory header; one action per step with a checkable result; global constraints; self-review.
- **plan-eng-review** (GS, V): hard scope gate; 15 cognitive patterns (boring by default, blast radius, reversibility, Conway, "make the change easy first", error budgets).
- **autoplan** (GS, V): six decision principles; classifies decisions before auto-deciding.
- **to-tickets** (MP, V): tracer-bullet vertical slices that are demoable, fit one context window, and declare blockers; prefactor first.
- **wayfinder** (MP, V): multi-session map as a tracker index, not a store.
- **feature-dev** (CPO, V): parallel code-explorer agents → clarifying questions → 2–3 architect agents with different stances (minimal, clean, pragmatic) → user picks.

## 3. Implementation
- **executing-plans** (SP, V): make rulings instead of stalling; completion contract per task.
- **incremental-implementation** (AO, V): thin slices that each leave the system working.
- **source-driven-development** (AO, V): verify against official docs and cite them.
- **constraint-driven-development** (AO, V): quality bar written into CONSTRAINTS.md; watches for suppressions, skipped tests, stripped assertions.
- **codebase-design** (MP, V): deep-module vocabulary (module, interface, depth, seam, adapter, leverage, locality), after Ousterhout and Feathers.
- **prototype** (MP, V): throwaway code that answers one question, on a throwaway branch.
- **deslop-shared-libs** (GS, V): extract only after proving ≥2 real call sites.
- **finding-duplicate-functions** (SPL, V): classical extraction, then LLM clustering by intent.
- **react-best-practices** (VL, V): 70 rules in 8 categories, ordered by impact, one file per rule.

## 4. Testing
- **test-driven-development** (SP, V): Iron Law; mandatory watch-it-fail; delete code written before its test.
- **tdd** (MP, V): test only at seams agreed in advance; anti-patterns: implementation-coupled, tautological, horizontal slicing.
- **qa** (GS, V): weighted health score; diff-aware mode; atomic fix commits with regression tests.
- **webapp-testing** (AN, V): helper scripts treated as black boxes (`--help`, don't read the source); server-lifecycle helper.
- **property-based-testing** (TOB, V): property catalog (roundtrip, inverse, invariant, oracle).
- **mutation-testing** (TOB, V): triage surviving mutants.
- **crap-score** (DN, V): complexity² × (1 − coverage)³ + complexity.
- **terraform-test** (HC, V); **playwright** (OAI, V).

## 5. Debugging
- **systematic-debugging** (SP, V): Iron Law; four phases; after three failed fixes, question the architecture; find-polluter.sh.
- **investigate** (GS, V): scope lock via hook; three-strike stop; structured escalation.
- **diagnosing-bugs** (MP, V): "build a feedback loop — this IS the skill"; ten loop types; minimise; 3–5 falsifiable ranked hypotheses; tagged debug logs; regression test only at a correct seam.
- **context-degradation** (CE, V): lost-in-middle, poisoning, distraction, confusion, clash.

## 6. Code review
- **review** (GS, V): scope-drift check; enum completeness (grep outside the diff); specialist army; Fix-First.
- **code-review** (CPO, V): Haiku gate; five parallel reviewers; a separate agent scores each issue 0–100; only high-confidence issues posted.
- **pr-review-toolkit** (CPO): silent-failure-hunter, type-design-analyzer, pr-test-analyzer, comment-analyzer.
- **code-review** (MP, V): Standards and Spec subagents in parallel, never merged or reranked; Fowler smell baseline.
- **code-review-and-quality** (AO, V): five axes; approve when the change definitely improves code health.
- **receiving-code-review** (SP, V): no performative agreement; verify, then implement or push back.
- **doubt-driven-development** (AO, V): fresh-context reviewer biased to disprove each non-trivial decision.
- **find-bugs** (SEN, V); **iterate-pr** (SEN, V); **django-perf-review** (SEN, V: "zero findings is acceptable").

## 7. Security
- **cso** (GS, V): evidence before assurance; confidence gates.
- **fp-check** (TOB, V): rationalizations to reject, each paired with a required action; explicit TRUE/FALSE POSITIVE verdict.
- **variant-analysis** (TOB, V): one root cause, many manifestations.
- **differential-review** (TOB, V): depth scales with codebase size; states coverage limits.
- **audit-context-building** (TOB, V): build understanding, not verdicts.
- **sharp-edges**, **spec-to-code-compliance**, **supply-chain-risk-auditor** (TOB, V: "unavailable data is never evidence of risk").
- **security-review** (SEN, V: high-confidence only); **gha-security-review** (SEN, V: no concrete exploit, no finding); **skill-scanner** (SEN, V).
- **security-threat-model**, **security-ownership-map** (OAI, V).
- **careful / guard / freeze** (GS, V): enforced by hooks, not prose.

## 8. Performance
- **benchmark** (GS, V); **web-perf** (CF, V: fetch thresholds rather than recall them); **performance-optimization** (AO, D); **supabase-postgres-best-practices** (SUP, V); **react-native-best-practices** (CS, V).

## 9. Frontend / UI
- **frontend-design** (AN, V): names current AI-design clusters to avoid.
- **impeccable** (IMP, V): verify in bounded passes, not a loop.
- **ui-ux-pro-max** (UUX, V); **web-design-guidelines** (VL, V: fetches the latest guidelines every run); gstack design-*; Expo skills.

## 10. Backend / API / DB
- **mcp-builder** (AN, V): research → implement → review → write 10 eval questions.
- **api-and-interface-design** (AO); Cloudflare workers skills (CF, V); **stripe-best-practices** (STR, V: pin API versions); **neon-postgres-branches** (NEON, V); HashiCorp terraform skills (HC); WS backend patterns.

## 11. DevOps / CI / Release
- **ship** (GS, V): merge base before tests; bisectable commits; verification gate before push.
- **finishing-a-development-branch** (SP, V): tests first; exactly three options.
- **gh-fix-ci** (OAI, V): fetch logs, summarise, get plan approval before fixing.
- **land-and-deploy / canary** (GS); AO ci-cd, shipping, observability; WS incident-response, slo-implementation.

## 12. Docs
- **document-release** (GS, V): Diátaxis coverage map from the diff.
- **agents-md** (SEN, V): under 60 lines, never over 100.
- documentation-and-adrs (AO); claude-md-improver (CPO).

## 13. Git workflow
- **using-git-worktrees** (SP, V): detect existing isolation first; never fight the harness.
- **pr-writer** (SEN, V): PR body is a cover note for reviewers, not a changelog.
- resolving-merge-conflicts (MP); yeet / gh-address-comments (OAI); retro (GS).

## 14. Meta / skill authoring
- **writing-skills** (SP, V): watch an agent fail without the skill first.
- **skill-creator** (AN, V): with-skill vs baseline runs, grader, blind comparator, description optimisation.
- **writing-for-agents** (MP, V): descriptions as context pointers; front-load the keyword.
- **skill-writer** (SEN, V): SKILL.md as a router with "open when…" pointers; ships EVAL.md.

## 15. Agent orchestration
- **subagent-driven-development** (SP, V): statuses DONE / DONE_WITH_CONCERNS / NEEDS_CONTEXT / BLOCKED; per-task model tiers; review package from recorded base.
- **dispatching-parallel-agents** (SP, V).
- **do-and-judge / judge-with-debate** (NEO, V): meta-judge writes the rubric before judging.
- **ralph-loop** (CPO, V); **handoff** (MP); context-save/restore (GS).

## Recurring techniques worth copying
1. Iron Law + rationalization table + red flags.
2. Gate before claims (identify command → run → read → claim).
3. Fresh-context adversarial reviewers.
4. Confidence filtering; zero findings is acceptable.
5. Scripts measure, the model judges.
6. Retrieval over pre-training (fetch current docs and thresholds).
7. Guardrails enforced by hooks, not prose.
8. Evals for skills (baseline vs with-skill, trigger optimisation).
