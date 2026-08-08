---
name: project-setup
description: Create a bounded local project repository from a complete architecture recommendation and matching human approval. Use after the architecture gate passes and before task decomposition or implementation, when Codex needs to create the approved scaffold, initialize the required local Git branches, and record setup evidence without creating a GitHub repository, installing unapproved dependencies, or implementing product features.
---

# Project Setup

Create only the local foundation authorized by the approved architecture and execution
plan. Stop before task decomposition or implementation.

## Required Inputs

Read:

- `AGENTS.md` and applicable repository policy documents
- `intake/outputs/contract_intake_output.md`
- `intake/decisions/intake_review_checklist.md`
- `intake/outputs/architecture_recommendation.md`
- `intake/decisions/architecture_review_checklist.md`
- `docs/target-technical-stack.md`
- `docs/branching-strategy.md`

Obtain explicit human confirmation of:

- the exact target directory
- allowed and forbidden paths
- whether architecture artifacts or client information may enter source control
- the approved project name, shape, stack, and repository layout
- permission for local Git initialization and the initial scaffold commit

Do not infer a decision from directory existence or an architecture suggestion.

## Workflow

1. Confirm the working tree containing the delivery system and any target directory are
   understood. Preserve unrelated changes and refuse a non-empty target unless the human
   explicitly approves updating that exact project.
2. Run the existing gate without creating a project:

   ```bash
   <client-delivery-pipeline-skill>/scripts/client_pipeline.sh validate-architecture-gate <client>
   ```

   Stop on any failure. Do not reproduce, weaken, or bypass the gate manually.
3. Compare the requested setup with the approved recommendation. Use the approved
   architecture as controlling input and `docs/target-technical-stack.md` as the default.
   A deviation requires a cited approved `REQ-###` and documented tradeoff.
4. Present a bounded setup plan before writing. List the exact target, files and
   directories, Git operations, dependency actions, expected evidence, and stop point.
   Stop for human direction if any choice would materially alter architecture, hosting,
   paid services, security, privacy, accessibility, backup, or data handling.
5. Create the smallest scaffold required by the approved project shape. Include only
   agreed configuration, documentation, source/test directories, and ignore rules. Do
   not add placeholder product behavior or speculative services.
6. Create a repository-root `AGENTS.md` containing the approved project guidance:
   - task and branch rules
   - verification commands that are available in the initial scaffold
   - generated or protected paths known at setup time
   - data, secret, production, merge, and deployment boundaries
   - how human approvals and independent review are recorded

   Keep it project-specific and concise. Do not copy the delivery system's `AGENTS.md`
   verbatim or claim commands are runnable before their dependencies exist.
   Start from `templates/repository/AGENTS.md`, configure its integration branch and
   verification commands, and preserve risk-based escalation and exact-HEAD review.
   Also create `.gitattributes` from `templates/repository/.gitattributes`, keep shell
   scripts LF-only and executable, and include `bash -n` validation where available.
7. Record environment prerequisites by category: repository dependencies, generated
   tool artifacts, operating-system libraries, services or credentials, and interactive
   privileges. Approval in one category does not authorize another. Do not install or
   provision them during setup.
8. Do not copy intake or architecture artifacts into the new repository unless the
   human explicitly approves those exact artifacts for source control. Never copy raw
   sources, secrets, credentials, `.env` contents, or unnecessary client data.
9. Do not create accounts or paid services. Install ordinary project dependencies when
   needed for the approved scaffold, using normal environment permission prompts. Add
   declarations only when the architecture approves them and record the reason. Pause
   for financial, licensing, credential, compliance, or production consequences.
10. When local Git initialization and the initial scaffold commit are approved:
   - initialize `main`
   - commit only the reviewed scaffold paths
   - create `dev`, `qa`, and `staging` from that initial commit
   - return to `main`

   Verify all four branches exist. Do not configure remotes, push, create GitHub
   repositories, or change repository protections.
11. Run scaffold-appropriate checks that do not require unapproved installation. Record
   commands, results, skipped checks, and blockers.
12. Write `intake/outputs/project_setup_report.md` unless the human approves another
    exact evidence path. Include:
    - approved recommendation path and SHA-256
    - target directory
    - files and directories created
    - stack and approved deviations
    - dependency decisions
    - repository guidance created in `AGENTS.md`
    - categorized environment prerequisites
    - Git branch and commit evidence
    - data included or deliberately excluded
    - verification results
    - remaining human decisions and blockers
13. Stop before task decomposition, implementation, remote creation, push, or deployment.

## Completion Conditions

Report setup complete only when:

- the architecture gate passed immediately before setup
- the scaffold matches the approved architecture
- a repository-root `AGENTS.md` records the approved project rules and available checks
- no forbidden data or path was accessed
- dependency decisions are documented
- `main`, `dev`, `qa`, and `staging` exist locally at the reviewed initial commit
- verification evidence and the setup report exist
- the working tree contains no unexplained changes

Otherwise report the setup as blocked or incomplete and identify the exact next human
decision. Never mark architecture or project setup approved on a human's behalf.

## Boundaries

- Do not create or configure a GitHub repository or remote.
- Do not push, merge, deploy, modify billing, or create paid services.
- Do not implement product features or decompose implementation tasks.
- Do not invent requirements, stack choices, environments, or production settings.
- Do not overwrite a non-empty target or modify unrelated repositories.
- Do not access broad home, mounted-drive, or unrelated client paths.
- Do not commit secrets, client source material, or unapproved artifacts.
- Do not approve your own setup or architecture work.
