# Autonomous Delivery Design

## Objective

Move the product owner's normal involvement toward:

```text
define product intent -> approve a delivery wave -> review usable outcomes
```

Autonomy is bounded by durable authorization. Repository artifacts determine what may
run; conversation may request or explain a decision but does not replace its record.

## Control Plane

Task YAML is the unit of execution. It records lifecycle state, requirement ownership,
dependencies and merge gates, paths, contracts, runtime resources, verification,
evidence, approval, and bounded amendments. Planning prose explains the design but
cannot override task metadata.

The planning validator must eventually validate the complete repository plan:

- every approved requirement is task-owned or deferred, never both
- documented ordering equals dependency and merge-gate ordering
- every approval binds an approver, timestamp, scope, and reviewed artifact
- concurrent tasks have disjoint paths, no competing contract writes, and compatible
  runtime resources
- expected migration, schema, index, generated, and negative-test paths are owned
- every deferral has a concrete re-entry condition

## Delivery Loop

```text
approve wave -> select executable task -> isolated implementation -> verification
-> local commit -> push -> pull request -> configured checks/reviews -> remediation
-> authorized merge -> post-merge verification -> unlock dependents -> repeat
```

Use `autonomous-delivery-orchestration` for the loop, `execute-delivery-task` for one
task. Humans remain
responsible for financial/legal decisions, authorization expansions, human-only
credentials, ungranted production authority, and experiential acceptance.

## Product-Evaluation Policy

Architecture and decomposition must identify the earliest owner-testable workflow.
For an application, this normally includes local persistence and the mutations needed
to create invented data before polished read-only views. A local sandbox is a product
capability, not deferred infrastructure. Record its constraints explicitly: invented
data only, local identity, local persistence, no invitations or external services, no
production claims, and a warning against real sensitive data.

## Skill Coverage

| Delivery capability | Skill | Status |
|---|---|---|
| Discovery and scope | `contract-intake` | Implemented |
| Architecture and owner-testable slice | `architecture-recommendation` | Implemented; revised policy |
| Repository foundation | `project-setup` | Implemented |
| Executable wave planning | `task-decomposition` | Implemented; revised metadata |
| Merge-aware scheduling and resumption | `autonomous-delivery-orchestration` | Added |
| Product implementation and verification | `execute-delivery-task` | Added |
| Cross-task acceptance and QA evidence | `qa-evidence` | Next skill to extract from a usable slice |
| Security and privacy review | `security-review` | Add when a project threat model exists |
| Release/deployment | `release-execution` | Add after an approved staging workflow |
| Client acceptance and handoff | `client-acceptance` | Add after observing contract closeout |
| Retrospective/process improvement | `retrospective` | Add after the next autonomous wave |

Do not create framework-specific frontend, backend, or database skills merely to mirror
job titles. The execution skill should invoke repository instructions and existing
technology skills. Create a specialized skill only when repeated contract work reveals
non-obvious procedure, project-specific references, or a deterministic script worth
reusing.

## Remaining Engineering Work

The current schema and execution validator establish the authorization vocabulary but
do not yet form a daemon or GitHub-integrated orchestrator. Before unattended use, add:

1. repository-level plan checks for prose/graph/YAML agreement, contract conflicts,
   runtime contention, and authorization artifact integrity;
2. a state-transition command that records an auditable event log;
3. merge, CI, and pull-request adapters with idempotent resumption;
4. isolated worktree allocation and cleanup;
5. QA-evidence workflows based on actual project artifacts;
6. a dry-run scheduler test suite covering conflicts, amendments, and failed gates.

Until those exist, the new orchestration skill is an executable operating procedure,
not a claim of fully unattended automation.

## Next Milestones

### 1. Repository-Level Plan Linter

Build a validator that evaluates the delivery plan as a whole, including requirement
coverage, dependency diagrams, task YAML, approval records, allowed paths, shared
contracts, and runtime-resource conflicts. This prevents contradictory plans from
reaching implementation and gives the orchestrator one deterministic readiness check.

### 2. Auditable Task State Transitions

Add a command that moves tasks through the delivery state machine and records each
transition as an append-only event with actor, time, reason, and supporting artifact.
This converts conversational progress updates into durable, resumable orchestration
state and prevents agents from entering protected states without evidence.

### 3. Bounded Amendment Workflow

Implement amendment request, approval, rejection, and resumption commands around the
schema already defined. This allows a blocked task to request one narrowly described
adjacent change without receiving broad repository access or requiring the delivery
wave to be manually reconstructed.

### 4. Dry-Run Scheduler

Build a scheduler that computes the next executable tasks and proposed concurrency
without creating branches or changing remote state. Test dependency blocking, path
overlap, shared-contract writes, runtime contention, amendments, and failed gates.
Dry-run output will let the product owner inspect orchestration decisions before live
automation is enabled.

### 5. Isolated Worktree Execution

Automate branch and worktree allocation for each executable task, invoke the bounded
task-execution skill, collect verification evidence, and preserve resumable state.
This is the point where the system begins doing contract implementation work with
minimal handoff prompting while keeping concurrent changes isolated.

### 6. Pull-Request Feedback and QA Evidence

Extract reusable pull-request feedback handling and `qa-evidence` from real project
artifacts. QA evidence should prove that the combined owner-testable workflow works,
not merely that individual task checks pass.

### 7. Merge-Aware GitHub Integration

Add idempotent adapters for pull-request creation, review state, merge detection, and
integration-branch refresh. After an authorized merge, the orchestrator should update
state, unlock dependents, and resume automatically without duplicating pull requests or
repeating completed work.

### 8. First Autonomous Delivery-Wave Pilot

Run one approved, low-risk wave through planning, implementation, review, merge, and
owner acceptance using invented local data. Measure human interventions, invalid stops,
retries, elapsed time, and evidence quality. Use the results to tighten the skills and
validators before enabling broader or production-adjacent work.

### 9. Release, Acceptance, and Retrospective Workflows

After the pilot establishes a real staging and handoff process, add reusable
`release-execution`, `client-acceptance`, and `retrospective` skills. These should be
derived from observed contract closeout work so they encode proven gates rather than
speculative ceremony.
