# skills-map

Principal-grade Agent Skills for software and product engineering. There are **53 skills** covering the whole lifecycle, from deciding how complex a piece of work is to operating it in production. They were synthesized from the best open-source skill collections, and each follows the open [Agent Skills spec](https://agentskills.io/specification), so the same files work in Claude Code, Codex, Gemini CLI, Copilot, Cursor and OpenCode.

- **[CATALOG.md](CATALOG.md)**: about 150 excellent open-source engineering skills found across the internet (as of 2026-09-28), with sources, licenses, and what makes each one good.
- **[docs/SKILL-STANDARD.md](docs/SKILL-STANDARD.md)**: the authoring contract every skill here follows.
- **[research/](research/)**: raw research notes (standards, repos, registries, licenses, failure modes).

## Start here: complexity decides the process

Every engagement starts with [`assessing-complexity`](skills/assessing-complexity/SKILL.md). It scores the work 0–3 on eight risk dimensions: scope, uncertainty, reversibility, blast radius, coupling, data sensitivity, scale and operability. **The highest-risk dimension sets the tier**, not the average. Each tier runs a matching track:

| Tier | Example | Track |
|---|---|---|
| **C0** Trivial | typo, copy change | edit → verify |
| **C1** Small | new sort option on an existing endpoint | TDD → verify → self-review |
| **C2** Feature | CSV export of a user's invoices | clarify → spec → plan → incremental TDD → review → ship |
| **C3** System | live column rename, new auth store, public API change | C2 + design doc, plan review, test strategy, flags, observability, plus architecture, threat, privacy, migration, capacity or resilience skills as the scores demand |
| **C4** Product | new product, platform, or multi-quarter initiative | [`engineering-products-end-to-end`](skills/engineering-products-end-to-end/SKILL.md): frame → discover → shape increments → architect → plan → build → launch readiness → staged release → operate and learn, with a gate after every phase |
| **Spike** | "can we render PDFs in <500 ms?" | time-boxed throwaway, written answer, then re-assess |

Re-scoring happens whenever new evidence appears. The tier only moves up on its own; a lighter track needs the user's agreement and is recorded as an accepted risk.

## Skills

★ marks the 18 skills in the default **`swe-core`** bundle.

### `swe-lead`

Principal-engineer triage and leadership: complexity assessment, end-to-end product playbook, technical debt.

| Skill | What it is |
|---|---|
| [assessing-complexity](skills/assessing-complexity/SKILL.md) ★ | Principal-engineer triage that scores a piece of work on risk dimensions and picks the process track and skills it needs |
| [engineering-products-end-to-end](skills/engineering-products-end-to-end/SKILL.md) | Principal-engineer playbook that takes a product or platform from problem to operated system through gated phases |
| [managing-technical-debt](skills/managing-technical-debt/SKILL.md) | Finding, recording, prioritizing and paying down technical debt so it is visible to product decisions |

### `swe-product`

Product engineering: scoping the smallest valuable increment and measuring outcomes.

| Skill | What it is |
|---|---|
| [measuring-product-outcomes](skills/measuring-product-outcomes/SKILL.md) | Defining success metrics, product analytics events and A/B experiments so a feature's impact can be proven |
| [scoping-product-increments](skills/scoping-product-increments/SKILL.md) | Scoping a product problem down to the smallest valuable increment worth building next |

### `swe-define`

Clarify intent and write specs before any code.

| Skill | What it is |
|---|---|
| [clarifying-intent](skills/clarifying-intent/SKILL.md) ★ | Intent-discovery interview before building anything new or changing behavior |
| [writing-specs](skills/writing-specs/SKILL.md) ★ | Written specification for a feature, subsystem, or significant change, produced from an agreed intent and the current code |

### `swe-architect`

System architecture, capacity, domain and data modeling, resilience, threat modeling, privacy, design docs.

| Skill | What it is |
|---|---|
| [designing-data-models](skills/designing-data-models/SKILL.md) | Access-pattern-driven schema design covering keys, types, constraints, indexes, tenancy and store choice |
| [designing-resilient-systems](skills/designing-resilient-systems/SKILL.md) | Failure-mode design for distributed calls: timeouts, retries, idempotency, breakers, bulkheads, backpressure |
| [designing-system-architecture](skills/designing-system-architecture/SKILL.md) | System-level architecture design for new products, services and major re-platforms, driven by quality attributes and explicit trade-offs |
| [estimating-capacity](skills/estimating-capacity/SKILL.md) | Back-of-envelope estimation of traffic, storage, bandwidth, concurrency, latency and cost |
| [handling-personal-data](skills/handling-personal-data/SKILL.md) | Engineering practice for collecting, storing, using and deleting personal data |
| [modeling-domains](skills/modeling-domains/SKILL.md) | Domain modeling with a shared glossary, bounded contexts, aggregates and invariants |
| [modeling-threats](skills/modeling-threats/SKILL.md) | Design-time threat modeling of a system, feature or architecture change |
| [writing-design-docs](skills/writing-design-docs/SKILL.md) | Technical design documents and RFCs that decide how a system or change will be built |

### `swe-plan`

Turn specs into reviewable implementation plans and pressure-test them.

| Skill | What it is |
|---|---|
| [planning-implementation](skills/planning-implementation/SKILL.md) ★ | Implementation plan built from an approved spec or clear requirements, as ordered vertical-slice tasks with exact files, interfaces, tests, and verification commands |
| [reviewing-plans](skills/reviewing-plans/SKILL.md) | Engineering review of a plan, spec, or design before implementation starts, covering scope, architecture, failure modes, tests, and performance |

### `swe-build`

Implementation: incremental delivery, TDD, test strategy, E2E, accessibility, LLM features, interfaces, refactoring.

| Skill | What it is |
|---|---|
| [building-accessible-interfaces](skills/building-accessible-interfaces/SKILL.md) | WCAG 2.2 AA accessibility for web UIs, from semantic markup to keyboard, focus, forms and screen readers |
| [building-llm-features](skills/building-llm-features/SKILL.md) | Engineering discipline for product features that call an LLM: evals, prompts, structured output, tools, injection defense, cost |
| [designing-interfaces](skills/designing-interfaces/SKILL.md) | Interface and module design for APIs, public functions, module boundaries and service contracts |
| [grounding-in-official-docs](skills/grounding-in-official-docs/SKILL.md) ★ | Version-accurate use of frameworks, libraries, SDKs, CLIs and cloud APIs, checked against primary sources instead of memory |
| [implementing-incrementally](skills/implementing-incrementally/SKILL.md) ★ | Discipline for building features in thin, verified slices, executing a plan task by task, and keeping the codebase working between steps |
| [onboarding-to-codebases](skills/onboarding-to-codebases/SKILL.md) ★ | Structured orientation in an unfamiliar repository, service or subsystem, ending in an evidence-backed map |
| [planning-test-strategy](skills/planning-test-strategy/SKILL.md) | Risk-based test strategy for a feature, service or system |
| [refactoring-legacy-code](skills/refactoring-legacy-code/SKILL.md) | Safe change of untested or poorly understood code using characterization tests, seams and small reversible steps |
| [simplifying-code](skills/simplifying-code/SKILL.md) ★ | Behavior-preserving cleanup of working code for readability, duplication and needless complexity |
| [test-driven-development](skills/test-driven-development/SKILL.md) ★ | Test-first development discipline (red, green, refactor) for features, bug fixes and behavior changes |
| [testing-end-to-end](skills/testing-end-to-end/SKILL.md) | Reliable browser and API end-to-end tests for critical user journeys |

### `swe-debug`

Root-cause debugging, flaky-test triage, and evidence before claiming done.

| Skill | What it is |
|---|---|
| [debugging-systematically](skills/debugging-systematically/SKILL.md) ★ | Root-cause debugging discipline for bugs, failures and regressions |
| [triaging-flaky-tests](skills/triaging-flaky-tests/SKILL.md) | Diagnosis discipline for non-deterministic tests |
| [verifying-before-completion](skills/verifying-before-completion/SKILL.md) ★ | Evidence gate before any claim that work is done, fixed, passing, or ready |

### `swe-review`

Multi-axis code review, receiving review feedback, and security audits.

| Skill | What it is |
|---|---|
| [auditing-security](skills/auditing-security/SKILL.md) ★ | Evidence-based security audit of code, a diff, or a system surface, reporting only findings with a concrete attack path |
| [receiving-code-review](skills/receiving-code-review/SKILL.md) ★ | Discipline for acting on code review feedback from people, bots or other agents |
| [reviewing-code](skills/reviewing-code/SKILL.md) ★ | Multi-axis review of a diff, branch or pull request for spec fit, correctness and repo standards, with confidence-filtered findings |

### `swe-operate`

Production: performance, safe database migrations, observability, incidents, cloud cost.

| Skill | What it is |
|---|---|
| [controlling-cloud-costs](skills/controlling-cloud-costs/SKILL.md) | Measure-first cloud cost reduction and cost-aware design |
| [instrumenting-observability](skills/instrumenting-observability/SKILL.md) | Vendor-neutral logging, metrics, tracing, SLO and alerting practice built on OpenTelemetry |
| [migrating-databases-safely](skills/migrating-databases-safely/SKILL.md) | Zero-downtime schema and data migration discipline for production databases |
| [optimizing-performance](skills/optimizing-performance/SKILL.md) | Measure-first performance work across backend services, databases and frontends |
| [responding-to-incidents](skills/responding-to-incidents/SKILL.md) | Production incident response, mitigation-first, through to a blameless postmortem |

### `swe-ship`

Delivery: git, CI pipelines and fixes, infrastructure as code, feature flags, dependency upgrades, shipping.

| Skill | What it is |
|---|---|
| [fixing-ci-failures](skills/fixing-ci-failures/SKILL.md) ★ | Triage and repair of failing CI checks and pipelines |
| [managing-feature-flags](skills/managing-feature-flags/SKILL.md) | Feature flag lifecycle from creation through rollout to removal, including safe defaults, targeting and flag-debt cleanup |
| [resolving-merge-conflicts](skills/resolving-merge-conflicts/SKILL.md) | Resolving git merge, rebase, and cherry-pick conflicts by reconstructing what each side intended |
| [setting-up-ci-pipelines](skills/setting-up-ci-pipelines/SKILL.md) | Design and hardening of CI pipelines for fast feedback, reproducibility and least privilege |
| [shipping-changes](skills/shipping-changes/SKILL.md) ★ | End-to-end discipline for taking finished work from a branch to merged and released, including pre-merge verification, integration choice, staged rollout and rollback |
| [upgrading-dependencies](skills/upgrading-dependencies/SKILL.md) | Safe, incremental dependency and framework upgrade practice, from a single package to a monorepo-wide major bump |
| [using-git-worktrees](skills/using-git-worktrees/SKILL.md) | Isolated git worktree workspaces for parallel or risky work |
| [writing-commits-and-prs](skills/writing-commits-and-prs/SKILL.md) ★ | Commit messages, commit splitting, and pull request titles and descriptions that follow the repository's own conventions |
| [writing-infrastructure-as-code](skills/writing-infrastructure-as-code/SKILL.md) | Safe authoring and change of infrastructure as code (Terraform/OpenTofu, Pulumi, CDK) and container images |

### `swe-docs`

Decision records, release docs, and agent context files (AGENTS.md / CLAUDE.md).

| Skill | What it is |
|---|---|
| [documenting-decisions](skills/documenting-decisions/SKILL.md) | Architecture decision records and keeping project docs in step with shipped code |
| [writing-agent-context-files](skills/writing-agent-context-files/SKILL.md) | Short, verified AGENTS.md and CLAUDE.md files that give coding agents a repo's non-obvious facts |

### `swe-agents`

Working with agents: dispatching subagents, session handoffs, authoring and evaluating skills.

| Skill | What it is |
|---|---|
| [authoring-skills](skills/authoring-skills/SKILL.md) | Test-first authoring and security vetting of Agent Skills (SKILL.md) |
| [dispatching-subagents](skills/dispatching-subagents/SKILL.md) ★ | Delegation discipline for handing work to subagents, parallel agents, or background workers |
| [handing-off-sessions](skills/handing-off-sessions/SKILL.md) | Session handoff documents that let a fresh agent or a later session resume work without the original conversation |

## Install

### Claude Code (plugin marketplace)

```bash
claude plugin marketplace add shreyansh-jain/agent-maxxing   # or a local path to this repo
claude plugin install swe-core@skills-map               # the default set
claude plugin install swe-architect@skills-map          # add categories as needed
```

Plugins: `swe-core`, `swe-all`, and one per category (`swe-lead`, `swe-product`, `swe-define`, `swe-architect`, `swe-plan`, `swe-build`, `swe-debug`, `swe-review`, `swe-operate`, `swe-ship`, `swe-docs`, `swe-agents`). Skills are namespaced by plugin, for example `/swe-core:assessing-complexity`.

### Any agent that reads SKILL.md

```bash
bash scripts/install.sh --plugin swe-core                           # ~/.agents/skills (Codex, Gemini CLI, Copilot, Cursor, OpenCode)
bash scripts/install.sh --plugin swe-core --target ~/.claude/skills # Claude Code, personal
bash scripts/install.sh --category architect --target .agents/skills
bash scripts/install.sh --skill debugging-systematically --dry-run
```

The installer symlinks by default (`--copy` copies instead) and never overwrites an existing skill that it didn't create.

### Don't install everything

All skill descriptions load into the agent's startup catalog. That catalog has a budget, and anything past it is silently dropped. Codex's budget, for example, is about 8,000 characters.

- `swe-core` fits comfortably at about 5.6k characters.
- `swe-all` (about 15.4k characters) may overflow alongside other installed skills.

Install `swe-core` plus the categories you actually use. Avoid pairing this repo with overlapping suites such as superpowers, gstack, or Matt Pocock's skills: they ship the same capabilities and compete for the same triggers.

## Design decisions

Each choice responds to a failure mode documented in the [research](research/03-directories-popularity-criticisms.md):

| Failure seen in the wild | What this repo does |
|---|---|
| Skills don't trigger (a skill was never invoked in 56% of cases in Vercel's evals) | Descriptions are a noun phrase plus "Use when …" with concrete triggers, and never summarize the workflow. Every skill ships `evals/triggers.json` with near-miss negatives |
| Silent catalog overflow | Budgets: ≤500-character descriptions, a `swe-core` bundle under 8k, and a validator warning when any bundle exceeds 8k |
| Bloated skills (6–14k words) | Bodies of 600–1,100 words, with detail in `references/` loaded on demand |
| Overlapping suites fight | One skill per capability. Every skill names its siblings under **Not for:** |
| Agents rationalize past rules | Discipline skills carry an Iron Law, a rationalization table and red flags |
| Unverifiable claims ("done", "fixed") | `verifying-before-completion` is on every track; process steps end in checkable exit criteria |
| Skills that commit or deploy on their own | Every irreversible step (commit, push, merge, deploy, apply, delete) runs only when the user asks in that session |
| Non-portable frontmatter | Only the six spec keys; runtime-specific fields are rejected by the validator |
| No evals | Every skill ships ≥3 behavior evals (at least one pressure scenario) in skill-creator's schema |
| License and supply-chain risk | Upstreams are license-checked; copyleft sources are borrowed as ideas only; an overlap check keeps copying at 0–2.5% |

