#!/usr/bin/env bash

set -uo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd -P)"
TEST_ROOT="$(mktemp -d "${TMPDIR:-/tmp}/repository-tools-test.XXXXXX")"
FAILURES=0

cleanup() {
  rm -rf -- "$TEST_ROOT"
}
trap cleanup EXIT

pass() {
  printf 'ok - %s\n' "$1"
}

fail() {
  printf 'not ok - %s\n' "$1" >&2
  FAILURES=$((FAILURES + 1))
}

run_test() {
  local name="$1"
  shift
  if "$@"; then
    pass "$name"
  else
    fail "$name"
  fi
}

make_installer_fixture() {
  local root="$1"
  mkdir -p "$root/tools" "$root/.agents/skills" "$root/tmp"
  cp "$REPO_ROOT/tools/install-external-skills.sh" "$root/tools/"
}

make_mock_curl() {
  local bin_dir="$1"
  mkdir -p "$bin_dir"
  cat >"$bin_dir/curl" <<'MOCK'
#!/usr/bin/env bash
set -u
output=""
while [ "$#" -gt 0 ]; do
  case "$1" in
    -o|--output)
      output="$2"
      shift 2
      ;;
    *)
      shift
      ;;
  esac
done
[ -n "$output" ] || exit 64
mkdir -p "$(dirname "$output")"
case "${MOCK_CURL_MODE:-success}" in
  fail)
    printf '%s\n' partial-download >"$output"
    exit 23
    ;;
  invalid)
    printf '%s\n' '---' 'name: invalid' '---' >"$output"
    exit 0
    ;;
esac
cat >"$output" <<'SKILL'
---
name: downloaded
description: Downloaded fixture.
---
SKILL
MOCK
  chmod +x "$bin_dir/curl"
}

make_mock_git() {
  local bin_dir="$1"
  mkdir -p "$bin_dir"
  cat >"$bin_dir/git" <<'MOCK'
#!/usr/bin/env bash
set -u
case "${1:-}" in
  clone)
    destination="${!#}"
    mkdir -p "$destination/skills/systematic-debugging"
    cat >"$destination/skills/systematic-debugging/SKILL.md" <<'SKILL'
---
name: systematic-debugging
description: Downloaded fixture.
---
SKILL
    ;;
  sparse-checkout)
    ;;
  *)
    exit 64
    ;;
esac
MOCK
  chmod +x "$bin_dir/git"
}

make_failing_cp() {
  local bin_dir="$1"
  cat >"$bin_dir/cp" <<'MOCK'
#!/usr/bin/env bash
exit 74
MOCK
  chmod +x "$bin_dir/cp"
}

make_failing_final_mv() {
  local bin_dir="$1"
  cat >"$bin_dir/mv" <<'MOCK'
#!/usr/bin/env bash
set -u
source_path="${@: -2:1}"
dest_path="${@: -1}"
if [[ "$source_path" == */.install-*/payload ]] \
  && [ "$dest_path" = "${MOCK_MV_FAIL_DEST:-}" ]; then
  exit 75
fi
exec /usr/bin/mv "$@"
MOCK
  chmod +x "$bin_dir/mv"
}

write_original_skill() {
  local dest="$1"
  mkdir -p "$dest"
  cat >"$dest/SKILL.md" <<'SKILL'
---
name: original
description: Original fixture that must survive a failed update.
---
SKILL
}

no_installer_artifacts() {
  local skills_dir="$1"
  [ -z "$(find "$skills_dir" -mindepth 1 -maxdepth 1 \
    \( -name '.install-*' -o -name '.backup-*' \) -print -quit)" ]
}

test_single_file_failure_preserves_existing() {
  local root="$TEST_ROOT/single-failure"
  local mock_bin="$root/mock-bin"
  make_installer_fixture "$root"
  make_mock_curl "$mock_bin"
  write_original_skill "$root/.agents/skills/empirical-prompt-tuning"

  PATH="$mock_bin:$PATH" TMPDIR="$root/tmp" MOCK_CURL_MODE=fail \
    "$root/tools/install-external-skills.sh" empirical-prompt-tuning \
    >"$root/output.log" 2>&1
  local status=$?

  [ "$status" -ne 0 ] \
    && grep -q '^name: original$' \
      "$root/.agents/skills/empirical-prompt-tuning/SKILL.md" \
    && no_installer_artifacts "$root/.agents/skills"
}

