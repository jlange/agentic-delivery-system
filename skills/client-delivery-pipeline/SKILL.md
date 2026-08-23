---
name: client-delivery-pipeline
description: Use when running a supervised client project pipeline for contract intake, transcript or file review, approved intake folders, synthetic demo repository setup, task branch scaffolding, Codex implementation prompts, PR review, or client-demo workflow automation. Use for repeating the FundLTC-style process with new clients while preserving human approval gates, local data safety, and bounded agent paths.
---

# Client Delivery Pipeline

Use this skill to run a supervised client-intake-to-demo workflow with less manual setup.

The workflow supports:

- Creating lowercase client intake folders.
- Copying exact approved source files from Windows or WSL paths.
- Creating bounded Codex intake prompts.
- Creating human review checklists.
- Creating synthetic demo Git repositories.
- Creating first implementation tasks.
- Creating local implementation prompts.
- Keeping review prompts out of committed task scope.

## Core Safety Rules

Preserve these gates:

- Human selects which files enter intake.
- Human decides whether raw source files are safe for agent review.
- Human approves scope before architecture or implementation.
- Human approves the architecture and execution plan before project initialization.
- Human approves real data access.
- Human approves GitHub repo creation, PR creation, merge, and deployment.
- Agents must not inspect broad local paths such as `/mnt/c`, `/mnt/d`, `/mnt/e`, `$HOME`, `.ssh`, `.config`, or `.codex`.
- Agents must not use production data, credentials, billing, or client systems unless explicitly approved.

## Script

Use the bundled script for repeatable setup:

```bash
scripts/client_pipeline.sh --help
```

When running from an installed skill path, resolve the skill directory and call:

```bash
<skill-dir>/scripts/client_pipeline.sh <command>
```

The script is conservative. It scaffolds folders, prompt files, tasks, and local ignores. It does not merge PRs, deploy, approve data, or create GitHub repos.

## Standard Workflow

### 1. Initialize Intake

Use a lowercase client name:

```bash
<skill-dir>/scripts/client_pipeline.sh init-intake fundltc
```

This creates:

```text
~/work/clients/<client>/intake/source
~/work/clients/<client>/intake/notes
~/work/clients/<client>/intake/redacted
~/work/clients/<client>/intake/outputs
~/work/clients/<client>/intake/decisions
```

### 2. Copy Exact Source Files

Copy only files that the human explicitly selected:

```bash
<skill-dir>/scripts/client_pipeline.sh copy-source <client> <file> [file...]
```

If the human confirms those exact files are approved for agent review:

```bash
<skill-dir>/scripts/client_pipeline.sh copy-source --agent-safe <client> <file> [file...]
```

Do not ask agents to search Windows Downloads, Desktop, home directories, or broad mounted drives.

### 3. Create Intake Prompt

```bash
<skill-dir>/scripts/client_pipeline.sh write-intake-prompt <client>
```

Run Codex from the intake folder only after confirming the `redacted/` files are safe:

```bash
cd ~/work/clients/<client>/intake
codex exec --skip-git-repo-check --sandbox workspace-write < notes/contract_intake_prompt.md
```

If Codex cannot write, capture its Markdown output and save it manually to:

```text
~/work/clients/<client>/intake/outputs/contract_intake_output.md
```

### 4. Create Human Review Checklist

```bash
<skill-dir>/scripts/client_pipeline.sh write-review-checklist <client>
```

Human review is required before treating anything as approved scope.

### 5. Produce Architecture Recommendation

After the intake checklist records approved scope and data-handling declarations:

```bash
<skill-dir>/scripts/client_pipeline.sh write-architecture-prompt <client>
```

Run the solution architect from the client intake directory. It may write only:

- `intake/outputs/architecture_recommendation.md`
- `intake/decisions/architecture_review_checklist.md`

The recommendation must follow the `architecture-recommendation` skill. A human must
review it and complete the checklist. The architect must not approve its own work.
`Authoring status: draft` means complete for review but not approved; `blocked` means
no final recommendation exists and project initialization must remain unavailable.

### 6. Approve Architecture And Execution Plan

Project initialization requires all of the following in
`intake/decisions/architecture_review_checklist.md`:

- recommendation `Authoring status: draft`
- `Architecture review status: approved`
- the fixed recommendation path and its matching lowercase SHA-256 digest
- `Data-handling approval: approved`
- resolved security, privacy, accessibility, backup/recovery, hosting, and paid-service decisions
- `Authorization to proceed to project setup: approved`
- a named reviewer and ISO `YYYY-MM-DD` review date
- an unambiguous no-blocker declaration under `## Unresolved Blockers`

The checklist must also preserve rejected or deferred alternatives. Missing, pending,
stale, or blocked evidence fails closed. The digest binds approval to the exact content
reviewed; changing the recommendation requires renewed human approval.

Human-authored approval fields are parsed case-insensitively with surrounding whitespace
ignored. The no-blocker section accepts `None`, `None.`, `No blockers`, or
`No unresolved blockers`, with optional blank lines and an optional Markdown bullet.
This normalization does not guess misspellings, reinterpret ambiguous prose, relax the
approved artifact path, or bypass digest and traceability checks.

After completing review, the human can calculate the recorded digest with:

```bash
sha256sum intake/outputs/architecture_recommendation.md
```

Validate the gate without creating a project:

```bash
<skill-dir>/scripts/client_pipeline.sh validate-architecture-gate <client>
```

### 7. Initialize Demo Repo

After the architecture and execution plan are explicitly approved:

```bash
<skill-dir>/scripts/client_pipeline.sh init-demo-repo <client> <repo-name>
```

This creates a local Git repo scaffold under:

```text
~/work/clients/<client>/<repo-name>
```

After task-plan or wave authorization, push task branches and continue through the
configured review and merge policy. Pause only for a risk-based escalation condition;
do not add a redundant prompt for routine remote engineering actions.

### 8. Create Demo Task

```bash
<skill-dir>/scripts/client_pipeline.sh write-demo-task <client> <repo-name>
```

The first task is `DEMO-001-generate-synthetic-workbooks.md`.

### 9. Create Local Agent Prompts

```bash
<skill-dir>/scripts/client_pipeline.sh write-demo-agent-prompts <client> <repo-name>
```

Prompts are written to `prompts-local/` and added to `.git/info/exclude` so they stay local by default. This avoids repeating the out-of-scope `prompts/` issue encountered during the FundLTC demo PR.

### 10. Implementation And Review Pattern

Use task branches:

```bash
git checkout -b task/DEMO-001-generate-synthetic-workbooks
```

Run Codex with the local implementation prompt. Open a PR after committing and pushing.

Use the repository's configured pull-request checks and review policy.

Allowed review commands should be read-only or non-destructive verification commands. Do not approve commands that install global packages, access `/mnt/c`, merge, push, delete broadly, or deploy.

## Merge Rules

Before merging:

- Resolve blocking review findings.
- Confirm working tree is clean.
- Confirm no out-of-scope files are included.
- Confirm no real client data is committed.
- Human approves merge.

## When To Stop

Stop and ask the human when:

- Source files may contain sensitive data.
- Scope is unclear.
- A tool needs real client data.
- A dependency install changes the environment.
- A command wants broad filesystem access.
- A command wants to push, merge, deploy, delete, or modify billing/account settings.
- Tests fail repeatedly.
