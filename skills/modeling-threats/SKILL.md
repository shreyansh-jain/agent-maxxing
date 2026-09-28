---
name: modeling-threats
description: Design-time threat modeling of a system, feature or architecture change. Use when designing anything handling auth, money, personal or multi-tenant data, uploads, webhooks or LLM agents with tools, or when asked how an attacker could abuse it or for STRIDE.
license: Apache-2.0
metadata:
  version: "0.1.0"
  category: "architect"
  sources: "openai/skills security-threat-model (Apache-2.0); wshobson/agents stride-analysis-patterns, threat-mitigation-mapping (MIT); garrytan/gstack cso (MIT); addyosmani/agent-skills security-and-hardening (MIT); ideas: trailofbits/skills"
---

# Modeling Threats

A threat model is a short list of realistic abuse paths against the assets that matter, each with a named mitigation and an owner, or an explicit decision to accept the risk. It is not a checklist of every threat that might exist.

## When to use

- Designing a new service, feature or integration that crosses a trust boundary: public endpoints, auth, payments, file uploads, webhooks, third-party callbacks, admin tooling
- Adding multi-tenancy, sharing, delegation or impersonation
- Giving an LLM or agent tools, retrieval, browsing or code execution
- A design doc or RFC needs its security section
- "What could go wrong?", "how would someone abuse this?", "do a STRIDE pass"

**Not for:** auditing existing code or a diff for vulnerabilities (use `auditing-security`); deciding what personal data to collect, how long to keep it and how to delete it (use `handling-personal-data`); failures without an attacker, like outages and overload (use `designing-resilient-systems`).

## Process

1. **Scope and model the system from evidence.** State what is in and out of scope, and whether this is a design (docs) or an existing system (repo). List the components, data stores, external services and entry points. Draw the data flow as a list of edges, `A → B: data, protocol, auth`. Every component comes from the design doc or the code (`file:line`); mark anything else as an assumption.
   Exit: a data-flow list where every entry point and store is present, and assumptions are labelled.

2. **Mark trust boundaries and assets.** A trust boundary is any edge where the caller's privilege or identity changes: internet → edge, tenant → shared service, service → database, your code → third-party API, user content → LLM prompt, CI → production. List the assets an attacker wants: credentials and tokens, personal data, money movement, integrity-critical state (balances, permissions, audit logs), availability-critical paths, signing keys, build artifacts.
   Exit: each boundary names what is checked when crossing it (authn, authz, validation, rate limit, encryption), or says "nothing".

3. **Describe the attacker realistically.** List who can reach each entry point: anonymous internet user, authenticated user of another tenant, malicious insider with read access, compromised dependency, a document the LLM reads. Also state what they *cannot* do, so severity is not inflated.
   Exit: 2–5 attacker profiles, each with its reach and non-capabilities.

4. **Enumerate abuse paths with STRIDE per boundary.** At each boundary, ask the six questions in [stride-prompts.md](references/stride-prompts.md): Spoofing, Tampering, Repudiation, Information disclosure, Denial of service, Elevation of privilege. Write each surviving threat as an abuse path: *attacker → entry point → weakness → asset → impact*. Prefer 5–15 specific paths over 60 generic ones. For LLM and agent features, also run the agent checklist in the reference (prompt injection through retrieved content, tool abuse, data exfiltration via tool calls, excessive autonomy).
   Exit: every boundary has been asked all six questions, and each kept threat is a complete abuse path.

5. **Rank by likelihood × impact.** Rate each 1–3 with a one-line justification that accounts for existing controls. Priority: 9 or 6 = critical/high, 3–4 = medium, 1–2 = low. State which assumption most influences each high ranking. If the user is available, confirm the 1–3 assumptions that move the ranking most: exposure, tenancy, data sensitivity.
   Exit: a ranked table with justifications, and the assumptions that drive it.

6. **Map mitigations to owners.** For each high and medium threat, name a *specific* control at a *specific* place ("per-tenant authz check in `OrderRepository.find`", not "validate input"), whether it already exists (with evidence) or is new, and who owns it. Prefer controls that remove a whole class of threat: parameterized queries, allowlists, capability tokens, least-privilege credentials, sandboxing.
   Exit: every high threat has a mitigation and an owner, or a residual-risk entry.

7. **Record residual risk explicitly.** Anything not mitigated gets a line: the threat, why it is accepted (cost, likelihood, compensating control), who accepted it, and when to revisit. Unrecorded acceptance is just an unknown.
   Exit: no high threat is left without either a mitigation or a named acceptance.

8. **Write it down next to the design.** Save the model as `<feature>-threat-model.md` beside the design doc, or as its security section. Re-run steps 2–5 when a new boundary, asset or entry point is added.

## Output

```
Scope: <in> / <out>   Basis: design doc | repo @ <sha>
Data flow: A → B: <data>, <protocol>, <auth>   (one line per edge)
Trust boundaries: <edge>: checks <authn/authz/validation/rate limit> | none
Assets: <asset>: <why it matters>
Attackers: <profile>: can <reach>; cannot <non-capability>

| # | Abuse path | STRIDE | L | I | Priority | Mitigation (exists? where) | Owner |
|---|---|---|---|---|---|---|---|

Residual risk: <threat>: accepted by <who> because <reason>; revisit <when>
Assumptions that drive the ranking: …
```

## Red flags

- Threats with no asset or impact ("XSS is possible")
- Mitigations written as categories ("add validation") rather than a control at a location
- Components or controls claimed without a file, doc or diagram behind them
- An LLM feature modeled without treating retrieved content and tool output as attacker-controlled
- All threats rated "medium"; ranking was not actually done
- "Accepted" risks with no name attached

## References

- [stride-prompts.md](references/stride-prompts.md): open at step 4 for the per-boundary STRIDE questions and the LLM/agent threat checklist
