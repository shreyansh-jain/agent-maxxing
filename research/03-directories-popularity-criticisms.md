# Directories, popularity, themes, gaps, criticisms

Researched 2026-09-28. Counts were read through a summarizing fetch, so treat them as approximate. `[U]` = unverified or single-source.

## Directories

| Directory | What | Size |
|---|---|---|
| skills.sh | Vercel leaderboard ranked by `npx skills add` installs across 20+ agents | claims 1.43M skills; #1 find-skills 3.6M installs |
| vercel-labs/skills | the `npx skills` CLI, de-facto package manager | ~20k stars [U] |
| SkillsMP (skillsmp.com) | crawl of every public SKILL.md on GitHub | 425k–3M (conflicting) |
| claude-plugins.dev/skills | auto-indexed registry with download counts | — |
| ComposioHQ/awesome-claude-skills | curated list | 75.8k stars |
| VoltAgent/awesome-agent-skills | curated, grouped by vendor | 35k stars, 1,497+ skills |
| travisvn/awesome-claude-skills | curated + security notes | 15.2k stars |
| sickn33/antigravity-awesome-skills | mega-bundle | 2,445+ skills [U stars] |
| Agensi, claudemarketplaces.com, mcpmarket.com, SupaSkills | smaller marketplaces | — |

Large repos acting as directories: mattpocock/skills (270.8k★), obra/superpowers (292.2k★), anthropics/skills (178.7k★), addyosmani/agent-skills (99.5k★).

## Top engineering skills (installs from skills.sh)

- **mattpocock/skills** — grill-me (1.2M), domain-modeling (710k), codebase-design (687k), diagnosing-bugs (673k), code-review (626k; standards + spec axes), implement (624k; TDD + review), wayfinder (576k; multi-session planning), to-spec (572k), research (571k), to-tickets (562k), resolving-merge-conflicts (549k), git-guardrails-claude-code (405k), setup-pre-commit (396k), handoff, tdd, triage, improve-codebase-architecture.
- **obra/superpowers** — systematic-debugging, test-driven-development, verification-before-completion, brainstorming, writing-plans, executing-plans, subagent-driven-development, using-git-worktrees, requesting/receiving-code-review, writing-skills.
- **addyosmani/agent-skills** — spec-driven-development, planning-and-task-breakdown, incremental-implementation, api-and-interface-design, debugging-and-error-recovery, code-review-and-quality (5 axes, severity labels), security-and-hardening, performance-optimization, git-workflow-and-versioning, ci-cd-and-automation, deprecation-and-migration, documentation-and-adrs, observability-and-instrumentation, shipping-and-launch.
- **Vercel / Anthropic** — vercel-react-best-practices (749k), web-design-guidelines (674k), agent-browser (960k), frontend-design (930k), webapp-testing, mcp-builder, skill-creator (evals/benchmarks).
- **Others** — forrestchang/andrej-karpathy-skills [U stars], trailofbits/skills (differential-review, supply-chain-risk-auditor, mutation-testing, property-based-testing, CodeQL/Semgrep), garrytan/gstack (/review /ship /qa /plan-eng-review /investigate /cso), wshobson/agents (architecture-patterns, api-design-principles), caveman (542k; output token cut), mksglu/context-mode, Microsoft azure-* skills, prisma-database-setup [U].

## Recurring themes

Near-universal: planning before code, TDD, systematic debugging, code review (giving + receiving), verification before "done", subagent orchestration, git hygiene, session handoff.
Common: frontend/UI + a11y, React/web perf, browser/E2E testing, security audit, API design/architecture, skill authoring, commit/PR/changelog writing.
Narrow: observability, CI/CD, deprecation/migration, ADRs, dependency upgrades, DB schema.

## Gaps (inferred)

Incident response/on-call; production DB migrations (expand-contract, backfills, locks); dependency/framework upgrades at scale; vendor-neutral observability-driven debugging; backend/DB performance and load testing; flaky-test and slow-CI triage; legacy codebase onboarding + characterization tests; JVM/Go/Rust/C++ coverage; feature-flag cleanup, release/rollback; evals proving skills work.

## Criticisms and lessons

- **Skills often don't trigger.** Vercel evals: skill never invoked in 56% of cases; a compressed AGENTS.md docs index hit 100% (https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals). Put passive knowledge in always-loaded context; use skills for procedures with precise "when" descriptions.
- **Description budget overflow.** All names + descriptions share a startup budget (~15k chars [U]); overflow drops silently (https://dev.to/lizechengnet/why-claude-code-skills-dont-trigger-and-how-to-fix-them-in-2026-o7h).
- **Token bloat / context rot.** Keep SKILL.md lean (~2–3k tokens), most important guidance first, detail in references (https://www.mindstudio.ai/blog/context-rot-claude-code-skills-bloated-files).
- **Overlap and conflict.** Superpowers, Pocock, Osmani, gstack all ship TDD/debug/review and compete for triggers. Mega-bundles make behavior unpredictable.
- **Supply-chain risk.** 26.1% of 31,132 skills vulnerable, 5.2% likely malicious (https://arxiv.org/html/2602.06547v1); Snyk ToxicSkills found prompt injection in 36% (https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub/). Audit before installing.
- **No evals.** "Skills Without Evals Are Just Markdown and Hope" (https://dev.to/danielsogl/skills-without-evals-are-just-markdown-and-hope-3a71).

Sources: https://skills.sh · https://www.firecrawl.dev/blog/best-claude-code-skills · https://composio.dev/content/top-claude-skills · https://www.agensi.io/learn/best-claude-code-skills-2026 · https://simonwillison.net/tags/skills/ · https://vercel.com/changelog/introducing-skills-the-open-agent-skills-ecosystem
