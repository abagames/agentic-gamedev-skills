#!/usr/bin/env bash
# Diff the skill directories under .agents/skills/ against the skill names
# referenced in README.md (Local Skills tables + External Skill References).
# Exits non-zero on mismatch so CI / pre-commit can catch README drift.
#
# A skill counts as "in README" if its directory name appears as a backtick
# token (`skill-name`) anywhere in README.md. External (gitignored) skills
# are excluded from the local-side check but are still expected to appear
# in the External Skill References section.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SKILLS_DIR="$REPO_ROOT/.agents/skills"
README="$REPO_ROOT/README.md"
GITIGNORE="$REPO_ROOT/.gitignore"

[ -d "$SKILLS_DIR" ] || { echo "no $SKILLS_DIR" >&2; exit 2; }
[ -f "$README" ] || { echo "no $README" >&2; exit 2; }

# Skill directories present on disk
mapfile -t on_disk < <(find "$SKILLS_DIR" -mindepth 1 -maxdepth 1 -type d -printf '%f\n' | sort)

# Skill names mentioned in README, restricted to declaration positions:
#   - table rows:    | `skill-name` | ...
#   - list entries:  - `skill-name`: ...
mapfile -t in_readme < <(
  grep -oE '^[[:space:]]*[|-][[:space:]]+`[a-z][a-z0-9-]+`' "$README" \
    | grep -oE '`[a-z][a-z0-9-]+`' \
    | tr -d '`' | sort -u
)

# Externally sourced (gitignored) skills
mapfile -t external < <(grep -oE '\.agents/skills/[a-z0-9-]+/?' "$GITIGNORE" 2>/dev/null \
  | sed -E 's#\.agents/skills/##; s#/$##' | sort -u || true)

is_external() {
  local name="$1"
  for e in "${external[@]:-}"; do [ "$e" = "$name" ] && return 0; done
  return 1
}

contains() {
  local needle="$1"; shift
  for x in "$@"; do [ "$x" = "$needle" ] && return 0; done
  return 1
}

missing_from_readme=()
missing_from_disk=()

for name in "${on_disk[@]}"; do
  if ! contains "$name" "${in_readme[@]}"; then
    missing_from_readme+=("$name")
  fi
done

# Only warn about README → disk for non-external skills, since external skills
# are intentionally absent from disk in clean checkouts.
for name in "${in_readme[@]}"; do
  # Skip names that are obviously not skills (single-word commons grep picks up).
  case "$name" in
    references|assets|scripts|tools|agents|skills|godot-base|*\ *) continue ;;
  esac
  if ! contains "$name" "${on_disk[@]}"; then
    if ! is_external "$name"; then
      missing_from_disk+=("$name")
    fi
  fi
done

status=0
if [ "${#missing_from_readme[@]}" -gt 0 ]; then
  echo "skills present on disk but not mentioned in README.md:" >&2
  printf '  - %s\n' "${missing_from_readme[@]}" >&2
  status=1
fi
if [ "${#missing_from_disk[@]}" -gt 0 ]; then
  echo "skills mentioned in README.md but not on disk (and not gitignored):" >&2
  printf '  - %s\n' "${missing_from_disk[@]}" >&2
  status=1
fi

if [ "$status" -eq 0 ]; then
  echo "README ↔ .agents/skills/ in sync (${#on_disk[@]} skill directories)."
fi
exit "$status"
