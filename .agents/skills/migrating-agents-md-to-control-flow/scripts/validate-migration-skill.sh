#!/usr/bin/env bash
set -euo pipefail

skill_dir="${1:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
skill_md="$skill_dir/SKILL.md"
openai_yaml="$skill_dir/agents/openai.yaml"
failure_modes="$skill_dir/references/failure-modes.md"
self_validator="$skill_dir/scripts/validate-migration-skill.sh"
report_validator="$skill_dir/scripts/validate-migration-report.sh"

failures=0

fail() {
  printf 'FAIL: %s\n' "$1" >&2
  failures=$((failures + 1))
}

ok() {
  printf 'OK: %s\n' "$1"
}

require_file() {
  if [[ -f "$1" ]]; then
    ok "file exists: ${1#$skill_dir/}"
  else
    fail "missing file: ${1#$skill_dir/}"
  fi
}

require_literal() {
  local file="$1"
  local text="$2"
  local label="$3"

  if [[ ! -f "$file" ]]; then
    fail "cannot check missing file for $label: ${file#$skill_dir/}"
    return
  fi

  if grep -Fq -- "$text" "$file"; then
    ok "$label"
  else
    fail "$label missing literal: $text"
  fi
}

require_regex() {
  local file="$1"
  local regex="$2"
  local label="$3"

  if [[ ! -f "$file" ]]; then
    fail "cannot check missing file for $label: ${file#$skill_dir/}"
    return
  fi

  if grep -Eq -- "$regex" "$file"; then
    ok "$label"
  else
    fail "$label missing pattern: $regex"
  fi
}

require_file "$skill_md"
require_file "$openai_yaml"
require_file "$failure_modes"
require_file "$self_validator"
require_file "$report_validator"

folder_name="$(basename "$skill_dir")"
frontmatter_name="$(sed -n 's/^name: //p' "$skill_md" | head -n 1)"
if [[ "$frontmatter_name" == "$folder_name" ]]; then
  ok "frontmatter name matches folder"
else
  fail "frontmatter name '$frontmatter_name' does not match folder '$folder_name'"
fi

require_regex "$skill_md" '^description: .+' 'frontmatter description is present'
require_literal "$openai_yaml" "Use \$$folder_name" 'default prompt names this skill'

required_sections=(
  '## Applicability Gate'
  '## Core Heuristics'
  '## Classification'
  '### E. Deterministic Orchestration'
  '## Procedure'
  '## Skill Candidate Test'
  '## Output Requirements'
  '## Safety Boundaries'
  '## Final Checklist'
)

for section in "${required_sections[@]}"; do
  require_literal "$skill_md" "$section" "required section: $section"
done

required_report_sections=(
  'Workflow Migration Gate Decision'
  'Runtime Shapes and Control-Flow Candidates'
  'Scriptable Checks and LLM-Only Judgments'
  'Control-Flow Assets Produced'
  'Finalization State'
)

for section in "${required_report_sections[@]}"; do
  require_literal "$skill_md" "$section" "migration report section: $section"
done

failure_mode_sections=(
  '## Missing Control Flow'
  '## Scriptable Check Left to the LLM'
  '## Fake State Machine'
  '## False Enforcement'
)

for section in "${failure_mode_sections[@]}"; do
  require_literal "$failure_modes" "$section" "failure mode: $section"
done

require_literal "$skill_md" 'references/failure-modes.md' 'failure modes reference is discoverable'
require_literal "$skill_md" 'scripts/validate-migration-skill.sh' 'self-validation script is referenced'
require_literal "$skill_md" 'scripts/validate-migration-report.sh' 'migration report validator is referenced'

quick_validate="${QUICK_VALIDATE:-/home/cs8k/.codex/skills/.system/skill-creator/scripts/quick_validate.py}"
if [[ -f "$quick_validate" ]]; then
  python3 "$quick_validate" "$skill_dir" >/tmp/migrating-flow-skill-quick-validate.log 2>&1 \
    && ok 'quick_validate.py passes' \
    || fail "quick_validate.py failed; see /tmp/migrating-flow-skill-quick-validate.log"
else
  printf 'WARN: quick_validate.py not found at %s\n' "$quick_validate" >&2
fi

if (( failures > 0 )); then
  printf '\n%d validation check(s) failed.\n' "$failures" >&2
  exit 1
fi

printf '\nAll migration skill validation checks passed.\n'
