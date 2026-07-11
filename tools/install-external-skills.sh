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
  # Self-clearing: a bare RETURN trap would persist after this function
  # returns and reference the out-of-scope $tmp under `set -u`.
  trap 'rm -rf "$tmp"; trap - RETURN' RETURN
  echo "→ $name (subtree $subdir of $repo@$ref)"
  git clone --depth 1 --branch "$ref" --filter=blob:none --sparse "$repo" "$tmp/repo" >/dev/null 2>&1
  ( cd "$tmp/repo" && git sparse-checkout set "$subdir" >/dev/null )
  rm -rf "$dest"
  mkdir -p "$dest"
  cp -R "$tmp/repo/$subdir/." "$dest/"
}

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
