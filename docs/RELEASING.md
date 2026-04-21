# Releasing

How to cut a release of a `lawpowers` plugin. Each plugin (`ua`, `pl`) is released **independently**, with its own tag, its own GitHub Release, and its own CHANGELOG.

> **TL;DR:** most of this is automated by [`scripts/release.sh`](../scripts/release.sh):
> ```bash
> ./scripts/release.sh prepare ua 0.5.0       # bump + branch + PR
> # … review and merge the PR on GitHub …
> ./scripts/release.sh publish ua 0.5.0       # tag ua/v0.5.0 + GitHub Release
> ```
> The manual procedure below explains what the script does step by step; follow it when debugging or when you want finer control.

## Why per-plugin releases

Users don't install "the marketplace" — they install a specific plugin via `/plugin install ua@lawpowers` or `/plugin install pl@lawpowers`. Each plugin has its own `version` in `plugin.json` and moves on its own schedule. Releasing them together under one umbrella tag (`v0.6.0` = `ua 0.4.0` + `pl 0.2.0`) confused users who saw "install v0.6.0" and wondered why their plugin showed `0.4.0`.

Going forward:

- **One release = one plugin.** Tags are namespaced: `ua/vX.Y.Z`, `pl/vX.Y.Z`. The tag version always matches the plugin's `version` field exactly.
- **Umbrella `vX.Y.Z` tags are retired.** Historical tags (`v0.1.0`…`v0.6.0`) stay on the repo unchanged; no new umbrella tags are created.
- **Marketplace `metadata.version`** remains as an internal field in `.claude-plugin/marketplace.json`. It's bumped on catalog-shape changes (plugin added/removed, cross-plugin structural reshuffle) — but it's **not** tagged publicly and has no GitHub Release.
- **Root `CHANGELOG.md`** is historical; new version-specific entries go only into plugin CHANGELOGs (`plugins/ua/CHANGELOG.md`, `plugins/pl/CHANGELOG.md`). Monorepo-level tooling or structural notes can still land there as dated (not versioned) entries.

## Prerequisites

- `gh` CLI installed and authenticated (`gh auth status`).
- Write access to the repo.
- Clean `main` locally: `git checkout main && git pull`.

## 1. Decide the bump

Pick one plugin (`ua` or `pl`) and one version per semver.

Semver guidelines for `0.x`:

- **Patch** (`0.4.0 → 0.4.1`) — wording fixes, new skills or agents that don't break existing invocations, non-breaking internal refactors.
- **Minor** (`0.4.0 → 0.5.0`) — significant additions (new agent category, new skill set) or a breaking change during `0.x` pre-1.0.
- **Major** (`0.x → 1.0.0`) — not yet; reserved for first stable API commitment or a deliberate breaking restructure.

## 2. Update the version fields

For a release of plugin `<P>` (`ua` or `pl`) to version `X.Y.Z`, two fields move in lockstep — both must change:

```
plugins/<P>/.claude-plugin/plugin.json       → "version": "X.Y.Z"
.claude-plugin/marketplace.json              → "plugins[N].version": "X.Y.Z"   # N=0 for ua, 1 for pl
```

If this release also changes the marketplace catalog shape (e.g. adding or removing a plugin), also bump `marketplace.json` → `metadata.version`. For ordinary plugin-only releases, leave `metadata.version` alone.

Source of truth — [`.version-bump.json`](../.version-bump.json).

Validate after:

```bash
claude plugin validate .
```

Must report `✔ Validation passed`.

## 3. Add the CHANGELOG entry

Edit the CHANGELOG of the plugin you're releasing:

| Changelog | Language | When to edit |
|---|---|---|
| [`plugins/ua/CHANGELOG.md`](../plugins/ua/CHANGELOG.md) | Ukrainian | Every `ua` release. |
| [`plugins/pl/CHANGELOG.md`](../plugins/pl/CHANGELOG.md) | Polish | Every `pl` release. |
| [root `CHANGELOG.md`](../CHANGELOG.md) | English | **Only** for cross-cutting monorepo changes (tooling, structural reshuffle touching both plugins). Ordinary plugin releases do not touch this file. |

Every changelog follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Insert a new section at the top (right below the heading) and add a matching link reference at the bottom — pointing to the **per-plugin tag URL**.

### Plugin `plugins/ua/CHANGELOG.md` template (Ukrainian)

```markdown
## [X.Y.Z] — YYYY-MM-DD

### Added / Changed / Fixed / Removed

- **Короткий жирний заголовок** — конкретний опис. Посилатись на статті НПА (zakon.rada ID), рішення ВС, PR-номер.

### Migration

Only if breaking. Exact commands users need to run:

    /plugin marketplace update lawpowers
    /plugin uninstall ua@lawpowers
    /plugin install ua@lawpowers
    /reload-plugins

[X.Y.Z]: https://github.com/crankshift/lawpowers/releases/tag/ua/vX.Y.Z
```

### Plugin `plugins/pl/CHANGELOG.md` template (Polish)

