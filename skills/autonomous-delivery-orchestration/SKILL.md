---
name: autonomous-delivery-orchestration
description: Advance an approved delivery wave through dependency-ready task selection, isolated execution, verification, independent review, pull requests, merge detection, and automatic resumption. Use when a repository contains machine-readable approved task YAML and the operator wants bounded implementation to continue with minimal prompting while stopping for product decisions, authorization conflicts, unsafe operations, or failed mandatory gates.
---

# Autonomous Delivery Orchestration

Treat repository task and authorization artifacts as the control plane. Coordinate work;
do not reinterpret scope or perform implementation directly when an execution agent can
own a bounded task.

## Entry Gate

1. Read repository policy, the approved wave, task YAML, and integration-branch state.
2. Validate every task against the canonical schema and planning validator.
3. Require a durable approval record whose scope includes the task and whose artifact
   digest or revision still matches.
4. Derive task readiness. A task is executable only when it is approved, every
   `execution_gate.requires_merged` task is merged, no amendment is pending, and its
   required environment is available.
5. Stop if prose, diagrams, task metadata, approval records, or Git state disagree.

## Scheduling Loop

1. Refresh the integration branch and pull-request state.
2. Reconcile merged tasks and update their durable state through the repository's
   approved state-update mechanism.
3. Compute executable tasks from metadata; never choose from conversational memory.
4. Compute safe concurrency using all of:
   - non-overlapping allowed paths
   - no shared contract written by more than one active task
   - no mutually exclusive runtime resource or test-state claim
   - common ancestry at the approved planning revision
5. Select the earliest owner-testable vertical slice before supporting or read-only
   work when dependencies permit.
6. Create an isolated branch or worktree and invoke `execute-delivery-task` with only
   the task path and repository starting point.
7. After verification, request independent review by a different agent or reviewer.
8. Require a committed implementation and use `independent-local-review`. The review
   must be clean or fully dispositioned for the exact HEAD before push. Rerun it after
   every commit; stop on reviewer unavailability or invalid output.
9. Open a pull request when approved wave authorization permits remote writes. Attach
   requirement IDs, verification evidence, amendment history, and review outcome.
10. Wait for required CI and configured reviews. Remediate actionable feedback and
    repeat verification and local review after changes.
11. Merge when required conditions pass and authorization already covers the merge.
    Refresh the integration branch and verify the merged commit and checks. Then restart
    this loop. Do not stop at pull-request creation.

Read [references/state-machine.md](references/state-machine.md) when implementing or
auditing orchestration state transitions.

## Bounded Amendments

When correct implementation needs a path or permission outside current authorization:

1. Stop only the affected task.
2. Record `amendment_requested` with the exact path, reason, permitted change, and
   additional verification.
3. Continue unrelated safe tasks.
4. Resume only after a human approval record is added and validated.
5. Grant only the approved change; an amendment never authorizes unrelated edits.

## Stop Conditions

Stop the affected work for a financial, legal, contractual, licensing, regulatory or
compliance decision; a missing human-only credential or permission; ungranted
production authority; an irreversible unresolved business decision; metadata conflict;
unapproved scope expansion; sensitive-data risk; reviewer failure; destructive action
without safeguards; incompatible review directions; or an unsatisfied mandatory check.
Routine Git, dependency, test, commit, push, pull-request, and authorized merge actions
are not human decisions. Use normal environment permission prompts when required.

## Completion

A wave is complete only when every included task is merged or explicitly cancelled by
an authorized record, all acceptance evidence is present, and the owner-testable slice
has an executable acceptance path. Report deferred work and its re-entry conditions.
