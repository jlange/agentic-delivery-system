# Local Data Safety

This document defines how local Windows and WSL files should be handled when using agents.

## Core rule

Agents should only inspect files that were intentionally placed in the approved project or intake directory.

Do not ask agents to search the whole machine, Windows home directory, Downloads folder, Desktop, or mounted drives.

## WSL and Windows filesystem access

WSL can usually access Windows drives through mount paths such as:

- `/mnt/c`
- `/mnt/d`
- `/mnt/e`

That access is convenient for moving selected files, but it should not be treated as an approved search area for agents.

## Safe intake pattern

Use this pattern for client source material:

1. Export files from the source system.
2. Manually choose the files needed for intake.
3. Copy selected files into the client intake folder.
4. Redact sensitive content when needed.
5. Ask agents to review only the approved intake path.

Recommended structure:

- `source/`: original selected files
- `notes/`: human notes
- `redacted/`: copies safe for agent review
- `outputs/`: generated artifacts
- `decisions/`: approved human or client decisions

## Allowed paths

Agent prompts should define allowed paths explicitly.

Example:

- Allowed paths: `~/work/clients/client-name/intake/redacted`
- Allowed paths: `~/work/clients/client-name/intake/source` when raw source review is approved

## Forbidden paths

Unless explicitly approved for a specific task, agents must not inspect:

- `/mnt/c`
- `/mnt/d`
- `/mnt/e`
- `~/`
- `~/.ssh`
- `~/.config`
- `~/.codex`
- Windows Downloads
- Windows Desktop
- browser profile directories
- password-manager exports
- unrelated client folders

## Prompt rule

Every intake or project task should include:

- allowed paths
- forbidden paths
- whether raw source files may be reviewed
- whether redaction is required
- whether client data may be sent to external AI systems

## Secrets and sensitive data

Do not provide agents with:

- passwords
- API keys
- access tokens
- private keys
- production credentials
- payment data
- regulated data
- unnecessary personal data
- unrelated client data

If a transcript or source file contains sensitive content, create a redacted copy before agent review.

## Running agents

Do not start agents from:

- `/mnt/c`
- `/mnt/c/Users`
- `/mnt/c/Users/RestingRobot`
- `~/`

Start agents from the specific repository, project directory, or approved intake directory.

## Human responsibility

Humans are responsible for selecting what files enter the intake area.

Agents may analyze approved files, but they should not discover or collect files from broader local storage.
