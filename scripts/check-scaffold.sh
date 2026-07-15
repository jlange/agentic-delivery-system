#!/usr/bin/env bash
set -euo pipefail

required=(
  "AGENTS.md"
  "README.md"
  ".gitignore"
  ".codex/config.toml"
  ".codex/agents/requirements_analyst.toml"
  ".codex/agents/solution_architect.toml"
  ".codex/agents/task_planner.toml"
  ".codex/agents/backend_engineer.toml"
  ".codex/agents/frontend_engineer.toml"
  ".codex/agents/database_engineer.toml"
  ".codex/agents/design_reviewer.toml"
  ".codex/agents/qa_engineer.toml"
  ".codex/agents/security_reviewer.toml"
  ".codex/agents/devops_engineer.toml"
  ".codex/agents/code_reviewer.toml"
  "schemas/task.schema.json"
  "templates/tasks/task.yaml"
  "docs/operating-model.md"
  "docs/manual-todo.md"
)

for path in "${required[@]}"; do
  [[ -e "$path" ]] || { echo "missing $path" >&2; exit 1; }
done

grep -q '^max_threads = 4$' .codex/config.toml
grep -q '^max_depth = 1$' .codex/config.toml

echo "Scaffold check passed."