test_subtree_copy_failure_preserves_existing() {
  local root="$TEST_ROOT/subtree-failure"
  local mock_bin="$root/mock-bin"
  make_installer_fixture "$root"
  make_mock_git "$mock_bin"
  make_failing_cp "$mock_bin"
  write_original_skill "$root/.agents/skills/systematic-debugging"

  PATH="$mock_bin:$PATH" TMPDIR="$root/tmp" \
    "$root/tools/install-external-skills.sh" systematic-debugging \
    >"$root/output.log" 2>&1
  local status=$?

  [ "$status" -ne 0 ] \
    && grep -q '^name: original$' \
      "$root/.agents/skills/systematic-debugging/SKILL.md" \
    && no_installer_artifacts "$root/.agents/skills"
}

test_invalid_payload_preserves_existing() {
  local root="$TEST_ROOT/invalid-payload"
  local mock_bin="$root/mock-bin"
  make_installer_fixture "$root"
  make_mock_curl "$mock_bin"
  write_original_skill "$root/.agents/skills/empirical-prompt-tuning"

  PATH="$mock_bin:$PATH" TMPDIR="$root/tmp" MOCK_CURL_MODE=invalid \
    "$root/tools/install-external-skills.sh" empirical-prompt-tuning \
    >"$root/output.log" 2>&1
  local status=$?

  [ "$status" -ne 0 ] \
    && grep -q '^name: original$' \
      "$root/.agents/skills/empirical-prompt-tuning/SKILL.md" \
    && no_installer_artifacts "$root/.agents/skills"
}

test_final_move_failure_restores_existing() {
  local root="$TEST_ROOT/final-move-failure"
  local mock_bin="$root/mock-bin"
  local dest="$root/.agents/skills/empirical-prompt-tuning"
  make_installer_fixture "$root"
  make_mock_curl "$mock_bin"
  make_failing_final_mv "$mock_bin"
  write_original_skill "$dest"

  PATH="$mock_bin:$PATH" TMPDIR="$root/tmp" MOCK_CURL_MODE=success \
    MOCK_MV_FAIL_DEST="$dest" \
    "$root/tools/install-external-skills.sh" empirical-prompt-tuning \
    >"$root/output.log" 2>&1
  local status=$?

  [ "$status" -ne 0 ] \
    && grep -q '^name: original$' "$dest/SKILL.md" \
    && no_installer_artifacts "$root/.agents/skills"
}

test_successful_single_file_install() {
  local root="$TEST_ROOT/single-success"
  local mock_bin="$root/mock-bin"
  make_installer_fixture "$root"
  make_mock_curl "$mock_bin"
  write_original_skill "$root/.agents/skills/empirical-prompt-tuning"

  PATH="$mock_bin:$PATH" TMPDIR="$root/tmp" MOCK_CURL_MODE=success \
    "$root/tools/install-external-skills.sh" empirical-prompt-tuning \
    >"$root/output.log" 2>&1 \
    && grep -q '^name: downloaded$' \
      "$root/.agents/skills/empirical-prompt-tuning/SKILL.md" \
    && no_installer_artifacts "$root/.agents/skills"
}

test_successful_subtree_install() {
  local root="$TEST_ROOT/subtree-success"
  local mock_bin="$root/mock-bin"
  make_installer_fixture "$root"
  make_mock_git "$mock_bin"
  write_original_skill "$root/.agents/skills/systematic-debugging"

  PATH="$mock_bin:$PATH" TMPDIR="$root/tmp" \
    "$root/tools/install-external-skills.sh" systematic-debugging \
    >"$root/output.log" 2>&1 \
    && grep -q '^name: systematic-debugging$' \
      "$root/.agents/skills/systematic-debugging/SKILL.md" \
    && grep -q '^description: Downloaded fixture.$' \
      "$root/.agents/skills/systematic-debugging/SKILL.md" \
    && no_installer_artifacts "$root/.agents/skills"
}

