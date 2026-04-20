#!/usr/bin/env bash
#
# Release helper for the lawpowers monorepo.
# See docs/RELEASING.md for the full manual procedure; this script
# automates the mechanical parts.
#
# Usage:
#   ./scripts/release.sh bump <marketplace-version> [ua-version] [pl-version]
#       Update the marketplace metadata.version and, optionally, plugin
#       versions. Leave a plugin version blank or use '-' to skip it.
#       Validates the plugin afterwards.
#
#   ./scripts/release.sh prepare <marketplace-version> [ua-version] [pl-version]
#       From a clean main: create branch release-v<version>, run bump,
#       wait for you to edit CHANGELOG entries, commit, push, open a PR.
#
#   ./scripts/release.sh publish <marketplace-version>
#       After the PR merges: pull main, tag the merge commit, publish
#       a GitHub Release with body extracted from the root CHANGELOG
#       section for that version.
#
# Requirements: bash, git, gh (authenticated), jq, awk, claude CLI.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MARKETPLACE_JSON="$REPO_ROOT/.claude-plugin/marketplace.json"
UA_PLUGIN_JSON="$REPO_ROOT/ua/.claude-plugin/plugin.json"
PL_PLUGIN_JSON="$REPO_ROOT/pl/.claude-plugin/plugin.json"
CHANGELOG="$REPO_ROOT/CHANGELOG.md"
UA_CHANGELOG="$REPO_ROOT/ua/CHANGELOG.md"
PL_CHANGELOG="$REPO_ROOT/pl/CHANGELOG.md"

die() { echo "error: $*" >&2; exit 1; }
info() { echo "==> $*"; }

require_tool() {
  command -v "$1" >/dev/null 2>&1 || die "required tool not found: $1"
}

check_tools() {
  for t in git gh jq awk claude; do
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

# Extract the CHANGELOG section for a given version.
# Reads from "## [VERSION]" up to (but not including) the next "## [".
extract_section() {
  local file="$1" version="$2"
  awk -v v="$version" '
    $0 ~ "^## \\[" v "\\]" { inside=1; print; next }
    inside && /^## \[/ { exit }
    inside { print }
    END { if (!inside) exit 1 }
  ' "$file"
}

# Build release body by concatenating root + plugin CHANGELOG sections.
build_release_body() {
  local version="$1"
  extract_section "$CHANGELOG" "$version"

  if grep -q "^## \[$version\]" "$UA_CHANGELOG" 2>/dev/null; then
    echo
    echo "---"
    echo
    echo "### Плагін \`ua\` (детально)"
    echo
    extract_section "$UA_CHANGELOG" "$version"
  fi

  if grep -q "^## \[$version\]" "$PL_CHANGELOG" 2>/dev/null; then
    echo
    echo "---"
    echo
    echo "### Plagin \`pl\` (szczegółowo)"
    echo
    extract_section "$PL_CHANGELOG" "$version"
  fi
}

cmd_bump() {
  local mk_v="${1:?usage: bump <marketplace-version> [ua-version] [pl-version]}"
  local ua_v="${2:-}"
  local pl_v="${3:-}"

  info "marketplace.metadata.version → $mk_v"
  set_json_field "$MARKETPLACE_JSON" '.metadata.version' "$mk_v"

  if [[ -n "$ua_v" && "$ua_v" != "-" ]]; then
    info "ua plugin → $ua_v"
    set_json_field "$UA_PLUGIN_JSON" '.version' "$ua_v"
    set_json_field "$MARKETPLACE_JSON" '.plugins[0].version' "$ua_v"
  fi

  if [[ -n "$pl_v" && "$pl_v" != "-" ]]; then
    info "pl plugin → $pl_v"
    set_json_field "$PL_PLUGIN_JSON" '.version' "$pl_v"
    set_json_field "$MARKETPLACE_JSON" '.plugins[1].version' "$pl_v"
  fi

  info "validating plugin..."
  claude plugin validate "$REPO_ROOT"
}

cmd_prepare() {
  local mk_v="${1:?usage: prepare <marketplace-version> [ua-version] [pl-version]}"
  local ua_v="${2:-}"
  local pl_v="${3:-}"

  cd "$REPO_ROOT"

  if ! git diff --quiet || ! git diff --cached --quiet; then
    die "working tree not clean; commit or stash first"
  fi

  info "switching to main and pulling..."
  git checkout main
  git pull --ff-only origin main

  local branch="release-v$mk_v"
  if git rev-parse --verify "$branch" >/dev/null 2>&1; then
    die "branch $branch already exists locally"
  fi
  git checkout -b "$branch"

  cmd_bump "$mk_v" "$ua_v" "$pl_v"

  cat <<MSG

Now edit the CHANGELOGs:

  - $CHANGELOG (English, root; always required)
$( [[ -n "$ua_v" && "$ua_v" != "-" ]] && echo "  - $UA_CHANGELOG (Ukrainian; \`ua\` bumped)" || echo "  - $UA_CHANGELOG (Ukrainian; only if \`ua\` changed)" )
$( [[ -n "$pl_v" && "$pl_v" != "-" ]] && echo "  - $PL_CHANGELOG (Polish; \`pl\` bumped)" || echo "  - $PL_CHANGELOG (Polish; only if \`pl\` changed)" )

Add a [$mk_v] section at the top of each, plus the link reference at the bottom.
See docs/RELEASING.md for templates.

Press Enter when done.
MSG
  read -r _

  if ! grep -q "^## \[$mk_v\]" "$CHANGELOG"; then
    die "no [$mk_v] section found in root CHANGELOG.md"
  fi
  if ! grep -q "^\[$mk_v\]:" "$CHANGELOG"; then
    die "no [$mk_v]: link reference at the bottom of root CHANGELOG.md"
  fi

  info "committing..."
  git add -A
  git commit -m "v$mk_v: release"
  git push -u origin "$branch"

  info "opening PR..."
  local body
  body=$(build_release_body "$mk_v")
  gh pr create --base main --head "$branch" \
    --title "v$mk_v" \
    --body "$body"

  cat <<MSG

PR opened. Merge it on GitHub, then run:

  ./scripts/release.sh publish $mk_v

MSG
}

cmd_publish() {
  local version="${1:?usage: publish <version>}"

  cd "$REPO_ROOT"

  info "switching to main and pulling..."
  git checkout main
  git pull --ff-only origin main

  local merge_sha
  merge_sha=$(git rev-parse HEAD)

  if git rev-parse --verify "v$version" >/dev/null 2>&1; then
    die "tag v$version already exists"
  fi

  info "tagging v$version on $merge_sha..."
  git tag -a "v$version" "$merge_sha" -m "v$version"
  git push origin "v$version"

  info "publishing GitHub release..."
  local body
  body=$(build_release_body "$version")
  echo "$body" | gh release create "v$version" \
    --title "v$version" \
    --notes-file - \
    --latest

  local url
  url=$(gh release view "v$version" --json url --jq .url)
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
