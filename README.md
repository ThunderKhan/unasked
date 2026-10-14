# Unasked

**Find the questions you forgot to ask.**

Unasked is a planned, focused AI requirements-discovery tool for freelance developers and small software agencies. Give it notes from a conversation about **one web-app feature**, and it proposes up to **three high-impact implementation questions** the client may not have answered yet.

Instead of summarizing the conversation or generating a PRD, it helps the developer spot what wasn't discussed. Record the client's answer or dismiss an irrelevant suggestion, then re-analyze without repeatedly asking the same resolved question.

> **Project status:** Planning only. No working app or validated model results yet. All planning files are `status: draft`.

## Planning documents

**[Open the complete documentation index](docs/README.md)** for the recommended reading order and research rationale.

| Document | Purpose |
| --- | --- |
| [Scope](docs/scope.md) | Kernel, target problem, and hard scope boundary |
| [Users](docs/users.md) · [User journey](docs/user-journey.md) | Primary/secondary users and exact one-feature interaction |
| [PRD](docs/prd.md) · [MVP](docs/mvp.md) | Behaviors, acceptance criteria, measurable definition of done |
| [Technical spec](docs/spec.md) · [AI quality](docs/ai-quality.md) | Proposed architecture and rules for reliable model output |
| [Implementation plan](docs/implementation-plan.md) | M0–M3 build tasks, prerequisites and exit tests |
| [User validation](docs/user-validation.md) · [Decisions and risks](docs/decisions-and-risks.md) | Buyer discovery, assumptions, privacy and remaining choices |

**The MVP:** paste notes about one software feature → get 0–3 specific unanswered questions with reasons → record an answer or dismiss a question → re-analyze.

**Not building:** a chatbot, meeting recorder, PDF generator, CRM, feature graph, or multi-agent platform.

## Why open-weight AI?

An existing open-weight model interprets client language and recommends context-sensitive *missing decisions*, rather than relying solely on fixed checklists. Whether that actually improves developer outcomes is the project's main hypothesis and will be tested. The initial technical proposal uses local model inference so synthetic demos do not require sending text to a third-party API.

## Origin of planning process

The planning sequence adapts the [Devpost Learn: Build With AI Basics agent skills](https://github.com/challengepost/learn-ai-basics), especially `2-scope`, `3-prd`, and `4-spec`, to this DEV Community Hacktoberfest Side Hustle challenge project (not a Devpost challenge). Their curriculum is [MIT-licensed](https://github.com/challengepost/learn-ai-basics/blob/main/LICENSE) (Copyright (c) 2026 Devpost). These documents are our project drafts, **not** claims that the original curriculum has been formally completed or approved.

If using a compatible local coding agent, the upstream skills may be installed separately:

```bash
npx skills add challengepost/learn-ai-basics --all -y
```

Install is optional for reading or editing these documents. The skill's original workflow calls for explicit approval of each plan; our four drafts are being reviewed together.

## Privacy and status

Only use synthetic or appropriately anonymized client notes during initial development and public demos. Client notes may be commercially sensitive. Storage, inference hosting, and a public interactive deployment have not yet been finalized. Do not treat Unasked as an authoritative source of requirements.
