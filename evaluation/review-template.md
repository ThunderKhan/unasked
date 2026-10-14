# Unasked M0 — Human Review Sheet

**Status: Not evaluated.** Fill this only after running `python -m evaluation.probe` on the actual chosen Ollama model. Never invent metrics or copy unapproved client notes into a public report.

## Run metadata

- Date:
- Reviewer(s):
- Machine (RAM, GPU model/VRAM):
- Ollama version:
- Exact model tag / digest / quantization:
- Number of runs (cold/warm):
- Notes synthetic or approved/anonymized:
- Result file path (local only):

## Per-case review

| Case | Generic baseline: useful questions / 3 | Unasked: useful questions / 3 | Important gold topics in top 3? | Any already-answered re-asked? | Any fabricated client fact/quote? | Time (seconds) |
| --- | --- | --- | --- | --- | --- | --- |
| Booking | Not evaluated | Not evaluated | Not evaluated | Not evaluated | Not evaluated | Not measured |
| Registration | Not evaluated | Not evaluated | Not evaluated | Not evaluated | Not evaluated | Not measured |
| Checkout | Not evaluated | Not evaluated | Not evaluated | Not evaluated | Not evaluated | Not measured |

**Human rating rubric:** 2 = useful, unresolved, actionable and important; 1 = marginal; 0 = irrelevant, already answered, vague or invented. Rate semantic equivalence, not textual similarity. Gold topics in `cases.json` are preliminary seed annotations, not independent ground truth.

## Decision-history test

- Booking double-booking answered: Did any semantically equivalent question recur?
- Registration password recovery answered: Did any equivalent question recur?
- Checkout failed-payment answered: Did any equivalent question recur?
- Do different `gap_key` labels mask the same resolved topic?
- Did a distinct useful remaining gap still surface when appropriate?

## Notes on failures

- Exact generated question and case:
- What was wrong / important omitted:
- Was the error model reasoning, schema, source excerpt, or deterministic filtering?
- Proposed smallest corrective change:

## Decision

- [ ] **GO** — real output is schema-valid, grounded, repeatedly helpful, and decision history demonstrably works.
- [ ] **REVISE** — kernel seems promising but a specific reliability issue blocks the next slice.
- [ ] **STOP / RETHINK** — no credible usefulness advantage over generic baseline or checklist.

Rationale and evidence:

## Follow-up before claiming production quality

Expand to the 10 human-reviewed synthetic cases in `docs/mvp.md`. A three-case spike is a **feasibility screen, not reliable model-quality certification**.