## Repository layout

```
skills/<name>/SKILL.md          entry point: frontmatter + body contract
skills/<name>/references/       detail loaded on demand
skills/<name>/scripts/          helpers (run via bash/python3)
skills/<name>/assets/           templates the skill fills in
skills/<name>/evals/            evals.json (behavior) + triggers.json (activation)
.claude-plugin/marketplace.json generated from metadata.category
scripts/validate_skills.py      enforces docs/SKILL-STANDARD.md
scripts/build_marketplace.py    regenerates the marketplace (--check in CI)
scripts/build_notices.py        regenerates THIRD_PARTY_NOTICES.md from metadata.sources (--check in CI)
scripts/install.sh              cross-runtime installer
templates/skill/                starting point for a new skill
.github/workflows/validate.yml  runs all checks on every PR
```

Adding a skill takes a directory, a `category`, and `sources`. The generators handle the plugins and credits. See [SKILL-STANDARD.md § 7](docs/SKILL-STANDARD.md#7-adding-a-skill).

## Status

Every skill is **v0.1.0**. The evals are written but have not been run yet. The standard promotes a skill to v1.0.0 once its evals beat a no-skill baseline. Run them with Anthropic's [skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator), which does with-skill vs baseline runs, blind comparison, and description optimization.

Two reference files were written from general knowledge and should be checked against primary docs before you rely on them:
- `migrating-databases-safely/references/lock-safety.md` (Postgres and MySQL lock behavior per version);
- `estimating-capacity/references/numbers.md` (latency orders of magnitude).

## Credits

These skills stand on the work of the people and teams below. Every skill records its exact upstream skills in `metadata.sources`, and **[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)** lists each source's commit, license and copyright, and which skills use it.

| Source | License | What it contributed |
|---|---|---|
| [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) (Addy Osmani) | MIT | Full-lifecycle structure, rationalization tables, doubt- and source-driven development, observability, shipping |
| [mattpocock/skills](https://github.com/mattpocock/skills) (Matt Pocock) | MIT | Feedback-loop debugging, design-tree interviews, seams-first TDD, two-axis review, deep-module vocabulary |
| [obra/superpowers](https://github.com/obra/superpowers) (Jesse Vincent) | MIT | Iron Laws, verification gates, plans, subagent-driven development, worktrees, TDD for skills |
| [garrytan/gstack](https://github.com/garrytan/gstack) (Garry Tan) | MIT | Scope-drift review, specialist checklists, eng-manager cognitive patterns, ship and canary flows, security audits |
| [wshobson/agents](https://github.com/wshobson/agents) (Seth Hobson) | MIT | Architecture, resilience, data, observability, incident and infrastructure pattern references |
| [getsentry/skills](https://github.com/getsentry/skills) (Sentry) | Apache-2.0 | Confidence-filtered review, PR cover notes, AGENTS.md sizing, skill scanning, CI iteration |
| [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official), [anthropics/skills](https://github.com/anthropics/skills) (Anthropic) | Apache-2.0 | Confidence-scored parallel review, code explorers, skill-creator evals, webapp testing |
| [openai/skills](https://github.com/openai/skills) (OpenAI) | Apache-2.0 | CI log triage, threat modeling, goal definition |
| [supabase/agent-skills](https://github.com/supabase/agent-skills), [addyosmani/web-quality-skills](https://github.com/addyosmani/web-quality-skills), [LukasNiessen/terrashark](https://github.com/LukasNiessen/terrashark), [levnikolaevich/claude-code-skills](https://github.com/levnikolaevich/claude-code-skills), [muratcankoylan/Agent-Skills-for-Context-Engineering](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering) | MIT | Postgres practice, WCAG audits, IaC failure modes, test strategy, LLM evaluation |
| [trailofbits/skills](https://github.com/trailofbits/skills), [hashicorp/agent-skills](https://github.com/hashicorp/agent-skills), [antonbabenko/terraform-skill](https://github.com/antonbabenko/terraform-skill), [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills), [NeoLabHQ/context-engineering-kit](https://github.com/NeoLabHQ/context-engineering-kit) | CC-BY-SA / MPL / custom / none / GPL | Ideas only (no text): variant analysis, depth scaling, IaC risk categories, UI guidelines, rubric-first judging |

### Independence and trademarks

skills-map is an independent, personal project. It is not affiliated with, sponsored by, or endorsed by any of the people or companies named in this repository, and listing a source does not imply that its authors endorse this work.

Claude and Anthropic are trademarks of Anthropic, PBC. OpenAI, Codex, GitHub, Copilot, Gemini, Cursor, Vercel, Sentry and all other product and company names are trademarks of their respective owners. They appear here only to identify compatible tools and credit sources.

## License

[Apache-2.0](LICENSE). Upstream license texts are in [licenses/](licenses/).
