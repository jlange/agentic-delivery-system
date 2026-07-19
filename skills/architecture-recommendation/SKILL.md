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

Do not read unrelated client folders, `/mnt/c`, home directories, credentials, or unapproved source material.

## Workflow

1. Confirm the intake output and review checklist exist.
2. Summarize the approved project goal and MVP scope.
3. Separate approved scope from deferred scope and unresolved questions.
4. Identify likely users, workflows, data entities, integrations, permissions, and operational constraints.
5. Recommend the project shape:
   - static site
   - automation script
   - internal tool
   - modular monolith
   - full web application
   - other justified shape
6. Recommend the technical stack conservatively.
7. Explain key tradeoffs and rejected alternatives.
8. Identify risks, assumptions, and decisions requiring human approval.
9. Propose a demo/prototype path when useful.
10. Stop before project creation or implementation.

## Output

Create or update:

- `intake/outputs/architecture_recommendation.md`

Use this structure:

# Architecture Recommendation

## Source Material Reviewed

## Approved MVP Scope

## Deferred Scope

## Unresolved Questions

## Recommended Project Shape

## Recommended Technical Stack

## Core Workflows

## Data Model Outline

## Integrations and External Systems

## Security, Privacy, and Access Control

## Hosting and Deployment Considerations

## Testing and Verification Strategy

## Demo or Prototype Path

## Key Tradeoffs

## Risks and Mitigations

## Human Decisions Required

## Recommendation Summary

## Boundaries

- Do not implement code.
- Do not create a repository scaffold.
- Do not install dependencies.
- Do not create GitHub repositories.
- Do not make paid-service, hosting, billing, legal, or contract decisions.
- Do not treat assumptions as approved requirements.
- Do not include secrets or unnecessary sensitive source excerpts.
- Stop and request human review before project creation.
