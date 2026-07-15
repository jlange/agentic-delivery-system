# Target Technical Stack

This document defines the default technical stack for client projects created through the agentic delivery system.

## Default approach

Use a modular monolith by default.

A modular monolith means:

- One repository.
- One primary application.
- One primary database.
- Clear internal modules.
- Simple deployment.
- Strong boundaries inside the codebase.
- No microservices unless the contract clearly requires them.

This is the default because most contract websites, dashboards, portals, scheduling systems, admin tools, and small SaaS products do not benefit from distributed systems complexity.

## Default application stack

Use this stack unless a client requirement justifies a different choice:

- TypeScript
- Next.js
- React
- Tailwind CSS
- shadcn/ui when appropriate
- PostgreSQL
- Supabase when managed auth, database, storage, and simple backend services are useful
- Playwright for end-to-end tests
- GitHub for source control and pull requests
- GitHub Actions for CI when the project is ready for automation

## Repository model

Client projects should prefer one repository unless there is a strong reason to split.

Recommended layout:

- `app/` or `src/app/`: routes and page-level application structure
- `src/features/`: feature modules
- `src/server/`: server-side application logic
- `src/db/`: database schema, migrations, and data access
- `src/ui/`: reusable interface components
- `src/lib/`: shared utilities
- `tests/`: automated tests
- `docs/`: project documentation and decisions

## Modular boundaries

Feature modules should own their core workflows, UI, validation, server actions or API calls, and tests where practical.

Shared code should be promoted only when at least two modules genuinely need it.

Avoid global utility growth that hides business behavior.

## Backend default

Prefer the backend model already supported by the chosen framework.

For Next.js projects, use server-side framework capabilities first. Add a separate API service only when the contract, scale, security model, integration profile, or deployment target requires it.

## Database default

Use PostgreSQL by default.

Use Supabase when the project benefits from managed PostgreSQL, authentication, storage, row-level security, and quick deployment.

Database work must include explicit ownership of:

- schema changes
- migrations
- access control
- seed data
- backup expectations
- environment separation
- verification commands

## Authentication default

Use managed authentication when it reduces risk and meets the contract.

Acceptable defaults include Supabase Auth, Auth.js, Better Auth, or a client-required provider.

Do not build custom authentication unless there is a strong requirement.

## Testing default

Every project should define verification at these levels as appropriate:

- type checking
- linting
- unit or component tests
- integration tests
- Playwright end-to-end tests for critical workflows
- manual acceptance checks when automation is not practical

Agents must report verification evidence, not just completion claims.

## Deployment default

Use the simplest deployment target that satisfies the contract.

Common defaults:

- Vercel for Next.js websites and web apps
- Supabase for managed PostgreSQL and auth
- Railway or Render when a long-running backend service is needed
- Cloudflare when edge routing, DNS, or workers are central to the project

Production deploys require human approval.

## When to avoid the default stack

Use a different stack when:

- the client already has a required stack
- the project must integrate deeply with an existing platform
- compliance or hosting rules require it
- the project is primarily content-managed and better suited to Webflow, Framer, WordPress, or Shopify
- the project needs native mobile, desktop, or heavy real-time capabilities

## Explicit non-goals

The default system does not start with:

- microservices
- Kubernetes
- distributed event systems
- custom auth
- custom payment handling
- multi-repo architecture
- premature service extraction
- local model fine-tuning
- production automation without approval
