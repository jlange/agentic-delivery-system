# Operating Model

This delivery system uses bounded autonomy by default. Humans approve product intent,
architecture, and delivery waves. Agents may then select, implement, verify, review,
and advance machine-authorized tasks until a genuine decision or safety boundary is
reached. Humans retain control over scope changes, billing, production credentials,
protected merges, deployments, and destructive actions.

## Flow

1. Capture client material.
2. Extract explicit requirements, assumptions, questions, risks, and acceptance criteria.
3. Approve scope before architecture work begins.
4. Produce a minimal architecture and execution plan.
5. Approve the plan before implementation begins.
6. Split work into bounded tasks with allowed paths, forbidden paths, verification commands, and required evidence.
7. Validate and approve the task plan before assigning implementation work.
8. Select approved dependency-ready work and run implementation in isolated branches or worktrees.
9. Run automated checks and independent review.
10. Open a pull request and merge according to the wave's durable authorization.
11. Detect merges, unlock dependents, and continue automatically.
12. Present the earliest usable slice for owner acceptance.
13. Record lessons and process improvements.

## Human gates

- Contract scope and pricing
- Client decisions
- Paid services and billing
- Secrets and credentials
- Production deploys
- Merges to protected branches unless the approved wave explicitly configures an automatic merge policy
- Destructive actions
- Budget or concurrency increases
- Task-plan authorization before implementation
