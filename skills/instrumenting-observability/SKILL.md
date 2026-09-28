---
name: instrumenting-observability
description: Vendor-neutral logging, metrics, tracing, SLO and alerting practice built on OpenTelemetry. Use when adding logs, metrics or spans to a feature, shipping something that runs in production, defining SLOs or alerts, fixing noisy or missing alerts, or when a production problem cannot be explained from the telemetry that exists.
license: Apache-2.0
metadata:
  version: "0.1.0"
  category: "operate"
  sources: "addyosmani/agent-skills observability-and-instrumentation (MIT); wshobson/agents slo-implementation, distributed-tracing, prometheus-configuration (MIT)"
---

# Instrumenting Observability

Telemetry exists to answer questions on-call will ask at 3am. Write the questions first, then emit only the signals that answer them.

## When to use

- Building or changing a feature that will run in production
- Adding logging, metrics, tracing, dashboards, SLOs or alerts
- Alerts page too often, never fire, or fire without a runbook
- A production issue happened and the existing data could not explain it
- Moving from a vendor SDK to OpenTelemetry

**Not for:** diagnosing a bug you can reproduce locally (use `debugging-systematically`); an active outage (use `responding-to-incidents`); making something faster (use `optimizing-performance`).

## Process

1. **Write the on-call questions.** For the feature, list 2–4 questions someone paged will ask. For example: "What fraction of payments succeed on the first try?", "Which provider is failing?", "Is the queue falling behind?" Every signal you add must answer one of them.
   Exit: a written list of questions, each mapped to the signal that answers it.

2. **Pick the signal per question.** Metrics tell you *that* something is wrong (aggregates, cheap, alertable). Traces tell you *where* (the per-request path across services, sampled). Logs tell you *why* (a specific event with its context).
   Exit: each question has exactly one primary signal.

3. **Instrument with OpenTelemetry.**
   - **Traces:** turn on auto-instrumentation for HTTP, gRPC, database and queue clients. Add manual spans only around meaningful units of work (`charge_provider`, `apply_discounts`). Propagate context across every async boundary: HTTP headers, queue message attributes, job payloads. Follow the semantic conventions for attribute names (`http.route`, `db.system`, `messaging.system`).
   - **Metrics:** use RED for request paths (Rate, Errors, Duration as a *histogram*) and USE for resources (Utilization, Saturation, Errors). Keep label values in small fixed sets: route template, status class, dependency name. Never use user ids, raw URLs, emails, request ids or error text as labels, because cardinality is what breaks metrics backends.
   - **Logs:** one JSON object per event, with a stable `event` name, machine-readable fields, and the trace id and span id attached so logs join to traces. Use levels consistently: `error` means an invariant broke and someone may need to act; `warn` means degraded but handled; `info` means a business event.
   Exit: one request can be followed from its entry point to its last dependency by trace id.

4. **Keep secrets and PII out.** Use an allowlist of fields. Never log whole request or response bodies, tokens, passwords or full card numbers. Hash or truncate identifiers when the question only needs grouping.
   Exit: you have grepped the new log and span attributes for `password|token|secret|authorization|email` and nothing sensitive appears.

5. **Define SLOs, then alert on burn rate.** Pick an SLI users feel, such as the success ratio or the share of requests under a latency threshold. Then set a target, e.g. 99.9% over 28 days. Page on *fast burn* (e.g. 14× the budget rate over 1h, confirmed over 5m). Open a ticket on *slow burn* (e.g. 1× over 3 days). Alert on symptoms (error ratio, latency, queue age), not causes (CPU, one pod restarting).
   Exit: every alert has a threshold justified by the SLO, a severity of *page* or *ticket*, and a runbook link.

6. **Write the runbook.** Keep it to three sections: what the alert means for users, the first query or dashboard to open, and who to escalate to. If the honest action is "ignore it", delete the alert.

7. **Verify the telemetry itself.** Trigger the path in a dev or staging environment and look at the output. Check that the span appears with the right parent, the metric increments with the expected labels, and the log line carries the trace id. Force an error and confirm the alert query would match it.
   Exit: you have seen each new signal with your own eyes, not assumed it.

## Output

```
Feature: <name>
Questions → signals:
  1. <question> → metric <name>{labels} / span <name> / log event <name>
SLO: <SLI> ≥ <target> over <window>   Alerts: page <burn rule>, ticket <burn rule>
Runbook: <path>
Verified: <how each signal was observed>
```

## Red flags

- Logging "just in case" with no question behind it
- String-interpolated log messages instead of structured fields
- A label whose values are unbounded: ids, URLs, messages
- Averages instead of histograms and percentiles
- An alert with no runbook, or one that people routinely acknowledge and ignore
- Context lost at a queue or thread boundary, which shows up as orphan spans
- Vendor-specific SDK calls scattered through business code instead of behind OpenTelemetry

## References

- [otel-quickstart.md](references/otel-quickstart.md): open when wiring OpenTelemetry into a service for the first time, or when choosing burn-rate thresholds
