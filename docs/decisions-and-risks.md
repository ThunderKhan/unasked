---
doc: decisions-and-risks
status: draft
---

# Unasked — Decisions, Assumptions and Risks

**Use this to prevent planning drift.** A recommendation is **not** a user-approved decision. Keep the accepted MVP boundary separate from unresolved design/architecture choices.

## Established boundaries (from conversation)

| ID | Decision | Why |
| --- | --- | --- |
| D-01 | Unasked finds missed questions **about one web-app feature** | The aim is a narrow, testable product, not a full requirements platform |
| D-02 | Show **up to 3** high-impact unanswered questions | Avoid overwhelming developers |
| D-03 | User records actual client answer or dismisses; **then re-analyzes** | Prove stateful improvement beyond a one-shot AI prompt |
| D-04 | No chatbot, PDF/PRD generator, transcription, account platform or fine-tuning | None proves the core question-finding outcome |
| D-05 | Use an **existing open-weight model** first; evaluate before elaborate UI | Model performance and value are the key uncertainties |
| D-06 | Primary user is a developer doing client discovery | Grounded in the builder's first-hand workflow |

## Proposed but unapproved choices

| ID | Recommendation | Main tradeoff | Checkpoint |
| --- | --- | --- | --- |
| P-01 | Single-page, responsive workbench with restrained style | Simple to use; design identity still undecided | Before front-end polish |
| P-02 | Ephemeral tab-session data; no database | Better data minimization; accidental refresh loses notes/answers | Before M1 |
| P-03 | Local React/TypeScript frontend + FastAPI/Pydantic backend + Ollama | Familiar/open tooling; user must run multiple processes | Before M1 |
| P-04 | Test quantized Qwen3 or Gemma model candidate | Hardware speed and output quality not yet verified | M0 |
| P-05 | Local working demo plus video rather than paid hosted inference | Cheap/private development; judges may prefer click-through deployment | Before ship |
| P-06 | Not-applicable requires a reason; Undo available | Slightly more UI logic, improves clarity | Before M2 |
| P-07 | Synthetic test suite initially covers booking, registration, checkout | Fast measurable start; not representative of all software projects | M0/M3 |

These rows must not be silently rewritten as confirmed choices in code or submissions. Resolve the consequential ones in conversation; routine implementation details can follow from the selected direction.

## Risk register, with mitigation and stop triggers

| Risk | Impact | Mitigation in current scope | Stop/rethink trigger |
| --- | --- | --- | --- |
| **Question quality is generic** | Product offers no advantage over a prompt | Compare against generic same-model prompt and checklist | No meaningful relevance improvement on human-reviewed cases |
| **Already-answered requirement is re-asked** | User trust drops | Canonical topic keys, deterministic filtering, paraphrase tests | Same exact resolved key survives filtering |
| **AI invents client statements** | Incorrect requirements and damage to trust | Verbatim-excerpt validation; label uncertainty; never mark suggestions as commitments | Fabricated quotes in reviewed results |
| **Sensitive client text leaks** | Commercial/confidential exposure | Local development, demo with synthetic notes, no raw request logs, no remote provider by default | Unapproved storage/transmission or public demo using real client notes |
| **Prompt injection in notes** | Model output contaminated by untrusted text | Separate task instructions from notes; validate output and forbid tools/actions | Notes cause unauthorized side effects or bypass validation |
| **Model too slow or unreliable** | Working demo blocked | Feasibility spike M0, alternative small model, honest fail states | Cannot produce structured useful output on available machine |
| **Secondary user causes scope growth** | Accounts/collaboration consume time | Same shared screen; lead can review manually | New auth/approval flow demanded before kernel works |
| **False commercial confidence** | Misleading submission | Record interview evidence and distinguish praise from repeat use/payment | Monetization claims rely only on guesses |

Severity labels are intentionally qualitative; probabilities and real-world frequencies have not been measured.

## Data and permission policy for development

1. **Synthetic notes first**. Never commit real client notes, identifiable meeting transcripts, customer names or credentials.
2. User-entered notes are **untrusted** data. Only approved developer actions update decisions.
3. Current draft proposes no server retention and ephemeral browser memory; implement and verify before claiming either.
4. Expose model/provider and what happens to input truthfully in the interface. If using any hosted inference later, revise the privacy statement and obtain appropriate authorization.
5. Don't collect real interview examples or publish feedback without consent, and don't place personal research notes in this public repo.
6. Public evaluation fixtures must be fictional or appropriately permissioned and redacted.

## Change control

To propose an additional feature, answer:

- Which exact [primary user](users.md) problem does it solve?
- Does the [one-minute journey](user-journey.md) need it?
- Which agreed feature will be **cut** to make room?
- How will we verify it against [MVP success](mvp.md)?
- Has the change been approved and reflected in PRD, spec, and implementation plan?

If these aren't answered, defer it. The aim is **a small complete product, not a document-driven large platform**.

## Pending approval order

1. Confirm one-screen interaction and visual feel.
2. Confirm data persistence/privacy behavior (ephemeral vs minimal local persistence).
3. Confirm demo runtime/hosting and which machine will run inference.
4. Confirm implementation stack **after M0 feasibility**.
5. Mark planning documents approved only after consequential decisions are settled.

### Risk background

- [OWASP LLM Top 10 (2025)](https://genai.owasp.org/llm-top-10/)
- [OWASP: Sensitive information disclosure](https://genai.owasp.org/llmrisk/llm022025-sensitive-information-disclosure/)
- [NIST: Generative AI risk profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
