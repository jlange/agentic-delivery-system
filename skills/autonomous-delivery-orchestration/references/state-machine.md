# Delivery State Machine

Use these task states as durable facts, not conversational labels:

```text
planned -> awaiting_approval -> approved_blocked_by_dependency -> executable
-> implementing -> verifying -> committed -> independent_review
-> review_findings -> implementing | review_current_head_valid -> pushed
-> pull_request_open -> checks_pending -> changes_requested | merge_ready
-> merged -> post_merge_verifying -> complete -> unlock_dependents
```

The resumable boundary path is:

```text
implementing -> amendment_requested -> amendment_approved -> implementing
```

Only a human authorization artifact may enter initial task-plan approval,
`amendment_approved`, or a production action requiring authority not already granted.
An approved wave may authorize routine pull-request and merge transitions. Git,
review-attestation, CI, and pull-request state provide evidence. Never infer a
transition from a prompt alone, and never enter `complete` before post-merge verification.
