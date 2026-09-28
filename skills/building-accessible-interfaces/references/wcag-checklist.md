# WCAG 2.2 AA checklist

Last checked: 2026-09-28. The normative text is the authority: [WCAG 2.2](https://www.w3.org/TR/WCAG22/), [Quick Reference](https://www.w3.org/WAI/WCAG22/quickref/), [ARIA Authoring Practices (APG)](https://www.w3.org/WAI/ARIA/apg/). Re-check the W3C pages before making a formal conformance claim.

## Contents

- Perceivable
- Operable
- Understandable
- Robust
- New in 2.2
- Widget patterns

## Perceivable

| Criterion | Check |
|---|---|
| 1.1.1 Non-text content | Meaningful images have `alt` text; decorative images use `alt=""`; icon buttons have names |
| 1.2.x Media | Captions for video with audio; transcripts for audio-only content |
| 1.3.1 Info and relationships | Headings, lists, tables (`th`, `scope`) and form labels are in markup, not just in styling |
| 1.3.5 Identify input purpose | `autocomplete` set on personal-data fields |
| 1.4.1 Use of color | State and errors are not shown by color alone |
| 1.4.3 Contrast (minimum) | 4.5:1 for text; 3:1 for large text (≥24px, or ≥18.66px bold) |
| 1.4.10 Reflow | No horizontal scroll at 320 CSS px wide |
| 1.4.11 Non-text contrast | 3:1 for UI component boundaries, icons and focus indicators |
| 1.4.12 Text spacing | Layout survives increased line, letter and word spacing |
| 1.4.13 Content on hover/focus | Tooltips can be dismissed with Esc, can be hovered, and stay until dismissed |

## Operable

| Criterion | Check |
|---|---|
| 2.1.1 Keyboard | Every function is available from the keyboard |
| 2.1.2 No keyboard trap | Focus can always move away (except inside a modal, which Esc closes) |
| 2.2.1 Timing adjustable | Session timeouts warn the user and can be extended |
| 2.3.1 Three flashes | Nothing flashes more than 3 times per second |
| 2.4.1 Bypass blocks | Skip link to main content, or landmarks |
| 2.4.3 Focus order | Focus order matches the reading order |
| 2.4.4 Link purpose | Link text makes sense in context (no bare "click here") |
| 2.4.6 Headings and labels | Headings and labels are descriptive |
| 2.4.7 Focus visible | A visible focus indicator on every focusable element |
| 2.5.3 Label in name | The accessible name contains the visible label text |

## Understandable

| Criterion | Check |
|---|---|
| 3.1.1 Language of page | `<html lang="…">` is set |
| 3.2.1 / 3.2.2 On focus / on input | Focusing or changing a field does not navigate or submit unexpectedly |
| 3.3.1 Error identification | Errors are described in text and tied to the field |
| 3.3.2 Labels or instructions | Every input has a visible label; the required format is stated |
| 3.3.3 Error suggestion | The message says how to fix the error |
| 3.3.4 Error prevention | Legal and financial submissions can be reviewed, corrected or reversed |

## Robust

| Criterion | Check |
|---|---|
| 4.1.2 Name, role, value | Custom widgets expose name, role and state (`aria-expanded`, `aria-selected`, `aria-checked`) |
| 4.1.3 Status messages | Async results are announced through `role="status"` or `alert` without moving focus |

## New in 2.2

| Criterion | Check |
|---|---|
| 2.4.11 Focus not obscured (minimum) | A focused element is not fully hidden by sticky headers, footers or banners |
| 2.5.7 Dragging movements | Every drag action has a single-pointer alternative (buttons, click-to-move) |
| 2.5.8 Target size (minimum) | Targets are at least 24×24 CSS px, or have enough spacing around them |
| 3.2.6 Consistent help | Help mechanisms appear in the same place across pages |
| 3.3.7 Redundant entry | Information already entered is auto-filled or selectable, not retyped |
| 3.3.8 Accessible authentication (minimum) | No cognitive test to log in; allow paste, password managers, passkeys or email links |

4.1.1 Parsing is obsolete in WCAG 2.2.

## Widget patterns (APG)

| Widget | Keyboard contract |
|---|---|
| Dialog (modal) | Focus moves inside on open; Tab cycles within the dialog; Esc closes it; focus returns to the trigger. Prefer native `<dialog>` with `showModal()` |
| Menu button | Enter, Space or ↓ opens the menu; arrows move between items; Esc closes it and returns focus |
| Tabs | Arrows move between tabs; Tab moves into the panel; `aria-selected` on the active tab |
| Combobox / autocomplete | `aria-expanded`, `aria-controls`, `aria-activedescendant`; ↑/↓ move through options; Enter selects; Esc closes |
| Disclosure / accordion | A button with `aria-expanded` toggles the region |
| Toast | `role="status"` region already present in the DOM; does not steal focus; stays long enough to read, or can be paused |
