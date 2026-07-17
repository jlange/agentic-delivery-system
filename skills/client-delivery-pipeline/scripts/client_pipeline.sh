#!/usr/bin/env bash
set -euo pipefail

WORK_ROOT="${WORK_ROOT:-$HOME/work}"
SYSTEM_ROOT="${SYSTEM_ROOT:-$WORK_ROOT/agentic-delivery-system}"
CLIENTS_ROOT="${CLIENTS_ROOT:-$WORK_ROOT/clients}"

usage() {
  cat <<'EOF'
Usage:
  client_pipeline.sh init-intake <client>
  client_pipeline.sh copy-source [--agent-safe] <client> <file> [file...]
  client_pipeline.sh write-intake-prompt <client>
  client_pipeline.sh write-review-checklist <client>
  client_pipeline.sh init-demo-repo <client> <repo-name>
  client_pipeline.sh write-demo-task <client> <repo-name>
  client_pipeline.sh write-demo-agent-prompts <client> <repo-name>

Environment overrides:
  WORK_ROOT=/home/restingrobot/work
  SYSTEM_ROOT=/home/restingrobot/work/agentic-delivery-system
  CLIENTS_ROOT=/home/restingrobot/work/clients
EOF
}

die() {
  echo "error: $*" >&2
  exit 1
}

require_lowercase_name() {
  local value="$1"
  [[ "$value" =~ ^[a-z0-9][a-z0-9-]*$ ]] || die "name must be lowercase kebab style: $value"
}

intake_dir() {
  local client="$1"
  echo "$CLIENTS_ROOT/$client/intake"
}

demo_repo_dir() {
  local client="$1"
  local repo="$2"
  echo "$CLIENTS_ROOT/$client/$repo"
}

cmd_init_intake() {
  local client="${1:-}"
  [[ -n "$client" ]] || die "missing client"
  require_lowercase_name "$client"

  local root
  root="$(intake_dir "$client")"
  mkdir -p "$root/source" "$root/notes" "$root/redacted" "$root/outputs" "$root/decisions"

  echo "Created intake folders:"
  find "$root" -maxdepth 1 -type d | sort
}

cmd_copy_source() {
  local agent_safe=0
  if [[ "${1:-}" == "--agent-safe" ]]; then
    agent_safe=1
    shift
  fi

  local client="${1:-}"
  [[ -n "$client" ]] || die "missing client"
  require_lowercase_name "$client"
  shift || true

  [[ "$#" -gt 0 ]] || die "provide at least one file"

  local root
  root="$(intake_dir "$client")"
  [[ -d "$root/source" ]] || die "intake source folder does not exist; run init-intake first"

  local file
  for file in "$@"; do
    [[ -f "$file" ]] || die "not a file: $file"
    cp "$file" "$root/source/"
    echo "copied to source: $file"

    if [[ "$agent_safe" -eq 1 ]]; then
      cp "$file" "$root/redacted/"
      echo "copied to redacted: $file"
    fi
  done
}

