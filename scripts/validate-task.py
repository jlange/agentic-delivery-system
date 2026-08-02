#!/usr/bin/env python3
"""Validate an approved delivery task before agent execution."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path, PurePosixPath
from typing import Any

import jsonschema
import yaml


REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SCHEMA = REPOSITORY_ROOT / "schemas" / "task.schema.json"
FORBIDDEN_ALLOWED_PATHS = {
    "/",
    "/home",
    "/mnt",
    "/mnt/c",
    "/mnt/d",
    "/mnt/e",
    "~",
    "~/",
    "clients",
    "clients/**",
}


def load_yaml(path: Path) -> Any:
    with path.open(encoding="utf-8") as task_file:
        return yaml.safe_load(task_file)


def load_schema(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as schema_file:
        return json.load(schema_file)


def format_schema_error(error: jsonschema.ValidationError) -> str:
    location = ".".join(str(part) for part in error.absolute_path) or "<root>"
    return f"{location}: {error.message}"


def unsafe_allowed_path(path: str) -> bool:
    normalized = path.strip().replace("\\", "/")
    if normalized in FORBIDDEN_ALLOWED_PATHS:
        return True
    if normalized.startswith(("~/", "/home/", "/mnt/", "../", "/")):
        return True
    parts = PurePosixPath(normalized).parts
    return bool(parts and parts[0] == "clients")


def validate_task(task: Any, schema: dict[str, Any]) -> list[str]:
    validator = jsonschema.Draft202012Validator(schema)
    errors = [
        format_schema_error(error)
        for error in sorted(validator.iter_errors(task), key=lambda item: list(item.absolute_path))
    ]
    if errors or not isinstance(task, dict):
        return errors

    executable_states = {"approved", "executable", "implementing", "amendment_approved"}
    if task["status"] not in executable_states:
        errors.append("status: task is not in an executable approved state")

    approval = task.get("approval", {})
    if approval.get("status") != "approved":
        errors.append("approval.status: durable human approval is required")

    dependency_set = set(task.get("dependencies", []))
    merge_gate_set = set(task.get("execution_gate", {}).get("requires_merged", []))
    if dependency_set != merge_gate_set:
        errors.append("execution_gate.requires_merged: must match dependencies")

    for amendment_index, amendment in enumerate(task.get("amendments", [])):
        if amendment.get("status") == "approved" and not amendment.get("approval_artifact"):
            errors.append(
                f"amendments.{amendment_index}.approval_artifact: required for an approved amendment"
            )

    for index, path in enumerate(task["allowed_paths"]):
        if unsafe_allowed_path(path):
            errors.append(
                f"allowed_paths.{index}: broad, client, home, absolute, or mounted-drive access is forbidden"
            )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate an approved task YAML file before agent execution."
    )
    parser.add_argument("task", type=Path, help="path to the task YAML file")
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
    args = parser.parse_args()

    try:
        task = load_yaml(args.task)
        schema = load_schema(args.schema)
    except (OSError, json.JSONDecodeError, yaml.YAMLError) as error:
        print(f"validation failed: {error}", file=sys.stderr)
        return 2

    errors = validate_task(task, schema)
    if errors:
        print(f"{args.task}: task validation failed", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"{args.task}: approved task is valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
