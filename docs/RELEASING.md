# Releasing

How to cut a unified `lawpowers` package release. A release has one version, one `vX.Y.Z` tag, and one GitHub Release. The UA and PL changelogs remain component history, but they are not released as separate public version lines.

> **TL;DR:** most of this is automated by [`scripts/release.sh`](../scripts/release.sh):
> ```bash
> ./scripts/release.sh prepare 0.7.1       # bump + branch + PR
> # ... review and merge the PR on GitHub ...
> ./scripts/release.sh publish 0.7.1       # tag v0.7.1 + GitHub Release
> ```
> The manual procedure below explains what the script does step by step; follow it when debugging or when you want finer control.

## Why Unified Releases

OpenCode installs Lawpowers as one git package plugin, and the Claude/Codex adapter manifests are generated compatibility surfaces for the same canonical root sources. Keeping one version avoids a mismatch where OpenCode reports one package while UA and PL report separate release lines.

Going forward:

- **One release = one Lawpowers package version.** Tags are `vX.Y.Z`.
- **All active version fields move together.** Root `package.json`, marketplace metadata, marketplace plugin entries, Claude manifests, and Codex manifests share the same version.
- **Component changelogs still matter.** Update `plugins/ua/CHANGELOG.md` or `plugins/pl/CHANGELOG.md` when that jurisdiction changed, but publish release notes from the root `CHANGELOG.md`.

## Prerequisites

- `gh` CLI installed and authenticated (`gh auth status`).
- Write access to the repo.
- Clean `main` locally: `git checkout main && git pull`.

## 1. Decide The Bump

Pick one Lawpowers version per semver.

Semver guidelines for `0.x`:

- **Patch** (`0.7.0` → `0.7.1`) — wording fixes, non-breaking validation/script fixes, or small docs corrections.
- **Minor** (`0.7.0` → `0.8.0`) — significant additions or breaking changes during `0.x` pre-1.0.
- **Major** (`0.x` → `1.0.0`) — reserved for first stable API commitment or a deliberate breaking restructure.

## 2. Update Version Fields

For release `X.Y.Z`, update every field listed in [`.version-bump.json`](../.version-bump.json):

```text
package.json                                  -> "version": "X.Y.Z"
.claude-plugin/marketplace.json              -> "metadata.version": "X.Y.Z"
.claude-plugin/marketplace.json              -> "plugins[0].version": "X.Y.Z"
.claude-plugin/marketplace.json              -> "plugins[1].version": "X.Y.Z"
plugins/ua/.claude-plugin/plugin.json        -> "version": "X.Y.Z"
plugins/ua/.codex-plugin/plugin.json         -> "version": "X.Y.Z"
plugins/pl/.claude-plugin/plugin.json        -> "version": "X.Y.Z"
plugins/pl/.codex-plugin/plugin.json         -> "version": "X.Y.Z"
```

The release helper does this automatically:

```bash
./scripts/release.sh bump X.Y.Z
```

## 3. Add Changelog Entries

Edit the root changelog for every public release:

| Changelog | Language | When to edit |
|---|---|---|
| [`CHANGELOG.md`](../CHANGELOG.md) | English | Every public release. Release notes are extracted from here. |
| [`plugins/ua/CHANGELOG.md`](../plugins/ua/CHANGELOG.md) | Ukrainian | When UA agents, skills, manifests, or docs changed. |
| [`plugins/pl/CHANGELOG.md`](../plugins/pl/CHANGELOG.md) | Polish | When PL agents, skills, manifests, or docs changed. |

Root changelog template:

```markdown
## [X.Y.Z] — YYYY-MM-DD

### Added / Changed / Fixed / Removed

- Short concrete description of what changed.

### Migration

Only if breaking. Include exact user commands.

[X.Y.Z]: https://github.com/crankshift/lawpowers/releases/tag/vX.Y.Z
```

Component changelog headings use the same `X.Y.Z` version and link to the same root `vX.Y.Z` release tag.

## 4. Validate

Run the adapter generators and validators before committing:

