# Architecture approval gates

An architecture recommendation and its approval are separate artifacts. The architect
may write a draft recommendation and draft review checklist, but only a human may set
the architecture status to approved and authorize project setup.

Project-initialization automation must fail closed. It should require a non-empty
recommendation plus a durable checklist that identifies the reviewer and date, resolves
material operational decisions, records no unresolved blockers, approves data handling,
and explicitly authorizes project setup. The existence of an intake approval or an
architecture document alone is not sufficient evidence.
