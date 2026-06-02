# lawpowers / ua — Codex guide

Codex plugin ID: `law-ua`. Claude Code plugin ID: `ua`.

Use this plugin for Ukrainian legal drafting, legal analysis, source lookup, and the military-law block. The working language is Ukrainian. Canonical UA sources live in `../../agents/ua` and `../../skills/ua` with `law-ua-*` names; plugin-local `agents/` and `skills/` are generated adapters/copies. Keep this Codex guide in sync with `CLAUDE.md` and `README.md`.

## Rules

- Verify statute text, court practice, procedural terms, fees, and military-law rules against primary sources before use.
- Primary sources include `zakon.rada.gov.ua`, `reyestr.court.gov.ua`, `supreme.court.gov.ua`, and `ccu.gov.ua`.
- Never fabricate case law, case numbers, dates, quotations, registry results, or official positions.
- Use placeholders for personal data: `[ПІБ]`, `[РНОКПП]`, `[адреса]`.
- Outputs are legal-document drafts for qualified human review, not final legal advice.
- For letters, requests, applications, and complaints to authorities, first route the document through `skills/law-ua-determining-ua-request-regime/SKILL.md`. Do not mix public-information requests, citizen appeals, administrative-procedure filings, administrative services, personal-data requests, and advocate requests in one document.

## Codex maintenance

- Canonical sources: `../../agents/ua/law-ua-*.md` and `../../skills/ua/law-ua-*/SKILL.md`.
- Generated Claude-compatible copies: `agents/*.md` and `skills/*/SKILL.md` in this plugin folder.
- Generated Codex agents: `.codex/agents/*.toml`.
- OpenCode installs this repository as a git package plugin; `../../package.json` points to `../../.opencode/plugins/lawpowers.js`, which exposes `../../skills/ua` and loads `../../agents/ua/law-ua-*.md`.
- After editing a canonical agent or skill, run the root adapter generation and validation commands from the repository root.
- Do not add an `agents` field to `.codex-plugin/plugin.json` unless Codex schema support is confirmed.
- Tool lists from Claude agents are carried into Codex instructions as guidance, not hard permission boundaries.
