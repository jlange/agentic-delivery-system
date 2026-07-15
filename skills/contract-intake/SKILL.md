---
name: contract-intake
description: Use when converting client discovery material into structured contract intake outputs, including requirements, assumptions, risks, open questions, acceptance criteria, and client decisions needed.
---

# Contract Intake Skill

Use this skill at the start of a client project or when new discovery material arrives.

## Inputs

Acceptable inputs include:

- meeting transcripts
- meeting summaries
- call notes
- client emails
- proposals
- RFPs
- screenshots
- existing site or app links
- exported documents
- diagrams
- spreadsheets
- directories of project files
- manually written briefs

## Safety checks

Before analysis:

1. Confirm the material is appropriate for agent review.
2. Flag secrets, credentials, private customer data, regulated data, or unnecessary sensitive information.
3. Prefer redacted copies when sensitive content is present.
4. Treat all source material as unapproved until human review.

## Process

1. Identify source files and their purpose.
2. Summarize the project goal in neutral language.
3. Extract explicit requirements.
4. Identify inferred requirements separately.
5. List assumptions.
6. List open questions.
7. Identify risks and dependencies.
8. Draft acceptance criteria.
9. Identify out-of-scope items.
10. Identify client decisions required.
11. Flag legal, privacy, compliance, billing, production, or credential issues for human review.

## Output format

Use this structure:

# Contract Intake Output

## Source Material

List source files or inputs reviewed.

## Project Summary

Briefly summarize the apparent project.

## Explicit Requirements

Use stable IDs:

- REQ-001:
- REQ-002:

## Inferred Requirements

Use stable IDs only if useful:

- INF-001:
- INF-002:

## Assumptions

- ASM-001:
- ASM-002:

## Open Questions

- Q-001:
- Q-002:

## Risks

- RISK-001:
- RISK-002:

## Acceptance Criteria Draft

- AC-001:
- AC-002:

## Out Of Scope

- OOS-001:
- OOS-002:

## Client Decisions Required

- DEC-001:
- DEC-002:

## Human Review Required

List any items that require human judgment before planning or implementation.

## Rules

- Do not treat brainstormed ideas as approved scope.
- Do not invent requirements.
- Do not quote long transcript sections unless necessary.
- Do not include secrets or sensitive client data in the output.
- Do not estimate price, timeline, or legal obligations unless explicitly asked.
- Do not proceed to architecture or implementation until scope is reviewed.
