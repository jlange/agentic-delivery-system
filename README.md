# Agentic Delivery System

A supervised software-delivery framework for contract websites, web applications, internal tools, automation projects, and self-owned software products.

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
7. Human approval of the task plan
8. Agent execution in isolated worktrees
9. Automated testing and independent review
10. Human merge approval
11. Staging, acceptance, delivery, and retrospective

Task decomposition produces draft, dependency-aware YAML tasks with bounded paths,
verification commands, required evidence, and explicit human gates. Draft tasks must
pass structural plan validation and receive human approval before implementation.
When a decision blocks only later work, a human may authorize a bounded partial plan;
every omitted requirement must be recorded with a reason and re-entry condition.

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

- .codex/      Project-scoped Codex configuration and agents
- agents/      Reusable agent definitions
- docs/        Operating model and process documentation
- examples/    Sanitized sample projects and artifacts
- schemas/     Task and artifact validation schemas
- scripts/     Setup and workflow automation
- skills/      Reusable agent skills
- templates/   Client-project and delivery-document templates
- tests/       Tests for scripts, schemas, and automation

## Status

This repository is in supervised pilot use. It has been used for an initial client-style intake, demo project, pull request, and independent review workflow. Production client work still requires human review, explicit approval gates, and project-specific safeguards.

Implemented reusable workflow skills currently cover contract intake, architecture
recommendation, project setup, task decomposition, and the supervised client-delivery
pipeline. Later implementation, QA-evidence, review, release, and retrospective skills
will be added from validated project workflows.
