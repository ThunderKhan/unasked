---
doc: user-journey
status: draft
---

# Unasked — User Journey and Interaction States

**This is the MVP journey, not a multi-feature roadmap.** Cross-references: [users](users.md), [scope](scope.md), [PRD](prd.md), and [technical spec](spec.md). All content below is a proposal for review.

## One outcome

**Before starting a web-feature build, a developer identifies and clarifies one consequential requirement they otherwise might have missed.**

## Before, during, and after using Unasked

| Stage | Developer action | Problem to solve | Product response | Completion signal |
| --- | --- | --- | --- | --- |
| 0. Outside the app | Has a short conversation with a client about **one feature** | Some requirements remain implicit | No automatic attendance or recording | Notes exist |
| 1. Enter | Opens one-page workbench | May not know what to paste | Empty input, one clearly fictional example, brief privacy/limitation notice | Understands "one feature, pasted notes" |
| 2. Describe | Pastes or edits notes | Notes may be incomplete or sensitive | Preserve exact text; reject empty input | Valid notes ready |
| 3. Analyze | Clicks **Find missing questions** | Hard to tell what was never clarified | Loading state → 0–3 high-impact questions with implementation rationale | Understands what to ask |
| 4. Evaluate | Reads the suggestions | Some AI suggestions may be off-target | Shows context and uncertainty; user chooses action | Selects a relevant item |
| 5a. Confirm | Asks client **outside Unasked**, types a confirmed answer | Avoid treating an assumption as fact | Requires non-empty answer; moves item to resolved list | Decision recorded |
| 5b. Dismiss | Marks question **Not applicable**, provides a reason | Avoid wasting client's time | Marks item inapplicable; reversible | Decision recorded |
| 6. Re-check | Presses **Re-analyze** | Earlier questions should not recur | Sends notes + prior decisions; filters resolved topics; proposes remaining gaps | Original issue stays resolved |
| 7. Exit | Leaves the tab or reloads | Data-retention expectations must be clear | Proposed MVP **does not persist** session | User was warned before leaving |

The **secondary user** may review the same screen with the developer; this is not a separate app journey.

## The primary path, as a story

A developer leaves a client meeting with this **synthetic** note:

> "We want customers to choose a slot on our website. They'll get an email once a booking is confirmed. Admins should be able to see bookings."

They paste it into Unasked and press **Find missing questions**. A top result may be:

- **Question:** "What happens if two customers select the same slot?"
- **Why it matters:** "The answer affects conflict handling and database consistency."
- **Evidence:** The note mentions selecting slots. The **absence** of a booking-conflict rule is the issue; the AI must not claim the client explicitly discussed double-booking.

The developer then asks the client and records:

> "Only one confirmed booking per slot; the other customer must pick another slot."

When the developer re-analyzes, the same booking-conflict issue must not reappear in different wording. The app may surface a *different* unresolved decision such as rescheduling, but **must not force exactly three questions**.

**A single question found and resolved is a complete product demo.**

## State diagram

~~~text
EMPTY NOTES
   │ user types notes
   ▼
READY ─────── analyze ───────► LOADING
                                 │
              ┌──────────────────┼───────────────────┐
              ▼                  ▼                   ▼
        RESULTS (0–3)       NO IMPORTANT GAPS      ERROR
              │                  │                   │
     ┌────────┴────────┐         │                 retry
     ▼                 ▼         │                   │
RECORD ANSWER      NOT APPLICABLE│                   │
     │                 │         │                   │
     └────────┬────────┘         │                   │
              ▼                  │                   │
         DECISION SAVED ◄────────┘                   │
              │                                      │
              └── re-analyze (with decisions) ───────┘
~~~

**Question lifecycle for MVP:** recommended → answered **or** not_applicable → optionally undone → eligible for re-analysis. The requested **asked** and **deferred** statuses are **not** present; adding them would enlarge the core workflow. Recording an answer only after client confirmation is a user policy, not something the software can independently certify.

## Interaction details that must remain consistent

1. **Analyze vs Re-analyze:** same backend operation; button label reflects current state. No invisible background AI calls.
2. **Priority:** show a ranking/order, not an unsupported numerical confidence score.
3. **Answer:** user types a nonblank decision; do not auto-fill or assume what the client will say.
4. **Not applicable:** user provides a nonblank reason so the dismissal is auditable within the session.
5. **Undo:** removes that decision and makes the topic eligible again.
6. **Input edit after answer:** keep prior decisions for the session; warn that they may be stale. Never silently invalidate confirmed answers.
7. **No matching gap:** say "No high-impact unanswered questions found in these notes", **not** "All requirements complete."
8. **Loading/error:** notes and prior decisions stay visible; malformed output cannot appear as question cards.

## Minimal layout, not an invented extra feature

~~~text
┌───────────────────────────────────────────────────┐
│ unasked.           Find what you forgot to ask    │
├─────────────────────┬─────────────────────────────┤
│ Client notes        │ Most important questions    │
│ [ editable text ]   │ 1. Question / why / actions │
│                     │ 2. Question / why / actions │
│ [Find questions]    │ 3. Question / why / actions │
│                     │ [Resolved decisions]        │
└─────────────────────┴─────────────────────────────┘
Mobile: stack the same two areas vertically.
~~~

This is a **behavioral wireframe**, not approved visual styling. Typography, colors, and whether the layout is side-by-side remain provisional in [PRD](prd.md).

## Edge paths to demonstrate

| Input/event | Expected behavior |
| --- | --- |
| Blank or whitespace notes | No AI call, helpful inline error |
| Notes mention multiple features | Ask the developer to narrow the notes to one feature |
| Explicitly answered cancellation rule | Do **not** ask cancellation question again |
| Semantically equivalent answered topic under different wording | Attempt stable gap-key suppression; evaluate failures honestly |
| Missing rationale or fabricated source excerpt | Drop/repair unsafe result, never present a fake quotation |
| Model timeout or invalid JSON | Preserve input and decisions; show retry state |
| User reopens the page | Session cleared if ephemeral mode approved and implemented |

## UX validity check

Test the complete story with one developer without instructing them where to click. Record where they hesitate or misinterpret an AI suggestion as a confirmed fact; fix clarity before adding functionality. See [user-validation](user-validation.md).

### Research foundation

Journey stages and minimum useful slices: [Atlassian story mapping](https://www.atlassian.com/agile/product-management/story-mapping). Human control and recoverable actions: [Google PAIR Feedback + Control](https://pair.withgoogle.com/guidebook-v2/chapter/feedback-controls/) and [Mental Models](https://pair.withgoogle.com/guidebook-v2/chapter/mental-models/).
