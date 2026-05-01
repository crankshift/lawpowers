# lawpowers — Codex contributor guide

This repository supports both Claude Code and Codex. Claude Code remains supported through `.claude-plugin/` manifests and `CLAUDE.md`; Codex support lives in `.agents/plugins/marketplace.json`, plugin-level `.codex-plugin/plugin.json`, and this `AGENTS.md` instruction file.

## Plugin map

| Jurisdiction | Claude plugin ID | Codex plugin ID | Folder | Language |
|---|---|---|---|---|
| Ukraine | `ua` | `law-ua` | `plugins/ua` | Ukrainian |
| Poland | `pl` | `law-pl` | `plugins/pl` | Polish |

Keep the existing folders and Claude IDs unchanged. Codex uses collision-safe IDs because Businesspowers also has `ua` and `pl` plugins.

## Repository rules

- One jurisdiction equals one plugin; do not mix UA and PL legal content inside one agent or skill.
- Plugin language matches jurisdiction: UA content in Ukrainian, PL content in Polish, root docs in English.
- `agents/` and `skills/` remain the source of truth for plugin behavior.
- When adding or renaming agents or skills, update the plugin README, `CLAUDE.md`, `AGENTS.md`, Claude manifest, and Codex manifest/marketplace when the public surface changes.
- Do not commit real personal or client data. Use placeholders such as `[ПІБ]`, `[РНОКПП]`, `[imię i nazwisko]`, and `[PESEL]`.
- Legal citations, court decisions, and procedural amounts must be verified against primary sources before use.

## Codex layout

- `.agents/plugins/marketplace.json` is the Codex marketplace catalog.
- `plugins/*/.codex-plugin/plugin.json` is the Codex plugin manifest.
- `AGENTS.md` files are Codex-facing contributor instructions.
- `CLAUDE.md` files remain Claude-facing contributor instructions.

## Verification

After changing Codex support, validate JSON manifests and verify each marketplace `source.path` points to a plugin folder with `.codex-plugin/plugin.json` and `skills/`.
