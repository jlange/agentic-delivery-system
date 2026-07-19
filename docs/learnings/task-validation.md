# Task validation

JSON Schema verifies the structure of delivery tasks, but execution readiness also
requires policy checks. In particular, a structurally valid draft must not be
treated as executable, and `allowed_paths` must not grant broad access to home,
client, parent, absolute, or mounted-drive locations.

Run task validation before starting implementation:

```bash
python3 scripts/validate-task.py tasks/<task-file>.yaml
```

The validator depends on the development-only packages in `requirements-dev.txt`.
It exits nonzero and reports field-level errors when a task is malformed,
unapproved, or grants unsafe access.
