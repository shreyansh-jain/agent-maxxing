# Catalog of open-source software-engineering skills

This catalog covers the best Agent Skills (`SKILL.md`) for software engineering published anywhere, as of **2026-09-28**. It is grouped by lifecycle phase. Seven research passes produced it: official specs, the big collections, awesome-lists and registries, vendor repos, community and language packs, a license audit, and a read of locally installed skills. Raw notes are in [`research/`](research/).

**Columns**
- **License** is the SPDX id read from the repo's LICENSE file. `none` means there is no license file, so the default is all rights reserved.
- **→ here** names the skill in this repo that absorbed the technique.

**Stars and installs** are as reported on 2026-09-28 (GitHub API and skills.sh) and are approximate.

## Contents

1. [The big collections](#the-big-collections)
2. [Define: intent and specs](#define-intent-and-specs)
3. [Plan](#plan)
4. [Build](#build)
5. [Test](#test)
6. [Debug](#debug)
7. [Review](#review)
8. [Security](#security)
9. [Performance](#performance)
10. [Frontend / UI](#frontend--ui)
11. [Backend, API, data](#backend-api-data)
12. [Operate: CI, release, observability, incidents](#operate-ci-release-observability-incidents)
13. [Git workflow](#git-workflow)
14. [Docs and agent context](#docs-and-agent-context)
15. [Agent orchestration and context](#agent-orchestration-and-context)
16. [Skill authoring and evals](#skill-authoring-and-evals)
17. [Language and framework packs](#language-and-framework-packs)
18. [Directories and registries](#directories-and-registries)
19. [License watch-list](#license-watch-list)
20. [What the research says works, and what fails](#what-the-research-says-works-and-what-fails)

## The big collections

| Repo | Stars | License | Character |
|---|---|---|---|
| [obra/superpowers](https://github.com/obra/superpowers) | 292k | MIT | A process methodology: Iron Laws, rationalization tables, subagent-driven development. The most-copied style |
| [mattpocock/skills](https://github.com/mattpocock/skills) | 271k | MIT | Short and sharp; the most-installed engineering skills on skills.sh; skills share one vocabulary |
| [anthropics/skills](https://github.com/anthropics/skills) | 179k | per skill (Apache-2.0 / proprietary) | Reference skills plus skill-creator (evals) |
| [garrytan/gstack](https://github.com/garrytan/gstack) | 134k | MIT | A "virtual engineering team" of slash-command workflows. Very long, with a shared preamble |
| [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) | 99.5k | MIT | 25 skills covering the whole lifecycle, each with rationalizations and red flags |
| [wshobson/agents](https://github.com/wshobson/agents) | 40k | MIT | 183 skills; the widest stack coverage; a reference-pattern knowledge base |
| [github/awesome-copilot](https://github.com/github/awesome-copilot) | 39k | MIT (per-skill overrides) | 441 community skills |
| [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official) | 37k | Apache-2.0 | code-review, feature-dev, pr-review-toolkit, plugin-dev, skill-creator |
| [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) | 31.6k | none (README: MIT) | React/Next performance rules, web design guidelines |
| [openai/skills](https://github.com/openai/skills) | 27.7k | per skill | Codex catalog: gh-fix-ci, threat model, yeet |
| [trailofbits/skills](https://github.com/trailofbits/skills) | 7.3k | CC-BY-SA-4.0 | The best security-audit skills available |
| [getsentry/skills](https://github.com/getsentry/skills) | 1.0k | Apache-2.0 | Tight engineering-hygiene skills: find-bugs, pr-writer, agents-md |

## Define: intent and specs

| Skill | Repo | License | Why it's excellent | → here |
|---|---|---|---|---|
| brainstorming | obra/superpowers | MIT | A hard gate: no implementation before design approval. Classifies each request as Spike, Bounded or Architectural, out loud | clarifying-intent |
| grilling / grill-me (1.2M installs) | mattpocock/skills | MIT | Treats the plan as a design tree. Each round asks the whole frontier of unblocked questions, each with a recommended answer. Facts are looked up; only decisions go to the user | clarifying-intent |
| grill-with-docs | mattpocock/skills | MIT | The same interview, writing ADRs and a glossary as it goes | clarifying-intent, documenting-decisions |
| interview-me | addyosmani/agent-skills | MIT | One question at a time until ~95% confidence; "what they ask ≠ what they want" | clarifying-intent |
| office-hours | garrytan/gstack | MIT | Six forcing questions (demand reality, status quo, narrowest wedge…) plus a premise challenge | clarifying-intent |
| idea-refine | addyosmani/agent-skills | MIT | Divergent, then convergent, shaping of an idea | clarifying-intent |
| spec | garrytan/gstack | MIT | Five strict phases; reads the code before asking technical questions; a quality gate before the issue is filed | writing-specs |
| spec-driven-development | addyosmani/agent-skills | MIT | Objectives, boundaries and success criteria in a PRD before any code | writing-specs |
| to-spec | mattpocock/skills | MIT | Synthesizes the conversation into a tracker issue with no new interview | writing-specs |
| define-goal | openai/skills | Apache-2.0 | Measurable outcomes and evidence rather than activity | writing-specs |
| spec-miner | Jeffallan/claude-skills | MIT | Reverse-engineers a spec from existing code | onboarding-to-codebases |

## Plan

| Skill | Repo | License | Why it's excellent | → here |
|---|---|---|---|---|
| writing-plans | obra/superpowers | MIT | A mandatory header and global constraints. Each task is the smallest independently rejectable unit, in 2–5-minute steps. No placeholders | planning-implementation |
| to-tickets | mattpocock/skills | MIT | Tracer-bullet vertical slices that can be demoed, fit one context window, and declare their blockers; prefactoring first | planning-implementation |
| wayfinder | mattpocock/skills | MIT | For work spanning several sessions: the map issue is an index, not a store | planning-implementation |
| planning-and-task-breakdown | addyosmani/agent-skills | MIT | A dependency graph, then vertical slices, then checkpoints | planning-implementation |
| plan-eng-review | garrytan/gstack | MIT | 15 engineering-manager cognitive patterns (boring by default, blast radius, reversibility); a scope challenge | reviewing-plans |
| autoplan | garrytan/gstack | MIT | Six decision principles; classifies decisions before deciding them automatically | reviewing-plans |
| plan-ceo-review / plan-design-review / plan-devex-review | garrytan/gstack | MIT | Scope, design and DX lenses on a plan | reviewing-plans |
| feature-dev | anthropics/claude-plugins-official | Apache-2.0 | Parallel explorer agents, then 2–3 architect agents with different stances (minimal, clean, pragmatic); the user picks | reviewing-plans |
| doubt-driven-development | addyosmani/agent-skills | MIT | A fresh-context adversarial reviewer for each non-trivial decision, capped at 3 cycles | reviewing-plans |
| planning-with-files | OthmanAdi/planning-with-files | MIT | Plan, findings and progress files on disk, re-injected by hooks so they survive compaction | handing-off-sessions |

## Build

| Skill | Repo | License | Why it's excellent | → here |
|---|---|---|---|---|
| executing-plans | obra/superpowers | MIT | Makes rulings instead of stalling; a completion contract for every task | implementing-incrementally |
| incremental-implementation | addyosmani/agent-skills | MIT | Thin slices that each leave the system working; feature flags for incomplete work | implementing-incrementally |
| implement | mattpocock/skills | MIT | TDD at agreed seams; type-check often, run the full suite once at the end | implementing-incrementally |
| constraint-driven-development | addyosmani/agent-skills | MIT | The quality bar lives in CONSTRAINTS.md; catches suppressions, skipped tests and stripped assertions | implementing-incrementally |
| codebase-design | mattpocock/skills | MIT | Deep-module vocabulary (module, interface, depth, seam, adapter, leverage, locality) | designing-interfaces |
| api-and-interface-design | addyosmani/agent-skills | MIT | Contract first; Hyrum's Law; consistent error semantics; prefer addition over modification | designing-interfaces |
| improve-codebase-architecture | mattpocock/skills | MIT | Finds opportunities to deepen modules, then grills you on the one you pick | refactoring-legacy-code |
| source-driven-development | addyosmani/agent-skills | MIT | Reads versions from the lockfile, fetches the official docs, cites them | grounding-in-official-docs |
| code-simplification | addyosmani/agent-skills | MIT | Preserves behavior exactly; Chesterton's fence; scoped to what changed | simplifying-code |
| code-simplifier | anthropics/claude-plugins-official, getsentry/skills | Apache-2.0 | Simplifies recently changed code only | simplifying-code |
| deslop-shared-libs | garrytan/gstack | MIT | Extracts shared code only after proving at least two real call sites | simplifying-code |
| ponytail | DietrichGebert/ponytail | MIT | The laziest-working-solution ladder (does it need to exist → stdlib → native → one line) | simplifying-code |
| finding-duplicate-functions | obra/superpowers-lab | MIT | Catalogs functions, clusters them, then finds same-intent duplicates in LLM-written code | simplifying-code |
| deprecation-and-migration | addyosmani/agent-skills | MIT | Code is a liability; expand/contract; compulsory vs advisory deprecation | refactoring-legacy-code, migrating-databases-safely |
| legacy-modernizer | Jeffallan/claude-skills | MIT | Incremental modernization of legacy code | refactoring-legacy-code |
| prototype | mattpocock/skills | MIT | Throwaway code that answers exactly one question, on a throwaway branch | implementing-incrementally |

## Test

| Skill | Repo | License | Why it's excellent | → here |
|---|---|---|---|---|
| test-driven-development | obra/superpowers | MIT | Iron Law: no production code without a failing test; you must watch it fail; code written before its test gets deleted | test-driven-development |
| tdd | mattpocock/skills | MIT | Tests only at seams agreed in advance; anti-patterns: implementation-coupled, tautological, horizontal slicing | test-driven-development |
| test-driven-development | addyosmani/agent-skills | MIT | The prove-it pattern for bugs; test sizes; DAMP over DRY | test-driven-development |
| condition-based-waiting | obra/superpowers(-skills) | MIT | Replaces sleeps with condition polling in async tests | triaging-flaky-tests |
| triage-flaky-test | datadog-labs/agent-skills | MIT | Flaky-test triage backed by CI telemetry | triaging-flaky-tests |
| property-based-testing | trailofbits/skills | CC-BY-SA-4.0 | A property catalog (roundtrip, inverse, invariant, oracle) | ideas only |
| mutation-testing | trailofbits/skills | CC-BY-SA-4.0 | Triages surviving mutants into real bugs | ideas only |
| qa / qa-only | garrytan/gstack | MIT | Browser QA with a weighted health score; diff-aware mode; atomic fixes | — |
| webapp-testing | anthropics/skills | Apache-2.0 | Playwright; helper scripts treated as black boxes (`--help`, don't read the source) | — |
| playwright-cli | microsoft/playwright-cli | Apache-2.0 | Official browser automation for agents | — |
| crap-score / test-anti-patterns | dotnet/skills | MIT | Complexity² × (1 − coverage)³ + complexity finds risky code | test-driven-development |
| test-suite-auditor | levnikolaevich/claude-code-skills | MIT | Audits whether a test's oracle is reliable | reviewing-code |

## Debug

| Skill | Repo | License | Why it's excellent | → here |
|---|---|---|---|---|
| diagnosing-bugs (673k installs) | mattpocock/skills | MIT | "Build a feedback loop: this IS the skill." Ten loop types; minimise the repro; 3–5 falsifiable hypotheses; tagged debug logs | debugging-systematically |
| systematic-debugging | obra/superpowers | MIT | Iron Law: no fix without root cause. After three failed fixes, question the architecture. Ships find-polluter.sh | debugging-systematically |
| investigate | garrytan/gstack | MIT | Scope lock enforced by a hook; a three-strike stop; structured escalation | debugging-systematically |
| debugging-and-error-recovery | addyosmani/agent-skills | MIT | Stop the line: reproduce, localise, reduce, fix, guard | debugging-systematically |
| root-cause-tracing / defense-in-depth | obra/superpowers | MIT | Trace backwards to where bad data is made; validate at every layer | debugging-systematically |
| parallel-debugging | wshobson/agents | MIT | Competing hypotheses tested in parallel agents | dispatching-subagents |
| verification-before-completion (223k installs) | obra/superpowers | MIT | No completion claim without fresh evidence; regression proof by reverting the fix | verifying-before-completion |
| context-degradation | muratcankoylan/Agent-Skills-for-Context-Engineering | MIT | Five named failure patterns of long contexts | handing-off-sessions |

## Review

| Skill | Repo | License | Why it's excellent | → here |
|---|---|---|---|---|
| code-review (626k installs) | mattpocock/skills | MIT | Standards and Spec axes run in separate subagents and are never merged or reranked; a Fowler smell baseline | reviewing-code |
| review | garrytan/gstack | MIT | Checks for scope drift; greps outside the diff for sibling enum values; a "specialist army"; fixes first | reviewing-code |
| code-review | anthropics/claude-plugins-official | Apache-2.0 | Five parallel reviewers; a separate agent scores each issue 0–100 for confidence; only high-confidence issues are posted | reviewing-code |
| pr-review-toolkit | anthropics/claude-plugins-official | Apache-2.0 | silent-failure-hunter, type-design-analyzer, pr-test-analyzer, comment-analyzer | reviewing-code |
| code-review-and-quality | addyosmani/agent-skills | MIT | Five axes; approve when code health definitely improves; change sizing | reviewing-code |
| find-bugs | getsentry/skills | Apache-2.0 | Reads the full diff, then maps the attack surface file by file | reviewing-code |
| django-perf-review | getsentry/skills | Apache-2.0 | "Zero findings is acceptable. Pattern matching is not validation" | reviewing-code, optimizing-performance |
| open-code-review | alibaba/open-code-review | Apache-2.0 | An open review pipeline | — |
| requesting-code-review | obra/superpowers | MIT | The reviewer gets the SHAs and the requirements, never the session history | reviewing-code |
| receiving-code-review | obra/superpowers | MIT | No performative agreement; verify each point, then implement or push back | receiving-code-review |
| gh-address-comments | openai/skills | Apache-2.0 | Works through PR comments systematically | receiving-code-review |
| second-opinion / codex | trailofbits/skills, garrytan/gstack | CC-BY-SA / MIT | A review from a different model | reviewing-code |

## Security

| Skill | Repo | License | Why it's excellent | → here |
|---|---|---|---|---|
| cso | garrytan/gstack | MIT | 14 phases: secrets archaeology in git history, supply chain, CI/CD, LLM security, OWASP, STRIDE, confidence gates | auditing-security |
| security-and-hardening | addyosmani/agent-skills | MIT | Threat model first; a three-tier boundary system (always, ask first, never) | auditing-security |
| security-review | getsentry/skills | Apache-2.0 | High-confidence findings only; based on the OWASP cheat sheets | auditing-security |
| gha-security-review | getsentry/skills | Apache-2.0 | No concrete exploit, no finding; GitHub Actions injection | auditing-security |
| skill-scanner | getsentry/skills | Apache-2.0 | Scans third-party skills for prompt injection, secrets and excess permissions | authoring-skills |
| security-threat-model / security-ownership-map | openai/skills | Apache-2.0 | Every claim anchored to repo evidence; a bus-factor graph built from git | auditing-security |
| differential-review | trailofbits/skills | CC-BY-SA-4.0 | Depth scales with codebase size; states coverage limits honestly | ideas only |
| fp-check | trailofbits/skills | CC-BY-SA-4.0 | Rejects listed rationalizations; returns an explicit TRUE or FALSE POSITIVE | ideas only |
| variant-analysis | trailofbits/skills | CC-BY-SA-4.0 | One root cause shows up in many places | ideas only |
| sharp-edges / supply-chain-risk-auditor / agentic-actions-auditor | trailofbits/skills | CC-BY-SA-4.0 | Easy-to-misuse APIs; "unavailable data is never evidence of risk"; attacker input reaching AI actions in CI | ideas only |
| static-analysis (codeql, semgrep, sarif) | trailofbits/skills | CC-BY-SA-4.0 | Drives static-analysis tools | — |
| snyk-fix / secure-dependency-health-check | snyk/studio-recipes | Apache-2.0 | Scan, then remediate | upgrading-dependencies |
| careful / guard / freeze | garrytan/gstack | MIT | Blocks destructive commands with hooks, not prose | shipping-changes |
| git-guardrails-claude-code | mattpocock/skills | MIT | Hooks that block dangerous git commands | — |
| docker-destructive-guardrails | docker/skills | Apache-2.0 | A safety gate before prune and delete | — |

## Performance

| Skill | Repo | License | Why it's excellent | → here |
|---|---|---|---|---|
| performance-optimization | addyosmani/agent-skills | MIT | Measure first; Core Web Vitals targets; N+1 detection; keep or revert | optimizing-performance |
| benchmark | garrytan/gstack | MIT | Baseline, compare, budget, trend | optimizing-performance |
| web-perf | cloudflare/skills | Apache-2.0 | Fetches thresholds instead of recalling them | optimizing-performance |
| core-web-vitals | addyosmani/web-quality-skills | MIT | LCP, INP and CLS from field and lab evidence | optimizing-performance |
| supabase-postgres-best-practices | supabase/agent-skills | MIT | Postgres rules ordered by impact, one file per rule | optimizing-performance, migrating-databases-safely |
| mongodb-query-optimizer | mongodb/agent-skills | Apache-2.0 | Reads explain plans and tunes indexes | optimizing-performance |
| k6-perf-test-website | grafana/skills | Apache-2.0 | Load testing | optimizing-performance |
| react-native-best-practices | callstackincubator/agent-skills | MIT | FPS, TTI, bundle size, memory | — |

## Frontend / UI

| Skill | Repo | License | Why it's excellent |
|---|---|---|---|
| frontend-design (930k installs) | anthropics/skills | Apache-2.0 | Names the current clusters of AI-generated design so they can be avoided |
| react-best-practices (749k) | vercel-labs/agent-skills | none (README: MIT) | 70 rules in 8 categories, ordered by impact |
| web-design-guidelines (674k) | vercel-labs/agent-skills | none (README: MIT) | Fetches the latest guidelines on every run; terse `file:line` output |
| composition-patterns | vercel-labs/agent-skills | MIT (frontmatter) | Compound components instead of boolean-prop sprawl |
| impeccable | pbakaus/impeccable | Apache-2.0 | "Verify in bounded passes, not a loop" |
| ui-ux-pro-max | nextlevelbuilder/ui-ux-pro-max-skill | MIT | A searchable design knowledge base |
| frontend-ui-engineering | addyosmani/agent-skills | MIT | WCAG 2.1 AA; avoids the AI aesthetic |
| accessibility | addyosmani/web-quality-skills | MIT | WCAG 2.2 audits |
| agent-browser (960k) | vercel-labs/agent-browser | not checked | Browser automation for verification |
| dev-browser | SawyerHood/dev-browser | MIT | A warm daemon; ARIA snapshots with element refs |

Frontend-specific skills stay in their upstream repos. This repo covers practices that apply across stacks.

## Backend, API, data

| Skill | Repo | License | Why it's excellent | → here |
|---|---|---|---|---|
| mcp-builder | anthropics/skills | Apache-2.0 | Tools designed for agents; ships 10 eval questions | designing-interfaces |
| api-design-principles / architecture-patterns | wshobson/agents | MIT | REST and GraphQL design; clean architecture, hexagonal, DDD | designing-interfaces |
| database-migration / postgresql-table-design / sql-optimization-patterns | wshobson/agents | MIT | Migration and schema pattern references | migrating-databases-safely |
| postgres-database-migration / design-postgres-tables | timescale/pg-aiguide | Apache-2.0 | Postgres migration guidance | migrating-databases-safely |
| neon-postgres-branches | neondatabase/agent-skills | Apache-2.0 | Tests migrations on database branches | migrating-databases-safely |
| convex-migrate-rehearse | get-convex/agent-skills | Apache-2.0 | Rehearses a migration before running it for real | migrating-databases-safely |
| stripe-best-practices / upgrade-stripe | stripe/ai | MIT | Pins API versions; upgrade path | upgrading-dependencies |
| workers-best-practices / durable-objects | cloudflare/skills | Apache-2.0 | Retrieval over pre-training | — |
| terraform-style-guide / terraform-test | hashicorp/agent-skills | MPL-2.0 | Authoritative Terraform conventions | — |
| terraform-skill | antonbabenko/terraform-skill | custom | A response contract: risk category, validation, rollback; `plan -destroy` gate | migrating-databases-safely (idea) |
| mongodb-schema-design, redis-core, prisma-*, dbt-* | vendors | Apache-2.0 / MIT | Vendor-authoritative data skills | — |

## Operate: CI, release, observability, incidents

| Skill | Repo | License | Why it's excellent | → here |
|---|---|---|---|---|
| ship | garrytan/gstack | MIT | Merges the base branch before tests; bisectable commits; a verification gate before push | shipping-changes |
| finishing-a-development-branch | obra/superpowers | MIT | Tests first, then exactly three options: merge, PR or keep | shipping-changes |
| shipping-and-launch | addyosmani/agent-skills | MIT | Pre-launch checklist; staged rollout; rollback thresholds | shipping-changes |
| land-and-deploy / canary | garrytan/gstack | MIT | Merge, deploy and verify; compare against a screenshot baseline after deploy | shipping-changes |
| gh-fix-ci | openai/skills | Apache-2.0 | Fetches logs, summarizes the failure, gets plan approval before fixing | fixing-ci-failures |
| iterate-pr | getsentry/skills | Apache-2.0 | Loops until CI is green and feedback is handled; stops at human gates | fixing-ci-failures |
| ci-cd-and-automation | addyosmani/agent-skills | MIT | Quality-gate pipeline; feeds CI failures back to the agent | fixing-ci-failures |
| investigating-ci-failures | PostHog/skills | MIT | CI-failure triage | fixing-ci-failures |
| observability-and-instrumentation | addyosmani/agent-skills | MIT | Define "working" first; pick the right signal; verify the telemetry itself | instrumenting-observability |
| distributed-tracing / prometheus / slo-implementation | wshobson/agents | MIT | Observability pattern references | instrumenting-observability |
| opentelemetry / promql | grafana/skills | Apache-2.0 | OpenTelemetry and PromQL | instrumenting-observability |
| incident-response / postmortem-writing / on-call-handoff | wshobson/agents | MIT | Operations playbooks | responding-to-incidents |
| sre-triage | elastic/agent-skills | Apache-2.0 | SRE triage | responding-to-incidents |
| expo-upgrade / prisma-upgrade-v7 / upgrading-dbt | vendors | MIT / Apache-2.0 | Framework-specific upgrade paths | upgrading-dependencies |
| dependency-upgrader | levnikolaevich/claude-code-skills | MIT | Upgrades in reversible batches | upgrading-dependencies |

## Git workflow

| Skill | Repo | License | Why it's excellent | → here |
|---|---|---|---|---|
| using-git-worktrees | obra/superpowers | MIT | Detects existing isolation first; never fights the harness | using-git-worktrees |
| git-workflow-and-versioning | addyosmani/agent-skills | MIT | Atomic commits; splits a messy tree into clean commits; the save-point pattern | writing-commits-and-prs |
| commit / pr-writer / create-branch | getsentry/skills | Apache-2.0 | The PR body is a cover note for reviewers, not a changelog; refuses to commit on main | writing-commits-and-prs |
| commit-commands | anthropics/claude-plugins-official | Apache-2.0 | Commit, push and PR commands | writing-commits-and-prs |
| yeet | openai/skills | Apache-2.0 | Stage, commit, push and PR in one go | writing-commits-and-prs |
| resolving-merge-conflicts (549k) | mattpocock/skills | MIT | Reads both intents from history; never invents behavior | resolving-merge-conflicts |
| using-tmux-for-interactive-commands | obra/superpowers-lab | MIT | Lets the agent drive `rebase -i`, REPLs and vim | — |
| retro | garrytan/gstack | MIT | Weekly metrics from git history | — |

## Docs and agent context

| Skill | Repo | License | Why it's excellent | → here |
|---|---|---|---|---|
| documentation-and-adrs | addyosmani/agent-skills | MIT | ADR template; follows the existing convention first | documenting-decisions |
| domain-modeling | mattpocock/skills | MIT | A CONTEXT.md glossary and ADRs that other skills read | documenting-decisions |
| document-release | garrytan/gstack | MIT | Maps doc coverage against the diff, using Diátaxis | documenting-decisions |
| agents-md | getsentry/skills | Apache-2.0 | Under 60 lines, never over 100; inspects the repo first | writing-agent-context-files |
| claude-md-improver | anthropics/claude-plugins-official | Apache-2.0 | Quality report, then targeted edits | writing-agent-context-files |
| context-engineering | addyosmani/agent-skills | MIT | A hierarchy of context layers: rules → specs → source → errors → conversation | writing-agent-context-files |
| wiki-* | microsoft/skills | MIT | Generates codebase wikis and onboarding docs | onboarding-to-codebases |

## Agent orchestration and context

| Skill | Repo | License | Why it's excellent | → here |
|---|---|---|---|---|
| subagent-driven-development | obra/superpowers | MIT | A fresh subagent per task; a status contract; per-task review; model tiers | dispatching-subagents |
| dispatching-parallel-agents | obra/superpowers | MIT | One agent per independent domain; lists when not to parallelize | dispatching-subagents |
| do-and-judge / judge-with-debate | NeoLabHQ/context-engineering-kit | GPL-3.0 | A meta-judge writes the rubric before anything is judged | ideas only |
| multi-agent-patterns | muratcankoylan/Agent-Skills-for-Context-Engineering | MIT | Orchestration patterns | dispatching-subagents |
| handoff | mattpocock/skills | MIT | References artifacts instead of duplicating them; redacts secrets; suggests skills for the next session | handing-off-sessions |
| context-save / context-restore | garrytan/gstack | MIT | Saves and restores working context across sessions | handing-off-sessions |
| ralph-loop | anthropics/claude-plugins-official | Apache-2.0 | A Stop hook re-feeds the prompt until a completion promise appears | — |
| caveman (542k) | JuliusBrussee/caveman | not checked | Cuts output tokens | — |

## Skill authoring and evals

| Skill | Repo | License | Why it's excellent | → here |
|---|---|---|---|---|
| skill-creator | anthropics/skills | Apache-2.0 | With-skill vs baseline runs, a grader, a blind comparator, and description optimization with a train/test split | authoring-skills |
| writing-skills | obra/superpowers | MIT | TDD for docs: watch an agent fail without the skill first; match the form to the failure | authoring-skills |
| writing-for-agents | mattpocock/skills | MIT | The description is a context pointer: front-load the keyword | authoring-skills |
| skill-writer | getsentry/skills | Apache-2.0 | SKILL.md as a router with "open when…" pointers; ships an EVAL.md | authoring-skills |
| plugin-dev | anthropics/claude-plugins-official | Apache-2.0 | Authoring plugins, hooks, agents and commands | authoring-skills |

## Language and framework packs

| Area | Best pack | License |
|---|---|---|
| Go | [samber/cc-skills-golang](https://github.com/samber/cc-skills-golang) (46 skills: concurrency, goroutine leaks, errors, perf) | MIT |
| Go style | [cxuu/golang-skills](https://github.com/cxuu/golang-skills) | Apache-2.0 |
| Python, TypeScript, Rust, K8s, Terraform, CI | [wshobson/agents](https://github.com/wshobson/agents) | MIT |
| Per-stack personas (Django, FastAPI, Spring, Rails, Laravel, NestJS…) | [Jeffallan/claude-skills](https://github.com/Jeffallan/claude-skills) | MIT |
| .NET | [dotnet/skills](https://github.com/dotnet/skills) | MIT |
| Azure | [microsoft/skills](https://github.com/microsoft/skills) | MIT |
| GCP | [google/skills](https://github.com/google/skills) | Apache-2.0 |
| AWS | [awslabs/agent-plugins](https://github.com/awslabs/agent-plugins) | Apache-2.0 |
| Cloudflare | [cloudflare/skills](https://github.com/cloudflare/skills) | Apache-2.0 |
| React / Next | [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) | none (README: MIT) |
| React Native / Expo | [expo/skills](https://github.com/expo/skills), [callstackincubator/agent-skills](https://github.com/callstackincubator/agent-skills) | MIT |
| Angular | [angular/skills](https://github.com/angular/skills) | none |
| SwiftUI | [twostraws/SwiftUI-Agent-Skill](https://github.com/twostraws/SwiftUI-Agent-Skill), [AvdLee/SwiftUI-Agent-Skill](https://github.com/AvdLee/SwiftUI-Agent-Skill), [steipete/agent-scripts](https://github.com/steipete/agent-scripts) | MIT |
| Android / Compose | [skydoves/compose-performance-skills](https://github.com/skydoves/compose-performance-skills) | Apache-2.0 |
| Java / Spring | [decebals/claude-code-java](https://github.com/decebals/claude-code-java), [sivaprasadreddy/sivalabs-agent-skills](https://github.com/sivaprasadreddy/sivalabs-agent-skills) | MIT |
| Terraform | [hashicorp/agent-skills](https://github.com/hashicorp/agent-skills) (MPL-2.0), [antonbabenko/terraform-skill](https://github.com/antonbabenko/terraform-skill) (custom) | — |
| GraphQL | [apollographql/skills](https://github.com/apollographql/skills) | MIT |
| Postgres | [supabase/agent-skills](https://github.com/supabase/agent-skills), [timescale/pg-aiguide](https://github.com/timescale/pg-aiguide) | MIT / Apache-2.0 |
| Web quality | [addyosmani/web-quality-skills](https://github.com/addyosmani/web-quality-skills) | MIT |

## Directories and registries

| Directory | What it is |
|---|---|
| [skills.sh](https://skills.sh) | Vercel's leaderboard, ranked by `npx skills add` installs |
| [SkillsMP](https://skillsmp.com) | A crawl of every public SKILL.md |
| [claude-plugins.dev](https://claude-plugins.dev/skills) | Auto-indexed registry with download counts |
| [VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills) | ~1,500 curated skills, grouped by vendor |
| [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) | Curated list |
| [travisvn/awesome-claude-skills](https://github.com/travisvn/awesome-claude-skills) | Curated list with security notes |
| [agentskills.io](https://agentskills.io) | The open spec, plus a list of 40+ compatible clients |

## License watch-list

- **Do not copy**:
  - anthropics/skills docx, pdf, pptx and xlsx (proprietary);
  - claude-plugins-official `claude-security` (proprietary);
  - openai/skills `figma*` (Figma Developer Terms);
  - ykdojo/claude-code-tips (all rights reserved);
  - hesreallyhim/awesome-claude-code (CC BY-NC-ND);
  - dpearson2699/swift-ios-skills (PolyForm);
  - Semgrep (Semgrep Rules License);
  - Databricks (custom license);
  - repos with no LICENSE file.
- **Copyleft; borrow ideas only**:
  - trailofbits/skills (CC-BY-SA-4.0);
  - NeoLabHQ/context-engineering-kit (GPL-3.0);
  - hashicorp/agent-skills (MPL-2.0; file-level copyleft).
- **Safe to adapt with attribution**: MIT and Apache-2.0 repos. See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

## What the research says works, and what fails

**Works:**
1. An Iron Law, a rationalization table and a red-flags list, for discipline skills.
2. A gate before any claim: identify the proving command, run it, read the output, then claim.
3. Fresh-context adversarial reviewers.
4. Confidence filtering, where "zero findings" is an acceptable result.
5. Scripts that measure while the model judges.
6. Retrieval over pre-training: fetch current docs and thresholds instead of relying on memory.
7. Guardrails enforced by hooks rather than prose.
8. Evals: with-skill vs baseline runs, plus optimizing when a skill triggers.

**Fails:**
1. **Under-triggering.** In Vercel's evals the skill was never invoked in 56% of cases, and an AGENTS.md docs index beat the skill.
2. **Silent description-budget overflow**, when too many skills are installed.
3. **Bloated bodies.** gstack skills run 6–14k words each.
4. **Overlapping suites fighting for the same trigger.** Superpowers, Pocock, Osmani and gstack all ship TDD, debugging and review skills.
5. **Supply-chain risk.** A 2026 study of 31k skills found 26% vulnerable and 5% likely malicious.
6. **No evals.**

The repo's design responds to each of these; see the [README](README.md#design-decisions).
