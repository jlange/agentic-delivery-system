# Review Contract

## Required result

Store reviewer identity and model, base reference and merge-base SHA, reviewed HEAD SHA,
UTC timestamp, status, findings, dispositions, and final clean-review status. Each
finding contains severity, file, line, and explanation.

`clean` means the reviewer ran successfully and returned no actionable findings. It
never means the reviewer was missing, unavailable, unauthenticated, rate-limited,
timed out, unable to read the repository, or returned invalid output.

## Data boundary

Claude Code may transmit repository source to an external service. Before enabling it,
apply the project's approved policy for external-model use, enterprise data controls,
regulated or sensitive code, logging, and retention. Projects that prohibit external
review must configure an approved self-hosted independent reviewer or stop at the gate.
Never print credentials or sensitive environment variables.

## Stronger enforcement

Local review tooling standardizes execution but is not authoritative enforcement. CI
may validate a signed or otherwise trustworthy attestation for the current SHA, while
branch protection requires that check. A pre-push hook is useful feedback but cannot be
the only control because it can be bypassed locally.
