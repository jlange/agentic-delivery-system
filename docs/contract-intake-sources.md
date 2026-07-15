# Contract Intake Sources

This document defines acceptable input sources for contract intake.

## Purpose

Contract intake converts client-provided material into structured requirements, assumptions, questions, risks, and acceptance criteria.

The intake process must support multiple source types because not every contract begins from the same kind of material.

## Accepted source types

Accepted intake sources include:

- meeting transcripts
- meeting summaries
- call notes
- client emails
- proposals
- RFPs
- screenshots
- existing website or application links
- exported documents
- diagrams
- spreadsheets
- directories of project files
- manually written briefs

## Meeting transcripts

Meeting transcripts may be used when:

- recording consent has been handled
- the client understands the meeting is being recorded or summarized
- the transcript does not contain secrets, credentials, or unnecessary private data
- sensitive content is redacted before agent review when needed

Meeting transcripts should be treated as raw source material, not approved requirements.

## Intake directory

A client intake directory may contain multiple files for agent review.

Recommended structure:

- `source/`: original client-provided files
- `notes/`: human notes and call summaries
- `redacted/`: redacted copies safe for agent review
- `outputs/`: generated intake artifacts
- `decisions/`: client-approved decisions

## Agent handling

The requirements analyst should extract:

- explicit requirements
- inferred requirements
- assumptions
- open questions
- risks
- acceptance criteria
- out-of-scope items
- client decisions required

The agent must not treat transcript discussion, brainstorming, or tentative ideas as approved scope.

## Human review

A human must review intake output before it becomes approved project scope.

Unclear, sensitive, legal, pricing, compliance, privacy, or production-impacting items must be flagged for human decision.
