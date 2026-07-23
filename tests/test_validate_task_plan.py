from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parent.parent
SPEC = importlib.util.spec_from_file_location(
    "validate_task_plan",
    ROOT / "skills" / "task-decomposition" / "scripts" / "validate-task-plan.py",
)
assert SPEC and SPEC.loader
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


class ValidateTaskPlanTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = json.loads((ROOT / "schemas" / "task.schema.json").read_text())

    def task(self, task_id: str = "FE-001", dependencies: list[str] | None = None) -> dict:
        return {
            "id": task_id,
            "title": "Build approved project slice",
            "role": "frontend_engineer",
            "status": "draft",
            "risk": "low",
            "requirement_ids": ["REQ-001"],
            "dependencies": dependencies or [],
            "allowed_paths": ["src/features/example/**"],
            "forbidden_paths": [".env", ".env.*"],
            "acceptance_criteria": ["AC-001 is observable."],
            "verification_commands": ["pnpm test"],
            "required_evidence": ["Passing output for AC-001."],
            "human_gate": False,
        }

    def validate(self, tasks: list[dict], approved: set[str] | None = None) -> list[str]:
        with tempfile.TemporaryDirectory() as directory:
            paths = []
            for index, task in enumerate(tasks):
                path = Path(directory) / f"task-{index}.yaml"
                path.write_text(yaml.safe_dump(task, sort_keys=False), encoding="utf-8")
                paths.append(path)
            return VALIDATOR.validate_plan(paths, self.schema, approved or {"REQ-001", "AC-001"})

    def test_valid_draft_plan_is_accepted(self) -> None:
        self.assertEqual([], self.validate([self.task()]))

    def test_unapproved_or_missing_coverage_is_rejected(self) -> None:
        task = self.task()
        task["acceptance_criteria"] = ["Observable result without an approved ID."]
        task["required_evidence"] = ["Passing output."]
        errors = self.validate([task])
        self.assertTrue(any("without task coverage: AC-001" in error for error in errors))

    def test_unknown_dependency_and_cycle_are_rejected(self) -> None:
        unknown = self.task(dependencies=["API-999"])
        self.assertTrue(any("unknown dependency API-999" in error for error in self.validate([unknown])))

        first = self.task("FE-001", ["FE-002"])
        second = self.task("FE-002", ["FE-001"])
        errors = self.validate([first, second])
        self.assertTrue(any(error.startswith("dependency cycle:") for error in errors))

    def test_unsafe_allowed_path_is_rejected(self) -> None:
        task = self.task()
        task["allowed_paths"] = ["/mnt/c"]
        self.assertTrue(any("broad or unsafe" in error for error in self.validate([task])))

    def test_non_draft_task_is_rejected(self) -> None:
        task = self.task()
        task["status"] = "approved"
        self.assertTrue(any("status must be draft" in error for error in self.validate([task])))


if __name__ == "__main__":
    unittest.main()