```bash
python3 scripts/generate-claude-plugin-files.py
python3 scripts/convert-agents-to-codex.py
python3 scripts/validate-codex-agents.py
python3 scripts/validate-platform-adapters.py
python3 scripts/validate-ua-request-regime.py
python3 scripts/validate-pl-request-regime.py
python3 -m json.tool package.json >/dev/null
python3 -m json.tool .claude-plugin/marketplace.json >/dev/null
python3 -m json.tool plugins/ua/.claude-plugin/plugin.json >/dev/null
python3 -m json.tool plugins/ua/.codex-plugin/plugin.json >/dev/null
python3 -m json.tool plugins/pl/.claude-plugin/plugin.json >/dev/null
python3 -m json.tool plugins/pl/.codex-plugin/plugin.json >/dev/null
git diff --check
```

All commands must exit 0.

## 5. PR And Merge

Open a feature branch, push, open a PR, merge.

```bash
git checkout -b release-vX.Y.Z
git add -A
git commit -m "lawpowers vX.Y.Z: release"
git push -u origin release-vX.Y.Z
gh pr create --base main --head release-vX.Y.Z \
  --title "lawpowers vX.Y.Z" \
  --body "$(awk '/## \[X.Y.Z\]/,/## \[/' CHANGELOG.md | sed '$d')"
```

Review and merge the PR on GitHub.

## 6. Tag And Publish

The tag name is `vX.Y.Z`.

```bash
git checkout main
git pull --ff-only origin main
MERGE_SHA=$(git rev-parse HEAD)
git tag -a "vX.Y.Z" "$MERGE_SHA" -m "lawpowers vX.Y.Z"
git push origin "vX.Y.Z"
```

Create the GitHub Release from the root changelog section:

```bash
gh release create "vX.Y.Z" \
  --title "lawpowers vX.Y.Z" \
  --notes-file <(awk '/## \[X.Y.Z\]/,/## \[/' CHANGELOG.md | sed '$d')
```

Flags:

- `--prerelease` — for `-rc.N` or similar.
- `--draft` — inspect the generated page before publishing.
- Do not use `--latest` unless you deliberately need to override GitHub's default release ordering.

## 7. Verify

```bash
git ls-remote --tags origin "refs/tags/vX.Y.Z"
gh release view "vX.Y.Z" --json name,tagName,url,isDraft,isPrerelease
```

Users with installed Claude plugins pick up the new version with:

```text
/plugin marketplace update lawpowers
/reload-plugins
```

Codex users should run:

```bash
codex plugin marketplace upgrade lawpowers
```

OpenCode users should restart OpenCode after updating config or package state, then verify with `opencode debug skill`.

## Common Pitfalls

- **Forgetting one version field.** All active version fields listed in `.version-bump.json` move together.
- **Tagging before the PR merges.** Tag the merge commit, not a stale branch commit.
- **Using retired per-jurisdiction tags.** Do not publish `ua/vX.Y.Z` or `pl/vX.Y.Z` for new releases.
- **Omitting the root changelog link reference.** The `[X.Y.Z]: https://...` line makes the section title clickable and keeps release notes traceable.

## Rolling Back A Release

If a release has a critical issue:

1. Prefer a hotfix as a new patch version.
2. If the tag was pushed but the Release should not stay public, delete the Release and tag:

```bash
gh release delete "vX.Y.Z" --yes
git push origin ":refs/tags/vX.Y.Z"
git tag -d "vX.Y.Z"
```

3. Never force-push to `main` to undo a merged release PR; always roll forward with a new patch.

## Related Files

- [`scripts/release.sh`](../scripts/release.sh) — automates `bump`, `prepare` and `publish` for unified package releases.
- [`CHANGELOG.md`](../CHANGELOG.md) — root release changelog and release-note source.
- [`plugins/ua/CHANGELOG.md`](../plugins/ua/CHANGELOG.md) — UA component history.
- [`plugins/pl/CHANGELOG.md`](../plugins/pl/CHANGELOG.md) — PL component history.
- [`.version-bump.json`](../.version-bump.json) — inventory of versioned fields.
- [`CLAUDE.md`](../CLAUDE.md) — contributor guide with abbreviated release guidance.
