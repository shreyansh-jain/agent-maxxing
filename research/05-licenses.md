# Licenses of source repos (checked 2026-09-28)

Read from shallow clones and cross-checked against the GitHub license API. This is a reading of the licenses, not legal advice.

| Repo | SPDX | Copyright line | Copy + adapt? | Obligation |
|---|---|---|---|---|
| obra/superpowers | MIT | `Copyright (c) 2025 Jesse Vincent` | yes | keep notice |
| garrytan/gstack | MIT (+ some Apache-2.0-derived design files listed in its NOTICE.md) | `Copyright (c) 2026 Garry Tan` | yes | keep notice; Apache files need their own notice |
| mattpocock/skills | MIT | `Copyright (c) 2026 Matt Pocock` | yes | keep notice |
| wshobson/agents | MIT | `Copyright (c) 2024 Seth Hobson` | yes | keep notice |
| microsoft/skills | MIT | `Copyright (c) Microsoft Corporation.` | yes | keep notice |
| github/awesome-copilot | MIT root, per-skill overrides | `Copyright GitHub, Inc.` (root) | check each folder | per skill |
| vercel-labs/agent-skills | MIT per README (no LICENSE file) | none stated | yes, low risk | credit Vercel + MIT text |
| anthropics/skills | per skill `LICENSE.txt` | Apache files are template text | Apache-2.0 skills yes (skill-creator, mcp-builder, webapp-testing, frontend-design, …) | Apache §4: include license, mark changes |
| anthropics/skills docx/pdf/pptx/xlsx | proprietary | © Anthropic, PBC | **NO** | — |
| anthropics/skills doc-coauthoring | none found | — | **avoid** | — |
| anthropics/claude-plugins-official | Apache-2.0 | template | yes (code-review, feature-dev, pr-review-toolkit, commit-commands, plugin-dev, skill-creator…) | Apache §4 |
| claude-plugins-official/claude-security | proprietary | — | **NO** | — |
| trailofbits/skills | CC-BY-SA-4.0 | "Made by Trail of Bits" | yes, **ShareAlike** | adaptations must stay CC BY-SA 4.0 |
| openai/skills | per skill: Apache-2.0 (31), MIT (notion-*, vercel-deploy) | template / holder per file | yes except figma* | per skill |
| openai/skills figma* | Figma Developer Terms | — | **NO** | — |
| huggingface/skills | Apache-2.0 | template | yes | Apache §4 |

## Policy adopted for this repo

- Repo license: **Apache-2.0** (compatible with MIT and Apache inputs).
- `THIRD_PARTY_NOTICES.md` lists each upstream: URL, SPDX, exact copyright line, which of our skills drew from it, and a pointer to `licenses/<file>`.
- Every adapted skill records its sources in `metadata` (`upstream`, `upstream-license`) and states "Adapted from …" in the README credits table.
- Skills here are **rewritten syntheses** (ideas combined from several sources, new wording), not verbatim copies. Where text is carried over closely, the upstream notice travels with it.
- **Not copied:** proprietary Anthropic document skills, claude-security, openai figma*, doc-coauthoring.
- **Trail of Bits (CC-BY-SA-4.0):** ideas only, reworded from scratch; no text adapted, so ShareAlike does not attach. If text is ever adapted, it goes under `skills-cc-by-sa/` with its own LICENSE.
