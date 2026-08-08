from __future__ import annotations

import importlib.util
import json
import unittest
from copy import deepcopy
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SPEC = importlib.util.spec_from_file_location(
    "validate_task", ROOT / "scripts" / "validate-task.py"
)
assert SPEC and SPEC.loader
VALIDATE_TASK = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATE_TASK)


class ValidateTaskTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = json.loads((ROOT / "schemas" / "task.schema.json").read_text())
        cls.valid_task = VALIDATE_TASK.load_yaml(
            ROOT / "tasks" / "ADS-001-validate-task-files.yaml"
        )

    def errors_for(self, **changes: object) -> list[str]:
        task = deepcopy(self.valid_task)
        task.update(changes)
        return VALIDATE_TASK.validate_task(task, self.schema)

    def test_approved_bounded_task_is_valid(self) -> None:
        self.assertEqual([], self.errors_for())

    def test_task_awaiting_approval_is_rejected(self) -> None:
        self.assertIn(
            "status: task is not in an executable approved state",
            self.errors_for(status="awaiting_approval"),
        )

    def test_dependency_merge_gate_must_match(self) -> None:
        errors = self.errors_for(dependencies=["DB-001"])
        self.assertIn("execution_gate.requires_merged: must match dependencies", errors)

    def test_approved_amendment_requires_artifact(self) -> None:
        errors = self.errors_for(amendments=[{
            "requested_path": "src/schema.ts",
            "reason": "Required integrity constraint.",
            "permitted_change": "Composite key only.",
            "status": "approved",
        }])
        self.assertTrue(any("approval_artifact" in error for error in errors))

    def test_missing_path_boundaries_are_rejected(self) -> None:
        errors = self.errors_for(allowed_paths=[])
        self.assertTrue(any(error.startswith("allowed_paths:") for error in errors))

    def test_missing_requirement_ids_are_rejected(self) -> None:
        errors = self.errors_for(requirement_ids=[])
        self.assertTrue(any(error.startswith("requirement_ids:") for error in errors))

    def test_incomplete_evidence_is_rejected(self) -> None:
        errors = self.errors_for(required_evidence=[])
        self.assertTrue(any(error.startswith("required_evidence:") for error in errors))

    def test_broad_or_sensitive_allowed_paths_are_rejected(self) -> None:
        for path in ("/mnt/c", "~/work", "/home/person/project", "clients/acme/**", "../other"):
            with self.subTest(path=path):
                errors = self.errors_for(allowed_paths=[path])
                self.assertTrue(any("access is forbidden" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
