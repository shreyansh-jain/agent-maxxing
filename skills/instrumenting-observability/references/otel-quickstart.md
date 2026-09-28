# OpenTelemetry quickstart and SLO burn rates

Last reviewed 2026-09-28. OpenTelemetry package names and configuration change often. Before copying anything below, check the current getting-started page for your language at https://opentelemetry.io/docs/languages/.

## Wiring a service

1. Install the SDK, the auto-instrumentation packages for your language, and an OTLP exporter.
2. Initialise the SDK **before** any other import. With auto-instrumentation, the libraries it patches must load after it.
3. Configure through environment variables, not code, so the same build runs anywhere:

```bash
OTEL_SERVICE_NAME=checkout-service
OTEL_RESOURCE_ATTRIBUTES=deployment.environment=staging,service.version=1.14.2
OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4317
OTEL_TRACES_SAMPLER=parentbased_traceidratio
OTEL_TRACES_SAMPLER_ARG=0.1
```

4. Send telemetry to an **OpenTelemetry Collector** rather than straight to a vendor. The collector handles batching, redaction (the `attributes` / `transform` processors), tail sampling, and fan-out to backends. Switching vendors then means editing the collector config, not the code.

Example (Node.js):

```typescript
// tracing.ts: import this first, e.g. node --import ./tracing.js server.js
import { NodeSDK } from '@opentelemetry/sdk-node';
import { getNodeAutoInstrumentations } from '@opentelemetry/auto-instrumentations-node';
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-grpc';

new NodeSDK({
  traceExporter: new OTLPTraceExporter(),
  instrumentations: [getNodeAutoInstrumentations()],
}).start();
```

## Manual span pattern

```typescript
import { trace, SpanStatusCode } from '@opentelemetry/api';
const tracer = trace.getTracer('checkout');

export async function chargeProvider(order: Order) {
  return tracer.startActiveSpan('charge_provider', async (span) => {
    span.setAttribute('payment.provider', order.provider); // bounded value
    try {
      return await provider.charge(order);
    } catch (err) {
      span.recordException(err as Error);
      span.setStatus({ code: SpanStatusCode.ERROR });
      throw err;
    } finally {
      span.end();
    }
  });
}
```

## Multi-window burn-rate alerts

Error budget = 1 − SLO. For a 99.9% SLO the budget is 0.1%. A burn rate of 1 uses up the budget exactly over the SLO window.

| Severity | Burn rate | Long window | Short window | Budget spent when it fires |
|---|---|---|---|---|
| page | 14.4 | 1h | 5m | 2% of a 30-day budget |
| page | 6 | 6h | 30m | 5% |
| ticket | 1 | 3d | 6h | 10% |

An alert fires only when **both** windows exceed the rate. The long window shows the burn is significant; the short window shows it is still happening. These values follow the Google SRE Workbook's "Alerting on SLOs" chapter (https://sre.google/workbook/alerting-on-slos/).

PromQL shape for the first row:

```promql
(
  sum(rate(http_requests_total{job="checkout",status_class="5xx"}[1h]))
  / sum(rate(http_requests_total{job="checkout"}[1h]))
) > (14.4 * 0.001)
and
(
  sum(rate(http_requests_total{job="checkout",status_class="5xx"}[5m]))
  / sum(rate(http_requests_total{job="checkout"}[5m]))
) > (14.4 * 0.001)
```
