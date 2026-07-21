from __future__ import annotations

import os
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "skills" / "client-delivery-pipeline" / "scripts" / "client_pipeline.sh"


class ArchitectureGateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        self.work_root = Path(self.temporary_directory.name) / "work"
        self.clients_root = self.work_root / "clients"
        self.environment = os.environ.copy()
        self.environment.update(
            {
                "WORK_ROOT": str(self.work_root),
                "CLIENTS_ROOT": str(self.clients_root),
                "SYSTEM_ROOT": str(ROOT),
            }
        )
        self.run_script("init-intake", "example")
        self.intake = self.clients_root / "example" / "intake"
        (self.intake / "outputs" / "contract_intake_output.md").write_text(
            "# Contract Intake Output\n\nREQ-001: Example.\nAC-001: Observable result.\n",
            encoding="utf-8",
        )
        (self.intake / "decisions" / "intake_review_checklist.md").write_text(
            """# Approved Intake Review

Intake status: approved
Allowed paths: intake/outputs and intake/decisions
Forbidden paths: mounted drives, home, and unrelated client folders
Raw source review: prohibited
Redaction requirement: required
External AI client-data use: prohibited
""",
            encoding="utf-8",
        )

    def run_script(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["bash", str(SCRIPT), *arguments],
            env=self.environment,
            text=True,
            capture_output=True,
            check=False,
        )

    def write_architecture_artifacts(self, *, approved: bool) -> None:
        (self.intake / "outputs" / "architecture_recommendation.md").write_text(
            """# Architecture Recommendation

## Recommendation Status
draft
## Data-Handling Declarations
Approved declarations.
## System and Component Boundaries
Component A.
## Data Flows
Input to output.
## Recommended Technical Stack
Default stack.
## Accessibility Requirements
REQ-001 applies.
## Backup and Recovery Expectations
Documented.
## Testing and Verification Strategy
AC-001 is verified.
## Requirements Traceability
REQ-001 and AC-001.
## Execution Plan
One phase.
## Dependency and Sequencing Notes
None.
## Architecture Decision Records
ADR-001.
""",
            encoding="utf-8",
        )
        status = "approved" if approved else "draft"
        authorization = "approved" if approved else "pending"
        decisions = "approved" if approved else "pending"
        blockers = "None." if approved else "REQ-002 needs a hosting decision."
        (self.intake / "decisions" / "architecture_review_checklist.md").write_text(
            f"""# Architecture Review Checklist

Architecture status: {status}
Approved architecture and execution plan: ../outputs/architecture_recommendation.md
Data-handling approval: {decisions}
Security decision: {decisions}
Privacy decision: {decisions}
Accessibility decision: {decisions}
Backup and recovery decision: {decisions}
Hosting decision: {decisions}
Paid-service decision: {decisions}
Authorization to proceed to project setup: {authorization}
Reviewer: Project Owner
Review date: 2026-07-20

## Rejected Or Deferred Alternatives

None.

## Unresolved Blockers
{blockers}
""",
            encoding="utf-8",
        )

    def test_architecture_prompt_requires_approved_intake_artifacts(self) -> None:
        result = self.run_script("write-architecture-prompt", "example")
        self.assertEqual(0, result.returncode, result.stderr)
        prompt = self.intake / "notes" / "architecture_recommendation_prompt.md"
        self.assertTrue(prompt.is_file())
        prompt_text = prompt.read_text(encoding="utf-8")
        self.assertIn("Allowed write paths", prompt_text)
        self.assertIn("skills/architecture-recommendation/SKILL.md", prompt_text)

    def test_architecture_prompt_rejects_unapproved_intake(self) -> None:
        checklist = self.intake / "decisions" / "intake_review_checklist.md"
        checklist.write_text("Intake status: draft\n", encoding="utf-8")
        result = self.run_script("write-architecture-prompt", "example")
        self.assertNotEqual(0, result.returncode)
        self.assertIn("intake status must be approved", result.stderr)

    def test_generated_intake_checklist_has_architecture_gate_fields(self) -> None:
        result = self.run_script("write-review-checklist", "example")
        self.assertEqual(0, result.returncode, result.stderr)
        checklist = self.intake / "decisions" / "intake_review_checklist.md"
        checklist_text = checklist.read_text(encoding="utf-8")
        self.assertIn("Intake status: draft", checklist_text)
        self.assertIn("External AI client-data use: pending", checklist_text)

    def test_init_demo_repo_rejects_incomplete_architecture(self) -> None:
        self.write_architecture_artifacts(approved=True)
        output = self.intake / "outputs" / "architecture_recommendation.md"
        output.write_text("# Architecture Recommendation\n", encoding="utf-8")
        result = self.run_script("init-demo-repo", "example", "demo")
        self.assertNotEqual(0, result.returncode)
        self.assertIn("missing section", result.stderr)

    def test_init_demo_repo_rejects_missing_architecture_evidence(self) -> None:
        result = self.run_script("init-demo-repo", "example", "demo")
        self.assertNotEqual(0, result.returncode)
        self.assertIn("architecture recommendation missing", result.stderr)
        self.assertFalse((self.clients_root / "example" / "demo").exists())

    def test_init_demo_repo_rejects_draft_architecture(self) -> None:
        self.write_architecture_artifacts(approved=False)
        result = self.run_script("init-demo-repo", "example", "demo")
        self.assertNotEqual(0, result.returncode)
        self.assertIn("architecture status must be approved", result.stderr)
        self.assertFalse((self.clients_root / "example" / "demo").exists())

    def test_init_demo_repo_accepts_complete_human_approval(self) -> None:
        self.write_architecture_artifacts(approved=True)
        result = self.run_script("init-demo-repo", "example", "demo")
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertTrue((self.clients_root / "example" / "demo" / ".git").is_dir())


if __name__ == "__main__":
    unittest.main()
