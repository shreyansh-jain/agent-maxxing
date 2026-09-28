# Community, individual and language-specific skill collections (2026-09-28)

Stars and SPDX come from the GitHub API. Skill counts are SKILL.md files found in shallow clones. `[U]` = not opened.

## Headline collections

| Repo | Stars | License | Skills | Standout |
|---|---|---|---|---|
| https://github.com/mattpocock/skills | 270.8k | MIT | 38 | Shared vocabulary (seam, depth, locality) across skills; diagnosing-bugs feedback-loop gate; tdd at agreed seams; wayfinder; to-tickets |
| https://github.com/addyosmani/agent-skills | 99.5k | MIT | 25 | Full lifecycle; doubt-driven (fresh-context adversary, max 3 cycles); source-driven (lockfile versions → official docs → cite) |
| https://github.com/addyosmani/web-quality-skills | 2.85k | MIT | 6 | core-web-vitals, performance, accessibility (WCAG 2.2), seo, audits grounded in Lighthouse |
| https://github.com/wshobson/agents | 40.0k | MIT | 183 | Widest stack coverage (Python, Go, Rust, TS, K8s, Terraform, CI, observability, CQRS/saga); reference patterns rather than process |
| https://github.com/obra/superpowers-skills | 748 | MIT | 31 | Older wiki: condition-based-waiting, testing-anti-patterns, when-stuck, problem-solving skills (stale since 2025-10) |
| https://github.com/obra/superpowers-lab | 429 | MIT | 4 | finding-duplicate-functions (catalog → cluster → same-intent), using-tmux-for-interactive-commands |
| https://github.com/Jeffallan/claude-skills | 11.7k | MIT | 67 | Per-stack persona skills (python-pro, golang-pro, rust-engineer, spring-boot, django, fastapi, k8s, terraform, sre…), spec-miner, legacy-modernizer |
| https://github.com/alirezarezvani/claude-skills | 26.7k | MIT | 846 | Large, mostly non-engineering; many copies of others' skills |
| https://github.com/jezweb/claude-skills | 1.0k | MIT | 63 | Cloudflare + React + Tailwind v4 scaffolders |
| https://github.com/NeoLabHQ/context-engineering-kit | 1.7k | **GPL-3.0** | ~100 | do-and-judge (meta-judge writes the rubric first), judge-with-debate, kaizen 5-whys |
| https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering | 18.0k | MIT | 23 | Context rot, compression, multi-agent patterns, LLM-as-judge evaluation |
| https://github.com/levnikolaevich/claude-code-skills | 565 | MIT | 31 | Evidence-gated lifecycle; persistence-auditor; test-suite-auditor; dependency-upgrader in reversible batches |
| https://github.com/davila7/claude-code-templates | 32.0k | MIT | 914 | Aggregator (for discovery only) |
| https://github.com/hesreallyhim/awesome-claude-code | 54.7k | **CC BY-NC-ND 4.0** | — | Curation only; not reusable |
| https://github.com/ykdojo/claude-code-tips | 10.2k | **All rights reserved** | 9 | gha, handoff, half-clone; not reusable |
| https://github.com/SawyerHood/dev-browser | 6.6k | MIT | 1 | Warm browser daemon, ARIA snapshots with refs |
| https://github.com/steipete/agent-scripts | 6.7k | MIT | 54 | Swift concurrency, SwiftUI perf audits, Instruments profiling, create-cli |
| https://github.com/K-Dense-AI/scientific-agent-skills | 46.9k | MIT | 166 | Science, not engineering |

## Viral single-purpose skills

| Repo | Stars | License | Technique |
|---|---|---|---|
| https://github.com/DietrichGebert/ponytail | 147k [U inflated?] | MIT | Laziest-working-solution ladder (does this need to exist → stdlib → native → one line); review variant lists what to delete |
| https://github.com/OthmanAdi/planning-with-files | 27.2k | MIT | Plan files on disk, re-injected by frontmatter hooks so they survive compaction |
| https://github.com/tt-a1i/archify | 73.0k | MIT | Architecture and sequence diagrams checked by a validator |
| https://github.com/Egonex-AI/Understand-Anything | 84.4k | MIT | Code knowledge graphs [U] |

## Language / framework packs

| Area | Repo | Stars | License | Notes |
|---|---|---|---|---|
| Go | https://github.com/samber/cc-skills-golang | 3.3k | MIT | 46 skills (concurrency, goroutine leaks, errors, perf, testing, library skills) |
| Go | https://github.com/cxuu/golang-skills | 164 | Apache-2.0 | Google/Uber style distilled |
| Terraform | https://github.com/antonbabenko/terraform-skill | 2.4k | custom | Response contract: assumptions, risk category, validation, rollback; `plan -destroy` gate |
| Terraform | https://github.com/LukasNiessen/terrashark | 718 | MIT | Diagnose failure mode first, then load that mode's reference |
| Swift | https://github.com/twostraws/SwiftUI-Agent-Skill | 4.9k | MIT | 9-step review, one reference per step; "report only genuine problems" |
| Swift | https://github.com/AvdLee/SwiftUI-Agent-Skill | 3.6k | MIT | 34 references; view as invalidation boundary |
| Swift | https://github.com/dpearson2699/swift-ios-skills | 1.2k | **PolyForm Perimeter** | Restrictive |
| Apple | https://github.com/rshankras/claude-code-apple-skills | 769 | MIT | 183 skills |
| Android | https://github.com/skydoves/compose-performance-skills | 509 | Apache-2.0 | Compose recomposition and stability |
| Android | https://github.com/new-silvermoon/awesome-android-agent-skills | 970 | Apache-2.0 | |
| Java/Spring | https://github.com/decebals/claude-code-java | 747 | MIT | 18 skills |
| Java/Spring | https://github.com/sivaprasadreddy/sivalabs-agent-skills | 184 | MIT | spring-modulith-verifier, jspecify, java-code-review |
| GraphQL | https://github.com/apollographql/skills | 115 | MIT | 14 vendor skills |
| Python/Django/FastAPI | — | — | — | No strong standalone pack; use wshobson python-* and Jeffallan django/fastapi |
| Rust/TypeScript | — | — | — | No pack above ~1k stars; use wshobson and Jeffallan |

## Reuse caveats

- Not reusable: ykdojo (all rights reserved), hesreallyhim (NC-ND), dpearson2699 (PolyForm), zircote (no license).
- Copyleft: NeoLabHQ, maxrave-dev/kotlin-footguns (GPL-3.0). Borrow ideas only.
- Aggregators (alirezarezvani, davila7) re-host others' work; trace a skill to its origin before citing it.
