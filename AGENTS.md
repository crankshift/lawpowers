# lawpowers — Codex contributor guide

This repository supports Claude Code, Codex, and OpenCode. Claude Code remains supported through `.claude-plugin/` manifests and `CLAUDE.md`; Codex support lives in `.agents/plugins/marketplace.json`, plugin-level `.codex-plugin/plugin.json`, and this `AGENTS.md` instruction file; OpenCode support lives in root `package.json` plus `.opencode/plugins/lawpowers.js` for git package installation.

## Plugin map

| Jurisdiction | Claude plugin ID | Codex plugin ID | Folder | Language |
|---|---|---|---|---|
| Ukraine | `ua` | `law-ua` | `plugins/ua` | Ukrainian |
| Poland | `pl` | `law-pl` | `plugins/pl` | Polish |

Keep the existing folders and Claude IDs unchanged. Codex uses collision-safe IDs because Businesspowers also has `ua` and `pl` plugins.

## Repository rules

- One jurisdiction equals one plugin; do not mix UA and PL legal content inside one agent or skill.
- Plugin language matches jurisdiction: UA content in Ukrainian, PL content in Polish, root docs in English.
- Top-level `agents/<jurisdiction>` and `skills/<jurisdiction>` are the source of truth for plugin behavior. Canonical agent and skill names are namespaced with `law-ua-` or `law-pl-`. Files under `plugins/*/agents`, `plugins/*/skills`, and `plugins/*/.codex/agents` are generated adapters.
- When adding or renaming agents or skills, update the plugin README, `CLAUDE.md`, `AGENTS.md`, Claude manifest, and Codex manifest/marketplace when the public surface changes.
- Do not commit real personal or client data. Use placeholders such as `[ПІБ]`, `[РНОКПП]`, `[imię i nazwisko]`, and `[PESEL]`.
- Legal citations, court decisions, and procedural amounts must be verified against primary sources before use.

## Codex layout

- `.agents/plugins/marketplace.json` is the Codex marketplace catalog.
- `plugins/*/.codex-plugin/plugin.json` is the Codex plugin manifest.
- `AGENTS.md` files are Codex-facing contributor instructions.
- `CLAUDE.md` files remain Claude-facing contributor instructions.
- `plugins/*/agents` and `plugins/*/skills` are generated Claude-compatible plugin copies derived from top-level canonical sources.
- `plugins/*/.codex/agents/*.toml` are generated Codex custom-agent shims derived from top-level canonical agent files.
- `package.json` exposes `.opencode/plugins/lawpowers.js` as the OpenCode package plugin entrypoint; that plugin anchors to the installed package root, exposes root `skills/ua` and `skills/pl`, and loads root `agents/ua` and `agents/pl` into OpenCode.
- Codex plugin manifests do not currently expose an `agents` field, so do not add one unless the schema changes; keep generated `.codex/agents/` files committed for compatibility/import workflows.

## Verification

After changing Codex support, validate JSON manifests and verify each marketplace `source.path` points to a plugin folder with `.codex-plugin/plugin.json` and `skills/`.

Run these after editing agents or Codex support:

```bash
python3 scripts/generate-claude-plugin-files.py
python3 scripts/convert-agents-to-codex.py
python3 scripts/validate-codex-agents.py
python3 scripts/validate-platform-adapters.py
```

Then validate JSON manifests with `python3 -m json.tool` and run the normal Claude plugin validation flow.
