---
name: auditing-security
description: Evidence-based security audit of code, a diff, or a system surface, reporting only findings with a concrete attack path. Use when asked for a security review or audit, before a release or pentest, when code touches auth, payments, uploads, webhooks, secrets, CI pipelines or agent tools, or when a scanner or report flags a possible vulnerability to confirm or dismiss.
license: Apache-2.0
metadata:
  version: "0.1.0"
  category: "review"
  sources: "garrytan/gstack cso and review security specialist (MIT); getsentry/skills security-review and find-bugs (Apache-2.0); addyosmani/agent-skills security-and-hardening (MIT); ideas: trailofbits/skills"
---

# Auditing Security

A vulnerability is an attacker-controlled input that reaches a sensitive operation across a security boundary and produces real impact. Report that path with evidence, or it is not a finding.

## When to use

- "Security review this", "audit the auth service", "are we safe to launch?", "pentest prep"
- A change touches authentication, authorization, sessions, payments, uploads, webhooks, secrets, crypto, deserialization, CI/CD workflows, infrastructure config, or LLM and agent tool calls
- A scanner result, bug bounty report or reviewer comment claims a vulnerability, and you need a true-or-false-positive verdict

**Not for:** general pre-merge review, where security is one checklist among several (use `reviewing-code`); updating vulnerable dependencies after the audit (use `upgrading-dependencies`); an active breach (use `responding-to-incidents`).

## The rule

```
NO FINDING WITHOUT SOURCE → PATH → SINK → IMPACT, EACH BACKED BY CODE OR CONFIG
```

Violating the letter of the rule is violating the spirit of the rule. Pattern matches are leads, not findings. A report full of theoretical issues trains people to ignore the real ones.

## Process

1. **Fix scope and depth.** Agree on what is in scope: a diff, a service, or a surface. Scale depth to size. Under ~20 files, read everything. For 20–200 files, read every trust boundary and every changed file. Above that, rank surfaces by exposure and impact and go deep on the top ones.
   Exit: a written scope and a coverage plan. Anything you will not assess is named now, not discovered later.

2. **Build context, not verdicts.** Map the actors (anonymous, user, admin, tenant, service, CI), the assets (data, money, credentials, compute), the entry points (routes, jobs, queues, webhooks, file parsers, CLI flags, agent tools), the trust boundaries, and the invariants ("a user can read only their own org's invoices"). Resist naming vulnerabilities during this phase. Early verdicts anchor the rest of the audit.
   Exit: a short model listing actors, assets, entry points, boundaries and invariants, with file references.

3. **Hunt by category.** Walk each entry point through the categories in [attack-surface.md](references/attack-surface.md) that apply: injection, authorization and IDOR, authentication and sessions, secrets (including git history), crypto, SSRF, file handling, deserialization, business logic, supply chain, CI/CD and infrastructure, LLM and agent tools. Run the available scanners (for example `semgrep`, `gitleaks`, `osv-scanner`, `npm audit`), and treat their output as leads. A missing tool or an empty scan is a coverage gap, not a clean result.
   Exit: a candidate list, each with its entry point and suspected sink.

4. **Trace every candidate end to end.** For each one, answer:
   - Is the source **attacker-controlled**? Operator config, env vars set at deploy time, and constants usually are not. Env vars populated from PR content in CI are.
   - Does the path **cross a boundary** the attacker should not cross?
   - What **mitigations** sit on the path: framework auto-escaping, parameterized ORM calls, middleware, schema validation, network policy?
   - What is the **impact** in this application, with the attacker's realistic prerequisites?
   Exit: each candidate is **supported** (all four answered with file:line evidence), **hypothesis** (plausible, but one link is unverified; name it), or **disproved** (keep the reason as coverage evidence).

5. **Challenge each supported finding.** Give an independent reviewer the location, the claimed invariant violation and this rubric, *without* your conclusion. Use a fresh-context subagent when one is available; otherwise do a separate skeptical pass and label it as such. The reviewer tries to disprove the finding by checking callers, middleware, config and legitimate uses. Record any dissent.
   Exit: each finding has a TRUE POSITIVE or FALSE POSITIVE verdict with the reason. If reachability is unknown, say "unknown". Do not write "unreachable".

6. **Search for variants.** One root cause usually shows up in several places. After confirming a finding, search for the same pattern (same sink, same missing check, same helper misuse) across the scope.
   Exit: variants are listed under the parent finding.

7. **Report.** Use the format below. Start with the coverage status. Proofs of concept run only locally or in tests, and only with the user's permission. Never run them against production or third-party systems, and never take destructive actions.

## Output

```
Security audit: <scope> | Coverage: complete | partial (<gaps>) | not assessed (<why>)
Model: <actors, assets, key boundaries in 3–5 lines>

| ID | Severity | Confidence | Location | Finding |
|----|----------|------------|----------|---------|
| S1 | High | High | api/invoices.ts:58 | IDOR: any user reads any org's invoice |

S1. Attack path: <source> → <path> → <sink> → <impact>
    Evidence: <file:line for each link>; mitigations checked: <…>
    Challenge: <verdict and dissent> | Variants: <locations>
    Fix: <concrete change>; regression test: <what it asserts>

Hypotheses (not findings): <each with the missing link and how to settle it>
Disproved: <candidate: reason> (coverage evidence)
Not assessed: <areas, tools unavailable>
```

Severity reflects impact and the attacker's prerequisites in this application, not a pattern name or a CVSS number. When nothing survives, write "No supported findings in the assessed scope", followed by the coverage section. Never write "the code is secure".

## Rationalizations

| Excuse | Reality |
|---|---|
| "It matches the injection pattern, report it" | Trace the source first. Parameterized queries and auto-escaped templates are the common false positives. |
| "The ID is a UUID, so it can't be guessed" | UUIDs leak through URLs, logs and shared links. They are not authorization. Check the ownership check. |
| "It's behind login, so it's fine" | Login answers who you are, not what you may touch. Most real bugs are horizontal access between users. |
| "The scanner found nothing" | Scanners miss logic and authorization bugs. An empty scan counts as coverage evidence only for what the scanner actually checks. |
| "Report it anyway, better safe than sorry" | False positives cost trust and time. Put unverified items under Hypotheses with the link that is missing. |
| "It's just a dev dependency / internal endpoint" | Check reachability. CI runners, preview deploys and SSRF make "internal" reachable. |

## Red flags

- A finding with no attacker-controlled source identified
- Severity chosen from the vulnerability name rather than the impact here
- "Secure" or "no issues" stated without a coverage section
- Running exploit code against a shared or production environment
- Pasting real secrets into the report instead of `<REDACTED>` and a location

## References

- [attack-surface.md](references/attack-surface.md): open at step 3 for the per-category checklist and the search commands
