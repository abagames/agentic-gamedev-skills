#!/usr/bin/env bash
# Diff the skill directories under .agents/skills/ against the skill names
# referenced in each README (Local Skills tables + External Skill References).
# Exits non-zero on mismatch so CI / pre-commit can catch README drift.
#
# README.md is required. README.ja.md is checked with the same rules whenever
# it exists, so the translated skill list cannot silently fall behind.
#
# A skill counts as "in README" if its directory name appears as a backtick
# token (`skill-name`) anywhere in that file. External (gitignored) skills
# are excluded from the local-side check but are still expected to appear
# in the External Skill References section.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SKILLS_DIR="$REPO_ROOT/.agents/skills"
README="$REPO_ROOT/README.md"
GITIGNORE="$REPO_ROOT/.gitignore"

[ -d "$SKILLS_DIR" ] || { echo "no $SKILLS_DIR" >&2; exit 2; }
[ -f "$README" ] || { echo "no $README" >&2; exit 2; }

readmes=("$README")
[ -f "$REPO_ROOT/README.ja.md" ] && readmes+=("$REPO_ROOT/README.ja.md")

# Skills present on disk. A directory is not a skill until it has the required
# entry point; ignore empty staging directories and abandoned support folders.
mapfile -t on_disk < <(
  find "$SKILLS_DIR" -mindepth 2 -maxdepth 2 -type f -name SKILL.md -printf '%h\n' \
    | sed 's#.*/##' | sort
)

# Skill names mentioned in a README, restricted to declaration positions:
#   - table rows:    | `skill-name` | ... or | [`skill-name`](...) | ...
#   - list entries:  - `skill-name`: ... or - [`skill-name`](...): ...
declared_in() {
  grep -oE '^[[:space:]]*[|-][[:space:]]+\[?`[a-z][a-z0-9-]+`' "$1" \
    | grep -oE '`[a-z][a-z0-9-]+`' \
    | tr -d '`' | sort -u
}

# Externally sourced (gitignored) skills. Preserve wildcard entries such as
# godot-* so an installed matching directory is excluded from the local list,
# while exact entries can also be required in README.md.
mapfile -t external_patterns < <(
  sed -nE 's#^\.agents/skills/([^/]+)/$#\1#p' "$GITIGNORE" | sort -u
)
external_exact=()
for pattern in "${external_patterns[@]}"; do
  if [[ "$pattern" != *'*'* && "$pattern" != *'?'* && "$pattern" != *'['* ]]; then
    external_exact+=("$pattern")
  fi
done

is_external() {
  local name="$1"
  local pattern
  for pattern in "${external_patterns[@]}"; do
    # The unquoted right-hand side intentionally applies .gitignore-style
    # basename globs such as godot-* to one skill directory name.
    [[ "$name" == $pattern ]] && return 0
  done
  return 1
}

contains() {
  local needle="$1"; shift
  for x in "$@"; do [ "$x" = "$needle" ] && return 0; done
  return 1
}

status=0

check_readme() {
  local file="$1"
  local label="${file##*/}"
  local name
  local -a in_readme missing_from_readme missing_from_disk
  local -a missing_external_from_readme

  mapfile -t in_readme < <(declared_in "$file")
  missing_from_readme=()
  missing_from_disk=()
  missing_external_from_readme=()

  for name in "${on_disk[@]}"; do
    if ! contains "$name" "${in_readme[@]}" && ! is_external "$name"; then
      missing_from_readme+=("$name")
    fi
  done

  # Exact external entries are part of the documented skill catalog even when
  # they are absent from a clean checkout. Wildcard entries describe optional
  # families and therefore do not require a literal README declaration.
  for name in "${external_exact[@]}"; do
    if ! contains "$name" "${in_readme[@]}"; then
      missing_external_from_readme+=("$name")
    fi
  done

  # Only warn about README → disk for non-external skills, since external skills
  # are intentionally absent from disk in clean checkouts.
  for name in "${in_readme[@]}"; do
    # Skip names that are obviously not skills (single-word commons grep picks
    # up): supporting directories and frontmatter field names.
    case "$name" in
      references|assets|scripts|tools|agents|skills|godot-base) continue ;;
      name|description|*\ *) continue ;;
    esac
    if ! contains "$name" "${on_disk[@]}"; then
      if ! is_external "$name"; then
        missing_from_disk+=("$name")
      fi
    fi
  done

  if [ "${#missing_from_readme[@]}" -gt 0 ]; then
    echo "skills present on disk but not mentioned in $label:" >&2
    printf '  - %s\n' "${missing_from_readme[@]}" >&2
    status=1
  fi
  if [ "${#missing_from_disk[@]}" -gt 0 ]; then
    echo "skills mentioned in $label but not on disk (and not gitignored):" >&2
    printf '  - %s\n' "${missing_from_disk[@]}" >&2
    status=1
  fi
  if [ "${#missing_external_from_readme[@]}" -gt 0 ]; then
    echo "external skills in .gitignore but not mentioned in $label:" >&2
    printf '  - %s\n' "${missing_external_from_readme[@]}" >&2
    status=1
  fi
}

for readme in "${readmes[@]}"; do
  check_readme "$readme"
done

if [ "$status" -eq 0 ]; then
  labels=()
  for readme in "${readmes[@]}"; do labels+=("${readme##*/}"); done
  echo "${labels[*]} ↔ .agents/skills/ in sync (${#on_disk[@]} skills)."
fi
exit "$status"
