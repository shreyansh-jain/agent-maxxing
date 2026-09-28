---
name: building-accessible-interfaces
description: WCAG 2.2 AA accessibility for web UIs, from semantic markup to keyboard, focus, forms and screen readers. Use when building or reviewing UI components, pages or forms, fixing an axe or Lighthouse accessibility report, or when keyboard or screen reader users report problems.
license: Apache-2.0
metadata:
  version: "0.1.0"
  category: "build"
  sources: "addyosmani/web-quality-skills accessibility (MIT); addyosmani/agent-skills frontend-ui-engineering (MIT); wshobson/agents wcag-audit-patterns (MIT); ideas: vercel-labs/agent-skills web-design-guidelines"
---

# Building Accessible Interfaces

Use native HTML elements so the browser provides keyboard, focus and screen reader behavior for free. Reach for ARIA only to describe what HTML cannot, and prove the result with a keyboard and a screen reader, not only a scanner.

## When to use

- Building or changing a component, page, form, dialog, menu, table or custom widget
- An axe, Lighthouse or WAVE report lists accessibility violations
- A user reports they cannot reach, operate or understand something with a keyboard, screen reader, zoom or voice control
- A product or legal requirement names WCAG, ADA, Section 508 or the European Accessibility Act

**Not for:** general visual polish or layout (use `designing-interfaces` for component APIs); journey tests that happen to use role locators (use `testing-end-to-end`); page-speed work (use `optimizing-performance`).

## The rule

```
NATIVE ELEMENT FIRST; ARIA ONLY WHEN NO ELEMENT FITS; DONE ONLY AFTER A KEYBOARD PASS
```

Violating the letter of the rule is violating the spirit of the rule. A `div` with a click handler and `role="button"` still needs you to rebuild focus, Enter/Space handling and disabled state by hand, and it usually ends up missing one of them.

## Process

1. **Structure with semantics.** Use real `button`, `a href`, `input`, `select`, `label`, `table`, `dialog`, `nav`, `main`, `header` and `footer`. Give the page one `h1`, and don't skip heading levels. Set `lang` on `html`. A link goes somewhere; a button does something.
   Exit: no clickable `div` or `span`, and landmarks and headings describe the page outline.

2. **Name everything.** Every control has an accessible name: a visible `<label for>`, the button's text, or `aria-label` for icon-only controls. Images get `alt` text that conveys their purpose, or `alt=""` if decorative. Errors and hints are linked with `aria-describedby`.
   Exit: the browser's accessibility tree shows a meaningful name for every interactive element.

3. **Make it keyboard operable.** Everything that works with a mouse works with Tab, Shift+Tab, Enter, Space, Escape and the arrow keys where the pattern expects them (menus, tabs, listboxes). Focus order follows visual order. There is no positive `tabindex`, and no keyboard traps. Provide a skip link to the main content.
   Exit: you can complete the task with the keyboard alone.

4. **Keep focus visible and managed.** Focus indicators must be clearly visible and not hidden behind sticky headers (WCAG 2.2 adds "focus not obscured"). Opening a dialog moves focus into it and keeps it there; closing it returns focus to the trigger. After client-side navigation, move focus to the new page's heading, or announce the change.
   Exit: at every step you can see where focus is, and it never gets lost behind something else.

5. **Meet perception minimums.** Contrast is at least 4.5:1 for body text and 3:1 for large text, icons and focus rings. Color is never the only signal. Content reflows at 320 px wide and at 200% zoom without horizontal scrolling. Pointer targets are at least 24×24 CSS px. Honor `prefers-reduced-motion` and don't flash.
   Exit: the automated contrast check passes and a manual zoom check passes.

6. **Build forms that forgive.** Show labels outside the field, not placeholder-only text. Mark required fields in text as well as with `required`. Give specific error messages next to the field, and on submit move focus to the first error or an error summary. Support autofill (`autocomplete` attributes) and paste. Don't make users re-enter information the site already has.
   Exit: an invalid submit leads a screen reader user straight to the problem and says how to fix it.

7. **Announce dynamic changes.** Toasts, async results, and "saved" states use a polite live region (`role="status"`) that exists in the DOM before its content changes. Use assertive announcements only for errors that block the user. Loading states say what is loading.
   Exit: a screen reader hears the outcome of every async action.

8. **Test in three layers.** (a) Automated: run axe (browser extension, `@axe-core/playwright`, or Lighthouse) and fix every violation. Automated checks find only about a third of the issues. (b) Keyboard-only pass through the changed flow. (c) Screen reader smoke test with VoiceOver, NVDA or TalkBack: can you hear what each control is, what state it is in, and what happened after you acted?
   Exit: all three layers pass, and you report what each one covered.

## Output

```
Scope: <components/pages>  Standard: WCAG 2.2 AA
Automated: <tool> → <N> violations fixed, <M> remaining (with reason)
Keyboard: <flow> completed without mouse: yes/no, issues: …
Screen reader: <reader + browser>: <what was heard, issues>
Remaining risks: <criteria not verified, e.g. captions for video>
```

## Rationalizations

| Excuse | Reality |
|---|---|
| "axe passes, so it's accessible" | Automated tools miss keyboard traps, focus order, bad names and confusing announcements. Do the keyboard and screen reader passes. |
| "We'll add accessibility later" | Retrofitting means rewriting components. Semantics cost nothing at build time. |
| "Add `role` and `aria-*` to the div" | Each ARIA attribute is a promise you must implement by hand. A native element keeps those promises for you. |
| "`outline: none` looks cleaner" | Then keyboard users are lost. Style the focus ring; never remove it. |
| "Placeholder text is the label" | It disappears on input, has low contrast, and is often not announced reliably. |

## Red flags

- `onClick` on a `div` or `span`; `href="#"` links that act as buttons
- `outline: none` or `:focus { outline: 0 }` with no replacement
- `aria-hidden="true"` on a focusable element; `tabindex` greater than 0
- Icon-only buttons with no accessible name
- A modal that doesn't trap focus or return it on close
- Error states shown only in red

## References

- [wcag-checklist.md](references/wcag-checklist.md): open when auditing a page or preparing a conformance claim; includes the new 2.2 criteria and links to the normative text
