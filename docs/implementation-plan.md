---
doc: implementation-plan
status: draft
---

# Unasked — Implementation Plan

**Purpose:** Turn the existing [PRD](prd.md), [spec](spec.md), [MVP contract](mvp.md), [user journey](user-journey.md), and [AI quality contract](ai-quality.md) into **small, verifiable development slices**. Nothing here authorizes new product features. Stack/model choices are **proposed** until the open decisions are closed.

## Objective and hard boundary

**Definition of success:** A developer pastes notes about one requested web feature, sees up to three relevant missing implementation questions with reasons, records a genuine client answer or dismisses an irrelevant question, and re-analyzes **without the same resolved issue recurring**.

**In scope:** single-user browser workbench, one API endpoint using one existing open-weight LLM, answer/not-applicable/undo in current tab, reproducible baseline evaluation, clear errors and demo.

**Out of scope:** voice/live call capture; "asked" / "deferred"; project database, accounts, collaboration, PM tool integrations; chat, graphs, PDF/PRD generation, payments; training/fine-tuning; multiple agents. See [scope.md > Explicitly Cut](scope.md).

## Delivery rules

1. Build **vertical slices** in which a person can exercise functionality end to end; do not build the entire frontend then bolt on AI.
2. Run the M0 feasibility experiment **before polishing the interface**.
3. Keep each slice in a focused branch/PR or an equivalent reviewable commit with a test/demo of its acceptance criteria.
4. Prefer **working, tested simplicity** over extra options. Automated correctness checks for state transitions and API validation are essential, not optional polish.
5. No "done" checkmark based solely on files existing. Verify runtime and actual AI behavior before marking steps complete.
6. Keep all tests and demos free of real client-private data.

## Dependencies and recommended sequence

~~~text
D0: Confirm pending product/hosting choices
    │
    ▼
M0: Prove open-weight model can identify gaps / return valid JSON
    │
    ▼
M1: Notes → API → up to 3 real question cards
    │
    ▼
M2: Answer / not-applicable / undo → re-analysis
    │
    ▼
M3: Test baselines + recover failures + demo and README
~~~

**If M0 fails, stop adding UI.** Adjust the prompt/model or narrow supported feature types. The MVP's central claim depends on that kernel working.

## D0 — Prepare (documents and repository)

- [ ] Review/approve or modify the **three blocking user choices** listed in [decisions-and-risks](decisions-and-risks.md): visual treatment, persistence/privacy, demo runtime.
- [ ] Validate model availability, license, machine capability and local inference API; record exact tested model tag.
- [ ] Confirm repo uses one Python toolchain, one Node toolchain, and a documented way to run both; do not add containerization by default.
- [ ] Create synthetic test fixtures only, with no confidential names or customer data.

**Exit:** consequential choices tracked, repo clean, no sensitive data in git.

## M0 — Model feasibility and AI contract

**Reason:** The product fails if the model offers pleasant but irrelevant questions or repeats already settled decisions.

