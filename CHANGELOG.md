# lawpowers — Changelog

Unified Lawpowers package changelog. Jurisdiction changelogs capture component-level history, but public releases now use one package tag, `vX.Y.Z`.

## Component History

- [`plugins/ua/CHANGELOG.md`](./plugins/ua/CHANGELOG.md) — UA component history, written in Ukrainian.
- [`plugins/pl/CHANGELOG.md`](./plugins/pl/CHANGELOG.md) — PL component history, written in Polish.

For the release procedure, see [`docs/RELEASING.md`](./docs/RELEASING.md).

## [0.7.0] — 2026-06-02

### Added

- Added OpenCode git package support through root `package.json` and `.opencode/plugins/lawpowers.js`; OpenCode now loads canonical `skills/ua`, `skills/pl`, `agents/ua`, and `agents/pl` directly from the installed git package.
- Documented both project-scoped and global OpenCode installation in `README.md`, including restart and `opencode debug skill` verification guidance.

### Changed

- Lawpowers now uses one unified package/plugin version, `0.7.0`, across root `package.json`, marketplace metadata, Claude plugin manifests, Codex plugin manifests, and the marketplace plugin entries.
- Added/updated platform adapter validation so Claude-compatible copies, Codex shims, and OpenCode package loading stay tied to the top-level canonical sources.
- Generated Claude plugin adapter files and Codex custom-agent shims now use collision-safe `law-ua-*` / `law-pl-*` canonical names.

### Breaking

- Direct references to old generated adapter names such as `claim-drafter`, `request-drafter`, or `calculating-oplata-sadowa` should be updated to the corresponding `law-ua-*` or `law-pl-*` names.
- Local edits in generated Codex files under `plugins/*/.codex/agents` are not preserved; edit top-level canonical `agents/<jurisdiction>/law-*.md` and regenerate adapters instead.

### Migration

- Claude Code users should update the marketplace and reinstall affected plugins to clear stale generated adapter files.
- Codex users should run `codex plugin marketplace upgrade lawpowers`.
- OpenCode users should add `lawpowers@git+https://github.com/crankshift/lawpowers.git` to project or global `opencode.jsonc`, restart OpenCode, then verify with `opencode debug skill`.

## Older Monorepo-Level Log

### 2026-05-01 — Codex agent compatibility

- `ua` bumped to `0.6.2`: generated Codex custom-agent TOML files from the existing Claude agents.
- `pl` bumped to `0.4.2`: same Codex custom-agent compatibility layer.
- Added `scripts/convert-agents-to-codex.py` and `scripts/validate-codex-agents.py` for keeping Claude and Codex agent artifacts in sync.
- Marketplace `metadata.version` bumped to `0.6.2`.

### 2026-05-01 — Codex support

- `ua` bumped to `0.6.1`: Codex marketplace/manifest support, `AGENTS.md`, and Codex install docs.
- `pl` bumped to `0.4.1`: same Codex support.
- Marketplace `metadata.version` bumped to `0.6.1`.

Entries below cover older cross-cutting changes only (layout moves, release tooling, CI, shared scripts, repo renames). Plugin content changes — new agents, new skills, updated statute references — live in the component changelogs.

### 2026-04-21 — Per-plugin release tags

Per-plugin namespaced tags (`ua/vX.Y.Z`, `pl/vX.Y.Z`) were introduced here and later retired for `v0.7.0` in favor of one unified Lawpowers package tag, `vX.Y.Z`.

- Historical umbrella tags `v0.1.0`…`v0.5.0` remain on the repo as git tags and have GitHub Releases. `v0.6.0` was deleted in favour of the per-plugin tag `pl/v0.2.0` that covered the same state at the time.
- Marketplace `metadata.version` was temporarily treated as an internal field. As of `v0.7.0`, it follows the unified package version.
- Release helper `scripts/release.sh` was temporarily rewired for per-plugin flow and was later restored to unified package releases.

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

## Historical Release Tags

These tags predate the current unified `vX.Y.Z` release model or belong to the retired per-plugin experiment. They remain listed for history.

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

[0.7.0]: https://github.com/crankshift/lawpowers/releases/tag/v0.7.0
[v0.5.0]: https://github.com/crankshift/lawpowers/releases/tag/v0.5.0
[v0.4.2]: https://github.com/crankshift/lawpowers/releases/tag/v0.4.2
[v0.4.1]: https://github.com/crankshift/lawpowers/releases/tag/v0.4.1
[v0.4.0]: https://github.com/crankshift/lawpowers/releases/tag/v0.4.0
[v0.3.0]: https://github.com/crankshift/lawpowers/releases/tag/v0.3.0
[v0.2.0]: https://github.com/crankshift/lawpowers/releases/tag/v0.2.0
[v0.1.0]: https://github.com/crankshift/lawpowers/releases/tag/v0.1.0
