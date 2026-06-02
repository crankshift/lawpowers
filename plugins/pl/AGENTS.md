# lawpowers / pl — Codex guide

Codex plugin ID: `law-pl`. Claude Code plugin ID: `pl`.

Use this plugin for Polish legal drafting, legal analysis, and official-source workflows. The working language is Polish. Canonical PL sources live in `../../agents/pl` and `../../skills/pl` with `law-pl-*` names; plugin-local `agents/` and `skills/` are generated adapters/copies. Keep this Codex guide in sync with `CLAUDE.md` and `README.md`.

## Rules

- Verify statute text, court practice, procedural terms, fees, and registry information against primary sources before use.
- Primary sources include `isap.sejm.gov.pl`, `dziennikustaw.gov.pl`, `orzeczenia.ms.gov.pl`, `sn.pl`, `nsa.gov.pl`, and `trybunal.gov.pl`.
- Never fabricate case law, case numbers, dates, quotations, registry results, or official positions.
- Use placeholders for personal data: `[imię i nazwisko]`, `[PESEL]`, `[NIP]`, `[adres]`.
- Outputs are legal-document drafts for qualified human review, not final legal advice.
- For letters, requests, applications, complaints, petitions, registry requests, RODO requests, and special-procedure filings, first route the document through `skills/law-pl-determining-pl-request-regime/SKILL.md`. Do not mix UDIP, KPA, PPSA, RODO, registry, tax, ZUS, cudzoziemcy, USC, and professional-letter regimes in one document.

## Codex maintenance

- Canonical sources: `../../agents/pl/law-pl-*.md` and `../../skills/pl/law-pl-*/SKILL.md`.
- Generated Claude-compatible copies: `agents/*.md` and `skills/*/SKILL.md` in this plugin folder.
- Generated Codex agents: `.codex/agents/*.toml`.
- OpenCode installs this repository as a git package plugin; `../../package.json` points to `../../.opencode/plugins/lawpowers.js`, which exposes `../../skills/pl` and loads `../../agents/pl/law-pl-*.md`.
- After editing a canonical agent or skill, run the root adapter generation and validation commands from the repository root.
- Do not add an `agents` field to `.codex-plugin/plugin.json` unless Codex schema support is confirmed.
- Tool lists from Claude agents are carried into Codex instructions as guidance, not hard permission boundaries.
