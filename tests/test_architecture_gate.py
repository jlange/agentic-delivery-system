from __future__ import annotations

import hashlib
import os
import re
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "skills" / "client-delivery-pipeline" / "scripts" / "client_pipeline.sh"


def bash_path(path: Path) -> str:
    """Return a path Git Bash and native Bash can both consume."""
    resolved_path = path.resolve()
    try:
        relative = resolved_path.relative_to(ROOT)
        return relative.as_posix() or "."
    except ValueError:
        pass
    resolved = str(resolved_path)
    if os.name == "nt":
        drive, remainder = os.path.splitdrive(resolved)
        return f"/{drive[0].lower()}{remainder.replace(chr(92), '/')}"
    return resolved


class ArchitectureGateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory(dir=ROOT)
        self.addCleanup(self.temporary_directory.cleanup)
        self.work_root = Path(self.temporary_directory.name) / "work"
        self.clients_root = self.work_root / "clients"
        self.environment = os.environ.copy()
        self.environment.update(
            {
                "WORK_ROOT": bash_path(self.work_root),
                "CLIENTS_ROOT": bash_path(self.clients_root),
                "SYSTEM_ROOT": bash_path(ROOT),
            }
        )
        initialization = self.run_script("init-intake", "example")
        self.assertEqual(0, initialization.returncode, initialization.stderr)
        self.intake = self.clients_root / "example" / "intake"
        (self.intake / "outputs" / "contract_intake_output.md").write_text(
            """# Contract Intake Output

REQ-001: First requirement.
REQ-002: Second requirement.
AC-001: First observable result.
AC-002: Second observable result.
""",
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
            ["bash", "-l", bash_path(SCRIPT), *arguments],
            env=self.environment,
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def write_architecture_artifacts(
        self,
        *,
        authoring_status: str | None = "draft",
        review_status: str = "approved",
        authorization: str = "approved",
        traceability: str = "REQ-001 REQ-002 AC-001 AC-002.",
    ) -> None:
        status_line = (
            f"Authoring status: {authoring_status}" if authoring_status is not None else ""
        )
        recommendation = f"""# Architecture Recommendation

## Authoring State
{status_line}
## Data-Handling Declarations
Approved declarations.
## System and Component Boundaries
Component A.
## Data Flows
Input to output.
## Recommended Technical Stack
Default stack.
## Accessibility Requirements
REQ-001 and REQ-002 apply.
## Backup and Recovery Expectations
Documented.
## Testing and Verification Strategy
AC-001 and AC-002 are verified.
## Requirements Traceability
{traceability}
## Execution Plan
One phase.
## Dependency and Sequencing Notes
None.
## Architecture Decision Records
ADR-001.
"""
        output = self.intake / "outputs" / "architecture_recommendation.md"
        output.write_text(recommendation, encoding="utf-8")
        digest = hashlib.sha256(output.read_bytes()).hexdigest()
        decisions = "approved" if review_status == "approved" else "pending"
        blockers = "None." if review_status == "approved" else "REQ-002 needs a decision."
        (self.intake / "decisions" / "architecture_review_checklist.md").write_text(
            f"""# Architecture Review Checklist

Architecture review status: {review_status}
Approved recommendation artifact: ../outputs/architecture_recommendation.md
Approved recommendation SHA-256: {digest}
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

    def test_architecture_prompt_accepts_case_and_whitespace_variations(self) -> None:
        checklist = self.intake / "decisions" / "intake_review_checklist.md"
        checklist.write_text(
            """# Approved Intake Review

"""
            + "  intake STATUS : APPROVED  \n"
            + """
Allowed Paths: intake/outputs and intake/decisions
Forbidden Paths: mounted drives and unrelated client folders
Raw Source Review: Prohibited
Redaction Requirement: Required
External AI Client-Data Use: Prohibited
""",
            encoding="utf-8",
        )
        result = self.run_script("write-architecture-prompt", "example")
        self.assertEqual(0, result.returncode, result.stderr)

    def test_generated_intake_checklist_has_architecture_gate_fields(self) -> None:
        result = self.run_script("write-review-checklist", "example")
        self.assertEqual(0, result.returncode, result.stderr)
        checklist = self.intake / "decisions" / "intake_review_checklist.md"
        checklist_text = checklist.read_text(encoding="utf-8")
        self.assertIn("Intake status: draft", checklist_text)
        self.assertIn("External AI client-data use: pending", checklist_text)

    def test_init_demo_repo_rejects_incomplete_architecture(self) -> None:
        self.write_architecture_artifacts()
        output = self.intake / "outputs" / "architecture_recommendation.md"
        output.write_text("# Architecture Recommendation\n", encoding="utf-8")
        result = self.run_script("init-demo-repo", "example", "demo")
        self.assertNotEqual(0, result.returncode)
        self.assertIn("exactly one section", result.stderr)

    def test_init_demo_repo_rejects_missing_architecture_evidence(self) -> None:
        result = self.run_script("init-demo-repo", "example", "demo")
        self.assertNotEqual(0, result.returncode)
        self.assertIn("architecture recommendation missing", result.stderr)
        self.assertFalse((self.clients_root / "example" / "demo").exists())

    def test_init_demo_repo_rejects_draft_checklist_approval(self) -> None:
        self.write_architecture_artifacts(review_status="draft", authorization="pending")
        result = self.run_script("init-demo-repo", "example", "demo")
        self.assertNotEqual(0, result.returncode)
        self.assertIn("architecture review status must be approved", result.stderr)
        self.assertFalse((self.clients_root / "example" / "demo").exists())

    def test_init_demo_repo_rejects_blocked_recommendation_with_human_approval(self) -> None:
        self.write_architecture_artifacts(authoring_status="blocked")
        result = self.run_script("init-demo-repo", "example", "demo")
        self.assertNotEqual(0, result.returncode)
        self.assertIn("authoring status is blocked", result.stderr)

    def test_init_demo_repo_rejects_missing_or_invalid_authoring_status(self) -> None:
        cases = (
            (None, "exactly one Authoring status"),
            ("incomplete", "Authoring status must be draft or blocked"),
        )
        for status, expected_error in cases:
            with self.subTest(status=status):
                self.write_architecture_artifacts(authoring_status=status)
                result = self.run_script("init-demo-repo", "example", "demo")
                self.assertNotEqual(0, result.returncode)
                self.assertIn(expected_error, result.stderr)

    def test_init_demo_repo_rejects_missing_human_authorization(self) -> None:
        self.write_architecture_artifacts(authorization="pending")
        result = self.run_script("init-demo-repo", "example", "demo")
        self.assertNotEqual(0, result.returncode)
        self.assertIn("project setup is not explicitly authorized", result.stderr)

    def test_init_demo_repo_rejects_recommendation_changed_after_approval(self) -> None:
        self.write_architecture_artifacts()
        output = self.intake / "outputs" / "architecture_recommendation.md"
        output.write_text(
            output.read_text(encoding="utf-8") + "\nPost-review change.\n",
            encoding="utf-8",
        )
        result = self.run_script("init-demo-repo", "example", "demo")
        self.assertNotEqual(0, result.returncode)
        self.assertIn("does not match the current recommendation", result.stderr)

    def test_complete_intake_traceability_is_accepted(self) -> None:
        self.write_architecture_artifacts()
        result = self.run_script("init-demo-repo", "example", "demo")
        self.assertEqual(0, result.returncode, result.stderr)

    def test_validate_architecture_gate_does_not_create_project(self) -> None:
        self.write_architecture_artifacts()
        result = self.run_script("validate-architecture-gate", "example")
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("Architecture gate approved for example", result.stdout)
        self.assertEqual([], list((self.clients_root / "example").glob("*/.git")))

    def test_gate_accepts_harmless_human_format_variations(self) -> None:
        self.write_architecture_artifacts()
        output = self.intake / "outputs" / "architecture_recommendation.md"
        recommendation = output.read_text(encoding="utf-8")
        recommendation = recommendation.replace(
            "## Authoring State\nAuthoring status: draft",
            "  ## authoring state  \n Authoring Status : DRAFT ",
        )
        output.write_text(recommendation, encoding="utf-8")
        digest = hashlib.sha256(output.read_bytes()).hexdigest().upper()

        checklist = self.intake / "decisions" / "architecture_review_checklist.md"
        review = checklist.read_text(encoding="utf-8")
        review = re.sub(
            r"Approved recommendation SHA-256: [0-9a-f]{64}",
            f"Approved Recommendation SHA-256 : {digest}",
            review,
        )
        review = review.replace(": approved", ": APPROVED")
        review = review.replace(
            "## Unresolved Blockers\nNone.",
            "## unresolved blockers\n\nnone",
        )
        review = review.replace(
            "## Rejected Or Deferred Alternatives",
            "## rejected or deferred alternatives",
        )
        checklist.write_text(review, encoding="utf-8")

        result = self.run_script("validate-architecture-gate", "example")
        self.assertEqual(0, result.returncode, result.stderr)

    def test_gate_accepts_unambiguous_no_blocker_phrases(self) -> None:
        for declaration in ("None", "none.", "- No blockers", "No unresolved blockers."):
            with self.subTest(declaration=declaration):
                self.write_architecture_artifacts()
                checklist = self.intake / "decisions" / "architecture_review_checklist.md"
                review = checklist.read_text(encoding="utf-8")
                review = review.replace("## Unresolved Blockers\nNone.", f"## Unresolved Blockers\n\n{declaration}")
                checklist.write_text(review, encoding="utf-8")
                result = self.run_script("validate-architecture-gate", "example")
                self.assertEqual(0, result.returncode, result.stderr)

    def test_gate_rejects_ambiguous_no_blocker_declaration(self) -> None:
        self.write_architecture_artifacts()
        checklist = self.intake / "decisions" / "architecture_review_checklist.md"
        review = checklist.read_text(encoding="utf-8")
        review = review.replace(
            "## Unresolved Blockers\nNone.",
            "## Unresolved Blockers\nNone, except hosting approval.",
        )
        checklist.write_text(review, encoding="utf-8")
        result = self.run_script("validate-architecture-gate", "example")
        self.assertNotEqual(0, result.returncode)
        self.assertIn("unresolved architecture blockers", result.stderr)

    def test_gate_rejects_pending_case_insensitively(self) -> None:
        self.write_architecture_artifacts()
        checklist = self.intake / "decisions" / "architecture_review_checklist.md"
        review = checklist.read_text(encoding="utf-8")
        review = review.replace("Security decision: approved", "Security decision: PENDING")
        checklist.write_text(review, encoding="utf-8")
        result = self.run_script("validate-architecture-gate", "example")
        self.assertNotEqual(0, result.returncode)
        self.assertIn("Security decision must be resolved", result.stderr)

    def test_missing_requirement_mapping_is_rejected(self) -> None:
        self.write_architecture_artifacts(traceability="REQ-001 AC-001 AC-002.")
        result = self.run_script("init-demo-repo", "example", "demo")
        self.assertNotEqual(0, result.returncode)
        self.assertIn("missing approved IDs: REQ-002", result.stderr)

    def test_missing_acceptance_criterion_mapping_is_rejected(self) -> None:
        self.write_architecture_artifacts(traceability="REQ-001 REQ-002 AC-001.")
        result = self.run_script("init-demo-repo", "example", "demo")
        self.assertNotEqual(0, result.returncode)
        self.assertIn("AC-002", result.stderr)

    def test_ids_outside_traceability_section_do_not_count(self) -> None:
        self.write_architecture_artifacts(traceability="REQ-001 AC-001.")
        result = self.run_script("init-demo-repo", "example", "demo")
        self.assertNotEqual(0, result.returncode)
        self.assertIn("AC-002", result.stderr)
        self.assertIn("REQ-002", result.stderr)

    def test_duplicate_mappings_do_not_conceal_missing_id(self) -> None:
        self.write_architecture_artifacts(
            traceability="REQ-001 REQ-001 AC-001 AC-001 AC-002."
        )
        result = self.run_script("init-demo-repo", "example", "demo")
        self.assertNotEqual(0, result.returncode)
        self.assertIn("REQ-002", result.stderr)

    def test_absent_or_malformed_traceability_section_is_rejected(self) -> None:
        for replacement in ("", "### Requirements Traceability"):
            with self.subTest(replacement=replacement):
                self.write_architecture_artifacts()
                output = self.intake / "outputs" / "architecture_recommendation.md"
                recommendation = output.read_text(encoding="utf-8")
                recommendation = recommendation.replace(
                    "## Requirements Traceability", replacement
                )
                output.write_text(recommendation, encoding="utf-8")
                result = self.run_script("init-demo-repo", "example", "demo")
                self.assertNotEqual(0, result.returncode)
                self.assertIn(
                    "exactly one section: Requirements Traceability", result.stderr
                )

    def test_init_demo_repo_accepts_complete_human_approval(self) -> None:
        self.write_architecture_artifacts()
        result = self.run_script("init-demo-repo", "example", "demo")
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertTrue((self.clients_root / "example" / "demo" / ".git").is_dir())


if __name__ == "__main__":
    unittest.main()
