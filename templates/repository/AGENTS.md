# Delivery policy

- Use the configured integration branch (`dev` unless project configuration says otherwise).
- Synchronize it, create an isolated task branch, and implement only approved scope.
- Run all relevant tests, linters, type checks, and builds; commit before review.
- Before push, run the configured independent Claude Code review against the complete
  `<integration-base>...HEAD` diff. Claude is read-only. Fix valid in-scope findings,
  verify and commit again, then review the new HEAD. Never bypass a failed, unavailable,
  invalid, or stale review.
- Push the task branch, create a pull request into the integration branch, wait for
  required checks and reviews, and address actionable feedback.
- Merge when repository requirements pass and existing authorization permits it. Then
  update the local integration branch and verify the merged commit and required checks.
  Pull-request creation alone is not completion.
- Pause for financial, legal, contractual, licensing, regulatory, compliance, missing
  credential/permission, ungranted production authority, or irreversible business
  decisions. Continue routine in-scope engineering work autonomously, using normal tool
  permission prompts where required.
- Source sent to an external reviewer must comply with the project's data policy.