```markdown
## [X.Y.Z] — YYYY-MM-DD

### Added / Changed / Fixed / Removed

- **Krótki pogrubiony nagłówek** — konkretny opis. Odwołania do ISAP, Portal Orzeczeń, sygnatur akt, numer PR.

[X.Y.Z]: https://github.com/crankshift/lawpowers/releases/tag/pl/vX.Y.Z
```

## 4. PR and merge

Open a feature branch, push, open a PR, merge.

```bash
git checkout -b release-<plugin>-vX.Y.Z           # e.g. release-ua-v0.5.0
git add -A
git commit -m "<plugin> vX.Y.Z: <headline>"
git push -u origin release-<plugin>-vX.Y.Z
gh pr create --base main --head release-<plugin>-vX.Y.Z \
  --title "<plugin> vX.Y.Z: <headline>" \
  --body "$(sed -n '/## \[X.Y.Z\]/,/## \[/p' plugins/<plugin>/CHANGELOG.md | sed '$d')"
```

Review. Merge the PR on GitHub (this repo enforces PR review — direct push to `main` is blocked).

## 5. Tag the merge commit and push

The tag name is `<plugin>/vX.Y.Z` — GitHub supports `/` in tag names.

```bash
git checkout main && git pull
MERGE_SHA=$(git rev-parse HEAD)
git tag -a "<plugin>/vX.Y.Z" "$MERGE_SHA" -m "<plugin> vX.Y.Z — <headline>"
git push origin "<plugin>/vX.Y.Z"
```

## 6. Create the GitHub Release

Release notes use the **plugin's** CHANGELOG section as the body (language of the plugin).

```bash
gh release create "<plugin>/vX.Y.Z" \
  --title "<plugin> vX.Y.Z — <headline>" \
  --notes-file <(awk '/## \[X.Y.Z\]/,/## \[/' plugins/<plugin>/CHANGELOG.md | sed '$d')
```

Flags:

- `--prerelease` — for `-rc.N` or similar.
- `--draft` — inspect the generated page before publishing.
- `--latest` — **skip** this flag in most cases. With two independent release lines, marking one as "latest" hides the other on the Releases page; let GitHub pick the latest by date automatically.

## 7. Verify

```bash
gh release view "<plugin>/vX.Y.Z" --json name,tagName,isLatest,url
```

Users with installed plugins pick up the new version with:

```
/plugin marketplace update lawpowers
/reload-plugins
```

Users with auto-update enabled for the `lawpowers` marketplace get it on their next Claude Code startup.

## Common pitfalls

- **Forgetting to bump `plugins[N].version` in the marketplace.** The plugin version is listed in two places; leaving one stale makes updates silently fail. Always grep for the old version after editing.
- **Tagging before the PR merges.** Tag the merge commit, not the last commit on the feature branch.
- **Omitting the link reference at the bottom of the plugin CHANGELOG.** The `[X.Y.Z]: https://…` line at the end is what makes the section title clickable.
- **Using an umbrella `vX.Y.Z` tag instead of `<plugin>/vX.Y.Z`.** Umbrella tags are retired — they caused the UX confusion that motivated this split. Always use the namespaced form.
- **Marking a plugin release as `--latest`.** With two release lines, this hides the sibling plugin's latest on the Releases page. Leave it off unless you really mean it.

## Bumping marketplace `metadata.version`

Needed only when the marketplace catalog itself changes shape (plugin added/removed, entries renamed, cross-cutting doc reshuffle). It is not tied to a git tag.

```bash
./scripts/release.sh bump-marketplace 0.7.0
```

Commit the change on a regular feature branch; no tag, no GitHub Release. The bump exists so Claude Code can detect catalog changes for `/plugin marketplace update`.

## Rolling back a release

If a release has a critical issue:

1. Publish a hotfix as a new patch version — don't delete the tag.
2. If the tag was pushed but the Release isn't public yet, delete the draft and the tag:
   ```bash
   gh release delete "<plugin>/vX.Y.Z" --yes
   git push origin ":refs/tags/<plugin>/vX.Y.Z"
   git tag -d "<plugin>/vX.Y.Z"
   ```
3. Never force-push to `main` to "undo" a merged release PR; always roll forward with a new patch.

## Related files

- [`scripts/release.sh`](../scripts/release.sh) — automates `bump`, `prepare` (bump + branch + PR), and `publish` (tag + GitHub Release) per plugin.
- [`plugins/ua/CHANGELOG.md`](../plugins/ua/CHANGELOG.md) — plugin `ua` history (Ukrainian).
- [`plugins/pl/CHANGELOG.md`](../plugins/pl/CHANGELOG.md) — plugin `pl` history (Polish).
- [`CHANGELOG.md`](../CHANGELOG.md) — historical umbrella log + monorepo-level notes (English).
- [`.version-bump.json`](../.version-bump.json) — inventory of versioned fields.
- [`CLAUDE.md`](../CLAUDE.md) — contributor guide with the abbreviated release section.
