# Skill standards (verified 2026-09-28)

## Agent Skills open spec — https://agentskills.io/specification

Layout: `<name>/SKILL.md` (required) + optional `scripts/`, `references/`, `assets/`. Other files allowed.

| Field | Req | Constraint |
|---|---|---|
| `name` | yes | 1–64 chars, `^[a-z0-9]+(-[a-z0-9]+)*$` (no leading/trailing/double hyphen), must equal parent dir |
| `description` | yes | 1–1024 chars; what it does + when to use |
| `license` | no | SPDX name or bundled file reference |
| `compatibility` | no | 1–500 chars; environment requirements |
| `metadata` | no | string→string map |
| `allowed-tools` | no | space-separated, experimental |

Progressive disclosure: metadata ~100 tokens at startup; body on activation (<5k tokens, <500 lines); references one level deep, loaded on demand.

Validator: `skills-ref validate <dir>` (github.com/agentskills/agentskills/tree/main/skills-ref) — rejects any key outside the six fields. Demo-grade per its README.

Client guidance: scan `<project>/.agents/skills/` and `~/.agents/skills/`; project overrides user.

## Anthropic authoring rules — https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices

- `name` must not contain `anthropic` or `claude`, nor XML tags.
- Description in third person; says what + when.
- Gerund names preferred (`processing-pdfs`); avoid `helper`, `utils`, `tools`.
- Body <500 lines; TOC for references >100 lines; forward slashes; MCP tools as `Server:tool`.
- Scripts: handle errors ("solve, don't defer"), no magic constants, say whether to execute or read.
- ≥3 evals per skill; test on Haiku, Sonnet, Opus; no time-sensitive info.

## Claude Code extensions — https://code.claude.com/docs/en/skills

`when_to_use`, `argument-hint`, `arguments`, `disable-model-invocation`, `user-invocable`, `allowed-tools`, `disallowed-tools`, `model`, `effort`, `context: fork`, `agent`, `background`, `hooks`, `paths`, `shell`. Substitutions: `$ARGUMENTS`, `${CLAUDE_SKILL_DIR}`, `${CLAUDE_PROJECT_DIR}`, `${CLAUDE_PLUGIN_ROOT}`, etc.

**Portability trap:** claude.ai uploads and the Skills API hard-fail on any key outside the six spec fields.

Locations: `~/.claude/skills/`, `.claude/skills/`, `<plugin>/skills/<name>/` (namespaced `plugin:skill`).

## Plugins & marketplaces — https://code.claude.com/docs/en/plugins-reference

- `.claude-plugin/plugin.json`: only `name` required (kebab-case). Optional `version`, `description`, `author{name}`, `homepage`, `repository`, `license`, `keywords`, component paths.
- Default plugin layout: `skills/<name>/SKILL.md`, `agents/`, `hooks/hooks.json`, `.mcp.json`. A root `CLAUDE.md` is not loaded.
- `.claude-plugin/marketplace.json`: required `name`, `owner{name}`, `plugins[]` (each `name` + `source`). Relative sources resolve from the marketplace root; `..` is rejected.
- Reserved marketplace names include `agent-skills`, `anthropic-agent-skills`, `claude-plugins-official`, `claude-community`.
- Validate: `claude plugin validate [--strict]`. Install: `claude plugin marketplace add owner/repo` then `claude plugin install <plugin>@<marketplace>`.

## Cross-runtime paths

| Client | Project | User |
|---|---|---|
| Claude Code | `.claude/skills` | `~/.claude/skills` |
| Codex | `.agents/skills` | `~/.agents/skills` |
| Gemini CLI | `.gemini/skills`, `.agents/skills` | `~/.gemini/skills`, `~/.agents/skills` |
| Copilot / VS Code | `.github/skills`, `.claude/skills`, `.agents/skills` | `~/.copilot/skills`, `~/.claude/skills`, `~/.agents/skills` |
| Cursor | `.agents/skills`, `.cursor/skills` (+ reads `.claude`, `.codex`) | same under `~` |
| OpenCode | `.opencode/skills`, `.claude/skills`, `.agents/skills` | `~/.config/opencode/skills`, `~/.claude/skills`, `~/.agents/skills` |

## anthropics/skills

19 skills; `template/SKILL.md` is minimal; `spec/` points to agentskills.io. Marketplace `anthropic-agent-skills` uses `source: "./"`, `strict: false`, explicit `skills` arrays. Most skills Apache-2.0; docx/pdf/pptx/xlsx source-available.

## Portability rules adopted for this repo

1. Only the six spec fields in `SKILL.md` frontmatter.
2. `name` == dir, spec regex, ≤64, no `claude`/`anthropic`.
3. Third-person description ≤1024 chars (aim ≤500), trigger-focused.
4. Body <500 lines / <5k tokens; detail in `references/`.
5. Distribute as a Claude Code plugin marketplace *and* a plain `skills/` tree that `npx skills add` / symlinks into `.agents/skills` can consume.
