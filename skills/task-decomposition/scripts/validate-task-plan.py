#!/usr/bin/env python3
"""Validate a task set awaiting durable human approval."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path, PurePosixPath
from typing import Any

import jsonschema
import yaml


ID_PATTERN = re.compile(r"\b(?:REQ|AC)-\d{3}\b")
DATE_PATTERN = re.compile(r"\d{4}-\d{2}-\d{2}")
FORBIDDEN_ALLOWED_PATHS = {"/", "/home", "/mnt", "/mnt/c", "/mnt/d", "/mnt/e", "~", "~/", "clients", "clients/**"}


def unsafe_allowed_path(value: str) -> bool:
    path = value.strip().replace("\\", "/")
    if path in FORBIDDEN_ALLOWED_PATHS or path.startswith(("~/", "/home/", "/mnt/", "../", "/")):
        return True
    parts = PurePosixPath(path).parts
    return bool(parts and parts[0] == "clients")


def load_task(path: Path) -> Any:
    with path.open(encoding="utf-8") as stream:
        return yaml.safe_load(stream)


def schema_errors(task: Any, schema: dict[str, Any]) -> list[str]:
    validator = jsonschema.Draft202012Validator(schema)
    result = []
    for error in sorted(validator.iter_errors(task), key=lambda item: list(item.absolute_path)):
        location = ".".join(str(part) for part in error.absolute_path) or "<root>"
        result.append(f"{location}: {error.message}")
    return result


def find_cycle(dependencies: dict[str, list[str]]) -> list[str] | None:
    visiting: list[str] = []
    visited: set[str] = set()

    def visit(task_id: str) -> list[str] | None:
        if task_id in visiting:
            start = visiting.index(task_id)
            return visiting[start:] + [task_id]
        if task_id in visited:
            return None
        visiting.append(task_id)
        for dependency in dependencies.get(task_id, []):
            cycle = visit(dependency)
            if cycle:
                return cycle
        visiting.pop()
        visited.add(task_id)
        return None

    for task_id in dependencies:
        cycle = visit(task_id)
        if cycle:
            return cycle
    return None


def validate_deferrals(deferrals: Any, approved_ids: set[str]) -> tuple[set[str], list[str]]:
    errors: list[str] = []
    if not isinstance(deferrals, dict):
        return set(), ["deferrals: document must be a mapping"]
    if deferrals.get("scope") != "partial":
        errors.append("deferrals.scope: must be partial")
    authorization = deferrals.get("authorization")
    if not isinstance(authorization, dict):
        errors.append("deferrals.authorization: approval evidence must be a mapping")
    else:
        for field in ("artifact", "approved_by"):
            value = authorization.get(field)
            if not isinstance(value, str) or not value.strip():
                errors.append(f"deferrals.authorization.{field}: non-empty text is required")
        approval_date = authorization.get("approval_date")
        if not isinstance(approval_date, str) or not DATE_PATTERN.fullmatch(approval_date):
            errors.append(
                "deferrals.authorization.approval_date: ISO YYYY-MM-DD date is required"
            )
    entries = deferrals.get("deferred")
    if not isinstance(entries, dict) or not entries:
        errors.append("deferrals.deferred: at least one deferred ID is required")
        return set(), errors

    deferred_ids: set[str] = set()
    for item_id, entry in entries.items():
        if not isinstance(item_id, str) or not ID_PATTERN.fullmatch(item_id):
            errors.append(f"deferrals.deferred: invalid approved ID {item_id!r}")
            continue
        deferred_ids.add(item_id)
        if item_id not in approved_ids:
            errors.append(f"deferrals.deferred.{item_id}: ID is not approved")
        if not isinstance(entry, dict):
            errors.append(f"deferrals.deferred.{item_id}: entry must be a mapping")
            continue
        if entry.get("gate_type") not in {"task-scoped", "production-only"}:
            errors.append(
                f"deferrals.deferred.{item_id}.gate_type: "
                "must be task-scoped or production-only"
            )
        for field in ("reason", "reentry_condition"):
            value = entry.get(field)
            if not isinstance(value, str) or not value.strip():
                errors.append(f"deferrals.deferred.{item_id}.{field}: non-empty text is required")
    return deferred_ids, errors


def validate_plan(
    task_paths: list[Path],
    schema: dict[str, Any],
    approved_ids: set[str],
    deferrals: Any | None = None,
) -> list[str]:
    errors: list[str] = []
    tasks: dict[str, dict[str, Any]] = {}
    covered_ids: set[str] = set()

    for path in task_paths:
        try:
            task = load_task(path)
        except (OSError, yaml.YAMLError) as error:
            errors.append(f"{path}: cannot load task: {error}")
            continue
        structural = schema_errors(task, schema)
        errors.extend(f"{path}: {error}" for error in structural)
        if structural or not isinstance(task, dict):
            continue
        task_id = task["id"]
        if task_id in tasks:
            errors.append(f"{path}: duplicate task id {task_id}")
        else:
            tasks[task_id] = task
        if task["status"] != "awaiting_approval":
            errors.append(f"{path}: status must be awaiting_approval before human approval")
        if set(task["dependencies"]) != set(task["execution_gate"]["requires_merged"]):
            errors.append(f"{path}: execution merge gates must match dependencies")
        for index, allowed_path in enumerate(task["allowed_paths"]):
            if unsafe_allowed_path(allowed_path):
                errors.append(f"{path}: allowed_paths.{index} is broad or unsafe")
        covered_ids.update(task["requirement_ids"])
        for field in ("acceptance_criteria", "verification_commands", "required_evidence"):
            covered_ids.update(ID_PATTERN.findall("\n".join(task[field])))

    dependencies = {task_id: task["dependencies"] for task_id, task in tasks.items()}
    for task_id, dependency_ids in dependencies.items():
        for dependency_id in dependency_ids:
            if dependency_id == task_id:
                errors.append(f"{task_id}: task cannot depend on itself")
            elif dependency_id not in tasks:
                errors.append(f"{task_id}: unknown dependency {dependency_id}")
    cycle = find_cycle(dependencies)
    if cycle:
        errors.append(f"dependency cycle: {' -> '.join(cycle)}")

    deferred_ids: set[str] = set()
    if deferrals is not None:
        deferred_ids, deferral_errors = validate_deferrals(deferrals, approved_ids)
        errors.extend(deferral_errors)
    overlap = sorted(covered_ids & deferred_ids)
    if overlap:
        errors.append(f"approved IDs cannot be both covered and deferred: {', '.join(overlap)}")

    missing = sorted(approved_ids - covered_ids - deferred_ids)
    unexpected = sorted(covered_ids - approved_ids)
    if missing:
        errors.append(f"approved IDs without task coverage: {', '.join(missing)}")
    if unexpected:
        errors.append(f"task plan references unapproved IDs: {', '.join(unexpected)}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate task-plan YAML awaiting approval.")
    parser.add_argument("--schema", required=True, type=Path)
    parser.add_argument("--requirements", required=True, type=Path)
    parser.add_argument("--tasks", required=True, type=Path)
    parser.add_argument("--deferrals", type=Path)
    args = parser.parse_args()

    try:
        schema = json.loads(args.schema.read_text(encoding="utf-8"))
        approved_ids = set(ID_PATTERN.findall(args.requirements.read_text(encoding="utf-8")))
        deferrals = load_task(args.deferrals) if args.deferrals else None
    except (OSError, json.JSONDecodeError, yaml.YAMLError) as error:
        print(f"plan validation failed: {error}", file=sys.stderr)
        return 2
    if not approved_ids:
        print("plan validation failed: approved requirements contain no REQ/AC IDs", file=sys.stderr)
        return 2
    task_paths = sorted(args.tasks.glob("*.yaml"))
    if not task_paths:
        print("plan validation failed: task directory contains no YAML tasks", file=sys.stderr)
        return 2

    errors = validate_plan(task_paths, schema, approved_ids, deferrals)
    if errors:
        print("task plan validation failed", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    scope = "partial" if deferrals is not None else "full"
    print(
        f"Draft {scope} task plan is structurally valid: "
        f"{len(task_paths)} tasks account for {len(approved_ids)} approved IDs"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
