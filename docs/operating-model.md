# Operating Model

Humans approve product intent, architecture, and bounded delivery waves. Within that
authorization, agents autonomously synchronize the integration branch, create task
branches, implement, install ordinary dependencies, verify, commit, obtain independent
review, push, open and remediate pull requests, merge, synchronize locally, and verify
the merged result. The integration branch defaults to `dev` and is configurable.

## Delivery loop

```text
approved wave -> sync -> branch -> implement -> verify -> commit -> Claude exact-HEAD review
-> fix/disposition -> rereview after changes -> push -> PR -> CI/reviews -> remediation
-> merge -> sync integration -> verify merge -> complete
```

An open pull request is not completion.

## Risk-based escalation

Pause for financial consequences; legal, contractual, licensing, regulatory, or
compliance consequences; human-only credentials or permissions; production authority
not already granted; or an irreversible business decision unresolved by approved policy.
Scope amendments and sensitive-data conflicts retain their authorization gates. Routine
engineering operations are not business decisions; use normal tool permission prompts.

## Enforcement

- Behavioral guidance: repository `AGENTS.md`.
- Standardized execution: exact-HEAD review tooling and evidence.
- Optional mechanical enforcement: CI attestation validation and branch protection.
  Local hooks alone are insufficient.
