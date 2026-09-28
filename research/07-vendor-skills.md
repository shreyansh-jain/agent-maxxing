# Vendor / company skill repos (2026-09-28)

SPDX ids were read from each repo's actual LICENSE file. "none" means there is no root LICENSE file, which defaults to all rights reserved even if the README says otherwise.

| Repo | Stars | SPDX | Skills | Engineering highlights |
|---|---|---|---|---|
| https://github.com/vercel-labs/agent-skills | 31.6k | none (README says MIT) | 9 | react-best-practices, composition-patterns, web-design-guidelines, react-native, view-transitions, deploy, optimize, writing-guidelines |
| https://github.com/openai/skills | 27.7k | per skill (mostly Apache-2.0) | 44 | gh-fix-ci, gh-address-comments, yeet, security-threat-model, security-best-practices, security-ownership-map, playwright, deployers |
| https://github.com/huggingface/skills | 11.1k | Apache-2.0 | 26 | hf-cli, trainers, evals, spaces, local models |
| https://github.com/trailofbits/skills | 7.3k | CC-BY-SA-4.0 | ~85 | differential-review, fp-check, variant-analysis, sharp-edges, property-based-testing, mutation-testing, fuzzing, codeql/semgrep, supply-chain-risk-auditor, agentic-actions-auditor |
| https://github.com/remotion-dev/skills | 4.7k | none | 12 | video |
| https://github.com/google-gemini/gemini-skills | 4.2k | Apache-2.0 | 3 | gemini-api-dev |
| https://github.com/microsoft/skills | 3.1k | MIT | 203 | Azure SDKs, azure-diagnostics, kql, wiki-* (codebase wikis/onboarding) |
| https://github.com/cloudflare/skills | 2.9k | Apache-2.0 | 14 | workers-best-practices, wrangler, durable-objects, agents-sdk, web-perf |
| https://github.com/supabase/agent-skills | 2.7k | MIT | 2 | supabase-postgres-best-practices |
| https://github.com/expo/skills | 2.6k | MIT | 25 | expo-overview router, expo-upgrade, native UI |
| https://github.com/stripe/ai | 1.8k | MIT | 10 | stripe-best-practices, upgrade-stripe |
| https://github.com/langchain-ai/langchain-skills | 1.3k | MIT | 24 | langgraph, eval-engineering |
| https://github.com/getsentry/skills | 1.0k | Apache-2.0 | 27 | code-review, find-bugs, security-review, gha-security-review, django-perf-review, iterate-pr, commit, pr-writer, agents-md, skill-writer, skill-scanner |
| https://github.com/awslabs/agent-plugins | 904 | Apache-2.0 | 34 | lambda, serverless, step-functions, architecture diagrams |
| https://github.com/hashicorp/agent-skills | 877 | **MPL-2.0** | 20 | terraform-style-guide, terraform-test, refactor-module, provider dev |
| https://github.com/dbt-labs/dbt-agent-skills | 727 | Apache-2.0 | 16 | unit tests, troubleshooting, upgrades |
| https://github.com/elastic/agent-skills | 589 | Apache-2.0 | 25 | esql, query optimization, sre-triage |
| https://github.com/Shopify/Shopify-AI-Toolkit | 578 | MIT | 23 | admin GraphQL, functions, app-store review |
| https://github.com/docker/skills | 362 | Apache-2.0 | 11 | build strategies, compose, destructive guardrails |
| https://github.com/databricks/databricks-agent-skills | 331 | custom (not OSS) | 34 | — |
| https://github.com/semgrep/skills | 315 | Semgrep Rules License (not OSI) | 3 | semgrep, code-security, llm-security |
| https://github.com/grafana/skills | 275 | Apache-2.0 | ~55 | promql, k6, cardinality, opentelemetry |
| https://github.com/datadog-labs/agent-skills | 174 | MIT | ~45 | apm, logs, monitors, triage-flaky-test, unblock-pr |
| https://github.com/redis/agent-skills | 158 | MIT | 8 | core, connections, security |
| https://github.com/mongodb/agent-skills | 187 | Apache-2.0 | 8 | schema design, query optimizer |
| https://github.com/neondatabase/agent-skills | 95 | Apache-2.0 | 8 | postgres branches |
| https://github.com/pulumi/agent-skills | 70 | Apache-2.0 | 17 | best practices, tf-to-pulumi |
| https://github.com/prisma/skills | 65 | MIT | 9 | upgrade-v7, client API |
| https://github.com/get-convex/agent-skills | 62 | Apache-2.0 | 33 | authz, migrate-rehearse, deploy-guard |
| https://github.com/PostHog/skills | 71 | MIT | 331 | instrumentation, CI failures, stale feature flags |
| https://github.com/microsoft/playwright-cli | 13.6k | Apache-2.0 | 1 | playwright-cli |
| https://github.com/timescale/pg-aiguide | 1.85k | Apache-2.0 | 10 | postgres table design, migrations |
| https://github.com/alibaba/open-code-review | 42k | Apache-2.0 | 2 | open-code-review |
| https://github.com/snyk/studio-recipes | ? | Apache-2.0 | 8 | snyk-fix, dependency health, iac, sbom |
| https://github.com/temporalio/skill-temporal-developer | 222 | MIT | 1 | temporal |
| better-auth/skills, clerk/skills, JetBrains/skills, figma/mcp-server-guide | — | none | — | legally unclear |

No official Linear skill repo was found; `openai/skills/.curated/linear` is the closest. `snyk/agent-skills` does not exist; Snyk's skills live in `snyk/studio-recipes`.

## 15 most valuable vendor skills

1. vercel react-best-practices
2. vercel web-design-guidelines
3. trailofbits differential-review
4. trailofbits property-based-testing
5. trailofbits variant-analysis and fp-check
6. getsentry iterate-pr
7. getsentry find-bugs and code-review
8. getsentry gha-security-review
9. openai gh-fix-ci
10. openai security-threat-model
11. supabase postgres-best-practices
12. hashicorp terraform-style-guide and terraform-test
13. docker build-strategies and destructive-guardrails
14. microsoft playwright-cli
15. cloudflare workers-best-practices and web-perf

Runners-up: sentry claude-settings-audit and agents-md, upgrade-stripe, prisma-upgrade-v7, expo-upgrade, mongodb-schema-design, snyk-fix, datadog triage-flaky-test, convex-deploy-guard.
