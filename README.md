# Agentic Delivery System

A supervised software-delivery framework for contract websites and web applications.

The system is designed to:

- Convert client briefs into approved requirements and acceptance criteria.
- Generate architecture and execution plans before implementation begins.
- Break approved plans into bounded, dependency-aware tasks.
- Delegate work to specialized agents using isolated Git worktrees.
- Require automated verification and independent review before merge.
- Preserve evidence, decisions, and lessons from every project.
- Improve the delivery process through Compound Engineering.

## Operating model

The initial workflow is supervised and repository-based:

1. Contract intake
2. Requirements clarification
3. Human approval of scope
4. Architecture and execution planning
5. Human approval of the plan
6. Task decomposition
7. Agent execution in isolated worktrees
8. Automated testing and independent review
9. Human merge approval
10. Staging, acceptance, delivery, and retrospective

## Safety boundaries

Agents must not:

- Invent unresolved client requirements.
- Push directly to `main`.
- Merge their own work.
- Deploy to production without human approval.
- Store secrets or client data in source control.
- Make billing, account, legal, or contractual decisions.
- Perform destructive operations without explicit approval.
- Leave comments, metadata, signatures, or other markers stating that work was AI-generated unless required by law, license, repository policy, or contract.
- Exceed configured usage, concurrency, retry, or budget limits without human approval.

## Repository contents

```text
.codex/      Project-scoped Codex configuration and agents
agents/      Reusable agent definitions
docs/        Operating model and process documentation
examples/    Sanitized sample projects and artifacts
schemas/     Task and artifact validation schemas
scripts/     Setup and workflow automation
skills/      Reusable agent skills
templates/   Client-project and delivery-document templates
tests/       Tests for scripts, schemas, and automation
Status
This repository is currently being scaffolded. No production client work should use it until the supervised pilot has completed successfully.

## Status

This repository is currently being scaffolded. No production client work should use it until the supervised pilot has completed successfully.
