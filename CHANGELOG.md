# lawpowers — Changelog

Index of per-plugin CHANGELOGs and a log of **monorepo-level** structural and tooling changes. Plugin content history lives with each plugin.

## Plugin history

- [`plugins/ua/CHANGELOG.md`](./plugins/ua/CHANGELOG.md) — plugin `ua` (Ukrainian law, written in Ukrainian). Tagged `ua/vX.Y.Z`.
- [`plugins/pl/CHANGELOG.md`](./plugins/pl/CHANGELOG.md) — plugin `pl` (Polish law, written in Polish). Tagged `pl/vX.Y.Z`.

For the release procedure, see [`docs/RELEASING.md`](./docs/RELEASING.md).

## Monorepo-level log

Entries below cover cross-cutting changes only (layout moves, release tooling, CI, shared scripts, repo renames). Plugin content changes — new agents, new skills, updated statute references — go in the plugin CHANGELOG, not here. The log is dated; there is no monorepo-level version anymore.

### 2026-04-21 — Per-plugin release tags

Releases are now cut per plugin with namespaced tags (`ua/vX.Y.Z`, `pl/vX.Y.Z`). The umbrella `vX.Y.Z` tag scheme is retired — it confused users who install plugins individually.

- Historical umbrella tags `v0.1.0`…`v0.5.0` remain on the repo as git tags and have GitHub Releases. `v0.6.0` was deleted in favour of the per-plugin tag `pl/v0.2.0` that covers the same state.
- Marketplace `metadata.version` stays as an internal field, bumped on catalog-shape changes. It is not publicly tagged.
- Release helper `scripts/release.sh` rewired for per-plugin flow (`bump <plugin> <version>`, `prepare`, `publish`). Separate `bump-marketplace` command for catalog-shape bumps.

PRs: #19 (tooling + docs switch), #20 (CHANGELOG link-ref cleanup).

### 2026-04-20 — Monorepo layout: `plugins/<code>/`

Plugin directories moved from repo root to a `plugins/` container:

- `ua/` → `plugins/ua/`
- `pl/` → `plugins/pl/`

Marketplace `plugins[N].source` paths updated accordingly (`"./ua"` → `"./plugins/ua"`, `"./pl"` → `"./plugins/pl"`). Namespace (`ua`, `pl`) and commands (`/ua:…`, `/pl:…`) unchanged.

Originally released as umbrella `v0.5.0`. Required reinstall:

```
/plugin marketplace update lawpowers
/plugin uninstall ua@lawpowers
/plugin install ua@lawpowers
/plugin uninstall pl@lawpowers   # if installed
/plugin install pl@lawpowers
/reload-plugins
```

### 2026-04-20 — Release tooling

Added [`scripts/release.sh`](./scripts/release.sh) — bash helper for bump / prepare / publish. Full manual in [`docs/RELEASING.md`](./docs/RELEASING.md). Originally released as umbrella `v0.4.2`.

### 2026-04-20 — Split CHANGELOGs

Single CHANGELOG split into three: this root file for monorepo/tooling, [`plugins/ua/CHANGELOG.md`](./plugins/ua/CHANGELOG.md) (Ukrainian), [`plugins/pl/CHANGELOG.md`](./plugins/pl/CHANGELOG.md) (Polish). Originally released as umbrella `v0.4.1`.

### 2026-04-20 — Monorepo conversion + plugin `pl` introduction

- Plugin `ua` moved from repo root to the `ua/` subdirectory; marketplace `source` changed `"./"` → `"./ua"`.
- Marketplace catalog now lists two plugins (`ua`, `pl`).
- Plugin `pl` added as a first release — see [`plugins/pl/CHANGELOG.md`](./plugins/pl/CHANGELOG.md) `[0.1.0]`.
- Root `CLAUDE.md` and `README.md` rewritten in English.
- `author` / `owner` fields across manifests changed `"Yurii"` → `"crankshift"`.

Plugin-level detail for `ua`: [`plugins/ua/CHANGELOG.md`](./plugins/ua/CHANGELOG.md) `[0.4.0]`. Originally released as umbrella `v0.4.0`. Required reinstall for `ua` users:

