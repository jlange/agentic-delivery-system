---
name: task-decomposition
description: Convert an approved architecture execution plan and completed project scaffold into bounded, dependency-aware machine-executable implementation tasks, including safely limited partial plans when later work is blocked by unresolved decisions. Use after project setup and before implementation to map requirements and acceptance criteria, prioritize the earliest owner-testable slice, encode durable authorization and merge gates, compute safe concurrency from paths, contracts, and runtime resources, and prepare a human task-plan approval gate.
---

# Task Decomposition

Create an executable plan, not product code. Produce tasks awaiting human approval and
stop before branches, worktrees, implementation, remote operations, or deployment.

## Required Inputs

Read:

- the project `AGENTS.md` and applicable policies
- the approved intake output and intake review checklist
- the approved architecture recommendation and architecture review checklist
- `intake/outputs/project_setup_report.md`
- approved post-setup change records under `intake/decisions/`, when present
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
4. Inspect the target repository read-only and compare it with the setup report.
   Accept a later change only when a record declares `Post-setup change status:
   approved` and identifies the exact change, approver, ISO approval date, scope impact,
   architecture impact, and data-handling impact. Do not rewrite historical setup
   evidence. Stop on unexplained or unapproved drift.
5. Classify unresolved decisions:
   - **global blocker**: affects project shape, trust or data boundaries, the shared
     foundation, or the ability to bound and verify every proposed task
   - **task-scoped blocker**: affects only identifiable requirements or later task waves
   - **production-only gate**: affects deployment, production data, paid services, or a
     production-readiness claim but not authorized local synthetic work
   - **non-blocking decision**: can be resolved inside an already approved task boundary
     without changing architecture or product behavior
6. Stop on a global blocker. For task-scoped blockers, create a partial plan only when
   the human explicitly authorizes its exact scope. Record production-only gates but do
   not let them block unrelated local synthetic tasks.

Never repair or bypass an entry-gate failure while decomposing tasks.

## Workflow

1. Extract every approved `REQ-###` and `AC-###`, architecture phase, component,
   dependency, risk, human gate, and verification obligation.
2. Build a requirement-to-task matrix before writing task files. For a full plan, map
   every material requirement to implementation ownership and every acceptance
   criterion to verification. For a partial plan, map each approved ID to exactly one
   of task coverage or an explicit deferral.
3. Build a command-provenance matrix. For every verification command, identify whether
   it exists in the approved scaffold or which task creates it. Sequence each consumer
   after the owning task. Treat missing scripts, test harnesses, generators, services,
   and runtimes as blockers or explicit prerequisites rather than assuming they exist.
4. Inventory tracked files that setup, generation, build, migration, and test commands
   are expected to create or modify. Include those exact files in allowed paths before
   approval. Do not use a broad directory merely because a framework may generate one
   focused file.
5. Classify non-repository prerequisites separately:
   - package or lockfile installation
   - downloaded tool artifacts such as browser binaries
   - operating-system libraries
   - external services or credentials
   - interactive privileges such as `sudo`

   Record the owning task, approval source, verification method, and stopping behavior
   for each prerequisite. Never infer one category's authorization from another.
6. Identify the smallest workflow the product owner can personally use with invented
   local data. Order the first wave around that mutable, persistent vertical slice;
   do not optimize for read-only traceability before usability. Split work into the
   smallest independently implementable and reviewable vertical slices. Create foundation-only tasks when later work genuinely depends on shared
   routing, schema, design primitives, or tooling.
7. Assign one primary role and a stable role prefix:
   - `FE` frontend engineer
   - `API` backend engineer
   - `DB` database engineer
   - `OPS` DevOps engineer
   - `QA` QA engineer
   - `SEC` security reviewer
   - `DES` design reviewer
8. Give each task explicit repository-relative allowed paths. Use the narrowest paths
   that permit completion. Always forbid secrets, environment files, unrelated client
   material, broad home or mounted-drive paths, and unapproved architecture artifacts.
9. Encode dependencies both by task ID and in `execution_gate.requires_merged`; they
   must agree. Record each task's named contracts read or written and exclusive runtime
   resources. Sequence migrations before consumers and shared
   foundations before feature tasks. Tasks that can run concurrently must not own the
   same files or overlapping path trees. Also confirm their environment prerequisites
   can run concurrently without shared ports, services, caches, or interactive prompts.
10. Write observable acceptance criteria tied to approved requirements. Do not restate
   implementation steps as acceptance criteria.
