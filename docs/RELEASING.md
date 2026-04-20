# Releasing

How to cut a release of `lawpowers`. Manual, six steps, all from the command line.

> **TL;DR:** most of this is automated by [`scripts/release.sh`](../scripts/release.sh):
> ```bash
> ./scripts/release.sh prepare 0.5.0       # bump + branch + PR
> # … review and merge the PR on GitHub …
> ./scripts/release.sh publish 0.5.0       # tag + GitHub Release
> ```
> The manual procedure below explains what the script does step by step; follow it when debugging or when you want finer control.

## Prerequisites

- `gh` CLI installed and authenticated (`gh auth status`).
- Write access to the repo.
- Clean `main` locally: `git checkout main && git pull`.

## 1. Decide which versions to bump

Three version fields can move independently:

| Field | Location | Bump when |
|---|---|---|
| Marketplace version | `.claude-plugin/marketplace.json` → `metadata.version` | Any user-visible change to the marketplace catalog (plugin added/removed, plugin version changes). |
| Plugin version | `<plugin>/.claude-plugin/plugin.json` → `version` AND `.claude-plugin/marketplace.json` → `plugins[N].version` | When that specific plugin changes. |

[`.version-bump.json`](../.version-bump.json) is the source of truth for which fields must stay in sync — check it before editing.

Semver guidelines for `0.x`:

- **Patch** (`0.4.0 → 0.4.1`) — wording fixes, new skills or agents that don't break existing invocations, non-breaking internal refactors.
- **Minor** (`0.4.0 → 0.5.0`) — significant additions (new agent category, new skill set) or a breaking change during `0.x` pre-1.0.
- **Major** (`0.x → 1.0.0`) — not yet; reserved for first stable API commitment or a deliberate breaking restructure.

## 2. Update the version fields

Edit each file listed in `.version-bump.json` for the plugin(s) you're releasing. Typical case — bumping `ua` alone:

```
ua/.claude-plugin/plugin.json            → "version": "X.Y.Z"
.claude-plugin/marketplace.json          → "plugins[0].version": "X.Y.Z"
.claude-plugin/marketplace.json          → "metadata.version": "X.Y.Z"   # if catalog itself moved
```

Validate after:

```bash
claude plugin validate .
```

Must report `✔ Validation passed`.

## 3. Add CHANGELOG entries

Three changelogs are maintained in parallel. Which you edit depends on what changed:

| Changelog | Language | When to edit |
|---|---|---|
| [root `CHANGELOG.md`](../CHANGELOG.md) | English | Marketplace-level changes (catalog, monorepo structure, shared tooling). Also writes a short summary referencing the plugin CHANGELOG for every plugin-affecting release. |
| [`ua/CHANGELOG.md`](../ua/CHANGELOG.md) | Ukrainian | Plugin `ua` changes — agents, skills, templates, docs. |
| [`pl/CHANGELOG.md`](../pl/CHANGELOG.md) | Polish | Plugin `pl` changes. |

For a typical release you'll touch the root changelog **plus** the changelog of whichever plugin you modified. Every changelog follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Insert a new section at the top (right below the heading) and add a matching link reference at the bottom.

### Root `CHANGELOG.md` template (English)

```markdown
## [X.Y.Z] — YYYY-MM-DD

### Changed — plugin `ua`

One-line summary. Details in [`ua/CHANGELOG.md`](./ua/CHANGELOG.md).

### Migration

Only if breaking. Exact commands users need to run:

    /plugin marketplace update lawpowers
    /plugin uninstall ua@lawpowers
    /plugin install ua@lawpowers
    /reload-plugins

[X.Y.Z]: https://github.com/crankshift/lawpowers/releases/tag/vX.Y.Z
```

### Plugin `ua/CHANGELOG.md` template (Ukrainian)

```markdown
## [X.Y.Z] — YYYY-MM-DD

### Added / Changed / Fixed / Removed

- **Короткий жирний заголовок** — конкретний опис. Посилатись на статті НПА (zakon.rada ID), рішення ВС, PR-номер.

[X.Y.Z]: https://github.com/crankshift/lawpowers/releases/tag/vX.Y.Z
```

### Plugin `pl/CHANGELOG.md` template (Polish)

