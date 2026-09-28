---
name: upgrading-dependencies
description: Safe, incremental dependency and framework upgrade practice, from a single package to a monorepo-wide major bump. Use when bumping a library, framework, language runtime or toolchain version, handling Dependabot or Renovate PRs, fixing a deprecated or end-of-life dependency, resolving a vulnerable-dependency advisory, or running codemods for a breaking release.
license: Apache-2.0
metadata:
  version: "0.1.0"
  category: "ship"
  sources: "wshobson/agents dependency-upgrade, react-modernization (MIT); addyosmani/agent-skills deprecation-and-migration, source-driven-development (MIT)"
---

# Upgrading Dependencies

Upgrade one breaking boundary at a time, reading the maintainers' migration notes rather than recalling them. Keep every step green before starting the next.

## When to use

- Bumping a package, framework, runtime (Node, Python, JDK, Go) or build tool
- Reviewing or merging Dependabot / Renovate PRs
- A security advisory requires a version change
- A dependency is deprecated, end-of-life or unmaintained
- A major release ships codemods or a migration guide

**Not for:** a database schema change that comes with an ORM upgrade (use `migrating-databases-safely` for the schema part); CI that broke because an unpinned tool drifted (use `fixing-ci-failures`); choosing a library for new work (use `grounding-in-official-docs`).

## The rule

```
ONE MAJOR VERSION OF ONE DEPENDENCY PER STEP, GREEN BEFORE THE NEXT
```

Violating the letter of the rule is violating the spirit of the rule. A combined bump that breaks can't be bisected; a sequence of green steps can.

## Process

1. **Inventory.** Record the current and target versions and why the upgrade is happening (security, EOL, a needed feature). Record the package's role, whether it is direct or transitive (`npm ls <pkg>`, `pip show`, `go mod why`, `mvn dependency:tree`), and which packages have peer or compatibility constraints on it.
   Exit: a short table of package, from, to, reason, and the dependencies it constrains.

2. **Read the maintainers' notes for every version you cross.** Read the CHANGELOG, release notes and migration guide for *each* major version between current and target, fetched from the project's repo or docs. Don't rely on memory, because breaking changes are exactly what training data gets wrong. Record the breaking changes that apply to this codebase, and grep for each affected API: `rg "componentWillMount|findDOMNode"`.
   Exit: a list of breaking changes, each with its hit count in this repo (0 is a valid count).

3. **Order the path.** Upgrade the lowest layer first: runtime, then build tooling, then frameworks, then libraries. Within one package, go one major version at a time. When a major release ships a "bridge" minor that deprecates before it removes, land that minor first and clear its deprecation warnings.
   Exit: a numbered sequence of steps, each small enough to review and to revert on its own.

4. **Establish a green baseline.** Before changing anything, run the type check, the build, and the tests most related to the affected code. Record the results. If the baseline is already red, say so and stop: you can't judge an upgrade against a broken baseline.

5. **Execute one step.** Bump the version and regenerate the lockfile with the project's own tool (`npm install`, `pnpm install`, `uv lock`, `poetry lock`, `go get`). Never edit the lockfile by hand. Run the official codemod if one exists (`npx @next/codemod`, `npx react-codemod`, `pyupgrade`, `go fix`, OpenRewrite), then read its diff. Fix whatever breaking changes remain by hand.
   Exit: the type check, build and related tests are back to the baseline, and there are no new deprecation warnings you haven't explained.

6. **Check the runtime, not only the build.** Start the app or run a smoke path that exercises the upgraded library at runtime. Many breaking changes are behavioural and don't show up at compile time: defaults, serialization, timezones, peer-resolution changes.
   Exit: the smoke path works, shown by output or a screenshot.

7. **Record and repeat.** Keep each step as a separate commit if the user has asked you to commit, otherwise as a separate reviewable change. Its message should name the version jump and the breaking changes handled. Then do the next step.

For **batches of minor and patch updates** (Dependabot or Renovate), group them by risk. Dev-only tooling can go together. Runtime libraries go individually, or in small groups sharing an owner. Read the release notes for anything that has had a security fix or a behaviour change.

## Output

```
Upgrade: <pkg> <from> → <to>   Reason: <security/EOL/feature>
Path: 1) <step>  2) <step> ...
Breaking changes handled: <change> → <files touched> (codemod | manual)
Verified: typecheck ✓ build ✓ tests <scope> ✓ runtime smoke <how> ✓
Deferred: <deprecations or follow-ups, with reason>
```

## Rationalizations

| Excuse | Reality |
|---|---|
| "Just bump everything to latest at once" | When it breaks, you can't tell which bump did it. One boundary per step. |
| "I know what changed in v5" | Read the migration guide anyway. Recalled breaking changes are the most common source of wrong upgrade code. |
| "Tests pass, so it works" | Behavioural changes such as defaults, serialization and timezones often have no tests. Run the smoke path. |
| "Add --legacy-peer-deps / --force and move on" | That hides a real incompatibility until runtime. Resolve the peer constraint. |
| "Pin it with an override and skip the upgrade" | An override is a deliberate, documented exception with an owner, not a fix. |

## Red flags

- Several major bumps in one change
- Lockfile edited by hand, or deleted and regenerated wholesale
- Breaking changes described from memory, with no link to the release notes
- `--force`, `--legacy-peer-deps`, `resolutions` or `overrides` added without explanation
- New deprecation warnings dismissed as noise
- Upgrading while the baseline is already red
