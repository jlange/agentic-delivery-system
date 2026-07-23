---
name: task-decomposition
description: Convert an approved architecture execution plan and completed project scaffold into bounded, dependency-aware draft implementation tasks. Use after project setup and before implementation when Codex must map requirements and acceptance criteria to task YAML files, assign specialist roles and path ownership, define sequencing and verification evidence, validate plan coverage, and prepare a human task-plan approval gate.
---

# Task Decomposition

Create an executable plan, not product code. Produce draft tasks for human review and
stop before branches, worktrees, implementation, remote operations, or deployment.

## Required Inputs

Read:

- the project `AGENTS.md` and applicable policies
- the approved intake output and intake review checklist
- the approved architecture recommendation and architecture review checklist
- `intake/outputs/project_setup_report.md`
- the target repository tree and dependency declarations
- the delivery system's `schemas/task.schema.json`, task template, role definitions,
  branching strategy, and target technical stack

Confirm the exact target repository and permitted planning-output paths. Require human
confirmation that project setup is complete and task planning may begin. Do not infer
approval from an existing scaffold.

## Entry Gate

1. Run the existing architecture gate. Stop on failure.
2. Verify the architecture digest in the setup report matches the currently approved
   recommendation.
3. Verify the setup report identifies the target repository, setup verification, and
   `main`, `dev`, `qa`, and `staging` at the reviewed scaffold commit.
4. Inspect the target repository read-only. Stop on unexplained changes, a mismatched
   layout, missing setup evidence, or a material architecture decision still pending.

Never repair or bypass an entry-gate failure while decomposing tasks.

## Workflow

1. Extract every approved `REQ-###` and `AC-###`, architecture phase, component,
   dependency, risk, human gate, and verification obligation.
2. Build a requirement-to-task matrix before writing task files. Map every material
   requirement to implementation ownership and every acceptance criterion to at least
   one verification task or command.
3. Split work into the smallest independently implementable and reviewable vertical
   slices. Create foundation-only tasks when later work genuinely depends on shared
   routing, schema, design primitives, or tooling.
4. Assign one primary role and a stable role prefix:
   - `FE` frontend engineer
   - `API` backend engineer
   - `DB` database engineer
   - `OPS` DevOps engineer
   - `QA` QA engineer
   - `SEC` security reviewer
   - `DES` design reviewer
5. Give each task explicit repository-relative allowed paths. Use the narrowest paths
   that permit completion. Always forbid secrets, environment files, unrelated client
   material, broad home or mounted-drive paths, and unapproved architecture artifacts.
6. Encode dependencies by task ID. Sequence migrations before consumers and shared
   foundations before feature tasks. Tasks that can run concurrently must not own the
   same files or overlapping path trees.
7. Write observable acceptance criteria tied to approved requirements. Do not restate
   implementation steps as acceptance criteria.
8. Specify commands that can actually run in the scaffolded project and evidence that
   proves the result. Include focused checks plus broader regression checks when risk
   warrants them. Do not propose dependency installation unless separately approved.
9. Mark every generated task `status: draft`. Set `human_gate: true` when execution,
   data access, migrations, paid services, credentials, external systems, destructive
   actions, or architecture-sensitive choices require human approval.
10. Write the plan outputs, run the bundled validator, resolve structural errors, and
    present the plan for human review. Never change task status to `approved` yourself.

## Outputs

Write only to the exact approved planning paths, normally:

- `tasks/<TASK-ID>-<slug>.yaml`
- `docs/task-plan.md`
- `docs/task-plan-review-checklist.md`

Use the canonical task schema without additional YAML fields. Put cross-task details in
`docs/task-plan.md`, including:

- source artifacts and approved architecture digest
- requirement and acceptance-criterion coverage matrix
- dependency graph and ordered execution waves
- safe concurrency groups and shared-file exclusions
- risk and human-gate summary
- verification strategy
- deferred scope, blockers, and assumptions

The review checklist must leave these decisions pending for a human:

```text
Task plan review status: draft
Architecture digest verified: pending
Requirement coverage approved: pending
Acceptance-criterion coverage approved: pending
Dependencies and concurrency approved: pending
Path boundaries approved: pending
Verification and evidence approved: pending
Authorization to begin implementation: pending
Reviewer: pending
Review date: pending
```

Include sections for rejected or deferred tasks, unresolved blockers, and reviewer
notes. Only a human may approve the plan and individual task files.

## Plan Validation

Run:

```bash
python skills/task-decomposition/scripts/validate-task-plan.py \
  --schema schemas/task.schema.json \
  --requirements <approved-intake-output> \
  --tasks <target-project>/tasks
```

The validator checks YAML structure, draft status, unique IDs, known acyclic
dependencies, safe allowed paths, and aggregate `REQ-###`/`AC-###` coverage. It does
not grant human approval. After approval, run the delivery system's execution validator
against each task before assigning it to an implementation agent.

## Completion Conditions

Report decomposition complete for review only when all approved IDs are covered, every
task passes plan validation, dependencies form an acyclic graph, concurrency is safe,
paths are bounded, verification is runnable, and no unresolved blocker remains.

## Boundaries

- Do not implement product code or modify the scaffold.
- Do not create branches, worktrees, commits, remotes, pull requests, or deployments.
- Do not expand scope, invent requirements, or revise architecture decisions.
- Do not approve tasks or the task plan.
- Do not assign overlapping write ownership to concurrent tasks.
- Do not expose secrets, raw client material, credentials, or `.env` contents.
- Stop when a task cannot be bounded, verified, or assigned without a human decision.
