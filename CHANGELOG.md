# lawpowers — Changelog

Marketplace-level change log. Plugin-specific entries live alongside each plugin:

- [`ua/CHANGELOG.md`](./plugins/ua/CHANGELOG.md) — Ukrainian law plugin (written in Ukrainian).
- [`pl/CHANGELOG.md`](./plugins/pl/CHANGELOG.md) — Polish law plugin (written in Polish).

This root file covers:
- Marketplace version bumps (`.claude-plugin/marketplace.json:metadata.version`).
- Monorepo-level structural changes.
- Cross-cutting documentation and tooling.

For the release procedure see [`docs/RELEASING.md`](./docs/RELEASING.md).

Format — [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versioning — [SemVer](https://semver.org/spec/v2.0.0.html). Marketplace and individual plugin versions are tracked independently.

## [0.5.0] — 2026-04-20

### Changed — BREAKING (marketplace layout)

- Plugin directories moved from repo root to a dedicated `plugins/` container:
  - `ua/` → `plugins/ua/`
  - `pl/` → `plugins/pl/`
- Marketplace `plugins[N].source` paths updated accordingly (`"./ua"` → `"./plugins/ua"`, `"./pl"` → `"./plugins/pl"`).
- `name` of each plugin is unchanged (`ua`, `pl`), so install commands stay as `/plugin install ua@lawpowers` and `/plugin install pl@lawpowers`. Command prefixes (`/ua:…`, `/pl:…`) are also unchanged.

All cross-references were updated across root docs, scripts, templates, and plugin-nested files:

- Root `README.md`, `CLAUDE.md` — layout diagrams and links.
- `.github/PULL_REQUEST_TEMPLATE.md` — CHANGELOG paths, `--plugin-dir` examples.
- `docs/RELEASING.md` — plugin-manifest paths in CHANGELOG templates.
- `scripts/release.sh` — hard-coded `UA_PLUGIN_JSON` / `PL_PLUGIN_JSON` / `*_CHANGELOG` paths.
- `.version-bump.json` — tracked file paths.
- `plugins/ua/*` and `plugins/pl/*` — relative links updated (`../README.md` → `../../README.md`, etc.); internal structure diagrams refreshed.

### Bumped

- Marketplace `metadata.version`: `0.4.2` → `0.5.0`. Plugin `version` fields untouched (`ua` stays `0.4.0`, `pl` stays `0.1.0`).

### Migration

```
/plugin marketplace update lawpowers
/plugin uninstall ua@lawpowers
/plugin install ua@lawpowers
/plugin uninstall pl@lawpowers   # if installed
/plugin install pl@lawpowers
/reload-plugins
```

Claude Code re-fetches the plugin from the new source path; namespace and commands remain identical.

### Rationale

A `plugins/` container makes room for non-plugin tooling at the repo root (CI workflows, shared config, evaluation harnesses) without scattering plugin content. Future jurisdictions go in `plugins/<code>/` alongside `ua` and `pl`.

## [0.4.2] — 2026-04-20

### Added — tooling

- `scripts/release.sh` — bash helper that automates the mechanical parts of the release flow: `bump`, `prepare` (bump + branch + PR), and `publish` (tag + GitHub Release). Safety checks for clean working tree, existing branch/tag, and `gh` auth. Runs `claude plugin validate` after every bump.
- `docs/RELEASING.md` got a TL;DR pointer to the new script plus cross-links in "Related files".

### Bumped

- Marketplace `metadata.version`: `0.4.1` → `0.4.2`. Plugin versions untouched.

No migration needed.

```
/plugin marketplace update lawpowers
/reload-plugins
```

## [0.4.1] — 2026-04-20

### Changed — documentation

Split the single CHANGELOG into three:

- Root `CHANGELOG.md` (English) — marketplace-level summaries with references.
- `ua/CHANGELOG.md` (Ukrainian) — detailed plugin-`ua` history, backfilled from v0.1.0.
- `pl/CHANGELOG.md` (Polish) — plugin-`pl` history, starting at v0.1.0.

`docs/RELEASING.md` updated with templates per language and an optional `gh release create` invocation that concatenates root + plugin CHANGELOG sections. `CLAUDE.md` and per-plugin `README.md` files link to the appropriate CHANGELOG first.

### Bumped

- Marketplace `metadata.version`: `0.4.0` → `0.4.1`. Plugin versions untouched (`ua` stays at `0.4.0`, `pl` at `0.1.0`) — no agent or skill changed.

No migration needed. Users just run:

```
/plugin marketplace update lawpowers
/reload-plugins
```

## [0.4.0] — 2026-04-20

### Changed — BREAKING (monorepo restructure)

- Plugin `ua` files moved from repo root to the `ua/` subdirectory. Marketplace `source` for `ua` changed from `"./"` to `"./ua"`.
- `marketplace.json` now lists two plugins: `ua` and `pl`.
- Root `CLAUDE.md` and `README.md` rewritten in English.
- `.version-bump.json` restructured for multi-plugin versioning.
- `author`/`owner` fields across all manifests changed `"Yurii"` → `"crankshift"`.

See [`ua/CHANGELOG.md`](./plugins/ua/CHANGELOG.md) for plugin-level details.

### Added — plugin `pl` v0.1.0

First release of the Polish law plugin. 10 agents, 6 skills. See [`pl/CHANGELOG.md`](./plugins/pl/CHANGELOG.md) for the full catalog.

### Added — documentation

- `ua/README.md`, `pl/README.md` — detailed per-plugin user docs in each plugin's working language.
- `ua/CLAUDE.md`, `pl/CLAUDE.md` — contributor context per plugin.
- `docs/RELEASING.md` — full release procedure with commands and pitfalls.

### Migration for `ua` users from 0.3.0

Plugin name and namespace (`ua`, `/ua:…`) are unchanged, but the marketplace `source` change requires reinstall:

```
/plugin marketplace update lawpowers
/plugin uninstall ua@lawpowers
/plugin install ua@lawpowers
/reload-plugins
```

## [0.3.0] — 2026-04-20

### Changed — BREAKING (rename cascade)

Preparation for the monorepo — the repo, marketplace, and plugin were all renamed:

- GitHub repo: `crankshift/legal-ua` → `crankshift/lawpowers`.
- Marketplace name: `legal-ua` → `lawpowers`.
- Plugin identifier: `legal-ua` → `ua`.
- Command prefix: `/legal-ua:…` → `/ua:…`.

Plugin-level changes (including the sonnet→inherit model switch) — see [`ua/CHANGELOG.md`](./plugins/ua/CHANGELOG.md).

### Migration for existing users

```
/plugin uninstall legal-ua@legal-ua
/plugin marketplace remove legal-ua
/plugin marketplace add crankshift/lawpowers
/plugin install ua@lawpowers
/reload-plugins
```

## [0.2.0] — 2026-04-20

### Added — plugin `legal-ua` (predecessor of `ua`)

Military block for service members in ЗСУ — 5 new agents and 4 new skills. Plugin-level details in [`ua/CHANGELOG.md`](./plugins/ua/CHANGELOG.md) under 0.2.0.

## [0.1.0] — 2026-04-20

### Added — initial plugin conversion

Repo converted to an installable Claude Code plugin with `plugin.json` and `marketplace.json`. Plugin-level details in [`ua/CHANGELOG.md`](./plugins/ua/CHANGELOG.md) under 0.1.0.

[0.5.0]: https://github.com/crankshift/lawpowers/releases/tag/v0.5.0
[0.4.2]: https://github.com/crankshift/lawpowers/releases/tag/v0.4.2
[0.4.1]: https://github.com/crankshift/lawpowers/releases/tag/v0.4.1
[0.4.0]: https://github.com/crankshift/lawpowers/releases/tag/v0.4.0
[0.3.0]: https://github.com/crankshift/lawpowers/releases/tag/v0.3.0
[0.2.0]: https://github.com/crankshift/lawpowers/releases/tag/v0.2.0
[0.1.0]: https://github.com/crankshift/lawpowers/releases/tag/v0.1.0
