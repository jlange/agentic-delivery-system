---
name: execute-delivery-task
description: Implement, test, and prepare one approved machine-readable delivery task within its authorized paths and decisions. Use when an approved dependency-ready task must be completed in an isolated branch or worktree, including focused product code, database, frontend, backend, QA, design, security, or DevOps work and narrowly approved resumable path amendments.
---

# Execute Delivery Task

Execute one task end to end. The task file and linked approved artifacts are
authoritative; keep the handoff prompt small.

## Entry Gate

1. Read repository policy, the task YAML, linked requirements, architecture decisions,
   and approval artifact.
2. Run the execution validator. Confirm dependencies are merged and the working branch
   starts at the required integration revision.
3. Inspect the relevant code and tests before editing. Preserve unrelated changes.
4. Confirm required runtime services and test resources are available without assuming
   that package approval authorizes OS packages, credentials, or external services.

## Implementation

1. Set the task state to `implementing` using the approved state mechanism.
2. Plan the smallest coherent change satisfying every acceptance criterion.
3. Implement product code, migrations, tests, fixtures, documentation, or configuration
   actually required by the task. Implementation includes the full vertical behavior,
   not only scaffolding or planning artifacts.
4. Prefer an owner-usable mutation path when the task belongs to the earliest
   product-evaluation slice. Synthetic read-only fixtures do not substitute for a
   workflow that creates and persists invented local data.
5. Remain inside allowed paths and approved contracts. Do not opportunistically fix
   unrelated issues.

## Boundary Conflict

If a necessary adjacent change is unauthorized, do not make it. Create a bounded
amendment record containing:

```yaml
task: DB-003
requested_path: src/db/schema/patient-review.ts
reason: Add the key required for same-plan referential integrity.
permitted_change: Composite unique key only.
additional_verification:
  - Negative cross-plan persistence tests.
```

Set the task to `amendment_requested`, report the exact blocker, and stop this task.
Resume from the existing worktree after a matching human approval is durable.

## Verification and Handoff

1. Run every required verification command and proportional regression checks.
2. Correct in-scope failures. Stop if a mandatory gate cannot pass within authorization.
3. Inspect the diff for path, contract, data, secret, migration, and generated-file
   violations.
4. Record concise command results and artifact evidence; do not claim skipped checks
   passed.
5. Commit and push only if task authorization permits them.
6. Hand the exact diff and evidence to an independent reviewer. The implementation
   agent must not approve its own work or merge it.

Read [references/evidence.md](references/evidence.md) when formatting completion
evidence.

## Completion

Report implementation complete only when all acceptance criteria have evidence, all
required checks pass, the diff remains authorized, and an independent review can start.
Otherwise report the precise resumable state and next authorized action.
