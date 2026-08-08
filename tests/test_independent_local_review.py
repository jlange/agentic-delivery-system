from __future__ import annotations

import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "skills" / "independent-local-review" / "scripts" / "review_branch.py"
SPEC = importlib.util.spec_from_file_location("review_branch", SCRIPT)
assert SPEC and SPEC.loader
REVIEW = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(REVIEW)


class IndependentReviewTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.output = Path(self.temp.name) / "review.json"

    @staticmethod
    def git_result(*args: str) -> str:
        return {
            ("rev-parse", "--verify", "origin/qa^{commit}"): "base-tip",
            ("merge-base", "origin/qa", "HEAD"): "base-sha",
            ("rev-parse", "HEAD"): "head-sha",
            ("diff", "--name-only", "origin/qa...HEAD"): "src/app.py",
        }[args]

    def test_custom_base_and_clean_review_continue(self) -> None:
        response = {"result": json.dumps({"status": "clean", "reviewer_model": "claude-test", "findings": []})}
        completed = subprocess.CompletedProcess([], 0, json.dumps(response), "")
        with patch.object(REVIEW.shutil, "which", return_value="claude"), patch.object(REVIEW, "run_git", side_effect=self.git_result), patch.object(REVIEW.subprocess, "run", return_value=completed) as runner:
            REVIEW.run_review("origin/qa", self.output, 30, "claude")
        self.assertIn("origin/qa...HEAD", runner.call_args.args[0][2])
        self.assertTrue(json.loads(self.output.read_text())["final_clean_review"])

    def test_missing_claude_fails_safely(self) -> None:
        with patch.object(REVIEW.shutil, "which", return_value=None), self.assertRaisesRegex(REVIEW.ReviewError, "executable not found"):
            REVIEW.run_review("origin/qa", self.output, 30, "claude")
        self.assertFalse(self.output.exists())

    def test_missing_base_fails_safely(self) -> None:
        with patch.object(REVIEW.shutil, "which", return_value="claude"), patch.object(REVIEW, "run_git", side_effect=REVIEW.ReviewError("missing")), self.assertRaisesRegex(REVIEW.ReviewError, "does not resolve"):
            REVIEW.run_review("origin/missing", self.output, 30, "claude")

    def test_empty_diff_is_not_approval(self) -> None:
        def empty(*args: str) -> str:
            return "" if args[0] == "diff" else "sha"
        with patch.object(REVIEW.shutil, "which", return_value="claude"), patch.object(REVIEW, "run_git", side_effect=empty), self.assertRaisesRegex(REVIEW.ReviewError, "No branch diff"):
            REVIEW.run_review("origin/dev", self.output, 30, "claude")
        self.assertFalse(self.output.exists())

    def test_reviewer_failure_is_not_approval(self) -> None:
        failed = subprocess.CompletedProcess([], 1, "", "authentication required")
        with patch.object(REVIEW.shutil, "which", return_value="claude"), patch.object(REVIEW, "run_git", side_effect=self.git_result), patch.object(REVIEW.subprocess, "run", return_value=failed), self.assertRaisesRegex(REVIEW.ReviewError, "not approved"):
            REVIEW.run_review("origin/qa", self.output, 30, "claude")

    def test_old_head_is_invalid_and_findings_need_disposition(self) -> None:
        record = {"review_status": "findings", "reviewed_head_sha": "old", "findings": [{"disposition": "pending"}]}
        self.output.write_text(json.dumps(record))
        with patch.object(REVIEW, "run_git", return_value="new"), self.assertRaisesRegex(REVIEW.ReviewError, "stale"):
            REVIEW.validate_attestation(self.output)
        record["reviewed_head_sha"] = "new"
        self.output.write_text(json.dumps(record))
        with patch.object(REVIEW, "run_git", return_value="new"), self.assertRaisesRegex(REVIEW.ReviewError, "unresolved"):
            REVIEW.validate_attestation(self.output)
        record["findings"][0] = {"disposition": "rejected", "disposition_reason": "Conflicts with AC-002."}
        self.output.write_text(json.dumps(record))
        with patch.object(REVIEW, "run_git", return_value="new"):
            REVIEW.validate_attestation(self.output)

    def test_templates_and_escalation_policy(self) -> None:
        agents = (ROOT / "templates" / "repository" / "AGENTS.md").read_text()
        attrs = (ROOT / "templates" / "repository" / ".gitattributes").read_text()
        self.assertIn("financial", agents)
        self.assertIn("routine in-scope engineering", agents)
        self.assertEqual("*.sh text eol=lf\n", attrs)


if __name__ == "__main__":
    unittest.main()
