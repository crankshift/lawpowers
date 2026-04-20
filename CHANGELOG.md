# lawpowers — Changelog

Marketplace-level change log. Plugin-specific entries live alongside each plugin:

- [`ua/CHANGELOG.md`](./ua/CHANGELOG.md) — Ukrainian law plugin (written in Ukrainian).
- [`pl/CHANGELOG.md`](./pl/CHANGELOG.md) — Polish law plugin (written in Polish).

This root file covers:
- Marketplace version bumps (`.claude-plugin/marketplace.json:metadata.version`).
- Monorepo-level structural changes.
- Cross-cutting documentation and tooling.

For the release procedure see [`docs/RELEASING.md`](./docs/RELEASING.md).

Format — [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versioning — [SemVer](https://semver.org/spec/v2.0.0.html). Marketplace and individual plugin versions are tracked independently.

## [0.4.0] — 2026-04-20

### Changed — BREAKING (monorepo restructure)

- Plugin `ua` files moved from repo root to the `ua/` subdirectory. Marketplace `source` for `ua` changed from `"./"` to `"./ua"`.
- `marketplace.json` now lists two plugins: `ua` and `pl`.
- Root `CLAUDE.md` and `README.md` rewritten in English.
- `.version-bump.json` restructured for multi-plugin versioning.
- `author`/`owner` fields across all manifests changed `"Yurii"` → `"crankshift"`.

See [`ua/CHANGELOG.md`](./ua/CHANGELOG.md) for plugin-level details.

### Added — plugin `pl` v0.1.0

First release of the Polish law plugin. 10 agents, 6 skills. See [`pl/CHANGELOG.md`](./pl/CHANGELOG.md) for the full catalog.

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

Plugin-level changes (including the sonnet→inherit model switch) — see [`ua/CHANGELOG.md`](./ua/CHANGELOG.md).

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

Military block for service members in ЗСУ — 5 new agents and 4 new skills. Plugin-level details in [`ua/CHANGELOG.md`](./ua/CHANGELOG.md) under 0.2.0.

## [0.1.0] — 2026-04-20

### Added — initial plugin conversion

Repo converted to an installable Claude Code plugin with `plugin.json` and `marketplace.json`. Plugin-level details in [`ua/CHANGELOG.md`](./ua/CHANGELOG.md) under 0.1.0.

[0.4.0]: https://github.com/crankshift/lawpowers/releases/tag/v0.4.0
[0.3.0]: https://github.com/crankshift/lawpowers/releases/tag/v0.3.0
[0.2.0]: https://github.com/crankshift/lawpowers/releases/tag/v0.2.0
[0.1.0]: https://github.com/crankshift/lawpowers/releases/tag/v0.1.0