test_default_install_updates_all_supported_skills() {
  local root="$TEST_ROOT/default-success"
  local mock_bin="$root/mock-bin"
  make_installer_fixture "$root"
  make_mock_curl "$mock_bin"
  make_mock_git "$mock_bin"

  PATH="$mock_bin:$PATH" TMPDIR="$root/tmp" MOCK_CURL_MODE=success \
    "$root/tools/install-external-skills.sh" >"$root/output.log" 2>&1 \
    && grep -q '^name: downloaded$' \
      "$root/.agents/skills/empirical-prompt-tuning/SKILL.md" \
    && grep -q '^name: systematic-debugging$' \
      "$root/.agents/skills/systematic-debugging/SKILL.md" \
    && no_installer_artifacts "$root/.agents/skills"
}

test_unknown_target_fails() {
  local root="$TEST_ROOT/unknown-target"
  make_installer_fixture "$root"

  "$root/tools/install-external-skills.sh" definitely-not-a-real-skill \
    >"$root/output.log" 2>&1
  [ "$?" -ne 0 ]
}

test_path_like_target_is_rejected() {
  local root="$TEST_ROOT/path-target"
  make_installer_fixture "$root"
  printf '%s\n' untouched >"$root/victim"

  "$root/tools/install-external-skills.sh" ../../victim \
    >"$root/output.log" 2>&1
  local status=$?

  [ "$status" -eq 2 ] \
    && grep -q '^invalid skill name:' "$root/output.log" \
    && grep -q '^untouched$' "$root/victim"
}

test_symlinked_skills_directory_is_rejected() {
  local root="$TEST_ROOT/symlinked-skills"
  mkdir -p "$root/tools" "$root/.agents" "$root/outside"
  cp "$REPO_ROOT/tools/install-external-skills.sh" "$root/tools/"
  ln -s "$root/outside" "$root/.agents/skills"

  "$root/tools/install-external-skills.sh" definitely-not-a-real-skill \
    >"$root/output.log" 2>&1
  local status=$?

  [ "$status" -eq 2 ] \
    && grep -q '^refusing symlinked skills directory:' "$root/output.log"
}

make_readme_fixture() {
  local root="$1"
  mkdir -p "$root/tools" "$root/.agents/skills/local-skill" \
    "$root/.agents/skills/godot-tweening"
  cp "$REPO_ROOT/tools/check-readme-skills.sh" "$root/tools/"
  cat >"$root/README.md" <<'README'
| Skill | Purpose |
| --- | --- |
| `local-skill` | Fixture |

## External Skill References

- [`external-one`](https://example.com): Fixture.
README
  cat >"$root/.gitignore" <<'GITIGNORE'
.agents/skills/external-one/
.agents/skills/godot-*/
GITIGNORE
}

test_readme_check_accepts_external_glob() {
  local root="$TEST_ROOT/readme-glob"
  make_readme_fixture "$root"
  "$root/tools/check-readme-skills.sh" >"$root/output.log" 2>&1
}

test_readme_check_requires_exact_external_entry() {
  local root="$TEST_ROOT/readme-external"
  make_readme_fixture "$root"
  sed -i '/external-one/d' "$root/README.md"

  "$root/tools/check-readme-skills.sh" >"$root/output.log" 2>&1
  [ "$?" -ne 0 ]
}

run_test "failed single-file update preserves the installed skill" \
  test_single_file_failure_preserves_existing
run_test "failed subtree copy preserves the installed skill" \
  test_subtree_copy_failure_preserves_existing
run_test "invalid downloaded payload preserves the installed skill" \
  test_invalid_payload_preserves_existing
run_test "failed final move restores the installed skill" \
  test_final_move_failure_restores_existing
run_test "successful single-file update installs validated content" \
  test_successful_single_file_install
run_test "successful subtree update installs validated content" \
  test_successful_subtree_install
run_test "default installer run updates every supported skill" \
  test_default_install_updates_all_supported_skills
run_test "unknown installer target exits non-zero" \
  test_unknown_target_fails
run_test "path-like installer target is rejected" \
  test_path_like_target_is_rejected
run_test "symlinked skills directory is rejected" \
  test_symlinked_skills_directory_is_rejected
run_test "README check treats matching glob directories as external" \
  test_readme_check_accepts_external_glob
run_test "README check requires exact external entries" \
  test_readme_check_requires_exact_external_entry

if [ "$FAILURES" -ne 0 ]; then
  printf '%s test(s) failed\n' "$FAILURES" >&2
  exit 1
fi

printf 'all repository tool tests passed\n'
