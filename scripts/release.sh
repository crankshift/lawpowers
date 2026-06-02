#!/usr/bin/env bash
#
# Release helper for the lawpowers package.
# See docs/RELEASING.md for the full manual procedure; this script
# automates the mechanical parts.
#
# Usage:
#   ./scripts/release.sh bump <version>
#       Update the unified Lawpowers version across package.json,
#       marketplace metadata, Claude manifests, and Codex manifests.
#
#   ./scripts/release.sh prepare <version>
#       From a clean main: create branch release-v<version>, run bump,
#       wait for you to edit changelogs, commit, push, open a PR.
#
#   ./scripts/release.sh publish <version>
#       After the PR merges: pull main, tag the merge commit as
#       v<version>, publish one GitHub Release with body extracted
#       from the root CHANGELOG section for that version.
#
# Requirements: bash, git, gh (authenticated), jq, awk, python3.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PACKAGE_JSON="$REPO_ROOT/package.json"
MARKETPLACE_JSON="$REPO_ROOT/.claude-plugin/marketplace.json"
ROOT_CHANGELOG="$REPO_ROOT/CHANGELOG.md"
UA_CLAUDE_JSON="$REPO_ROOT/plugins/ua/.claude-plugin/plugin.json"
UA_CODEX_JSON="$REPO_ROOT/plugins/ua/.codex-plugin/plugin.json"
PL_CLAUDE_JSON="$REPO_ROOT/plugins/pl/.claude-plugin/plugin.json"
PL_CODEX_JSON="$REPO_ROOT/plugins/pl/.codex-plugin/plugin.json"

die() { echo "error: $*" >&2; exit 1; }
info() { echo "==> $*"; }

require_tool() {
  command -v "$1" >/dev/null 2>&1 || die "required tool not found: $1"
}

check_tools() {
  for t in git gh jq awk python3; do
    require_tool "$t"
  done
  gh auth status >/dev/null 2>&1 || die "gh not authenticated; run 'gh auth login'"
}

# Set a JSON field using jq, preserving 2-space indent.
set_json_field() {
  local file="$1" path="$2" value="$3"
  [[ -f "$file" ]] || die "file not found: $file"
  local tmp
  tmp=$(mktemp)
  jq --indent 2 "$path = \"$value\"" "$file" >"$tmp"
  mv "$tmp" "$file"
}

require_json_version() {
  local file="$1" path="$2" expected="$3"
  local actual
  actual=$(jq -r "$path" "$file")
  [[ "$actual" == "$expected" ]] || die "$file $path is $actual, expected $expected"
}

validate_versions() {
  local version="$1"
  require_json_version "$PACKAGE_JSON" '.version' "$version"
  require_json_version "$MARKETPLACE_JSON" '.metadata.version' "$version"
  require_json_version "$MARKETPLACE_JSON" '.plugins[0].version' "$version"
  require_json_version "$MARKETPLACE_JSON" '.plugins[1].version' "$version"
  require_json_version "$UA_CLAUDE_JSON" '.version' "$version"
  require_json_version "$UA_CODEX_JSON" '.version' "$version"
  require_json_version "$PL_CLAUDE_JSON" '.version' "$version"
  require_json_version "$PL_CODEX_JSON" '.version' "$version"
}

run_validations() {
  python3 -m json.tool "$PACKAGE_JSON" >/dev/null
  python3 -m json.tool "$MARKETPLACE_JSON" >/dev/null
  python3 -m json.tool "$UA_CLAUDE_JSON" >/dev/null
  python3 -m json.tool "$UA_CODEX_JSON" >/dev/null
  python3 -m json.tool "$PL_CLAUDE_JSON" >/dev/null
  python3 -m json.tool "$PL_CODEX_JSON" >/dev/null
  python3 "$REPO_ROOT/scripts/validate-platform-adapters.py"
  python3 "$REPO_ROOT/scripts/validate-ua-request-regime.py"
  python3 "$REPO_ROOT/scripts/validate-pl-request-regime.py"
}

