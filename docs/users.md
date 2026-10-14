---
doc: user-profiles
status: draft
---

# Unasked — Users, Roles and Jobs

**Source of truth for who Unasked serves.** Based on [scope](scope.md) and [PRD](prd.md). These are **provisional, behavior-based profiles**, not validated research personas or quotes from real interviewees.

## Primary user — Developer leading feature discovery

**Role:** Freelance developer or a software developer at a small agency who asks a client about **one web-app feature** before estimating or building it.

- **Job to be done:** "When I finish a client feature discussion, help me spot the important implementation decisions nobody clarified so I can ask the right follow-up questions before development starts."
- **Trigger:** After a meeting, during a pause in discussion, or while reviewing meeting notes.
- **Current workaround (hypothesis):** Memory, personal checklists, scattered notes, generic LLM prompts, or another clarification call.
- **Main anxieties:** Asking irrelevant questions, slowing a meeting, exposing sensitive client notes, or mistakenly treating AI suggestions as agreed requirements.
- **Success:** A small number of *new, high-impact* questions relevant to the actual feature, with clear implementation consequences. A confirmed answer is not asked again.
- **Constraints:** Little time, incomplete notes, intermittent model availability; must remain in control of what is asked and recorded.
- **Actions inside MVP:** Paste/edit notes, analyze, read up to three question cards, record client's answer, dismiss with a reason, undo, re-analyze.
- **Non-actions:** No video recording, automatic customer outreach, document generation, or managing multiple simultaneous projects.

**Evidence:** This role and problem are informed by the builder's own software internship and client conversations. Frequency, severity, and willingness to pay have **not** been independently validated. See [user-validation](user-validation.md).

### Primary scenario

The client says, "Users should pick available slots and receive email confirmation." The developer realizes no one defined what happens when two people choose one slot. They ask the client, record "Only the first confirmed booking is accepted," and re-analyze. The same underlying question should disappear.

## Secondary user — Founder, tech lead or senior developer reviewing discovery

**Role:** A person who attends a client call with the primary user or later checks whether the team has clarified important decisions.

- **Job:** Review the prioritized follow-up questions and judge whether they warrant contacting the client.
- **Goal:** Reduce avoidable rework without creating lengthy requirements paperwork.
- **Interaction in MVP:** Can **look at the same single-user workspace** during an in-person review or screenshare. No separate login, reviewer mode, approval workflow, assignment, notifications, or shared storage.
- **Success:** Can understand why a suggested question matters, and see which client answers were actually confirmed.
- **Caution:** Being a valuable stakeholder does not make them a second engineered user interface.

This role is a **secondary user hypothesis**, not established buying behavior.

## Buyer — Solo practitioner or small-agency owner

The paying customer, if commercial demand exists, is likely to be the practicing developer or the agency owner who pays for developer tooling. The buyer and primary user may be the same person.

**Economic hypothesis:** A useful missing question prevents a follow-up cycle or expensive rework often enough to justify a small payment. Do not state that this has been demonstrated.

The MVP contains **no subscription, payment, billing, seats or pricing screens**.

## Client stakeholder — Not a product user

The client's requirements and answers are central to Unasked, but the **client does not use the application in the MVP**. The developer asks questions in the real world and types back only what was confirmed. There is no client portal or automatic interviewing.

## Explicitly outside the target audience for MVP

- Enterprise business-analysis teams needing formal requirements traceability.
- Sales organizations running sales-call coaching.
- Full project management and ticketing teams.
- Non-software domains such as legal discovery or medical consultation.
- Customers expecting Unasked to guarantee complete specifications.

## User-centered acceptance criteria

| Need | Observable evidence | Source |
| --- | --- | --- |
| Developer needs quick prioritization | At most three relevant questions; no noisy full checklist | [PRD](prd.md) |
| Developer needs confidence | Reasons connect each question to a potential implementation decision, not invented client statements | [AI quality](ai-quality.md) |
| Developer needs control | Answers and dismissals are explicit, reversible decisions | [User journey](user-journey.md) |
| Founder/lead needs an understandable review | Questions and saved answers are visible in one workspace without an account | [PRD](prd.md) |
| Everyone needs confidentiality | Synthetic/anonymized demo input and truthful processing/storage notice | [Decisions and risks](decisions-and-risks.md) |

## Questions to validate with users

1. After which type of call would they realistically open this? Would they paste notes mid-meeting or afterward?
2. What do they currently do when an important requirement is missing?
3. Which missing requirements have actually caused rework, and how was the problem detected?
4. Would top-three ranked prompts reduce their effort, or would the interface add an unnecessary step?
5. Who would authorize payment and what concrete alternative would Unasked replace?

**Do not fabricate ages, salaries, company names, interview quotes, or purchase intent.** Revise these profiles only when user evidence warrants it.

### Research approach

The profile emphasizes user goals and constraints rather than demographic decoration, following [Google PAIR's User Needs + Defining Success](https://pair.withgoogle.com/guidebook-v2/chapters) and [Atlassian's story mapping](https://www.atlassian.com/agile/product-management/story-mapping).
