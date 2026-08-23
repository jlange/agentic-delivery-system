---
name: execute-delivery-task
description: Carry one approved machine-readable delivery task through isolated implementation, verification, commit, pull-request checks and remediation, authorized merge, and post-merge verification. Use for dependency-ready product, database, frontend, backend, QA, design, security, or DevOps work and narrowly approved resumable amendments.
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

## Verification, Review, and Delivery

1. Run every required verification command and proportional regression checks.
2. Correct in-scope failures. Stop if a mandatory gate cannot pass within authorization.
3. Inspect the diff for path, contract, data, secret, migration, and generated-file
   violations.
4. Record concise command results and artifact evidence; do not claim skipped checks
   passed.
5. Commit locally, push the task branch, and create a pull request into the integration
   branch when authorized by the approved wave.
6. Wait for configured CI checks and repository reviews. Address actionable feedback,
   rerunning local verification and committing fixes after changes.
7. Merge when all repository conditions pass and existing authorization permits it.
   Refresh the local integration branch and verify the merged commit and required checks.

Read [references/evidence.md](references/evidence.md) when formatting completion
evidence.

## Completion

Report the task complete only after the pull request is merged, the local integration
branch is synchronized, and the merged commit and required checks are verified. A local
implementation, push, or open pull request is an intermediate state.