# Extract the root CHANGELOG section for a given version.
# Reads from "## [VERSION]" up to (but not including) the next "## [".
# Strips markdown link-reference lines from release notes.
extract_section() {
  local file="$1" version="$2"
  awk -v v="$version" '
    $0 ~ "^## \\[" v "\\]" { inside=1; print; next }
    inside && /^## \[/ { exit }
    inside && /^\[[^]]+\]:[[:space:]]+https?:\/\// { next }
    inside { print }
    END { if (!inside) exit 1 }
  ' "$file"
}

cmd_bump() {
  local version="${1:?usage: bump <version>}"

  info "lawpowers → $version"
  set_json_field "$PACKAGE_JSON" '.version' "$version"
  set_json_field "$MARKETPLACE_JSON" '.metadata.version' "$version"
  set_json_field "$MARKETPLACE_JSON" '.plugins[0].version' "$version"
  set_json_field "$MARKETPLACE_JSON" '.plugins[1].version' "$version"
  set_json_field "$UA_CLAUDE_JSON" '.version' "$version"
  set_json_field "$UA_CODEX_JSON" '.version' "$version"
  set_json_field "$PL_CLAUDE_JSON" '.version' "$version"
  set_json_field "$PL_CODEX_JSON" '.version' "$version"

  info "validating release metadata..."
  validate_versions "$version"
  run_validations
}

cmd_prepare() {
  local version="${1:?usage: prepare <version>}"

  cd "$REPO_ROOT"

  if ! git diff --quiet || ! git diff --cached --quiet; then
    die "working tree not clean; commit or stash first"
  fi

  info "switching to main and pulling..."
  git checkout main
  git pull --ff-only origin main

  local branch="release-v$version"
  if git rev-parse --verify "$branch" >/dev/null 2>&1; then
    die "branch $branch already exists locally"
  fi
  git checkout -b "$branch"

  cmd_bump "$version"

  cat <<MSG

Now edit the changelogs:

  - $ROOT_CHANGELOG
  - $REPO_ROOT/plugins/ua/CHANGELOG.md
  - $REPO_ROOT/plugins/pl/CHANGELOG.md

Add a [$version] section to the root changelog, plus the link reference at the bottom
pointing to https://github.com/crankshift/lawpowers/releases/tag/v$version
See docs/RELEASING.md for templates.

Press Enter when done.
MSG
  read -r _

  if ! grep -q "^## \[$version\]" "$ROOT_CHANGELOG"; then
    die "no [$version] section found in $ROOT_CHANGELOG"
  fi
  if ! grep -q "^\[$version\]:" "$ROOT_CHANGELOG"; then
    die "no [$version]: link reference at the bottom of $ROOT_CHANGELOG"
  fi

  info "committing..."
  git add -A
  git commit -m "lawpowers v$version: release"
  git push -u origin "$branch"

  info "opening PR..."
  local body
  body=$(extract_section "$ROOT_CHANGELOG" "$version")
  gh pr create --base main --head "$branch" \
    --title "lawpowers v$version" \
    --body "$body"

  cat <<MSG

PR opened. Merge it on GitHub, then run:

  ./scripts/release.sh publish $version

MSG
}

cmd_publish() {
  local version="${1:?usage: publish <version>}"

  cd "$REPO_ROOT"

  info "switching to main and pulling..."
  git checkout main
  git pull --ff-only origin main

  local merge_sha tag
  merge_sha=$(git rev-parse HEAD)
  tag="v$version"

  if git rev-parse --verify "$tag" >/dev/null 2>&1; then
    die "tag $tag already exists"
  fi

  info "tagging $tag on $merge_sha..."
  git tag -a "$tag" "$merge_sha" -m "lawpowers v$version"
  git push origin "$tag"

  info "publishing GitHub release..."
  local body
  body=$(extract_section "$ROOT_CHANGELOG" "$version")
  echo "$body" | gh release create "$tag" \
    --title "lawpowers v$version" \
    --notes-file -

  local url
  url=$(gh release view "$tag" --json url --jq .url)
  info "published: $url"
}

main() {
  check_tools
  local cmd="${1:-}"
  shift || true

  case "$cmd" in
    bump) cmd_bump "$@" ;;
    prepare) cmd_prepare "$@" ;;
    publish) cmd_publish "$@" ;;
    -h|--help|help|"")
      sed -n '2,/^$/p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
      ;;
    *)
      die "unknown command: $cmd (try --help)"
      ;;
  esac
}

main "$@"
