#!/usr/bin/env bash
# Fetch the external skills listed in README.md "External Skill References".
# These skills are gitignored under .agents/skills/ so they can be used locally
# without being committed to this repository.
#
# Usage:
#   tools/install-external-skills.sh            # install all
#   tools/install-external-skills.sh empirical-prompt-tuning
#
# Re-running on an existing skill directory updates it in place via `git pull`
# when the directory is a git checkout, otherwise re-fetches the SKILL.md only.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SKILLS_DIR="$REPO_ROOT/.agents/skills"
mkdir -p "$SKILLS_DIR"

# install_single_file <skill-name> <raw-url>
install_single_file() {
  local name="$1" url="$2"
  local dest="$SKILLS_DIR/$name"
  mkdir -p "$dest"
  echo "→ $name (single SKILL.md from $url)"
  curl -fsSL "$url" -o "$dest/SKILL.md"
}

# install_subtree <skill-name> <repo-url> <ref> <subdir-in-repo>
install_subtree() {
  local name="$1" repo="$2" ref="$3" subdir="$4"
  local dest="$SKILLS_DIR/$name"
  local tmp
  tmp="$(mktemp -d)"
  trap 'rm -rf "$tmp"' RETURN
  echo "→ $name (subtree $subdir of $repo@$ref)"
  git clone --depth 1 --branch "$ref" --filter=blob:none --sparse "$repo" "$tmp/repo" >/dev/null 2>&1
  ( cd "$tmp/repo" && git sparse-checkout set "$subdir" >/dev/null )
  rm -rf "$dest"
  mkdir -p "$dest"
  cp -R "$tmp/repo/$subdir/." "$dest/"
}

install_empirical_prompt_tuning() {
  install_single_file "empirical-prompt-tuning" \
    "https://raw.githubusercontent.com/mizchi/skills/main/empirical-prompt-tuning/SKILL.md"
}

install_systematic_debugging() {
  install_single_file "systematic-debugging" \
    "https://raw.githubusercontent.com/mxyhi/ok-skills/main/systematic-debugging/SKILL.md"
}

# godot-master: README states "Use selectively; do not install the full skill
# set by default." This script intentionally does not auto-install it. To pull a
# specific subtree by hand:
#   install_subtree "godot-master" \
#     "https://github.com/thedivergentai/gd-agentic-skills.git" "main" "<subdir>"

declare -A INSTALLERS=(
  [empirical-prompt-tuning]=install_empirical_prompt_tuning
  [systematic-debugging]=install_systematic_debugging
)

if [ "$#" -eq 0 ]; then
  targets=("${!INSTALLERS[@]}")
else
  targets=("$@")
fi

for name in "${targets[@]}"; do
  fn="${INSTALLERS[$name]:-}"
  if [ -z "$fn" ]; then
    echo "skip: '$name' is not a known external skill" >&2
    continue
  fi
  "$fn"
done

echo "done."
