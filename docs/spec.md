---
doc: spec
status: draft
---

# Unasked — Technical Spec (Proposed)

> This is a buildable **proposal**, not an approved architecture. Based on `scope.md` and `prd.md` drafts; resolve the documented user decisions before implementation.

## How This Works, In Plain Language

A developer pastes notes about one web-app feature. The browser sends those notes and any confirmed answers/dismissals to a small local server. The server asks **one existing open-weight language model** to identify important decisions that remain unclear. It checks that the reply has the expected structure, removes duplicates or previously resolved topics where possible, and returns up to three question cards. The developer records what the client actually answered; the next request includes that decision.

We are **not training a model**, building a multi-agent system, or secretly automating the meeting. The human remains the source of truth.

## The Core Journey Through the System

Implements `prd.md > The Core Journey`.

1. `NotesPanel` accepts plain text and validates non-empty input.
2. `App` sends `POST /api/analyze` with notes and the current decision history.
3. `analysis.py` assembles a restricted instruction and calls an Ollama model with a structured response schema.
4. `schemas.py` validates the response; `question_rules.py` deduplicates, checks evidence excerpts, excludes resolved topic IDs, and selects at most three questions.
5. The browser renders `QuestionCard` instances with rationale and contextual evidence.
6. `DecisionHistory` records an answer or a not-applicable reason; the UI keeps decisions for this tab session.
7. Re-analysis sends the new decisions, so an answered issue is not asked again. No action contacts the client.

## Stack

**Recommended, subject to approval:**