```
/plugin marketplace update lawpowers
/plugin uninstall ua@lawpowers
/plugin install ua@lawpowers
/reload-plugins
```

### 2026-04-20 — Rename cascade

Preparation for the monorepo — repo, marketplace, and plugin all renamed:

- GitHub repo: `crankshift/legal-ua` → `crankshift/lawpowers`.
- Marketplace name: `legal-ua` → `lawpowers`.
- Plugin identifier: `legal-ua` → `ua`.
- Command prefix: `/legal-ua:…` → `/ua:…`.

Plugin-level changes for `ua` (including the sonnet→inherit model switch) — [`plugins/ua/CHANGELOG.md`](./plugins/ua/CHANGELOG.md) `[0.3.0]`. Originally released as umbrella `v0.3.0`. Required reinstall:

```
/plugin uninstall legal-ua@legal-ua
/plugin marketplace remove legal-ua
/plugin marketplace add crankshift/lawpowers
/plugin install ua@lawpowers
/reload-plugins
```

### 2026-04-20 — Initial releases

- Umbrella `v0.1.0` — repo converted to an installable Claude Code plugin (`plugin.json` + `marketplace.json`). Plugin-level detail: [`plugins/ua/CHANGELOG.md`](./plugins/ua/CHANGELOG.md) `[0.1.0]`.
- Umbrella `v0.2.0` — military block for service members in ЗСУ added to plugin `ua`. Plugin-level detail: [`plugins/ua/CHANGELOG.md`](./plugins/ua/CHANGELOG.md) `[0.2.0]`.

## Historical umbrella release tags

These existed under the retired umbrella-tag scheme. They continue to resolve on GitHub as git tags and (mostly) as Releases; the per-plugin tags introduced on 2026-04-21 are the canonical way to link to a plugin version going forward.

| Tag | Date | What was shipped | Per-plugin pointer |
|---|---|---|---|
| `v0.5.0` | 2026-04-20 | Monorepo layout move (`plugins/` container). No plugin content change. | — (monorepo-structural) |
| `v0.4.2` | 2026-04-20 | Added `scripts/release.sh`. No plugin content change. | — (tooling) |
| `v0.4.1` | 2026-04-20 | Split CHANGELOGs. No plugin content change. | — (docs) |
| `v0.4.0` | 2026-04-20 | Monorepo conversion + plugin `pl` `[0.1.0]` + plugin `ua` `[0.4.0]`. | `ua` [`[0.4.0]`](./plugins/ua/CHANGELOG.md#040--2026-04-20), `pl` [`[0.1.0]`](./plugins/pl/CHANGELOG.md#010--2026-04-20) |
| `v0.3.0` | 2026-04-20 | Rename cascade + plugin `ua` `[0.3.0]` (model switch). | `ua` [`[0.3.0]`](./plugins/ua/CHANGELOG.md#030--2026-04-20) |
| `v0.2.0` | 2026-04-20 | Plugin `ua` `[0.2.0]` — military block. | `ua` [`[0.2.0]`](./plugins/ua/CHANGELOG.md#020--2026-04-20) |
| `v0.1.0` | 2026-04-20 | Plugin `ua` `[0.1.0]` — initial conversion. | `ua` [`[0.1.0]`](./plugins/ua/CHANGELOG.md#010--2026-04-20) |
| ~~`v0.6.0`~~ | ~~2026-04-21~~ | Plugin `pl` `[0.2.0]` — 7 new agents + 8 new skills. | **Replaced by** [`pl/v0.2.0`](https://github.com/crankshift/lawpowers/releases/tag/pl/v0.2.0) |

[v0.5.0]: https://github.com/crankshift/lawpowers/releases/tag/v0.5.0
[v0.4.2]: https://github.com/crankshift/lawpowers/releases/tag/v0.4.2
[v0.4.1]: https://github.com/crankshift/lawpowers/releases/tag/v0.4.1
[v0.4.0]: https://github.com/crankshift/lawpowers/releases/tag/v0.4.0
[v0.3.0]: https://github.com/crankshift/lawpowers/releases/tag/v0.3.0
[v0.2.0]: https://github.com/crankshift/lawpowers/releases/tag/v0.2.0
[v0.1.0]: https://github.com/crankshift/lawpowers/releases/tag/v0.1.0
