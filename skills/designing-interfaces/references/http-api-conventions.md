# HTTP API conventions

If the repo already has conventions, follow them. These defaults are for new APIs.

## Resources

- Use plural nouns for collections and put no verbs in paths: `GET /orders`, `POST /orders`, `GET /orders/{id}`.
- Model actions as sub-resources or state changes: `POST /orders/{id}/cancellation`, or a `PATCH` to `status`.
- Use one case style for JSON fields and keep to it across the whole API.

## Status codes

| Code | Meaning |
|---|---|
| 200 / 201 / 204 | OK, created (with a `Location` header), no content |
| 400 | the request is malformed (unparseable body, wrong types) |
| 401 | not authenticated |
| 403 | authenticated but not allowed |
| 404 | not found, or hidden from this caller |
| 409 | conflict: a duplicate or a version mismatch |
| 422 | well-formed but semantically invalid |
| 429 | rate limited; include `Retry-After` |
| 5xx | server fault; never include stack traces or internals |

## Error body

Use one shape everywhere:

```json
{ "error": { "code": "VALIDATION_ERROR", "message": "email is required", "details": { "field": "email" } } }
```

Callers branch on `code`, which is machine-readable and stable. `message` is for humans and may change.

## Pagination

- Prefer **cursor** pagination for lists that change or grow: `?limit=50&cursor=…` returns `{ items, next_cursor }`.
- Offset pagination is acceptable only for small, stable lists.
- Always cap `limit` and document the default.

## Versioning and evolution

- Additive changes are safe: new optional request fields, new response fields, new endpoints.
- Breaking changes are removing or renaming a field, changing a field's type, or making an optional field required. Ship them as a new version (`/v2/…` or a version header) with a deprecation window, and signal it with `Deprecation` / `Sunset` headers.
- Clients must ignore unknown response fields. Say so in the docs.

## Idempotency

- Accept an `Idempotency-Key` header on non-idempotent writes (payments, orders).
- Store the key under a unique constraint **before** doing the work. A concurrent duplicate then hits the constraint and gets the stored response replayed back.
- The same key with a different payload returns 422. It must not replay the first response.
- Keys expire after a documented window.

## Checklist before publishing

- [ ] Every operation has an example request and response
- [ ] Every error code a caller can receive is listed
- [ ] Auth requirements are stated per operation
- [ ] Limits (page size, rate, payload size) are documented
- [ ] Unknown-field handling is stated
