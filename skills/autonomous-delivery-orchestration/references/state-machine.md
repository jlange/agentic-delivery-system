# Delivery State Machine

Use these task states as durable facts, not conversational labels:

```text
planned -> awaiting_approval -> approved_blocked_by_dependency -> executable
-> implementing -> verifying -> independent_review -> pull_request_open
-> changes_requested | approved -> merged -> unlock_dependents
```

The resumable boundary path is:

```text
implementing -> amendment_requested -> amendment_approved -> implementing
```

Only a human authorization artifact may enter `approved`, `amendment_approved`, or a
merge/deploy state protected by repository policy. Git and pull-request state provide
evidence for later transitions. Never infer a transition from a prompt alone.
