---
doc: prd
status: draft
---

# Unasked — Product Requirements

**Product:** A single-feature client-discovery workbench that identifies the questions a software developer missed.

**Basis:** `scope.md > The Unique Kernel`, `Who It's For`, `The Core Loop`, and `The POC Boundary`.

> Proposed interaction details below are **draft recommendations**, not decisions already approved by the builder.

## The Core Journey

1. Open Unasked to a clean, single-page workspace explaining the task and showing a short **fictional** example.
2. Paste notes from a client conversation about **one** web-app feature.
3. Click **Find missing questions**. A visible working state appears.
4. See up to three questions, ranked by importance. Each card includes the question, why it matters for implementation, and the note excerpt supporting its context when available. The app must **not** present an absent detail as something the client stated.
5. On any card, either **Record answer** (type the client's actual answer and confirm) or **Not applicable** (dismiss with a short explanation).
6. Click **Re-analyze**; the system includes current notes and recorded decisions, filters resolved/dismissed issues, and proposes other useful questions if warranted.
7. Continue the conversation outside the app. If no important gaps remain, the app says so cautiously rather than declaring the specification complete.

## Screens and Layout

One responsive workspace; no navigation or secondary dashboard.

- **Header:** "Unasked", single-line promise, clear current-session indicator.
- **Notes area:** large editable text field, short guidance that notes should describe one feature, analyze button.
- **Questions area:** up to three stacked or side-by-side cards (depending on viewport) showing prioritization, explanation, and inline actions.
- **Resolved area:** a small collapsible list of recorded answers and not-applicable decisions, so the user understands why something disappeared from the top three.
- **Feedback:** loading, validation error, AI unavailable, and no-important-gap states appear in place without losing entered notes.

**Design note:** The exact typography, palette, and visual references still need confirmation. Do not invent an elaborate design system.

## Look and Feel

A focused developer tool, not a chat transcript, enterprise management dashboard, or "AI magic" marketing page. The content hierarchy should center on the next question to ask and its concrete development consequence. Favor concise text, readable spacing, clear status labels, and restrained emphasis. Palette/typeface remain open pending review.

## Features and Behavior

### Enter Discovery Notes

- Accept pasted or typed plain-text notes concerning **one** software feature.
- Keep user-entered text intact; never rewrite it as if client-approved.
- Reject an empty/whitespace-only submission with a clear message.
- If notes are ambiguous or cover many features, request narrower input rather than pretending to know the single feature.
- Display a clearly marked fictional example for first-time demo use; do not silently populate real user data.

**Acceptance:** A user can submit a plausible feature description; an empty submission triggers feedback and no analysis.

### Identify and Rank Missing Questions

- Return **zero to three** distinct, genuinely unanswered implementation questions.
- Each card displays: question, priority (relative order is sufficient), implementation consequence, and relevant supporting excerpt or "based on the provided context".
- The rationale identifies a *potential* decision; it must not fabricate an answer or assert a fact missing from the notes.
- Suggestions should be contextual to the feature, not generic "tell me more" questions.
- Already answered questions should not appear as open.
- When evidence is too thin, give a concise limitation and ask for more notes rather than invent details.

**Acceptance:** Booking notes that omit double-booking rules may produce a conflict-handling question; notes explicitly resolving that rule must not be reclassified as unanswered. The system can return fewer than three results.

### Record an Answer or Dismiss a Question

- **Record answer:** opens an inline field and requires non-empty answer text. Show the saved answer in the resolved area.
- **Not applicable:** marks the question irrelevant and records a short reason so future analysis can avoid it.
- **Undo:** the user can revert an accidental resolution or dismissal within the current session.
- Both actions modify the working session context; they do not automatically contact clients or change original notes.
- **Asked** and **deferred** are intentionally absent from the MVP.

**Acceptance:** Attempting to save a blank answer is blocked; a resolved or dismissed question is not duplicated in the next analysis; Undo makes it eligible again.

### Re-analyze Context

- Provide an explicit **Re-analyze** action after a decision or edit.
- Preserve existing notes and prior decisions during the current session.
- Recompute up to three unresolved questions with the updated context; distinguish a new question from an existing one when possible.
- A material change to the notes does not erase recorded answers, but the app warns the user if a prior decision may no longer match.

**Acceptance:** Answering "only one confirmed booking per slot" removes the same underlying double-booking question on refresh. Other gaps can surface without claiming a project is fully specified.

## States and Boundaries

- **Initial:** blank notes and one labeled fictional example.
- **Loading:** disable repeated submissions; preserve editable data.
- **No useful gaps:** "No high-impact unanswered questions found in these notes" plus caveat that this is not a completeness guarantee.
- **Model failure/time-out/invalid output:** an actionable retry message; never show malformed JSON as a user question or mark questions answered.
- **Sensitive information:** input is handled as confidential by design; use synthetic/anonymized notes for a public demo. Do not log raw notes on the backend.
- **Session lifetime (proposed):** ephemeral browser memory, cleared on refresh/close; no cloud storage or accounts. The UI must say so.
- **Trust:** model output is a suggestion; developer confirmation is authoritative. No automatic project commitments.

## Product Decisions

**Established from project discussions**
- One narrow task: detect missed questions in software-feature discovery.
- Show up to three important questions with reasons.
- Let the user record answers or dismiss irrelevant items and re-analyze.
- No chat interface, PDF generator, live meeting capture, or multi-agent product.
- A smallest-complete-version approach with measurable evaluation.

**Proposed, awaiting review**
- Single-page, two-area workbench.
- Ephemeral session (no persistence).
- Dismissal requires a reason; optional Undo.
- Fictional sample as first-use help.

## What We're Building

One complete interaction from notes → real-model gap analysis → prioritized cards → recorded answer/dismissal → improved next analysis, with visible error/empty states and reproducible tests.

## Deferred From the POC

Meeting recording and speech-to-text, a full asked/deferred lifecycle, persistent projects, exports, integrations, accounts, collaboration, complex feature dependencies, and analytics; none is necessary to prove the core loop.

## Possible Later Enhancements

Source-linked notes with timecodes; domain-specific checklists; a live low-distraction meeting side panel; client-facing follow-up collection; cross-session project memory, subject to privacy requirements.

## Non-Goals

- Replacing a business analyst or claiming a complete specification.
- Producing project estimates, architecture, contractual commitments, or an autogenerated PRD.
- Automatically interviewing or messaging the client.
- Storing real client-sensitive notes on a public demo server.
- Monetization/billing implementation during the hackathon.

## Open Questions

**Before spec approval**
1. Confirm visual direction beyond "focused and non-chat": typography/palette/reference.
2. Confirm session persistence policy: ephemeral-by-default is proposed for sensitive conversations.
3. Decide whether the demo must be publicly interactive or whether a reproducible local build plus recorded demo is sufficient.

**Can be checked during build**
- Which open-weight model delivers reliable structured analysis on the chosen hardware?
- Whether domain-specific analysis beats a generic-LLM and simple-checklist baseline.
