# Breaking dependencies to create a seam

Each technique is a small edit meant to be safe to make before any tests exist. Apply one at a time, keep each edit mechanical, and use automated refactoring tools when you have them.

| Problem in the code | Technique | Edit |
|---|---|---|
| Constructs its own collaborator (`new StripeClient()`) | **Parameterize constructor** | add a constructor or function parameter that defaults to the current construction |
| Calls a static or global (`Clock.now()`, `db.query`) | **Wrap the static** | add a thin instance method that calls it, then override or inject that method in the test |
| Big method that does IO in the middle | **Extract and override** | move the IO into its own method; in the test, subclass and override it |
| Reads config or env directly | **Extract parameter** | pass the value in; the caller reads the env |
| Hidden singleton | **Introduce setter for tests** | add a reset/set hook, clearly named for tests only (last resort) |
| Module-level import of a heavy dependency | **Substitute at the module boundary** | inject the module, or use the language's module-mocking at the boundary only |
| Deeply nested logic you need to test on its own | **Extract pure function** | lift the computation out as a function of its inputs, and call it from the original spot |

## Worked example (Python)

Before: impossible to test without the network and the clock.

```python
def send_overdue_reminders():
    today = datetime.date.today()
    for inv in Invoice.objects.filter(paid=False):
        if inv.due < today:
            requests.post(MAILER_URL, json={"to": inv.email, "id": inv.id})
```

After *parameterizing* the clock and the sender. Existing callers are unchanged because the defaults keep today's behavior:

```python
def send_overdue_reminders(today=None, send=None, invoices=None):
    today = today or datetime.date.today()
    send = send or (lambda payload: requests.post(MAILER_URL, json=payload))
    invoices = invoices if invoices is not None else Invoice.objects.filter(paid=False)
    for inv in invoices:
        if inv.due < today:
            send({"to": inv.email, "id": inv.id})
```

A characterization test can now pass in a fixed date, a list of invoices, and a `send` that records its calls.

## Sprout and wrap

- **Sprout function:** write the new logic as a new, fully tested function, then add a single call to it from the legacy code. The legacy code only gains one line.
- **Wrap function:** rename the old function to `_inner`, add a new function with the original name that calls `_inner` and adds the new behavior before or after it. Callers are untouched.

## Scratch refactoring

When the code is too confusing to know where the seams are, refactor it aggressively on a throwaway branch just to learn its structure. Then **throw that branch away** and do the real work in small, tested steps. The throwaway pass is for learning only; don't ship it.