**Build/test tasks:**
- [ ] Create 3 **synthetic** seed conversations: booking, registration, checkout. Each has human-written critical gaps and explicitly answered issues.
- [ ] Define schema: \`feature_label\`, \`questions[0..3]\`, \`gap_key\`, \`question\`, \`why_it_matters\`, \`source_excerpt?\`, \`priority\`, \`caution\`. See [spec.md > Data Model](spec.md).
- [ ] Implement a **single-model** analysis probe (initial recommendation Ollama + locally available Qwen/Gemma candidate).
- [ ] Validate JSON/schema, safe excerpts, and duplicate/suppressed topic IDs in code—not merely in prompt text.
- [ ] Benchmark at least one cold/warm response on target hardware; note model version, failures, and latency.
- [ ] Run exact and paraphrased "already answered" test cases; fix errors before relying on the model.

**Exit test:** A reproducible terminal/API run with valid structured output identifies at least one human-labeled important gap across the seed set, and does not invent source quotes. Compare with a generic prompt and static checklist early; failing comparisons trigger reconsideration, not false claims of superiority.

**Candidate areas in spec:** \`backend/app/schemas.py\`, \`analysis.py\`, \`question_rules.py\`; \`evaluation/cases.json\`.

## M1 — Smallest end-to-end usable slice

**Implements:** [PRD > Enter Discovery Notes and Identify and Rank Missing Questions](prd.md).

- [ ] Scaffold minimal React + TypeScript + Vite frontend and FastAPI backend **if D0 architecture accepted**.
- [ ] \`POST /api/analyze\` and \`GET /health\` return validated, bounded responses. Restrict CORS to expected origin.
- [ ] Make one **editable textarea**, one Find action, and up to three cards with question, priority, implementation consequence and verified context.
- [ ] Use actual model output in normal path; synthetic examples must be visibly labeled and not silently substituted.
- [ ] Handle no notes, busy state, no important gap, timeouts, and invalid output honestly.
- [ ] Prohibit raw-note server logging; do not store notes or decisions on backend.
- [ ] Add API/schema tests plus at least one real inference smoke test (skip explicitly if model unavailable in CI, never silently pass a fake).

**Exit test:** From browser, paste previously unseen valid synthetic feature notes and display 0–3 genuine output cards; failures do not clear notes or masquerade as success.

**Candidate areas:** \`frontend/src/App.tsx\`, \`components/NotesPanel.tsx\`, \`QuestionCard.tsx\`, \`lib/api.ts\`, \`backend/app/main.py\`, \`tests/test_api.py\`.

## M2 — Complete the decision loop

**Implements:** [PRD > Record an Answer or Dismiss a Question, Re-analyze Context](prd.md).

- [ ] **Record answer** requires typed, nonblank client-confirmed text. Save locally in current session, separate from original notes.
- [ ] **Not applicable** requires an explanatory reason; save with canonical \`gap_key\`.
- [ ] **Undo** removes the local decision and makes the topic eligible for suggestion.
- [ ] **Re-analyze** sends notes and current decisions to **the same API**; reject stale responses if requests overlap.
- [ ] Enforce suppression by canonical topic key; write unit tests for exact duplicates, near-paraphrases and distinct-but-similar topics.
- [ ] If notes are edited after a decision, warn of potential staleness without erasing history automatically.
- [ ] Ensure tab refresh clears data if ephemeral mode is accepted; communicate this before users enter notes.

**Exit test:** In browser, resolve a synthetic double-booking question, re-analyze, and verify that the same issue is absent while another relevant question may appear. Undo restores eligibility.

**Candidate areas:** \`frontend/src/components/DecisionHistory.tsx\`, \`types.ts\`, \`App.tsx\`; \`backend/app/question_rules.py\`, \`tests/test_question_rules.py\`.

## M3 — Verify, harden and present

**Implements:** [MVP > Definition of Done and Evaluation Protocol](mvp.md) and [user-validation](user-validation.md).

- [ ] Create **10 expert-reviewed synthetic scenarios** (not just cherry-picked seeds), including notes that already answer tempting questions.
- [ ] Compare static checklist, generic prompt with the **same model**, and Unasked; report critical-gap recall@3, useful-question precision@3, re-ask rate, unsupported claims and latency with denominators.
- [ ] Check unsafe excerpts, prompt-like instructions in notes, massive input, malformed JSON, timeout, model offline, repeated analyze clicks and keyboard navigation.
- [ ] Run automated tests, frontend build, and a fresh-clone startup smoke test. Record evidence; do not check boxes merely because a script exists.
- [ ] Get 1–2 relevant developers to attempt the **one-feature** flow with synthetic data; capture genuine, permissioned feedback privately.
- [ ] Update README with real installation commands, actual model tag, limitations and **truthful** privacy description after verifying implementation.
- [ ] Record 1-minute happy-path demo **plus an unseen input**; disclose known failure modes and whether no public deployment exists.
- [ ] Prepare DEV Community submission material according to the actual [challenge rules](https://dev.to/challenges/hf26); avoid assuming the Devpost curriculum governs this challenge.

**Exit test:** the complete human-usable flow works on a clean local setup, the evaluation is repeatable, quality issues are reported transparently, and the walkthrough proves core behavior with a real open-weight model.

## Minimum testing matrix

| Test | Level | Expected result | Relevant docs |
| --- | --- | --- | --- |
| Empty/whitespace input | UI + API | No inference; readable validation error | [PRD](prd.md) |
| Booking double-booking omitted | Model evaluation | Valuable unresolved question may surface | [AI quality](ai-quality.md) |
| Explicit booking-conflict rule in notes | Model evaluation | Don't ask a redundant conflict question | [MVP](mvp.md) |
| Same gap phrased differently after answer | Rules + model | Same topic suppressed | [AI quality](ai-quality.md) |
| Dismiss with empty reason | UI | Block save | [User journey](user-journey.md) |
| Undo after answered | UI + rules | Question eligible again | [PRD](prd.md) |
| Invented source excerpt | Rules | Quote omitted/rejected, never fabricated | [AI quality](ai-quality.md) |
| Model times out / malformed response | API + UI | Honest failure, notes preserved | [Spec](spec.md) |
| Prompt injection embedded in notes | Security regression | Notes treated as untrusted data | [Risks](decisions-and-risks.md) |
| Refresh page | UI | Session cleared **if proposed policy approved** | [Decisions](decisions-and-risks.md) |

## Done criteria for every implementation slice

- [ ] Behavior satisfies the cited PRD requirement and fits the user journey.
- [ ] Deterministic tests pass; a manual real-model demonstration was made for AI features.
- [ ] Error/empty states work; no confidential content is logged, committed or shipped.
- [ ] README or spec updated if observed behavior differs from the planned contract.
- [ ] Diff contains no unrelated integrations, account infrastructure or "just in case" features.
- [ ] Any consequential decision change recorded in [decisions-and-risks.md](decisions-and-risks.md).

## What will **not** become separate tasks

No Figma design system, database migrations, rate-card subscriptions, role-based access, mobile application, full analytics dashboard, live transcription, autonomous agents, or model fine-tuning. None is necessary to prove Unasked's one valuable moment.

### Supporting research

- [Atlassian: user story mapping and minimum useful slices](https://www.atlassian.com/agile/product-management/story-mapping)
- [Atlassian: definition of done](https://www.atlassian.com/agile/project-management/definition-of-done/)
- [GitHub Docs: planning work with dependencies/tasks](https://docs.github.com/en/issues/tracking-your-work-with-issues/learning-about-issues/planning-and-tracking-work-for-your-team-or-project)
