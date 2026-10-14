---
doc: user-validation
status: draft
---

# Unasked — Problem and Buyer Validation

**Purpose:** Check that people actually experience this narrow problem and that Unasked is meaningfully useful **before claiming a viable Side Hustle**. This document covers **customer discovery and usability**, whereas [mvp.md](mvp.md) defines technical evaluation metrics.

## What we know versus what we assume

| Claim | Current evidence | Next validation step |
| --- | --- | --- |
| A developer can miss important client requirements | Builder's first-hand experience | Interview 2–3 other practitioners and request recent concrete examples |
| Top-three targeted questions reduce confusion | Plausible hypothesis only | Observe a developer using synthetic notes |
| An open-weight model beats a checklist or generic prompt | **Not measured** | Run the matched baseline tests in [mvp.md](mvp.md) |
| Agency owner or freelancer would pay | **Not demonstrated** | Ask what they'd stop using or pay to replace after testing |
| Client data should be handled cautiously | Sensitive project information is plausible | Use synthetic input first and require consent for any real notes |

Avoid pretending that the personal experience of the builder is a representative market study.

## Recruiting for a fast but honest signal

- **Priority:** two independent freelance developers or small-agency developers who have personally led requirement calls.
- **Useful additional perspective:** one senior developer or founder who reviews feature requirements.
- **Not enough by itself:** friends who have never collected requirements, hackathon judges, or users praising a mockup.
- Do not ask anyone for actual confidential client records. Bring a **synthetic** scenario or let them anonymize their own examples; get explicit permission before retaining anything.

The initial sample is tiny and nonrepresentative. Describe any findings as **interview observations**, not market-level facts.

## 10-minute problem interview (before demo)

1. "Tell me about the most recent client feature discussion you led. What was the feature?"
2. "What information turned out to be missing after the meeting? How was it discovered?"
3. "What happened next—another call, delays, rework, or no meaningful consequence?"
4. "What do you use to prepare questions or check completeness now?"
5. "When would it be acceptable to paste notes into an external tool? What information would you remove?"

**Probe for actual past behavior**, not agreement with the pitch. Avoid leading with "Wouldn't AI solve that?"

## 10-minute task observation (after demo is working)

Ask them to act as the developer for a fictional appointment-booking request.

- Present the notes; do not explain where to click.
- Ask them to find one genuinely valuable missing question.
- Have them record a client answer and re-analyze.
- Ask what felt wrong, distracting, or missing. Note any place the UI implies the AI *knows* rather than *suggests*.
- Ask them to rank Unasked against their **existing workaround**, not against doing nothing.

**Capture:** task completion, confusion points, useful question found (yes/no + why), repeat-question mistakes, and observed time where feasible. Never manufacture scores.

## Buyer signal (after they have tried it)

Use non-leading questions:

- "What would you use instead if this disappeared tomorrow?"
- "Would this replace any work you currently pay for, or only add a step?"
- "Who in your team could approve payment for developer tooling?"
- "What is the smallest repeated workflow where this would have enough value to justify a fee?"
- "Would you commit to a second trial with your own anonymized notes?"

**Stronger than praise:** an agreed second trial, repeat voluntary use, a concrete budget conversation, or payment. No checkout is needed in this MVP.

## Minimal private evidence log

Create notes **outside the public repository** for real interviews (never names/emails without permission); publish only aggregate or anonymized observations with permission.

| Test ID | Role | Recent real problem described? | Useful gap found? | Confusion or failure | Real next-step commitment | Notes retained with consent? |
| --- | --- | --- | --- | --- | --- | --- |
| P01 | To recruit | — | — | — | — | — |
| P02 | To recruit | — | — | — | — | — |
| S01 | Optional lead | — | — | — | — | — |

These are **empty slots**, not completed interviews.

## Decision after research

- **Proceed:** at least one user identifies a nontrivial omitted decision and independently wants to try again; AI evaluation remains acceptable.
- **Revise:** questions are useful but too generic or repetitive; investigate a narrower software feature type or adjust ranking.
- **Stop/rethink:** the workflow adds more effort than a normal checklist, reviewers cannot distinguish its suggestions from generic AI, or nobody in this small sample has experienced the targeted pain. Do not manufacture a win to satisfy the challenge.

**Not proof of willingness to pay:** users saying "cool", liking the interface, or agreeing with a leading question.

### Research foundation

User-needs-first design and responsible input: [Google PAIR chapters](https://pair.withgoogle.com/guidebook-v2/chapters) and [data/evaluation](https://pair.withgoogle.com/guidebook-v2/chapter/data-collection/). This protocol is tailored to this project, not a claim of independently conducted interviews.
