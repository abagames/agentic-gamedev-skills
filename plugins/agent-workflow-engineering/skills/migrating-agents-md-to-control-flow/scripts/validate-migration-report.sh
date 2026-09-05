#!/usr/bin/env bash
set -euo pipefail

report="${1:-migration-report.md}"
failures=0

fail() {
  printf 'FAIL: %s\n' "$1" >&2
  failures=$((failures + 1))
}

ok() {
  printf 'OK: %s\n' "$1"
}

if [[ ! -f "$report" ]]; then
  printf 'FAIL: missing report: %s\n' "$report" >&2
  exit 1
fi

required_sections=(
  '## Summary'
  '## Workflow Migration Gate Decision'
  '## Instruction Sources Found'
  '## Rule Inventory'
  '## Classification Table'
  '## Runtime Shapes and Control-Flow Candidates'
  '## Scriptable Checks and LLM-Only Judgments'
  '## Proposed Migrations'
  '## Files to Generate or Modify'
  '## Control-Flow Assets Produced'
  '## Skill Candidate Decisions'
  '## Existing Skill Relationships'
  '## Rules Intentionally Left in AGENTS.md'
  '## Rules Not Safely Automatable'
  '## Risks / Ambiguities'
  '## Verification Plan'
  '## Finalization State'
)

for section in "${required_sections[@]}"; do
  if grep -Fq -- "$section" "$report"; then
    ok "section present: $section"
  else
    fail "missing section: $section"
  fi
done

while IFS= read -r section; do
  fail "section uses enforcement language without a local enforcing mechanism or advisory label: $section"
done < <(
  awk '
    function check_section() {
      if (has_enforcement && !has_mechanism) {
        print section
      }
    }
    /^## / {
      if (section != "") {
        check_section()
      }
      section = $0
      has_enforcement = 0
      has_mechanism = 0
      next
    }
    {
      if ($0 ~ /(enforced|blocking|must)/) {
        has_enforcement = 1
      }
      if ($0 ~ /(script|hook|CI|task runner|orchestrat|advisory|prose-only|LLM-only|not safely automatable)/) {
        has_mechanism = 1
      }
    }
    END {
      if (section != "") {
        check_section()
      }
    }
  ' "$report"
)

if (( failures > 0 )); then
  printf '\n%d migration report validation check(s) failed.\n' "$failures" >&2
  exit 1
fi

printf '\nMigration report validation checks passed.\n'
