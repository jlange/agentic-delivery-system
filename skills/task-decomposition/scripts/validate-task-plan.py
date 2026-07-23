#!/usr/bin/env python3
"""Validate a draft task set before human approval."""

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


def validate_plan(task_paths: list[Path], schema: dict[str, Any], approved_ids: set[str]) -> list[str]:
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
        if task["status"] != "draft":
            errors.append(f"{path}: status must be draft before human approval")
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

    missing = sorted(approved_ids - covered_ids)
    unexpected = sorted(covered_ids - approved_ids)
    if missing:
        errors.append(f"approved IDs without task coverage: {', '.join(missing)}")
    if unexpected:
        errors.append(f"task plan references unapproved IDs: {', '.join(unexpected)}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate draft task-plan YAML files.")
    parser.add_argument("--schema", required=True, type=Path)
    parser.add_argument("--requirements", required=True, type=Path)
    parser.add_argument("--tasks", required=True, type=Path)
    args = parser.parse_args()

    try:
        schema = json.loads(args.schema.read_text(encoding="utf-8"))
        approved_ids = set(ID_PATTERN.findall(args.requirements.read_text(encoding="utf-8")))
    except (OSError, json.JSONDecodeError) as error:
        print(f"plan validation failed: {error}", file=sys.stderr)
        return 2
    if not approved_ids:
        print("plan validation failed: approved requirements contain no REQ/AC IDs", file=sys.stderr)
        return 2
    task_paths = sorted(args.tasks.glob("*.yaml"))
    if not task_paths:
        print("plan validation failed: task directory contains no YAML tasks", file=sys.stderr)
        return 2

    errors = validate_plan(task_paths, schema, approved_ids)
    if errors:
        print("task plan validation failed", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"Draft task plan is structurally valid: {len(task_paths)} tasks cover {len(approved_ids)} approved IDs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
