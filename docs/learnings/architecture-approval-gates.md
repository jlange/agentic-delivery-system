# Architecture approval gates

An architecture recommendation and its approval are separate artifacts. The architect
sets an authoring status: `draft` means complete for human review, while `blocked` means
an unresolved requirement prevents a final recommendation. Neither state is human
approval. Only a human may approve the separate checklist and authorize project setup.

Human approval should identify both the stable relative artifact path and a SHA-256
digest. Binding approval to content prevents an edited recommendation from inheriting
approval intended for an earlier version.

Project-initialization automation must fail closed. It should require a non-empty
recommendation plus a durable checklist that identifies the reviewer and date, resolves
material operational decisions, records no unresolved blockers, approves data handling,
and explicitly authorizes project setup. The existence of an intake approval or an
architecture document alone is not sufficient evidence.

Fail-closed parsing does not require brittle presentation matching. Human-authored
status fields may safely ignore capitalization and surrounding whitespace, and a
no-blocker declaration may accept a small explicit allowlist such as `None` or
`No unresolved blockers`. Validators should ignore blank lines and harmless Markdown
bullets while continuing to reject misspellings, ambiguous prose, stale digests,
incorrect artifact paths, and unresolved decisions.

Traceability gates should compare unique approved intake IDs against IDs found only in
the recommendation's traceability section. Searching the whole document or checking for
one example ID can hide omissions; validators should report the complete missing set.

Project setup must eventually create the long-lived `main`, `dev`, `qa`, and `staging`
branches required by `docs/branching-strategy.md`. The demo initializer remains a
minimal example, while the `project-setup` skill requires all four local branches at
the reviewed scaffold commit before setup is complete.
