---
name: architecture-recommendation
description: Use after contract intake has been reviewed and approved to convert structured requirements and client decisions into architecture, stack, MVP, risk, and project-shape recommendations before any implementation work begins.
---

# Architecture Recommendation

Use this skill after `contract-intake` has produced intake outputs and the human operator has reviewed scope decisions.

## Inputs

Read only approved project material, typically:

- `intake/outputs/contract_intake_output.md`
- `intake/decisions/intake_review_checklist.md`
- Any explicitly approved supplemental notes under the client workspace

Before reading source material, confirm the intake review checklist records approved
scope and stable `REQ-###` and `AC-###` identifiers. Do not assign new meaning to an
existing ID. If approved material lacks stable IDs or contradicts itself, report a
blocking question and stop.

Do not read unrelated client folders, `/mnt/c`, home directories, credentials, or unapproved source material.

## Data-Handling Gate

The intake review must explicitly declare:

- allowed paths
- forbidden paths
- whether raw sources may be reviewed
- whether redaction is required
- whether client data may be sent to external AI systems

Do not infer permission from file availability. Review only declared allowed paths.
If any declaration is absent, contradictory, or marked pending, treat it as a blocker.

## Workflow

1. Confirm the intake output and review checklist exist.
2. Summarize the approved project goal and MVP scope.
3. Separate approved scope from deferred scope, blocking unresolved requirements, and
   non-blocking open questions. A question is blocking when its answer could materially
   change system shape, boundaries, data handling, security, hosting, paid services,
   accessibility, backup/recovery, or verification. If any blocker remains, produce only
   the blocker analysis, set authoring status to `blocked`, and do not make a final recommendation.
4. Identify likely users, workflows, data entities, integrations, permissions, and operational constraints.
5. Recommend the project shape:
   - static site
   - automation script
   - internal tool
   - modular monolith
   - full web application
   - other justified shape
6. Define system/component boundaries, trust boundaries, and end-to-end data flows.
7. Apply `docs/target-technical-stack.md` as the default. Any deviation must cite at
   least one approved `REQ-###` and explain the tradeoff.
8. Record an ADR for every material tradeoff affecting cost, complexity, security,
   privacy, accessibility, portability, hosting, backup/recovery, or maintainability.
9. Map every material `REQ-###` and `AC-###` to components or decisions and a
   verification approach. Missing mappings are blockers to approval.
10. Define an execution plan with phases, dependencies, sequencing constraints,
    concurrency exclusions, human gates, and task-decomposition inputs.
11. Define accessibility, backup/recovery, and verification expectations proportional
    to the approved requirements and risk.
12. Identify risks, assumptions, and decisions requiring human approval.
13. Propose a demo/prototype path when useful.
14. Create a draft human review checklist; never approve it yourself.
15. Stop before project creation, task decomposition, or implementation.

## Output

Create or update:

- `intake/outputs/architecture_recommendation.md`
- `intake/decisions/architecture_review_checklist.md` (draft only)

Use this structure:

# Architecture Recommendation

## Source Material Reviewed

## Authoring State

Declare exactly one field:

```text
Authoring status: draft
```

Use `draft` only when the recommendation is complete and ready for human review. Draft
means architect-authored and not yet human-approved; it does not mean incomplete. Use
`blocked` when a blocking unresolved requirement prevents a final recommendation. The
architect must never use `approved` or alter its authoring status based on checklist approval.

## Data-Handling Declarations

Record allowed paths, forbidden paths, raw-source permission, redaction requirement,
and external-AI permission exactly as approved, with the approving source.

## Approved MVP Scope

## Deferred Scope

## Blocking Unresolved Requirements

## Non-Blocking Open Questions

## Recommended Project Shape

## System and Component Boundaries

Include ownership, interfaces, trust boundaries, and explicit non-goals.

## Data Flows

Describe inputs, processing, storage, outputs, external transfers, retention, and
deletion where applicable.

## Recommended Technical Stack

## Core Workflows

## Data Model Outline

## Integrations and External Systems

## Security, Privacy, and Access Control

## Accessibility Requirements

## Backup and Recovery Expectations

## Hosting and Deployment Considerations

## Testing and Verification Strategy

## Requirements Traceability

Use a table with one row per material requirement or acceptance criterion:

| ID | Approved statement | Component or decision | Verification approach | Evidence |
|---|---|---|---|---|

## Execution Plan

Include phases, dependencies, sequencing, safe concurrency, human gates, and the
bounded task inputs needed by the later task-planning stage.

## Dependency and Sequencing Notes

## Architecture Decision Records

For each material decision use a stable `ADR-###`, status, approved requirement drivers,
decision, alternatives, tradeoffs, and consequences.

## Demo or Prototype Path

## Key Tradeoffs

## Risks and Mitigations

## Human Decisions Required

## Recommendation Summary

Omit this section when status is `blocked`; state what must be resolved instead.

## Human Approval Artifact

Create `intake/decisions/architecture_review_checklist.md` with these exact fields and
leave decisions unapproved for a human to complete:

```text
Architecture review status: draft
Approved recommendation artifact: ../outputs/architecture_recommendation.md
Approved recommendation SHA-256: pending
Data-handling approval: pending
Security decision: pending
Privacy decision: pending
Accessibility decision: pending
Backup and recovery decision: pending
Hosting decision: pending
Paid-service decision: pending
Authorization to proceed to project setup: pending
Reviewer: pending
Review date: pending

## Rejected Or Deferred Alternatives

Record alternatives and rationale here.

## Unresolved Blockers

Record blockers here. A human reviewer may enter `None.` only when all blockers are resolved.

## Reviewer Notes

Add review notes here.
```

The human reviewer must replace the digest with the lowercase SHA-256 of the exact
recommendation artifact being approved. Any later recommendation edit invalidates the
approval until the human reviews it and records the new digest.

The artifact must also contain sections for rejected or deferred alternatives,
unresolved blockers, and reviewer notes. Approval is valid only when a human changes
the review status and authorization to `approved`, resolves all decision fields,
confirms data handling, identifies the reviewer, records an ISO `YYYY-MM-DD` review
date, and binds approval to the current recommendation digest. A `blocked`
recommendation cannot be approved. Only a complete `draft` may pass human review.

## Boundaries

- Do not implement code.
- Do not create a repository scaffold.
- Do not install dependencies.
- Do not create GitHub repositories.
- Do not make paid-service, hosting, billing, legal, or contract decisions.
- Do not treat assumptions as approved requirements.
- Do not write outside the two output paths named above.
- Do not approve your own recommendation or remove unresolved blockers.
- Do not include secrets or unnecessary sensitive source excerpts.
- Stop and request human review before project creation.
