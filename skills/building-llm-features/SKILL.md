---
name: building-llm-features
description: Engineering discipline for product features that call an LLM: evals, prompts, structured output, tools, injection defense, cost. Use when adding or changing an LLM-powered feature, chatbot, agent, RAG pipeline, summarizer or classifier, or when one gives bad or unsafe output.
license: Apache-2.0
metadata:
  version: "0.1.0"
  category: "build"
  sources: "anthropics/skills mcp-builder (Apache-2.0); muratcankoylan/Agent-Skills-for-Context-Engineering evaluation (MIT); addyosmani/agent-skills source-driven-development (MIT); openai/skills define-goal (Apache-2.0)"
---

# Building LLM Features

A model call is a non-deterministic dependency that returns untrusted text. Measure it with evals, constrain it with schemas, and never let its output act without a check.

## When to use

- Adding a feature that calls an LLM API: summarize, classify, extract, generate, chat, answer from documents (RAG), or act with tools (agents)
- Changing a prompt, model, provider, temperature, or retrieval setup
- An LLM feature hallucinates, leaks data, breaks its output format, gets slow or expensive, or follows instructions hidden in user content

**Not for:** building MCP servers or agent tool interfaces as an API design problem (use `designing-interfaces`); general threat modeling of the whole system (use `modeling-threats`); checking the provider's current API parameters and model names (use `grounding-in-official-docs`, which this skill requires).

## The rule

```
NO PROMPT OR MODEL CHANGE SHIPS WITHOUT AN EVAL RUN AGAINST THE PREVIOUS VERSION
```

Violating the letter of the rule is violating the spirit of the rule. "It looked better on three examples" is anecdote, not evidence.

## Process

1. **Write the eval set before the prompt.** Collect 20–50 real or realistic inputs: typical cases, edge cases, adversarial cases (injection attempts, empty input, other languages, very long input), and cases where the right answer is "I don't know" or a refusal. For each case, write the expected output, or the property a good output must have.
   Grade with the cheapest reliable method:
   - exact match or schema validity for structured output;
   - rule checks (contains the citation, under 100 words, no PII);
   - an LLM judge with a written rubric only for open-ended quality, calibrated against a few human-labeled cases.
   Exit: a runnable eval command that prints a score for each case and overall.

2. **Check current provider facts at run time.** Model identifiers, context limits, pricing, structured-output and tool-use parameters change often. Read the provider's current docs or SDK types rather than recalling them (**REQUIRED:** `grounding-in-official-docs`). Keep model id and parameters in configuration, not scattered through code.
   Exit: the model, parameters and SDK version are pinned in one config location, with the doc source noted.

3. **Treat prompts as code.** Store prompts in versioned files or constants, not inline string concatenation. Separate trusted instructions (the system prompt) from untrusted content (user input, retrieved documents, tool results), and wrap untrusted content in clear delimiters. Put stable content first so provider prompt caching can reuse it.
   Exit: the prompt is diffable, reviewed like code, and tagged with a version that is logged on every call.

4. **Constrain the output.** When code consumes the output, ask for structured output (JSON schema, tool or function call, or the provider's structured-output mode) and **validate it** with a schema library before use. On a validation failure, retry once with the error message, then fail safely. Never `eval`, execute, render as raw HTML, or use as SQL any model output without the same validation you would apply to user input.
   Exit: every consumer of model output goes through a validator, and failures degrade gracefully.

5. **Defend against prompt injection.** Assume any retrieved page, email, file or tool result can contain instructions. Defenses, in layers:
   - least-privilege tools (read-only by default, scoped to the current user's data);
   - allowlist the tools available for each feature;
   - never put secrets in the prompt;
   - require human confirmation for high-impact actions (send, pay, delete, change permissions);
   - keep untrusted content out of the instruction channel;
   - check outputs for data exfiltration patterns (URLs with query data, markdown images).
   No prompt wording fully prevents injection, so rely on privilege limits, not phrasing.
   Exit: the eval set contains injection cases, and the worst possible tool action is bounded and confirmed.

6. **Budget latency and cost.** Set targets (p95 latency, cost per request, tokens per request). Measure them in the eval run. Use the smallest model that passes the evals. Stream responses the user watches. Cache deterministic calls. Cap max output tokens. Set a timeout and a fallback for every call: a smaller model, a cached answer, or a non-LLM path with a clear message.
   Exit: the budgets are written down and measured, and a provider outage yields a defined degraded behavior.

7. **Observe in production.** For each call, log the prompt version, model, token counts, latency, validation result and a request id. Log content only if privacy rules allow it, redacted. Collect user feedback signals (thumbs, edits, retries). Feed real failures back into the eval set.
   Exit: a bad answer reported by a user can be traced to its prompt version and inputs, and becomes a new eval case.

8. **Compare before shipping.** Run the eval for the old and the new version on the same set. Ship only if the target cases improve and no category regresses beyond an agreed tolerance. Roll out behind a flag (`managing-feature-flags`) when user impact is uncertain.

## Output

```
Feature: <name> · model/config: <config key> · prompt: <file>@<version>
Evals: <n cases> (<typical/edge/adversarial/refusal>) · grader: <schema | rules | judge+rubric>
Result: old <score> → new <score>; regressions: <none | list>
Output contract: <schema> validated by <library>; on failure: <retry once → fallback>
Tools: <list, permissions>; human confirmation for: <actions>
Budgets: p95 <ms>, cost/request <$>, max tokens <n> · fallback: <behavior>
Logged per call: prompt version, model, tokens, latency, validation, request id (content: <redacted | not logged>)
```

## Rationalizations

| Excuse | Reality |
|---|---|
| "The new prompt is obviously better, I tried a few" | Prompt changes fix three cases and break five you didn't look at. Run the evals. |
| "The model returns JSON reliably" | Until it doesn't under load, a model update, or odd input. Validate every time. |
| "We told it in the system prompt not to follow instructions in documents" | Injection defeats wording. Limit what the model can do. |
| "Evals can come after launch" | Then you cannot tell whether the next change helped or hurt. Twenty cases take an hour. |
| "Use the biggest model to be safe" | Cost and latency are product features. Use the smallest model that passes the evals. |

## Red flags

- Model output passed to `eval`, a shell, SQL, or `innerHTML`
- An agent tool that can delete, send or pay without confirmation
- Model ids hard-coded in many files, or chosen from memory
- No timeout on the LLM call
- API keys or other users' data inside the prompt
- "Tested it in the playground" as the only verification

## References

- [llm-eval-harness.md](references/llm-eval-harness.md): open when setting up the eval set, graders and old-vs-new comparison