11. Specify commands that can actually run in the scaffolded project and evidence that
   proves the result. Include focused checks plus broader regression checks when risk
   warrants them. Do not propose dependency installation unless separately approved.
12. Mark every generated task `status: awaiting_approval` and add a pending approval
   object that a human must update with approved status, approver, timestamp, scope,
   and artifact.
   Set `human_gate: true` when execution,
   data access, migrations, paid services, credentials, external systems, destructive
   actions, or architecture-sensitive choices require human approval.
13. For a parallel wave, require shared checklist and task-approval changes to land
    through the repository's normal branch and review policy before creating concurrent
    implementation branches. Each implementation task must start from that common
    approved commit and must not edit shared governance files.
14. Write the plan outputs, run the bundled validator, resolve structural errors, and
    present the plan for human review. Never change task status to `approved` yourself.

## Partial Plans

Use a partial plan only when all of these are true:

- the architecture and setup gates pass
- no global blocker remains
- a human authorizes the exact limited scope
- every omitted `REQ-###` and `AC-###` is attributable to a task-scoped or
  production-only gate
- omitted work cannot be reached through dependencies from an included task

Do not create speculative task YAML for deferred work. Create
`docs/task-plan-deferrals.yaml` with:

```yaml
scope: partial
authorization:
  artifact: intake/decisions/task_decomposition_scope_approval.md
  approved_by: Project Owner
  approval_date: 2026-07-22
deferred:
  REQ-002:
    gate_type: task-scoped
    reason: Exact unresolved decision or production-only gate.
    reentry_condition: Exact evidence required before decomposition.
```

Use one entry per deferred ID. Do not defer an ID that any generated task claims to
cover. In `docs/task-plan.md`, identify the bounded objective, explicitly excluded
components, deferred task waves, and why included tasks remain independently safe.

## Outputs

Write only to the exact approved planning paths, normally:

- `tasks/<TASK-ID>-<slug>.yaml`
- `docs/task-plan.md`
- `docs/task-plan-review-checklist.md`
- `docs/task-plan-deferrals.yaml` for a partial plan only

Use the canonical task schema without additional YAML fields. Encode approval,
merge gates, contract access, runtime resources, and amendments in task YAML. Put cross-task details in
`docs/task-plan.md`, including:

- source artifacts and approved architecture digest
- requirement and acceptance-criterion coverage matrix
- dependency graph and ordered execution waves
- command-provenance matrix
- generated-file inventory
- categorized environment-prerequisite matrix
- safe concurrency groups and shared-file exclusions
- risk and human-gate summary
- verification strategy
- deferred scope, blockers, and assumptions
- full or partial plan status and the human authorization source

The review checklist must leave these decisions pending for a human:

```text
Task plan review status: draft
Plan scope approval: pending
Architecture digest verified: pending
Post-setup changes verified: pending
Requirement coverage approved: pending
Deferrals and re-entry conditions approved: pending
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
  --tasks <target-project>/tasks \
  [--deferrals <target-project>/docs/task-plan-deferrals.yaml]
```

The validator checks YAML structure, awaiting-approval status, unique IDs, known acyclic
dependencies, matching merge gates, safe allowed paths, and aggregate `REQ-###`/`AC-###` task-or-deferral
coverage. A deferral file must identify partial scope, human authorization, reasons, and
re-entry conditions. It does not grant human approval. After approval, run the delivery
system's execution validator against each task before assigning it to an implementation
agent.

## Completion Conditions

Report a full decomposition complete for review only when every approved ID has task
coverage. Report a partial decomposition complete for review only when every approved
ID has exactly one of task coverage or a valid deferral, the limited scope has human
authorization, and no global blocker remains. In both cases, require valid tasks,
acyclic dependencies, safe concurrency, bounded paths, command provenance, generated
path ownership, categorized prerequisites, and runnable verification. Describe partial
coverage as foundation contribution or partial-plan accounting, never complete product
requirement satisfaction.

## Boundaries

- Do not implement product code or modify the scaffold.
- Do not create branches, worktrees, commits, remotes, pull requests, or deployments.
- Do not expand scope, invent requirements, or revise architecture decisions.
- Do not approve tasks or the task plan.
- Do not silently convert a full plan into a partial plan.
- Do not treat a task-scoped or production-only deferral as authorization to implement it.
- Do not assign overlapping write ownership to concurrent tasks.
- Do not expose secrets, raw client material, credentials, or `.env` contents.
- Stop when a task cannot be bounded, verified, or assigned without a human decision.
