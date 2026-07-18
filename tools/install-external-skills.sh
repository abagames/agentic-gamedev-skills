#!/usr/bin/env bash
# Fetch the external skills listed in README.md "External Skill References".
# These skills are gitignored under .agents/skills/ so they can be used locally
# without being committed to this repository.
#
# Usage:
#   tools/install-external-skills.sh            # install all
#   tools/install-external-skills.sh empirical-prompt-tuning
#
# Downloads are staged and validated before an existing skill is replaced. A
# failed download or copy leaves the previously installed skill unchanged.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SKILLS_DIR="$REPO_ROOT/.agents/skills"
mkdir -p "$SKILLS_DIR"

# Refuse to operate through a symlinked skills directory: replacement must stay
# inside this checkout even when the script is run from an untrusted location.
SKILLS_DIR_REAL="$(cd "$SKILLS_DIR" && pwd -P)"
if [ "$SKILLS_DIR_REAL" != "$SKILLS_DIR" ]; then
  echo "refusing symlinked skills directory: $SKILLS_DIR" >&2
  exit 2
fi

validate_skill_name() {
  local name="$1"
  case "$name" in
    ''|*[!a-z0-9-]*)
      echo "invalid skill name: '$name'" >&2
      return 2
      ;;
  esac
}

validate_skill_payload() {
  local name="$1" payload="$2"
  local skill_file="$payload/SKILL.md"

  if [ ! -s "$skill_file" ]; then
    echo "invalid $name payload: missing or empty SKILL.md" >&2
    return 1
  fi
  if [ "$(sed -n '1p' "$skill_file")" != '---' ] \
    || ! grep -q '^name:' "$skill_file" \
    || ! grep -q '^description:' "$skill_file"; then
    echo "invalid $name payload: incomplete SKILL.md frontmatter" >&2
    return 1
  fi
}

# replace_directory <skill-name> <staged-directory> <destination>
# The old destination is retained until the staged payload has been moved into
# place. If the final move fails, restore the old destination before returning.
replace_directory() {
  local name="$1" staged="$2" dest="$3"
  local backup_root backup

  if [ ! -e "$dest" ] && [ ! -L "$dest" ]; then
    mv -T -- "$staged" "$dest"
    return
  fi

  backup_root="$(mktemp -d "$SKILLS_DIR/.backup-${name}.XXXXXX")"
  backup="$backup_root/original"
  if ! mv -T -- "$dest" "$backup"; then
    rmdir "$backup_root"
    return 1
  fi

  if mv -T -- "$staged" "$dest"; then
    rm -rf -- "$backup_root"
    return
  fi

  echo "failed to install $name; restoring previous version" >&2
  if mv -T -- "$backup" "$dest"; then
    rmdir "$backup_root"
  else
    echo "restore failed; previous version remains at $backup" >&2
  fi
  return 1
}

# install_single_file <skill-name> <raw-url>
install_single_file() (
  local name="$1" url="$2"
  local dest="$SKILLS_DIR/$name"
  local work payload

  validate_skill_name "$name"
  work="$(mktemp -d "$SKILLS_DIR/.install-${name}.XXXXXX")"
  trap 'rm -rf -- "$work"' EXIT
  payload="$work/payload"
  mkdir "$payload"

  echo "→ $name (single SKILL.md from $url)"
  curl -fsSL "$url" -o "$payload/SKILL.md"
  validate_skill_payload "$name" "$payload"
  replace_directory "$name" "$payload" "$dest"
)

# install_subtree <skill-name> <repo-url> <ref> <subdir-in-repo>
install_subtree() (
  local name="$1" repo="$2" ref="$3" subdir="$4"
  local dest="$SKILLS_DIR/$name"
  local work payload

  validate_skill_name "$name"
  work="$(mktemp -d "$SKILLS_DIR/.install-${name}.XXXXXX")"
  trap 'rm -rf -- "$work"' EXIT
  payload="$work/payload"

  echo "→ $name (subtree $subdir of $repo@$ref)"
  git clone --quiet --depth 1 --branch "$ref" --filter=blob:none --sparse \
    "$repo" "$work/repo"
  ( cd "$work/repo" && git sparse-checkout set "$subdir" )
  mkdir "$payload"
  cp -R -- "$work/repo/$subdir/." "$payload/"
  validate_skill_payload "$name" "$payload"
  replace_directory "$name" "$payload" "$dest"
)

install_empirical_prompt_tuning() {
  install_single_file "empirical-prompt-tuning" \
    "https://raw.githubusercontent.com/mizchi/skills/main/meta/empirical-prompt-tuning/SKILL.md"
}

# systematic-debugging references sibling files (root-cause-tracing.md, etc.),
# so it must be fetched as a directory, not a single SKILL.md.
install_systematic_debugging() {
  install_subtree "systematic-debugging" \
    "https://github.com/obra/superpowers.git" "main" "skills/systematic-debugging"
}

# godot-master (gd-agentic-skills): never auto-installed. Per README, pull
# individual engine-topic skills only (e.g. godot-tweening, godot-particles,
# godot-debugging-profiling); the architecture doctrine and genre skills target
# production-scale Godot 4.7+ games and conflict with this repo's minimal
# mini-game approach. To pull one skill by hand:
#   install_subtree "godot-tweening" \
#     "https://github.com/thedivergentai/gd-agentic-skills.git" "main" \
#     "skills/godot-tweening"

declare -A INSTALLERS=(
  [empirical-prompt-tuning]=install_empirical_prompt_tuning
  [systematic-debugging]=install_systematic_debugging
)

if [ "$#" -eq 0 ]; then
  targets=(empirical-prompt-tuning systematic-debugging)
else
  targets=("$@")
fi

# Validate the complete request before installing anything, so a typo in a
# multi-skill invocation cannot produce a partial successful update.
for name in "${targets[@]}"; do
  validate_skill_name "$name"
  fn="${INSTALLERS[$name]:-}"
  if [ -z "$fn" ]; then
    echo "error: '$name' is not a known external skill" >&2
    exit 2
  fi
done

for name in "${targets[@]}"; do
  fn="${INSTALLERS[$name]}"
  "$fn"
done

echo "done."
