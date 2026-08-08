#!/usr/bin/env python3
"""Run a read-only Claude review and attest it to an exact Git HEAD."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


PROMPT = """Review the complete branch diff against {base}. Look for correctness bugs,
security issues, regressions, missing tests, and violations of the task contract. Report
only actionable findings with severity, file, line, and explanation. If there are no
actionable findings, state that explicitly. Do not modify files.

Inspect the merge-base-aware diff equivalent to: git diff {base}...HEAD
Return ONLY JSON with this shape:
{{"status":"clean|findings","reviewer_model":"model name or unknown","findings":[
{{"severity":"critical|high|medium|low","file":"path","line":1,"explanation":"..."}}
]}}"""

READ_ONLY_TOOLS = (
    "Read,Grep,Glob,Bash(git diff:*),Bash(git status:*),"
    "Bash(git rev-parse:*),Bash(git merge-base:*),Bash(git show:*)"
)


class ReviewError(RuntimeError):
    pass


def run_git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args], text=True, capture_output=True, check=False
    )
    if result.returncode:
        raise ReviewError(result.stderr.strip() or f"git {' '.join(args)} failed")
    return result.stdout.strip()


def parse_reviewer_output(stdout: str) -> dict:
    try:
        outer = json.loads(stdout)
        payload = outer.get("result", outer) if isinstance(outer, dict) else outer
        if isinstance(payload, str):
            payload = json.loads(payload)
    except (json.JSONDecodeError, AttributeError) as exc:
        raise ReviewError("Claude returned invalid structured review output") from exc
    if not isinstance(payload, dict):
        raise ReviewError("Claude returned invalid structured review output")
    status = payload.get("status")
    findings = payload.get("findings")
    if status not in {"clean", "findings"} or not isinstance(findings, list):
        raise ReviewError("Claude review output is missing status or findings")
    if status == "clean" and findings:
        raise ReviewError("Claude marked a review clean while returning findings")
    if status == "findings" and not findings:
        raise ReviewError("Claude reported findings without structured findings")
    required = {"severity", "file", "line", "explanation"}
    if any(not isinstance(item, dict) or not required <= item.keys() for item in findings):
        raise ReviewError("Claude returned a malformed finding")
    return payload


def validate_attestation(path: Path) -> None:
    try:
        record = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ReviewError(f"Cannot read valid review attestation: {path}") from exc
    head = run_git("rev-parse", "HEAD")
    if record.get("reviewed_head_sha") != head:
        raise ReviewError("Review is stale: reviewed SHA does not match current HEAD")
    status = record.get("review_status")
    if status not in {"clean", "findings"}:
        raise ReviewError("Review attestation has no successful review status")
    findings = record.get("findings", [])
    if status == "clean" and findings:
        raise ReviewError("Clean review attestation unexpectedly contains findings")
    if status == "findings":
        allowed = {"accepted_out_of_scope", "rejected", "duplicate", "non_required_style"}
        for finding in findings:
            if finding.get("disposition") not in allowed or not finding.get("disposition_reason"):
                raise ReviewError("Review findings remain unresolved; push or merge is blocked")


def run_review(base: str, output: Path, timeout: int, claude: str) -> None:
    executable = shutil.which(claude)
    if not executable:
        raise ReviewError(f"Claude Code executable not found: {claude}")
    try:
        run_git("rev-parse", "--verify", f"{base}^{{commit}}")
    except ReviewError as exc:
        raise ReviewError(f"Base reference does not resolve: {base}") from exc
    base_sha = run_git("merge-base", base, "HEAD")
    head_sha = run_git("rev-parse", "HEAD")
    if not run_git("diff", "--name-only", f"{base}...HEAD"):
        raise ReviewError("No branch diff to review; no review attestation was created")

    command = [
        executable, "-p", PROMPT.format(base=base), "--output-format", "json",
        "--permission-mode", "dontAsk", "--allowedTools", READ_ONLY_TOOLS,
    ]
    try:
        result = subprocess.run(
            command, text=True, capture_output=True, check=False, timeout=timeout
        )
    except subprocess.TimeoutExpired as exc:
        raise ReviewError(f"Claude review timed out after {timeout} seconds") from exc
    if result.returncode:
        detail = result.stderr.strip() or result.stdout.strip() or "unknown error"
        raise ReviewError(f"Claude review failed; not approved: {detail}")
    payload = parse_reviewer_output(result.stdout)
    findings = payload["findings"]
    record = {
        "review_status": payload["status"],
        "reviewer_identity": "Claude Code",
        "reviewer_model": payload.get("reviewer_model", "unknown"),
        "base_reference": base,
        "base_commit_sha": base_sha,
        "reviewed_head_sha": head_sha,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "findings": [{**item, "disposition": "pending"} for item in findings],
        "final_clean_review": payload["status"] == "clean",
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(f"Review recorded for {head_sha}: {payload['status']}")
    if findings:
        raise ReviewError("Actionable findings recorded; push or merge is blocked")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", default="origin/dev")
    parser.add_argument("--output", type=Path, default=Path(".delivery/reviews/review.json"))
    parser.add_argument("--timeout", type=int, default=900)
    parser.add_argument("--claude-command", default="claude")
    parser.add_argument("--check-attestation", type=Path)
    args = parser.parse_args()
    try:
        if args.check_attestation:
            validate_attestation(args.check_attestation)
            print("Review attestation is valid for current HEAD")
        else:
            run_review(args.base, args.output, args.timeout, args.claude_command)
    except ReviewError as exc:
        print(f"review blocked: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
