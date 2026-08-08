# Independent Claude Code Review

Codex may implement, but Claude Code is the default independent read-only reviewer
before a task branch is pushed. Install Claude Code and authenticate it using the
project's approved account and data controls. Missing installation, authentication,
quota, repository access, valid output, or reviewer availability blocks delivery.

After verification and a local commit, run:

```text
python <independent-local-review-skill>/scripts/review_branch.py --base origin/dev --output .delivery/reviews/review.json
```

Change `--base` when the integration branch is not `dev`. The tool validates the base
and non-empty three-dot diff, restricts Claude to read-only capabilities, requests
structured findings, and records the merge base and exact HEAD.

Fix valid in-scope findings, verify, commit, and review again. Technically disposition
incorrect, duplicate, out-of-scope, or non-required stylistic findings. Any changed HEAD
invalidates the result. Before push or merge run:

```text
python <independent-local-review-skill>/scripts/review_branch.py --check-attestation .delivery/reviews/review.json
```

External review may transmit source to the model service. Configure external-review
permission, enterprise controls, sensitive-code restrictions, logs, and retention. An
approved fallback must remain independent and emit equivalent exact-HEAD evidence. No
available approved reviewer means stop, never bypass.

## Enforcement levels

1. `AGENTS.md` provides behavioral guidance.
2. The wrapper standardizes review execution and evidence.
3. Optional CI and branch protection require a trustworthy current-SHA attestation.
   A local pre-push hook may help but is not authoritative alone.