| Part | Choice | Reason / tradeoff |
|---|---|---|
| Frontend | React + TypeScript + Vite | Familiar, quick to implement, easy to demo. [React](https://react.dev/), [TypeScript](https://www.typescriptlang.org/docs/), [Vite](https://vite.dev/guide/) |
| Styling | Tailwind CSS, restrained | Fast responsive layout; visual direction remains open. [Tailwind](https://tailwindcss.com/docs/installation) |
| API | Python + FastAPI + Pydantic | One endpoint with robust input/output validation. [FastAPI](https://fastapi.tiangolo.com/), [Pydantic](https://docs.pydantic.dev/latest/) |
| AI runtime | Ollama, local | Lets us use a real open-weight model without keys or per-call costs; may be slow on smaller hardware. [Ollama](https://docs.ollama.com/) |
| Initial candidate | Quantized Qwen3 4B (or comparable open-weight instruct model) | **Not yet validated** on this hardware or for consistent JSON; benchmark first. [Qwen models](https://ollama.com/library/qwen3) |
| Session decisions | React in-memory state | No accounts/database; refreshing loses the session (must be visible in UI). |
| Evaluation | Versioned synthetic test cases and simple script | Measures output usefulness instead of cherry-picking one demo. |

Do not hardcode a model choice as a product guarantee. Check actual model licensing, available tags, structured-output support, throughput and hardware requirements in an early spike. Lower-capacity models are not automatically reliable at semantic gap detection.

## Where It Runs and How Someone Tries It

**Default recommendation:** local app, local inference, synthetic demo notes. No hosted AI dependency.

Proposed development commands after the skeleton exists:

```bash
# Start Ollama (if not already running), then fetch selected model
ollama serve
ollama pull qwen3:4b

# API (from backend/)
python -m venv .venv
# Activate the environment for your OS
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000

# Web (from frontend/ in a separate shell)
npm install
npm run dev
```

Visit `http://localhost:5173`; verify the API at `http://localhost:8000/health`. These commands are **planned**, not tested; source files do not exist yet. Point the server to the configured local model and restrict CORS to the local Vite origin.

**Shipping:** record a short demo and link the public repository. A deployed interactive demo is a **separate pending decision**; if needed, choose a model-hosting plan only after local accuracy is established. Do not suggest client-private notes be pasted into an untrusted public demo.

## Look and Feel

Implements `prd.md > Screens and Layout` and `prd.md > Look and Feel`.

- Single workbench; on desktop notes and question cards can sit beside each other; on mobile stack vertically.
- Emphasize the next actionable question, not decorative AI charts.
- Clear text hierarchy, short explanations, visible buttons and status labels.
- Show that notes are processed locally **only when verified by the actual architecture**.
- Typography and palette are not decided; treat restrained professional styling as a **proposal**.

## Components

### NotesPanel (frontend)

Implements `prd.md > Enter Discovery Notes`.

Controlled text area, blank-input validation, explicit analyze action, fictional example, local-session notice. Does not start recording or upload files.

### QuestionCard (frontend)

Implements `prd.md > Identify and Rank Missing Questions`.

Displays one question, priority/rationale, optional verified source excerpt, and inline actions. Never show unsupported certainty as a confirmed client requirement.

### DecisionHistory (frontend)

Implements `prd.md > Record an Answer or Dismiss a Question`.

Maintains answered and not-applicable decisions (including user explanation), enables Undo, and exposes exactly what will be sent on re-analysis.

### AnalysisController (frontend)

Implements `prd.md > Re-analyze Context` and `States and Boundaries`.

Owns request/loading/error UI, aborts or ignores stale responses, preserves notes on failure, and keeps only current-session decisions in memory.

### AnalysisAPI (backend)

Implements `prd.md > Identify and Rank Missing Questions`.

Stateless `POST /api/analyze` endpoint; validates incoming text/decision sizes; never persists or logs raw notes. Separates instructions from user-supplied notes; notes are **data**, not commands.

### ModelGateway (backend)

Implements `prd.md > Identify and Rank Missing Questions`.

Calls `POST http://localhost:11434/api/chat` with `stream: false`, a configured model and an explicit JSON response format/schema where supported. Parses `message.content`; Pydantic validates it. If model/tooling support differs, document and fix at M0 rather than fabricating success.

References: [Ollama chat API](https://docs.ollama.com/api/chat), [Ollama structured outputs](https://docs.ollama.com/capabilities/structured-outputs).

### QuestionRules (backend)

Implements `prd.md > Identify and Rank Missing Questions` and `Record an Answer or Dismiss a Question`.

- Clamp output to three; reject empty/malformed/duplicate question strings.
- Keep question IDs stable by **decision topic**, not display wording. Begin with small supported feature categories; use a canonical `gap_key` and conservative semantic duplicate screening.
- Filter gap keys already answered/dismissed; do not suppress an unrelated topic because one similar word appears.
- Verify `source_excerpt` is a literal substring of the notes or omit it; never manufacture quotations.
- Flag uncertainty instead of pretending completeness.

**Limitation:** deterministic filtering cannot guarantee semantic equivalence across arbitrary client language. Validate against paraphrases in evaluation.

## Data Model

**Request — `POST /api/analyze` (illustrative contract):**

```json
{
  "notes": "Client wants a booking feature with confirmation emails.",
  "decisions": [
    {
      "gap_key": "booking.cancellation_policy",
      "question": "Can customers cancel?",
      "status": "answered",
      "detail": "No cancellation after confirmation."
    }
  ]
}
```

**Response — accepted only after schema validation:**

```json
{
  "feature_label": "Appointment booking",
  "questions": [
    {
      "gap_key": "booking.double_booking",
      "question": "What happens if two customers select the same time slot?",
      "why_it_matters": "The booking rules and data integrity depend on this choice.",
      "source_excerpt": "Client wants a booking feature",
      "priority": 1
    }
  ],
  "caution": "Suggestions need developer verification."
}
```

`decisions.status` is `answered | not_applicable`. `detail` is required non-empty. The model generates candidate `gap_key` values, but the app validates shape, canonicalization and duplication. Reject impossible status transitions; editing/undoing a decision happens locally. Do **not** persist raw notes on the server. Closing/reloading clears browser state under the proposed MVP behavior.

**Data provenance:** source excerpts support what topic was mentioned, **not** proof that an omitted rule is missing; the client must confirm whether a gap actually exists.

## File Structure

```text
unasked/
├── frontend/
│   ├── src/
│   │   ├── App.tsx                 # Single discovery workbench + session actions
│   │   ├── components/
│   │   │   ├── NotesPanel.tsx
│   │   │   ├── QuestionCard.tsx
│   │   │   └── DecisionHistory.tsx
│   │   ├── lib/api.ts              # POST /api/analyze
│   │   └── types.ts                # Question + decision shapes
│   └── package.json
├── backend/
│   ├── app/
│   │   ├── main.py                 # FastAPI route + health
│   │   ├── schemas.py              # Pydantic request/response contracts
│   │   ├── analysis.py             # Model gateway + constrained instructions
│   │   └── question_rules.py       # filtering + de-duplication
│   ├── tests/
│   │   ├── test_api.py
│   │   └── test_question_rules.py
│   └── requirements.txt
├── evaluation/
│   ├── cases.json                  # Curated synthetic notes + ground truth
│   └── evaluate.py                 # Baseline vs Unasked comparison
├── docs/                         # DEV Challenge planning documentation
│   ├── README.md
│   ├── scope.md
│   ├── users.md
│   ├── user-journey.md
│   ├── prd.md
│   ├── mvp.md
│   ├── spec.md
│   ├── ai-quality.md
│   ├── implementation-plan.md
│   ├── user-validation.md
│   └── decisions-and-risks.md
├── .gitignore
└── README.md
```

File structure is planned, not evidence of implemented code.

## External Services and Dependencies

- **Ollama local service:** `POST /api/chat`; runs on localhost, no external API key. Configure model with environment variable; do not store client notes in request/response logs. Verify model availability, JSON-schema behavior and runtime memory limits at M0.
- **FastAPI server:** browser calls `POST /api/analyze`, JSON in/out as above. Reject oversized input, empty text, invalid decision status and malformed payload with readable errors; constrain origins for browser access.
- **Public deployments:** none required in current proposal. If selected, reassess inference hosting, security, costs, rate limits, content retention and privacy disclosure before building that path.

## Important Failure Modes

1. **Model hallucinates a requirement or excerpt** → never mark model output as a fact; validate excerpts and show uncertainty; exclude unsupported quotations.
2. **Already resolved question reappears with new wording** → canonical gap keys, compare against decisions, cover paraphrases in tests; surface residual duplicates as correctness bugs.
3. **Model unavailable, slow, or emits bad JSON** → time-out/retry UI; keep notes/decisions untouched; do not show invalid results or substitute a fake successful answer.
4. **Prompt injection inside client notes** → treat input as untrusted data; validate schema and enforce all decisions server-side, not as model suggestions. No claim of complete injection immunity.

## What Was Simplified and Why

- Explicit **paste and analyze** instead of live recording — isolates the reasoning problem.
- **One open-weight model call** instead of fine-tuning, agents or retrieval — cheapest proof before optimizing.
- **Single tab-session state** instead of persistence — avoids accounts and handling long-lived sensitive notes.
- **Up to three question cards** instead of a comprehensive requirements checklist — optimizes for what to ask next.
- **One feature at a time** instead of multi-project tracking — smaller context and measurable evaluation.

## Decisions and Open Issues

**Established by earlier discussion:** narrow missing-question task, existing open-weight model, interactive non-chat output, inline answer/dismiss loop, strong scope and validation priority.

**Recommended but NOT accepted yet:** React/Vite/TypeScript + FastAPI + Ollama; Qwen3 4B as first candidate; local-only inference demo; ephemeral session; exact interface arrangement.

**A real uncertainty already raised:** whether to fine-tune, make an agent skill, or build an application. The lean answer is to start with structured inference in an interactive web app; model evaluation will determine whether further model work has evidence behind it.

**Blockers to mark `approved`:** runtime/demo deployment preference; privacy/persistence preference; visual identity; model feasibility on target hardware. Minor library versions can be pinned during build setup.

**Verification gate:** Run the M0 model experiment before spending time on detailed UI. If structured output and question quality are inadequate, reduce model burden or change the proposed inference approach before proceeding.
