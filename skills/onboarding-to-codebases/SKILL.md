---
name: onboarding-to-codebases
description: Structured orientation in an unfamiliar repository, service or subsystem, ending in an evidence-backed map. Use when starting work in a codebase for the first time, when asked how a feature or flow works end to end, before planning a change in code nobody on hand understands, or when the user asks for an architecture overview or a walkthrough.
license: Apache-2.0
metadata:
  version: "0.1.0"
  category: "build"
  sources: "anthropics/claude-plugins-official feature-dev code-explorer (Apache-2.0); mattpocock/skills improve-codebase-architecture (MIT); addyosmani/agent-skills context-engineering (MIT)"
---

# Onboarding to Codebases

Build understanding, not verdicts: map how the code actually works, with every claim tied to a file and line, before you judge, change, or plan it.

## When to use

- First session in a repo, service or subsystem
- "How does X work?", "where does Y happen?", "walk me through the flow from request to DB"
- Before planning a change in an area no one present understands
- The user wants an architecture overview, or a map for new team members

**Not for:** finding the cause of a specific failure (use `debugging-systematically`); changing untested code safely (use `refactoring-legacy-code`); a security or quality audit (use `auditing-security` or `reviewing-code`); writing the project's agent context file (use `writing-agent-context-files`, which can use this skill's map as input).

## The rule

```
NO VERDICTS UNTIL THE MAP IS COMPLETE AND EVERY CLAIM CITES FILE:LINE
```

Violating the letter of the rule is violating the spirit of the rule. While mapping, don't name bugs, propose refactors, or score quality: a verdict formed early anchors everything after it. If something alarms you, put it under **Questions** and keep mapping.

## Process

1. **Frame the question.** Write down what the user needs to understand and why (e.g. "how an order becomes an invoice, so we can add refunds"). A broad "understand the repo" still gets a stated depth: a one-page overview, or a deep trace of one flow.
   Exit: the question and the depth are written down.

2. **Read the map the repo already provides.** Read the README, CONTRIBUTING, AGENTS.md or CLAUDE.md, `docs/` and ADRs, then the build and dependency manifests, CI workflows (these list the real commands) and deployment config. Read `git log --oneline -50` and find the hot spots with `git log --format= --name-only | sort | uniq -c | sort -rn | head -20`.
   Exit: you know the language, framework, entry commands, main directories, and where recent change is concentrated.

3. **Find the entry points.** Locate the routes, CLI commands, queue consumers, cron jobs, UI screens and exported package APIs that relate to the question. Search for route tables, `main` functions and handler registrations.
   Exit: entry points listed with file:line.

4. **Trace one path end to end.** Follow a single real request or event from an entry point through each layer to storage and back. At each hop, record the function, the data shape, the side effects (DB writes, network calls, events), and the error handling. Read the actual code, not just file names. For large repos, give independent paths to separate subagents and ask each for a file:line trace.
   Exit: a numbered trace where every step has a file:line reference.

5. **Name the moving parts.** List the key modules and what each owns, the main data types, cross-cutting concerns (auth, config, logging, caching, transactions), and external dependencies. Record the project's own vocabulary as you go, and reuse it in the map.
   Exit: a component list where every responsibility is backed by a file reference.

6. **Check the map.** Choose two claims in your map and confirm them independently: run the code path, a single relevant test, or `--help`, or find a second place in the code that confirms each one. Mark any claim you could not confirm as **inferred**.
   Exit: each claim is either verified or marked inferred.

7. **Only now, observations.** If the user wants an opinion, give it after the map, clearly labeled, with evidence for each point.

## Output

```
Question: <what we set out to understand>
Stack & commands: <language/framework; build, test (single-file), run commands>
Entry points: <file:line list>
Trace: <1. file:line: what happens, data shape, side effects … n.>
Components: <module: responsibility (file refs)>
Glossary: <project terms and what they mean in code>
Questions / inferred: <open questions, claims not verified>
Observations (optional, after the map): <labeled opinions with evidence>
Essential files to read next: <5–10 paths>
```

Save the map where the repo keeps docs, if the user wants it kept. Otherwise leave it in the reply.

## Red flags

- Describing a module from its file name without having opened it
- "This is badly designed" before the trace is complete
- A trace step with no file:line
- Reading only the directory tree and the README
- Claims about runtime behavior that no test, run or second source confirms, and that aren't marked inferred
