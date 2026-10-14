---
doc: scope
status: draft
---

# Unasked — Scope

**One line:** Unasked helps a freelance developer or small-agency developer find the three most consequential unanswered implementation questions in notes from a client feature-discovery conversation.

> Draft based on our project discussions. Not yet approved for implementation.

## The Unique Kernel

Unasked spots **what the client never said**, rather than summarizing what was said. It produces a *ranked, explainable* set of missing decisions, then remembers the answers or dismissals within the working session so it does not keep asking the same thing.

This is not a general meeting assistant or a prompt-to-checklist generator. The essential demonstration is that the next analysis improves when the client supplies new information.

## Who It's For

A freelance software developer or developer at a small agency who interviews a client before estimating or implementing **one web-app feature**. Today they rely on memory, ad hoc notes, generic checklists, and follow-up calls when a consequential question was overlooked.

**Problem hypothesis:** Forgotten requirements cause unnecessary clarification and rework. **Unvalidated:** how often this occurs, whether this particular workflow saves meaningful time, and whether customers will pay.

## The Core Loop

1. Paste notes from a client conversation describing one requested web-app feature.
2. Select **Find missing questions**.
3. Review at most three *specific*, high-impact questions, each with a reason it matters.
4. Ask the client outside the app; record the answer inline, or mark an irrelevant question not applicable.
5. Re-analyze the expanded context; previously resolved/dismissed issues should not recur.

The developer stays in control of all project decisions.

## Inspiration & Identity

- **Identity:** A quiet "second pair of ears" and requirements detective; the promise is *Find the questions you forgot to ask*.
- **Interaction:** A focused, visual discovery workbench with question cards, **not** a chat interface or PDF generator.
- **Look and feel:** Clear, professional, lightweight, high-signal. Exact colors, font and layout are **not yet user-approved**; avoid generic AI-dashboard decoration.

## Why This Matters to the Builder

The idea comes from participating in client discovery discussions as a software developer intern, sometimes alongside a founder. Important questions are occasionally missed and must be raised later. The builder wants something that assists discovery rather than automating the client relationship.

## What "Working" Looks Like

In a short demo, paste synthetic notes about appointment booking. Unasked identifies an important unresolved issue (e.g., what happens if two customers select the same slot), explains the implementation consequence, accepts a concrete answer, and **does not repeat that issue** on the next analysis. It may recommend a different remaining gap.

A reviewer should be able to see real AI reasoning on unseen notes, not just a canned example.

## The POC Boundary

**Now:** one user, one feature at a time; pasted text; a single analysis action using a real open-weight model; up to three grounded questions; priority/reason; record answer or mark not applicable; re-analysis in the same session; a brief, honest evaluation against a baseline.

**Essential quality:** source-grounded interpretation; no fabricated client statements; safe handling of empty/ambiguous input and model failure; consistent question-state behavior.

## Later

Live transcription, persistent workspaces, feature maps, optional source uploads, collaboration, multi-feature projects, and integrations—only if the core gap-detection result is useful.

## Explicitly Cut

- **Chatbot or autonomous interviewer:** the developer leads the meeting.
- **Transcription and Zoom/Meet integration:** unnecessary to prove gap detection.
- **PRD/PDF/proposal generation:** output is questions, not documents.
- **Asked/deferred status workflow:** answer and not-applicable actions suffice for the first proof.
- **Contradiction detector and scope graph:** separate problems that dilute the experiment.
- **Accounts, team sync, payments, and CRM:** add operational work without testing the kernel.
- **Fine-tuning, RAG, multi-agent orchestration:** no evidence yet that simpler structured inference is inadequate.
- **Claims of guaranteed completeness or reduced cost:** not demonstrated.
