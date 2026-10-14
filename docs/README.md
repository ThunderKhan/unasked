# Unasked — Planning and Build Documentation

> **Status:** Design and implementation **drafts**, not an approved or completed product. No claims of a working model, user interviews, or commercial traction.

**Project:** Find the questions you forgot to ask. **One user, one web-app feature, at most three unanswered questions, and a complete answer/dismiss → re-analyze loop.**

## Reading order (source of truth)

| Step | Document | Question it answers | Owns |
| --- | --- | --- | --- |
| 1 | [Scope](scope.md) | Why build this, for whom, and what is cut? | Kernel and product boundary |
| 2 | [User profiles](users.md) | Who is primary, secondary, buyer, and not an app user? | Roles and jobs-to-be-done |
| 3 | [User journey](user-journey.md) | What happens from opening the app to re-analysis? | End-to-end flow and statuses |
| 4 | [PRD](prd.md) | Exactly what does the interface do and how is it accepted? | Product behavior and visual choices |
| 5 | [MVP and validation contract](mvp.md) | What is "done" and what must we measure? | MVP scope and success criteria |
| 6 | [Technical specification](spec.md) | How will code, API, state and inference fit together? | Proposed architecture/contract |
| 7 | [AI quality](ai-quality.md) | What counts as a valuable gap, and what must the model never do? | Output quality and AI failure rules |
| 8 | [Implementation plan](implementation-plan.md) | What gets built first and how does each slice pass? | Task sequencing and exit gates |
| 9 | [User validation](user-validation.md) | Do real developers find this useful enough to return or pay? | Interviews and product-market hypotheses |
| 10 | [Decisions and risks](decisions-and-risks.md) | Which choices are settled, proposed or dangerous? | Decision log, assumptions and privacy guardrails |

**Do not copy requirements into new documents unnecessarily.** Update the owning document; other docs should link to it. The planning files have \`status: draft\` until actual user review; a GitHub merge does **not** imply product approval.

## Core loop: one complete experience

~~~text
Paste notes (one feature)
      ↓
Analyze using a real open-weight model
      ↓
Show up to 3 important *unanswered* questions + why
      ↓
Record a confirmed client answer OR dismiss as not applicable
      ↓
Re-analyze, omitting resolved topics
~~~

The primary **developer** uses the app. A founder/tech lead may review the same screen as a **secondary user**. The client supplies answers outside the app. No accounts, "reviewer roles", outreach, PRD generator, full feature maps, or live meeting transcription.

## What was missing and why these documents were added

| Gap in the original four docs | Response | Why not another large document? |
| --- | --- | --- |
| Roles were implied rather than explicit | [users.md](users.md) | Provisional profiles, no invented demographics or market evidence |
| PRD described a journey but lacked full interaction-state walkthrough | [user-journey.md](user-journey.md) | One feature story, not an entire UX mapping program |
| MVP milestones were high-level | [implementation-plan.md](implementation-plan.md) | Concrete tasks, dependencies, acceptance and test gates |
| Model behavior was distributed between spec and MVP | [ai-quality.md](ai-quality.md) | One place for question quality, provenance and re-ask rules |
| Commercial value was a hypothesis with no outreach procedure | [user-validation.md](user-validation.md) | Short real-user interview/test, not a market-sizing report |
| Unapproved recommendations and privacy threats were easy to miss | [decisions-and-risks.md](decisions-and-risks.md) | One small change-control and confidentiality reference |

## Research basis

This is a **documentation-method audit**, not completed market/customer research:

- **User journey → minimum deliverable slice:** [Atlassian — Story mapping](https://www.atlassian.com/agile/product-management/story-mapping) encourages linking user goals and steps to MVP delivery.
- **Definition of done:** [Atlassian — Definition of Done](https://www.atlassian.com/agile/project-management/definition-of-done/) argues for shared verifiable completion criteria.
- **AI trust, control and error handling:** [Google People + AI Guidebook](https://pair.withgoogle.com/guidebook-v2/chapters) recommends communicating uncertainty, reversible actions, and graceful failure.
- **Measure AI quality:** [NIST AI RMF — Measure](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/) emphasizes benchmarking, verification and reporting limitations.
- **LLM risk coverage:** [OWASP LLM Top 10 (2025)](https://genai.owasp.org/llm-top-10/) addresses prompt injection and sensitive information disclosures.
- **Work tracking:** [GitHub — Plan and track work](https://docs.github.com/en/issues/tracking-your-work-with-issues/learning-about-issues/planning-and-tracking-work-for-your-team-or-project) supports small, traceable tasks and dependencies.

These sources inform **how we organize work**; they do **not** validate willingness to pay or show Unasked performs better than existing tools.

## Intentionally **not** added

- **A separate enterprise SRS/BRD:** would duplicate the focused PRD.
- **An independent 30-page business plan or pricing deck:** no customer evidence yet; user validation already specifies the test.
- **A complete design system and multi-screen wireframes:** the MVP has one workbench and unresolved visual direction.
- **A second evaluation report with fake scores:** technical metrics live in [mvp.md](mvp.md) and rating rules in [ai-quality.md](ai-quality.md); results will be created **after actual tests**.
- **Database schemas, auth architecture, collaboration or cloud operations playbooks:** those systems aren't being built.
- **A separate full test strategy:** essential tests and smoke checks already live in [implementation-plan.md](implementation-plan.md) and [ai-quality.md](ai-quality.md).

## Start building only after the first gate

Read [decisions-and-risks.md > Pending approval order](decisions-and-risks.md), then perform **M0: model feasibility** from [implementation-plan.md](implementation-plan.md). If the model cannot reliably surface real missing questions, change inference or narrow coverage **before** adding UI polish.

**Privacy:** all public demos and version-controlled fixtures use fictional/anonymized notes. Do not put client-confidential material in the public repo.
