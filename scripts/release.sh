#!/usr/bin/env bash
#
# Release helper for the lawpowers monorepo.
# See docs/RELEASING.md for the full manual procedure; this script
# automates the mechanical parts.
#
# Usage:
#   ./scripts/release.sh bump <plugin> <version>
#       Update the plugin's version in its plugin.json and in the
#       marketplace entry. <plugin> is 'ua' or 'pl'. Validates after.
#
#   ./scripts/release.sh bump-marketplace <version>
#       Update marketplace.json metadata.version only. Used on
#       catalog-shape changes (plugin added/removed, structural
#       reshuffle). Does not tag or publish anything.
#
#   ./scripts/release.sh prepare <plugin> <version>
#       From a clean main: create branch release-<plugin>-v<version>,
#       run bump, wait for you to edit the plugin CHANGELOG, commit,
#       push, open a PR.
#
#   ./scripts/release.sh publish <plugin> <version>
#       After the PR merges: pull main, tag the merge commit as
#       <plugin>/v<version>, publish a GitHub Release with body
#       extracted from the plugin CHANGELOG section for that version.
#
# Requirements: bash, git, gh (authenticated), jq, awk, claude CLI.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MARKETPLACE_JSON="$REPO_ROOT/.claude-plugin/marketplace.json"

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

# Resolve plugin paths/indices. Keeps plugin-specific knowledge in one place.
plugin_json_path() {
  case "$1" in
    ua) echo "$REPO_ROOT/plugins/ua/.claude-plugin/plugin.json" ;;
    pl) echo "$REPO_ROOT/plugins/pl/.claude-plugin/plugin.json" ;;
    *)  die "unknown plugin: $1 (expected 'ua' or 'pl')" ;;
  esac
}

plugin_changelog_path() {
  case "$1" in
    ua) echo "$REPO_ROOT/plugins/ua/CHANGELOG.md" ;;
    pl) echo "$REPO_ROOT/plugins/pl/CHANGELOG.md" ;;
    *)  die "unknown plugin: $1 (expected 'ua' or 'pl')" ;;
  esac
}

plugin_marketplace_index() {
  case "$1" in
    ua) echo "0" ;;
    pl) echo "1" ;;
    *)  die "unknown plugin: $1 (expected 'ua' or 'pl')" ;;
  esac
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

cmd_bump() {
  local plugin="${1:?usage: bump <plugin> <version>}"
  local version="${2:?usage: bump <plugin> <version>}"

  local plugin_json idx
  plugin_json=$(plugin_json_path "$plugin")
  idx=$(plugin_marketplace_index "$plugin")

  info "$plugin plugin → $version"
  set_json_field "$plugin_json" '.version' "$version"
  set_json_field "$MARKETPLACE_JSON" ".plugins[$idx].version" "$version"

  info "validating plugin..."
  claude plugin validate "$REPO_ROOT"
}

cmd_bump_marketplace() {
  local version="${1:?usage: bump-marketplace <version>}"

  info "marketplace.metadata.version → $version"
  set_json_field "$MARKETPLACE_JSON" '.metadata.version' "$version"

  info "validating plugin..."
  claude plugin validate "$REPO_ROOT"
}

cmd_prepare() {
  local plugin="${1:?usage: prepare <plugin> <version>}"
  local version="${2:?usage: prepare <plugin> <version>}"

  cd "$REPO_ROOT"

  if ! git diff --quiet || ! git diff --cached --quiet; then
    die "working tree not clean; commit or stash first"
  fi

  info "switching to main and pulling..."
  git checkout main
  git pull --ff-only origin main

  local branch="release-$plugin-v$version"
  if git rev-parse --verify "$branch" >/dev/null 2>&1; then
    die "branch $branch already exists locally"
  fi
  git checkout -b "$branch"

  cmd_bump "$plugin" "$version"

  local changelog
  changelog=$(plugin_changelog_path "$plugin")

  cat <<MSG

Now edit the CHANGELOG:

  - $changelog

Add a [$version] section at the top, plus the link reference at the bottom
pointing to https://github.com/crankshift/lawpowers/releases/tag/$plugin/v$version
See docs/RELEASING.md for templates.

Press Enter when done.
MSG
  read -r _

  if ! grep -q "^## \[$version\]" "$changelog"; then
    die "no [$version] section found in $changelog"
  fi
  if ! grep -q "^\[$version\]:" "$changelog"; then
    die "no [$version]: link reference at the bottom of $changelog"
  fi

  info "committing..."
  git add -A
  git commit -m "$plugin v$version: release"
  git push -u origin "$branch"

  info "opening PR..."
  local body
  body=$(extract_section "$changelog" "$version")
  gh pr create --base main --head "$branch" \
    --title "$plugin v$version" \
    --body "$body"

  cat <<MSG

PR opened. Merge it on GitHub, then run:

  ./scripts/release.sh publish $plugin $version

MSG
}

cmd_publish() {
  local plugin="${1:?usage: publish <plugin> <version>}"
  local version="${2:?usage: publish <plugin> <version>}"

  cd "$REPO_ROOT"

  info "switching to main and pulling..."
  git checkout main
  git pull --ff-only origin main

  local merge_sha tag
  merge_sha=$(git rev-parse HEAD)
  tag="$plugin/v$version"

  if git rev-parse --verify "$tag" >/dev/null 2>&1; then
    die "tag $tag already exists"
  fi

  info "tagging $tag on $merge_sha..."
  git tag -a "$tag" "$merge_sha" -m "$plugin v$version"
  git push origin "$tag"

  info "publishing GitHub release..."
  local changelog body
  changelog=$(plugin_changelog_path "$plugin")
  body=$(extract_section "$changelog" "$version")
  echo "$body" | gh release create "$tag" \
    --title "$plugin v$version" \
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
    bump-marketplace) cmd_bump_marketplace "$@" ;;
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
