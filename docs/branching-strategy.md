# Branching Strategy

This repository defines the default branch model for client projects created through the agentic delivery system.

## Standard branches

Client project repositories should use these long-lived branches:

- `main`: production-ready or released state.
- `staging`: pre-production validation branch.
- `qa`: integrated quality-assurance branch.
- `dev`: active integration branch for approved implementation work.

Feature and task branches should be short-lived and branch from the configured
integration branch, which defaults to `dev`.

## Default flow

feature/* -> dev -> qa -> staging -> main

## Agent rules

- Do not push task commits directly to long-lived branches. Use pull requests.
- Implementation agents should work on task branches such as `feature/FE-001-homepage-layout` or `task/API-003-auth-endpoint`.
- Merge upward after required checks and reviews. An approved delivery wave may
  authorize routine agent merge without a redundant human gate.
- Treat `main` as production-controlled even when the project has not launched yet.
- Treat `staging` as the final client or release-candidate validation branch.
- Treat `qa` as the branch for integrated test verification.
- Treat `dev` as the branch where approved completed tasks are assembled before QA.
- Do not skip branch levels unless a human explicitly approves the exception.
- Do not delete long-lived branches.
- Do not rewrite history on long-lived branches.

## Initial project setup

When creating a new client repository, initialize all four long-lived branches:

1. Start on `main`.
2. Create and push `dev`.
3. Create and push `qa`.
4. Create and push `staging`.
5. Return to `main`.

Suggested commands:

    git checkout main
    git checkout -b dev
    git push -u origin dev

    git checkout -b qa
    git push -u origin qa

    git checkout -b staging
    git push -u origin staging

    git checkout main

After branch creation, configure repository protection or rulesets when the GitHub plan supports them.

## Minimum manual protections

When available, configure protections for `main`, `staging`, `qa`, and `dev`:

- Require pull requests before merging.
- Require at least one review.
- Require status checks before merging.
- Block force pushes.
- Block branch deletion.
- Require conversation resolution.
- Apply rules to administrators when appropriate.
