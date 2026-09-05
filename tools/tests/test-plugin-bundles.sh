#!/usr/bin/env bash
set -euo pipefail
repo=$(cd "$(dirname "$0")/../.." && pwd); python=${PYTHON:-python3}
build="$repo/tools/plugin-bundles/build.py"; validate="$repo/tools/plugin-bundles/validate.py"
work=$(mktemp -d); trap 'rm -rf "$work"' EXIT; export PYTHONDONTWRITEBYTECODE=1

for composition in "$repo"/plugin-bundles/*.json; do
  [[ $(basename "$composition") == schema.json ]] && continue
  "$python" "$validate" --composition "$composition" --repo "$repo" >/dev/null
  for target in codex claude; do
    artifact=$($python "$build" "$composition" --target "$target" --output "$work/out" --repo "$repo")
    "$python" "$validate" --artifact "$artifact" --composition "$composition" --repo "$repo" >/dev/null
  done
done

fixture="$work/repo"
mkdir -p "$fixture/.agents/skills/test-skill" "$fixture/plugin-bundles" "$fixture/tools/plugin-bundles"
cp "$repo/LICENSE" "$fixture/LICENSE"; cp "$repo/plugin-bundles/schema.json" "$fixture/plugin-bundles/schema.json"
cp "$repo/tools/plugin-bundles/"*.py "$fixture/tools/plugin-bundles/"
printf '%s\n' '---' 'name: test-skill' 'description: Tests fixtures.' '---' '# Test' > "$fixture/.agents/skills/test-skill/SKILL.md"
base="$fixture/plugin-bundles/test.json"
printf '%s\n' '{"schemaVersion":1,"slug":"test-plugin","version":"0.1.0","description":"Test.","author":{"name":"test","url":"https://example.test"},"repository":"https://example.test","license":"MIT","keywords":["test"],"skills":["test-skill"],"targets":{"codex":{"displayName":"Test","shortDescription":"Short","category":"Developer Tools","defaultPrompts":["Test it."]},"claude":{"displayName":"Test"}}}' > "$base"
expect_failure() { if "$@" >"$work/unexpected.stdout" 2>"$work/expected.stderr"; then printf 'expected failure: %s\n' "$*" >&2; exit 1; fi; }
mutate() { "$python" -c 'import json,sys; d=json.load(open(sys.argv[1])); exec(sys.argv[2]); json.dump(d,open(sys.argv[3],"w"))' "$base" "$1" "$work/bad.json"; }

# One negative case for every declared field family, plus all uniqueness/length rules.
for mutation in 'd["unknown"]=1' 'd["schemaVersion"]=2' 'd["slug"]="Bad Slug"' 'd["version"]="1.0"' 'd["description"]="   "' 'd["author"]={"name":" "}' 'd["author"]["extra"]=1' 'd["author"]["url"]="http://bad"' 'd["repository"]="http://bad"' 'd["license"]=" "' 'd["keywords"]=["x","x"]' 'd["keywords"]=[" "]' 'd["skills"]=[]' 'd["skills"]=["test-skill","test-skill"]' 'd["skills"]=["missing-skill"]' 'd["targets"]={}' 'd["targets"]={"other":{"displayName":"x"}}' 'd["targets"]["codex"]["extra"]=1' 'd["targets"]["codex"]["displayName"]=" "' 'd["targets"]["codex"]["shortDescription"]=" "' 'd["targets"]["codex"]["category"]=" "' 'd["targets"]["codex"]["defaultPrompts"]=["x","x"]' 'd["targets"]["codex"]["defaultPrompts"]=[" "]' 'd["targets"]["codex"]["defaultPrompts"]=["x"*129]'; do
  mutate "$mutation"; expect_failure "$python" "$validate" --composition "$work/bad.json" --repo "$fixture"
done
ln -s SKILL.md "$fixture/.agents/skills/test-skill/link.md"; expect_failure "$python" "$validate" --composition "$base" --repo "$fixture"; rm "$fixture/.agents/skills/test-skill/link.md"
mkdir "$fixture/.agents/skills/test-skill/__pycache__"; printf x > "$fixture/.agents/skills/test-skill/__pycache__/bad.pyc"
expect_failure "$python" "$validate" --composition "$base" --repo "$fixture"; rm -r "$fixture/.agents/skills/test-skill/__pycache__"

# Publishable identities are immutable; changed effective content requires a version bump.
git -C "$fixture" init -q; git -C "$fixture" config user.email test@example.test; git -C "$fixture" config user.name test
git -C "$fixture" add .; git -C "$fixture" commit -qm initial
fixture_build="$fixture/tools/plugin-bundles/build.py"; fixture_validate="$fixture/tools/plugin-bundles/validate.py"
artifact=$($python "$fixture_build" "$base" --target codex --output "$work/release" --repo "$fixture" --publishable)
"$python" "$fixture_validate" --artifact "$artifact" --composition "$base" --repo "$fixture" --publishable >/dev/null
printf '\nChanged.\n' >> "$fixture/.agents/skills/test-skill/SKILL.md"
expect_failure "$python" "$fixture_build" "$base" --target codex --output "$work/release" --repo "$fixture" --publishable
git -C "$fixture" add .agents/skills/test-skill/SKILL.md; git -C "$fixture" commit -qm content-change
expect_failure "$python" "$fixture_build" "$base" --target codex --output "$work/release" --repo "$fixture" --publishable
"$python" -c 'import json,sys; p=sys.argv[1]; d=json.load(open(p)); d["version"]="0.1.1"; json.dump(d,open(p,"w"))' "$base"
git -C "$fixture" add plugin-bundles/test.json; git -C "$fixture" commit -qm version-bump
"$python" "$fixture_build" "$base" --target codex --output "$work/release" --repo "$fixture" --publishable >/dev/null
"$python" "$repo/tools/tests/test-plugin-bundle-integrity.py"
"$python" "$repo/tools/tests/test-published-plugins.py"
"$python" "$repo/tools/plugin-bundles/published.py" --repo "$repo" --check
"$python" "$repo/tools/plugin-bundles/package.py" --repo "$repo" --output "$work/packages" >/dev/null
(cd "$work/packages" && sha256sum --check SHA256SUMS >/dev/null)
expect_failure "$python" "$repo/tools/plugin-bundles/package.py" --repo "$repo" --output "$work/packages"
printf 'plugin bundle tests passed\n'
