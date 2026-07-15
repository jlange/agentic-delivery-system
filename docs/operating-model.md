# Operating Model

This delivery system is supervised by default. Agents may investigate, plan, implement, and review within approved task boundaries, but humans retain control over scope, billing, production credentials, merges, and deployments.

## Flow

1. Capture client material.
2. Extract explicit requirements, assumptions, questions, risks, and acceptance criteria.
3. Approve scope before architecture work begins.
4. Produce a minimal architecture and execution plan.
5. Approve the plan before implementation begins.
6. Split work into bounded tasks with allowed paths, forbidden paths, verification commands, and required evidence.
7. Run implementation in isolated branches or worktrees.
8. Run automated checks and independent review.
9. Merge only after human approval.
10. Record lessons and process improvements.

## Human gates

- Contract scope and pricing
- Client decisions
- Paid services and billing
- Secrets and credentials
- Production deploys
- Merges to main
- Destructive actions
- Budget or concurrency increases