```markdown
## [X.Y.Z] — YYYY-MM-DD

### Added / Changed / Fixed / Removed

- **Krótki pogrubiony nagłówek** — konkretny opis. Odwołania do ISAP, Portal Orzeczeń, sygnatur akt, numer PR.

[X.Y.Z]: https://github.com/crankshift/lawpowers/releases/tag/vX.Y.Z
```

## 4. PR and merge

Open a feature branch, push, open a PR, merge.

```bash
git checkout -b release-vX.Y.Z
git add -A
git commit -m "vX.Y.Z: <headline>"
git push -u origin release-vX.Y.Z
gh pr create --base main --head release-vX.Y.Z --title "vX.Y.Z: <headline>" --body "$(sed -n '/## \[X.Y.Z\]/,/## \[/p' CHANGELOG.md | sed '$d')"
```

Review. Merge the PR on GitHub (this repo enforces PR review — direct push to `main` is blocked).

## 5. Tag the merge commit and push

```bash
git checkout main && git pull
MERGE_SHA=$(git rev-parse HEAD)
git tag -a vX.Y.Z "$MERGE_SHA" -m "vX.Y.Z — <headline>"
git push origin vX.Y.Z
```

## 6. Create the GitHub Release

Release notes use the **root** `CHANGELOG.md` section as the body (English). The `awk` below reads everything between the target version header and the next one, then trims the trailing separator line.

```bash
gh release create vX.Y.Z \
  --title "vX.Y.Z — <headline>" \
  --notes-file <(awk '/## \[X.Y.Z\]/,/## \[/' CHANGELOG.md | sed '$d') \
  --latest
```

If you want the per-plugin detail visible directly in the release page, append the plugin changelog section too:

```bash
{
  awk '/## \[X.Y.Z\]/,/## \[/' CHANGELOG.md | sed '$d'
  echo
  echo '---'
  echo '### Плагін `ua` (детально)'
  awk '/## \[X.Y.Z\]/,/## \[/' ua/CHANGELOG.md | sed '$d'
} | gh release create vX.Y.Z --title "vX.Y.Z — <headline>" --notes-file - --latest
```

Flags:

- `--latest` marks this as the "Latest" release on the Releases page. Skip it if you're publishing an older patch out-of-order.
- `--prerelease` if you're doing an `-rc.N` or similar.
- `--draft` if you want to inspect the generated page before publishing.

## 7. Verify

```bash
gh release view vX.Y.Z --json name,tagName,isLatest,url
```

Users on installed plugins pick up the new version with:

```
/plugin marketplace update lawpowers
/reload-plugins
```

Users with auto-update enabled for the `lawpowers` marketplace get it on their next Claude Code startup.

## Common pitfalls

- **Forgetting to bump `plugins[N].version` in the marketplace.** The plugin version is listed in two places; leaving one stale makes updates silently fail. Always grep for the old version after editing.
- **Tagging before the PR merges.** Tag the merge commit, not the last commit on the feature branch.
- **Omitting the link reference at the bottom of CHANGELOG.md.** The `[X.Y.Z]: https://…` line at the end is what makes the section title clickable.
- **Using a raw version number (`0.4.0`) instead of the `v`-prefixed tag (`v0.4.0`).** GitHub Releases and existing tooling expect `v`.
- **Forgetting `--latest` on the Release.** If missing, the Releases page doesn't highlight the newest version.

## Rolling back a release

If a release has a critical issue:

1. Publish a hotfix as a new patch version — don't delete the tag.
2. If the tag was pushed but the Release isn't public yet, delete the draft and the tag:
   ```bash
   gh release delete vX.Y.Z --yes
   git push origin :refs/tags/vX.Y.Z
   git tag -d vX.Y.Z
   ```
3. Never force-push to `main` to "undo" a merged release PR; always roll forward with a new patch.

## Related files

- [`scripts/release.sh`](../scripts/release.sh) — automates `bump`, `prepare` (bump + branch + PR), and `publish` (tag + GitHub Release).
- [`CHANGELOG.md`](../CHANGELOG.md) — release history (root, English).
- [`ua/CHANGELOG.md`](../ua/CHANGELOG.md) — plugin `ua` history (Ukrainian).
- [`pl/CHANGELOG.md`](../pl/CHANGELOG.md) — plugin `pl` history (Polish).
- [`.version-bump.json`](../.version-bump.json) — inventory of versioned fields.
- [`CLAUDE.md`](../CLAUDE.md) — contributor guide with the abbreviated release section.
