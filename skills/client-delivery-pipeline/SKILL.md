---
name: client-delivery-pipeline
description: Use when running a supervised client project pipeline for contract intake, transcript or file review, approved intake folders, synthetic demo repository setup, task branch scaffolding, Codex implementation prompts, Claude review prompts, PR review, or client-demo workflow automation. Use for repeating the FundLTC-style process with new clients while preserving human approval gates, local data safety, and bounded agent paths.
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
- Creating local Codex and Claude prompts.
- Keeping review prompts out of committed task scope.

## Core Safety Rules

Preserve these gates:

- Human selects which files enter intake.
- Human decides whether raw source files are safe for agent review.
- Human approves scope before architecture or implementation.
- Human approves real data access.
- Human approves GitHub repo creation, PR creation, merge, and deployment.
- Agents must not inspect broad local paths such as `/mnt/c`, `/mnt/d`, `/mnt/e`, `$HOME`, `.ssh`, `.config`, `.codex`, or `.claude`.
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

### 5. Initialize Demo Repo

After scope is approved enough to start a demo:

```bash
<skill-dir>/scripts/client_pipeline.sh init-demo-repo <client> <repo-name>
```

This creates a local Git repo scaffold under:

```text
~/work/clients/<client>/<repo-name>
```

Push to GitHub only with explicit human approval.

### 6. Create Demo Task

```bash
<skill-dir>/scripts/client_pipeline.sh write-demo-task <client> <repo-name>
```

The first task is `DEMO-001-generate-synthetic-workbooks.md`.

### 7. Create Local Agent Prompts

```bash
<skill-dir>/scripts/client_pipeline.sh write-demo-agent-prompts <client> <repo-name>
```

Prompts are written to `prompts-local/` and added to `.git/info/exclude` so they stay local by default. This avoids repeating the out-of-scope `prompts/` issue encountered during the FundLTC demo PR.

### 8. Implementation And Review Pattern

Use task branches:

```bash
git checkout -b task/DEMO-001-generate-synthetic-workbooks
```

Run Codex with the local implementation prompt. Open a PR after committing and pushing.

Use Claude or Codex for independent review. Review only unless the human explicitly asks for fixes.

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
