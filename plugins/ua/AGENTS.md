# lawpowers / ua — Codex guide

Codex plugin ID: `law-ua`. Claude Code plugin ID: `ua`.

Use this plugin for Ukrainian legal drafting, legal analysis, source lookup, and the military-law block. The working language is Ukrainian. Keep `agents/` and `skills/` as the source of truth, and keep this Codex guide in sync with `CLAUDE.md` and `README.md`.

## Rules

- Verify statute text, court practice, procedural terms, fees, and military-law rules against primary sources before use.
- Primary sources include `zakon.rada.gov.ua`, `reyestr.court.gov.ua`, `supreme.court.gov.ua`, and `ccu.gov.ua`.
- Never fabricate case law, case numbers, dates, quotations, registry results, or official positions.
- Use placeholders for personal data: `[ПІБ]`, `[РНОКПП]`, `[адреса]`.
- Outputs are legal-document drafts for qualified human review, not final legal advice.

## Codex maintenance

- Codex manifest: `.codex-plugin/plugin.json`.
- Claude manifest: `.claude-plugin/plugin.json`.
- If agents or skills change, update both Codex and Claude docs where user-visible names or behavior changes.
- Generated Codex agents: `.codex/agents/*.toml`; source files: `agents/*.md`.
- After editing an agent, run `python3 scripts/convert-agents-to-codex.py` from the repo root, then `python3 scripts/validate-codex-agents.py`.
- Do not add an `agents` field to `.codex-plugin/plugin.json` unless Codex schema support is confirmed.
- Tool lists from Claude agents are carried into Codex instructions as guidance, not hard permission boundaries.
