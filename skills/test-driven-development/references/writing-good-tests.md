# Writing good tests

A test earns its place by catching one specific break. Before writing it, name the production change that would make it fail, and check whether that change would be a bug or a deliberate decision.

## Name the break

| If the only thing that can fail the test is… | Then… |
|---|---|
| a real bug (wrong branch, boundary, missing side effect) | keep it |
| a deliberate decision (a constant's value, message wording, private structure) | it is a change detector: test the behavior that depends on the decision instead |
| nothing, because the expected value is computed by the code under test | it is tautological: replace the expectation with a literal |

```typescript
// Tautological: the same builder produces both sides, so the test can never fail
expect(buildQuery({ tag: "urgent" })).toBe(buildQuery({ tag: "urgent" }));

// Hand-derived literal
expect(buildQuery({ tag: "urgent" })).toBe('tag:"urgent"');
```

## Test your contract, not the framework

Test what your code promises at its boundary: the route you register, the query you emit, the payload you return. Whether the framework calls your handler is the framework's test. Constructors, getters and trivial forwarding need a test only when they validate, normalise, default or derive something.

## Mocks

Mock **only** where your system meets something you don't control:

- third-party HTTP APIs, email, payments;
- the clock and randomness (inject them);
- the filesystem or network, when a temp dir or local server is impractical.

Never mock your own classes or modules. When a test needs a mock of your own code, the design is telling you something: inject the dependency, or test one level higher.

Before mocking a dependency, find out what side effects the real one has (retries, caching, ordering). A mock that skips those hides bugs.

Assert on outcomes, not on calls. `expect(mailer.send).toHaveBeenCalled()` proves the mock was called. Asserting on the message the fake outbox received proves the behavior.

## Structure

- **Arrange / Act / Assert**, with one blank line between them.
- **DAMP over DRY.** Repeat setup in each test when that keeps it readable on its own. Extract a builder only when the setup is noise.
- **Table-driven tests** for many input/output pairs, with the expected values written as literals.
- Keep test-only helpers in test utilities, never in production classes.

## Test sizes

| Size | Touches | Use for |
|---|---|---|
| Small | one process, no IO | logic, parsing, calculations |
| Medium | localhost: a real DB, a local server | repositories, handlers, integrations you own |
| Large | real external systems | a few end-to-end paths |

Put most tests at the smallest size that still goes through a real seam.
