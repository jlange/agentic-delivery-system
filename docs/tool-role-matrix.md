# Tool Role Matrix

This document defines the default role of each tool in the agentic delivery system.

## Summary

| Tool | Default role | Should do | Should not do |
|---|---|---|---|
| Codex | Primary implementation and repo agent | Implement bounded tasks, edit files, run tests, review code, maintain docs | Merge, deploy, change billing, use production secrets, exceed task scope |
| GitHub | Source of truth | Store code, issues, branches, pull requests, reviews, CI history | Replace human approval for scope, billing, production, or legal decisions |
| Skills | Reusable workflow procedures | Encode repeatable methods, checklists, templates, scripts, and references | Store secrets, client data, one-off decisions, or product code |
| Scripts | Repeatable automation | Create branches, validate scaffolds, run checks, generate templates | Perform destructive or production actions without approval |
| Humans | Accountable decision-makers | Approve scope, contracts, billing, permissions, merges, deployments, client decisions | Delegate legal, financial, or production accountability to agents |

## Codex

Use Codex as the default working agent for:

- implementing approved tasks
- editing repository files
- running local verification
- creating tests
- maintaining process documentation
- reviewing changes when it did not implement them

Codex should follow `AGENTS.md`, project config, task files, and applicable skills.

## GitHub

Use GitHub to coordinate durable project state.

GitHub should hold:

- source code
- task issues when useful
- branches
- pull requests
- review history
- CI results
- release history

Private notes, secrets, production credentials, and unnecessary client data do not belong in GitHub.

## Skills

Use skills for repeatable operating procedures.

A skill should make an agent better at a workflow without hard-coding a one-off project decision.

Skills should be added gradually as repeated patterns become clear.

## Scripts

Use scripts for repeatable mechanical actions.

Good script candidates:

- scaffold validation
- branch initialization
- task file validation
- local project checks
- evidence packaging
- template generation

Scripts must be conservative by default and should refuse risky actions unless explicitly approved.

## Humans

Humans remain responsible for:

- contract scope
- pricing
- client commitments
- account ownership
- paid services
- credentials
- privacy decisions
- legal and compliance questions
- merges to long-lived branches
- production deployments
