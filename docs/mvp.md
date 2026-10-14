---
doc: mvp
status: draft
---

# Unasked — MVP Contract and Validation Plan

**Goal:** Prove a developer can identify an important missing implementation decision from a feature-discovery conversation **before implementation begins**.

This is an adapted, explicit execution companion to `scope.md`, `prd.md`, and `spec.md`. It is not a separately required document of the original Devpost Learn curriculum.

## The Single User Story

As a developer talking to a client about one web feature, I paste my notes and get up to three relevant, actionable questions I have not yet answered, then record a client answer so the same issue stops appearing.

## Definition of Done

- [ ] A real open-weight model analyzes arbitrary pasted notes; not a scripted demo response.
- [ ] It outputs 0–3 specific question cards with the implementation consequence of each.
- [ ] It never treats an inference as a confirmed client fact.
- [ ] A recorded non-empty answer removes the same underlying gap when re-analyzed.
- [ ] A not-applicable decision, with explanation, suppresses the same gap; Undo restores it.
- [ ] Empty notes, API failures, malformed model JSON, and no-useful-gap cases have honest UI states.
- [ ] One synthetic scenario and one unseen scenario can be shown in a short recorded demo.
- [ ] Test results, known failures, and baseline comparisons are documented; nothing is passed off as real customer traction.

## Hard Scope Line

**Build:** paste notes, analyze, three question cards, why they matter, answer/dismiss, re-analyze, minimal session state, testable API.

**Don't build:** recording, speech-to-text, full meeting lifecycle, asked/deferred tracking, chat, document/PDF export, feature dependency maps, accounts, database, billing, multiple agents, fine-tuning, CRM integrations.

The executable task order, dependencies and exit tests are in [implementation-plan.md](implementation-plan.md). Question scoring and output safety rules are in [ai-quality.md](ai-quality.md).

## MVP Delivery Slices

### M0 — Feasibility Before UI

- Verify model licensing and inference on available hardware.
- Run the proposed open-weight model on **three synthetic discovery scenarios**: booking, registration and checkout.
- Validate parseable structured output, important missing questions, and no invented explicit answers.
- If it fails, adjust model/prompt or narrow supported feature types *before* building a complex UI.

### M1 — End-to-End Thin Slice

- Minimal textarea → one API call → up to three cards.
- Empty/loading/error states and schema-validation tests.
- No decorative UI work before a functioning call.

### M2 — Closing the Loop

- Record client answer or not-applicable reason.
- Re-analyze with decisions; require resolved-gap suppression.
- Add Undo and repeat/duplicate tests, including paraphrased questions.

### M3 — Reliability and Demo

- Run evaluation suite, fix the highest-severity errors, and record a demo with synthetic notes.
- Write only claims supported by actual results; disclose limitations.
- Include installation/run instructions and a simple privacy statement.

## Evaluation Protocol

Create **10 human-reviewed synthetic conversations** (ideally 3–4 booking, 3 registration, 3–4 checkout), including:
- Explicit high-impact gaps;
- Notes where a tempting question **has already been answered**;
- Irrelevant topics, vague notes, and paraphrased answers.

For each case, reviewers record which decisions are genuinely consequential, which are already answered, and which suggestions would waste client time.

Compare three approaches using the **same input cases**:
1. Domain-specific static checklist (simple baseline).
2. Generic prompt to the **same underlying model**, "What important questions should I ask?" (LLM baseline).
3. Unasked's structured and stateful approach.

**Metrics to report, without inventing results:**
- `critical_gap_recall_at_3`: fraction of expert-labeled critical gaps appearing in top three.
- `useful_question_precision_at_3`: proportion of proposed questions a reviewer considers valid, unresolved, and valuable.
- `resolved_reask_rate`: previously answered/dismissed topics proposed again after re-analysis.
- `unsupported_claims`: invented client statements or fabricated quotes.
- `latency`: approximate processing time on the recorded demo hardware.

**Proposed gates, to calibrate after first cases:** zero fabricated quotations in the suite; zero deterministic re-asks for exact known `gap_key` values; at least one genuinely useful critical gap on most missing-gap cases; error states never imply success. Do not cherry-pick or claim statistical significance from ten small cases.

## One-Minute Demo Storyboard

1. **0–15s:** Enter synthetic notes about a booking feature, leaving double-booking unspecified.
2. **15–30s:** Analyze; show the high-impact question and why it matters.
3. **30–45s:** Record the client's answer ("only one confirmed booking per slot").
4. **45–60s:** Re-analyze; show that the same gap disappears and a different unresolved question may appear.

Have an unedited, unseen input demo available too. If the model cannot find a particular example reliably, fix the model/workflow rather than pretending it did.

## Commercial Hypothesis (Not Yet Validated)

**Buyer:** solo developer or small software agency handling repeated client discovery.

**Value proposition:** fewer follow-up clarification cycles and reduced implementation rework.

**Evidence still needed:** one or two developers try anonymized notes; they identify a specific useful question they had missed; at least one expresses concrete willingness to use again or pay. Their feedback is qualitative, not proof of revenue.

**Pricing concept:** possible per-session or low-cost subscription, **hypothesis only**; no pricing UI in MVP.

## Stop Rules

- If Unasked doesn't outperform a simple checklist or generic prompt on question relevance, **improve or reconsider the core approach**, not the interface.
- If model responses are consistently unreliable on the target machine, switch or simplify inference before further design work.
- If no potential developer finds a missed question valuable, do not claim validated commercial demand.
- No scope expansion without a documented trade: one feature added means another is cut.

## Shipping Readiness

Use a public repository, a short honest demo video, setup instructions, evaluation limitations, attribution of the open-weight model, and a concise explanation of why open-source AI is meaningfully involved. Confirm the **actual target challenge rules** separately; this planning template is adapted from a different curriculum.
