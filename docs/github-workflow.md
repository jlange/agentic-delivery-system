# GitHub Workflow

This document defines GitHub's role in the agentic delivery system.

## Purpose

GitHub is the source of truth for client project code, reviews, branches, issues, pull requests, and delivery history.

Agents may assist with GitHub workflows, but humans retain control over repository ownership, permissions, merges, releases, and production deployment decisions.

## Repository ownership

Each client project should have a dedicated repository.

Before implementation begins, confirm:

- repository owner
- repository visibility
- client access expectations
- collaborator permissions
- billing responsibility
- branch strategy
- required protections

## Branch model

Client projects use the standard branch model defined in `docs/branching-strategy.md`:

- `main`
- `staging`
- `qa`
- `dev`
- short-lived feature or task branches

Agents should work on short-lived branches and avoid direct pushes to long-lived branches unless explicitly approved.

## Issues and tasks

Use GitHub issues when a project benefits from visible task tracking.

Each issue should include:

- requirement IDs
- task ID
- acceptance criteria
- allowed paths
- verification commands
- required evidence
- assigned role
- risk level
- human-gate status

## Pull requests

Every implementation task should normally end in a pull request.

Pull requests should include:

- requirement IDs
- task ID
- summary of changes
- verification commands run
- evidence or screenshots when relevant
- risks or follow-up work
- reviewer requested

## Reviews

Implementation agents must not approve their own work.

Use independent review for:

- authentication
- authorization
- database migrations
- payments
- deployment changes
- security-sensitive workflows
- client-critical user flows
- large refactors

Codex and Claude Code may review each other's work, but final merge approval remains human-controlled.

## CI

Use GitHub Actions when the project is ready for automated checks.

Typical checks include:

- install dependencies
- type check
- lint
- unit or component tests
- build
- Playwright tests for critical workflows

Do not rely on CI alone when manual client acceptance is required.

## Manual controls

Humans must approve:

- repository creation
- repository visibility changes
- collaborator access
- branch protection changes
- secrets and environment variables
- billing or paid services
- merges to long-lived branches
- production releases
- destructive repository actions

## Cost and access control

Use the least access required.

Do not grant broad organization permissions to agents or tools when repository-scoped access is enough.

Do not store GitHub tokens, deploy keys, or credentials in source control.
