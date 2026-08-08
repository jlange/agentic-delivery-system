---
name: independent-local-review
description: Run and validate a mandatory read-only Claude Code review of a complete task-branch diff before push, tied to the exact HEAD commit with structured findings and dispositions. Use after implementation and local verification are committed, whenever HEAD changes after review, or when checking whether an existing review attestation still permits push or merge.
---

# Independent Local Review

Run the bundled tool from the repository root after committing and verifying the task:

```text
python <skill-dir>/scripts/review_branch.py --base origin/dev --output .delivery/reviews/review.json
```

Use the configured integration reference; `origin/dev` is only the default. The tool
verifies the base and non-empty three-dot diff, invokes Claude with read-only tools,
requires structured output, and records the base commit and exact reviewed HEAD.

## Review Loop

1. Commit the complete implementation before review.
2. Run the tool and inspect every finding.
3. Classify each finding as `fixed`, `accepted_out_of_scope`, `rejected`, `duplicate`,
   or `non_required_style`. Give a concise technical reason for every disposition
   except `fixed`.
4. Fix every valid in-scope finding, rerun verification, and commit.
5. Rerun review after any HEAD change. Never reuse an attestation for another commit.
6. Continue only when the current HEAD has a clean review or every finding has a valid
   recorded disposition accepted by repository policy.

Validate an attestation immediately before push or merge:

```text
python <skill-dir>/scripts/review_branch.py --check-attestation .delivery/reviews/review.json
```

Treat missing Claude, authentication or quota failures, timeout, invalid output,
repository-read failure, base-resolution failure, or SHA mismatch as blockers. Never
translate reviewer unavailability into approval. An approved fallback reviewer must be
independent of the implementation agent and produce the same attestation fields.

Read [references/review-contract.md](references/review-contract.md) when configuring a
fallback, retention policy, or external-model data boundary.