cmd_write_intake_prompt() {
  local client="${1:-}"
  [[ -n "$client" ]] || die "missing client"
  require_lowercase_name "$client"

  local root
  root="$(intake_dir "$client")"
  [[ -d "$root/notes" ]] || die "intake notes folder does not exist; run init-intake first"

  cat > "$root/notes/contract_intake_prompt.md" <<EOF
# Contract Intake Request

Use the \`contract-intake\` skill from:

\`$SYSTEM_ROOT/skills/contract-intake/SKILL.md\`

Analyze only the approved intake files in:

\`$root/redacted\`

Allowed paths:

- \`$root/redacted\`
- \`$root/outputs\`

Forbidden paths:

- \`/mnt/c\`
- \`/mnt/d\`
- \`/mnt/e\`
- \`$HOME\`
- \`$HOME/.ssh\`
- \`$HOME/.config\`
- \`$HOME/.codex\`
- \`$HOME/.claude\`
- unrelated client folders

Task:

Create a structured contract intake output at:

\`$root/outputs/contract_intake_output.md\`

The output must include:

- source material reviewed
- project summary
- explicit requirements
- inferred requirements
- assumptions
- open questions
- risks
- draft acceptance criteria
- out-of-scope items
- client decisions required
- human review required

Important rules:

- Do not treat brainstormed ideas as approved scope.
- Do not invent requirements.
- Do not proceed to architecture or implementation.
- Do not include secrets or unnecessary sensitive data.
- Keep transcript quotes short and only when needed.
EOF

  echo "Wrote $root/notes/contract_intake_prompt.md"
}

cmd_write_review_checklist() {
  local client="${1:-}"
  [[ -n "$client" ]] || die "missing client"
  require_lowercase_name "$client"

  local root
  root="$(intake_dir "$client")"
  [[ -d "$root/decisions" ]] || die "intake decisions folder does not exist; run init-intake first"

  cat > "$root/decisions/intake_review_checklist.md" <<EOF
# ${client} Intake Review Checklist

Review source:

- \`../outputs/contract_intake_output.md\`

## Scope decision

- [ ] Initial scope is spreadsheet aggregation only.
- [ ] Meeting-minutes automation is included in initial scope.
- [ ] Meeting-minutes automation is deferred.
- [ ] Broader audits/forms/source-document automation is deferred.
- [ ] Other:

## Data access decision

- [ ] Development will use synthetic sample workbooks.
- [ ] Development will use redacted sample workbooks.
- [ ] Development will use approved real workbooks.
- [ ] No real facility data will be shared before agreement terms are approved.
- [ ] Other:

## Output decision

- [ ] Tool updates the existing master dashboard directly.
- [ ] Tool creates a review copy of the master dashboard.
- [ ] Tool creates a separate generated output workbook.
- [ ] Decision pending.

## Environment decision

- [ ] Tool will run manually.
- [ ] Tool will run on a facility work laptop.
- [ ] Tool will run on a facility-accessible network drive.
- [ ] IT/security approval is required before execution.
- [ ] Decision pending.

## Contract and approval

- [ ] Supervisor approval is required.
- [ ] NDA or confidentiality terms are required.
- [ ] Written proposal is required.
- [ ] Budget approval is required.
- [ ] Data-sharing terms are required.

## Open questions to resolve

- [ ] Which specific spreadsheets are in phase one?
- [ ] Which dashboard fields are in phase one?
- [ ] Are quarterly averages required?
- [ ] Are red/green indicators required?
- [ ] Who runs the tool?
- [ ] What validation process is required?
- [ ] What policies apply to scripts, AI tools, and external processing?

## Human notes

Add review notes here.
EOF

  echo "Wrote $root/decisions/intake_review_checklist.md"
}

cmd_init_demo_repo() {
  local client="${1:-}"
  local repo="${2:-}"
  [[ -n "$client" && -n "$repo" ]] || die "usage: init-demo-repo <client> <repo-name>"
  require_lowercase_name "$client"
  require_lowercase_name "$repo"

  local root
  root="$(demo_repo_dir "$client" "$repo")"
  mkdir -p "$root"
  cd "$root"

  if [[ ! -d .git ]]; then
    git init
    git branch -m main
  fi

  mkdir -p docs demo/source demo/master demo/output demo/mapping scripts tests tasks
  touch demo/output/.gitkeep

  if [[ -f "$(intake_dir "$client")/outputs/demo_plan.md" && ! -f docs/demo_plan.md ]]; then
    cp "$(intake_dir "$client")/outputs/demo_plan.md" docs/demo_plan.md
  fi

  if [[ ! -f .gitignore ]]; then
    cat > .gitignore <<'EOF'
# Python
__pycache__/
*.py[cod]
.venv/
venv/
.pytest_cache/

# Logs and temp files
*.log
tmp/
temp/

# Local/generated demo outputs
demo/output/*
!demo/output/.gitkeep

# Excel temporary files
~$*.xlsx
~$*.xlsm
~$*.xls

# OS/editor files
.DS_Store
Thumbs.db
.vscode/
.idea/
EOF
  fi

  if [[ ! -f README.md ]]; then
    cat > README.md <<EOF
# ${repo}

Synthetic spreadsheet aggregation demo.

## Goals

- Use synthetic data only.
- Create at least 15 source Excel files.
- Organize source files by metric folders.
- Use year-based sheet tabs and monthly values.
- Update selected fields in a master workbook.
- Ignore unmapped values.
- Produce an updated master workbook for review.

## Non-goals

- No real facility data.
- No network-drive execution.
- No automatic scheduling.
- No charts or visual dashboards.
- No production deployment.
EOF
  fi

  echo "Initialized demo repository at $root"
}

cmd_write_demo_task() {
  local client="${1:-}"
  local repo="${2:-}"
  [[ -n "$client" && -n "$repo" ]] || die "usage: write-demo-task <client> <repo-name>"
  require_lowercase_name "$client"
  require_lowercase_name "$repo"

  local root
  root="$(demo_repo_dir "$client" "$repo")"
  [[ -d "$root/.git" ]] || die "demo repo not found; run init-demo-repo first"
  mkdir -p "$root/tasks"

  cat > "$root/tasks/DEMO-001-generate-synthetic-workbooks.md" <<'EOF'
# DEMO-001: Generate synthetic demo workbooks

## Goal

Create the synthetic Excel workbook dataset for the spreadsheet aggregation demo.

## Background

The demo should prove that a manually run tool can read selected monthly values from multiple source workbooks, use explicit mapping rules, and update a master quality dashboard workbook.

No real facility data may be used.

## Allowed paths

- `demo/source/**`
- `demo/master/**`
- `demo/mapping/**`
- `scripts/**`
- `tests/**`
- `README.md`
- `docs/**`

## Forbidden paths

- `/mnt/c`
- `/mnt/d`
- `/mnt/e`
- files outside this repository
- real client or facility data

## Requirements

- Create at least 15 synthetic source Excel files.
- Organize source files into multiple metric folders.
- Use metric groups such as falls, infections, wounds, staffing, and audits.
- Each source workbook should include year-based sheet tabs.
- Each year sheet should include monthly values.
- Include at least one mapped metric per workbook.
- Include at least one extra unmapped value per workbook.
- Create one synthetic master dashboard workbook.
- Create one explicit mapping file.
- Use synthetic data only.

## Expected files

- `demo/source/**.xlsx`
- `demo/master/master_quality_dashboard.xlsx`
- `demo/mapping/metric_mapping.csv`
- `scripts/generate_demo_workbooks.py`

## Acceptance criteria

- At least 15 source workbooks exist.
- Source workbooks are spread across multiple metric folders.
- Workbooks can be opened by Excel.
- Master workbook can be opened by Excel.
- Mapping file clearly identifies source-to-target relationships.
- Script can regenerate the synthetic workbooks.
- No real facility data is present.

## Verification commands

- `python3 scripts/generate_demo_workbooks.py`
- `find demo/source -name "*.xlsx" | wc -l`
- `ls -lh demo/master/master_quality_dashboard.xlsx`
- `head -n 10 demo/mapping/metric_mapping.csv`
EOF

  echo "Wrote $root/tasks/DEMO-001-generate-synthetic-workbooks.md"
}

cmd_write_demo_agent_prompts() {
  local client="${1:-}"
  local repo="${2:-}"
  [[ -n "$client" && -n "$repo" ]] || die "usage: write-demo-agent-prompts <client> <repo-name>"
  require_lowercase_name "$client"
  require_lowercase_name "$repo"

  local root
  root="$(demo_repo_dir "$client" "$repo")"
  [[ -d "$root/.git" ]] || die "demo repo not found; run init-demo-repo first"
  mkdir -p "$root/prompts-local"

  cat > "$root/prompts-local/DEMO-001-codex-prompt.md" <<'EOF'
# DEMO-001 Implementation Request

Read and implement:

- `tasks/DEMO-001-generate-synthetic-workbooks.md`

Allowed paths:

- `demo/source/**`
- `demo/master/**`
- `demo/mapping/**`
- `scripts/**`
- `tests/**`
- `README.md`
- `docs/**`

Forbidden paths:

- `/mnt/c`
- `/mnt/d`
- `/mnt/e`
- files outside this repository
- real client or facility data

Requirements:

- Create synthetic data only.
- Generate at least 15 source Excel workbooks.
- Organize source workbooks across metric folders.
- Use year-based sheet tabs.
- Include monthly values.
- Include mapped and unmapped values.
- Create a master dashboard workbook.
- Create an explicit mapping CSV.
- Create a script that can regenerate the workbooks.
- Add lightweight verification if practical.
- Run the verification commands from the task file.

Stop conditions:

- Stop if a dependency must be installed manually.
- Stop if any real client or facility data would be needed.
- Stop after repeated test or generation failures.

Completion report:

- Files changed.
- Commands run.
- Verification results.
- Any risks or follow-up work.
EOF

  cat > "$root/prompts-local/DEMO-001-claude-review.md" <<'EOF'
# Claude Code Review Request

Review the DEMO-001 implementation branch for this repository.

Task file:

- `tasks/DEMO-001-generate-synthetic-workbooks.md`

You are reviewing only. Do not edit files, push, merge, deploy, or access files outside this repository.

Allowed paths:

- `demo/source/**`
- `demo/master/**`
- `demo/mapping/**`
- `scripts/**`
- `tests/**`
- `tasks/**`
- `docs/**`
- `README.md`
- `.gitignore`

Forbidden paths:

- `/mnt/c`
- `/mnt/d`
- `/mnt/e`
- files outside this repository
- real client or facility data

Please review:

- whether the implementation satisfies DEMO-001
- bugs in `scripts/generate_demo_workbooks.py`
- whether generated synthetic Excel files match the demo requirements
- whether `metric_mapping.csv` is clear and usable
- whether tests are meaningful and runnable
- whether any real facility data appears present
- whether generated artifacts are appropriate to commit

Output:

- Blocking findings
- Non-blocking findings
- Missing tests or verification gaps
- Security/privacy concerns
- Recommendation: approve, approve with notes, or request changes
EOF

  if ! grep -q '^prompts-local/$' "$root/.git/info/exclude" 2>/dev/null; then
    printf '\nprompts-local/\n' >> "$root/.git/info/exclude"
  fi

  echo "Wrote local prompts under $root/prompts-local"
  echo "Added prompts-local/ to local git exclude"
}

main() {
  local command="${1:-}"
  [[ -n "$command" ]] || { usage; exit 1; }
  shift || true

  case "$command" in
    init-intake) cmd_init_intake "$@" ;;
    copy-source) cmd_copy_source "$@" ;;
    write-intake-prompt) cmd_write_intake_prompt "$@" ;;
    write-review-checklist) cmd_write_review_checklist "$@" ;;
    init-demo-repo) cmd_init_demo_repo "$@" ;;
    write-demo-task) cmd_write_demo_task "$@" ;;
    write-demo-agent-prompts) cmd_write_demo_agent_prompts "$@" ;;
    -h|--help|help) usage ;;
    *) usage; die "unknown command: $command" ;;
  esac
}

main "$@"
